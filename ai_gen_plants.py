import csv
import os
import json
import re
from ctransformers import AutoModelForCausalLM
import random
import g

import util

# TODO: missing latin_name (and other) in json. fill it in ai_gen.



MODELS = [
    'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.1.Q8_0.gguf',
    'C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-3.Q8_0.gguf',
    'C:\\Users\\admin\\.cache\\lm-studio\\models\\mlabonne\\AlphaMonarch-7B-GGUF\\alphamonarch-7b.Q8_0.gguf',
    'C:\\Users\\admin\\.cache\\lm-studio\\models\\TheBloke\\Starling-LM-7B-alpha-GGUF\\starling-lm-7b-alpha.Q8_0.gguf',
]
MODEL = MODELS[0]

llm = AutoModelForCausalLM.from_pretrained(
    MODEL,
    model_type="mistral", 
    context_length=1024, 
    max_new_tokens=1024,
    )


plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]
cols = {}
for i, item in enumerate(plants[0]):
    cols[item] = i
plants = plants[1:g.ARTICLES_NUM]


def gen_reply(prompt):
    print()
    print("Q:")
    print()
    print(prompt)
    print()
    print("A:")
    print()
    reply = ''
    for text in llm(prompt, stream=True):
        reply += text
        print(text, end="", flush=True)
    print()
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



        # MEDICINE SECTION
        data = util.json_read(filepath)

        try: data_medicine = data['intro']
        except: data['intro'] = []

        if data['intro'] == []:
            prompt_paragraphs_num = 3
            prompt = f'''
                Write {prompt_paragraphs_num} paragraphs in 200 words about {common_name} ({latin_name}).
                In paragraph 1, write about the health benefits.
                In paragraph 2, write about the horticultural conditions.
                In paragraph 3, write about the botanical characteristics.
                Don't include numbers.
                Don't name the paragraphs.
            '''
            prompt = prompt_normalize(prompt)
            reply = gen_reply(prompt)
            reply_normalized = reply_normalize(reply)

            for paragraph in reply_normalized:
                print('***************************************')
                print(paragraph)
                print('***************************************')
            reply_paragraphs_num = len(reply_normalized)

            if len(reply_normalized) == prompt_paragraphs_num:
                data['intro'] = reply_normalized
                util.json_write(filepath, data)
            else:
                print(f'\n\n*** INTRO --- COULD NOT SAVE: paragraph num >> {reply_paragraphs_num} / {prompt_paragraphs_num} ***\n\n')

            running = True



        # MEDICINE SECTION
        data = util.json_read(filepath)
        
        try: data_medicine = data['medicine']
        except: data['medicine'] = []

        if data['medicine'] == []:
            prompt_paragraphs_num = 5
            prompt = f'''
                Write {prompt_paragraphs_num} paragraphs in 400 words about the medicinal aspects of {common_name} ({latin_name}).
                In paragraph 1, write about the health benefits and health conditions this plant helps, without mentioning constituents. Start paragraph 1 with the following words: "{common_name.capitalize()} ({latin_name}) has many health benefits, such as ".
                In paragraph 2, write about the medicinal constituents.
                In paragraph 3, write about the most used parts and medicinal preparations.
                In paragraph 4, write about the possible side effects.
                In paragraph 5, write about the precautions.
            '''
            prompt = prompt_normalize(prompt)
            reply = gen_reply(prompt)
            reply_normalized = reply_normalize(reply)
            
            for paragraph in reply_normalized:
                print('***************************************')
                print(paragraph)
                print('***************************************')
            reply_paragraphs_num = len(reply_normalized)

            if len(reply_normalized) == prompt_paragraphs_num:
                data['medicine'] = reply_normalized
                util.json_write(filepath, data)
            else:
                print(f'\n\n*** COULD NOT SAVE: paragraph num >> {reply_paragraphs_num} / {prompt_paragraphs_num} ***\n\n')

            running = True



        # HORTICULTURE SECTION
        data = util.json_read(filepath)

        try: data_horticulture = data['horticulture']
        except: data['horticulture'] = []

        if data['horticulture'] == []:
            prompt_paragraphs_num = 5
            prompt = f'''
                Write {prompt_paragraphs_num} paragraphs in 400 words about the horticultural aspects of {common_name} ({latin_name}).
                In paragraph 1, write what are the growth requirements.
                In paragraph 2, write what are the planting tips.
                In paragraph 3, write what are the caring tips.
                In paragraph 4, write what are the harvesting tips.
                In paragraph 5, write what are the pests and diseases.
                Include as much data as possible in as few words as possible.
                Use the metric system.
                Don't write lists.
            '''
            prompt = prompt_normalize(prompt)
            reply = gen_reply(prompt)
            reply_normalized = reply_normalize(reply)

            for paragraph in reply_normalized:
                print('***************************************')
                print(paragraph)
                print('***************************************')
            reply_paragraphs_num = len(reply_normalized)

            if len(reply_normalized) == prompt_paragraphs_num:
                data['horticulture'] = reply_normalized
                util.json_write(filepath, data)
            else:
                print(f'\n\n*** COULD NOT SAVE: paragraph num >> {reply_paragraphs_num} / {prompt_paragraphs_num} ***\n\n')

            running = True



        # BOTANY SECTION
        data = util.json_read(filepath)

        try: data_horticulture = data['botany']
        except: data['botany'] = []

        if data['botany'] == []:
            prompt_paragraphs_num = 5
            prompt = f'''
                    Write {prompt_paragraphs_num} paragraphs in 400 words about the botanical aspects of {common_name} ({latin_name}).
                    In paragraph 1, tell me the taxonomy, including domain, kingdom, phylum, class, order, family, genus, species. Then, tell me the common names. Also, start paragraph 1 with the following words: "{common_name}, with botanical name {latin_name}, belongs to the domain ".
                    In paragraph 2, tell me the morphology.
                    In paragraph 3, tell me the variants names and their differences.
                    In paragraph 4, tell me the geographic distribution and natural habitats.
                    In paragraph 5, tell me the life-cycle.
                    Use the metric system.
                '''
            prompt = prompt_normalize(prompt)
            reply = gen_reply(prompt)
            reply_normalized = reply_normalize(reply)

            for paragraph in reply_normalized:
                print('***************************************')
                print(paragraph)
                print('***************************************')
            reply_paragraphs_num = len(reply_normalized)

            if len(reply_normalized) == prompt_paragraphs_num:
                data['botany'] = reply_normalized
                util.json_write(filepath, data)
            else:
                print(f'\n\n*** COULD NOT SAVE: paragraph num >> {reply_paragraphs_num} / {prompt_paragraphs_num} ***\n\n')

            running = True

            # break

    return running


