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


ARTICLES_FILEPATH = 'articles-new.csv'

template = 'best herbal teas for <condition>'


def get_scientific_name(common_name, delimiter='\\'):
    rows = util.csv_get_rows('plants.csv', delimiter=delimiter)
    rows = [row for row in rows if row[1].lower().strip() in common_name.lower().strip()]
    scientific_name = rows[0][0].replace('-', ' ')
    return scientific_name


def scientific_names_check():
    for k, row in enumerate(articles_rows):
        keyword = row[0].strip()
        condition = row[1].strip().lower()
        folder = row[2].strip()
        preparation = row[3].strip().lower()

        condition_dash = condition.replace(' ', '-')

        data = util.json_read(f'database-new/articles/{folder}/{condition_dash}.json')
        remedies = data['remedies']
        herbs = [remedy['herb'] for remedy in remedies]

        for herb in herbs:
            try: 
                scientific_name = get_scientific_name(herb)
                print(herb, f'({scientific_name})')
            except:
                print(herb)


def scientific_names_missing():
    for k, row in enumerate(articles_rows):
        keyword = row[0].strip()
        condition = row[1].strip().lower()
        folder = row[2].strip()
        preparation = row[3].strip().lower()

        condition_dash = condition.replace(' ', '-')

        data = util.json_read(f'database-new/articles/{folder}/{condition_dash}.json')
        remedies = data['remedies']
        herbs = [remedy['herb'] for remedy in remedies]

        for herb in herbs:
            try: 
                scientific_name = get_scientific_name(herb)
            except:
                print(herb)

    


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



def init():
    for row in articles_rows:
        keyword = row[0].strip()
        condition = row[1].strip().lower()
        folder = row[2].strip()
        preparation = row[3].strip().lower()

        condition_dash = condition.replace(' ', '-')

        json_filepath = f'database-new/articles/{folder}/{condition_dash}.json'

        if util.file_read(json_filepath).strip() != '': continue

        data = {
            'remedy_num': 0,
            'title': keyword,
            'condition': condition,
            'preparation': preparation,
            'remedies': [],
        }

        util.json_write(json_filepath, data)


def ai_gen_remedies():
    for row in articles_rows:
        keyword = row[0].strip()
        condition = row[1].strip().lower()
        folder = row[2].strip()
        preparation = row[3].strip().lower()

        condition_dash = condition.replace(' ', '-')

        json_filepath = f'database-new/articles/{folder}/{condition_dash}.json'
        data = util.json_read(json_filepath)

        if len(data['remedies']) != 0: continue

        prompt = f'''
            Give me a numbered list of 30 {keyword}.
            Give me only the names, not the descriptions.
        '''
        prompt = '\n'.join([line.strip() for line in prompt.split('\n') if line.strip() != ''])
        reply = gen_reply(prompt).strip()

        lines = reply.split('\n')
        herbs = []
        for line in lines:
            line = line.strip().lower()
            if not line[0].isdigit(): continue
            if preparation not in line: continue
            if '. ' not in line: continue

            line = line.split('. ')[1]
            line = line.replace(preparation, '')
            line = line.strip()
            herbs.append(line)

        data['remedies'] = []
        for herb in herbs:
            data['remedies'].append(
                {
                    'herb': f'{herb}',
                    'preparation': f'{preparation}',
                    'intro': ''
                }
            )

        util.json_write(json_filepath, data)


