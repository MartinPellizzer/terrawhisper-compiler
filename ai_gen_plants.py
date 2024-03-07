import csv
import os
import json
import re
from ctransformers import AutoModelForCausalLM
import random
import time
from groq import Groq


import g

import util
import utils_ai


client = Groq(
    api_key='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',
)


# MODELS = [
#     'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.1.Q8_0.gguf',
#     'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.2.Q8_0.gguf',
#     'C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-3.Q8_0.gguf',
#     'C:\\Users\\admin\\.cache\\lm-studio\\models\\TheBloke\\Starling-LM-7B-alpha-GGUF\\starling-lm-7b-alpha.Q8_0.gguf',
# ]
# MODEL = MODELS[1]

# llm = AutoModelForCausalLM.from_pretrained(
#     MODEL,
#     model_type="mistral", 
#     context_length=1024, 
#     max_new_tokens=1024,
#     )



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


def folder_create(filepath):
    chunks = filepath.split('/')
    chunk_curr = ''
    for chunk in chunks[:-1]:
        chunk_curr += chunk + '/'
        try: os.makedirs(f'{chunk_curr}')
        except: pass


# def gen_reply(prompt):
#     print()
#     print("Q:")
#     print()
#     print(prompt)
#     print()
#     print("A:")
#     print()
#     reply = ''
#     for text in llm(prompt, stream=True):
#         reply += text
#         print(text, end="", flush=True)
#     print()
#     print()
#     return reply


def gen_reply(prompt):
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="mixtral-8x7b-32768",
    )

    reply = completion.choices[0].message.content
    print()
    print()
    print()
    print("Q:")
    print()
    print(prompt)
    print()
    print("A:")
    print()
    print(reply)
    print()
    return reply


def prompt_normalize(prompt):
    return '\n'.join([line.strip() for line in prompt.split('\n') if line.strip() != ''])


def reply_normalize(reply):
    paragraphs = [paragraph for paragraph in reply.split('\n')]
    paragraphs_filtered = []
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if ':' in paragraph:
            chunks = paragraph.split(':')
            if len(chunks[0].split(' ')) < 5:
                paragraph = chunks[1].strip()
            else:
                paragraph = ':'.join(chunks)
        if paragraph.strip() == '': continue
        if len(paragraph.split('. ')) == 1: continue
        if paragraph[0].isdigit(): paragraph = paragraph[1:]
        paragraphs_filtered.append(paragraph)
    # for paragraph in paragraphs_filtered:
    #     print(paragraph)
    # print(len(paragraphs_filtered))
    return paragraphs_filtered






def ai_gen_basic():
    for plant in plants:
        latin_name = plant[cols['latin_name']].strip()
        common_name = plant[cols['common_name']].strip()

        entity = latin_name.lower().replace(' ', '-')
        title = f'{latin_name} ({common_name})'

        filepath = f'database/articles/plants/{entity}.json'
        data = util.json_read(filepath)

        try: latin_name = data['latin_name']
        except: data['latin_name'] = latin_name

        try: common_name = data['common_name']
        except: data['common_name'] = common_name

        try: entity = data['entity']
        except: data['entity'] = entity

        try: title = data['title']
        except: data['title'] = title

        util.json_write(filepath, data)

        print(latin_name)
        # quit()


def ai_gen_json():
    running = False

    plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]

    cols = {}
    for i, item in enumerate(plants[0]):
        cols[item] = i

    for plant in plants[1:]:
        latin_name = plant[cols['latin_name']].strip()
        common_name = plant[cols['common_name']].strip()
        latin_name_dash = latin_name.lower().replace(' ', '-')

        filepath = f'database/articles/plants/{latin_name_dash}.json'

        # INIT
        try: data = util.json_read(filepath)
        except: 
            data = {
                'latin_name': latin_name,
                'common_name': common_name,
                'title': f'{latin_name} ({common_name})',
                'intro': [],
                'medicine': [],
                'horticulture': [],
                'botany': [],
            }
        util.json_write(filepath, data)
   




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
    paragraphs = reply.split('\n')
    paragraphs_filtered = []
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph == '': continue
        if paragraph[0].isdigit(): continue
        paragraphs_filtered.append(paragraph)
    return paragraphs_filtered



def reply_to_list(reply):
    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue

        if ':' in line: line = line.split(':')[1]
        if line.strip() == '': continue

        reply_formatted.append(line)
    return reply_formatted


def reply_to_json(reply, p_num):
    pass




#######################################################################
# ROOT
#######################################################################

