import csv
import os
import json
import re
import random
import time
from groq import Groq

import g

import util
import utils_ai
import prompts
import datetime




def get_common_name(latin_name):
    filepath = 'database/tables/plants.csv'
    rows = util.csv_get_rows_by_entity(filepath, latin_name)
    common_name = [row[1] for row in rows][0].strip()
    return common_name





plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]
cols = {}
for i, item in enumerate(plants[0]):
    cols[item] = i
plants = plants[1:g.ARTICLES_NUM+1]



def date_now():
    return datetime.datetime.now().date()


def ai_list_to_csv(entity, reply):
    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' in line: continue

        if not line[0].isdigit(): continue
        if '. ' in line: line = '. '.join(line.split('. ')[1:]).strip()
        else: continue
        if line == '': continue

        if '(' in line: line = line.split('(')[0].strip()
        # if ',' in line: line = line.split(',')[0].strip()

        if line.endswith('.'): line = line[0:-1]

        reply_formatted.append([entity, line])
    return reply_formatted


def reply_to_paragraphs(reply):
    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' in line: 
            tmp_line = line.split(':')[1]
            if tmp_line.strip() == '': continue
        if len(line.strip().split(' ')) <= 16: continue
        reply_formatted.append(line)
    return reply_formatted
    

def reply_to_list_2(reply):
    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue

        if not line[0].isdigit(): continue
        if '. ' in line: line = line.split('. ')[1]
        else: continue
        if ':' in line: line = line.split(':')[0]
        if '(' in line: line = line.split('(')[0]

        line = line.strip()
        if line == '': continue
        
        # if len(line.strip().split(' ')) <= 10: continue

        reply_formatted.append(line)
    return reply_formatted


def reply_remove_aka(reply, common_name):
    reply = reply.replace(f', also known as {common_name.lower()},', '')
    reply = reply.replace(f', also known as {common_name.title()},', '')
    reply = reply.replace(f', also known as {common_name.capitalize()},', '')
    return reply



#######################################################################
# ENTITY (root article)
#######################################################################

def ai_entity(json_filepath, section, paragraph_num, prompt, aka=True, save=True):
    var_val = []
    var_name = f'{section}'

    data = util.json_read(json_filepath)

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != []: return
    
    reply = utils_ai.gen_reply(prompt)
    if reply != '': 
        if not aka: 
            reply = reply_remove_aka(reply, data['common_name'])
            if "also known as" in reply:
                chunks = reply.split(',')
                reply = chunks[0] + ', '.join(chunks[2:])
        reply = reply_to_paragraphs(reply)

        print(len(reply))
        if len(reply) == paragraph_num:
            p = reply
            print('***************************************')
            print(p)
            print('***************************************')
            data[var_name] = p
            data['lastmod'] = str(date_now())
            if save: util.json_write(json_filepath, data)
            else: print('### NOT SAVED - TEST MODE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    time.sleep(30)


def ai_entity_main():
    plants_primary = [row for row in util.csv_get_rows('database/tables/plants.csv')[1:]]
    plants_secondary = [row for row in util.csv_get_rows('database/tables/plants-secondary.csv')[1:]]
    
    plants = []
    for plant in plants_primary: plants.append(plant)
    for plant in plants_secondary: plants.append(plant)

    for index, plant in enumerate(plants):
        print(index, '-', len(plants), '>>', plant)

        latin_name = plant[0].strip().capitalize()
        common_name = plant[1].strip().title()

        entity = latin_name.lower().replace(' ', '-')
        json_filepath = f'database/articles/plants/{entity}.json'

        data = util.json_read(json_filepath)
        data['entity'] = entity
        data['url'] = f'{entity}'
        data['latin_name'] = latin_name
        data['common_name'] = common_name
        data['title'] = f'What to know before using {latin_name} ({common_name})?'
        util.json_write(json_filepath, data)

        # INTRO
        for prompt in prompts.entity_intro:
            prompt = prompt.replace('[latin_name]', latin_name)
            ai_entity(json_filepath, 'intro_desc', 1, prompt)

        # MEDICINE
        for prompt in prompts.entity_medicine:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'medicine_intro', 1, prompt, aka=False, save=True)

        # for prompt in prompts.entity_benefits:
        #     prompt = prompt.replace('[latin_name]', latin_name)
        #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
        #     ai_entity(json_filepath, 'benefits', 1, prompt, aka=False)
        # for prompt in prompts.entity_constituents:
        #     prompt = prompt.replace('[latin_name]', latin_name)
        #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
        #     ai_entity(json_filepath, 'constituents', 1, prompt, aka=False)
        # for prompt in prompts.entity_preparations:
        #     prompt = prompt.replace('[latin_name]', latin_name)
        #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
        #     ai_entity(json_filepath, 'preparations', 1, prompt, aka=False, save=True)
        # for prompt in prompts.entity_side_effects:
        #     prompt = prompt.replace('[latin_name]', latin_name)
        #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
        #     ai_entity(json_filepath, 'side_effects', 1, prompt, aka=False, save=True)
        # for prompt in prompts.entity_precautions:
        #     prompt = prompt.replace('[latin_name]', latin_name)
        #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
        #     ai_entity(json_filepath, 'precautions', 1, prompt, aka=False, save=True)
        
        # HORTICULTURE
        for prompt in prompts.entity_horticulture_intro:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'horticulture_intro', 1, prompt, aka=False, save=True)
        for prompt in prompts.entity_horticulture_paragraphs:
            prompt = prompt.replace('[latin_name]', latin_name)
            ai_entity(json_filepath, 'horticulture_desc', 5, prompt)

        # BOTANY
        for prompt in prompts.entity_botany_intro:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'botany_intro', 1, prompt, aka=False, save=True)
        for prompt in prompts.entity_botany_paragraphs:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'botany_desc', 5, prompt, aka=False, save=True)

        # HISTORY
        for prompt in prompts.entity_history_intro:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'history_intro', 1, prompt, aka=False, save=True)
        for prompt in prompts.entity_history_paragraphs:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'history_desc', 5, prompt, aka=False, save=True)




