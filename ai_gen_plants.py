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


client = Groq(
    api_key='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',
)


MODELS = [
    'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.1.Q8_0.gguf',
    'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.2.Q8_0.gguf',
    'C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-3.Q8_0.gguf',
    'C:\\Users\\admin\\.cache\\lm-studio\\models\\TheBloke\\Starling-LM-7B-alpha-GGUF\\starling-lm-7b-alpha.Q8_0.gguf',
]
MODEL = MODELS[1]

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
   






#######################################################################
# ROOT
#######################################################################

def ai_entity_intro(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    intro = []
    try: intro = data['intro']
    except: data['intro'] = []

    if intro != []: return
    running = True

    prompt = f'''
        Write a 5-sentence paragraph about {latin_name} ({common_name}).

        In sentence 1, write the medicinal aspects.
        In sentence 2, write the horticulture aspects.
        In sentence 3, write the botanical aspects.
        In sentence 4, write the geographical aspects.
        In sentence 5, write the historical aspects.
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
        if ":" in line:
            line = line.split(':')[1].strip()
            if line == '': continue
        reply_formatted.append(line)

    if reply_formatted != '':
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')

        data['intro'] = reply_formatted
        util.json_write(filepath, data)

    return running


def ai_entity_medicine(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']
    
    try: data_medicine = data['medicine']
    except: data['medicine'] = []

    if data['medicine'] != []: return
    running = True

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

    return running


def ai_entity_horticolture(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: data_horticulture = data['horticulture']
    except: data['horticulture'] = []

    if data['horticulture'] != []: return
    running = True

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

    return running


def ai_entity_botany(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: data_horticulture = data['botany']
    except: data['botany'] = []

    if data['botany'] != []: return
    running = True

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

    return running


def ai_entity_main():
    running = False

    for index, plant in enumerate(plants):
        print(index, '-', len(plants))

        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()

        entity = latin_name.lower().replace(' ', '-')
        url = f'{entity}'

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

        # INTRO
        # running = ai_entity_intro(filepath, running)

        # MEDICINE
        running = ai_entity_medicine(filepath, running)

        # HORTICULTURE
        running = ai_entity_horticolture(filepath, running)

        # BOTANY
        running = ai_entity_botany(filepath, running)

    return running





#######################################################################
# ROOT >> MEDICINE
#######################################################################

def ai_entity_medicine_intro(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    intro = []
    try: intro = data['intro']
    except: data['intro'] = []

    if intro != []: return running
    running = True

    prompt = f'''
        Write a 5-sentence paragraph about the medicinal aspects of {latin_name} ({common_name}).

        In sentence 1, write the benefits.
        In sentence 2, write the constituents.
        In sentence 3, write the preparations.
        In sentence 4, write the side effects.
        In sentence 5, write the precautions.
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)

    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
        if ":" in line:
            line = ': '.join(line.split(':')[1:]).strip()
            if line == '': continue
        reply_formatted.append(line)

    if reply_formatted == '' or len(reply_formatted) == 1:
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')

        data['intro'] = reply_formatted
        util.json_write(filepath, data)

    return running


def ai_entity_medicine_constituents(filepath, running):
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


def ai_entity_medicine_preparations(filepath, running):
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


def ai_entity_medicine_side_effects(filepath, running):
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


def ai_entity_medicine_precautions(filepath, running):
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


def ai_entity_medicine_main():
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

        # INTRO
        running = ai_entity_medicine_intro(filepath, running)

        # BENEFITS
        ai_entity_medicine_benefits(filepath, running)

        # CONSTITUENTS
        ai_entity_medicine_constituents(filepath, running)

        # PREPARATIONS
        ai_entity_medicine_preparations(filepath, running)

        # SIDE EFFECTS
        ai_entity_medicine_side_effects(filepath, running)

        # PRECAUTIONS
        ai_entity_medicine_precautions(filepath, running)

    return running






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


def ai_entity_medicine_benefits_section(filepath, csv_benefits, running):
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


def ai_entity_medicine_benefits_definition(filepath, running):
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



