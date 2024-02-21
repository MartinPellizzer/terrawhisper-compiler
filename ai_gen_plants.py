import csv
import os
import json
import re
from ctransformers import AutoModelForCausalLM
import random

import util


MODELS = [
    'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.1.Q8_0.gguf',
]
MODEL = MODELS[0]

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
        if ':' in paragraph: paragraph = paragraph.split(':')[1].strip()
        if paragraph.strip() == '': continue
        paragraphs_filtered.append(paragraph)
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

        try: 
            data = util.json_read(filepath)
        except: 
            data = {
                'latin_name': latin_name,
                'common_name': common_name,
                'title': f'{latin_name} ({common_name})',
                'medicine': [],
            }

        try: data_medicine = data['medicine']
        except: data['medicine'] = []

        # print(data['medicine'])

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
            
            if len(reply_normalized) == prompt_paragraphs_num:
                data['medicine'] = reply_normalized
                util.json_write(filepath, data)

            running = True

            # break

    return running


running = True
while running:
    running = ai_gen_json()