#######################################################################
# MEDICINE
#######################################################################

def ai_medicine_section_text(entity, section, prompt):
    section_underscore = section.lower().strip().replace(' ', '_')
    section_dash = section.lower().strip().replace(' ', '-')
    var_val = ''
    var_name = f'{section_underscore}_text'

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '':  return

    rows = util.csv_get_rows_by_entity(f'database/tables/{section_dash}.csv', entity)
    lst = [row[1] for row in rows]
    lst = ', '.join(lst)

    prompt = prompt.replace('<lst>', lst)

    
    reply = utils_ai.gen_reply(prompt)
    reply = reply.replace(f', also known as {common_name.lower()},', '')
    reply = reply.replace(f', also known as {common_name.title()},', '')
    reply = reply.replace(f', also known as {common_name.capitalize()},', '')
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_section_list(entity, section, prompt):
    section_underscore = section.lower().strip().replace(' ', '_')
    section_dash = section.lower().strip().replace(' ', '-')
    var_val = []
    var_name = f'{section_underscore}_list'
    lst_num = 10

    filepath_in = f'database/tables/{section_dash}.csv'
    filepath_out = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath_out)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != []: return
    
    rows = [row[1] for row in util.csv_get_rows_by_entity(filepath_in, entity)]
    lst = ''.join(f'{i+1}. {row}\n' for i, row in enumerate(rows[:lst_num]))

    prompt = prompt.replace('<lst>', lst)
      
    
    reply = utils_ai.gen_reply(prompt)
    
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if ':' not in line: continue
        if '. 'not in line: continue
        if not reply.endswith('.'): reply += '.'
        line = line.strip()
        reply_formatted.append(line)

    if len(reply_formatted) == lst_num:
        print('***************************************')
        for paragraph in reply_formatted:
            print(paragraph)
        print('***************************************')

        data[var_name] = reply_formatted
        util.json_write(filepath_out, data)

    time.sleep(30)


def ai_medicine_benefits_description_list_csv(entity):
    running = False

    filepath = 'database/tables/benefits.csv'
    rows = util.csv_get_rows(filepath)
    
    if rows == []: return running

    for i, row in enumerate(rows):
        if row[0].strip() != entity: continue

        entity = row[0].strip()
        benefit = row[1].strip().lower()
        description = row[2].strip()
        latin_name = entity.replace('-', ' ').capitalize()
        common_name = get_common_name(latin_name)

        if description != '': continue

        running = True

        starting_text = f'{latin_name} {benefit} '
        prompt = f'''
            Explain in 1 sentence in detail why {latin_name} {benefit}.
            Start with these words: {starting_text}
        '''     
        
        reply = utils_ai.gen_reply(prompt)
        reply = starting_text + reply.strip()

        reply_formatted = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            if not reply.endswith('.'): continue
            reply_formatted.append(line)

        if len(reply_formatted) == 1:
            print('***************************************')
            for paragraph in reply_formatted:
                print(paragraph)
            print('***************************************')

            rows[i][2] = reply_formatted[0]
            util.csv_set_rows(filepath, rows)

        time.sleep(30)
        return running
    return running


