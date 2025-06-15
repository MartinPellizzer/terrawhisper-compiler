import os
import time
import shutil
import json

import util

from lib import components
from lib import templates

from oliark_io import file_write
from oliark_io import json_read, json_write
from oliark_io import csv_read_rows_to_json
from oliark import img_resize, img_resize_save, tw_img_gen_web_herb_rnd
from oliark_llm import llm_reply

import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

import chromadb
from chromadb.utils import embedding_functions

vault = '/home/ubuntu/vault'
proj_name = 'terrawhisper'

model_8b = f'/home/ubuntu/vault-tmp/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
model_validator_filepath = f'llms/Llama-3-Partonus-Lynx-8B-Instruct-Q4_K_M.gguf'
model = model_8b

ailments = csv_read_rows_to_json('systems-organs-ailments.csv', debug=True)

header_html = components.header_2()
footer_html = components.footer_2()

checkpoint_filepath = f'{vault}/stable-diffusion/checkpoints/juggernautXL_juggXIByRundiffusion.safetensors'
pipe = StableDiffusionXLPipeline.from_single_file(
    checkpoint_filepath, 
    torch_dtype=torch.float16, 
    use_safetensors=True, 
    variant="fp16"
).to('cuda')
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

db_path = f'{vault}/{proj_name}/database/{proj_name}'
chroma_client = chromadb.PersistentClient(path=db_path)
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='all-mpnet-base-v2', 
    device='cuda',
)

def llm_validate(question, context, answer):
    prompt = f'''
    Given the following QUESTION, DOCUMENT and ANSWER you must analyze the provided answer and determine whether it is faithful to the contents of the DOCUMENT. The ANSWER must not offer new information beyond the context provided in the DOCUMENT. The ANSWER also must not contradict information provided in the DOCUMENT. Output your final verdict by strictly following this format: "PASS" if the answer is faithful to the DOCUMENT and "FAIL" if the answer is not faithful to the DOCUMENT. Show your reasoning.

    --
    QUESTION (THIS DOES NOT COUNT AS BACKGROUND INFORMATION):
    {question}

    --
    DOCUMENT:
    {context}

    --
    ANSWER:
    {answer}

    --

    Your output should be in JSON FORMAT with the keys "REASONING" and "SCORE":
    {{"REASONING": <your reasoning as bullet points>, "SCORE": <your final score>}}
    '''
    reply = llm_reply(prompt, model_validator_filepath, max_tokens=256)
    return reply

def herbs_book():
    _herbs = csv_read_rows_to_json(f'database/csv/herbs-book.csv')
    start_time = time.time()
    for herb_i, herb in enumerate(_herbs[:]):
        print()
        print('***********************')
        print('***********************')
        print(f'{herb_i}/{len(_herbs)} - {herb}')
        print('***********************')
        print('***********************')
        print()
        art_herb_popular(herb, herb_i, _herbs)
        # art_herb_popular_validate(herb, herb_i, _herbs)
    end_time = time.time()
    print(f'total execution time in seconds: {(end_time - start_time)}')
    print(f'total execution time in minutes: {(end_time - start_time)/60}')
    print(f'total execution time in hours: {(end_time - start_time)/3600}')

def main_herbs_popular():
    _herbs = []
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        data = json_read(json_filepath, create=True)
        for obj in data['herbs']:
            found = False
            for herb in _herbs:
                if obj['plant_name_scientific'] == herb['plant_name_scientific']:
                    herb['confidence_score'] += obj['confidence_score']
                    found = True
                    break
            if not found:
                _herbs.append(obj)
    _herbs = sorted(_herbs, key=lambda x: x['confidence_score'], reverse=True)
    _ = llm_reply('', model)
    start_time = time.time()
    for herb_i, herb in enumerate(_herbs[:]):
        print()
        print('***********************')
        print('***********************')
        print(f'{herb_i}/{len(_herbs)} - {herb}')
        print('***********************')
        print('***********************')
        print()
        art_herb_popular(herb, herb_i, _herbs)
        # art_herb_popular_validate(herb, herb_i, _herbs)
    end_time = time.time()
    print(f'total execution time in seconds: {(end_time - start_time)}')
    print(f'total execution time in minutes: {(end_time - start_time)/60}')
    print(f'total execution time in hours: {(end_time - start_time)/3600}')