def ai_entity_medicine_benefits_description_text(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']
    benefits = data['benefits']

    for benefit in benefits[]:
        benefit_name = benefit['benefit_name']
        
        benefit_desc = ''
        try: benefit_desc = benefit['benefit_desc']
        except: benefit['benefit_desc'] = benefit_desc

        if benefit_desc != '': continue
        running = True

        # starting_text = f'"{common_name.title()} {benefit_name.lower()}" refers to its ability to '
        prompt = f'''
                Write a 5-sentence paragraph about this health benefit of {latin_name.capitalize()} ({common_name}): {benefit_name}.
                In sentence 1, write a detailed definition of "{benefit_name}" in the context of {latin_name.capitalize()}.
                In sentence 2, write what are the main active constituents of {latin_name.capitalize()} that give this benefit.
                In sentence 3, write what are the primary parts of the {latin_name.capitalize()} plant that give this benefit.
                In sentence 4, write what are the main medicinal preparations of {latin_name.capitalize()} that give this benefit.
                In sentence 5, write what are the main health conditions that this benefit of {latin_name.capitalize()} helps relieve.
            '''
        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()
        # if starting_text.lower().strip() not in reply.lower():
            # reply = starting_text + reply 

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


def ai_entity_medicine_benefits_main():
    running = False

    for index, plant in enumerate(plants):
        print(index, '-', len(plants))

        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')
        url = f'{entity}/medicine/benefits'
        benefits = [row[1] for row in util.csv_get_rows_by_entity('database/tables/benefits.csv', entity)]

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

        # LIST
        # running = ai_entity_medicine_benefits_list(filepath)

        # BENEFITS SECTIONS
        # running = ai_entity_medicine_benefits_section(filepath, benefits, running)

        # BENEFITS DEFINITIONS
        # running = ai_entity_medicine_benefits_definition(filepath, running)

        # BENEFITS DESCRIPTIONS
        running = ai_entity_medicine_benefits_description_text(filepath, running)

        # BENEFIT CONSTITUENTS LIST
        # running = ai_entity_medicine_benefits_constituents_list(filepath, running)

        # BENEFIT CONSTITUENTS TEXT
        # running = ai_entity_medicine_benefits_constituents_text(filepath, running)

        # BENEFIT CONDITIONS LIST
        # running = ai_entity_medicine_benefits_conditions_list(filepath, running)

        # BENEFIT CONDITIONS TEXT
        # running = ai_entity_medicine_benefits_conditions_text(filepath, running)

    return running


running = True
while running:
    # running = ai_gen_medicine_benefits_definition_section()
    # running = ai_gen_medicine_benefits_constituents_section()
    # running = ai_gen_medicine_benefits_constituents_text_section()
    # running = ai_gen_medicine_benefits_conditions_section()
    # running = ai_gen_medicine_benefits_conditions_text_section()

    # running = ai_entity_main()
    # running = ai_entity_medicine_main()
    running = ai_entity_medicine_benefits_main()



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

        prompt_paragraphs_num = 10
        prompt = f'''
            Write a numbered list of the {prompt_paragraphs_num} best health benefits of {common_name} ({latin_name}).
            Start each benefit with a third-person singular action verb.
            Write only the names of the benefits, not the descriptions.
            Write each benefit name in less than 5 words.
        '''

        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()

        reply_formatted = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue 
            if line[0].isdigit():
                if '. ' in line: line = line.split('. ')[1].strip()
                if line == '': continue
                if line.endswith('.'): line = line[0:-1]
                reply_formatted.append([entity, line, ''])

        if prompt_paragraphs_num == len(reply_formatted):
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)


def ai_entity_medicine_constituents_csv():
    filepath = 'database/tables/constituents.csv'

    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')

        print(index, '-', len(plants), '>>' , latin_name, '|', 'constituents')

        rows = util.csv_get_rows_by_entity(filepath, entity)
        if rows != []: continue

        prompt_paragraphs_num = 10
        prompt = f'''
            Write a numbered list of the {prompt_paragraphs_num} best active constituents of {common_name} ({latin_name}).
            Write only the names of the medicinal constituents, not the descriptions.
        '''

        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()

        reply_formatted = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue 
            if line[0].isdigit():
                if '. ' in line: line = line.split('. ')[1].strip()
                if line == '': continue
                if line.endswith('.'): line = line[0:-1]
                reply_formatted.append([entity, line])

        if prompt_paragraphs_num == len(reply_formatted):
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)


def ai_entity_medicine_preparations_csv():
    llm = AutoModelForCausalLM.from_pretrained(
        MODEL,
        model_type="mistral", 
        context_length=1024, 
        max_new_tokens=1024,
        )

    filepath = 'database/tables/preparations.csv'

    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')

        print(index, '-', len(plants), '>>' , latin_name, '|', 'preparations')

        rows = util.csv_get_rows_by_entity(filepath, entity)
        if rows != []: continue

        prompt_paragraphs_num = 10
        prompt = f'''
            Write a numbered list of the {prompt_paragraphs_num} best medicinal preparations of {latin_name} ({common_name}), such as infusion and tincture.
            Write only the names of the preparations, don't add descriptions.
            Use as few words as possible.
        '''

        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()

        reply_formatted = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue 
            if line[0].isdigit():
                if '. ' in line: line = line.split('. ')[1].strip()
                if line == '': continue
                # if line.endswith('.'): line = line[0:-1]
                line = line.lower()
                line = line.replace(common_name.lower(), '')
                line = line.replace(latin_name.lower(), '')
                line = line.split('(')[0].strip()
                reply_formatted.append([entity, line, ''])

        if prompt_paragraphs_num == len(reply_formatted):
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)