def ai_gen_medicine_section():
    plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]

    cols = {}
    for i, item in enumerate(plants[0]):
        cols[item] = i

    plants = plants[1:]

    for plant in plants:
        latin_name = plant[cols['latin_name']].strip()
        common_name = plant[cols['common_name']].strip()

        latin_name_dash = latin_name.lower().replace(' ', '-')
        entity = latin_name_dash
        url = f'{entity}/medicine'

        filepath = f'database/articles/plants/{url}.json'



        # CREATE FOLDER
        chunks = filepath.split('/')
        chunk_curr = ''
        for chunk in chunks[:-1]:
            chunk_curr += chunk + '/'
            try: os.makedirs(f'{chunk_curr}')
            except: pass



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



        # MEDICINE SECTION
        data = util.json_read(filepath)

        try: data_medicine = data['benefits']
        except: data['benefits'] = []

        if data['benefits'] == []:
            # starting_text = f'{common_name.title()} has many health benefits, such as '
            prompt = f'''
                Explain in 5 paragraphs in 400 words the health benefits of {common_name}. 
            '''
                # Start with these words: {starting_text}
            prompt = prompt_normalize(prompt)
            reply = gen_reply(prompt)
            reply_normalized = reply_normalize(reply)

            # if not reply_normalized.startswith(f'{starting_text}'):
            #     reply_normalized += starting_text + reply_normalized

            for paragraph in reply_normalized:
                print('***************************************')
                print(paragraph)
                print('***************************************')
            reply_paragraphs_num = len(reply_normalized)

            data['benefits'] = reply_normalized
            util.json_write(filepath, data)

            running = True


