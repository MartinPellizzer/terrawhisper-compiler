import csv
import os
import json
import re
from ctransformers import AutoModelForCausalLM
import random

import util


MODELS = [
    'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.1.Q8_0.gguf',
    'C:\\Users\\admin\\.cache\\lm-studio\\models\\mlabonne\\AlphaMonarch-7B-GGUF\\alphamonarch-7b.Q8_0.gguf',
]
MODEL = MODELS[1]

llm = AutoModelForCausalLM.from_pretrained(
    MODEL,
    model_type="mistral", 
    context_length=1024, 
    max_new_tokens=1024,
    )



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


running = True
while running:
    running = ai_gen_json()