def ai_gen_remedies_intro():
    for k, row in enumerate(articles_rows):
        keyword = row[0].strip()
        condition = row[1].strip().lower()
        folder = row[2].strip()
        preparation = row[3].strip().lower()

        condition_dash = condition.replace(' ', '-')

        json_filepath = f'database-new/articles/{folder}/{condition_dash}.json'

        data = util.json_read(json_filepath)
        remedies = data['remedies']

        for i, remedy in enumerate(remedies):
            print(k, len(articles_rows))
            print(i, len(remedies))
            herb = remedy['herb'].strip().lower()
            intro = remedy['intro'].strip()

            scientific_name = ''
            try: scientific_name = get_scientific_name(herb).capitalize()
            except: print(f'MISSING SCIENTIFIC NAME >> {herb}')

            if intro != '': continue

            prompt = f'''
                Explain why [0] [1] helps with [2]. 
                Answer in a 5-sentence paragraph without using lists. 
                Don't include studies.
                Don't include preparations.
            '''

            if scientific_name_formatted.strip() != '':
                scientific_name_formatted = f'({scientific_name})'
            prompt = prompt.replace('[0]', f'{herb} {scientific_name_formatted}')
            prompt = prompt.replace('[1]', preparation)
            prompt = prompt.replace('[2]', condition)
            reply = gen_reply(prompt)

            if ':' in reply: continue

            reply = reply.replace('\n', '')
            reply = re.sub("\s\s+" , " ", reply)

            data['remedies'][i]['intro'] = reply.strip()
            
            util.json_write(json_filepath, data)


def ai_gen_number():
    for row in articles_rows:
        keyword = row[0].strip()
        condition = row[1].strip().lower()
        folder = row[2].strip()
        preparation = row[3].strip().lower()

        condition_dash = condition.replace(' ', '-')

        json_filepath = f'database-new/articles/{folder}/{condition_dash}.json'
        data = util.json_read(json_filepath)

        try: number = data['remedy_num']
        except: data['remedy_num'] = 0

        if number == 0: data['remedy_num'] = random.choice([11, 13, 15])


        util.json_write(json_filepath, data)