def ai_entity_intro(filepath):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    intro = ''
    try: intro = data['intro']
    except: data['intro'] = intro
    # if intro != '': return

    prompt = f'''
        Write a 5-sentence paragraph about of {latin_name}.
        Include the medicinal properties of {latin_name}, the horticultural conditions of {latin_name}, and the botanical characteristics of {latin_name}.
        Don't include lists.
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data['intro'] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_entity_medicine(filepath):
    var_val = ''
    var_name = 'medicine_desc'

    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '': return

    prompt = f'''
        Write 5 paragraphs about the medicinal aspects of {latin_name}.
        In paragraph 1, write 5 sentences about the benefits of {latin_name}.
        In paragraph 2, write 5 sentences about the constituents of {latin_name}.
        In paragraph 3, write 5 sentences about the preparations of {latin_name}.
        In paragraph 4, write 5 sentences about the side effects of {latin_name}.
        In paragraph 5, write 5 sentences about the precautions of {latin_name}.
        Don't include lists.
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply_formatted = reply_to_list(reply)


    if len(reply_formatted) == 5:
        p = reply_formatted
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_entity_horticolture(filepath):
    var_val = ''
    var_name = 'horticulture_desc'

    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '': return

    prompt = f'''
        Write 5 paragraphs in 400 words about the horticultural aspects of {latin_name}.
        In paragraph 1, write 5 sentences about the growth requirements of {latin_name}.
        In paragraph 2, write 5 sentences about the planting tips of {latin_name}.
        In paragraph 3, write 5 sentences about the caring tips of {latin_name}.
        In paragraph 4, write 5 sentences about the harvesting tips of {latin_name}.
        In paragraph 5, write 5 sentences about the pests and diseases of {latin_name}.
        Don't include lists.
    '''  
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply_formatted = reply_to_list(reply)

    if len(reply_formatted) == 5:
        p = reply_formatted
        print('***************************************')
        print(p)
        print('***************************************')
        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_entity_botany(filepath):
    var_val = ''
    var_name = 'botany_desc'

    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '': return

    prompt = f'''
        Write 5 paragraphs in 400 words about the horticultural aspects of {latin_name}.
        In paragraph 1, write 5 sentences about the taxonomy of {latin_name}.
        In paragraph 2, write 5 sentences about the morphology of {latin_name}.
        In paragraph 3, write 5 sentences about the variants names and differences of {latin_name}.
        In paragraph 4, write 5 sentences about the geographic distribution and natural habitats of {latin_name}.
        In paragraph 5, write 5 sentences about the life-cycle of {latin_name}.
        Don't include lists.
    '''  
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply_formatted = reply_to_list(reply)

    if len(reply_formatted) == 5:
        p = reply_formatted
        print('***************************************')
        print(p)
        print('***************************************')
        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_entity_main():
    for index, plant in enumerate(plants):
        print(index, '-', len(plants))

        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()

        entity = latin_name.lower().replace(' ', '-')
        filepath = f'database/articles/plants/{entity}.json'
        
        data = util.json_read(filepath)
        data['entity'] = entity
        data['url'] = f'{entity}'
        data['latin_name'] = latin_name
        data['common_name'] = common_name
        data['title'] = f'What to know before using {latin_name} ({common_name})?'
        util.json_write(filepath, data)

        ai_entity_intro(filepath)
        ai_entity_medicine(filepath)
        ai_entity_horticolture(filepath)
        ai_entity_botany(filepath)








#######################################################################
# MEDICINE
#######################################################################