def ai_entity_medicine_side_effects_csv():
    MODEL = MODELS[1]

    llm = AutoModelForCausalLM.from_pretrained(
        MODEL,
        model_type="mistral", 
        context_length=1024, 
        max_new_tokens=1024,
        )

    filepath = 'database/tables/side-effects.csv'

    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')

        print(index, '-', len(plants), '>>' , latin_name, '|', 'side effects')

        rows = util.csv_get_rows_by_entity(filepath, entity)
        if rows != []: continue

        prompt_paragraphs_num = 10
        prompt = f'''
            Write a numbered list of {prompt_paragraphs_num} possible side effects of {latin_name} ({common_name}) when used medicinally.
            Write only the names of the side effects, not the descriptions.
            Use as few words as possible.
        '''

        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()

        reply_formatted = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue 
            if line[0].isdigit():
                if '. ' in line: line = line.split('. ')[1].strip()
                if line == '': continue
                line = line.lower()
                line = line.replace(common_name.lower(), '')
                line = line.replace(latin_name.lower(), '')
                line = line.split('(')[0].strip()
                if line.endswith('.'): line = line[0:-1]
                reply_formatted.append([entity, line, ''])

        if prompt_paragraphs_num == len(reply_formatted):
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)


def ai_entity_medicine_precautions_csv():
    MODEL = MODELS[1]

    llm = AutoModelForCausalLM.from_pretrained(
        MODEL,
        model_type="mistral", 
        context_length=1024, 
        max_new_tokens=1024,
        )

    filepath = 'database/tables/precautions.csv'

    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')

        print(index, '-', len(plants), '>>' , latin_name, '|', 'precautions')

        rows = util.csv_get_rows_by_entity(filepath, entity)
        if rows != []: continue

        prompt_paragraphs_num = 10
        prompt = f'''
            Write a numbered list of {prompt_paragraphs_num} precautions to take when using {latin_name} ({common_name}) medicinally.
            Start each precautions with a third-person singular action verb.
            Write only the names of the precautions, not the descriptions.
            Write each precaution name in less than 5 words.
        '''

        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()

        reply_formatted = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue 
            if line[0].isdigit():
                if '. ' in line: line = line.split('. ')[1].strip()
                if line == '': continue
                line = line.lower()
                line = line.replace(common_name.lower(), '')
                line = line.replace(latin_name.lower(), '')
                line = line.split('(')[0].strip()
                if line.endswith('.'): line = line[0:-1]
                reply_formatted.append([entity, line, ''])

        if prompt_paragraphs_num == len(reply_formatted):
            print('***************************************')
            for line in reply_formatted:
                print(line)
            print('***************************************')

            util.csv_add_rows(filepath, reply_formatted)





def get_common_name(latin_name):
    filepath = 'database/tables/plants.csv'
    rows = util.csv_get_rows_by_entity(filepath, latin_name)
    common_name = [row[1] for row in rows][0].strip()
    return common_name



def ai_entity_medicine_benefits_description_list(entity):
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

        return running
    return running


def ai_entity_medicine_benefits_description_text(entity):
    running = False

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    benefits_text = ''
    try: benefits_text = data['benefits_text']
    except: data['benefits_text'] = ''

    if benefits_text != '':  return running
    running = True

    lst = []
    rows = util.csv_get_rows_by_entity('database/tables/benefits.csv', entity)
    benefits = [row[1] for row in rows]
    benefits_formatted = ', '.join(benefits)

    starting_text = f'{latin_name} ({common_name}) has '
    prompt = f'''
        Explain in a 5-sentence paragraph the following health benefits of {latin_name}: {benefits_formatted}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = starting_text + reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
        if ":" in line:
            line = ': '.join(line.split(':')[1:]).strip()
            if line == '': continue
        reply_formatted.append(line)

    if reply_formatted == '' or len(reply_formatted) == 1:
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')

        data['benefits_text'] = reply_formatted
        util.json_write(filepath, data)

    return running



def ai_entity_medicine_constituents_description_list(entity):
    
    running = False

    filepath = 'database/tables/constituents.csv'
    rows = util.csv_get_rows(filepath)
    
    if rows == []: return

    for i, row in enumerate(rows):
        if row[0].strip() != entity: continue

        entity = row[0].strip()
        constituent = row[1].strip().lower()
        description = row[2].strip()
        latin_name = entity.replace('-', ' ').capitalize()
        common_name = get_common_name(latin_name)

        if description != '': continue

        running = True

        starting_text = f'{latin_name} contains {constituent.title()}, which '
        prompt = f'''
            Explain in 1 sentence in detail why {constituent.title()} in {latin_name} is good for health.
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

        return running
    return running