# TODO: put al ai_gen functions inside this one
def ai_gen_json():
    conditions = [row[0] for row in util.csv_get_rows('conditions.csv')]

    articles = []
    for condition in conditions:
        keyword = template.replace('<condition>', condition)
        condition_dash = condition.replace(' ', '-')
        articles.append(
            {
                'keyword': keyword,
                'condition': condition,
                'preparation': 'tea',
                'url': f'herbalism/tea/{condition_dash}',
                'remedies': [],
                'supplementary': [],
            }
        ) 

    for article in articles:
        keyword = article['keyword'].strip()
        condition = article['condition'].strip().lower()
        preparation = article['preparation'].strip().lower()
        url = article['url'].strip()
        remedies = article['remedies']
        supplementary = article['supplementary']
        condition_dash = condition.replace(' ', '-')

        json_filepath = f'database/articles/{url}.json'
        data = util.json_read(json_filepath)

        number = data['remedy_num'] = random.choice([11, 13, 15])
        try: number = data['remedy_num']
        except: data['remedy_num'] = number
        util.json_write(json_filepath, data)
        
        try: keyword = data['keyword']
        except: data['keyword'] = keyword
        util.json_write(json_filepath, data)

        try: condition = data['condition']
        except: data['condition'] = condition
        util.json_write(json_filepath, data)
        
        try: preparation = data['preparation']
        except: data['preparation'] = preparation
        util.json_write(json_filepath, data)
        
        try: url = data['url']
        except: data['url'] = url
        util.json_write(json_filepath, data)
        
        try: remedies = data['remedies']
        except: data['remedies'] = remedies
        util.json_write(json_filepath, data)
        
        try: supplementary = data['supplementary']
        except: data['supplementary'] = supplementary
        util.json_write(json_filepath, data)

        intro_1 = ''
        try: intro_1 = data['intro_1']
        except: data['intro_1'] = ''
        if intro_1.strip() == '': 
            prompt = f'''
                Write a 5-line paragraph about [1]. 
                Include a definition of the problem.
                Include how many people have this problem in the world every year.
                Include how this problem can negatively affect their quality of life.
                Include which are the main causes that make people have this problem.
                Include what effects this problem has on other aspects of health.
                Include numbers, percentages, and statistics.
            '''
            prompt = prompt.replace('[1]', condition)
            reply = gen_reply(prompt).strip()
            if '\n' not in reply:
                data['intro_1'] = reply
                util.json_write(json_filepath, data)

        intro_2 = ''
        try: intro_2 = data['intro_2']
        except: data['intro_2'] = ''
        if intro_2.strip() == '': 
            prompt = f'''
                Write a 5-line paragraph about herbal tea for [1]. 
            '''
            prompt = prompt.replace('[1]', condition)
            reply = gen_reply(prompt).strip()
            if '\n' not in reply:
                data['intro_2'] = reply
                util.json_write(json_filepath, data)

        # REMEDIES
        if len(remedies) == 0:
            prompt = f'''
                Give me a numbered list of the {number} {keyword}.
                Give me only the names, not the descriptions.
            '''
            prompt = '\n'.join([line.strip() for line in prompt.split('\n') if line.strip() != ''])
            reply = gen_reply(prompt).strip()

            lines = reply.split('\n')
            herbs = []
            for line in lines:
                line = line.strip().lower()
                if not line[0].isdigit(): continue
                if preparation not in line: continue
                if '. ' not in line: continue

                line = line.split('. ')[1]
                line = line.replace(preparation, '')
                line = line.replace(' leaf', '')
                line = line.replace(' root', '')
                line = line.replace(' seed', '')
                line = line.replace(' flower', '')
                line = line.replace(' bark', '')
                line = line.replace(' extract', '')
                line = line.replace(' oil', '')
                line = line.replace(' milk', '')
                line = line.replace(' berry', '')
                line = line.replace(' leaves', '')
                line = line.replace(' herbal', '')
                line = line.strip()
                herbs.append(line)

            data['remedies'] = []
            for herb in herbs:
                data['remedies'].append(
                    {
                        'herb': f'{herb}',
                        'preparation': f'{preparation}',
                        'intro': '',
                        'study': '',
                        'recipe': [],
                    }
                )

            util.json_write(json_filepath, data)

        # REMEDIES INTRO
        json_filepath = f'database/articles/{url}.json'
        data = util.json_read(json_filepath)

        for i, remedy in enumerate(remedies):
            herb = remedy['herb'].strip().lower()
            intro = remedy['intro'].strip()

            scientific_name = ''
            try: scientific_name = get_scientific_name(herb).capitalize()
            except: print(f'MISSING SCIENTIFIC NAME >> {herb}')

            if intro != '': continue

            prompt = f'''
                Explain why [0] [1] helps with [2]. 
                Answer in a 5-sentence paragraph without using lists. 
                Don't include studies.
                Don't include preparations.
            '''

            scientific_name_formatted = ''
            if scientific_name.strip() != '':
                scientific_name_formatted = f'({scientific_name})'
            prompt = prompt.replace('[0]', f'{herb} {scientific_name_formatted}')
            prompt = prompt.replace('[1]', preparation)
            prompt = prompt.replace('[2]', condition)
            reply = gen_reply(prompt)

            if ':' in reply: continue

            reply = reply.replace('\n', '')
            reply = re.sub("\s\s+" , " ", reply)

            data['remedies'][i]['intro'] = reply.strip()
            
            util.json_write(json_filepath, data)