def ai_medicine_intro(filepath):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    intro = ''
    try: intro = data['intro']
    except: data['intro'] = intro
    if intro != '': return

    prompt = f'''
        Write a 5-sentence paragraph about the medicinal aspects of {latin_name} ({common_name}).
        In sentence 1, write the benefits of {latin_name}.
        In sentence 2, write the constituents of {latin_name}.
        In sentence 3, write the preparations of {latin_name}.
        In sentence 4, write the side effects of {latin_name}.
        In sentence 5, write the precautions of {latin_name}.
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data['intro'] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_constituents(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    constituents_list = ''
    try: constituents_list = data['constituents_list']
    except: data['constituents_list'] = constituents_list
    if constituents_list != '': return
    running = True

    prompt_paragraphs_num = 10
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} best active constituents of {latin_name} ({common_name}) for health.
        Add descriptions to the active constituents.
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)

    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' not in line: continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            reply_formatted.append(line)

    if prompt_paragraphs_num == len(reply_formatted):
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')
        data['constituents_list'] = reply_formatted
        util.json_write(filepath, data)

    return running


def ai_medicine_preparations(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    preparations_list = []
    try: preparations_list = data['preparations_list']
    except: data['preparations_list'] = []

    if preparations_list != []: return
    running = True

    prompt_paragraphs_num = 10
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} best medicinal preparations of {latin_name} ({common_name}).
        Add descriptions to the medicinal preparations.
        Examples of medicinal preparations are infusions and tincures.
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)

    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' not in line: continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            reply_formatted.append(line)

    if prompt_paragraphs_num == len(reply_formatted):
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')
        data['preparations_list'] = reply_formatted
        util.json_write(filepath, data)
        
    return running


def ai_medicine_side_effects(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    side_effects_list = []
    try: side_effects_list = data['side_effects_list']
    except: data['side_effects_list'] = []

    if side_effects_list != []: return
    running = True

    prompt_paragraphs_num = 10
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} possible side effects of using {latin_name} ({common_name}) for medicinal purposes.
        Add descriptions to the side effects.
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)

    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' not in line: continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            reply_formatted.append(line)

    if prompt_paragraphs_num == len(reply_formatted):
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')
        data['side_effects_list'] = reply_formatted
        util.json_write(filepath, data)
        
    return running


def ai_medicine_precautions(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    precautions_list = []
    try: precautions_list = data['precautions_list']
    except: data['precautions_list'] = []

    if precautions_list != []: return
    running = True

    prompt_paragraphs_num = 10
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} precautions to take when of using {latin_name} ({common_name}) for medicinal purposes.
        Include the names of the precautions and add descriptions.
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)

    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' not in line: continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            reply_formatted.append(line)

    if prompt_paragraphs_num == len(reply_formatted):
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')
        data['precautions_list'] = reply_formatted
        util.json_write(filepath, data)
        
    return running


def ai_medicine_main():
    for index, plant in enumerate(plants):
        print(index, '-', len(plants))

        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()

        entity = latin_name.lower().replace(' ', '-')
        filepath = f'database/articles/plants/{entity}/medicine.json'
        
        data = util.json_read(filepath)
        data['entity'] = entity
        data['url'] = f'{entity}/medicine'
        data['latin_name'] = latin_name
        data['common_name'] = common_name
        data['title'] = f'{latin_name} ({common_name}) Medicinal Guide'
        util.json_write(filepath, data)

        ai_medicine_intro(filepath)

        # # BENEFITS
        # ai_entity_medicine_benefits(filepath, running)

        # # CONSTITUENTS
        # ai_entity_medicine_constituents(filepath, running)

        # # PREPARATIONS
        # ai_entity_medicine_preparations(filepath, running)

        # # SIDE EFFECTS
        # ai_entity_medicine_side_effects(filepath, running)

        # # PRECAUTIONS
        # ai_entity_medicine_precautions(filepath, running)





#######################################################################
# ROOT / MEDICINE
#######################################################################

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
        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
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







def ai_medicine_benefits_list(entity):
    filepath_in = 'database/tables/benefits.csv'
    filepath_out = f'database/articles/plants/{entity}/medicine.json'
    benefits_csv = [row[1] for row in util.csv_get_rows_by_entity(filepath_in, entity)]
    
    data = util.json_read(filepath_out)

    benefits_list = []
    try: benefits_list = data['benefits_list']
    except: data['benefits_list'] = benefits_list
    if benefits_list != []: return
    
    benefits_num = 10
    latin_name = entity.replace('-', ' ').strip().capitalize()
    lst = ''.join(f'{i+1}. {benefit}\n' for i, benefit in enumerate(benefits_csv[:benefits_num]))
    prompt = f'''
        Write a 1 sentence description for each benefit of {latin_name} in the following list:
        {lst}
        Answer in a ordered list using the following format. benefit: description.
    '''     
    prompt = prompt_normalize(prompt)
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

    if len(reply_formatted) == benefits_num:
        print('***************************************')
        for paragraph in reply_formatted:
            print(paragraph)
        print('***************************************')

        data['benefits_list'] = reply_formatted
        util.json_write(filepath_out, data)

    time.sleep(30)





def ai_medicine_constituents_text(entity):
    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    constituents_text = ''
    try: constituents_text = data['constituents_text']
    except: data['constituents_text'] = ''
    if constituents_text != '':  return

    rows = util.csv_get_rows_by_entity('database/tables/constituents.csv', entity)
    lst = [row[1] for row in rows]
    lst = ', '.join(lst)

    starting_text = f'{latin_name} has several active constituents, such as '
    prompt = f'''
        Explain in a 5-sentence paragraph the following medicinal constituents of {latin_name}: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data['constituents_text'] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_constituents_list(entity):
    filepath_in = 'database/tables/constituents.csv'
    filepath_out = f'database/articles/plants/{entity}/medicine.json'
    rows = [row[1] for row in util.csv_get_rows_by_entity(filepath_in, entity)]
    
    data = util.json_read(filepath_out)

    lst = []
    try: lst = data['constituents_list']
    except: data['constituents_list'] = lst
    if lst != []: return
    
    lst_num = 10
    latin_name = entity.replace('-', ' ').strip().capitalize()
    lst = ''.join(f'{i+1}. {benefit}\n' for i, benefit in enumerate(rows[:lst_num]))
    prompt = f'''
        Write a 1 sentence description for each medicinal constituent of {latin_name} in the following list:
        {lst}
        Answer in a ordered list using the following format. constituent: description.
    '''     
    prompt = prompt_normalize(prompt)
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

        data['constituents_list'] = reply_formatted
        util.json_write(filepath_out, data)

    time.sleep(30)