def ai_medicine_intro(entity, filepath):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    var_val = ''
    var_name = 'intro'
    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '': return

    prompt = f'''
        Write a 5-sentence paragraph about the medicinal aspects of {latin_name}.
        In sentence 1, write the benefits of {latin_name}.
        In sentence 2, write the constituents of {latin_name}.
        In sentence 3, write the preparations of {latin_name}.
        In sentence 4, write the side effects of {latin_name}.
        In sentence 5, write the precautions of {latin_name}.
    '''     
    reply = utils_ai.gen_reply(prompt)
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_main(plants='primary'):
    plants = []
    if plants == 'primary':
        plants_primary = [row for row in util.csv_get_rows('database/tables/plants.csv')[1:]]
        for plant in plants_primary: plants.append(plant)
    elif plants == 'secondary':
        plants_secondary = [row for row in util.csv_get_rows('database/tables/plants-secondary.csv')[1:]]
        for plant in plants_secondary: plants.append(plant)
    elif plants == 'primary_secondary':
        plants_primary = [row for row in util.csv_get_rows('database/tables/plants.csv')[1:]]
        for plant in plants_primary: plants.append(plant)
        plants_secondary = [row for row in util.csv_get_rows('database/tables/plants-secondary.csv')[1:]]
        for plant in plants_secondary: plants.append(plant)
    else: return

    for index, plant in enumerate(plants):
        print(index, '-', len(plants), '>>', plant)

        latin_name = plant[0].strip().capitalize()
        common_name = plant[1].strip().title()

        entity = latin_name.lower().replace(' ', '-')
        json_filepath = f'database/articles/plants/{entity}/medicine.json'

        data = util.json_read(filepath)
        data['entity'] = entity
        data['url'] = f'{entity}/medicine'
        data['latin_name'] = latin_name
        data['common_name'] = common_name
        data['title'] = f'{latin_name} ({common_name}) Medicinal Guide'
        util.json_write(filepath, data)

        # ai_medicine_intro(entity, filepath)

        # INTRO        
        for prompt in prompts.entity_medicine_intro:
            prompt = prompt.replace('[latin_name]', latin_name)
            ai_entity(json_filepath, 'intro', 1, prompt)

        # ai_medicine_section_text(entity, 'benefits', 
        #     f'''
        #         Explain in a 5-sentence paragraph the following health benefits of {latin_name}: <lst>.
        #         Start with these words: {latin_name}, also known as {common_name.lower()}, has several health benefits, such as '
        #     '''
        # )
        # ai_medicine_section_list(entity, 'benefits', 
        #     f'''
        #         Write a 1 sentence description for each benefit of {latin_name} in the following list: \n<lst>
        #         Answer in a ordered list using the following format. benefit: description.
        #     '''  
        # ) 
        
        # ai_medicine_section_text(entity, 'constituents', 
        #     f'''
        #         Explain in a 5-sentence paragraph the following medicinal constituents of {latin_name}: <lst>.
        #         Start with these words: {latin_name}, also known as {common_name.lower()}, has several active constituents, such as '
        #     '''   
        # )
        # ai_medicine_section_list(entity, 'constituents', 
        #     f'''
        #         Write a 1 sentence description for each medicinal constituent of {latin_name} in the following list: \n<lst>
        #         Answer in a ordered list using the following format. constituent: description.
        #     '''
        # ) 

        # prompt = f'''
        #     Explain in a 5-sentence paragraph the following medicinal preparations of {latin_name}: <lst>.
        #     Start with these words: {latin_name}, also known as {common_name.lower()}, has several medicinal preparations, such as '
        # '''
        # ai_medicine_section_text(entity, 'preparations', prompt)
        # prompt = f'''
        #     Write a 1 sentence description for each medicinal preparation of {latin_name} in the following list: \n<lst>
        #     Answer in a ordered list using the following format. preparation: description.
        # '''    
        # ai_medicine_section_list(entity, 'preparations', prompt) 

        # prompt = f'''
        #     Explain in a 5-sentence paragraph the following possible side effects of {latin_name}: <lst>.
        #     Start with these words: {latin_name}, also known as {common_name.lower()}, can have side effects if used improperly, '
        # '''   
        # ai_medicine_section_text(entity, 'side effects', prompt)
        # prompt = f'''
        #     Write a 1 sentence description for each possible side effect of {latin_name} in the following list: \n<lst>
        #     Answer in a ordered list using the following format. side effect: description.
        # '''  
        # ai_medicine_section_list(entity, 'side effects', prompt) 

        # prompt = f'''
        #     Explain in a 5-sentence paragraph the following precautions when using {latin_name} for medicinal purposes: <lst>.
        #     Start with these words: Before using {latin_name} it\'s important to take some precautions, such as '
        # '''     
        # ai_medicine_section_text(entity, 'precautions', prompt)
        # prompt = f'''
        #     Write a 1 sentence description for each of the following precaution you should take when using {latin_name} for medicinal purposes: \n<lst>
        #     Answer in a ordered list using the following format. precaution: description.
        # '''   
        # ai_medicine_section_list(entity, 'precautions', prompt) 





        # ai_medicine_intro(entity)
        # ai_medicine_benefits_text(entity)
        # ai_medicine_benefits_list(entity)
        # ai_medicine_constituents_text(entity)
        # ai_medicine_constituents_list(entity)
        # ai_medicine_preparations_text(entity)
        # ai_medicine_preparations_list(entity)
        # ai_medicine_side_effects_text(entity)
        # ai_medicine_side_effects_list(entity)
        # ai_medicine_precautions_text(entity)
        # ai_medicine_precautions_list(entity)





#######################################################################
# BENEFITS
#######################################################################

def ai_benefits_intro(entity):
    var_val = ''
    var_name = 'intro'
    
    filepath = f'database/articles/plants/{entity}/medicine/benefits.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']
    
    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '': return

    prompt = f'''
        Write a 5-sentence paragraph about the medicinal benefits of {latin_name}.
    '''     
    
    reply = utils_ai.gen_reply(prompt)
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_benefits_section(filepath, csv_benefits):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    benefits = []
    try: benefits = data['benefits']
    except: data['benefits'] = benefits
    if benefits != []: return

    benefits_tmp = []
    for benefit in csv_benefits:
        benefits_tmp.append({'benefit_name': benefit})
    
    data['benefits'] = benefits_tmp
    util.json_write(filepath, data)