def gen_output():
    for row in articles_rows:
        keyword = row[0].strip()
        condition = row[1].strip().lower()
        folder = row[2].strip()
        preparation = row[3].strip().lower()
        
        condition_dash = condition.replace(' ', '-')
        
        article_url = f'{folder}/{condition_dash}'
        filepath_out = f'output/{article_url}.md'
        util.file_write(filepath_out, '')

        json_filepath = f'database/articles/{folder}/{condition_dash}.json'
        data = util.json_read(json_filepath)

        remedy_num = data['remedy_num']
        title = data['title'].strip().lower()
        preparation = data['preparation'].strip().lower()
        intro_1 = data['intro_1'].strip()
        intro_2 = data['intro_2'].strip()
        remedies = data['remedies']
        # supplementary_list = data['supplementary']

        title_full = f'{remedy_num} {title}'.title()

        # META
        meta = f'''
            ---
            title: {title_full}
            ---
        '''
        for line in meta.split('\n'):
            line = line.strip()
            if line == '': continue
            util.file_append(filepath_out, f'{line}\n')
        util.file_append(filepath_out, f'\n\n')

        # TITLE
        util.file_append(filepath_out, f'# {title_full}\n\n')

        # # INTRO
        util.file_append(filepath_out, f'![Herbal Tea For {condition.title()}](/images/herbal-tea-for-{condition_dash}.jpg)\n\n')
        
        util.file_append(filepath_out, util.text_format_131(intro_1))
        util.file_append(filepath_out, util.text_format_131(intro_2))

        util.file_append(filepath_out, f'In this article, you\'ll learn which are the best herbal teas for {condition}, why they works, and how to make them.\n\n')

        # MAIN SECTIONS
        i = 1
        for remedy in remedies:
            if i > remedy_num: break

            herb = remedy['herb'].strip().lower()
            intro = remedy['intro'].strip()
            # study = remedy['study'].strip()
            # recipe = remedy['recipe']

            # if study == '': continue

            remedy = f"{herb} {preparation}".strip().lower()
            remedy_formatted = remedy.lower().replace(' ', '-')
            scientific_name = get_scientific_name(herb, delimiter='\\').strip().capitalize()

            # REMEDY TITLE
            remedy_h2 = f'## {i}. {herb} {preparation} ({scientific_name})'
            remedy_h2 = remedy_h2.replace(f'{preparation} {preparation}', f'{preparation}')
            util.file_append(filepath_out, f'{remedy_h2.title()}\n\n')

            # REMEDY INTRO
            util.file_append(filepath_out, util.text_format_131(intro))

            # REMEDY IMAGE
            util.file_append(filepath_out, f'The following image shows a cup of {remedy} for {condition}.\n\n')
            util.file_append(filepath_out, f'![{remedy.title()} For {condition.title()}](/images/{remedy_formatted}-for-{condition_dash}.jpg)\n\n')

        #     # REMEDY STUDY
        #     study_lines = study.split('. ')
        #     study_line_0 = study_lines[0]
        #     study_line_0_chunk_0 = study_line_0.split(',')[0].split('the')[0].strip()
        #     study_line_0_chunk_1 = 'the'.join(study_line_0.split(',')[0].split('the')[1:]).strip()
        #     study_line_0_chunk_2 = ','.join(study_line_0.split(',')[1:]).strip()
        #     study_line_0 = f'{study_line_0_chunk_0} the <strong><em>{study_line_0_chunk_1}</em></strong>, {study_line_0_chunk_2}'
        #     study_line_1 = '. '.join(study_lines[1:-1])
        #     study_line_2 = study_lines[-1]
        #     util.file_append(filepath_out, f'<div class="study-3">\n\n')
        #     util.file_append(filepath_out, f'<p>{study_line_0}.</p>\n\n')
        #     util.file_append(filepath_out, f'<p>{study_line_1}.</p>\n\n')
        #     util.file_append(filepath_out, f'<p>{study_line_2}</p>\n\n')
        #     util.file_append(filepath_out, f'</div>\n\n')

        #     # REMEDY RECIPE
        #     util.file_append(filepath_out, f'Below you can find a quick step-by-step recipe to make {remedy} for {PROBLEM}.\n\n')
        #     for k, item in enumerate(recipe):
        #         util.file_append(filepath_out, f'{k+1}. {item}\n')
        #     util.file_append(filepath_out, f'\n')

            i += 1


        # i = 1
        # for supplementary in supplementary_list:
        #     title = supplementary['title'].strip()
        #     content = supplementary['content'].strip()

        #     # SUPPLEMENTARY TITLE
        #     util.file_append(filepath_out, f'## {title.title()}\n\n')

        #     # SUPPLEMENTARY content
        #     lines = content.split('. ')
        #     line_0 = lines[0]
        #     line_1 = '. '.join(lines[1:-1])
        #     line_2 = lines[-1]
        #     util.file_append(filepath_out, f'{line_0}.\n\n')
        #     util.file_append(filepath_out, f'{line_1}.\n\n')
        #     util.file_append(filepath_out, f'{line_2}\n\n')