def ai_gen_medicine_benefits_section():
    plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]

    cols = {}
    for i, item in enumerate(plants[0]):
        cols[item] = i

    plants = plants[1:]

    for plant in plants:
        latin_name = plant[cols['latin_name']].strip()
        common_name = plant[cols['common_name']].strip()

        latin_name_dash = latin_name.lower().replace(' ', '-')
        entity = latin_name_dash
        url = f'{entity}/medicine/benefits'

        filepath = f'database/articles/plants/{url}.json'



        # CREATE FOLDER
        chunks = filepath.split('/')
        chunk_curr = ''
        for chunk in chunks[:-1]:
            chunk_curr += chunk + '/'
            try: os.makedirs(f'{chunk_curr}')
            except: pass



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



        # MEDICINE BENEFITS SECTION
        data = util.json_read(filepath)

        try: data_medicine = data['benefits']
        except: data['benefits'] = []

        if data['benefits'] == []:
            prompt_paragraphs_num = 20
            prompt = f'''
                Write a numbered list of the {prompt_paragraphs_num} best health benefits of {common_name} ({latin_name}).
                Write only the names, not the descriptions.
                Write only 1 health benefit for list item.
                Use as few words as possible.
                Start each benefit with a third-person singular action verb. 
            '''
            prompt = prompt_normalize(prompt)
            reply = gen_reply(prompt)

            reply = reply.strip()
            reply_formatted = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if line[0].isdigit():
                    line = line.split('. ')[1].strip()
                    if line == '': continue
                    if ':' in line: line = line.split(':')[0].strip()
                    if '&' in line: line = line.split('&')[0].strip()
                    if 'and' in line: line = line.split('and')[0].strip()
                    if ',' in line: line = line.split(',')[0].strip()
                    reply_formatted.append({"benefit": line})

            if prompt_paragraphs_num == len(reply_formatted):
                for paragraph in reply_formatted:
                    print('***************************************')
                    print(paragraph)
                    print('***************************************')

                data['benefits'] = reply_formatted
                util.json_write(filepath, data)

            running = True


def ai_gen_medicine_benefits_definition_section():
    plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]

    cols = {}
    for i, item in enumerate(plants[0]):
        cols[item] = i

    plants = plants[1:]

    for plant in plants[:g.ARTICLES_NUM]:
        latin_name = plant[cols['latin_name']].strip()
        common_name = plant[cols['common_name']].strip()

        latin_name_dash = latin_name.lower().replace(' ', '-')
        entity = latin_name_dash
        url = f'{entity}/medicine/benefits'

        filepath = f'database/articles/plants/{url}.json'



        # CREATE FOLDER
        chunks = filepath.split('/')
        chunk_curr = ''
        for chunk in chunks[:-1]:
            chunk_curr += chunk + '/'
            try: os.makedirs(f'{chunk_curr}')
            except: pass



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



        # MEDICINE BENEFITS CONTENT
        data = util.json_read(filepath)

        benefits = []
        try: benefits = data['benefits']
        except: continue

        for benefit in benefits[:10]:
            benefit_name = benefit['benefit']
            
            benefit_definition = ''
            try: benefit_definition = benefit['definition']
            except: benefit['definition'] = ''

            if benefit_definition != '': continue

            starting_text = f'"{common_name.title()} {benefit_name.lower()}" refers to its '
            prompt = f'''
                    Define in detail in 1 sentence what "{common_name} {benefit_name}" means. 
                    Start the sentence with these words: {starting_text}
                '''

            prompt = prompt_normalize(prompt)
            reply = gen_reply(prompt)
            # reply = reply.replace('"', '')
            reply = reply.strip()
            reply = starting_text + reply
            
            print('***************************************')
            print(reply)
            print('***************************************')

            if reply != '':
                benefit['definition'] = reply
                util.json_write(filepath, data)