def ai_entity_medicine_constituents_description_text(entity):
    running = False

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    constituents_text = ''
    try: constituents_text = data['constituents_text']
    except: data['constituents_text'] = ''

    if constituents_text != '':  return running
    running = True

    lst = []
    rows = util.csv_get_rows_by_entity('database/tables/constituents.csv', entity)
    constituents = [row[1] for row in rows]
    benefits_formatted = ', '.join(constituents)

    starting_text = f'{latin_name} ({common_name}) has several active constituents, '
    prompt = f'''
        Explain in a 5-sentence paragraph the following active constituents of {latin_name}: {benefits_formatted}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = starting_text + reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
        if ":" in line:
            line = ': '.join(line.split(':')[1:]).strip()
            if line == '': continue
        reply_formatted.append(line)

    if reply_formatted == '' or len(reply_formatted) == 1:
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')

        data['constituents_text'] = reply_formatted
        util.json_write(filepath, data)

    return running



def ai_entity_medicine_preparations_description_list(entity):
    
    running = False

    filepath = 'database/tables/preparations.csv'
    rows = util.csv_get_rows(filepath)
    
    if rows == []: return

    for i, row in enumerate(rows):
        if row[0].strip() != entity: continue

        entity = row[0].strip()
        preparations = row[1].strip().lower()
        description = row[2].strip()
        latin_name = entity.replace('-', ' ').capitalize()
        common_name = get_common_name(latin_name)

        if description != '': continue

        running = True

        starting_text = f'{latin_name} {preparations.title()} is '
        prompt = f'''
            Explain in 1 sentence in detail what are the health benefits of {latin_name.capitalize()} {preparations.title()}.
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

        return running
    return running


def ai_entity_medicine_preparations_description_text(entity):
    running = False

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    preparations_text = ''
    try: preparations_text = data['preparations_text']
    except: data['preparations_text'] = ''

    if preparations_text != '':  return running
    running = True

    lst = []
    rows = util.csv_get_rows_by_entity('database/tables/preparations.csv', entity)
    preparations = [row[1] for row in rows]
    benefits_formatted = ', '.join(preparations[:5])

    starting_text = f'{latin_name} ({common_name}) has many medicinal preparations, '
    prompt = f'''
        Explain in a 5-sentence paragraph what are the health benefits of the following medicinal preparations of {latin_name}: {benefits_formatted}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = starting_text + reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
        if ":" in line:
            line = ': '.join(line.split(':')[1:]).strip()
            if line == '': continue
        reply_formatted.append(line)

    if reply_formatted == '' or len(reply_formatted) == 1:
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')

        data['preparations_text'] = reply_formatted
        util.json_write(filepath, data)

    return running



def ai_entity_medicine_side_effects_description_list(entity):
    
    running = False

    filepath = 'database/tables/side-effects.csv'
    rows = util.csv_get_rows(filepath)
    
    if rows == []: return

    for i, row in enumerate(rows):
        if row[0].strip() != entity: continue

        entity = row[0].strip()
        side_effect = row[1].strip().lower()
        description = row[2].strip()
        latin_name = entity.replace('-', ' ').capitalize()
        common_name = get_common_name(latin_name)

        if description != '': continue

        running = True

        starting_text = f'{latin_name} may cause {side_effect.lower()} '
        prompt = f'''
            Explain in 1 sentence in detail why using {latin_name.capitalize()} improperly may cause {side_effect.title()}.
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

        return running
    return running