articles_rows = util.csv_get_rows(ARTICLES_FILEPATH)[1:]

# init()
# ai_gen_remedies()
# ai_gen_remedies_intro()




def gen_output_2():
    DB_ART_FOLDER = 'database/articles'
    DB_ART_TEA_FOLDER = 'herbalism/tea'
    articles_filepath = [
        f'{DB_ART_FOLDER}/{DB_ART_TEA_FOLDER}/{filename}' 
        for filename in os.listdir(f'{DB_ART_FOLDER}/{DB_ART_TEA_FOLDER}')
    ]
    
    for article_filepath in articles_filepath:
        article_filepath_in = article_filepath
        article_filepath_out = article_filepath.replace(DB_ART_FOLDER, 'output').replace('.json', '.md')

        data = util.json_read(article_filepath_in)

        remedy_num = data['remedy_num']
        keyword = data['keyword'].strip().lower()
        condition = data['condition'].strip().lower()
        preparation = data['preparation'].strip().lower()
        intro_1 = data['intro_1'].strip()
        intro_2 = data['intro_2'].strip()
        remedies = data['remedies']

        title = f'{remedy_num} {keyword}'.title()
        condition_dash = condition.replace(' ', '-')

        # CLEAR ARTICLE
        util.file_write(article_filepath_out, '')

        # META
        meta = f'''
            ---
            title: {title}
            ---
        '''
        for line in meta.split('\n'):
            line = line.strip()
            if line == '': continue
            util.file_append(article_filepath_out, f'{line}\n')
        util.file_append(article_filepath_out, f'\n\n')

        # TITLE
        util.file_append(article_filepath_out, f'# {title}\n\n')

        # INTRO
        util.file_append(article_filepath_out, f'![Herbal Tea For {condition.title()}](/images/herbal-tea-for-{condition_dash}.jpg)\n\n')
        util.file_append(article_filepath_out, util.text_format_131(intro_1))
        util.file_append(article_filepath_out, util.text_format_131(intro_2))
        util.file_append(article_filepath_out, f'In this article, you\'ll learn which are the best herbal teas for {condition}, why they works, and how to make them.\n\n')

        # MAIN SECTIONS
        i = 1
        for remedy in remedies:
            if i > remedy_num: break

            herb = remedy['herb'].strip().lower()
            intro = remedy['intro'].strip()
            # study = remedy['study'].strip()
            # recipe = remedy['recipe']

            # if study == '': continue

            remedy = f"{herb} {preparation}".strip().lower()
            remedy_formatted = remedy.lower().replace(' ', '-')
            try: scientific_name = get_scientific_name(herb, delimiter='\\').strip().capitalize()
            except: scientific_name = ''

            # REMEDY TITLE
            scientific_name_formatted = ''
            if scientific_name != '':
                scientific_name_formatted = f'({scientific_name})'
            remedy_h2 = f'## {i}. {herb} {preparation} {scientific_name_formatted}'
            remedy_h2 = remedy_h2.replace(f'{preparation} {preparation}', f'{preparation}')
            util.file_append(article_filepath_out, f'{remedy_h2.title()}\n\n')

            # REMEDY INTRO
            util.file_append(article_filepath_out, util.text_format_131(intro))

            # REMEDY IMAGE
            util.file_append(article_filepath_out, f'The following image shows a cup of {remedy} for {condition}.\n\n')
            util.file_append(article_filepath_out, f'![{remedy.title()} For {condition.title()}](/images/{remedy_formatted}-for-{condition_dash}.jpg)\n\n')

            i += 1




# ai_gen_json()
# ai_gen_number()
gen_output_2()

# scientific_names_missing()