def ai_gen_medicine_benefits_constituents_section():
    running = False
    
    plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]

    cols = {}
    for i, item in enumerate(plants[0]):
        cols[item] = i

    plants = plants[1:]

    for index, plant in enumerate(plants[:g.ARTICLES_NUM]):
        print(index, '-', g.ARTICLES_NUM)
        latin_name = plant[cols['latin_name']].strip()
        common_name = plant[cols['common_name']].strip()

        latin_name_dash = latin_name.lower().replace(' ', '-')
        entity = latin_name_dash
        url = f'{entity}/medicine/benefits'

        filepath = f'database/articles/plants/{url}.json'



        # CREATE FOLDER
        chunks = filepath.split('/')
        chunk_curr = ''
        for chunk in chunks[:-1]:
            chunk_curr += chunk + '/'
            try: os.makedirs(f'{chunk_curr}')
            except: pass



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



        # MEDICINE BENEFITS CONTENT
        data = util.json_read(filepath)

        benefits = []
        try: benefits = data['benefits']
        except: continue

        for benefit in benefits[:10]:
            benefit_name = benefit['benefit']
            
            benefit_constituents = []
            try: benefit_constituents = benefit['constituents']
            except: benefit['constituents'] = []

            if benefit_constituents != []: continue
            running = True
            
            prompt_paragraphs_num = 10
            prompt = f'''
                Write a numbered list of the {prompt_paragraphs_num} most important medicinal constituents of the {latin_name} plant that help with this benefit: {benefit_name}. 
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

            if prompt_paragraphs_num == len(reply_formatted):
                benefit['constituents'] = reply_formatted
                util.json_write(filepath, data)

    return running


def ai_gen_medicine_benefits_constituents_text_section():
    running = False

    plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]
    cols = {}
    for i, item in enumerate(plants[0]):
        cols[item] = i
    plants = plants[1:]

    for index, plant in enumerate(plants[:g.ARTICLES_NUM]):
        print(index, '-', g.ARTICLES_NUM)
        latin_name = plant[cols['latin_name']].strip()
        common_name = plant[cols['common_name']].strip()

        latin_name_dash = latin_name.lower().replace(' ', '-')
        entity = latin_name_dash
        url = f'{entity}/medicine/benefits'

        filepath = f'database/articles/plants/{url}.json'



        # CREATE FOLDER
        chunks = filepath.split('/')
        chunk_curr = ''
        for chunk in chunks[:-1]:
            chunk_curr += chunk + '/'
            try: os.makedirs(f'{chunk_curr}')
            except: pass



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



        # MEDICINE BENEFIT CONSTITUENTS TEXT CONTENT
        data = util.json_read(filepath)

        benefits = []
        try: benefits = data['benefits']
        except: continue

        for benefit in benefits[:10]:
            benefit_name = benefit['benefit']
            
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

            # constituents = '- ' + '\n- '.join(benefit_constituents[:7])
            # prompt = f'''
            #     For each constituent in the following list:
            #     {constituents}

            #     Write 1 short sentence explaining why that constituent in {common_name} {benefit_name}.
            # '''

            prompt = prompt_normalize(prompt)
            reply = gen_reply(prompt)
            reply = reply.strip()
            
            paragraphs = reply.split('\n')
            # paragraphs_filtered = []
            # for paragraph in paragraphs:
            #     if paragraph[0].isdigit(): continue
            #     paragraphs_filtered.append(paragraph)
            
            if len(paragraphs) == 1:            
                print('***************************************')
                print(reply)
                print('***************************************')

                benefit['constituents_text'] = reply
                util.json_write(filepath, data)

    return running


def ai_gen_medicine_benefits_conditions_section():
    running = False

    plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]

    cols = {}
    for i, item in enumerate(plants[0]):
        cols[item] = i

    plants = plants[1:]

    for plant in plants[:g.ARTICLES_NUM]:
        latin_name = plant[cols['latin_name']].strip()
        common_name = plant[cols['common_name']].strip()

        latin_name_dash = latin_name.lower().replace(' ', '-')
        entity = latin_name_dash
        url = f'{entity}/medicine/benefits'

        filepath = f'database/articles/plants/{url}.json'



        # CREATE FOLDER
        chunks = filepath.split('/')
        chunk_curr = ''
        for chunk in chunks[:-1]:
            chunk_curr += chunk + '/'
            try: os.makedirs(f'{chunk_curr}')
            except: pass



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



        # CONTENT
        data = util.json_read(filepath)

        benefits = []
        try: benefits = data['benefits']
        except: continue

        for benefit in benefits[:10]:
            benefit_name = benefit['benefit']
            
            
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
                if line[0].isdigit() and '. ' in line:
                    line = '. '.join(line.split('. ')[1:]).strip()
                    if line == '': continue
                    if ':' in line: continue
                    if '&' in line: line = line.split('&')[0].strip()
                    if 'and' in line: line = line.split('and')[0].strip()
                    if ',' in line: line = line.split(',')[0].strip()
                    if '(' in line: line = line.split('(')[0].strip()
                    if '-' in line: line = line.split('-')[0].strip()
                    reply_formatted.append(line)
            
            print('***************************************')
            print(reply_formatted)
            print('***************************************')

            if prompt_paragraphs_num == len(reply_formatted):
                benefit['conditions'] = reply_formatted
                util.json_write(filepath, data)

    return running