def ai_benefits_description(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']
    benefits = data['benefits']

    for benefit in benefits:
        benefit_name = benefit['benefit_name']
        
        benefit_desc = ''
        try: benefit_desc = benefit['benefit_desc']
        except: benefit['benefit_desc'] = benefit_desc

        if benefit_desc != '': continue
        running = True

        starting_text = f'{common_name.title()} {benefit_name.lower()}, meaning '
        prompt = f'''
                Write a 5-sentence paragraph about this health benefit of {latin_name.capitalize()} ({common_name}): {benefit_name}.
                In sentence 1, write a detailed definition of "{latin_name.capitalize()} {benefit_name}". Start this sentence with these words: {starting_text}.
                In sentence 2, write what are the main active constituents of {latin_name.capitalize()} that give this benefit.
                In sentence 3, write what are the primary parts of the {latin_name.capitalize()} plant that give this benefit.
                In sentence 4, write what are the main medicinal preparations of {latin_name.capitalize()} that give this benefit.
                In sentence 5, write what are the main health conditions that this benefit of {latin_name.capitalize()} helps relieve.
            '''
        
        reply = utils_ai.gen_reply(prompt)
        paragraphs_filtered = reply_to_paragraphs(reply)
        
        if len(paragraphs_filtered) == 1:
            p = paragraphs_filtered[0]
            print('***************************************')
            print(p)
            print('***************************************')

            benefit['benefit_desc'] = p
            util.json_write(filepath, data)
        
        time.sleep(30)

    return running


def ai_benefits_constituents(filepath):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    benefits = []
    try: benefits = data['benefits']
    except: return

    for benefit in benefits[:10]:
        benefit_name = benefit['benefit_name']
        
        var_val = ''
        var_name = 'constituents_list'
        try: var_val = benefit[var_name]
        except: benefit[var_name] = var_val
        if var_val != '': continue

        prompt = f'''
            Write a numbered list about 10 active constituents contained in {latin_name} that helps with {benefit_name}. 
            Write only the names of the constituents, not the descriptions.
            Write only 1 constituent per line.
            Write only constituents with short names.
            Write only constituents that don't include numbers in the names.
        '''
        
        reply = utils_ai.gen_reply(prompt)
        paragraphs_filtered = reply_to_list_2(reply)
        
        if len(paragraphs_filtered) >= 5:
            print('***************************************')
            print(paragraphs_filtered)
            print('***************************************')

            benefit[var_name] = paragraphs_filtered
            util.json_write(filepath, data)
        
        time.sleep(30)


def ai_benefits_main():
    benefits_num = 10

    for index, plant in enumerate(plants):
        print(index, '-', len(plants), '>>', plant[0])

        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')
        url = f'{entity}/medicine/benefits'
        csv_benefits = [row[1] for row in util.csv_get_rows_by_entity('database/tables/benefits.csv', entity)[:benefits_num]]

        filepath = f'database/articles/plants/{url}.json'
        data = util.json_read(filepath)
        data['entity'] = entity
        data['url'] = url
        data['latin_name'] = latin_name
        data['common_name'] = common_name
        data['title'] = f'10 Best Health Benefits of {latin_name} ({common_name})'
        util.json_write(filepath, data)

        ai_benefits_intro(entity)

        # ai_benefits_section(filepath, csv_benefits)
        # ai_benefits_description(filepath)
        # ai_benefits_constituents(filepath)
        





#######################################################################
# CONSTITUENTS
#######################################################################

def ai_constituents_intro(entity):
    var_val = ''
    var_name = 'intro'
    
    filepath = f'database/articles/plants/{entity}/medicine/constituents.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']
    
    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '': return

    prompt = f'''
        Write a 5-sentence paragraph about the active constituents of {latin_name} for medicinal purposes.
    '''     
    
    reply = utils_ai.gen_reply(prompt)
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_constituents_sections_csv_to_json(filepath, csv_rows):
    var_val = []
    var_name_p = 'constituents'
    var_name_s = 'constituent'

    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name_p]
    except: data[var_name_p] = var_val
    if var_val != []: return

    lst = [{f'{var_name_s}_name': csv_row} for csv_row in csv_rows]
    
    data[var_name_p] = lst
    util.json_write(filepath, data)


def ai_constituents_sections_description(filepath):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']
    constituents = data['constituents']

    for item in constituents:
        constituent_name = item['constituent_name']
        
        var_val = ''
        var_name = 'constituent_desc'
        try: var_val = item[var_name]
        except: item[var_name] = var_val
        if var_val != '': continue

        starting_text = f'The {constituent_name.lower()} contained in {latin_name.title()}, also known as {common_name.lower()}, is '
        prompt = f'''
                Write a 5-sentence paragraph about this active constituent of {latin_name.capitalize()} ({common_name}): {constituent_name}.
                In sentence 1, write a detailed definition of "{latin_name.capitalize()} {constituent_name}". Start this sentence with these words: {starting_text}.
                In sentence 2, write what are the main medicinal properties of this {latin_name.capitalize()} constituent.
                In sentence 3, write what are the main health conditions this {latin_name.capitalize()} constituent help relieve.
                In sentence 4, write what are the main parts of the {latin_name.capitalize()} plant that have this constituent.
                In sentence 5, write what are the some possible side effect of this {latin_name.capitalize()} constituent if used improperly.
                Don't add new empty lines between sentences.
            '''
        

        running = True
        while running:
            try:
                reply = utils_ai.gen_reply(prompt)
                running = False
            except:
                time.sleep(300)

        reply = reply.replace(f', also known as {common_name.lower()},', '')
        reply = reply.replace(f', also known as {common_name.title()},', '')
        reply = reply.replace(f', also known as {common_name.capitalize()},', '')
        paragraphs_filtered = reply_to_paragraphs(reply)
        
        if len(paragraphs_filtered) == 1:
            p = paragraphs_filtered[0]
            print('***************************************')
            print(p)
            print('***************************************')

            item[var_name] = p
            util.json_write(filepath, data)
        
        time.sleep(30)


def ai_constituents_main():
    sections_num = 10
    article_type = 'constituents'

    for index, plant in enumerate(plants):
        print(index, '-', len(plants), '>>', plant[0])

        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')
        url = f'{entity}/medicine/constituents'
        csv_rows = [row[1] for row in util.csv_get_rows_by_entity('database/tables/constituents.csv', entity)[:sections_num]]

        filepath = f'database/articles/plants/{url}.json'
        data = util.json_read(filepath)
        data['entity'] = entity
        data['url'] = url
        data['latin_name'] = latin_name
        data['common_name'] = common_name
        data['title'] = f'10 Best Active Constituents of {latin_name} ({common_name})'
        util.json_write(filepath, data)

        # ai_constituents_intro(entity)

        # ai_constituents_sections_csv_to_json(filepath, csv_rows)
        ai_constituents_sections_description(filepath)
        # ai_benefits_constituents(filepath)
        




#######################################################################
# PREPARATIONS
#######################################################################