def art_herb_popular(herb, herb_i, herbs):
    herb_name_scientific = herb['plant_name_scientific']
    herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
    url = f'herbs/{herb_slug}'
    json_filepath = f'database/json/{url}.json'
    html_filepath = f'website/{url}.html'
    title = f'What to know about {herb_name_scientific} before using it medicinally'
    '''
    if os.path.exists(json_filepath): os.remove(json_filepath)
    return 
    '''
    data = json_read(json_filepath, create=True)
    data['herb_slug'] = herb_slug
    data['herb_name_scientific'] = herb_name_scientific
    data['url'] = url
    if 'lastmod' not in data: data['lastmod'] = today()
    data['title'] = title
    json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## database generation for validation
    ## to remove when done
    ## ------------------------------------------------------------------------------------
    _json_filepath = 'database/plant-parts-filtered.json'
    parts = json_read(_json_filepath, create=True)
    if 0:
        prompt = f'''
            Write a list of the most important parts of the plant {herb_name_scientific} that are used for medicinal purposes.
            Choose only from these parts: roots, stems, leaves, flowers, fruits, and seeds.
            Don't include constituents, like: flavonoids, tannins, oils, etc.
            Write only the names of the parts, don't add descriptions.
            Don't include the name of the plant, only write the names of the parts.
            Write as few words as possible.
            Don't write fluff, only proven facts.
            Don't allucinate.
            Reply in JSON format using the following structure:
            [
                {{"part_name": "<insert name of part 1 here>"}},
                {{"part_name": "<insert name of part 2 here>"}},
                {{"part_name": "<insert name of part 3 here>"}}
            ]
            Reply only with the JSON, don't add additional content.
        '''
        reply = llm_reply(prompt, model).strip().lower()
        try: _parts = json.loads(reply)
        except: _parts = ''
        if _parts != '':
            for _part in _parts:
                found = False
                for part in parts:
                    if _part['part_name'] in part['part_name']:
                        found = True
                        break
                if not found:
                    parts.append({'part_name': _part['part_name']})
        json_write(_json_filepath, parts)
        return

    if 0:
        _json_filepath = 'database/preparations-test.json'
        preparations = json_read(_json_filepath)
        prompt = f'''
            Write a list of the most important medicinal preparations of the plant {herb_name_scientific}.
            Example of medicinal preparations are: teas, tincures, decoctions, salves, essential oils, creams, etc.
            Write only the names of the preparations, don't add descriptions.
            Don't include the name of the plants, only write the names of the preparations.
            Write as few words as possible.
            Don't write fluff, only proven facts.
            Don't allucinate.
            Reply in JSON format using the following structure:
            [
                {{"preparation_name": "<insert name of preparation 1 here>"}},
                {{"preparation_name": "<insert name of preparation 2 here>"}},
                {{"preparation_name": "<insert name of preparation 3 here>"}}
            ]
            Reply only with the JSON, don't add additional content.
        '''
        reply = llm_reply(prompt, model).strip().lower()
        try: _preparations = json.loads(reply)
        except: _preparations = ''
        if _preparations != '':
            for _preparation in _preparations:
                found = False
                for preparation in preparations:
                    if _preparation['preparation_name'] in preparation['preparation_name']:
                        found = True
                        break
                if not found:
                    preparations.append({'preparation_name': _preparation['preparation_name']})
        json_write(_json_filepath, preparations)
        return

    ## ----------------------------------------------------------------------------------------------
    ## ;common names
    ## ------------------------------------------------------------------------------------
    key = 'common_names'
    if key not in data: data[key] = []
    # data[key] = ''
    if data[key] == []:
        outputs = []
        for i in range(20):
            print(f'{i}/20 - {herb_i}/{len(herbs)}: {herb}')
            prompt = f'''
                Write a list of the common names of the plant {herb_name_scientific}.
                Write only 1 name for each list item.
                Write only the names, don't add descriptions.
                Write the as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the structure in the following example:
                [
                    {{"common_name": "<insert name of name 1 here>", "confidence_score": "10"}},
                    {{"common_name": "<insert name of name 2 here>", "confidence_score": "5"}},
                    {{"common_name": "<insert name of name 3 here>", "confidence_score": "7"}}
                ]
                Reply only with the JSON, don't add additional content.
            '''
            reply = llm_reply(prompt, model).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                names = []
                for item in json_data:
                    try: name = item['common_name']
                    except: continue
                    try: score = item['confidence_score']
                    except: continue
                    print(name)
                    ## TODO: check if constituent is valid here (find database of conditions?)
                    names.append({"name": name, "score": score})
                for obj in names:
                    name = obj['name'].lower().strip()
                    score = obj['score']
                    found = False
                    for output in outputs:
                        print(output)
                        print(name, '->', output['common_name'])
                        if name in output['common_name']: 
                            output['mentions'] += 1
                            output['score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'common_name': name, 
                            'mentions': 1, 
                            'score': int(score), 
                        })
            outputs_final = []
            for output in outputs:
                outputs_final.append({
                    'common_name': output['common_name'],
                    'score': int(output['mentions']) * int(output['score']),
                })
            outputs_final = sorted(outputs_final, key=lambda x: x['score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output in outputs_final:
                print(output)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = outputs_final[:10]
            json_write(json_filepath, data)

    ## ;uses ----------------------------------------------------------------------------------------------
    medicinal_systems = [
        'modern western medicine',
        'traditional chinese medicine',
        'ayurvedic medicine',
        'unani medicine',
        'homeopathic medicine',
    ]

    if 0:
        for medicinal_system in medicinal_systems:
            medicinal_system_dash = medicinal_system.replace(' ', '-')
            medicinal_system_underline = medicinal_system.replace(' ', '_')
            key = f'uses_{medicinal_system_underline}'
            if key in data: del data[key]
            json_write(json_filepath, data)
        return

    # ;uses data
    for medicinal_system in medicinal_systems:
        medicinal_system_dash = medicinal_system.replace(' ', '-')
        medicinal_system_underline = medicinal_system.replace(' ', '_')
        key = f'uses_{medicinal_system_underline}'
        if key not in data: data[key] = []
        # data[key] = ''
        if data[key] == []:
            outputs = []
            for i in range(20):
                print(f'{i}/20 - {herb_i}/{len(herbs)}: {herb} - {key}')
                prompt = f'''
                    Write a list of the 10 most common uses of the plant {herb_name_scientific} in {medicinal_system}.
                    By "uses" I mean health conditions (common ailments).
                    Also, give a confidence score in number format from 1 to 10 for each condition representing how much {herb_name_scientific} is used in {medicinal_system}.
                    Write only 1 ailment for each list item.
                    Write only the names of the conditions, don't add descriptions.
                    Write the as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in JSON format using the structure in the following example:
                    [
                        {{"condition_name": "<insert name of condition 1 here>", "confidence_score": "10"}},
                        {{"condition_name": "<insert name of condition 2 here>", "confidence_score": "5"}},
                        {{"condition_name": "<insert name of condition 3 here>", "confidence_score": "7"}}
                    ]
                    Reply only with the JSON, don't add additional content.
                '''
                prompt = f'''
                    Write a list of the 10 most common ailments the plant {herb_name_scientific} can help.
                    Also, give a confidence score in number format from 1 to 10 for each ailment representing how much {herb_name_scientific} is used in {medicinal_system}.
                    Write only 1 ailment for each list item.
                    Never write the word "and".
                    Write only the names of the conditions, don't add descriptions.
                    Write the as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in JSON format using the structure in the following example:
                    [
                        {{"condition_name": "<insert name of condition 1 here>", "confidence_score": "10"}},
                        {{"condition_name": "<insert name of condition 2 here>", "confidence_score": "5"}},
                        {{"condition_name": "<insert name of condition 3 here>", "confidence_score": "7"}}
                    ]
                    Reply only with the JSON, don't add additional content.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names = []
                    for item in json_data:
                        try: name = item['condition_name']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        names.append({"name": name, "score": score})
                    for obj in names:
                        name = obj['name'].lower().strip()
                        score = obj['score']
                        found = False
                        for output in outputs:
                            if name in output['name']: 
                                output['mentions'] += 1
                                output['score'] += int(score)
                                found = True
                                break
                        if not found:
                            outputs.append({
                                'name': name, 
                                'mentions': 1, 
                                'score': int(score), 
                            })
            outputs_final = []
            for output in outputs:
                outputs_final.append({
                    'name': output['name'],
                    'score': int(output['mentions']) * int(output['score']),
                })
            outputs_final = sorted(outputs_final, key=lambda x: x['score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output in outputs_final:
                print(output)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = outputs_final[:20]
            json_write(json_filepath, data)
    conditions_best = []
    for medicinal_system in medicinal_systems:
        medicinal_system_dash = medicinal_system.replace(' ', '-')
        medicinal_system_underline = medicinal_system.replace(' ', '_')
        for obj in data[f'uses_{medicinal_system_underline}']:
            found = False
            for _obj in conditions_best:
                if _obj['name'] in obj['name']:
                    _obj['score'] += obj['score']
                    found = True
                    break
            if not found:
                conditions_best.append(obj)
    conditions_best = sorted(conditions_best, key=lambda x: x['score'], reverse=True)
    conditions_best = [x['name'] for x in conditions_best[:10]]

    ## ;benefits ----------------------------------------------------------------------------------------------
    body_systems = [
        'circulatory',
        'digestive',
        'endocrine',
        'integumentary',
        'lymphatic',
        'musculoskeletal',
        'nervous',
        'reproductive',
        'respiratory',
        'urinary',
    ]

    if 0:
        key = f'benefits'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        for body_system in body_systems:
            key = f'benefits_{body_system}_system'
            if key in data: del data[key]
            json_write(json_filepath, data)
        return
    if 0:
        for body_system in body_systems:
            key = f'benefits_{body_system}_system_ailments'
            if key in data: del data[key]
            json_write(json_filepath, data)
        return

    key = 'benefits'
    if key not in data: data[key] = []
    # data[key] = ''
    if data[key] == []:
        print(f'{herb_i}/{len(herbs)}: {herb} - {key}')
        prompt = f'''
            Write a list of the 10 most important health benefits of the plant {herb_name_scientific}.
            Write only 1 benefit for each list item.
            Write only the names of the benefits, don't add descriptions.
            Start each list item with a third-person singular action verb.
            End each list item with the rest of the benefit.
            Make each benefit name at least 2-word long.
            Write the as few words as possible.
            Don't write fluff, only proven facts.
            Don't allucinate.
            Reply in JSON format using the following structure:
            [
                {{"benefit_name": "<insert name of benefit 1 here>"}},
                {{"benefit_name": "<insert name of benefit 2 here>"}},
                {{"benefit_name": "<insert name of benefit 3 here>"}}
            ]
            Reply only with the JSON, don't add additional content.
        '''
        reply = llm_reply(prompt, model).strip()
        try: _data = json.loads(reply)
        except: _data = ''
        if data != '':
            _names = []
            for _obj in _data:
                if 'benefit_name' in _obj:
                    _names.append({'name': _obj['benefit_name']})
            data[key] = _names[:20]
            json_write(json_filepath, data)

    for body_system in body_systems:
        key = f'benefits_{body_system}_system'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            print(f'{herb_i}/{len(herbs)}: {herb} - {key}')
            prompt = f'''
                Write a list of the 10 most important health benefits of the plant {herb_name_scientific} for the {body_system} system.
                Write only 1 benefit for each list item.
                Write only the names of the benefits, don't add descriptions.
                Include an action verb in each benefit name.
                Make each benefit name at least 2-word long.
                Write the as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the following structure:
                [
                    {{"benefit_name": "<insert name of benefit 1 here>"}},
                    {{"benefit_name": "<insert name of benefit 2 here>"}},
                    {{"benefit_name": "<insert name of benefit 3 here>"}}
                ]
                Reply only with the JSON, don't add additional content.
            '''
            reply = llm_reply(prompt, model).strip()
            try: _data = json.loads(reply)
            except: _data = ''
            if data != '':
                data[key] = _data[:20]
                json_write(json_filepath, data)

        key = f'benefits_{body_system}_system_ailments'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            print(f'{herb_i}/{len(herbs)}: {herb} - {key}')
            prompt = f'''
                Write a list of the most common uses of the plant {herb_name_scientific} for the {body_system} system.
                By "uses" I mean health conditions (common ailments).
                Also, give a confidence score in number format from 1 to 10 for each condition representing how much you are sure {herb_name_scientific} can help treating that condition.
                Write only 1 ailment for each list item.
                Write only the names of the conditions, don't add descriptions.
                Write the as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the structure in the following example:
                [
                    {{"condition_name": "<insert name of condition 1 here>", "confidence_score": "10"}},
                    {{"condition_name": "<insert name of condition 2 here>", "confidence_score": "5"}},
                    {{"condition_name": "<insert name of condition 3 here>", "confidence_score": "7"}}
                ]
                Reply only with the JSON, don't add additional content.
            '''
            reply = llm_reply(prompt, model).strip()
            try: json_data = json.loads(reply)
            except: json_data = {} 
            if json_data != {}:
                names = []
                for item in json_data:
                    try: name = item['condition_name']
                    except: continue
                    try: score = item['confidence_score']
                    except: continue
                    names.append({"name": name, "score": score})
                data[key] = names[:20]
                json_write(json_filepath, data)


    ## ;properties ----------------------------------------------------------------------------------------------
    if 0:
        key = f'properties'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return

    key = 'properties'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        print(f'{herb_i}/{len(herbs)}: {herb} - {key}')
        prompt = f'''
            Write a list of the most important medicinal properties of the plant {herb_name_scientific}.
            Examples of properties are: antimicrobial, antioxidant, anti-inflammatory, analgesic, pain relief, etc.
            Write only the names of the properties, don't add descriptions.
            Write as few words as possible.
            Don't write fluff, only proven facts.
            Don't allucinate.
            Reply in JSON format using the following structure:
            [
                {{"property_name": "<insert name of property 1 here>"}},
                {{"property_name": "<insert name of property 2 here>"}},
                {{"property_name": "<insert name of property 3 here>"}}
            ]
            Reply only with the JSON, don't add additional content.
        '''
        reply = llm_reply(prompt, model).strip().lower()
        try: _data = json.loads(reply)
        except: _data = ''
        if data != '':
            data[key] = _data[:20]
            json_write(json_filepath, data)

    ## ;constituents ----------------------------------------------------------------------------------------------
    if 0:
        key = f'constituents'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return

    key = 'constituents'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        outputs = []
        for i in range(20):
            print(f'{i}/20 - {herb_i}/{len(herbs)}: {herb}')
            prompt = f'''
                Write a list of the 10 best medicinal constituents of the plant {herb_name_scientific}.
                Also, give a confidence score in number format from 1 to 10 for each medicinal constituent representing how much you are sure that medicinal constituent is contained in the plant {herb_name_scientific}.
                Examples of medicinal constituents are: flavonoids, phenolic acids, saponins, etc.
                Write only the names of the constituents, don't add descriptions.
                Write the names of the constituents using as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the structure in the following example:
                [
                    {{"constituent_name": "<insert name of constituent 1 here>", "confidence_score": "10"}},
                    {{"constituent_name": "<insert name of constituent 2 here>", "confidence_score": "5"}},
                    {{"constituent_name": "<insert name of constituent 3 here>", "confidence_score": "7"}}
                ]
                Reply only with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                names = []
                for item in json_data:
                    try: name = item['constituent_name']
                    except: continue
                    try: score = item['confidence_score']
                    except: continue
                    names.append({"name": name, "score": score})
                for obj in names:
                    name = obj['name']
                    score = obj['score']
                    found = False
                    for output in outputs:
                        if name in output['name']: 
                            output['mentions'] += 1
                            output['score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'name': name, 
                            'mentions': 1, 
                            'score': int(score), 
                        })
            outputs_final = []
            for output in outputs:
                outputs_final.append({
                    'name': output['name'],
                    'score': int(output['mentions']) * int(output['score']),
                })
            outputs_final = sorted(outputs_final, key=lambda x: x['score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output in outputs_final:
                print(output)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = outputs_final[:20]
            json_write(json_filepath, data)

    ## ;parts ----------------------------------------------------------------------------------------------
    valid_parts = [
        'roots',
        'rhizomes',
        'stems',
        'leaves',
        'flowers',
        'fruits',
        'seeds',
    ]

    if 0:
        key = f'parts'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return

    key = 'parts'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        valid_parts_prompt = ', '.join(valid_parts)
        outputs = []
        tries_num = 20
        for i in range(tries_num):
            print(f'{i}/{tries_num} - {herb_i}/{len(herbs)}: {herb}')
            prompt = f'''
                Write a list of the most important parts of the plant {herb_name_scientific} that are used for medicinal purposes.
                For each part, give the following scores:
                - a presence score, in number format from 1 to 10 representing how much you believe {herb_name_scientific} has this part.
                - a health score, in number format from 1 to 10 representing how much you believe {herb_name_scientific} this part is good for health when used medicinally.
                - a usage score, in number format from 1 to 10 representing how common is to use this part of {herb_name_scientific} as a medicinal ingredient compared to other parts of the same plant.
                - a power score, in number format from 1 to 10 representing how strong is the effect of this part of {herb_name_scientific} as a medicinal ingredient compared to other parts of the same plant.
                Choose only from these parts: {valid_parts_prompt}.
                Always write the names of the parts in plural form, for example: Write leaves, not leaf.
                Write only the names of the parts, don't add descriptions.
                Don't include the name of the plant, only write the parts.
                Write the as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the structure in the following example:
                [
                    {{"part_name": "<insert name of part 1 here>", "presence_score": 10, "health_score": "9", "usage_score": 8, "power_score: 9"}},
                    {{"part_name": "<insert name of part 2 here>", "presence_score": 5, "health_score": "4", "usage_score": 2, "power_score: 6"}},
                    {{"part_name": "<insert name of part 3 here>", "presence_score": 7, "health_score": "6", "usage_score": 8, "power_score: 5"}}
                ]
                Reply only with the JSON, don't add additional content.
            '''
            reply = llm_reply(prompt, model).strip()
            try: json_data = json.loads(reply)
            except: json_data = '' 
            if json_data != '':
                parts = []
                for item in json_data:
                    try: name = item['part_name'].lower().strip()
                    except: continue
                    try: presence_score = item['presence_score']
                    except: continue
                    try: health_score = item['health_score']
                    except: continue
                    try: usage_score = item['usage_score']
                    except: continue
                    try: power_score = item['power_score']
                    except: continue
                    if name in valid_parts:
                        parts.append({
                            "name": name, 
                            "presence_score": presence_score, 
                            "health_score": health_score, 
                            "usage_score": usage_score, 
                            "power_score": power_score,
                        })
                for obj in parts:
                    name = obj['name'].lower().strip()
                    presence_score = obj['presence_score']
                    health_score = obj['health_score']
                    usage_score = obj['usage_score']
                    power_score = obj['power_score']
                    found = False
                    for output in outputs:
                        if name in output['name']: 
                            output['mentions'] += 1
                            output['presence_score'] += int(presence_score)
                            output['health_score'] += int(health_score)
                            output['usage_score'] += int(usage_score)
                            output['power_score'] += int(power_score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'name': name, 
                            'mentions': 1, 
                            'presence_score': int(presence_score), 
                            'health_score': int(health_score), 
                            'usage_score': int(usage_score), 
                            'power_score': int(power_score), 
                        })
        outputs_final = []
        for output in outputs:
            mentions = output['mentions']
            avg_presence_score = output['presence_score']/tries_num
            avg_health_score = output['health_score']/tries_num
            avg_usage_score = output['usage_score']/tries_num
            avg_power_score = output['power_score']/tries_num
            total_score = ((avg_presence_score + avg_health_score + avg_usage_score + avg_power_score)/4) * mentions/tries_num
            outputs_final.append({
                'name': output['name'],
                'mentions': mentions, 
                'presence_score': round(avg_presence_score, 2),
                'health_score': round(avg_health_score, 2),
                'usage_score': round(avg_usage_score, 2),
                'power_score': round(avg_power_score, 2),
                'total_score': round(total_score, 2),
            })
        print(outputs_final)
        outputs_final = sorted(outputs_final, key=lambda x: x['total_score'], reverse=True)
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs_final:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        data[key] = outputs_final[:20]
        json_write(json_filepath, data)

    ## ;preparations ----------------------------------------------------------------------------------------------
    score_min = 5
    valid_preparations = json_read('database/preparations.json')
    valid_preparations = [x['preparation_name'].split(',')[0].strip().lower() for x in valid_preparations if x['preparation_name'].split(',')[0].strip() != '']

    if 0:
        key = f'preparations'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return

    key = 'preparations'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        outputs = []
        tries_num = 20
        for i in range(tries_num):
            print(f'{i}/{tries_num} - {herb_i}/{len(herbs)}: {herb}')
            prompt = f'''
                Write a list of the most effective herbal preparations of the plant {herb_name_scientific} for medicinal purposes.
                For each preparation, give the following scores:
                - a difficulty score, in number format from 1 to 10 representing how much you believe that preparation {herb_name_scientific} is difficult to make.
                - a health score, in number format from 1 to 10 representing how much you believe that preparation with {herb_name_scientific} is good for health when used medicinally.
                - a usage score, in number format from 1 to 10 representing how common is to use that preparation with {herb_name_scientific} for medicinal purposes compared to other preparations made with the same plant.
                - a power score, in number format from 1 to 10 representing how strong is the effect of that preparation with {herb_name_scientific} for medicinal purposes compared to other preparations made with the same plant.
                Always write the names of the preparations in singular form.
                Write only the names of the preparations, don't add descriptions.
                Don't include the name of the plant, only write the names of the preparations.
                Write the as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the structure in the following example:
                [
                    {{"preparation_name": "<insert name of preparation 1 here>", "difficulty_score": 10, "health_score": "9", "usage_score": 8, "power_score: 9"}},
                    {{"preparation_name": "<insert name of preparation 2 here>", "difficulty_score": 5, "health_score": "4", "usage_score": 2, "power_score: 6"}},
                    {{"preparation_name": "<insert name of preparation 3 here>", "difficulty_score": 7, "health_score": "6", "usage_score": 8, "power_score: 5"}}
                ]
                Reply only with the JSON, don't add additional content.
            '''
            reply = llm_reply(prompt, model).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                preparations = []
                for item in json_data:
                    try: name = item['preparation_name'].lower().strip()
                    except: continue
                    try: difficulty_score = item['difficulty_score']
                    except: continue
                    try: health_score = item['health_score']
                    except: continue
                    try: usage_score = item['usage_score']
                    except: continue
                    try: power_score = item['power_score']
                    except: continue
                    if name.strip() == '': continue
                    for valid_preparation in valid_preparations:
                        if valid_preparation.lower().strip() in name.lower().strip():
                            preparations.append({
                                "preparation_name": valid_preparation, 
                                "preparation_difficulty_score": difficulty_score, 
                                "preparation_health_score": health_score, 
                                "preparation_usage_score": usage_score, 
                                "preparation_power_score": power_score,
                            })
                            break
                for obj in preparations:
                    name = obj['preparation_name'].lower().strip()
                    difficulty_score = obj['preparation_difficulty_score']
                    health_score = obj['preparation_health_score']
                    usage_score = obj['preparation_usage_score']
                    power_score = obj['preparation_power_score']
                    found = False
                    for output in outputs:
                        if name in output['preparation_name']: 
                            output['preparation_mentions'] += 1
                            output['preparation_difficulty_score'] += int(difficulty_score)
                            output['preparation_health_score'] += int(health_score)
                            output['preparation_usage_score'] += int(usage_score)
                            output['preparation_power_score'] += int(power_score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'preparation_name': name, 
                            'preparation_mentions': 1, 
                            'preparation_difficulty_score': int(difficulty_score), 
                            'preparation_health_score': int(health_score), 
                            'preparation_usage_score': int(usage_score), 
                            'preparation_power_score': int(power_score), 
                        })
        outputs_final = []
        for output in outputs:
            mentions = output['preparation_mentions']
            total_score = ((output['preparation_difficulty_score']/tries_num + output['preparation_health_score']/tries_num + output['preparation_usage_score']/tries_num + output['preparation_power_score']/tries_num) / 3)
            avg_difficulty_score = output['preparation_difficulty_score']/mentions
            avg_health_score = output['preparation_health_score']/mentions
            avg_usage_score = output['preparation_usage_score']/mentions
            avg_power_score = output['preparation_power_score']/mentions
            outputs_final.append({
                'preparation_name': output['preparation_name'],
                'preparation_mentions': mentions, 
                'preparation_difficulty_score': round(avg_difficulty_score, 2),
                'preparation_health_score': round(avg_health_score, 2),
                'preparation_usage_score': round(avg_usage_score, 2),
                'preparation_power_score': round(avg_power_score, 2),
                'preparation_total_score': round(total_score, 2),
            })
        outputs_final = sorted(outputs_final, key=lambda x: x['preparation_total_score'], reverse=True)
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs_final:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        if outputs_final != []:
            data[key] = outputs_final[:]
        else:
            data[key] = ''
        json_write(json_filepath, data)

    ## ;side_effects ----------------------------------------------------------------------------------------------
    if 0:
        key = f'side_effects'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return

    key = 'side_effects'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        prompt = f'''
            Write a list of 10 possible side effects of impropertly using the plant {herb_name_scientific} medicinally.
            Write only the names of the side effects, don't add descriptions.
            Start each list item with a third-person singular actionable verb.
            Don't write fluff, only proven data.
            Don't allucinate.
            Reply in JSON format using the following structure:
            [
                {{"side_effect_name": "<insert name of side_effect 1 here>"}},
                {{"side_effect_name": "<insert name of side_effect 2 here>"}},
                {{"side_effect_name": "<insert name of side_effect 3 here>"}}
            ]
            Reply only with the JSON, don't add additional content.
        '''
        reply = llm_reply(prompt, model).strip()
        try: _data = json.loads(reply)
        except: _data = ''
        if _data != '':
            data[key] = _data[:20]
            json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## ;precautions
    ## ----------------------------------------------------------------------------------------------
    if 0:
        key = f'precautions'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return

    key = 'precautions'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        prompt = f'''
            Write a list of 10 precautions to take when using the {herb_name_scientific} plant medicinally.
            Reply in as few words as possible.
            Never include the name of the plant.
            Reply in JSON format using the following structure:
            [
                {{"precaution_name": "<insert name of precaution 1 here>"}},
                {{"precaution_name": "<insert name of precaution 2 here>"}},
                {{"precaution_name": "<insert name of precaution 3 here>"}}
            ]
            Reply only with the JSON, don't add additional content.
        '''
        print(prompt)
        reply = llm_reply(prompt, model).strip()
        try: _data = json.loads(reply)
        except: _data = ''
        if data != '':
            _precautions = []
            for _precaution in _data:
                try: _precaution_name = _precaution['precaution_name']
                except: continue
                _precautions.append({'precaution_name': _precaution_name})
            if _precautions != []:
                data[key] = _precautions[:20]
                json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## ;images --------------------------------------------------------------------------------------
    ## ----------------------------------------------------------------------------------------------
    prompt_general = f'''
        {herb_name_scientific} plant, 
        natural light,
        outdoor,
        nature photography,
        high resolution, cinematic
    '''

    key = 'intro_image'
    if key not in data: data[key] = ''
    folder = f'{vault}/terrawhisper/images/herbs/intro'
    folder = f'{vault}/terrawhisper/images/herbs/all'
    out_1 = f'{vault}/terrawhisper/images/herbs/intro/{herb_slug}-plant.jpg'
    out_1 = f'{vault}/terrawhisper/images/herbs/all/{herb_slug}-plant.jpg'
    out_2 = f'website/images/herbs/{herb_slug}-plant.jpg'
    src_intro = f'/images/herbs/{herb_slug}-plant.jpg'
    alt_intro = f'{herb_name_scientific} plant'
    if not os.path.exists(folder): os.makedirs(folder)
    # if os.path.exists(folder): os.remove(out_1)
    if not os.path.exists(out_1):
        prompt = prompt_general
        negative_prompt = f'''
            text, logo, drawing, watermark, logo 
        '''
        print(prompt)
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        image.save(out_1)
        shutil.copy2(out_1, out_2)
        data[key] = src_intro
        json_write(json_filepath, data)
    if data[key] == '':
        if os.path.exists(out_2):
            data[key] = src_intro
            json_write(json_filepath, data)

    # ;cheatsheet image
    key = 'intro_image_cheatsheet'
    folder = f'{vault}/terrawhisper/images/herbs/all'
    # out_1 = f'{vault}/terrawhisper/images/herbs/all/{herb_slug}-plant-cheatsheet.jpg'
    out_2 = f'website/images/herbs/{herb_slug}-plant-cheatsheet.jpg'
    src_intro_cheatsheet = f'/images/herbs/{herb_slug}-plant-cheatsheet.jpg'
    alt_intro_cheatsheet = f'{herb_name_scientific} plant cheatsheet'
    # if os.path.exists(out_1): os.remove(out_1)
    # if os.path.exists(out_2): os.remove(out_2)
    if not os.path.exists(folder): os.makedirs(folder)
    if key not in data: data[key] = ''
    if not os.path.exists(out_2):
    # if True:
        data = json_read(json_filepath)
        a4_w = 2480
        a4_h = 3508
        image = Image.new('RGB', (a4_w, a4_h), '#ffffff')
        draw = ImageDraw.Draw(image)
        '''
        draw.line((0, 0, a4_w, 0), fill='#000000', width=4)
        draw.line((0, a4_h, a4_w, a4_h), fill='#000000', width=4)
        draw.line((0, 0, 0, a4_h), fill='#000000', width=4)
        draw.line((a4_w, 0, a4_w, a4_h), fill='#000000', width=4)
        '''
        y_cur = 64
        font_size = 80
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'{herb_name_scientific} Cheatsheet'.upper()
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((a4_w//2 - text_w//2, y_cur), text, '#000000', font=font)
        col_gap = int(a4_w * 0.03)
        x_cur = int(a4_w * 0.05)
        y_divider = y_cur + font_size + y_cur//2
        draw.line((x_cur, y_divider, a4_w - x_cur, y_divider), fill='#cdcdcd', width=4)
        y_content = y_divider + int(y_cur*1.5)
        y_cur = y_content
        rect_w = a4_w//2 - int(a4_w * 0.05) - col_gap//2
        rect_h = 64
        font_size_head = 30
        font_size_list = font_size_head
        x_text_offset = 32
        # uses
        draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#14532d')
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size_head)
        text = 'main medicinal uses'.upper()
        draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_head//2)), text, '#ffffff', font=font)
        y_cur += rect_h * 1
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size_list)
        lst = [x['condition_name'] for x in conditions_best] 
        y_start = y_cur
        for _i in range(len(lst)):
            y_cur = y_start + rect_h*_i
            if _i % 2 != 0:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#e5e5e5')
            else:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#ffffff')
            draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_list//2)), f'{_i+1}. {lst[_i].capitalize()}', '#000000', font=font)
        y_cur += rect_h * 2
        # benefits
        draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#14532d')
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size_head)
        text = 'primary health benefits'.upper()
        draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_head//2)), text, '#ffffff', font=font)
        y_cur += rect_h * 1
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size_list)
        lst = [x['name'] for x in data['benefits']]
        y_start = y_cur
        for _i in range(len(lst)):
            y_cur = y_start + rect_h*_i
            if _i % 2 != 0:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#e5e5e5')
            else:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#ffffff')
            draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_list//2)), f'{_i+1}. {lst[_i].capitalize()}', '#000000', font=font)
        y_cur += rect_h * 2
        # properties
        draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#14532d')
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size_head)
        text = 'dominant therapeutic properties'.upper()
        draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_head//2)), text, '#ffffff', font=font)
        y_cur += rect_h * 1
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size_list)
        lst = [x['property_name'] for x in data['properties']]
        y_start = y_cur
        for _i in range(len(lst)):
            y_cur = y_start + rect_h*_i
            if _i % 2 != 0:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#e5e5e5')
            else:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#ffffff')
            draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_list//2)), f'{_i+1}. {lst[_i].capitalize()}', '#000000', font=font)
        y_cur += rect_h * 2
        # constituents
        draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#14532d')
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size_head)
        text = 'major healing constituents'.upper()
        draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_head//2)), text, '#ffffff', font=font)
        y_cur += rect_h * 1
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size_list)
        lst = [x['name'] for x in data['constituents'][:10]]
        y_start = y_cur
        for _i in range(len(lst)):
            y_cur = y_start + rect_h*_i
            if _i % 2 != 0:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#e5e5e5')
            else:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#ffffff')
            draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_list//2)), f'{_i+1}. {lst[_i].capitalize()}', '#000000', font=font)
        y_cur += rect_h * 2
        y_cur = y_content
        x_cur = a4_w//2 + col_gap//2
        # parts
        draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#14532d')
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size_head)
        text = 'most used parts'.upper()
        draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_head//2)), text, '#ffffff', font=font)
        y_cur += rect_h * 1
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size_list)
        lst = [x['name'] for x in data['parts'][:10] if x['total_score'] > score_min]
        y_start = y_cur
        for _i in range(len(lst)):
            y_cur = y_start + rect_h*_i
            if _i % 2 != 0:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#e5e5e5')
            else:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#ffffff')
            draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_list//2)), f'{_i+1}. {lst[_i].capitalize()}', '#000000', font=font)
        y_cur += rect_h * 2
        # preparations
        draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#14532d')
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size_head)
        text = 'most common preparations'.upper()
        draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_head//2)), text, '#ffffff', font=font)
        y_cur += rect_h * 1
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size_list)
        lst = [x['preparation_name'] for x in data['preparations'][:10] if x['preparation_total_score'] > score_min]
        y_start = y_cur
        for _i in range(len(lst)):
            y_cur = y_start + rect_h*_i
            if _i % 2 != 0:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#e5e5e5')
            else:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#ffffff')
            draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_list//2)), f'{_i+1}. {lst[_i].capitalize()}', '#000000', font=font)
        y_cur += rect_h * 2
        # side effects
        draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#14532d')
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size_head)
        text = 'abusing side effects'.upper()
        draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_head//2)), text, '#ffffff', font=font)
        y_cur += rect_h * 1
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size_list)
        lst = [x['side_effect_name'] for x in data['side_effects'][:10]]
        y_start = y_cur
        for _i in range(len(lst)):
            y_cur = y_start + rect_h*_i
            if _i % 2 != 0:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#e5e5e5')
            else:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#ffffff')
            draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_list//2)), f'{_i+1}. {lst[_i].capitalize()}', '#000000', font=font)
        y_cur += rect_h * 2
        # precautions
        draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#14532d')
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size_head)
        text = 'precautions to take'.upper()
        draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_head//2)), text, '#ffffff', font=font)
        y_cur += rect_h * 1
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size_list)
        lst = [x['precaution_name'] for x in data['precautions'][:10]]
        y_start = y_cur
        for _i in range(len(lst)):
            y_cur = y_start + rect_h*_i
            if _i % 2 != 0:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#e5e5e5')
            else:
                draw.rectangle([(x_cur, y_cur), (x_cur+rect_w, y_cur+rect_h)], fill='#ffffff')
            draw.text((x_cur + x_text_offset, y_cur + (rect_h//2) - (font_size_list//2)), f'{_i+1}. {lst[_i].capitalize()}', '#000000', font=font)
        y_cur += rect_h * 2
        # footer
        text = 'Copyright Terrawhisper.com | Sharing this cheatsheet requires attribution (to Terrawhisper) | Selling this cheatsheet is not allowed'
        _, _, text_w, text_h = font.getbbox(text)
        y_cur = a4_h
        x_cur = int(a4_w * 0.05)
        draw.line((x_cur, y_cur - 32 - 32 - 32, a4_w - x_cur, y_cur - 32 - 32 - 32), fill='#cdcdcd', width=4)
        draw.text((a4_w//2 - text_w//2, y_cur - 32 - 32), text, '#000000', font=font)
        image_logo = Image.open('website/images-static/terrawhisper-logo.jpg')
        logo_w, logo_h = image_logo.size
        image_logo = img_resize(image_logo, w=int(logo_w*0.5), h=int(logo_h*0.5))
        logo_w, logo_h = image_logo.size
        image.paste(image_logo, (int(a4_w - logo_w - (a4_w*0.05)), int(y_cur - 32 - 32 - 32 - logo_h - 64)))
        # image.save(out_1)
        image.save(out_2)
        data[key] = src_intro
        json_write(json_filepath, data)

    key = 'uses_image'
    if key not in data: data[key] = ''
    folder = f'{vault}/terrawhisper/images/herbs/uses'
    folder = f'{vault}/terrawhisper/images/herbs/all'
    out_1 = f'{vault}/terrawhisper/images/herbs/uses/{herb_slug}-uses.jpg'
    out_1 = f'{vault}/terrawhisper/images/herbs/all/{herb_slug}-uses.jpg'
    out_2 = f'website/images/herbs/{herb_slug}-uses.jpg'
    src_uses = f'/images/herbs/{herb_slug}-uses.jpg'
    alt_uses = f'uses of {herb_name_scientific}'
    if not os.path.exists(folder): os.makedirs(folder)
    # if os.path.exists(out_1): os.remove(out_1)
    if not os.path.exists(out_1):
        prompt = f'''
            {herb_name_scientific} plant, 
            botanical illustration,
            minimalist, 
            beige background,
            high resolution
        '''
        prompt = prompt_general
        negative_prompt = f'''
            text, logo, drawing, watermark, logo 
        '''
        print(prompt)
        image_plant = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image_plant.save(out_1)
        if os.path.exists(out_2): os.remove(out_2)
    # if os.path.exists(out_2): os.remove(out_2)
    if not os.path.exists(out_2):
        image = Image.new('RGBA', (1216, 1216), '#000000')
        # text ---
        text_max_w = 0
        py = 48
        px = 36
        x_curr = px
        y_start = py
        draw = ImageDraw.Draw(image)
        font_size = 36
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'{herb_name_scientific}'.upper()
        lines = text.split(' ') 
        y_curr = y_start
        for line_i, line in enumerate(lines):
            _, _, text_w, text_h = font.getbbox(line)
            if text_max_w < text_w: text_max_w = text_w
            y_curr += font_size*line_i*1.2
            draw.text((x_curr, y_curr), line, '#ffffff', font=font)
        y_curr += font_size*1.2
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'(medicinal uses)'.lower()
        _, _, text_w, text_h = font.getbbox(text)
        if text_max_w < text_w: text_max_w = text_w
        draw.text((x_curr, y_curr), text, '#ffffff', font=font)
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        y_start = y_curr+font_size*1.2*2 + 48
        for _i, name in enumerate(conditions_best):
            text = f'{_i+1}. {name.capitalize()}'
            _, _, text_w, text_h = font.getbbox(text)
            if text_max_w < text_w: text_max_w = text_w
            y_curr = y_start + _i*font_size*2
            draw.text((x_curr, y_curr), text, '#ffffff', font=font)
        image_logo = Image.open('website/images-static/terrawhisper-logo-black.jpg')
        logo_w, logo_h = image_logo.size
        image_logo = img_resize(image_logo, w=int(logo_w*0.3), h=int(logo_h*0.3))
        logo_w, logo_h = image_logo.size
        image.paste(image_logo, (int(x_curr), int(1216-logo_h - py)))
        # plant ---
        text_area_w = text_max_w+px*2
        image_plant = Image.open(out_1)
        image_plant = img_resize(image_plant, w=1216-text_area_w, h=1216)
        image.paste(image_plant, (text_area_w, 0))
        # gen ---
        image = img_resize(image, w=768, h=768)
        image = image.convert('RGB')
        image.save(out_2)
        data[key] = src_uses
        json_write(json_filepath, data)
    if data[key] == '':
        if os.path.exists(out_2):
            data[key] = src_uses
            json_write(json_filepath, data)

    key = 'benefits_image'
    if key not in data: data[key] = ''
    folder = f'{vault}/terrawhisper/images/herbs/benefits'
    folder = f'{vault}/terrawhisper/images/herbs/all'
    out_1 = f'{vault}/terrawhisper/images/herbs/benefits/{herb_slug}-benefits.jpg'
    out_1 = f'{vault}/terrawhisper/images/herbs/all/{herb_slug}-benefits.jpg'
    out_2 = f'website/images/herbs/{herb_slug}-benefits.jpg'
    src_benefits = f'/images/herbs/{herb_slug}-benefits.jpg'
    alt_benefits = f'benefits of {herb_name_scientific}'
    if not os.path.exists(folder): os.makedirs(folder)
    # if os.path.exists(out_1): os.remove(out_1)
    if not os.path.exists(out_1):
        prompt = f'''
            {herb_name_scientific} plant, 
            watercolor illustration,
            minimalist, 
            dark background,
            high resolution
        '''
        negative_prompt = f'''
            text
        '''
        prompt = prompt_general
        negative_prompt = f'''
            text, logo, drawing, watermark, logo 
        '''
        print(prompt)
        image_plant = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image_plant.save(out_1)
        if os.path.exists(out_2): os.remove(out_2)
    # if os.path.exists(out_2): os.remove(out_2)
    if not os.path.exists(out_2):
        image = Image.new('RGBA', (1216, 1216), '#f5f5f5')
        # text ---
        text_max_w = 0
        py = 48
        px = 36
        x_curr = px
        y_start = py
        draw = ImageDraw.Draw(image)
        font_size = 36
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'{herb_name_scientific}'.upper()
        lines = text.split(' ') 
        y_curr = y_start
        for line_i, line in enumerate(lines):
            _, _, text_w, text_h = font.getbbox(line)
            if text_max_w < text_w: text_max_w = text_w
            y_curr += font_size*line_i*1.2
            draw.text((x_curr, y_curr), line, '#000000', font=font)
        y_curr += font_size*1.2
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'(health benefits)'.lower()
        _, _, text_w, text_h = font.getbbox(text)
        if text_max_w < text_w: text_max_w = text_w
        draw.text((x_curr, y_curr), text, '#000000', font=font)
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        y_start = y_curr+font_size*1.2*2 + 48
        for _i, benefit_name in enumerate([x['name'] for x in data['benefits'][:10]]):
            text = f'{_i+1}. {benefit_name.capitalize()}'
            _, _, text_w, text_h = font.getbbox(text)
            if text_max_w < text_w: text_max_w = text_w
            y_curr = y_start + _i*font_size*2
            draw.text((x_curr, y_curr), text, '#000000', font=font)
        image_logo = Image.open('website/images-static/terrawhisper-logo-white.png')
        logo_w, logo_h = image_logo.size
        image_logo = img_resize(image_logo, w=int(logo_w*0.3), h=int(logo_h*0.3))
        logo_w, logo_h = image_logo.size
        image.paste(image_logo, (int(x_curr), int(1216-logo_h - py)), image_logo)
        # plant ---
        text_area_w = text_max_w+px*2
        image_plant = Image.open(out_1)
        image_plant = img_resize(image_plant, w=1216-text_area_w, h=1216)
        image.paste(image_plant, (text_area_w, 0))
        # gen ---
        image = img_resize(image, w=768, h=768)
        image = image.convert('RGB')
        image.save(out_2)
        data[key] = src_benefits
        json_write(json_filepath, data)
    if data[key] == '':
        if os.path.exists(out_2):
            data[key] = src_benefits
            json_write(json_filepath, data)

    key = 'properties_image'
    if key not in data: data[key] = ''
    folder = f'{vault}/terrawhisper/images/herbs/properties'
    folder = f'{vault}/terrawhisper/images/herbs/all'
    out_1 = f'{vault}/terrawhisper/images/herbs/properties/{herb_slug}-properties.jpg'
    out_1 = f'{vault}/terrawhisper/images/herbs/all/{herb_slug}-properties.jpg'
    out_2 = f'website/images/herbs/{herb_slug}-properties.jpg'
    src_properties = f'/images/herbs/{herb_slug}-properties.jpg'
    alt_properties = f'properties of {herb_name_scientific}'
    if not os.path.exists(folder): os.makedirs(folder)
    # if os.path.exists(out_1): os.remove(out_1)
    if not os.path.exists(out_1):
        prompt = f'''
            {herb_name_scientific} plant, 
            blueprint drawing,
            minimalist, 
            blue background,
            high resolution
        '''
        negative_prompt = f'''
            text
        '''
        prompt = prompt_general
        negative_prompt = f'''
            text, logo, drawing, watermark, logo 
        '''
        print(prompt)
        image_plant = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image_plant.save(out_1)
        if os.path.exists(out_2): os.remove(out_2)
    # if os.path.exists(out_2): os.remove(out_2)
    if not os.path.exists(out_2):
        image = Image.new('RGBA', (1216, 1216), '#000000')
        # text ---
        text_max_w = 0
        py = 48
        px = 36
        x_curr = px
        y_start = py
        draw = ImageDraw.Draw(image)
        font_size = 36
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'{herb_name_scientific}'.upper()
        lines = text.split(' ') 
        y_curr = y_start
        for line_i, line in enumerate(lines):
            _, _, text_w, text_h = font.getbbox(line)
            if text_max_w < text_w: text_max_w = text_w
            y_curr += font_size*line_i*1.2
            draw.text((x_curr, y_curr), line, '#ffffff', font=font)
        y_curr += font_size*1.2
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'(therapeutic properties)'.lower()
        _, _, text_w, text_h = font.getbbox(text)
        if text_max_w < text_w: text_max_w = text_w
        draw.text((x_curr, y_curr), text, '#ffffff', font=font)
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        y_start = y_curr+font_size*1.2*2 + 48
        for _i, benefit_name in enumerate([x['property_name'] for x in data['properties'][:10]]):
            text = f'{_i+1}. {benefit_name.capitalize()}'
            _, _, text_w, text_h = font.getbbox(text)
            if text_max_w < text_w: text_max_w = text_w
            y_curr = y_start + _i*font_size*2
            draw.text((x_curr, y_curr), text, '#ffffff', font=font)
        image_logo = Image.open('website/images-static/terrawhisper-logo-black.jpg')
        logo_w, logo_h = image_logo.size
        image_logo = img_resize(image_logo, w=int(logo_w*0.3), h=int(logo_h*0.3))
        logo_w, logo_h = image_logo.size
        image.paste(image_logo, (int(x_curr), int(1216-logo_h - py)))
        # plant ---
        text_area_w = text_max_w+px*2
        image_plant = Image.open(out_1)
        image_plant = img_resize(image_plant, w=1216-text_area_w, h=1216)
        image.paste(image_plant, (text_area_w, 0))
        # gen ---
        image = img_resize(image, w=768, h=768)
        image = image.convert('RGB')
        image.save(out_2)
        data[key] = src_properties
        json_write(json_filepath, data)
    if data[key] == '':
        if os.path.exists(out_2):
            data[key] = src_properties
            json_write(json_filepath, data)

    key = 'constituents_image'
    if key not in data: data[key] = ''
    folder = f'{vault}/terrawhisper/images/herbs/constituents'
    folder = f'{vault}/terrawhisper/images/herbs/all'
    out_1 = f'{vault}/terrawhisper/images/herbs/constituents/{herb_slug}-constituents.jpg'
    out_1 = f'{vault}/terrawhisper/images/herbs/all/{herb_slug}-constituents.jpg'
    out_2 = f'website/images/herbs/{herb_slug}-constituents.jpg'
    src_constituents = f'/images/herbs/{herb_slug}-constituents.jpg'
    alt_constituents = f'constituents of {herb_name_scientific}'
    if not os.path.exists(folder): os.makedirs(folder)
    # if os.path.exists(out_1): os.remove(out_1)
    if not os.path.exists(out_1):
        prompt = f'''
            {herb_name_scientific} plant, 
            natural ligthing, 
            outdoor,
            high resolution, cinematic
        '''
        negative_prompt = f'''
            text
        '''
        prompt = prompt_general
        negative_prompt = f'''
            text, logo, drawing, watermark, logo 
        '''
        print(prompt)
        image_plant = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image_plant.save(out_1)
        if os.path.exists(out_2): os.remove(out_2)
    # if os.path.exists(out_2): os.remove(out_2)
    if not os.path.exists(out_2):
        image = Image.new('RGBA', (1216, 1216), '#f5f5f5')
        # text ---
        text_max_w = 0
        py = 48
        px = 36
        x_curr = px
        y_start = py
        draw = ImageDraw.Draw(image)
        font_size = 36
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'{herb_name_scientific}'.upper()
        lines = text.split(' ') 
        y_curr = y_start
        for line_i, line in enumerate(lines):
            _, _, text_w, text_h = font.getbbox(line)
            if text_max_w < text_w: text_max_w = text_w
            y_curr += font_size*line_i*1.2
            draw.text((x_curr, y_curr), line, '#000000', font=font)
        y_curr += font_size*1.2
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'(bioactive constituents)'.lower()
        _, _, text_w, text_h = font.getbbox(text)
        if text_max_w < text_w: text_max_w = text_w
        draw.text((x_curr, y_curr), text, '#000000', font=font)
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        y_start = y_curr+font_size*1.2*2 + 48
        for _i, benefit_name in enumerate([x['name'] for x in data['constituents'][:10]]):
            text = f'{_i+1}. {benefit_name.capitalize()}'
            _, _, text_w, text_h = font.getbbox(text)
            if text_max_w < text_w: text_max_w = text_w
            y_curr = y_start + _i*font_size*2
            draw.text((x_curr, y_curr), text, '#000000', font=font)
        image_logo = Image.open('website/images-static/terrawhisper-logo-white.png')
        logo_w, logo_h = image_logo.size
        image_logo = img_resize(image_logo, w=int(logo_w*0.3), h=int(logo_h*0.3))
        logo_w, logo_h = image_logo.size
        image.paste(image_logo, (int(x_curr), int(1216-logo_h - py)), image_logo)
        # plant ---
        text_area_w = text_max_w+px*2
        image_plant = Image.open(out_1)
        image_plant = img_resize(image_plant, w=1216-text_area_w, h=1216)
        image.paste(image_plant, (text_area_w, 0))
        # gen ---
        image = img_resize(image, w=768, h=768)
        image = image.convert('RGB')
        image.save(out_2)
        data[key] = src_constituents
        json_write(json_filepath, data)
    if data[key] == '':
        if os.path.exists(out_2):
            data[key] = src_constituents
            json_write(json_filepath, data)

    key = 'parts_image'
    if key not in data: data[key] = ''
    folder = f'{vault}/terrawhisper/images/herbs/parts'
    folder = f'{vault}/terrawhisper/images/herbs/all'
    out_1 = f'{vault}/terrawhisper/images/herbs/parts/{herb_slug}-parts.jpg'
    out_1 = f'{vault}/terrawhisper/images/herbs/all/{herb_slug}-parts.jpg'
    out_2 = f'website/images/herbs/{herb_slug}-parts.jpg'
    src_parts = f'/images/herbs/{herb_slug}-parts.jpg'
    alt_parts = f'parts of {herb_name_scientific}'
    if not os.path.exists(folder): os.makedirs(folder)
    # if os.path.exists(out_1): os.remove(out_1)
    if not os.path.exists(out_1):
        prompt = f'''
            {herb_name_scientific} plant, 
            painting, art nouveau, 
            high resolution
        '''
        negative_prompt = f'''
            text
        '''
        prompt = prompt_general
        negative_prompt = f'''
            text, logo, drawing, watermark, logo 
        '''
        print(prompt)
        image_plant = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image_plant.save(out_1)
        if os.path.exists(out_2): os.remove(out_2)
    # if os.path.exists(out_2): os.remove(out_2)
    if not os.path.exists(out_2):
        image = Image.new('RGBA', (1216, 1216), '#000000')
        # text ---
        text_max_w = 0
        py = 48
        px = 36
        x_curr = px
        y_start = py
        draw = ImageDraw.Draw(image)
        font_size = 36
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'{herb_name_scientific}'.upper()
        lines = text.split(' ') 
        y_curr = y_start
        for line_i, line in enumerate(lines):
            _, _, text_w, text_h = font.getbbox(line)
            if text_max_w < text_w: text_max_w = text_w
            y_curr += font_size*line_i*1.2
            draw.text((x_curr, y_curr), line, '#ffffff', font=font)
        y_curr += font_size*1.2
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'(medicinal parts)'.lower()
        _, _, text_w, text_h = font.getbbox(text)
        if text_max_w < text_w: text_max_w = text_w
        draw.text((x_curr, y_curr), text, '#ffffff', font=font)
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        y_start = y_curr+font_size*1.2*2 + 48
        names = [obj['name'].lower().strip() for obj in data['parts'] if obj['total_score'] >= 6]
        for _i, name in enumerate(names):
            text = f'{_i+1}. {name.capitalize()}'
            _, _, text_w, text_h = font.getbbox(text)
            if text_max_w < text_w: text_max_w = text_w
            y_curr = y_start + _i*font_size*2
            draw.text((x_curr, y_curr), text, '#ffffff', font=font)
        image_logo = Image.open('website/images-static/terrawhisper-logo-black.jpg')
        logo_w, logo_h = image_logo.size
        image_logo = img_resize(image_logo, w=int(logo_w*0.3), h=int(logo_h*0.3))
        logo_w, logo_h = image_logo.size
        image.paste(image_logo, (int(x_curr), int(1216-logo_h - py)))
        text_area_w = text_max_w+px*2
        image_plant = Image.open(out_1)
        image_plant = img_resize(image_plant, w=1216-text_area_w, h=1216)
        image.paste(image_plant, (text_area_w, 0))
        image = img_resize(image, w=768, h=768)
        image = image.convert('RGB')
        image.save(out_2)
        data[key] = src_parts
        json_write(json_filepath, data)
    if data[key] == '':
        if os.path.exists(out_2):
            data[key] = src_parts
            json_write(json_filepath, data)

    key = 'preparations_image'
    if key not in data: data[key] = ''
    folder = f'{vault}/terrawhisper/images/herbs/preparations'
    folder = f'{vault}/terrawhisper/images/herbs/all'
    out_1 = f'{vault}/terrawhisper/images/herbs/parts/{herb_slug}-preparations.jpg'
    out_1 = f'{vault}/terrawhisper/images/herbs/all/{herb_slug}-preparations.jpg'
    out_2 = f'website/images/herbs/{herb_slug}-preparations.jpg'
    src_preparations = f'/images/herbs/{herb_slug}-preparations.jpg'
    alt_preparations = f'preparations of {herb_name_scientific}'
    if not os.path.exists(folder): os.makedirs(folder)
    # if os.path.exists(out_1): os.remove(out_1)
    if not os.path.exists(out_1):
        prompt = f'''
            {herb_name_scientific} plant, 
            painting, art nouveau, 
            high resolution
        '''
        negative_prompt = f'''
            text
        '''
        prompt = prompt_general
        negative_prompt = f'''
            text, logo, drawing, watermark, logo 
        '''
        print(prompt)
        image_plant = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image_plant.save(out_1)
        if os.path.exists(out_2): os.remove(out_2)
    # if os.path.exists(out_2): os.remove(out_2)
    if not os.path.exists(out_2):
        image = Image.new('RGBA', (1216, 1216), '#000000')
        # text ---
        text_max_w = 0
        py = 48
        px = 36
        x_curr = px
        y_start = py
        draw = ImageDraw.Draw(image)
        font_size = 36
        font_path = f"website/assets/fonts/helvetica/Helvetica-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'{herb_name_scientific}'.upper()
        lines = text.split(' ') 
        y_curr = y_start
        for line_i, line in enumerate(lines):
            _, _, text_w, text_h = font.getbbox(line)
            if text_max_w < text_w: text_max_w = text_w
            y_curr += font_size*line_i*1.2
            draw.text((x_curr, y_curr), line, '#ffffff', font=font)
        y_curr += font_size*1.2
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        text = f'(medicinal preparations)'.lower()
        _, _, text_w, text_h = font.getbbox(text)
        if text_max_w < text_w: text_max_w = text_w
        draw.text((x_curr, y_curr), text, '#ffffff', font=font)
        font_size = 24
        font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
        font = ImageFont.truetype(font_path, font_size)
        y_start = y_curr+font_size*1.2*2 + 48
        _i = 0
        for obj in data['preparations']:
            if obj['preparation_total_score'] <= score_min: continue
            preparation_name = obj['preparation_name']
            preparation_slug = preparation_name.strip().lower().replace(' ', '-')
            if preparation_name == 'suppository': continue
            text = f'{_i+1}. {preparation_name.capitalize()}'
            _, _, text_w, text_h = font.getbbox(text)
            if text_max_w < text_w: text_max_w = text_w
            y_curr = y_start + _i*font_size*2
            draw.text((x_curr, y_curr), text, '#ffffff', font=font)
            _i += 1
        if 0:
            names = [obj['preparation_name'].lower().strip() for obj in data['preparations'] if obj['preparation_total_score'] >= score_min]
            for _i, name in enumerate(names):
                text = f'{_i+1}. {name.capitalize()}'
                _, _, text_w, text_h = font.getbbox(text)
                if text_max_w < text_w: text_max_w = text_w
                y_curr = y_start + _i*font_size*2
                draw.text((x_curr, y_curr), text, '#ffffff', font=font)
        image_logo = Image.open('website/images-static/terrawhisper-logo-black.jpg')
        logo_w, logo_h = image_logo.size
        image_logo = img_resize(image_logo, w=int(logo_w*0.3), h=int(logo_h*0.3))
        logo_w, logo_h = image_logo.size
        image.paste(image_logo, (int(x_curr), int(1216-logo_h - py)))
        text_area_w = text_max_w+px*2
        image_plant = Image.open(out_1)
        image_plant = img_resize(image_plant, w=1216-text_area_w, h=1216)
        image.paste(image_plant, (text_area_w, 0))
        image = img_resize(image, w=768, h=768)
        image = image.convert('RGB')
        image.save(out_2)
        data[key] = src_preparations
        json_write(json_filepath, data)
    if data[key] == '':
        if os.path.exists(out_2):
            data[key] = src_preparations
            json_write(json_filepath, data)

    for obj in data['preparations']:
        if obj['preparation_total_score'] <= score_min: continue
        preparation_name = obj['preparation_name']
        preparation_slug = preparation_name.strip().lower().replace(' ', '-')
        if preparation_name == 'suppository': continue
        key = 'preparation_image'
        if key not in obj: obj[key] = ''
        folder = f'{vault}/terrawhisper/images/herbs/preparations/{preparation_slug}'
        out_1 = f'{vault}/terrawhisper/images/herbs/preparations/{preparation_slug}/{herb_slug}-{preparation_slug}.jpg'
        out_2 = f'website/images/herbs/{herb_slug}-{preparation_slug}.jpg'
        src = f'/images/herbs/{herb_slug}-{preparation_slug}.jpg'
        alt = f'{preparation_name} made with {herb_name_scientific}'
        if not os.path.exists(folder): os.makedirs(folder)
        # if not os.path.exists(folder): os.remove(out_1)
        if not os.path.exists(out_1):
            prompt = f'''
                {herb_name_scientific} herbal {preparation_name}s, 
                on a wooden table, surrounded by herbs,
                soft light, diffused light, natural light, soft focus, 
                close-up, 
                perspective three-quarter view,
                depth of field, bokeh, 
                high resolution, cinematic
            '''
            negative_prompt = f'''
                text, logo, drawing, watermark, logo 
            '''
            print(prompt)
            image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
            image = img_resize(image, w=768, h=768)
            image.save(out_1)
            shutil.copy2(out_1, out_2)
            obj[key] = src
            json_write(json_filepath, data)
        if obj[key] == '':
            if os.path.exists(out_2):
                obj[key] = src
                json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## ----------------------------------------------------------------------------------------------
    ## ----------------------------------------------------------------------------------------------
    ## write post
    ## ----------------------------------------------------------------------------------------------
    ## ----------------------------------------------------------------------------------------------
    ## ----------------------------------------------------------------------------------------------

    ## ;intro
    if 0:
        key = f'intro_description'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        key = f'intro_study'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return

    # TODO: use json data in the description
    key = 'intro_description'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        prompt = f'''
            Write a 5-sentence detailed itroductive paragraph for an article about the {herb_name_scientific} herb.
            Start by stating what main medicinal uses this herb has, in terms of health conditions it helps.
            Include what main health benefits this herb has.
            Include what main therapeutic properties this herb has.
            Include what main bioactive compounds this herb has.
            Include what main herbal preparation people make with this herb.
            Start with the following words: {herb_name_scientific.capitalize()}, commonly known as {data['common_names'][0]['common_name']}, .
            Don't write fluff, only proven facts.
            Don't allucinate.
        '''
        reply = llm_reply(prompt, model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            data[key] = lines[0]
            json_write(json_filepath, data)

    key = 'intro_study'
    if key not in data: data[key] = ''
    ## UNCOMMENT to try to generate missing studies (maybe download plant-specific studies, or try different query)
    # if data[key] == []: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        collection_name = 'medicinal-plants'
        query = f'health benefits of {herb_name_scientific}'
        collection = chroma_client.get_or_create_collection(
            name=collection_name, 
            embedding_function=sentence_transformer_ef,
        )
        results = collection.query(query_texts=[query], n_results=10)
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        abstracts = [[documents[i], metadatas[i]] for i in range(len(documents))]
        studies_relevant = []
        for abstract in abstracts:
            prompt = f'''
                Does the following study talk about the health benefits, medicinal constituents, or medicinal efficacy of {query}?
                STUDY:
                {abstract[0]}
                Reply in JSON format using the structure provided in the following example:
                {{
                    "reply": <insert only "yes" or "no" here>,
                    "reason": <explain why you choose "yes" or "no" here>
                }}
                
            '''
            reply = llm_reply(prompt, model)
            try: _data = json.loads(reply)
            except: _data = {} 
            if _data != {}:
                if 'reply' in _data and 'reason' in _data:
                    if _data['reply'] == 'yes':
                        studies_relevant.append({
                            'study_abstract': abstract[0],
                            'study_meta': abstract[1],
                        })
        studies_output = []
        if studies_relevant != []:
            for study_relevant in studies_relevant:
                study_abstract = study_relevant['study_abstract']
                journal_title = study_relevant['study_meta']['journal_title']
                prompt = f'''
                    Write a 3-sentence short paragraph explaining the positive effects of {herb_name_scientific} according to the data provided by the STUDY below. 
                    STUDY:
                    {study_abstract}
                    GUIDELINES:
                    Always refer to the plant with either "{herb_name_scientific}" or "it", don't use other names.
                    Start the reply with the following words: According to a study published by {journal_title}, .
                '''
                reply = llm_reply(prompt, model)
                reply = reply.replace(journal_title, f'"{journal_title}"').replace('""', '"')
                print('###################################################')
                print(reply)
                print('###################################################')
                validate_tries = 3
                for _ in range(validate_tries):
                    question = f'''Write a 3-sentence short paragraph explaining the positive effects of {herb_name_scientific} according to the data from the STUDY below.'''
                    study_to_validate = f'{study_abstract} {journal_title}'
                    reply_validated = llm_validate(question, study_to_validate, reply)
                    try: _json_data = json.loads(reply_validated)
                    except: _json_data = {} 
                    if _json_data != {}:
                        if _json_data['SCORE'] == 'PASS' or _json_data['SCORE'] == 'SUCCESS':
                            studies_output.append(reply.strip())
                            break
                        elif _json_data['SCORE'] == 'FAIL':
                            break
                        else:
                            continue
        if studies_output != []:
            data[key] = studies_output
            json_write(json_filepath, data)
        else:
            data[key] = []
            json_write(json_filepath, data)

    ## ;uses
    ## ----------------------------------------------------------------------------------------------
    if 0:
        key = f'uses_description'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        key = f'uses_list'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        for medicinal_system in medicinal_systems:
            medicinal_system_dash = medicinal_system.replace(' ', '-')
            medicinal_system_underline = medicinal_system.replace(' ', '_')
            key = f'uses_{medicinal_system_underline}_description'
            if key in data: del data[key]
            json_write(json_filepath, data)
        return

    key = 'uses_description'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        names = [condition.lower().strip() for condition in conditions_best]
        names_prompt = ', '.join(names)
        prompt = f'''
            Write 1 detailed paragraph about what are the most common uses of the plant {herb_name_scientific} for health conditions, and explain what constituents this plant has that are responsible for the relief of those conditions.
            For "uses" I mean which health conditions this plant heal.
            In specific, discuss the following conditions in this exact order: {names_prompt}.
            Only mention a condition once throughout the paragraph, don't name the same condition multiple times.
            Pack as much information in as few words as possible.
            Don't write fluff, only proven data.
            Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
            Don't allucinate.
            Write the paragraph in 5 sentences.
            Write only the paragraph, don't add additional info.
            Don't add references or citations.
            Start with the following words: The main medicinal uses of {herb_name_scientific} are .
            Don't include all the conditions in the first sentence, but distribute them homogeneously throughout the paragraph.
            Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
        '''
        print(prompt)
        reply = llm_reply(prompt, model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            data[key] = lines[0]
            json_write(json_filepath, data)

    key = 'uses_list'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        names = [name for name in conditions_best]
        names_prompt = ', '.join(names)
        items_prompt = []
        for name in names:
            items_prompt.append(f'{{"condition_name": "{name}", "description": "describe why {herb_name_scientific} is used for this condition."}}') 
        items_prompt = ', \n'.join(items_prompt)
        prompt = f'''
            Write a description for each of the following health conditions on why the plant {herb_name_scientific} is used for that condition.
            Write the descriptions in full, complete and detailed sentences.
            Don't write fluff, only proven facts.
            Don't allucinate.
            DOn't include the name of the plant.
            Reply in JSON format using the following structure:
            [
                {items_prompt}
            ]
            Only reply with the JSON, don't add additional info.
        '''
        print(prompt)
        reply = llm_reply(prompt, model).strip()
        try: _data = json.loads(reply)
        except: _data = {}
        if _data != {}:
            error = False
            for obj in _data:
                if 'condition_name' not in obj or 'description' not in obj:
                    error = True
                    break
            if not error:
                data[key] = _data
                json_write(json_filepath, data)

    for medicinal_system in medicinal_systems:
        medicinal_system_dash = medicinal_system.replace(' ', '-')
        medicinal_system_underline = medicinal_system.replace(' ', '_')
        key = f'uses_{medicinal_system_underline}_description'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            names = [obj['name'] for obj in data[f'uses_{medicinal_system_underline}']]
            prompt = f'''
                Write 1 detailed paragraph about what are the most common health condition that are treated with the plant {herb_name_scientific} in {medicinal_system}.
                Include the following conditions in this exact order: {names}.
                Only mention a condition once throughout the paragraph, don't mention the same condition multiple times.
                Pack as much information in as few words as possible.
                Don't write fluff, only proven data.
                Don't allucinate.
                Write the paragraph in 5 sentences.
                Write only the paragraph, don't add additional info.
                Don't add references or citations.
                Start with the following words: In {medicinal_system}, {herb_name_scientific} is used to .
                Don't include all the conditions in the first sentence, but distribute them homogeneously throughout the paragraph.
                Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
            '''
            print(prompt)
            reply = llm_reply(prompt, model)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## ;benefits
    ## ----------------------------------------------------------------------------------------------
    if 0:
        key = f'benefits_description'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        key = f'benefits_list'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        for body_system in body_systems:
            key = f'benefits_{body_system}_system_description'
            if key in data: del data[key]
            json_write(json_filepath, data)
        return

    key = 'benefits_description'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        names = [obj['name'].lower().strip() for obj in data['benefits']]
        names_prompt = ', '.join(names)
        prompt = f'''
            Write 1 detailed paragraph about what are the health benefits of the plant {herb_name_scientific}, and explain what medicinal properties this plant has that are responsible for the health benefits.
            Discuss the following health benefits in this exact order: {names}.
            Only mention a benefit once throughout the paragraph, don't name the same benefit multiple times.
            The main subject of each sentence is the discussed health benefit.
            Pack as much information in as few words as possible.  Don't write fluff, only proven data.  Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
            Don't allucinate.
            Write the paragraph in 5 sentences.
            Write only the paragraph, don't add additional info.
            Don't add references or citations.
            Start with the following words: {herb_name_scientific} {names[0]} .
            Don't include all the benefits in the first sentence, but distribute them homogeneously throughout the paragraph.
            Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
        '''
        print(prompt)
        reply = llm_reply(prompt, model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            data[key] = lines[0]
            json_write(json_filepath, data)

    key = 'benefits_list'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        names = [obj['name'].lower().strip() for obj in data['benefits']]
        names_prompt = ', '.join(names)
        items_prompt = []
        for name in names:
            items_prompt.append(f'{{"benefit_name": "{name}", "description": "describe what is this benefit of {herb_name_scientific} and why this plant has this benefit."}}') 
        items_prompt = ', \n'.join(items_prompt)
        prompt = f'''
            Write a description for each of the following health benefits on what is this benefit of {herb_name_scientific} and why this plant has it.
            Write the descriptions in full, complete and detailed sentences.
            Don't write fluff, only proven facts.
            Don't allucinate.
            Don't include the name of the plant.
            Reply in JSON format using the following structure:
            [
                {items_prompt}
            ]
            Only reply with the JSON, don't add additional info.
        '''
        print(prompt)
        reply = llm_reply(prompt, model).strip()
        try: _data = json.loads(reply)
        except: _data = {}
        if _data != {}:
            error = False
            for obj in _data:
                if 'benefit_name' not in obj or 'description' not in obj:
                    error = True
                    break
            if not error:
                data[key] = _data
                json_write(json_filepath, data)

    for body_system in body_systems:
        key = f'benefits_{body_system}_system_description'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            names = [obj['benefit_name'].lower().strip() for obj in data[f'benefits_{body_system}_system']]
            names_prompt = ', '.join(names)
            prompt = f'''
                Write 1 detailed paragraph about what are the health benefits of the plant {herb_name_scientific} for the {body_system} system, and explain what medicinal properties this plant has that are responsible for the health benefits.
                Discuss the following health benefits in this exact order: {names}.
                Examples of medicinal properties are like: antimicrobial, antioxidant, anti-inflammatory, etc.
                Only mention a benefit once throughout the paragraph, don't name the same benefit multiple times.
                The main subject of each sentence is the discussed health benefit.
                Pack as much information in as few words as possible.
                Don't write fluff, only proven data.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Don't allucinate.
                Write the paragraph in 5 sentences.
                Write only the paragraph, don't add additional info.
                Don't add references or citations.
                Start with the following words: {herb_name_scientific} {names[0]} .
                Don't include all the benefits in the first sentence, but distribute them homogeneously throughout the paragraph.
                Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
            '''
            print(prompt)
            reply = llm_reply(prompt, model)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## ;properties
    ## ----------------------------------------------------------------------------------------------
    if 0:
        key = f'properties_description'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        key = f'properties_list'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return

    key = 'properties_description'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        names = [obj['property_name'].lower().strip() for obj in data['properties']]
        names_prompt = ', '.join(names[:10])
        prompt = f'''
            Write 1 detailed paragraph about what are the therapeutic properties of the plant {herb_name_scientific}, and explain what are the bioactive compounds of this plant that are responsible for the medicinal properties.
            Discuss the following medicinal properties in this exact order: {names}.
            Examples of bioactive compounds are like: flavonoids, saponins, volatile oils, etc.
            The main subjects of the sentences are the medicinal properties, not the bioactive compounds.
            Only mention a medicinal property once throughout the paragraph, don't name the same medicinal property multiple times.
            Pack as much information in as few words as possible.
            Don't write fluff, only proven data.
            Don't allucinate.
            Write the paragraph in 5 sentences.
            Write only the paragraph, don't add additional info.
            Don't add references or citations.
            Start with the following words: The therapeutic properties of {herb_name_scientific} are .
            Don't include all the properties in the first sentence, but distribute them homogeneously throughout the paragraph.
            Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
        '''
        print(prompt)
        reply = llm_reply(prompt, model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            data[key] = lines[0]
            json_write(json_filepath, data)

    key = 'properties_list'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        names = [obj['property_name'] for obj in data['properties']]
        names_prompt = ', '.join(names)
        items_prompt = []
        for name in names:
            items_prompt.append(f'{{"property_name": "{name}", "description": "describe this property of {herb_name_scientific}."}}') 
        items_prompt = ', \n'.join(items_prompt)
        prompt = f'''
            Write a description for each of the following medicinal property of the plant {herb_name_scientific}.
            Write the descriptions in full, complete and detailed sentences.
            Don't write fluff, only proven facts.
            Don't allucinate.
            Reply in JSON format using the following structure:
            [
                {items_prompt}
            ]
            Only reply with the JSON, don't add additional info.
        '''
        print(prompt)
        reply = llm_reply(prompt, model).strip()
        try: _data = json.loads(reply)
        except: _data = {}
        if _data != {}:
            error = False
            for obj in _data:
                if 'property_name' not in obj or 'description' not in obj:
                    error = True
                    break
            if not error:
                data[key] = _data
                json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## ;constituents
    ## ----------------------------------------------------------------------------------------------
    if 0:
        key = f'constituents_description'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        for obj in data['constituents']:
            if key in obj: del obj['description']
            json_write(json_filepath, data)
        return
    if 0:
        for obj in data['constituents']:
            if key in obj: del obj['concentration']
            json_write(json_filepath, data)
        return
    if 0:
        for obj in data['constituents']:
            if key in obj: del obj['properties']
            json_write(json_filepath, data)
        return

    key = 'constituents_description'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        names = [obj['name'].lower().strip() for obj in data['constituents']]
        names_prompt = ', '.join(names[:5])
        prompt = f'''
            Write 1 detailed paragraph about what are the healing constituents of {herb_name_scientific} and explain why.
            Include the following constituents: {names_prompt}.
            Pack as much information in as few words as possible.
            Don't write fluff, only proven data.
            Don't allucinate.
            Don't write the character ";".
            Write the paragraph in 5 sentences.
            Start the reply with the following words: The healing constituents of {herb_name_scientific} are .
        '''
        print(prompt)
        reply = llm_reply(prompt, model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            data[key] = lines[0]
            json_write(json_filepath, data)

    for obj in data['constituents']:
        key = 'description'
        if key not in obj: obj[key] = ''
        # obj[key] = ''
        if obj[key] == '':
            name = obj['name']
            prompt = f'''
                Write a short 1-sentence description of following medicinal constituent of the plant {herb_name_scientific}: {name}.
                In the description include the name of the constituent and state its properties without explaining why they give their health benefits.
                Don't mention anything about the validity of the information or if its effected are recognized or documented.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the following structure:
                {{
                    "name": "{name}", 
                    "description": "<write the description here>"
                }}
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            try: _data = json.loads(reply)
            except: _data = {}
            if _data != {}:
                if 'name' in _data and 'description' in _data:
                    obj[key] = _data['description']
                    json_write(json_filepath, data)

    for obj in data['constituents']:
        key = 'concentration'
        if key not in obj: obj[key] = ''
        # obj[key] = ''
        if obj[key] == '':
            name = obj['name']
            prompt = f'''
                Write the estimate concentration for the following medicinal constituent of the plant {herb_name_scientific}: {name}.
                Write the concentration by choosing only from the following words: "high", "medium", "low".
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the following structure:
                {{
                    "name": "{name}", 
                    "concentration": "estimate the concentration by writing only high, medium, or low"
                }}
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            try: _data = json.loads(reply)
            except: _data = {}
            if _data != {}:
                if 'name' in _data and 'concentration' in _data:
                    obj[key] = _data['concentration']
                    json_write(json_filepath, data)

    for obj_i, obj in enumerate(data['constituents']):
        key = 'properties'
        if key not in obj: obj[key] = ''
        # obj[key] = ''
        if obj[key] == '':
            name = obj['name']
            prompt = f'''
                Write a list of properies for the following medicinal constituent of the plant {herb_name_scientific}: {name}.
                Examples of properties are: antimicrobial, antioxidant, anti-inflammatory, analgesic, pain relief, etc.
                Write only the names of the properties, don't add additional info.
                Write as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the following structure:
                {{
                    "name": "{name}", 
                    "properties": "[property 1, property 2, property 3, etc.]"
                }}
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            try: _data = json.loads(reply)
            except: _data = {}
            if _data != {}:
                if 'name' in _data and 'properties' in _data:
                    obj[key] = _data['properties']
                    json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## ;parts
    ## ----------------------------------------------------------------------------------------------
    if 0:
        key = f'parts_desciption'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        key = f'parts_list'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        for obj in data['parts']:
            if key in obj: del obj['constituents']
            json_write(json_filepath, data)
        return

    key = 'parts_description'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        names = [obj['name'].lower().strip() for obj in data['parts'] if obj['total_score'] >= 6]
        names_prompt = ', '.join(names[:10])
        prompt = f'''
            Write 1 detailed paragraph about what are the parts of the plant {herb_name_scientific} that are used medicinally.
            In specific, discuss the following parts: {names}.
            Only discuss the parts listed above, don't write about other parts.
            Explain what are the primary bioactive compounds of each part.
            Examples of bioactive compounds are like: flavonoids, saponins, volatile oils, etc.
            Explain what are the primary medicinal properties of each part.
            Examples of medicinal properties are like: anti-inflammatory, antioxidant, analgesic, etc.
            Pack as much information in as few words as possible.
            Don't write fluff, only proven data.
            Don't allucinate.
            Write the paragraph in 5 sentences.
            Write only the paragraph, don't add additional info.
            Don't add references or citations.
            Start with the following words: The most used parts of {herb_name_scientific} for medicinal purposes are {names}.
            Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
        '''
        reply = llm_reply(prompt, model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            data[key] = lines[0]
            json_write(json_filepath, data)

    key = 'parts_list'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        names = [obj['name'] for obj in data['parts'] if obj['total_score'] >= 6]
        names_prompt = ', '.join(names)
        items_prompt = []
        for name in names:
            items_prompt.append(f'{{"name": "{name}", "description": "<write the description here starting with the words: The {name} of this plant "}}') 
        items_prompt = ', \n'.join(items_prompt)
        prompt = f'''
            Write a 1-sentence detailed description for each of the following parts of the plant {herb_name_scientific}: {names_prompt}.
            In each description, explain what are the major bioactive compouns of that part, what are the main medicinal properties, and what are the primary health benefits.
            Don't explain what this part is, don't give a definition for the part, don't explaing how this part is made.
            Explain only what are the medicinal properties of the plant and what are their major bioactive compounds.
            Never include the name of the plant in the description.
            Write the descriptions in full, complete and detailed sentences.
            Pack as much information in as few words as possible.
            Don't write fluff, only proven facts.
            Don't allucinate.
            Reply in JSON format using the following structure:
            [
                {items_prompt}
            ]
            Only reply with the JSON, don't add additional info.
        '''
        reply = llm_reply(prompt, model).strip()
        try: _data = json.loads(reply)
        except: _data = {}
        if _data != {}:
            error = False
            for obj in _data:
                if 'name' not in obj or 'description' not in obj:
                    error = True
                    break
            if not error:
                data[key] = _data
                json_write(json_filepath, data)

    for obj in data['parts']:
        key = 'constituents'
        if key not in obj: obj[key] = ''
        # obj[key] = ''
        if obj[key] == '':
            name = obj['name']
            prompt = f'''
                Write a list of the 10 major medicinal constituents found in the following part of the plant {herb_name_scientific}: {name}.
                Examples of medicinal constituents are like: flavonoids, saponins, volatile oils, etc.
                Write only the names of the constituents, don't add additional info.
                Write as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the following structure:
                {{
                    "name": "{name}", 
                    "constituents": "[constituent 1, constituent 2, constituent 3, etc.]"
                }}
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            try: _data = json.loads(reply)
            except: _data = {}
            if _data != {}:
                if 'name' in _data and 'constituents' in _data:
                    obj[key] = _data['constituents']
                    json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## ;preparations
    ## ----------------------------------------------------------------------------------------------
    # TODO: rerun the delete of preparations_ailments?
    if 0:
        for obj in data['preparations']:
            if key in obj: del obj['preparation_ailments']
            json_write(json_filepath, data)
        return
    if 0:
        key = f'preparation_description'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        key = f'preparations_list'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        for obj in data['preparations']:
            if key in obj: del obj['parts']
            json_write(json_filepath, data)
        return
    if 0:
        for obj in data['preparations']:
            if key in obj: del obj['overview']
            json_write(json_filepath, data)
        return
    if 0:
        for obj in data['preparations']:
            if key in obj: del obj['preparation_recipe']
            json_write(json_filepath, data)
        return


    for obj in data['preparations']:
        if obj['preparation_total_score'] <= score_min: continue 
        key = 'preparation_ailments'
        if key not in obj: obj[key] = ''
        # obj[key] = ''
        if obj[key] == '':
            preparation_name = obj['preparation_name']
            outputs = []
            tries_num = 1
            for i in range(tries_num):
                print(f'{i+1}/{tries_num} - {herb_i}/{len(herbs)}: {herb}')
                prompt = f'''
                    Write a list of the most common ailments that are treated with {herb_name_scientific} herbal {preparation_name}.
                    Also, give a confidence score in number format from 1 to 10 for each ailment representing how much you believe {herb_name_scientific} herbal {preparation_name} is widely adopted for that specific ailment.
                    Write only 1 ailment for each list item.
                    Never use the word "and".
                    Write only the names of the ailment, don't add descriptions.
                    Write the as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in JSON format using the structure in the following example:
                    [
                        {{"ailment_name": "<insert name of ailment 1 here>", "ailment_confidence_score": "10"}},
                        {{"ailment_name": "<insert name of ailment 2 here>", "ailment_confidence_score": "5"}},
                        {{"ailment_name": "<insert name of ailment 3 here>", "ailment_confidence_score": "7"}}
                    ]
                    Reply only with the JSON, don't add additional content.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    ailments = []
                    for item in json_data:
                        try: ailment_name = item['ailment_name']
                        except: continue
                        try: ailment_confidence_score = item['ailment_confidence_score']
                        except: continue
                        ailments.append({
                            "ailment_name": ailment_name, 
                            "ailment_confidence_score": ailment_confidence_score,
                        })
                    for ailment in ailments:
                        ailment_name = ailment['ailment_name'].lower().strip()
                        ailment_confidence_score = ailment['ailment_confidence_score']
                        found = False
                        for output in outputs:
                            if ailment_name in output['ailment_name']: 
                                output['ailment_mentions'] += 1
                                output['ailment_confidence_score'] += int(ailment_confidence_score)
                                found = True
                                break
                        if not found:
                            outputs.append({
                                'ailment_name': ailment_name, 
                                'ailment_mentions': 1, 
                                'ailment_confidence_score': int(ailment_confidence_score), 
                            })
            outputs_final = []
            for output in outputs:
                outputs_final.append({
                    'ailment_name': output['ailment_name'],
                    'ailment_confidence_score': int(output['ailment_mentions']) * int(output['ailment_confidence_score']),
                })
            outputs_final = sorted(outputs_final, key=lambda x: x['ailment_confidence_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output in outputs_final:
                print(output)
            print('***********************')
            print('***********************')
            print('***********************')
            obj[key] = outputs_final[:20]
            json_write(json_filepath, data)

    key = 'preparation_description'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        names = [obj['preparation_name'].lower().strip() for obj in data['preparations'] if obj['preparation_total_score'] >= score_min]
        names_prompt = ', '.join(names[:])
        prompt = f'''
            Write 1 detailed paragraph about what are the medicinal preparations of the plant {herb_name_scientific}, and explain for what they are used for.
            Discuss the following preparations in this exact order: {names}.
            The main subjects of the sentences are the preparations.
            Only mention a preparation once throughout the paragraph, don't name the same preparation multiple times.
            Pack as much information in as few words as possible.
            Don't write fluff, only proven data.
            Don't allucinate.
            Write the paragraph in 5 sentences.
            Write only the paragraph, don't add additional info.
            Don't add references or citations.
            Start with the following words: The most common herbal preparation of {herb_name_scientific} for medicinal purposes are .
            Don't include all the preparations in the first sentence, but distribute them homogeneously throughout the paragraph.
            Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
        '''
        print(prompt)
        reply = llm_reply(prompt, model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            data[key] = lines[0]
            json_write(json_filepath, data)

    if 0:
        key = 'preparations_list'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            names = [obj['preparation_name'] for obj in data['preparations'] if obj['preparation_total_score'] >= score_min]
            items_prompt = []
            for name in names:
                items_prompt.append(f'{{"preparation_name": "{name}", "description": "describe why {herb_name_scientific} {name} is used for this condition."}}') 
            items_prompt = ', \n'.join(items_prompt)
            prompt = f'''
                Write a description for each of the following herbal preparations of the plant {herb_name_scientific} on what are their most common medicinal uses.
                Write the descriptions in full, complete and detailed sentences.
                Don't write fluff, only proven facts.
                Don't allucinate.
                DOn't include the name of the plant.
                Reply in JSON format using the following structure:
                [
                    {items_prompt}
                ]
                Only reply with the JSON, don't add additional info.
            '''
            print(prompt)
            reply = llm_reply(prompt, model).strip()
            try: _data = json.loads(reply)
            except: _data = {}
            if _data != {}:
                error = False
                for obj in _data:
                    if 'preparation_name' not in obj or 'description' not in obj:
                        error = True
                        break
                if not error:
                    data[key] = _data
                    json_write(json_filepath, data)

    for obj in data['preparations']:
        if obj['preparation_total_score'] <= score_min: continue
        key = 'preparation_list_description'
        if key not in obj: obj[key] = ''
        # obj[key] = ''
        if obj[key] == '':
            preparation_name = obj['preparation_name']
            prompt = f'''
                Write a 1-sentence detailed description for the following medicinal preparation the plant {herb_name_scientific}: {preparation_name}.
                In the description explain what are the most common medicinal uses of the praparation.
                Write as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Don't include how the medicinal preparation is made, extracted or from which part of the plant it comes from.
                Don't include the name of the plant.
                Reply in JSON format using the following structure:
                {{
                    "preparation_name": "{preparation_name}", 
                    "preparation_description": "<write the 1-sentence description here>"
                }}
                Only reply with the JSON, don't add additional info.
                Start the description with these words: "{preparation_name.capitalize()} made from this plant ".
            '''
            reply = llm_reply(prompt, model).strip()
            try: _data = json.loads(reply)
            except: _data = {}
            if _data != {}:
                if 'preparation_name' in _data and 'preparation_description' in _data:
                    obj[key] = _data['preparation_description']
                    json_write(json_filepath, data)

    for obj in data['preparations']:
        if obj['preparation_total_score'] <= score_min: continue
        key = 'preparation_parts'
        if key not in obj: obj[key] = ''
        # obj[key] = ''
        if obj[key] == '':
            parts_names = [x['name'].lower().strip() for x in data['parts'] if x['total_score'] >= score_min]
            parts_names_prompt = ', '.join(parts_names)
            preparation_name = obj['preparation_name']
            prompt = f'''
                Write a list of the most used parts of the plant {herb_name_scientific} used to make the following medicinal preparation: {preparation_name}.
                Only choose from the following botanical parts: {parts_names_prompt}.
                Write only the names of the parts, don't add additional info.
                Write as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the following structure:
                {{
                    "preparation_name": "{preparation_name}", 
                    "preparation_parts": "[part 1, part 2, part 3, etc.]"
                }}
                Only reply with the JSON, don't add additional info.
            '''
            prompt = f'''
                Choose from the following list of PARTS of the plant {herb_name_scientific} the ones that are most used to make the following medicinal PREPARATION.
                PREPARATION: {preparation_name}.
                PARTS: {parts_names_prompt}.
                Write only the names of the parts, don't add additional info.
                Write as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the following structure:
                {{
                    "preparation_name": "{preparation_name}", 
                    "preparation_parts": "[part 1, part 2, part 3, etc.]"
                }}
                Only reply with the JSON, don't add additional info.
            '''
            try: _data = json.loads(reply)
            except: _data = {}
            if _data != {}:
                if 'preparation_name' in _data and 'preparation_parts' in _data:
                    valid = True
                    for preparation_part in _data['preparation_parts']:
                        if preparation_part.strip().lower() not in parts_names:
                            valid = False
                            break
                    if valid: 
                        obj[key] = _data['preparation_parts']
                        json_write(json_filepath, data)

    # h3 - overview
    for obj in data['preparations']:
        if obj['preparation_total_score'] <= score_min: continue 
        preparation_name = obj['preparation_name']
        ailments_names = [x['ailment_name'] for x in obj['preparation_ailments']]
        ailments_names_prompt = ', '.join(ailments_names)
        parts_names = [x for x in obj['preparation_parts']]
        parts_names_prompt = ', '.join(parts_names)
        preparation_difficulty_score = obj['preparation_difficulty_score']
        if preparation_difficulty_score < 4: preparation_difficulty_score_str = 'easy'
        elif preparation_difficulty_score < 7: preparation_difficulty_score_str = 'moderately difficult'
        elif preparation_difficulty_score < 10: preparation_difficulty_score_str = 'hard'
        preparation_power_score = obj['preparation_power_score']
        if preparation_power_score < 4: preparation_power_score_str = 'weak'
        elif preparation_power_score < 7: preparation_power_score_str = 'moderate'
        elif preparation_power_score < 10: preparation_power_score_str = 'strong'
        preparation_usage_score = obj['preparation_usage_score']
        if preparation_usage_score < 4: preparation_usage_score_str = 'uncommon'
        elif preparation_usage_score < 7: preparation_usage_score_str = 'common'
        elif preparation_usage_score < 10: preparation_usage_score_str = 'very common'
        key = 'preparation_overview'
        if key not in obj: obj[key] = ''
        # obj[key] = ''
        if obj[key] == '':
            prompt = f'''
                Write a detailed paragraph for an article about {herb_name_scientific} herbal {preparation_name} and using the following GUIDELINES, and STURUCTURE.
                <GUIDELINES>
                Write as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Don't add new empty lines between sentences. Reply with 1 paragraph.
                Use a conversational style of writing.
                Start the reply with the following words: {herb_name_scientific} {preparation_name} .
                </GUIDELINES>
                <STURCTURE>
                Discuss that this preparation is used to treat {ailments_names_prompt}.
                Discuss that this preparation is {preparation_usage_score_str} used.
                Discuss that this preparation has a {preparation_usage_score_str} effect.
                Discuss that this preparation is made with {parts_names_prompt}.
                Discuss that this preparation is {preparation_difficulty_score_str} to make.
                </STURCTURE>
            '''
            print(prompt)
            reply = llm_reply(prompt, model).strip()
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                obj[key] = lines[0]
                json_write(json_filepath, data)

    for obj in data['preparations']:
        if obj['preparation_total_score'] <= score_min: continue 
        key = 'preparation_recipe'
        if key not in obj: obj[key] = ''
        # obj[key] = ''
        if obj[key] == '':
            preparation_name = obj['preparation_name']
            parts_names = [x for x in obj['preparation_parts']]
            parts_names_prompt = ', '.join(parts_names)
            _recipe_json = {}
            running = True
            _i = 0
            while(running):
                _i += 1
                if _i > 10: break
                prompt = f'''
                    Write a 5-step recipe on how to make {herb_name_scientific} herbal {preparation_name}.
                    Write each step of the recipe in one short complete sentence.
                    Include these ingredients: {parts_names_prompt}.
                    Don't include dosages.
                    Reply in JSON format using the following structure:
                    {{
                        "preparation_recipe": [
                            "<write step 1 here>", 
                            "<write step 2 here>", 
                            "<write step 3 here>", 
                            "<write step 4 here>", 
                            "<write step 5 here>"
                        ]
                    }}
                    Only reply with the JSON, don't add additional info.
                '''
                print(prompt)
                reply = llm_reply(prompt, model).strip()
                if "I can't" in reply or 'I cannot' in reply: break
                try: _recipe_json = json.loads(reply)
                except: _recipe_json = {}
                if _recipe_json == {}: continue
                if 'preparation_recipe' not in _recipe_json: continue
                steps_prompt = '\n '.join(_recipe_json['preparation_recipe'])
                prompt = f'''
                    Here's a list of STEPS for a recipe to make {herb_name_scientific} {preparation_name}. Tell me if the steps are congruent and don't contraddict each others, and explain me why.
                    Reply only with "yes" or "no" when telling me the congruency.
                    <STEPS>
                    {steps_prompt}
                    </STEPS>
                    Reply in JSON format using the following structure:
                    {{
                        "is_congruent": <insert yes or no here>, 
                        "explanation": <explain why>
                    }},
                    Only reply with the JSON, don't add additional info.
                '''
                print(prompt)
                reply = llm_reply(prompt, model).strip()
                try: _data = json.loads(reply)
                except: _data = {}
                if _data == {}: continue
                if 'is_congruent' in _data:
                    if _data['is_congruent'].lower().strip() == 'yes':
                        running = False
            if _recipe_json != {}:
                obj[key] = _recipe_json['preparation_recipe']
                json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## ;side_effects
    ## ----------------------------------------------------------------------------------------------
    # TODO: rerun the delete of preparations_ailments?
    if 0:
        key = f'side_effects_overview'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        for obj in data['side_effects']:
            if key in obj: del obj['side_effect_list_description']
            json_write(json_filepath, data)
        return

    key = 'side_effects_overview'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        side_effects_names = [obj['side_effect_name'].lower().strip() for obj in data['side_effects']]
        side_effects_names_prompt = ', '.join(side_effects_names[:10])
        prompt = f'''
            Write 1 detailed paragraph about what are the possible side effects of using improperly the plant {herb_name_scientific}.
            Discuss the following side effects in this exact order: {side_effects_names}.
            The main subjects of the sentences are the side effects.
            Only mention a side effect once throughout the paragraph, don't name the same side effect multiple times.
            Pack as much information in as few words as possible.
            Don't write fluff, only proven data.
            Don't allucinate.
            Write the paragraph in 5 sentences.
            Write only the paragraph, don't add additional info.
            Don't add references or citations.
            Start with the following words: The possible side effects of improperly using {herb_name_scientific} are  .
            Don't include all the side effects in the first sentence, but distribute them homogeneously throughout the paragraph.
            Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
        '''
        reply = llm_reply(prompt, model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            data[key] = lines[0]
            json_write(json_filepath, data)

    for obj in data['side_effects']:
        key = 'side_effect_list_description'
        if key not in obj: obj[key] = ''
        # obj[key] = ''
        if obj[key] == '':
            side_effect_name = obj['side_effect_name']
            prompt = f'''
                Write a 1-sentence detailed description for the following side effect of the plant {herb_name_scientific}: {side_effect_name}.
                Write as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Reply in JSON format using the following structure:
                {{
                    "side_effect_name": "{side_effect_name}", 
                    "side_effect_description": "<write the 1-sentence description here>"
                }}
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            try: _data = json.loads(reply)
            except: _data = {}
            if _data != {}:
                if 'side_effect_name' in _data and 'side_effect_description' in _data:
                    obj[key] = _data['side_effect_description']
                    json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## ;precautions
    ## ----------------------------------------------------------------------------------------------
    if 0:
        key = f'precautions_overview'
        if key in data: del data[key]
        json_write(json_filepath, data)
        return
    if 0:
        for obj in data['precautions']:
            if key in obj: del obj['precaution_list_description']
            json_write(json_filepath, data)
        return

    key = 'precautions_overview'
    if key not in data: data[key] = ''
    # data[key] = ''
    if data[key] == '':
        precautions_names = [obj['precaution_name'].lower().strip() for obj in data['precautions']]
        precautions_names_prompt = ', '.join(precautions_names[:10])
        prompt = f'''
            Write 1 detailed paragraph about what are the precautions to take before using the plant {herb_name_scientific} medicinally.
            Discuss the following precautions in this exact order: {precautions_names}.
            The main subjects of the sentences are the precautions.
            Only mention a precaution once throughout the paragraph, don't name the same precaution multiple times.
            Pack as much information in as few words as possible.
            Don't write fluff, only proven data.
            Don't allucinate.
            Write the paragraph in 5 sentences.
            Write only the paragraph, don't add additional info.
            Don't add references or citations.
            Start with the following words: The precautions to take before using {herb_name_scientific} medicinally are  .
            Don't include all the precautions in the first sentence, but distribute them homogeneously throughout the paragraph.
            Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
        '''
        print(prompt)
        reply = llm_reply(prompt, model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            data[key] = lines[0]
            json_write(json_filepath, data)
        else:
            print('########################################')
            print(lines)
            print('########################################')

    for obj in data['precautions']:
        key = 'precaution_list_description'
        if key not in obj: obj[key] = ''
        # obj[key] = ''
        if obj[key] == '':
            precaution_name = obj['precaution_name']
            prompt = f'''
                Write a 1-sentence detailed description for the following precaution of the plant {herb_name_scientific}: {precaution_name}.
                Write as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Reply in JSON format using the following structure:
                {{
                    "precaution_name": "{precaution_name}", 
                    "precaution_description": "<write the 1-sentence description here>"
                }}
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            try: _data = json.loads(reply)
            except: _data = {}
            if _data != {}:
                if 'precaution_name' in _data and 'precaution_description' in _data:
                    obj[key] = _data['precaution_description']
                    json_write(json_filepath, data)

    ## ----------------------------------------------------------------------------------------------
    ## ----------------------------------------------------------------------------------------------
    ## ----------------------------------------------------------------------------------------------
    ## ;html
    ## ----------------------------------------------------------------------------------------------
    ## ----------------------------------------------------------------------------------------------
    ## ----------------------------------------------------------------------------------------------
    article_html = ''
    article_html += f'<h1>{title}</h1>\n'
    article_html += f'<img class="mb-16" src="{src_intro}" alt="{alt_intro}">\n'
    article_html += f'{util.text_format_1N1_html(data["intro_description"])}\n'
    if data['intro_study'] != []:
        article_html += f'<div class="study-featured">'
        article_html += f'<p class="text-bold">Featured Study:</p>'
        article_html += f'<p class="pb-0 mb-0">{data["intro_study"][0]}</p>'
        article_html += f'</div>\n'
    article_html += f'<p>The following article explains in detail what are the medicinal uses of {herb_name_scientific}, its health benefits, therapeutic properties, bioactive compounds, used parts, and herbal preparation. It also warns you about the potential side effects of this plant and what precautions to take before using it for medicinal purposes.</p>\n'
    article_html += f'<p><strong>ARTICLE SUMMARY:</strong> The table below summarizes the most crucial information about {herb_name_scientific} provided in the article below, which is useful if you are in a hurry and don\'t have time to dig deep into the very detailed content that follows.</p>\n'
    article_html += f'<table>\n'
    article_html += f'<tr>\n'
    article_html += f'<th>Medicinal Aspect</th>\n'
    article_html += f'<th>Summary</th>\n'
    article_html += f'</tr>\n'
    lst = ', '.join([x['condition_name'].capitalize() for x in data['uses_list'][:10]])
    article_html += f'<tr>\n'
    article_html += f'<td>Uses</td>\n'
    article_html += f'<td>{lst}</td>\n'
    article_html += f'</tr>\n'
    lst = ', '.join([x['name'].capitalize() for x in data['benefits'][:10]])
    article_html += f'<tr>\n'
    article_html += f'<td>Benefits</td>\n'
    article_html += f'<td>{lst}</td>\n'
    article_html += f'</tr>\n'
    lst = ', '.join([x['property_name'].capitalize() for x in data['properties'][:10]])
    article_html += f'<tr>\n'
    article_html += f'<td>Properties</td>\n'
    article_html += f'<td>{lst}</td>\n'
    article_html += f'</tr>\n'
    lst = ', '.join([x['name'].capitalize() for x in data['constituents'][:10]])
    article_html += f'<tr>\n'
    article_html += f'<td>Constituents</td>\n'
    article_html += f'<td>{lst}</td>\n'
    article_html += f'</tr>\n'
    lst = ', '.join([x['name'].capitalize() for x in data['parts'][:10] if x['total_score'] > score_min])
    article_html += f'<tr>\n'
    article_html += f'<td>Parts</td>\n'
    article_html += f'<td>{lst}</td>\n'
    article_html += f'</tr>\n'
    lst = ', '.join([x['preparation_name'].capitalize() for x in data['preparations'][:10] if x['preparation_total_score'] > score_min])
    article_html += f'<tr>\n'
    article_html += f'<td>Preparations</td>\n'
    article_html += f'<td>{lst}</td>\n'
    article_html += f'</tr>\n'
    lst = ', '.join([x['side_effect_name'].capitalize() for x in data['side_effects'][:10]])
    article_html += f'<tr>\n'
    article_html += f'<td>Side Effects</td>\n'
    article_html += f'<td>{lst}</td>\n'
    article_html += f'</tr>\n'
    lst = ', '.join([x['precaution_name'].capitalize() for x in data['precautions'][:10]])
    article_html += f'<tr>\n'
    article_html += f'<td>Precaution</td>\n'
    article_html += f'<td>{lst}</td>\n'
    article_html += f'</tr>\n'
    article_html += f'</table>\n'
    article_html += f'<p><strong>BONUS CHEATSHEET:</strong> The cheatsheet below illustrates the most important medicinal aspects of {herb_name_scientific}. Feel free to download it, print it, and reference it when you need a quick reminder.</p>\n'
    # ;cheatsheet
    article_html += f'<img class="mb-48" src="{src_intro_cheatsheet}" alt="{alt_intro_cheatsheet}">\n'

    # ;uses
    article_html += f'<h2>What are the main medicinal uses of {herb_name_scientific}?</h2>\n'
    article_html += f'{util.text_format_1N1_html(data["uses_description"])}\n'
    article_html += f'<p>The following illustration give a summary of the main medicinal uses of {herb_name_scientific}.</p>\n'
    article_html += f'<img class="mb-16" src="{src_uses}" alt="{alt_uses}">\n'
    article_html += f'<p>The list below provide more details on why {herb_name_scientific} is used to alleviate the health conditions mentioned in the illustration above.</p>\n'
    article_html += f'<ul>\n'
    for obj in data['uses_list'][:10]:
        name = obj["condition_name"].title()
        description = obj["description"]
        article_html += f'<li><strong>{name}:</strong> {obj["description"]}</li>\n'
    article_html += f'</ul>\n'
    article_html += f'<p>The table that follows gives an overview of what are the most common health conditions that are treated with {herb_name_scientific}, in each of the major medicinal systems.</p>\n'
    article_html += f'<table>\n'
    article_html += f'<tr>\n'
    article_html += f'<th>Medicinal System</th>\n'
    article_html += f'<th>Conditions Treated</th>\n'
    article_html += f'</tr>\n'
    for medicinal_system in medicinal_systems:
        medicinal_system_dash = medicinal_system.replace(' ', '-')
        medicinal_system_underline = medicinal_system.replace(' ', '_')
        ailments = ', '.join([obj['name'].title() for obj in data[f'uses_{medicinal_system_underline}']])
        article_html += f'<tr>\n'
        article_html += f'<td>{medicinal_system.title()}</td>\n'
        article_html += f'<td>{ailments}</td>\n'
        article_html += f'</tr>\n'
    article_html += f'</table>\n'
    for medicinal_system in medicinal_systems:
        medicinal_system_dash = medicinal_system.replace(' ', '-')
        medicinal_system_underline = medicinal_system.replace(' ', '_')
        article_html += f'<h3>{medicinal_system.title()}</h3>\n'
        key = f'uses_{medicinal_system_underline}_description'
        article_html += f'{util.text_format_1N1_html(data[key])}\n'

    # benefits
    article_html += f'<h2>What are the primary health benefits of {herb_name_scientific}?</h2>\n'
    article_html += f'{util.text_format_1N1_html(data["benefits_description"])}\n'
    article_html += f'<p>The following illustration give a summary of the primary health benefits of {herb_name_scientific}.</p>\n'
    article_html += f'<img class="mb-16" src="{src_benefits}" alt="{alt_benefits}">\n'
    article_html += f'<p>The list below provides more details on why {herb_name_scientific} offers the health benefits mentioned in the illustration above.</p>\n'
    article_html += f'<ul>\n'
    for obj in data['benefits_list'][:10]:
        name = obj["benefit_name"].title()
        description = obj["description"]
        article_html += f'<li><strong>{name}:</strong> {obj["description"]}</li>\n'
    article_html += f'</ul>\n'
    article_html += f'<p>The table that follows gives an overview of what are the primary health benefits of {herb_name_scientific} for each of the major body system.</p>\n'
    article_html += f'<table>\n'
    article_html += f'<tr>\n'
    article_html += f'<th>Body System</th>\n'
    article_html += f'<th>Health Benefits</th>\n'
    article_html += f'</tr>\n'
    for body_system in body_systems:
        benefits = ', '.join([obj['benefit_name'].title() for obj in data[f'benefits_{body_system}_system']])
        article_html += f'<tr>\n'
        article_html += f'<td>{body_system.title()} System</td>\n'
        article_html += f'<td>{benefits}</td>\n'
        article_html += f'</tr>\n'
    article_html += f'</table>\n'
    for body_system in body_systems:
        key = f'benefits_{body_system}_system_description'
        article_html += f'<h3>{body_system.title()} System</h3>\n'
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
        article_html += f'<p>The medicinal benefits of {herb_name_scientific} on the {body_system} system help relieving the health conditions listed below.</p>\n'
        key = f'benefits_{body_system}_system_ailments'
        article_html += f'<ul>\n'
        for obj in data[key][:10]:
            article_html += f'<li>{obj["name"].capitalize()}</li>\n'
        article_html += f'</ul>\n'

    # ;properties
    article_html += f'<h2>What are the dominant therapeutic properties of {herb_name_scientific}?</h2>\n'
    article_html += f'{util.text_format_1N1_html(data["properties_description"])}\n'
    article_html += f'<p>The following illustration give a summary of the dominant therapeutic properties of {herb_name_scientific}.</p>\n'
    article_html += f'<img class="mb-16" src="{src_properties}" alt="{alt_properties}">\n'
    article_html += f'<p>The list below provides more details on why {herb_name_scientific} has the therapeutic properties mentioned in the illustration above.</p>\n'
    article_html += f'<ul>\n'
    for obj in data['properties_list'][:10]:
        name = obj["property_name"].title()
        description = obj["description"]
        article_html += f'<li><strong>{name}:</strong> {obj["description"]}</li>\n'
    article_html += f'</ul>\n'

    # ;constituents
    article_html += f'<h2>What are the major healing constituents of {herb_name_scientific}?</h2>\n'
    article_html += f'{util.text_format_1N1_html(data["constituents_description"])}\n'
    article_html += f'<p>The following illustration give a summary of the major healing consitutents of {herb_name_scientific}.</p>\n'
    article_html += f'<img class="mb-16" src="{src_constituents}" alt="{alt_constituents}">\n'
    article_html += f'<p>The list below provides more details on what are the major healing constituents of {herb_name_scientific} and why they are important for health.'
    article_html += f'<ul>\n'
    for obj in data['constituents'][:10]:
        name = obj["name"]
        description = obj["description"]
        article_html += f'<li><strong>{name}:</strong> {obj["description"]}</li>\n'
    article_html += f'</ul>\n'
    article_html += f'<p>The table that follows estimates the relative concentrations of the main medicinal constituents contained in {herb_name_scientific} and lists the most relevant medicinal properties of each constituent based on the corresponding concentrations.</p>\n'
    article_html += f'<table>\n'
    article_html += f'<tr>\n'
    article_html += f'<th>Constituent</th>\n'
    article_html += f'<th>Concentration</th>\n'
    article_html += f'<th>Properties</th>\n'
    article_html += f'</tr>\n'
    for obj in data['constituents'][:10]:
        name = obj["name"]
        concentration = obj["concentration"].upper()
        properties = ', '.join([x.capitalize() for x in obj["properties"]])
        article_html += f'<tr>\n'
        article_html += f'<td>{name}</td>\n'
        article_html += f'<td>{concentration}</td>\n'
        article_html += f'<td>{properties}</td>\n'
        article_html += f'</tr>\n'
    article_html += f'</table>\n'

    ## ;parts
    article_html += f'<h2>What are the most used parts of {herb_name_scientific} in medicine?</h2>\n'
    article_html += f'{util.text_format_1N1_html(data["parts_description"])}\n'
    article_html += f'<p>The following illustration give a summary of the most used parts of {herb_name_scientific} in medicine.</p>\n'
    article_html += f'<img class="mb-16" src="{src_parts}" alt="{alt_parts}">\n'
    article_html += f'<p>The list below provides more details on what are the most used parts of {herb_name_scientific} in medicine and why.'
    article_html += f'<ul>\n'
    for obj in data['parts_list']:
        name = obj["name"].title()
        description = obj["description"]
        article_html += f'<li><strong>{name}:</strong> {obj["description"]}</li>\n'
    article_html += f'</ul>\n'
    article_html += f'<p>The table that follows gives a more complete list of healing constituents found in each part of {herb_name_scientific} mentioned above.</p>\n'
    article_html += f'<table>\n'
    article_html += f'<tr>\n'
    article_html += f'<th>Part</th>\n'
    article_html += f'<th>Constituents</th>\n'
    '''
    article_html += f'<th>Mentions</th>\n'
    article_html += f'<th>Presence</th>\n'
    article_html += f'<th>Health</th>\n'
    article_html += f'<th>Usage</th>\n'
    article_html += f'<th>Power</th>\n'
    article_html += f'<th>Total</th>\n'
    '''
    article_html += f'</tr>\n'
    for obj in data['parts']:
        if obj['name'] != '' and obj['constituents'] != '':
            name = obj["name"].title()
            constituents = ', '.join([x.capitalize() for x in obj["constituents"]])
            mentions = obj["mentions"]
            presence_score = obj["presence_score"]
            health_score = obj["health_score"]
            usage_score = obj["usage_score"]
            power_score = obj["power_score"]
            total_score = obj["total_score"]
            if total_score >= 6:
                article_html += f'<tr>\n'
                article_html += f'<td>{name}</td>\n'
                article_html += f'<td>{constituents}</td>\n'
                '''
                article_html += f'<td>{mentions}</td>\n'
                article_html += f'<td>{presence_score}</td>\n'
                article_html += f'<td>{health_score}</td>\n'
                article_html += f'<td>{usage_score}</td>\n'
                article_html += f'<td>{power_score}</td>\n'
                article_html += f'<td>{total_score}</td>\n'
                '''
                article_html += f'</tr>\n'
    article_html += f'</table>\n'

    ## ;preparations
    article_html += f'<h2>What are the most common medicinal preparations of {herb_name_scientific}?</h2>\n'
    article_html += f'{util.text_format_1N1_html(data["preparation_description"])}\n'
    article_html += f'<p>The following illustration give a summary of the most common medicinal preparations of {herb_name_scientific}.</p>\n'
    article_html += f'<img class="mb-16" src="{src_preparations}" alt="{alt_preparations}">\n'
    article_html += f'<p>The list below provides more details on what are the most common medicinal preparations of {herb_name_scientific} and what are their main uses.'
    article_html += f'<ul>\n'
    for obj in data['preparations']:
        if obj['preparation_total_score'] <= score_min: continue
        preparation_name = obj["preparation_name"].title()
        preparation_list_description = obj["preparation_list_description"]
        if preparation_name.lower() == 'suppository': continue
        article_html += f'<li><strong>{preparation_name}:</strong> {preparation_list_description}</li>\n'
    article_html += f'</ul>\n'
    article_html += f'<p>The table that follows shows what are the most used parts of {herb_name_scientific} for each medicinal preparation.</p>\n'
    article_html += f'<table>\n'
    article_html += f'<tr>\n'
    article_html += f'<th>Preparation</th>\n'
    article_html += f'<th>Parts</th>\n'
    article_html += f'</tr>\n'
    for obj in data['preparations']:
        if obj['preparation_total_score'] <= score_min: continue
        preparation_name = obj["preparation_name"].capitalize()
        preparation_parts = ', '.join([x.capitalize() for x in obj["preparation_parts"]])
        if preparation_name.lower() == 'suppository': continue
        article_html += f'<tr>\n'
        article_html += f'<td>{preparation_name}</td>\n'
        article_html += f'<td>{preparation_parts}</td>\n'
        article_html += f'</tr>\n'
    article_html += f'</table>\n'

    ## TODO:
    ## do h3 content for preparations
    ## include uses, difficulty of preparation, adoption, power, recipe (ingredients form "parts")
    for obj in data['preparations']:
        if obj['preparation_total_score'] <= score_min: continue
        preparation_name = obj['preparation_name']
        preparation_slug = preparation_name.lower().strip().replace(' ', '-')
        if preparation_name.lower() == 'suppository': continue
        article_html += f'<h3>{preparation_name.title()}</h3>\n'
        article_html += f'{util.text_format_1N1_html(obj["preparation_overview"])}\n'
        key = 'preparation_image'
        if key in obj: 
            if obj[key] != '':
                if preparation_slug != 'decoction' and preparation_slug != 'poultice' and preparation_slug != 'capsule': 
                    src = f'/images/herbs/{herb_slug}-{preparation_slug}.jpg'
                    alt = f'{preparation_name} made with {herb_name_scientific}'
                    article_html += f'<p>Below you find an image of {herb_name_scientific} {preparation_name}.</p>\n'
                    article_html += f'<img class="mb-16" src="{src}" alt="{alt}">\n'
        key = 'preparation_recipe'
        if key in obj: 
            if obj[key] != '':
                article_html += f'<p>Below you find a 5-step quick procedure to make effective medicinal {herb_name_scientific} {preparation_name}.</p>\n'
                article_html += f'<ol>\n'
                for step in obj[key]:
                    article_html += f'<li>{step}</li>\n'
                article_html += f'</ol>\n'

    ## ;side effects
    article_html += f'<h2>What are the possible side effects of {herb_name_scientific} if used improperly?</h2>\n'
    article_html += f'{util.text_format_1N1_html(data["side_effects_overview"])}\n'
    article_html += f'<p>The most common side effects {herb_name_scientific} gives people when used improperly are listed below, along with a brief explanation.</p>'
    article_html += f'<ul>\n'
    for obj in data['side_effects']:
        side_effect_name = obj["side_effect_name"].title()
        side_effect_list_description = obj["side_effect_list_description"]
        article_html += f'<li><strong>{side_effect_name}:</strong> {side_effect_list_description}</li>\n'
    article_html += f'</ul>\n'

    ## ;precautions
    article_html += f'<h2>What are the precautions to take before using {herb_name_scientific} medicinally?</h2>\n'
    article_html += f'{util.text_format_1N1_html(data["precautions_overview"])}\n'
    article_html += f'<p>The most important precautions you must take before using {herb_name_scientific} for medicinal purposes are listed below, along with a brief explanation.</p>'
    article_html += f'<ul>\n'
    for obj in data['precautions']:
        name = obj["precaution_name"].title()
        description = obj["precaution_list_description"]
        article_html += f'<li><strong>{name}:</strong> {description}</li>\n'
    article_html += f'</ul>\n'

    ## ;studies
    studies = data['intro_study'][1:4]
    if len(studies) > 0:
        article_html += f'<h2>Are there scientific studies that prove the medical effectiveness of {herb_name_scientific}?</h2>\n'
        if len(studies) == 1:
            article_html += f'<p>Yes, there are several scientific studies that prove the medicianl effectiveness of {herb_name_scientific}. The following is an interesting one.</p>'
            for study_i, study_text in enumerate(studies):
                article_html += f'<p>{study_text}</p>\n'
        if len(studies) > 1:
            article_html += f'<p>Yes, there are several scientific studies that prove the medicianl effectiveness of {herb_name_scientific}. Here are some studies that are worthy of notice.</p>'
            for study_i, study_text in enumerate(studies):
                if study_i == 0:
                    article_html += f'<p>{study_text}</p>\n'
                elif study_i == 1:
                    study_text = study_text.replace(
                        'According to a study published by',
                        'In another study published by',
                    )
                    article_html += f'<p>{study_text}</p>\n'
                elif study_i == 2:
                    study_text = study_text.replace(
                        'According to a study published by',
                        'A different research published by',
                    )
                    article_html += f'<p>{study_text}</p>\n'

    ## ;related
    article_html += f'<h2>Related herbs to {herb_name_scientific}?</h2>\n'
    related_herbs = []
    try: 
        herb_1 = herbs[herb_i+1]
        herb_1_slug = herb_1['plant_name_scientific'].strip().lower().replace(' ', '-')
        data_1 = json_read(f'database/json/herbs/{herb_1_slug}.json')
        src_1 = data_1['intro_image']
        alt_1 = f"{herb_1['plant_name_scientific']} plant"
        related_herbs.append({
            'img_html': f'<img src="{src_1}" alt="{alt_1}">',
            'herb_name_scientific': data_1['herb_name_scientific'],
            'url': f'/{data_1["url"]}.html',
        })
    except: pass
    try:
        herb_2 = herbs[herb_i+2]
        herb_2_slug = herb_2['plant_name_scientific'].strip().lower().replace(' ', '-')
        data_2 = json_read(f'database/json/herbs/{herb_2_slug}.json')
        src_2 = data_2['intro_image']
        alt_2 = f"{herb_2['plant_name_scientific']} plant"
        related_herbs.append({
            'img_html': f'<img src="{src_2}" alt="{alt_2}">',
            'herb_name_scientific': data_2['herb_name_scientific'],
            'url': f'/{data_2["url"]}.html',
        })
    except: pass
    article_html += f'<div class="flex gap-64 justify-center">\n'
    for related_herb in related_herbs:
        url = related_herb['url']
        article_html += f'<div class="flex-1">\n'
        article_html += f'<a href="{url}">\n'
        article_html += f'{related_herb["img_html"]}\n'
        article_html += f'<h3>{related_herb["herb_name_scientific"]}</h3>\n'
        article_html += f'</a>\n'
        article_html += f'</div>\n'
    article_html += f'</div>\n'

    breadcrumbs = util.breadcrumbs(html_filepath)
    meta = components.meta(article_html, data["lastmod"])
    article = components.table_of_contents(article_html)
    html = templates.article(title, header_html, breadcrumbs, meta, article, footer_html)
    file_write(html_filepath, html)
    # quit()

main_herbs_popular()
herbs_book()

quit()
# TODO: complete homepage (bg and images and errors)
# TODO: check all images in articles for coherence
# TODO: check errors in other pages