def ai_gen_medicine_benefits_conditions_text_section():
    running = False
    plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]

    cols = {}
    for i, item in enumerate(plants[0]):
        cols[item] = i

    plants = plants[1:]

    for index, plant in enumerate(plants[:g.ARTICLES_NUM]):
        print(index, '-', g.ARTICLES_NUM)
        latin_name = plant[cols['latin_name']].strip()
        common_name = plant[cols['common_name']].strip()

        latin_name_dash = latin_name.lower().replace(' ', '-')
        entity = latin_name_dash
        url = f'{entity}/medicine/benefits'

        filepath = f'database/articles/plants/{url}.json'



        # CREATE FOLDER
        chunks = filepath.split('/')
        chunk_curr = ''
        for chunk in chunks[:-1]:
            chunk_curr += chunk + '/'
            try: os.makedirs(f'{chunk_curr}')
            except: pass



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



        # MEDICINE BENEFIT CONSTITUENTS TEXT CONTENT
        data = util.json_read(filepath)

        benefits = []
        try: benefits = data['benefits']
        except: continue

        for benefit in benefits[:10]:
            benefit_name = benefit['benefit']
            
            benefit_conditions = ''
            try: benefit_conditions = benefit['conditions']
            except: benefit['conditions'] = ''
            
            benefit_conditions_text = ''
            try: benefit_conditions_text = benefit['conditions_text']
            except: benefit['conditions_text'] = ''

            if benefit_conditions == []: continue
            if benefit_conditions_text != '': continue
            
            running = True

            conditions = ', '.join(benefit_conditions[:7])
            # starting_text = f'{common_name} '
            prompt = f'''
                Write a 60-word paragraph explaining how the fact that {common_name} {benefit_name.lower()} helps with the following conditions: {conditions}.
            '''
            prompt = prompt_normalize(prompt)
            reply = gen_reply(prompt)
            reply = reply.strip()
            
            paragraphs = reply.split('\n')
            paragraphs_filtered = []
            for paragraph in paragraphs:
                # if paragraph[0].isdigit(): continue
                if ': ' in paragraph:
                    paragraph = ': '.join(paragraph.split(': ')[1:])
                paragraphs_filtered.append(paragraph)

            if len(paragraphs_filtered) == 1:
                paragraphs_filtered = '\n'.join(paragraphs_filtered)
                print('***************************************')
                print(paragraphs_filtered)
                print('***************************************')

                benefit['conditions_text'] = paragraphs_filtered
                util.json_write(filepath, data)

    return running


#######################################################################
# ROOT >> MEDICINE
#######################################################################

def folder_create(filepath):
    chunks = filepath.split('/')
    chunk_curr = ''
    for chunk in chunks[:-1]:
        chunk_curr += chunk + '/'
        try: os.makedirs(f'{chunk_curr}')
        except: pass





def ai_entity_medicine_benefits(filepath):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    benefits_list = []
    try: benefits_list = data['benefits_list']
    except: data['benefits_list'] = []

    if benefits_list != []: return
    running = True

    prompt_paragraphs_num = 10
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} best health benefits of {latin_name} ({common_name}).
        Add descriptions to the health benefits.
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)

    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if line[0].isdigit():
            line = line.split('. ')[1].strip()
            if line == '': continue
            reply_formatted.append(line)

    if prompt_paragraphs_num == len(reply_formatted):
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')

        data['benefits_list'] = reply_formatted
        util.json_write(filepath, data)


def ai_entity_medicine_constituents(filepath):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    constituents_list = []
    try: constituents_list = data['constituents_list']
    except: data['constituents_list'] = []

    if constituents_list != []: return
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
        if line[0].isdigit():
            line = line.split('. ')[1].strip()
            if line == '': continue
            reply_formatted.append(line)

    if prompt_paragraphs_num == len(reply_formatted):
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')
        data['constituents_list'] = reply_formatted
        util.json_write(filepath, data)


def ai_entity_medicine_preparations(filepath):
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
        if line[0].isdigit():
            line = line.split('. ')[1].strip()
            if line == '': continue
            reply_formatted.append(line)

    if prompt_paragraphs_num == len(reply_formatted):
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')
        data['preparations_list'] = reply_formatted
        util.json_write(filepath, data)


def ai_entity_medicine():
    running = False

    for index, plant in enumerate(plants):
        print(index, '-', len(plants))

        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()

        entity = latin_name.lower().replace(' ', '-')
        url = f'{entity}/medicine'

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

        # BENEFITS
        # ai_entity_medicine_benefits(filepath)

        # CONSTITUENTS
        # ai_entity_medicine_constituents(filepath)

        # PREPARATIONS
        ai_entity_medicine_preparations(filepath)

    return running





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


running = True
while running:
    # ai_gen_medicine_benefits_definition_section()
    # running = ai_gen_medicine_benefits_constituents_section()
    # running = ai_gen_medicine_benefits_constituents_text_section()
    # running = ai_gen_medicine_benefits_conditions_section()
    # running = ai_gen_medicine_benefits_conditions_text_section()
    running = ai_entity_medicine()