def ai_preparations_intro(entity):
    var_val = ''
    var_name = 'intro'
    
    filepath = f'database/articles/plants/{entity}/medicine/preparations.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']
    
    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '': return

    prompt = f'''
        Write a 5-sentence paragraph about the medicinal preparations of {latin_name} (ex. tisane and tincture).
    '''     
    
    reply = utils_ai.gen_reply(prompt)
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_preparations_sections_csv_to_json(filepath, csv_rows):
    var_val = []
    var_name_p = 'preparations'
    var_name_s = 'preparation'

    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name_p]
    except: data[var_name_p] = var_val
    if var_val != []: return

    lst = [{f'{var_name_s}_name': csv_row} for csv_row in csv_rows]
    
    data[var_name_p] = lst
    util.json_write(filepath, data)


def ai_preparations_sections_description(filepath):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']
    preparations = data['preparations']

    for item in preparations:
        preparation_name = item['name']
        
        var_val = ''
        var_name = 'desc'
        try: var_val = item[var_name]
        except: item[var_name] = var_val
        if var_val != '': continue

        starting_text = f'{latin_name.title()} {preparation_name.lower()} is '
        prompt = f'''
                Write 1 paragraph in 5 sentences about this medicinal preparations of {latin_name.capitalize()} ({common_name}): {preparation_name}.
                In sentence 1, write a detailed definition of "{latin_name.capitalize()} {preparation_name}". Start this sentence with these words: {starting_text}.
                In sentence 2, write what are the main health benefits of this {latin_name.capitalize()} preparation.
                In sentence 3, write what are the main plant parts used for this {latin_name.capitalize()} preparation.
                In sentence 4, write how to make this {latin_name.capitalize()} preparation.
                In sentence 5, write what are the main precautions to take when using this {latin_name.capitalize()} preparation.
                Don't add new empty lines between sentences.
            '''
        

        running = True
        while running:
            try:
                reply = utils_ai.gen_reply(prompt)
                running = False
            except:
                time.sleep(300)

        reply = reply.replace(f', also known as {common_name.lower()},', '')
        reply = reply.replace(f', also known as {common_name.title()},', '')
        reply = reply.replace(f', also known as {common_name.capitalize()},', '')
        paragraphs_filtered = reply_to_paragraphs(reply)
        
        if len(paragraphs_filtered) == 1:
            p = paragraphs_filtered[0]
            print('***************************************')
            print(p)
            print('***************************************')

            item[var_name] = p
            util.json_write(filepath, data)
        
        time.sleep(30)


def ai_preparations_main():
    sections_num = 10
    article_type = 'preparations'

    for index, plant in enumerate(plants):
        print(index, '-', len(plants), '>>', plant[0])

        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')
        url = f'{entity}/medicine/preparations'
        csv_rows = [row[1] for row in util.csv_get_rows_by_entity('database/tables/preparations.csv', entity)[:sections_num]]

        filepath = f'database/articles/plants/{url}.json'
        data = util.json_read(filepath)
        data['entity'] = entity
        data['url'] = url
        data['latin_name'] = latin_name
        data['common_name'] = common_name
        data['title'] = f'10 Best Medicinal Preparations of {latin_name} ({common_name})'
        util.json_write(filepath, data)

        ai_preparations_intro(entity)
        ai_preparations_sections_csv_to_json(filepath, csv_rows)
        ai_preparations_sections_description(filepath)
        




#######################################################################
# SIDE EFFECTS
#######################################################################

def ai_side_effects_intro(entity):
    var_val = ''
    var_name = 'intro'
    
    filepath = f'database/articles/plants/{entity}/medicine/side-effects.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']
    
    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '': return

    prompt = f'''
        Write a 5-sentence paragraph about the possible health side effects of {latin_name} if used improperly.
    '''     
    
    reply = utils_ai.gen_reply(prompt)
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_side_effects_sections_csv_to_json(filepath, csv_rows):
    var_val = []
    var_name_p = 'preparations'
    var_name_s = 'preparation'

    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name_p]
    except: data[var_name_p] = var_val
    if var_val != []: return

    lst = [{f'{var_name_s}_name': csv_row} for csv_row in csv_rows]
    
    data[var_name_p] = lst
    util.json_write(filepath, data)


def ai_side_effects_sections_description(filepath):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']
    preparations = data['preparations']

    for item in preparations:
        preparation_name = item['name']
        
        var_val = ''
        var_name = 'desc'
        try: var_val = item[var_name]
        except: item[var_name] = var_val
        if var_val != '': continue

        starting_text = f'{latin_name.title()} {preparation_name.lower()} is '
        prompt = f'''
                Write 1 paragraph in 5 sentences about this medicinal preparations of {latin_name.capitalize()} ({common_name}): {preparation_name}.
                In sentence 1, write a detailed definition of "{latin_name.capitalize()} {preparation_name}". Start this sentence with these words: {starting_text}.
                In sentence 2, write what are the main health benefits of this {latin_name.capitalize()} preparation.
                In sentence 3, write what are the main plant parts used for this {latin_name.capitalize()} preparation.
                In sentence 4, write how to make this {latin_name.capitalize()} preparation.
                In sentence 5, write what are the main precautions to take when using this {latin_name.capitalize()} preparation.
                Don't add new empty lines between sentences.
            '''
        

        running = True
        while running:
            try:
                reply = utils_ai.gen_reply(prompt)
                running = False
            except:
                time.sleep(300)

        reply = reply.replace(f', also known as {common_name.lower()},', '')
        reply = reply.replace(f', also known as {common_name.title()},', '')
        reply = reply.replace(f', also known as {common_name.capitalize()},', '')
        paragraphs_filtered = reply_to_paragraphs(reply)
        
        if len(paragraphs_filtered) == 1:
            p = paragraphs_filtered[0]
            print('***************************************')
            print(p)
            print('***************************************')

            item[var_name] = p
            util.json_write(filepath, data)
        
        time.sleep(30)