def ai_entity_medicine_side_effects_description_text(entity):
    running = False

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    side_effects_text = ''
    try: side_effects_text = data['side_effects_text']
    except: data['side_effects_text'] = ''

    if side_effects_text != '':  return running
    running = True

    lst = []
    rows = util.csv_get_rows_by_entity('database/tables/side-effects.csv', entity)
    side_effects = [row[1] for row in rows]
    lst = ', '.join(side_effects[:5])

    starting_text = f'{latin_name} ({common_name}) can have side effects if used improperly, '
    prompt = f'''
        Explain in a 5-sentence paragraph the following possible side effects of {latin_name}: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = starting_text + reply.strip()

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
        if ":" in line:
            line = ': '.join(line.split(':')[1:]).strip()
            if line == '': continue
        reply_formatted.append(line)

    if reply_formatted == '' or len(reply_formatted) == 1:
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')

        data['side_effects_text'] = reply_formatted
        util.json_write(filepath, data)

    return running



def ai_entity_medicine_precautions_description(entity):
    
    running = False

    filepath = 'database/tables/precautions.csv'
    rows = util.csv_get_rows(filepath)
    
    if rows == []: return

    for i, row in enumerate(rows):
        if row[0].strip() != entity: continue

        entity = row[0].strip()
        precaution = row[1].strip().lower()
        description = row[2].strip()
        latin_name = entity.replace('-', ' ').capitalize()
        common_name = get_common_name(latin_name)

        if description != '': continue

        running = True

        starting_text = f'{precaution.capitalize()} '
        prompt = f'''
            Explain in 1 sentence in detail why it is important to take the following precaution whe using {latin_name.capitalize()}: {precaution.title()}.
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
            reply = reply.replace(f' ({common_name.title()})', '')
            reply = reply.replace(f' ({common_name.lower()})', '')
            reply = reply.replace(f', also known as {common_name.title()},', '')
            reply = reply.replace(f', also known as {common_name.lower()},', '')
            reply_formatted.append(line)

        if len(reply_formatted) == 1:
            print('***************************************')
            for paragraph in reply_formatted:
                print(paragraph)
            print('***************************************')

            rows[i][2] = reply_formatted[0]
            util.csv_set_rows(filepath, rows)

        return running
    return running









# ai_entity_medicine_benefits_csv()
# ai_entity_medicine_constituents_csv()
# ai_entity_medicine_preparations_csv()
# ai_entity_medicine_side_effects_csv()
# ai_entity_medicine_precautions_csv()


for index, plant in enumerate(plants):
    print(index, '-', len(plants))

    latin_name = plant[cols['latin_name']].strip().capitalize()
    common_name = plant[cols['common_name']].strip().title()

    entity = latin_name.lower().replace(' ', '-')

    running = True
    while running:
        running = ai_entity_medicine_benefits_description_text(entity)
        running = ai_entity_medicine_benefits_description_list(entity)

        running = ai_entity_medicine_constituents_description_text(entity)
        running = ai_entity_medicine_constituents_description_list(entity)

        running = ai_entity_medicine_preparations_description_text(entity)
        running = ai_entity_medicine_preparations_description_list(entity)

        running = ai_entity_medicine_side_effects_description_list(entity)
        running = ai_entity_medicine_side_effects_description_text(entity)
        # running = ai_entity_medicine_precautions_description(entity)

# def article_clear_data():
#     filepath = 'database/articles/plants/achillea-millefolium/medicine.json'

# article_clear_data()




def json_entity_medicine(entity):
    rows = util.csv_get_rows_by_entity('database/tables/benefits.csv', entity)
    lst = [f'{row[1].title()}: {row[2]}' for row in rows]
    article_filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(article_filepath)
    data['benefits_list'] = lst
    data = util.json_write(article_filepath, data)

    rows = util.csv_get_rows_by_entity('database/tables/constituents.csv', entity)
    lst = [f'{row[1].title()}: {row[2]}' for row in rows]
    article_filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(article_filepath)
    data['constituents_list'] = lst
    data = util.json_write(article_filepath, data)

    rows = util.csv_get_rows_by_entity('database/tables/preparations.csv', entity)
    lst = [f'{row[1].title()}: {row[2]}' for row in rows]
    article_filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(article_filepath)
    data['preparations_list'] = lst
    data = util.json_write(article_filepath, data)

    rows = util.csv_get_rows_by_entity('database/tables/side-effects.csv', entity)
    lst = [f'{row[1].title()}: {row[2]}' for row in rows]
    article_filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(article_filepath)
    data['side_effects_list'] = lst
    data = util.json_write(article_filepath, data)

    rows = util.csv_get_rows_by_entity('database/tables/precautions.csv', entity)
    lst = [f'{row[1].title()}: {row[2]}' for row in rows]
    article_filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(article_filepath)
    data['precautions_list'] = lst
    data = util.json_write(article_filepath, data)



for index, plant in enumerate(plants):
    latin_name = plant[cols['latin_name']].strip().capitalize()
    common_name = plant[cols['common_name']].strip().title()
    entity = latin_name.lower().replace(' ', '-')

    json_entity_medicine(entity)

