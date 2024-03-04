import time
import re

from groq import Groq

import util

client = Groq(
    api_key='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',
)



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



def ai_herbalism_teas_conditions_csv(condition, condition_i):
    print(f'{condition_i+1}/{len(conditions)} -- {condition}')
    filepath = 'database/tables/herbalism-teas-conditions.csv'
    rows = util.csv_get_rows_by_entity(filepath, condition)

    if rows != []: return

    prompt_paragraphs_num = 20
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} best herbal teas for {condition}.
        Write only the names of the herbs of the herbal teas, not the descriptions.
        Include only 1 herb for each list item.
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
            if '. ' in line: line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            if line.endswith('.'): line = line[0:-1]
            reply_formatted.append([condition, line, ''])

    if prompt_paragraphs_num == len(reply_formatted):
        print('***************************************')
        for line in reply_formatted:
            print(line)
        print('***************************************')

        util.csv_add_rows(filepath, reply_formatted)
        
    time.sleep(30)


def ai_herbalism_teas_conditions_csv_to_json():
    rows = util.csv_get_rows('database/tables/conditions.csv')
    conditions = [row[0] for row in rows[1:]]
    for condition in conditions:
        condition_dash = condition.lower().strip().replace(' ', '-')
        rows = util.csv_get_rows_by_entity('database/tables/herbalism-teas-conditions.csv', condition)
        
        if not rows: continue

        remedies = []
        for row in rows:
            remedies.append(
                {
                    'remedy_name': row[1],
                }
            )

        article_filepath = f'database/articles/herbalism/tea/{condition_dash}.json'
        data = util.json_read(article_filepath)

        remedies_json = []
        try: remedies_json = data['remedies']
        except: data['remedies'] = remedies_json

        if data['remedies']: continue

        data['remedies'] = remedies
        data = util.json_write(article_filepath, data)
        


def ai_herbalism_teas_conditions_description(condition, condition_i):
    condition_dash = condition.strip().lower().replace(' ', '-')
    filepath = f'database/articles/herbalism/tea/{condition_dash}.json'
    data = util.json_read(filepath)

    for index, remedy in enumerate(data['remedies']):
        print(f'{condition_i+1}/{len(conditions)} >> {index+1}/{len(data["remedies"])} -- {condition}')
        remedy_name = remedy['remedy_name']

        remedy_desc = ''
        try: remedy_desc = remedy['remedy_desc']
        except: remedy['remedy_desc'] = ''

        if remedy_desc != '': continue

        remedy_name_formatted = remedy_name.lower().strip() + ' tea'
        remedy_name_formatted = remedy_name_formatted.replace(' tea tea', ' tea')
        starting_text = f'{remedy_name_formatted.capitalize()} helps with {condition.lower()} because '
        prompt = f'''
            Explain in a 5-sentence paragraph why {remedy_name_formatted} helps with {condition.lower()}.
            Start with these words: {starting_text}
        '''     
        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()
        if starting_text.lower().strip() not in reply.lower():
            reply = starting_text + reply 

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
            line = line.replace('...', '')
            line = re.sub("\s\s+" , " ", line)
            reply_formatted.append(line)

        if reply_formatted == '' or len(reply_formatted) == 1:
            print('***************************************')
            for paragraph in reply_formatted:
                print(paragraph)
            print('***************************************')

            data['remedies'][index]['remedy_desc'] = reply_formatted[0]
            util.json_write(filepath, data)

        time.sleep(30)
        # return running


def ai_herbalism_teas_conditions_recipe(condition, condition_i):
    condition_dash = condition.strip().lower().replace(' ', '-')
    filepath = f'database/articles/herbalism/tea/{condition_dash}.json'
    data = util.json_read(filepath)

    if not data: return


    for index, remedy in enumerate(data['remedies']):
        print(f'{condition_i+1}/{len(conditions)} >> {index+1}/{len(data["remedies"])} -- {condition}')
        remedy_name = remedy['remedy_name']

        remedy_recipe = []
        try: remedy_recipe = remedy['remedy_recipe']
        except: remedy['remedy_recipe'] = []

        if remedy_recipe != []: continue

        remedy_name_formatted = remedy_name.lower().strip() + ' tea'
        remedy_name_formatted = remedy_name_formatted.replace(' tea tea', ' tea')
        prompt = f'''
            Write a detailed 5-step recipe in ordered list format on how to make {remedy_name_formatted} for {condition.lower()}.
            Include numbers like ingredient dosages and times of preparation in the steps when applicable.
            Each step must be only 1 sentence long.
        '''     
        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()

        reply_formatted = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if not line[0].isdigit(): continue
            
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            reply_formatted.append(line)

        if reply_formatted == '' or len(reply_formatted) == 5:
            print('***************************************')
            for paragraph in reply_formatted:
                print(paragraph)
            print('***************************************')

            data['remedies'][index]['remedy_recipe'] = reply_formatted
            util.json_write(filepath, data)

        time.sleep(30)


def ai_herbalism_teas_conditions_init(condition):
    condition_dash = condition.strip().lower().replace(' ', '-')
    filepath = f'database/articles/herbalism/tea/{condition_dash}.json'
    data = util.json_read(filepath)

    condition_json = ''
    try: condition_json = data['condition']
    except: data['condition'] = condition_json
    if condition_json == '': data['condition'] = condition

    preparation_json = ''
    try: preparation_json = data['preparation']
    except: data['preparation'] = preparation_json
    if preparation_json == '': data['preparation'] = 'tea'

    title_json = ''
    try: title_json = data['title']
    except: data['title'] = title_json
    if title_json == '': data['title'] = f'best herbal teas for {condition}'

    url_json = ''
    try: url_json = data['url']
    except: data['url'] = url_json
    if url_json == '': data['url'] = f'herbalism/tea/{condition_dash}'

    util.json_write(filepath, data)


rows = util.csv_get_rows('database/tables/conditions.csv')
conditions = [row[0] for row in rows[1:]]
for condition_i, condition in enumerate(conditions):
    ai_herbalism_teas_conditions_init(condition)

    # ai_herbalism_teas_conditions_csv(condition, condition_i)
    # ai_herbalism_teas_conditions_csv_to_json()

    # ai_herbalism_teas_conditions_description(condition, condition_i)
    # ai_herbalism_teas_conditions_recipe(condition, condition_i)
    