def ai_side_effects_main():
    sections_num = 10
    for index, plant in enumerate(plants):
        print(index, '-', len(plants), '>>', plant[0])

        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')
        url = f'{entity}/medicine/side-effects'
        csv_rows = [row[1] for row in util.csv_get_rows_by_entity('database/tables/side-effects.csv', entity)[:sections_num]]

        json_filepath = f'database/articles/plants/{url}.json'

        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['entity'] = entity
        data['url'] = url
        data['latin_name'] = latin_name
        data['common_name'] = common_name
        data['title'] = f'10 possible side effects of {latin_name} ({common_name}) if used improperly'
        util.json_write(json_filepath, data)

        ai_side_effects_intro(entity)
        # ai_side_effects_sections_csv_to_json(json_filepath, csv_rows)
        # ai_side_effects_sections_description(json_filepath)
        


# def ai_side_effects_main():
#     plants_primary = [row for row in util.csv_get_rows('database/tables/plants.csv')[1:]]
#     plants_secondary = [row for row in util.csv_get_rows('database/tables/plants-secondary.csv')[1:]]
    
#     plants = []
#     for plant in plants_primary: plants.append(plant)
#     for plant in plants_secondary: plants.append(plant)

#     for index, plant in enumerate(plants):
#         print(index, '-', len(plants), '>>', plant)

#         latin_name = plant[0].strip().capitalize()
#         common_name = plant[1].strip().title()

#         entity = latin_name.lower().replace(' ', '-')
#         json_filepath = f'database/articles/plants/{entity}/medicine/side-effects.json'

#         util.json_generate_if_not_exists(json_filepath)
#         data = util.json_read(json_filepath)
#         data['entity'] = entity
#         data['url'] = f'{entity}'
#         data['latin_name'] = latin_name
#         data['common_name'] = common_name
#         data['title'] = f'10 possible side effects of {latin_name} ({common_name}) if used improperly'
#         util.json_write(json_filepath, data)
#         # quit()

#         # INTRO
#         for prompt in prompts.side_effects_intro:
#             prompt = prompt.replace('[latin_name]', latin_name)
#             ai_entity(json_filepath, 'side_effects_intro', 1, prompt, aka=False, save=True)

#         # MEDICINE
#         # for prompt in prompts.entity_medicine:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
#         #     ai_entity(json_filepath, 'medicine_intro', 1, prompt, aka=False, save=True)

#         # for prompt in prompts.entity_benefits:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
#         #     ai_entity(json_filepath, 'benefits', 1, prompt, aka=False)
#         # for prompt in prompts.entity_constituents:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
#         #     ai_entity(json_filepath, 'constituents', 1, prompt, aka=False)
#         # for prompt in prompts.entity_preparations:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
#         #     ai_entity(json_filepath, 'preparations', 1, prompt, aka=False, save=True)
#         # for prompt in prompts.entity_side_effects:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
#         #     ai_entity(json_filepath, 'side_effects', 1, prompt, aka=False, save=True)
#         # for prompt in prompts.entity_precautions:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
#         #     ai_entity(json_filepath, 'precautions', 1, prompt, aka=False, save=True)
        
#         # # HORTICULTURE
#         # for prompt in prompts.entity_horticulture_intro:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
#         #     ai_entity(json_filepath, 'horticulture_intro', 1, prompt, aka=False, save=True)
#         # for prompt in prompts.entity_horticulture_paragraphs:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     ai_entity(json_filepath, 'horticulture_desc', 5, prompt)

#         # # BOTANY
#         # for prompt in prompts.entity_botany_intro:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
#         #     ai_entity(json_filepath, 'botany_intro', 1, prompt, aka=False, save=True)
#         # for prompt in prompts.entity_botany_paragraphs:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
#         #     ai_entity(json_filepath, 'botany_desc', 5, prompt, aka=False, save=True)

#         # # HISTORY
#         # for prompt in prompts.entity_history_intro:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
#         #     ai_entity(json_filepath, 'history_intro', 1, prompt, aka=False, save=True)
#         # for prompt in prompts.entity_history_paragraphs:
#         #     prompt = prompt.replace('[latin_name]', latin_name)
#         #     prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
#         #     ai_entity(json_filepath, 'history_desc', 5, prompt, aka=False, save=True)





#######################################################################
# CSV
#######################################################################

def ai_entity_medicine_benefits_csv():
    filepath = 'database/tables/benefits.csv'

    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')

        print(index, '-', len(plants), '>>' , latin_name, '|', 'benefits')

        rows = util.csv_get_rows_by_entity(filepath, entity)
        if rows != []: continue

        prompt = f'''
            List the 17 best health benefits of {common_name} ({latin_name}).
            # Start each benefit with a third-person singular action verb.
            # Write only the names of the benefits, not the descriptions.
            # Write each benefit name in less than 5 words.
            # Don't include side effects similar to those you already added.
        '''

        
        reply = utils_ai.gen_reply(prompt)
        reply_formatted = ai_list_to_csv(entity, reply)

        if len(reply_formatted) >= 10:
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)

        time.sleep(30)


def ai_entity_medicine_constituents_csv():
    filepath = 'database/tables/constituents.csv'

    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')

        print(index, '-', len(plants), '>>' , latin_name, '|', 'constituents')

        rows = util.csv_get_rows_by_entity(filepath, entity)
        if rows != []: continue

        prompt = f'''
            List the 20 most important medicinal constituents of {latin_name}.
            An example of medicinal constituents are flavonoids and tannins.
            Write only the names of the constituents, not the descriptions.
            Write only 1 constituent per list item.
            Use few words as possible.
        '''

        
        reply = utils_ai.gen_reply(prompt)
        reply_formatted = ai_list_to_csv(entity, reply)

        if len(reply_formatted) >= 10:
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)
        
        time.sleep(30)