def ai_medicine_preparations_text(entity):
    var_val = ''
    var_name = 'preparations_text'

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '':  return

    rows = util.csv_get_rows_by_entity('database/tables/constituents.csv', entity)
    lst = [row[1] for row in rows]
    lst = ', '.join(lst)

    starting_text = f'{latin_name} has several medicinal preparations, such as '
    prompt = f'''
        Explain in a 5-sentence paragraph the following medicinal preparations of {latin_name}: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_preparations_list(entity):
    var_val = []
    var_name = 'preparations_list'

    filepath_in = 'database/tables/preparations.csv'
    filepath_out = f'database/articles/plants/{entity}/medicine.json'
    rows = [row[1] for row in util.csv_get_rows_by_entity(filepath_in, entity)]
    
    data = util.json_read(filepath_out)

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != []: return
    
    lst_num = 10
    latin_name = entity.replace('-', ' ').strip().capitalize()
    lst = ''.join(f'{i+1}. {benefit}\n' for i, benefit in enumerate(rows[:lst_num]))
    prompt = f'''
        Write a 1 sentence description for each medicinal preparation of {latin_name} in the following list:
        {lst}
        Answer in a ordered list using the following format. preparation: description.
    '''     
    prompt = prompt_normalize(prompt)
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





def ai_medicine_side_effects_text(entity):
    var_val = ''
    var_name = 'side_effects_text'

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '':  return

    rows = util.csv_get_rows_by_entity('database/tables/side-effects.csv', entity)
    lst = [row[1] for row in rows]
    lst = ', '.join(lst)

    starting_text = f'{latin_name} can have side effects if used improperly, '
    prompt = f'''
        Explain in a 5-sentence paragraph the following possible side effects of {latin_name}: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_side_effects_list(entity):
    var_val = []
    var_name = 'side_effects_list'

    filepath_in = 'database/tables/side-effects.csv'
    filepath_out = f'database/articles/plants/{entity}/medicine.json'
    rows = [row[1] for row in util.csv_get_rows_by_entity(filepath_in, entity)]
    
    data = util.json_read(filepath_out)

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != []: return
    
    lst_num = 10
    latin_name = entity.replace('-', ' ').strip().capitalize()
    lst = ''.join(f'{i+1}. {item}\n' for i, item in enumerate(rows[:lst_num]))
    prompt = f'''
        Write a 1 sentence description for each possible side effect of {latin_name} in the following list:
        {lst}
        Answer in a ordered list using the following format. side effect: description.
    '''     
    prompt = prompt_normalize(prompt)
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


    


def ai_medicine_precautions_text(entity):
    
    var_val = ''
    var_name = 'precautions_text'

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '':  return

    rows = util.csv_get_rows_by_entity('database/tables/precautions.csv', entity)
    lst = [row[1] for row in rows]
    lst = ', '.join(lst)

    starting_text = f'Before using {latin_name} it\'s important to take some precautions, such as '
    prompt = f'''
        Explain in a 5-sentence paragraph the following precautions when using {latin_name} for medicinal purposes: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_precautions_list(entity):
    var_val = []
    var_name = 'precautions_list'

    filepath_in = 'database/tables/precautions.csv'
    filepath_out = f'database/articles/plants/{entity}/medicine.json'
    rows = [row[1] for row in util.csv_get_rows_by_entity(filepath_in, entity)]
    
    data = util.json_read(filepath_out)

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != []: return
    
    lst_num = 10
    latin_name = entity.replace('-', ' ').strip().capitalize()
    lst = ''.join(f'{i+1}. {item}\n' for i, item in enumerate(rows[:lst_num]))
    prompt = f'''
        Write a 1 sentence description for each of the following precaution you should take when using {latin_name} for medicinal purposes:
        {lst}
        Answer in a ordered list using the following format. precaution: description.
    '''     
    prompt = prompt_normalize(prompt)
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


    


def ai_medicine_main_2():
    for index, plant in enumerate(plants):
        print(index, '-', len(plants))

        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()

        entity = latin_name.lower().replace(' ', '-')
        filepath = f'database/articles/plants/{entity}/medicine.json'
        
        data = util.json_read(filepath)
        data['entity'] = entity
        data['url'] = f'{entity}/medicine'
        data['latin_name'] = latin_name
        data['common_name'] = common_name
        data['title'] = f'{latin_name} ({common_name}) Medicinal Guide'
        util.json_write(filepath, data)

        # ai_medicine_intro(filepath)
        ai_medicine_benefits_list(entity)
        ai_medicine_constituents_text(entity)
        ai_medicine_constituents_list(entity)
        ai_medicine_preparations_text(entity)
        ai_medicine_preparations_list(entity)
        ai_medicine_side_effects_text(entity)
        ai_medicine_side_effects_list(entity)
        ai_medicine_precautions_text(entity)
        ai_medicine_precautions_list(entity)

        # # BENEFITS
        # ai_entity_medicine_benefits(filepath, running)

        # # CONSTITUENTS
        # ai_entity_medicine_constituents(filepath, running)

        # # PREPARATIONS
        # ai_entity_medicine_preparations(filepath, running)

        # # SIDE EFFECTS
        # ai_entity_medicine_side_effects(filepath, running)

        # # PRECAUTIONS
        # ai_entity_medicine_precautions(filepath, running)





ai_medicine_main_2()
quit()



#######################################################################
# ROOT >> MEDICINE >> BENEFITS
#######################################################################

# RESETS
def entity_medicine_benefits_init():
    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')
        url = f'{entity}/medicine/benefits'
        filepath = f'database/articles/plants/{url}.json'
        folder_create(filepath)

        data = util.json_read(filepath)
        if not data: continue
        data['benefits'] = []
        util.json_write(filepath, data)
    
# entity_medicine_benefits_init()

# ---------------------------------------------------------------------


def ai_benefits_section(filepath, csv_benefits, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    benefits = []
    try: benefits = data['benefits']
    except: data['benefits'] = benefits

    if benefits != []: return
    running = True

    benefits_tmp = []
    for benefit in csv_benefits:
        benefits_tmp.append({'benefit_name': benefit})
    
    data['benefits'] = benefits_tmp
    util.json_write(filepath, data)


# def ai_entity_medicine_benefits_list(filepath):
#     running = False

#     data = util.json_read(filepath)
#     latin_name = data['latin_name']
#     common_name = data['common_name']

#     try: benefits = data['benefits']
#     except: data['benefits'] = []

#     if data['benefits'] != []: return running
#     running = True
    
#     prompt_num = 10
#     prompt = f'''
#         Write a numbered list of the {prompt_num} best health benefits of {common_name} ({latin_name}).
#         Include names and descriptions.
#         Start the names with a third-person singular action verb.
#     '''
#     prompt = prompt_normalize(prompt)
#     reply = gen_reply(prompt)
#     reply = reply.strip()