def ai_entity_medicine_preparations_csv():
    filepath = 'database/tables/plants-medicine-preparations.csv'

    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')

        print(index, '-', len(plants), '>>' , latin_name, '|', 'preparations')

        rows = util.csv_get_rows_by_entity(filepath, entity)
        if rows != []: continue

        prompt = f'''
            Write a numbered list of the 20 best medicinal preparations of {latin_name} ({common_name}).
            Examples of preparations are infusion and tincture.
            Write only the names of the preparations, don't add descriptions.
            Don't include the name of the plant.
        '''

        
        reply = utils_ai.gen_reply(prompt)
        reply_formatted = ai_list_to_csv(entity, reply)

        if len(reply_formatted) >= 10:
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)
        
        time.sleep(30)


def ai_entity_medicine_side_effects_csv():
    filepath = 'database/tables/side-effects.csv'

    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')

        print(index, '-', len(plants), '>>' , latin_name, '|', 'side effects')

        rows = util.csv_get_rows_by_entity(filepath, entity)
        if rows != []: continue

        prompt_num = 15
        
        prompt = f'''
            Write a numbered list of {prompt_num} possible side effects of {latin_name} ({common_name}) when used medicinally.
            Write only the names of the side effects, not the descriptions.
            Don't include examples for the side effects names.
            Don't include side effects with long names.
        '''

        
        reply = utils_ai.gen_reply(prompt)
        reply_formatted = ai_list_to_csv(entity, reply)

        if len(reply_formatted) >= 10:
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)
        
        time.sleep(30)


def ai_entity_medicine_precautions_csv():
    filepath = 'database/tables/precautions.csv'

    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')

        print(index, '-', len(plants), '>>' , latin_name, '|', 'precautions')

        rows = util.csv_get_rows_by_entity(filepath, entity)
        if rows != []: continue

        prompt = f'''
            Write a numbered list of the 20 most important precautions to take when using {latin_name} ({common_name}) for medicinal purposes.
            Write only the names of the precautions, not the descriptions.
            Start each precaution with a third-person singular action verb.
            Answer in as few words as possible.
        '''

        
        reply = utils_ai.gen_reply(prompt)
        reply_formatted = ai_list_to_csv(entity, reply)

        if len(reply_formatted) >= 10:
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)
        
        time.sleep(30)


#######################################################################################


# def ai_entity_taxonomy_csv():
#     csv_filepath = 'database/tables/taxonomy.csv'
#     plants = [row for row in util.csv_get_rows('database/tables/plants.csv')[1:]]

#     for index, plant in enumerate(plants):
#         latin_name = plant[cols['latin_name']].strip().capitalize()
#         common_name = plant[cols['common_name']].strip().title()
#         entity = latin_name.lower().replace(' ', '-')

#         print(index, '-', len(plants), '>>' , latin_name, '|', 'taxonomy')

#         rows = util.csv_get_rows_by_entity(csv_filepath, entity)
#         if rows != []: continue

#         prompt = f'''
#             Give me an ordered list with the Linnaean Taxonomy of {latin_name}. Include:
#             1. Kingdom
#             2. Phylum
#             3. Class
#             4. Order
#             5. Family
#             6. Genus
#             7. Species
#         '''

#         reply = utils_ai.gen_reply(prompt).strip()

#         reply_formatted = [entity]
#         i = 0
#         for line in reply.split('\n'):
#             line = line.strip()
#             if line == '': continue
#             if not line[0].isdigit(): continue
#             if '. ' in line: line = '. '.join(line.split('. ')[1:])
#             else: continue
#             if ': ' in line: 
#                 line_name = line.split(': ')[0].strip()
#                 if line_name.lower() == 'species': line_desc = latin_name
#                 else: line_desc = line.split(': ')[1].strip()
#             else: continue
#             if '(' in line_desc: line_desc = line_desc.split('(')[0].strip()
#             line_name = line_name.replace('*', '')
#             line_desc = line_desc.replace('*', '')
#             line_name = line_name.lower()
#             if i == 0 and line_name == 'kingdom':
#                 reply_formatted.append(line_desc)
#             elif i == 1 and line_name == 'phylum':
#                 reply_formatted.append(line_desc)
#             elif i == 2 and line_name == 'class':
#                 reply_formatted.append(line_desc)
#             elif i == 3 and line_name == 'order':
#                 reply_formatted.append(line_desc)
#             elif i == 4 and line_name == 'family':
#                 reply_formatted.append(line_desc)
#             elif i == 5 and line_name == 'genus':
#                 reply_formatted.append(line_desc)
#             elif i == 6 and line_name == 'species':
#                 reply_formatted.append(line_desc)
#             else: continue
#             i += 1

#         print(len(reply_formatted))
#         if len(reply_formatted) == 8:
#             print('***************************************')
#             for line in reply_formatted:
#                 print(line)
#             print('***************************************')
#             util.csv_add_rows(csv_filepath, [reply_formatted])

#         time.sleep(30)



def clear_entity_field(field): 
    plants_primary = [row for row in util.csv_get_rows('database/tables/plants.csv')[1:]]
    plants_secondary = [row for row in util.csv_get_rows('database/tables/plants-secondary.csv')[1:]]
    
    plants = []
    for plant in plants_primary: plants.append(plant)
    for plant in plants_secondary: plants.append(plant)

    for index, plant in enumerate(plants):
        print(index, '-', len(plants), '>>', plant)

        latin_name = plant[0].strip().capitalize()
        common_name = plant[1].strip().title()

        entity = latin_name.lower().replace(' ', '-')
        json_filepath = f'database/articles/plants/{entity}.json'

        data = util.json_read(json_filepath)
        data[field] = []
        util.json_write(json_filepath, data)