#     reply_formatted = []
#     for line in reply.split('\n'):
#         line_name = ''
#         line_desc = ''
#         line = line.strip()
#         if line == '': continue

#         if ': ' in line: 
#             line_name = line.split(': ')[0].strip()
#             line_desc = ': '.join(line.split(': ')[1:]).strip()
#             if line_name == '': continue
#             if line_desc == '': continue

#             if line_name[0].isdigit():
#                 if '. ' in line_name: line_name = line_name.split('. ')[1].strip()
#                 if line_name == '': continue
#                 reply_formatted.append({"name": line_name, "desc": line_desc})

#     if prompt_num == len(reply_formatted):
#         for paragraph in reply_formatted:
#             print('***************************************')
#             print(paragraph)
#             print('***************************************')

#         data['benefits'] = reply_formatted
#         util.json_write(filepath, data)

#     return running


def ai_benefits_definition(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    benefits = []
    try: benefits = data['benefits']
    except: return

    for benefit in benefits[:10]:
        benefit_name = benefit['benefit_name']
        
        benefit_definition = ''
        try: benefit_definition = benefit['definition']
        except: benefit['definition'] = benefit_definition

        if benefit_definition != '': continue
        running = True

        starting_text = f'"{common_name.title()} {benefit_name.lower()}" refers to its ability to '
        prompt = f'''
                Define in detail in 1 sentence what "{common_name} {benefit_name}" means. 
                Start the sentence with these words: {starting_text}
            '''
        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()
        if starting_text.lower().strip() not in reply.lower():
            reply = starting_text + reply 

        paragraphs = reply.split('\n')
        paragraphs_filtered = []
        for paragraph in paragraphs:
            if ":" in paragraph: continue
            if paragraph[0].isdigit(): continue
            if len(paragraph.split('. ')) != 1: continue
            paragraphs_filtered.append(paragraph)
        
        if len(paragraphs_filtered) == 1:
            print('***************************************')
            print(reply)
            print('***************************************')

            benefit['definition'] = paragraphs_filtered[0]
            util.json_write(filepath, data)
        
        time.sleep(30)

    return running


def ai_benefits_description_text(filepath, running):
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
        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
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


def ai_entity_medicine_benefits_constituents_list(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    # benefits = []
    # try: benefits = data['benefits']
    # except: return

    for benefit in benefits[:10]:
        # TODO: UNIFY WHEN POSSIBLE
        try: benefit_name = benefit['name']
        except: benefit_name = benefit['benefit']

        benefit_constituents = []
        try: benefit_constituents = benefit['constituents']
        except: benefit['constituents'] = []

        if benefit_constituents != []: continue
        running = True
        
        prompt_num = 10
        prompt = f'''
            Write a numbered list of the {prompt_num} most important medicinal constituents of {latin_name} that help with this benefit: {benefit_name}. 
            Write only the names of the constituents, not the descriptions.
        '''        
        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)

        reply = reply.strip()
        reply_formatted = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if line[0].isdigit() and '. ' in line:
                line = '. '.join(line.split('. ')[1:]).strip()
                if line == '': continue
                if ':' in line: line = line.split(':')[0].strip()
                if '(' in line: line = line.split('(')[0].strip()
                if line.endswith('.'): line = line[0:-1]
                if len(line.split(' ')) > 3: continue
                reply_formatted.append(line)
        
        print('***************************************')
        print(reply_formatted)
        print('***************************************')

        if prompt_num == len(reply_formatted):
            benefit['constituents'] = reply_formatted
            util.json_write(filepath, data)

    return running


def ai_entity_medicine_benefits_constituents_text(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    benefits = []
    try: benefits = data['benefits']
    except: return

    for benefit in benefits[:10]:
        # TODO: UNIFY WHEN POSSIBLE
        try: benefit_name = benefit['name']
        except: benefit_name = benefit['benefit']
        
        benefit_constituents = []
        try: benefit_constituents = benefit['constituents']
        except: benefit['constituents'] = []
        
        benefit_constituents_text = ''
        try: benefit_constituents_text = benefit['constituents_text']
        except: benefit['constituents_text'] = ''

        if benefit_constituents == []: continue
        if benefit_constituents_text != '': continue
        running = True

        constituents = ', '.join(benefit_constituents[:7])
        prompt = f'''
            Write a 60-word paragraph explaining how these constituents contained in the {common_name} plant {benefit_name}: {constituents}.
        '''

        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()
        
        paragraphs = reply.split('\n')
        paragraphs_filtered = []
        for paragraph in paragraphs:
            if ":" in paragraph: continue
            if paragraph[0].isdigit(): continue
            if len(paragraph.split('. ')) < 2: continue
            paragraphs_filtered.append(paragraph)

        if len(paragraphs_filtered) == 1:            
            print('***************************************')
            print(paragraphs_filtered[0])
            print('***************************************')

            benefit['constituents_text'] = paragraphs_filtered[0]
            util.json_write(filepath, data)

    return running


def ai_entity_medicine_benefits_conditions_list(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    benefits = []
    try: benefits = data['benefits']
    except: return

    for benefit in benefits[:10]:
        # TODO: UNIFY WHEN POSSIBLE
        try: benefit_name = benefit['name']
        except: benefit_name = benefit['benefit']

        benefit_conditions = []
        try: benefit_conditions = benefit['conditions']
        except: benefit['conditions'] = []

        if benefit_conditions != []: continue
        running = True

        prompt_paragraphs_num = 10
        prompt = f'''
            Write a numbered list of the {prompt_paragraphs_num} most common health conditions helped by this benefit of {common_name}: {benefit_name}.
            Give me just the names of the conditions, not the descriptions.
        '''        
        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)

        reply = reply.strip()
        reply_formatted = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            if line[0].isdigit() and '. ' in line:
                line = '. '.join(line.split('. ')[1:]).strip()
                line = line.split('(')[0].strip()
                if line == '': continue
                if len(line.split(' ')) > 5: continue
                reply_formatted.append(line)
        
        print('***************************************')
        print(reply_formatted)
        print('***************************************')

        if prompt_paragraphs_num == len(reply_formatted):
            benefit['conditions'] = reply_formatted
            util.json_write(filepath, data)

    return running


def ai_entity_medicine_benefits_conditions_text(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    benefits = []
    try: benefits = data['benefits']
    except: return

    for benefit in benefits[:10]:
        # TODO: UNIFY WHEN POSSIBLE
        try: benefit_name = benefit['name']
        except: benefit_name = benefit['benefit']
        
        benefit_conditions = []
        try: benefit_conditions = benefit['conditions']
        except: benefit['conditions'] = []
        
        benefit_conditions_text = ''
        try: benefit_conditions_text = benefit['conditions_text']
        except: benefit['conditions_text'] = ''

        if benefit_conditions == []: continue
        if benefit_conditions_text != '': continue
        running = True

        conditions = ', '.join(benefit_conditions[:7])
        prompt = f'''
            Write a 60-word paragraph explaining how the fact that {common_name} {benefit_name.lower()} helps with the following conditions: {conditions}.
        '''

        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()
        
        paragraphs = reply.split('\n')
        paragraphs_filtered = []
        for paragraph in paragraphs:
            if ":" in paragraph: continue
            if paragraph.strip() == '': continue
            if paragraph[0].isdigit(): continue
            if len(paragraph.split('. ')) < 2: continue
            paragraphs_filtered.append(paragraph)

        if len(paragraphs_filtered) == 1:            
            print('***************************************')
            print(paragraphs_filtered[0])
            print('***************************************')

            benefit['conditions_text'] = paragraphs_filtered[0]
            util.json_write(filepath, data)

    return running


def ai_benefits_main():
    benefits_num = 10
    running = True

    for index, plant in enumerate(plants):
        print(index, '-', len(plants))

        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')
        url = f'{entity}/medicine/benefits'
        csv_benefits = [row[1] for row in util.csv_get_rows_by_entity('database/tables/benefits.csv', entity)[:benefits_num]]

        filepath = f'database/articles/plants/{url}.json'
        folder_create(filepath)

        # INIT
        data = util.json_read(filepath)
        if not data:
            data = {
                'entity': entity,
                'url': url,
                'latin_name': latin_name,
                'common_name': common_name,
                'title': f'{latin_name} ({common_name})',
            }
            print(f'creating new file: {filepath}')
        util.json_write(filepath, data)

        ai_benefits_section(filepath, csv_benefits, running)
        ai_benefits_description_text(filepath, running)
        




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

        prompt_num = 20
        prompt = f'''
            List the {prompt_num} best health benefits of {common_name} ({latin_name}).
            Start each benefit with a third-person singular action verb.
            Write only the names of the benefits, not the descriptions.
            Write each benefit name in less than 5 words.
            Don't include side effects similar to those you already added.
        '''

        prompt = prompt_normalize(prompt)
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

        prompt_num = 20
        prompt = f'''
            List the {prompt_num} most important medicinal constituents of {latin_name}.
            Write only the names of the constituents, not the descriptions.
            Write only 1 constituent per list item.
            Don't include examples for the constituents names.
            Use few words as possible.
        '''

        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply_formatted = ai_list_to_csv(entity, reply)

        if len(reply_formatted) >= 10:
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)
        
        time.sleep(30)


def ai_entity_medicine_preparations_csv():
    filepath = 'database/tables/preparations.csv'

    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')

        print(index, '-', len(plants), '>>' , latin_name, '|', 'preparations')

        rows = util.csv_get_rows_by_entity(filepath, entity)
        if rows != []: continue

        prompt_num = 20
        
        prompt = f'''
            Write a numbered list of the {prompt_num} best medicinal preparations of {latin_name} ({common_name}).
            Examples of preparations are infusion and tincture.
            Write only the names of the preparations, don't add descriptions.
            Don't include examples for the preparations names.
            Don't include preparations with long names.
            Don't include preparations similar to those you already added.
        '''

        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
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
            Don't include side effects similar to those you already added.
        '''

        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
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

        prompt_num = 20
        
        prompt = f'''
            Write a numbered list of the {prompt_num} most important precautions to take when using {latin_name} ({common_name}) for medicinal purposes.
            Write only the names of the precautions, not the descriptions.
            Start each benefit with a third-person singular action verb.
            Write each precautions using less than 7 words.
            Don't include precautions similar to those you already added.
        '''

        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply_formatted = ai_list_to_csv(entity, reply)

        if len(reply_formatted) >= 10:
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)
        
        time.sleep(30)



# ai_entity_medicine_benefits_csv()
# ai_entity_medicine_constituents_csv()
ai_entity_medicine_preparations_csv()
# ai_entity_medicine_side_effects_csv()
# ai_entity_medicine_precautions_csv()



quit()



def ai_medicine_benefits_text(data):
    entity = data['entity']
    latin_name = data['latin_name']
    common_name = data['common_name']

    filepath = f'database/articles/plants/{entity}/medicine.json'

    benefits_text = ''
    try: benefits_text = data['benefits_text']
    except: data['benefits_text'] = benefits_text
    if benefits_text != '':  return

    rows = util.csv_get_rows_by_entity('database/tables/benefits.csv', entity)
    benefits = [row[1] for row in rows]
    benefits_formatted = ', '.join(benefits)

    aka = f', also known as {common_name.lower()},'
    starting_text = f'{latin_name}{aka} has '
    prompt = f'''
        Explain in a 5-sentence paragraph the following health benefits of {latin_name}: {benefits_formatted}.
        Don't include the common name of the plant.
        Start with the following words: {starting_text}
    '''
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = reply.replace(aka, '')
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data['benefits_text'] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_constituents_text(data):
    section = 'constituents'

    entity = data['entity']
    latin_name = data['latin_name']
    common_name = data['common_name']

    data_param = f'{section}_text'
    data_var = ''
    try: data_var = data[data_param]
    except: data[data_param] = data_var

    if data_var != '':  return

    rows = util.csv_get_rows_by_entity(f'database/tables/{section}.csv', entity)
    lst = [row[1] for row in rows]
    lst_formatted = ', '.join(lst)

    aka = f', also known as {common_name.lower()},'
    starting_text = f'{latin_name}{aka} has several active constituents, '
    prompt = f'''
        Explain in a 5-sentence paragraph the following active constituents of {latin_name}: {lst_formatted}.
        Start with these words: {starting_text}
    '''    
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = reply.replace(aka, '')
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[data_param] = p
        util.json_write(f'database/articles/plants/{entity}/medicine.json', data)

    time.sleep(30)


def ai_medicine_preparations_text(data):
    section = 'preparations'

    entity = data['entity']
    latin_name = data['latin_name']
    common_name = data['common_name']

    data_param = f'{section}_text'
    data_var = ''
    try: data_var = data[data_param]
    except: data[data_param] = data_var

    if data_var != '':  return

    rows = util.csv_get_rows_by_entity(f'database/tables/{section}.csv', entity)
    lst = [row[1] for row in rows]
    lst_formatted = ', '.join(lst)

    starting_text = f'{latin_name}, also known as {common_name.lower()}, has many medicinal preparations, such as '
    prompt = f'''
        Explain in a 5-sentence paragraph the following medicinal preparations of {latin_name}: {lst_formatted}.
        Start with these words: {starting_text}
    '''    
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = reply.replace(f', also known as {common_name.lower()},', '')
    reply = reply.replace(f', also known as {common_name.title()},', '')
    reply = reply.replace(f', also known as {common_name.capitalize()},', '')
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[data_param] = p
        util.json_write(f'database/articles/plants/{entity}/medicine.json', data)

    time.sleep(30)


def ai_medicine_side_effects_text(data):
    section = 'side-effects'

    entity = data['entity']
    latin_name = data['latin_name']
    common_name = data['common_name']

    data_param = f'{section}_text'.replace('-', '_')
    data_var = ''
    try: data_var = data[data_param]
    except: data[data_param] = data_var

    if data_var != '':  return

    rows = util.csv_get_rows_by_entity(f'database/tables/{section}.csv', entity)
    lst = [row[1] for row in rows]
    lst_formatted = ', '.join(lst)

    starting_text = f'{latin_name}, also known as {common_name.lower()}, can have side effects if used improperly, such as'
    prompt = f'''
        Explain in a 5-sentence paragraph the following possible side effects of {latin_name}: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = reply.replace(f', also known as {common_name.lower()},', '')
    reply = reply.replace(f', also known as {common_name.title()},', '')
    reply = reply.replace(f', also known as {common_name.capitalize()},', '')
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[data_param] = p
        util.json_write(f'database/articles/plants/{entity}/medicine.json', data)

    time.sleep(30)


def ai_medicine_precautions_text(data):
    section = 'precautions'

    entity = data['entity']
    latin_name = data['latin_name']
    common_name = data['common_name']

    data_param = f'{section}_text'.replace('-', '_')
    data_var = ''
    try: data_var = data[data_param]
    except: data[data_param] = data_var

    # if data_var != '':  return

    rows = util.csv_get_rows_by_entity(f'database/tables/{section}.csv', entity)
    lst = [row[1] for row in rows]
    lst_formatted = ', '.join(lst)

    starting_text = f'It\'s important to take some precautions when using {latin_name} for medicinal purposes, such as'
    prompt = f'''
        Explain in a 5-sentence paragraph why is important to take the following precautions when using {latin_name} for medicinal purposes: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = reply.replace(f', also known as {common_name.lower()},', '')
    reply = reply.replace(f', also known as {common_name.title()},', '')
    reply = reply.replace(f', also known as {common_name.capitalize()},', '')
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[data_param] = p
        util.json_write(f'database/articles/plants/{entity}/medicine.json', data)

    time.sleep(30)



def ai_medicine_main():
    for plant in plants:
        latin_name = plant[cols['latin_name']].strip()
        common_name = plant[cols['common_name']].strip()

        entity = latin_name.lower().replace(' ', '-')
        filepath = f'database/articles/plants/{entity}/medicine.json'

        data = util.json_read(filepath)
        data['entity'] = entity
        data['url'] = f'{entity}/medicine'
        data['latin_name'] = latin_name
        data['common_name'] = common_name
        data['title'] = f'{latin_name} ({common_name}) Medicinal Properties and Uses'
        util.json_write(filepath, data)

        ai_medicine_benefits_text(data)
        ai_medicine_constituents_text(data)
        ai_medicine_preparations_text(data)
        ai_medicine_side_effects_text(data)
        ai_medicine_precautions_text(data)



ai_medicine_main()








# running = True
# while running:
    # running = ai_gen_medicine_benefits_definition_section()
    # running = ai_gen_medicine_benefits_constituents_section()
    # running = ai_gen_medicine_benefits_constituents_text_section()
    # running = ai_gen_medicine_benefits_conditions_section()
    # running = ai_gen_medicine_benefits_conditions_text_section()

    # running = ai_entity_main()
    # running = ai_entity_medicine_main()
    # running = ai_entity_medicine_benefits_main()







# for index, plant in enumerate(plants):
#     print(index, '-', len(plants))

#     latin_name = plant[cols['latin_name']].strip().capitalize()
#     entity = latin_name.lower().replace(' ', '-')

#     ai_medicine_benefits_description_text(entity)

#     # ai_entity_medicine_benefits_description_list(entity)

#     # running = ai_entity_medicine_constituents_description_text(entity)
#     # running = ai_entity_medicine_constituents_description_list(entity)

#     # running = ai_entity_medicine_preparations_description_text(entity)
#     # running = ai_entity_medicine_preparations_description_list(entity)

#     # running = ai_entity_medicine_side_effects_description_list(entity)
#     # running = ai_entity_medicine_side_effects_description_text(entity)

#     # running = ai_entity_medicine_precautions_description(entity)

# # def article_clear_data():
# #     filepath = 'database/articles/plants/achillea-millefolium/medicine.json'

# # article_clear_data()




# def json_entity_medicine(entity):
#     rows = util.csv_get_rows_by_entity('database/tables/benefits.csv', entity)
#     lst = [f'{row[1].title()}: {row[2]}' for row in rows]
#     article_filepath = f'database/articles/plants/{entity}/medicine.json'
#     data = util.json_read(article_filepath)
#     data['benefits_list'] = lst
#     data = util.json_write(article_filepath, data)

#     rows = util.csv_get_rows_by_entity('database/tables/constituents.csv', entity)
#     lst = [f'{row[1].title()}: {row[2]}' for row in rows]
#     article_filepath = f'database/articles/plants/{entity}/medicine.json'
#     data = util.json_read(article_filepath)
#     data['constituents_list'] = lst
#     data = util.json_write(article_filepath, data)

#     rows = util.csv_get_rows_by_entity('database/tables/preparations.csv', entity)
#     lst = [f'{row[1].title()}: {row[2]}' for row in rows]
#     article_filepath = f'database/articles/plants/{entity}/medicine.json'
#     data = util.json_read(article_filepath)
#     data['preparations_list'] = lst
#     data = util.json_write(article_filepath, data)

#     rows = util.csv_get_rows_by_entity('database/tables/side-effects.csv', entity)
#     lst = [f'{row[1].title()}: {row[2]}' for row in rows]
#     article_filepath = f'database/articles/plants/{entity}/medicine.json'
#     data = util.json_read(article_filepath)
#     data['side_effects_list'] = lst
#     data = util.json_write(article_filepath, data)

#     rows = util.csv_get_rows_by_entity('database/tables/precautions.csv', entity)
#     lst = [f'{row[1].title()}: {row[2]}' for row in rows]
#     article_filepath = f'database/articles/plants/{entity}/medicine.json'
#     data = util.json_read(article_filepath)
#     data['precautions_list'] = lst
#     data = util.json_write(article_filepath, data)



# for index, plant in enumerate(plants):
#     latin_name = plant[cols['latin_name']].strip().capitalize()
#     common_name = plant[cols['common_name']].strip().title()
#     entity = latin_name.lower().replace(' ', '-')

#     json_entity_medicine(entity)