##################################################################
# TREFLE
##################################################################
        
def ai_entity_trefle_main():
    index_last_plant = 50
    number_of_plants_to_do_today = index_last_plant + 25

    plants_trefle = [row for row in util.csv_get_rows('database/tables/_plants_all_new.csv')[1:]]
    plants_trefle_today = plants_trefle[index_last_plant:number_of_plants_to_do_today]

    plants_primary = [row for row in util.csv_get_rows('database/tables/plants.csv')[1:]]
    plants_secondary = [row for row in util.csv_get_rows('database/tables/plants-secondary.csv')[1:]]
    
    plants_done = []
    for plant in plants_primary: plants_done.append(plant)
    for plant in plants_secondary: plants_done.append(plant)

    for index, plant in enumerate(plants_trefle_today):
        print(index, '-', len(plants_trefle_today), '>>', plant)

        # skip plants from primary and secondary
        found = False
        for plant_done in plants_done:
            if plant[0].lower().strip() in plant_done[0].lower().strip().replace(' ', '-'): 
                found = True
                break
        if found: continue

        entity = plant[0].strip()
        latin_name = entity.replace('-', ' ').capitalize()
        common_name = plant[2].strip().title()
        genus = plant[3].strip().title()
        family = plant[4].strip().title()

        json_filepath = f'database/articles/plants_trefle/{entity}.json'

        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['entity'] = entity
        data['url'] = f'{entity}'
        data['latin_name'] = latin_name
        data['common_name'] = common_name
        data['genus'] = genus
        data['family'] = family
        data['title'] = f'What to know before using {latin_name} ({common_name})?'
        try: lastmod = data['lastmod']
        except: data['lastmod'] = str(date_now())
        util.json_write(json_filepath, data)

        # INTRO
        for prompt in prompts.entity_intro:
            prompt = prompt.replace('[latin_name]', latin_name)
            ai_entity(json_filepath, 'intro_desc', 1, prompt, save=True)

        # MEDICINE
        for prompt in prompts.entity_medicine_intro:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'medicine_intro', 1, prompt, aka=False, save=True)
        for prompt in prompts.entity_medicine_paragraphs:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'medicine_desc', 5, prompt, aka=False, save=True)

        # HORTICULTURE
        for prompt in prompts.entity_horticulture_intro:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'horticulture_intro', 1, prompt, aka=False, save=True)
        for prompt in prompts.entity_horticulture_paragraphs:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'horticulture_desc', 5, prompt, aka=False, save=True)

        # BOTANY
        for prompt in prompts.entity_botany_intro:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            prompt = prompt.replace('[genus]', genus)
            prompt = prompt.replace('[family]', family)
            ai_entity(json_filepath, 'botany_intro', 1, prompt, aka=False, save=True)
        for prompt in prompts.entity_botany_paragraphs:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            prompt = prompt.replace('[genus]', genus)
            prompt = prompt.replace('[family]', family)
            ai_entity(json_filepath, 'botany_desc', 5, prompt, aka=False, save=True)

        # HISTORY
        for prompt in prompts.entity_history_intro:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'history_intro', 1, prompt, aka=False, save=True)
        for prompt in prompts.entity_history_paragraphs:
            prompt = prompt.replace('[latin_name]', latin_name)
            prompt = prompt.replace('[aka]', f', also known as {common_name.lower()},')
            ai_entity(json_filepath, 'history_desc', 5, prompt, aka=False, save=True)



##################################################################
# MOD FIELDS
##################################################################


def field_rename(folderpath, name_old, name_new): 
    for filename in os.listdir(folderpath):
        if filename.endswith('.json'):
            filepath = f'{folderpath}/{filename}'
            print(filepath)
            
            content = util.file_read(filepath)
            content = content.replace(name_old, name_new)
            util.file_write(filepath, content)
            

def field_delete(folderpath, key): 
    for filename in os.listdir(folderpath):
        if filename.endswith('.json'):
            filepath = f'{folderpath}/{filename}'
            print(filepath)
            
            data = util.json_read(filepath)
            del data[key]
            util.json_write(filepath, data)
            # quit()

    # plants_primary = [row for row in util.csv_get_rows('database/tables/plants.csv')[1:]]
    # plants_secondary = [row for row in util.csv_get_rows('database/tables/plants-secondary.csv')[1:]]
    
    # plants = []
    # for plant in plants_primary: plants.append(plant)
    # for plant in plants_secondary: plants.append(plant)

    # for index, plant in enumerate(plants):
    #     print(index, '-', len(plants), '>>', plant)
    #     content = csv.file_read()

        # latin_name = plant[0].strip().capitalize()
        # common_name = plant[1].strip().title()

        # entity = latin_name.lower().replace(' ', '-')
        # json_filepath = f'database/articles/plants/{entity}.json'

        # data = util.json_read(json_filepath)
        # data[field] = []
        # util.json_write(json_filepath, data)



##################################################################
# EXE
##################################################################


# clear_entity_field('medicine_desc')

# ai_entity_medicine_benefits_csv()
# ai_entity_medicine_constituents_csv()
# ai_entity_medicine_preparations_csv()
# ai_entity_medicine_side_effects_csv()
# ai_entity_medicine_precautions_csv()

# ai_entity_taxonomy_csv()

# ai_entity_main()
# ai_entity_trefle_main()

# ai_medicine_main()
# ai_benefits_main()
# ai_constituents_main()
# ai_preparations_main()
ai_side_effects_main() # TODO


# field_rename('database/articles/plants', 'medicine_desc', 'medicine_intro')
# field_delete('database/articles/plants', 'intro_desc')