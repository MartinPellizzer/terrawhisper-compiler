from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import os
import re
import sys
import json
import time
import winsound

from ctransformers import AutoModelForCausalLM

import utils

duration = 1000
freq = 440

# REMEDIES_FILEPATH = f'database/remedies/remedies.csv'



# # 1. Find problem >> [insomnia]
# # 2. Add to >> static_articles.csv
# # 3. FIND and ADD remedies to >> database/remedies/remedies.csv
# # 4. gen_ai_manual.py init, strart
# # 5. generate recipes with chatgpt
# # 6. gen_ai_manual.py output-2

# prompt_2 = f'''
#     Explain how to make [0] for [1].
#     Answer in 3-5 list items and don't add extra info.
#     Make each list item 10 words or less.
#     Include dosages in list items.
#     Start each list item with an action verb.
#     Don't include optional items.
#     Don't include notes.
# '''

models = [
    'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.1.Q8_0.gguf',
    'C:\\Users\\admin\\Desktop\\models\\mixtral-8x7b-instruct-v0.1.Q5_K_M.gguf',
]


def csv_get_rows(filepath, delimiter='\\'):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, line in enumerate(reader):
            rows.append(line)
    return rows


def file_read(filepath):
    with open(filepath, 'a', encoding='utf-8') as f: pass
    with open(filepath, 'r', encoding='utf-8') as f: 
        text = f.read()
    return text


def file_append(filepath, text):
    with open(filepath, 'a', encoding='utf-8') as f: 
        f.write(text)


def file_write(filepath, text):
    with open(filepath, 'w', encoding='utf-8') as f: 
        f.write(text)


def get_scientific_name(common_name, delimiter='\\'):
    rows = csv_get_rows('plants.csv', delimiter=delimiter)
    rows = [row for row in rows if common_name.lower().strip() in row[1].lower().strip()]
    scientific_name = rows[0][0].replace('-', ' ')
    return scientific_name


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


# problem = 'high blood pressure'
# # problems_sub = ['period (pms) bloating', 'menopause bloating']
# # problems_rel = ['digestion', 'gas']

# problem = problem.lower().strip()
# problem_formatted = problem.replace(' ', '-').lower().strip()

# article_url = f'herbalism/tea/{problem_formatted}'

# remedy_llst = [row for row in csv_get_rows(REMEDIES_FILEPATH) if row[0].lower().strip() == problem]


# # CREATE FOLDERS
# folder_curr = 'database-new/articles/'
# for chunk in article_url.split('/'):
#     folder_curr += chunk + '/'
#     try: os.makedirs(folder_curr)
#     except: pass

# rows = csv_get_rows(f'static-articles.csv')
# article_row = [row for row in rows if row[1].lower().strip() == article_url][0]
# article_url = article_row[1]
# article_num = article_row[2]
# article_title = article_row[3]
# print(article_row)

# title_num = int([f'{row[2]}' for row in rows if row[1].lower().strip() == article_url][0])

# rows = csv_get_rows(f'database/remedies/remedies.csv')
# remedies = [[row[2], row[1]] for row in rows if problem == row[0].lower().strip()]

llm = AutoModelForCausalLM.from_pretrained(
    models[0],
    model_type="mistral", 
    context_length=2048, 
    max_new_tokens=1024,
    )
   




# if sys.argv[1] == 'init':
#     for i, remedy in enumerate(remedies):
#         remedy_formatted = remedy.replace(' ', '-').lower().strip()
#         _filepath = f'database-new/articles/herbalism/tea/{problem}/{remedy_formatted}-recipe.md'
#         with open(_filepath, 'a', encoding='utf-8') as f: pass
#         _filepath = f'database-new/articles/herbalism/tea/{problem}/{remedy_formatted}-study-scraped.md'
#         with open(_filepath, 'a', encoding='utf-8') as f: pass
#         _filepath = f'database-new/articles/herbalism/tea/{problem}/{remedy_formatted}-study.md'
#         with open(_filepath, 'a', encoding='utf-8') as f: pass



# def generate_intro():
#     try: os.makedirs(f'database-new/articles/herbalism/tea/{problem_formatted}/intro')
#     except: pass
#     _filepath = f'database-new/articles/herbalism/tea/{problem_formatted}/intro/_intro.md'
#     content = file_read(_filepath)
#     if content.strip() == '': 
#         curr_prompt = f'''
#             Write a 5-line paragraph about [1]. 
#             Include a definition of the problem.
#             Include how many people have this problem in the world every year.
#             Include how this problem can negatively affect their quality of life.
#             Include which are the main causes that make people have this problem.
#             Include what effects this problem has on other aspects of health.
#             Include numbers, percentages, and statistics, without mentioning the sources.

#         '''

#         curr_prompt = curr_prompt.replace('[1]', problem)
#         reply = gen_reply(curr_prompt)

#         file_write(_filepath, reply)

        
#     _filepath = f'database-new/articles/herbalism/tea/{problem_formatted}/intro/_intro-2.md'
#     content = file_read(_filepath)
#     if content.strip() == '': 
#         curr_prompt = f'''
#             Write a 5-line paragraph about herbal tea for [1]. 
#         '''

#         curr_prompt = curr_prompt.replace('[1]', problem)
#         reply = gen_reply(curr_prompt)

#         file_write(_filepath, reply)

        

# def generate_remedy_intro():
#     llm = AutoModelForCausalLM.from_pretrained(
#         models[0],
#         model_type="mistral", 
#         context_length=1024, 
#         max_new_tokens=1024,
#         )

#     for i, remedy in enumerate(remedies):
#         herb = remedy[0].capitalize()
#         print(herb)
#         preparation = remedy[1].lower()
#         scientific_name = get_scientific_name(herb)

#         remedy_string = ' '.join(remedy)
#         remedy_string = re.sub("\s\s+" , " ", remedy_string)
#         remedy_formatted = remedy_string.replace(' ', '-').lower().strip()
#         filepath = f'database-new/articles/herbalism/tea/{problem_formatted}/{remedy_formatted}.md'

#         content = file_read(filepath)
#         if content.strip() != '': continue

#         curr_prompt = f'''
#             Explain why [0] helps with [1]. Answer in a 5-line paragraph without using lists.
#         '''

#         curr_prompt = curr_prompt.replace('[0]', f'{herb} ({scientific_name}) {preparation}')
#         curr_prompt = curr_prompt.replace('[1]', problem)
#         reply = gen_reply(curr_prompt)

#         file_append(filepath, reply)


# def generate_remedy_recipe():
#     llm = AutoModelForCausalLM.from_pretrained(
#         models[0],
#         model_type="mistral", 
#         context_length=256, 
#         max_new_tokens=256,
#         )

#     for i, remedy in enumerate(remedies):
#         herb = remedy[0].capitalize()
#         print(herb)
#         preparation = remedy[1].lower()
#         scientific_name = get_scientific_name(herb)

#         remedy_string = ' '.join(remedy)
#         remedy_string = re.sub("\s\s+" , " ", remedy_string)
#         remedy_formatted = remedy_string.replace(' ', '-').lower().strip()
        
#         try: os.makedirs(f'database-new/articles/herbalism/tea/{problem_formatted}/remedy-recipe')
#         except: pass
#         filepath = f'database-new/articles/herbalism/tea/{problem_formatted}/remedy-recipe/{remedy_formatted}-recipe.md'

#         # print(_filepath)
#         # if os.path.exists(_filepath): os.remove(_filepath)

#         # SKIP IF FILE ALREADY HAS CONTENT
#         file_append(filepath, '')
#         content = file_read(filepath)
#         if content.strip() != '': continue

#         curr_prompt = f'''
#             Write a 5-step recipe to make [0] for [1].
#             Answer with short sentences.
#             Include dosages for ingredients and time for steeping.
#         '''
#         curr_prompt = curr_prompt.replace('[0]', f'{herb} ({scientific_name}) {preparation}')
#         curr_prompt = curr_prompt.replace('[1]', problem)
#         reply = gen_reply(curr_prompt)

#         file_append(filepath, reply)


# def generate_remedy_study_scrape(): 
#     for remedy in remedies:
#         # remedy = remedies[0]
#         herb = remedy[0].lower().strip()
#         preparation = remedy[1]
#         scientific_name = get_scientific_name(herb)
    
#         remedy_string = ' '.join(remedy)
#         remedy_string = re.sub("\s\s+" , " ", remedy_string)
#         remedy_formatted = remedy_string.replace(' ', '-').lower()

#         try: os.makedirs(f'database-new/articles/herbalism/tea/{problem_formatted}/remedy-study')
#         except: pass
#         filepath_out = f'database-new/articles/{article_url}/remedy-study/{remedy_formatted}-study-scraped.md'
        
#         if file_read(filepath_out).strip() != '': continue

#         print()
#         print()
#         print()
#         print(filepath_out)

#         print('Driver Opened...')
#         driver = webdriver.Firefox()
#         driver.get("https://scholar.google.com/")
#         time.sleep(3)

#         query = f'{scientific_name} {problem}'.lower().strip()

#         e = driver.find_element(By.XPATH, '//input[@name="q"]')
#         e.send_keys(query)
#         time.sleep(3)
#         e.send_keys(Keys.RETURN)
#         time.sleep(10)

#         main_element = driver.find_element(By.XPATH, '//div[@role="main"]')
#         articles_elements = main_element.find_elements(By.XPATH, './/h3/..')

#         articles_urls = []
#         for article_element in articles_elements:
#             a_elements = article_element.find_elements(By.XPATH, './/a')
#             try: study_url = article_element.find_element(By.XPATH, './/h3/a').get_attribute('href')
#             except: continue
#             articles_urls.append(study_url)

#         for study_url in articles_urls:
#             print(study_url)
#             try: driver.get(study_url)
#             except: continue
#             time.sleep(10)

#             abstract_headers = driver.find_elements(By.XPATH, "//*[contains(text(), 'Abstract')]")
#             abstract_text = ''
#             for abstract_header in abstract_headers:
#                 try:
#                     abstract_elements = abstract_header.find_elements(By.XPATH, "following-sibling::*")
#                     for abstract_element in abstract_elements:
#                         try: abstract_text = abstract_element.text + '\n\n'
#                         except: pass
#                 except: pass
            
#             print(abstract_text)
#             if abstract_text != '': 
#                 file_append(filepath_out, study_url)
#                 file_append(filepath_out, '\n\n')
#                 file_append(filepath_out, abstract_text)
#                 time.sleep(10)
#                 print('Driver Closed!')
#                 break

#         driver.quit()
#         driver = None
#         time.sleep(10)


# def generate_remedy_study_summary(force=False): 
#     llm = AutoModelForCausalLM.from_pretrained(
#         models[0],
#         model_type="mistral", 
#         context_length=2048, 
#         max_new_tokens=256,
#         )

#     for i, remedy in enumerate(remedies):
#         remedy_string = ' '.join(remedy).lower().strip()
#         remedy_string = re.sub("\s\s+" , " ", remedy_string)
#         remedy_formatted = remedy_string.replace(' ', '-').lower().strip()
#         filepath_in = f'database-new/articles/herbalism/tea/{problem_formatted}/remedy-study/{remedy_formatted}-study-scraped.md'
#         filepath_out = f'database-new/articles/herbalism/tea/{problem_formatted}/remedy-study/{remedy_formatted}-study.md'
#         print(filepath_out)

#         abstract = file_read(filepath_in)
#         summary = file_read(filepath_out)
        
#         if abstract.strip() == '': continue
#         if not force:
#             if summary.strip() != '': continue
        
#         lines = abstract.split('\n')
#         abstract_formatted = []
#         for line in lines[1:]:
#             line = line.strip()
#             if line == '': continue
#             if line.startswith('source: '): continue
#             words = line.split(' ')
#             # if len(words) <= 5: continue
#             abstract_formatted.append(line)
#         abstract_formatted = ' '.join(abstract_formatted)

#         herb = remedy_string.replace(' Tea', '')
#         herb = remedy_string.replace(' tea', '')
#         curr_prompt = f'''
#             Summarize the following study writing about [0] for [1] in a 5-line paragraph:

#             {abstract_formatted}
#         '''
        
#         curr_prompt = curr_prompt.replace('[0]', herb)
#         curr_prompt = curr_prompt.replace('[1]', problem)
#         reply = gen_reply(curr_prompt)
        
#         if reply.strip().endswith('.'):
#             file_write(filepath_out, reply)


# def generate_init_2():
#     folderpath_in = f'database-new/articles/{article_url}'
#     file_append(f'{folderpath_in}/intro.md', '')
#     for i, remedy_lst in enumerate(remedy_llst):
#         herb = remedy_lst[2].lower().strip()
#         herb_formatted = herb.replace(' ', '-')
#         remedy_foldername = f'{i}-{herb_formatted}' 
#         remedy_folderpath = f'{folderpath_in}/{remedy_foldername}'
#         try: os.makedirs(remedy_folderpath)
#         except: pass
#         file_append(f'{remedy_folderpath}/intro.md', '')
#         file_append(f'{remedy_folderpath}/study.md', '')
#         file_append(f'{remedy_folderpath}/recipe.md', '')


# def generate_output_2():
#     filepath_out = f'static/{article_url}.md'
#     folderpath_in = f'database-new/articles/{article_url}'

#     remedy_folders = [folder for folder in os.listdir(folderpath_in) if folder[0].isdigit()]

#     file_write(filepath_out, '')

#     meta_title = f'{article_num} {article_title}'

#     # META
#     meta = f'''
#         ---
#         title: {meta_title}
#         ---
#     '''
#     for line in meta.split('\n'):
#         line = line.strip()
#         if line == '': continue
#         file_append(filepath_out, f'{line}\n')
#     file_append(filepath_out, '\n\n')

#     # TITLE
#     file_append(filepath_out, f'# {article_num} {article_title}\n\n')

#     # INTRO
#     try: intro = file_read(f'{folderpath_in}/intro.md')
#     except: intro = ''
#     file_append(filepath_out, f'![Herbal Tea For {problem.title()}](/images/herbal-tea-for-{problem_formatted}.jpg)\n\n')
#     file_append(filepath_out, f'{intro}\n\n')
#     file_append(filepath_out, f'In this article, you\'ll learn which are the best herbal teas for {problem}. Also, for each herbal tea, you\'ll be provided with a scientific study that proves the effectiveness of the herb for {problem} and a step-by-step recipe to easily make the herbal tea.\n\n')

#     for i, remedy_lst in enumerate(remedy_llst):
#         remedy = ' '.join([remedy_lst[2].strip(), remedy_lst[1].strip()])
#         remedy_formatted = remedy.lower().replace(' ', '-')
#         herb = remedy_lst[2].strip().lower()
#         scientific_name = get_scientific_name(herb, delimiter='\\')
#         remedy_h2 = f'## {i+1}. {remedy_lst[2].strip()} ({scientific_name}) {remedy_lst[1].strip()}'.title()
        
#         # GET REMEDY FOLDER
#         remedy_folder_curr = ''
#         for remedy_folder in remedy_folders:
#             if herb.replace(' ', '-') in remedy_folder:
#                 remedy_folder_curr = remedy_folder
#                 break

#         # IF REMEDY FOLDER EXISTS
#         intro = ''
#         study = ''
#         recipe = ''
#         if remedy_folder_curr != '':
#             remedy_folderpath = f'{folderpath_in}/{remedy_folder_curr}'
#             try: intro = file_read(f'{remedy_folderpath}/intro.md')
#             except: pass
#             try: study = file_read(f'{remedy_folderpath}/study.md')
#             except: pass
#             try: recipe = file_read(f'{remedy_folderpath}/recipe.md')
#             except: pass

#             print(remedy_folderpath)

#         recipe = recipe.strip()
#         recipe_formatted = ''
#         if recipe != '':
#             lines = recipe.split('\n')
#             for i, line in enumerate(lines):
#                 recipe_formatted += f'{i}. {line}\n'

#         intro = intro.replace('. ', '. \n\n')
        
#         study = f'<div class="study-3"><p>{study}</p></div>'

#         file_append(filepath_out, f'{remedy_h2}\n\n')
#         file_append(filepath_out, f'{intro}\n\n')
#         file_append(filepath_out, f'The following image shows a cup of {remedy.title()} for {problem}.\n\n')
#         file_append(filepath_out, f'![{remedy.title()} For {problem.title()}](/images/{remedy_formatted}-for-{problem_formatted}.jpg)\n\n')
#         file_append(filepath_out, f'{study}\n\n')
#         file_append(filepath_out, f'Below you can find a quick and easy step-by-step recipe to make {remedy.title()} for {problem}.\n\n')
#         file_append(filepath_out, f'{recipe_formatted}\n\n')

#     supplementary = file_read(f'{folderpath_in}/supplementary.md')
#     file_append(filepath_out, f'{supplementary}\n\n')


# def generate_output():
#     filepath_out = f'static/{article_url}.md'
#     if os.path.exists(filepath_out): os.remove(filepath_out)

#     _filepath = f'database/remedies/remedies.csv'
#     _rows = csv_get_rows(_filepath)
#     _remedies = [[_row[2], _row[1]] for _row in _rows if _row[0].lower().strip() == problem]
#     problem_formatted = problem.replace(' ', '-').lower().strip()

#     # INTRO
#     _filepath = f'static-articles.csv'
#     _rows = csv_get_rows(_filepath)
#     _title = [f'{_row[2]} {_row[3]}' for _row in _rows if _row[1].lower().strip() == article_url][0]
#     _meta = f'''
#         ---
#         title: {_title}
#         ---
#     '''
#     _filepath = f'database-new/articles/herbalism/tea/{problem_formatted}/intro/_intro.md'
#     _intro = file_read(_filepath)
#     _filepath = f'database-new/articles/herbalism/tea/{problem_formatted}/intro/_intro-2.md'
#     _intro_2 = file_read(_filepath)

#     _intro_end = f'In this article, you\'ll learn which are the best herbal teas for {problem}. You\'ll also find ascientific studies that prove the effectiveness of the herbs and easy to make recipes to make the medicinal herbal teas.'
    
#     with open(filepath_out, 'a', encoding='utf-8') as f: 
#         for _line in _meta.strip().split('\n'):
#             f.write(f'{_line.strip()}\n')
#         f.write(f'\n\n')
#         f.write(f'# {_title}\n\n')
#         f.write(f'![Herbal Tea For {problem.title()}](/images/herbal-tea-for-{problem_formatted}.jpg)\n\n')
#         f.write(f'{_intro}\n\n')
#         f.write(f'{_intro_2}\n\n')
#         f.write(f'{_intro_end}\n\n')

#     for i, _remedy in enumerate(remedies):
#         _remedy_text = ' '.join(_remedy)
#         _remedy_plant = _remedy[0]
#         _rows_plants = csv_get_rows(f'plants.csv', delimiter='\\')
#         _scientific_name = [f'{_row[0]}' for _row in _rows_plants if _row[1].lower().strip() == _remedy[0].lower().strip()]
#         try:
#             _scientific_name_formatted = _scientific_name[0].replace('-', ' ').capitalize()
#         except:
#             _scientific_name_formatted = ''
#             print(f'Missing Scientific Name >> {_remedy}')

#         _remedy_text = re.sub("\s\s+" , " ", _remedy_text)
#         _remedy_text_formatted = _remedy_text.replace(' ', '-').lower().strip()

#         _filepath_in = f'database-new/articles/herbalism/tea/{problem_formatted}/remedy-intro/{_remedy_text_formatted}.md'
#         _content = file_read(_filepath_in)

#         # CLEAN INTRO TEXT
#         _sentences = _content.split('. ')
#         _sentences_filtered = []
#         for _sentence in _sentences:
#             if _sentence.startswith('Overall,'): continue
#             else: _sentences_filtered.append(_sentence)
#         _sentences_filtered = '. '.join(_sentences_filtered) + '.'
#         # _sentences_filtered = _sentences_filtered.replace('can', '')
#         # _sentences_filtered = _sentences_filtered.replace('may', '')
#         # _sentences_filtered = _sentences_filtered.replace('might', '')
#         _sentences_filtered = _sentences_filtered.replace('..', '.')
#         _sentences_filtered = re.sub("\s\s+" , " ", _sentences_filtered)
#         _sentences_filtered = _sentences_filtered.strip()

#         # RECIPE
#         _filepath_in = f'database-new/articles/herbalism/tea/{problem_formatted}/remedy-recipe/{_remedy_text_formatted}-recipe.md'
#         _content = file_read(_filepath_in)

#         _lines = _content.split('\n')
#         _lines_filtered = []
#         _i = 1
#         print(_filepath_in)
#         for _line in _lines:
#             _valid_line = False
#             _line = _line.strip()
#             if _line == '': continue
#             if re.search('\d: ', _line):
#                 _line = _line.split(': ')[1]
#                 _valid_line = True
#             elif re.search('\d\. ', _line):
#                 _line = _line.split('. ')[1]
#                 _valid_line = True
#             elif re.search('\d\) ', _line):
#                 _line = _line.split(') ')[1]
#                 _valid_line = True
            
#             if _valid_line:
#                 if ': ' in _line: _line = _line.split(': ')[1].capitalize()
#                 # _line = f'{_i}. {_line}'
#                 _line = f'{_line}'
#                 _line = _line.replace('!', '.')
#                 _lines_filtered.append(_line)
#                 _i += 1
#                 # print(_line)
#             else:
#                 print('false')
        
#         _lines_formatted = ''
#         for _i, _line in enumerate(_lines_filtered):
#             _lines_formatted += f'{_i}. {_line}\n'

#         # STUDY
#         filepath = f'database-new/articles/herbalism/tea/{problem_formatted}/remedy-study/{_remedy_text_formatted}-study.md'
#         _study = file_read(filepath).strip()
#         # _study_lines = _study.split('. ')
#         # _study_lines = _study.split('\n')
#         _study_lines = _study.replace('\n', ' ')
#         _study_lines = re.sub("\s\s+" , " ", _study_lines)

#         study_scraped = file_read(f'database-new/articles/herbalism/tea/{problem_formatted}/remedy-study/{_remedy_text_formatted}-study-scraped.md').strip()
#         lines = study_scraped.split('\n')
#         if lines[0].startswith('source: '): source = lines[0].split(':')[1].strip()
#         else: source = ''
#         if 'journal' not in source.lower().strip(): source += f' Publication'
#         study_intro = f'Here is a scientific study documenting the effectiveness of {_remedy_plant} for {problem}'
#         if source != '': study_intro += f'  by the <em>{source}</em>.'
#         else: study_intro += f'.'

#         # INTRO LINES?
#         _intro_lines = _sentences_filtered.split('. ')

#         # GENERATE OUTPUT
#         _remedy_formatted = _remedy_text.replace(' ', '-').lower().strip()
#         problem_formatted = problem.replace(' ', '-').lower().strip()
#         with open(filepath_out, 'a', encoding='utf-8') as f:
#             f.write(f'## {i+1}. {_remedy[0].strip().title()} ({_scientific_name_formatted.strip()}) {_remedy[1].strip().title()}\n\n')
#             for _line in _intro_lines:
#                 f.write(f'{_line}.\n\n'.replace('..', '.'))
#             f.write(f'The following image shows a cup of {_remedy_text.title()} made for {problem}.\n\n')
#             f.write(f'![{_remedy_text.title()} For {problem.title()}](/images/{_remedy_formatted}-for-{problem_formatted}.jpg)\n\n')
#             f.write(f'<div class="study">\n\n')
#             f.write(f'''
#             <svg class="icon-study" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
#             <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
#             </svg>
#             \n\n''')
#             f.write(f'<p>{study_intro}</p>\n\n')
#             f.write(f'<p>{_study_lines}</p>')
#             # for _study in _study_lines:
#             #     _study = f'{_study}.'
#             #     _study = _study.replace('..', '.')
#             #     f.write(f'<p>{_study}</p>\n\n')
#             f.write(f'</div>\n\n')

#             f.write(f'Below you can find an easy and quick step-by-step recipe to make {_remedy_text.title()} for {problem}.\n\n')
#             f.write(f'{_lines_formatted}\n\n')
    
#     folderpath = f'database-new/articles/herbalism/tea/{problem_formatted}/supplemetary-questions'
#     try: os.makedirs(folderpath)
#     except: pass
#     for filename in os.listdir(folderpath):
#         filepath = f'{folderpath}/{filename}'
#         content = file_read(filepath)
#         content = content.strip() + '\n\n'
#         file_append(filepath_out, content)


# def generate_supplementary_questions():
#     filepath_out = f'database-new/articles/herbalism/tea/{problem_formatted}/supplemetary-questions'
#     try: os.makedirs(filepath_out)
#     except: pass

#     filepath = f'database-new/articles/herbalism/tea/{problem_formatted}/_supplemetary-questions.md'
#     content = file_read(filepath)
#     if content.strip() == '': 
#         print('no question for supplementary content')
#         return

#     questions = content.split('\n')
#     for i, question in enumerate(questions):
#         print(f'{i}/{len(questions)}')
#         question = question.strip().capitalize()

#         curr_prompt = f'''
#             {question} Answer with a short paragraph. Start the answer with: The best herbal 
#         '''
#         reply = gen_reply(curr_prompt)

#         reply = f'## {question}\n\n{reply}'
#         file_write(f'{filepath_out}/{i}.md', reply)


# def generate_prompt():
#     for remedy_lst in remedy_llst:
#         common_name = remedy_lst[2].strip().lower()
#         try: scientific_name = get_scientific_name(common_name)
#         except: scientific_name = ''
#         # print(common_name, f'({scientific_name})')

#         print(f'''
#         >> {common_name}

#             Write a 60-word paragraph about {common_name} ({scientific_name}) Tea for {problem}. 
#             Explain what constituents this herb has that help with this problem and how it does it. 
#             Include only facts, not opinions. 
#             Don't use words like "can", "may", "might", etc... 
#             Use a straightforward tone of voice.
#             Start with the following words: {common_name} ({scientific_name}) Tea contains
        
#         -------------------------------------------------------
#         ''')

#         print(f'''
#         >> {common_name}

#             Give me 2 lists about the following remedy: {common_name} ({scientific_name}) Tea for {problem}.

#             - in list 1, write the most essential ingredients (with dosages) for this remedy. start each item on this list with a dosage expressed in a numerical value. don't give me optional ingredients like honey. give me only the main herb and water in the list of ingredients. make the ingredient list unnumbered (use the character "-").
#             - in list 2, write the instructions to make this remedy. make this list numbered. don't give me optional instructions. make this list 5 items long.

#             a few rules:
#             - each element in the lists must be short and straight to the point. 
#             - don't give me additional notes.
        
#         -------------------------------------------------------
#         ''')

#         print(f'''
#             Write a 5-line paragraph about {problem}. 
#             Include a definition of the problem.
#             Include how many people have this problem in the world every year by using numbers and statistics.
#             Include how this problem can negatively affect their quality of life.
#             Include which are the main causes that make people have this problem.
#             Include what effects this problem has on other aspects of health.
#             Include numbers, percentages, and statistics, without mentioning the sources.

#         -------------------------------------------------------
#         ''')

#         print(f'''
#             Write a 5-line paragraph about herbal tea for {problem}. 

#         -------------------------------------------------------
#         ''')

#         lst = [item[2].strip() for item in remedy_llst]
#         remedies_prompt = ', '.join(lst)
#         print(f'''
#             Tell me in a 60-word paragraph what are the worst herbal teas for {problem} and explain why?
            
#             Exclude the following herbal teas from your answer: {remedies_prompt}.

#             Start the answer with these words: The worst herbal teas for {problem} are 

#         -------------------------------------------------------
#         ''')

#         print(f'''
#             Tell me in a 60-word paragraph what is the best time to drink herbal tea for {problem} and explain why?

#             Start the answer with these words: The best time to drink herbal tea for {problem} is 
#         -------------------------------------------------------
#         ''')

#         print(f'''
#             Tell me in a 60-word paragraph What are the possible side effects and precautions associated with using herbal teas for {problem} and explain why?
#         -------------------------------------------------------
#         ''')

#         print(f'''
#             Tell me in a 60-word paragraph What is the best herbal tea blend for {problem} and explain why?
#             For this mix, choose 3 herbs from the following: {remedies_prompt}.
#         -------------------------------------------------------
#         ''')

#         print(f'''
#             Tell me in a 60-word paragraph How long does it take for herbal teas to alleviate {problem} and explain why it takes that time to alleviate it?
#             Start the answer with these words: Herbal teas take 

#         -------------------------------------------------------
#         ''')



        



# if sys.argv[1] == 'intro':
#     generate_intro()
#     winsound.Beep(freq, duration)

# # if sys.argv[1] == 'remedy-intro':
# #     generate_remedy_intro()
# #     winsound.Beep(freq, duration)

# # if sys.argv[1] == 'remedy-recipe':
# #     generate_remedy_recipe()
# #     winsound.Beep(freq, duration)

# if sys.argv[1] == 'remedy-study-scrape':
#     generate_remedy_study_scrape()
#     winsound.Beep(freq, duration)

# if sys.argv[1] == 'remedy-study-summary':
#     generate_remedy_study_summary()
#     winsound.Beep(freq, duration)
    
# if sys.argv[1] == 'remedy-study-summary-force':
#     generate_remedy_study_summary(force=True)
#     winsound.Beep(freq, duration)

# if sys.argv[1] == 'supplementary-questions':
#     generate_supplementary_questions()

# if sys.argv[1] == 'output':
#     generate_output()

# if sys.argv[1] == 'output-2':
#     generate_output_2()
# if sys.argv[1] == 'init-2':
#     generate_init_2()
    
# if sys.argv[1] == 'prompt':
#     generate_prompt()



# if sys.argv[1] == 'all':
#     generate_intro()
#     generate_remedy_intro()
#     generate_remedy_recipe()
#     generate_remedy_study_scrape()
#     generate_remedy_study_summary()
#     generate_output()
#     winsound.Beep(freq, duration)











import json



REMEDY_NUM = 11
PROBLEM = 'upset stomach'.lower().strip()
PROBLEM_FORMATTED = PROBLEM.replace(' ', '-').lower().strip()

PREPARATION = 'tea'
TITLE = f'herbal {PREPARATION} for {PROBLEM}'
REMEDIES = [
    'Peppermint',
    'Ginger',
    'Chamomile',
    'Fennel',
    'Spearmint',
    'Holy basil',
    'Licorice',
    'Dandelion',
    'Green',
    'Black',
    'Lemon balm',
    'Cinnamon',
    'Echinacea',
    'Raspberry leaf',
    'Lavender',
    'Marshmallow root',
    'Cardamom',
    'Meadowsweet',
    'Slippery elm',
    'Turmeric'
]

PROBLEM_DASH = PROBLEM.lower().strip().replace(' ', '-')
articles_folderpath = 'database-new/articles/herbalism/tea'
article_filepath = f'{articles_folderpath}/{PROBLEM_DASH}.json'
article_url = f'herbalism/tea/{PROBLEM_FORMATTED}'


def scientific_names_check():
    with open(article_filepath, 'r', encoding='utf-8') as f: data = json.load(f)
    remedies = data['remedies']
    herbs = [remedy['herb'] for remedy in remedies]

    for herb in herbs:
        try: 
            scientific_name = get_scientific_name(herb)
            print(herb, f'({scientific_name})')
        except:
            print(herb)


def json_read(filepath):
    with open(filepath, 'r', encoding='utf-8') as f: 
        return json.load(f)


def json_write(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)


def json_append(filepath, data):
    with open(filepath, 'a') as f:
        json.dump(data, f)


def ai_gen_remedy_intro():
    llm = AutoModelForCausalLM.from_pretrained(
        models[0],
        model_type="mistral", 
        context_length=1024, 
        max_new_tokens=1024,
        )

    data = json_read(article_filepath)
    remedies = data['remedies']

    for i, remedy in enumerate(remedies):
        herb = remedy['herb'].strip().lower()
        intro = remedy['intro'].strip()
        study = remedy['study'].strip()
        scientific_name = get_scientific_name(herb).capitalize()

        if intro != '': continue
        if study == '': continue

        prompt = f'''
            Explain why [0] [1] helps with [2]. Answer in a 5-line paragraph without using lists.
        '''

        prompt = prompt.replace('[0]', f'{herb} ({scientific_name})')
        prompt = prompt.replace('[1]', PREPARATION)
        prompt = prompt.replace('[2]', PROBLEM)
        reply = gen_reply(prompt)
        reply = reply.replace('\n', '')
        reply = re.sub("\s\s+" , " ", reply)

        data['remedies'][i]['intro'] = reply.strip()

        with open(article_filepath, 'w') as f:
            json.dump(data, f)


def ai_gen_remedy_recipe():
    llm = AutoModelForCausalLM.from_pretrained(
        models[0],
        model_type="mistral", 
        context_length=1024, 
        max_new_tokens=1024,
        )

    data = json_read(article_filepath)
    remedies = data['remedies']

    for i, remedy in enumerate(remedies):
        herb = remedy['herb'].strip().lower()
        study = remedy['study'].strip()
        recipe = remedy['recipe']
        scientific_name = get_scientific_name(herb).capitalize()

        if len(recipe) != 0: continue
        if study == '': continue

        prompt = f'''
            Write a 5-step recipe to make [0] [1] for [2].
            Answer with short sentences.
            Include dosages for ingredients and time for preparation.
        '''
        prompt = prompt.replace('[0]', f'{herb} ({scientific_name})')
        prompt = prompt.replace('[1]', PREPARATION)
        prompt = prompt.replace('[2]', PROBLEM)
        reply = gen_reply(prompt)

        _lines = reply.split('\n')
        _lines_filtered = []
        _i = 1
        for _line in _lines:
            _valid_line = False
            _line = _line.strip()
            if _line == '': continue
            if re.search('\d: ', _line):
                _line = _line.split(': ')[1]
                _valid_line = True
            elif re.search('\d\. ', _line):
                _line = _line.split('. ')[1]
                _valid_line = True
            elif re.search('\d\) ', _line):
                _line = _line.split(') ')[1]
                _valid_line = True
            
            if _valid_line:
                if ': ' in _line: _line = _line.split(': ')[1].capitalize()
                _line = f'{_line}'
                _line = _line.replace('!', '.')
                _lines_filtered.append(_line)
                _i += 1
            else:
                print('false')

        # _lines_formatted = ''
        # for _i, _line in enumerate(_lines_filtered):
        #     _lines_formatted += f'{_i}. {_line}\n'


        data['remedies'][i]['recipe'] = _lines_filtered

        json_write(article_filepath, data)
        # print(data)
        # quit()


def generate_intro_2():
    llm = AutoModelForCausalLM.from_pretrained(
        models[0],
        model_type="mistral", 
        context_length=1024, 
        max_new_tokens=1024,
        )

    data = json_read(article_filepath)
    intro_1 = data['intro_1']
    if intro_1.strip() == '': 
        prompt = f'''
            Write a 5-line paragraph about [1]. 
            Include a definition of the problem.
            Include how many people have this problem in the world every year.
            Include how this problem can negatively affect their quality of life.
            Include which are the main causes that make people have this problem.
            Include what effects this problem has on other aspects of health.
            Include numbers, percentages, and statistics, without mentioning the sources.

        '''
        prompt = prompt.replace('[1]', problem)
        reply = gen_reply(prompt).strip()
        data['intro_1'] = reply
        with open(article_filepath, 'w') as f:
            json.dump(data, f)


    data = json_read(article_filepath)
    intro_1 = data['intro_2']
    if intro_1.strip() == '': 
        prompt = f'''
            Write a 5-line paragraph about herbal tea for [1]. 
        '''
        prompt = prompt.replace('[1]', problem)
        reply = gen_reply(prompt).strip()
        data['intro_2'] = reply
        with open(article_filepath, 'w') as f:
            json.dump(data, f)


def generate_output_3():
    filepath_out = f'static/{article_url}.md'
    
    file_write(filepath_out, '')

    data = json_read(article_filepath)

    remedy_num = data['remedy_num']
    title = data['title'].strip().lower()
    preparation = data['preparation'].strip().lower()
    intro_1 = data['intro_1'].strip()
    intro_2 = data['intro_2'].strip()
    remedies = data['remedies']
    supplementary_list = data['supplementary']

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
        file_append(filepath_out, f'{line}\n')
    file_append(filepath_out, f'\n\n')

    # TITLE
    file_append(filepath_out, f'# {title_full}\n\n')

    # INTRO
    file_append(filepath_out, f'![Herbal Tea For {PROBLEM.title()}](/images/herbal-tea-for-{PROBLEM_DASH}.jpg)\n\n')
    
    lines = intro_1.split('. ')
    line_0 = lines[0]
    line_1 = '. '.join(lines[1:-1])
    line_2 = lines[-1]
    file_append(filepath_out, f'{line_0}.\n\n')
    file_append(filepath_out, f'{line_1}.\n\n')
    file_append(filepath_out, f'{line_2}\n\n')
    # file_append(filepath_out, f'{intro_1}\n\n')
    
    lines = intro_2.split('. ')
    line_0 = lines[0]
    line_1 = '. '.join(lines[1:-1])
    line_2 = lines[-1]
    file_append(filepath_out, f'{line_0}.\n\n')
    file_append(filepath_out, f'{line_1}.\n\n')
    file_append(filepath_out, f'{line_2}\n\n')

    file_append(filepath_out, f'In this article, you\'ll learn which are the best herbal teas for {PROBLEM}. Also, for each herbal tea, you\'ll be provided with a scientific study that proves the effectiveness of the herb for {PROBLEM} and a step-by-step recipe to easily make the herbal tea.\n\n')

    # MAIN SECTIONS
    i = 1
    for remedy in remedies:
        herb = remedy['herb'].strip().lower()
        intro = remedy['intro'].strip()
        study = remedy['study'].strip()
        recipe = remedy['recipe']

        if study == '': continue

        remedy = f"{herb} {preparation}".strip().lower()
        remedy_formatted = remedy.lower().replace(' ', '-')
        scientific_name = get_scientific_name(herb, delimiter='\\').strip().capitalize()

        # REMEDY TITLE
        remedy_h2 = f'## {i}. {herb} {preparation} ({scientific_name})'
        remedy_h2 = remedy_h2.replace(f'{preparation} {preparation}', f'{preparation}')
        file_append(filepath_out, f'{remedy_h2.title()}\n\n')

        # REMEDY INTRO
        intro_lines = intro.split('. ')
        intro_line_0 = intro_lines[0]
        intro_line_1 = '. '.join(intro_lines[1:-1])
        intro_line_2 = intro_lines[-1]
        file_append(filepath_out, f'{intro_line_0}.\n\n')
        file_append(filepath_out, f'{intro_line_1}.\n\n')
        file_append(filepath_out, f'{intro_line_2}\n\n')

        # REMEDY IMAGE
        file_append(filepath_out, f'The following image shows a cup of {remedy} for {PROBLEM}.\n\n')
        file_append(filepath_out, f'![{remedy.title()} For {PROBLEM.title()}](/images/{remedy_formatted}-for-{PROBLEM_DASH}.jpg)\n\n')

        # REMEDY STUDY
        study_lines = study.split('. ')
        study_line_0 = study_lines[0]
        study_line_0_chunk_0 = study_line_0.split(',')[0].split('the')[0].strip()
        study_line_0_chunk_1 = 'the'.join(study_line_0.split(',')[0].split('the')[1:]).strip()
        study_line_0_chunk_2 = ','.join(study_line_0.split(',')[1:]).strip()
        study_line_0 = f'{study_line_0_chunk_0} the <strong><em>{study_line_0_chunk_1}</em></strong>, {study_line_0_chunk_2}'
        study_line_1 = '. '.join(study_lines[1:-1])
        study_line_2 = study_lines[-1]
        file_append(filepath_out, f'<div class="study-3">\n\n')
        file_append(filepath_out, f'<p>{study_line_0}.</p>\n\n')
        file_append(filepath_out, f'<p>{study_line_1}.</p>\n\n')
        file_append(filepath_out, f'<p>{study_line_2}</p>\n\n')
        file_append(filepath_out, f'</div>\n\n')

        # REMEDY RECIPE
        file_append(filepath_out, f'Below you can find a quick step-by-step recipe to make {remedy} for {PROBLEM}.\n\n')
        for k, item in enumerate(recipe):
            file_append(filepath_out, f'{k+1}. {item}\n')
        file_append(filepath_out, f'\n')

        i += 1


    i = 1
    for supplementary in supplementary_list:
        title = supplementary['title'].strip()
        content = supplementary['content'].strip()

        # SUPPLEMENTARY TITLE
        file_append(filepath_out, f'## {title.title()}\n\n')

        # SUPPLEMENTARY content
        lines = content.split('. ')
        line_0 = lines[0]
        line_1 = '. '.join(lines[1:-1])
        line_2 = lines[-1]
        file_append(filepath_out, f'{line_0}.\n\n')
        file_append(filepath_out, f'{line_1}.\n\n')
        file_append(filepath_out, f'{line_2}\n\n')




def ai_gen_supplementary():
    llm = AutoModelForCausalLM.from_pretrained(
        models[0],
        model_type="mistral", 
        context_length=256, 
        max_new_tokens=512,
        )
    
    data = json_read(article_filepath)
    supplementary_list = data["supplementary"]
    herbs = [remedy['herb'] for remedy in data['remedies']]

    i = 0

    # BEST BLEND
    title = supplementary_list[0]['title'].strip()
    content = supplementary_list[0]['content'].strip()

    if title != '' and content == '':
        reply_start = 'The best herbal tea mix for upset stomach is '
        prompt = f'''
            Write a 60-word paragraph answering the following question: {title}
            {reply_start}
        '''
        reply = gen_reply(prompt).strip()
        reply = reply_start + reply
        reply = reply.replace('\n')
        reply = re.sub("\s\s+" , " ", reply)

        data["supplementary"][0]['content'] = reply

        json_write(article_filepath, data)
    i += 1

    # DOSAGE EFFECTS
    title = supplementary_list[i]['title'].strip()
    content = supplementary_list[i]['content'].strip()

    if title != '' and content == '': 
        herbs_text = ', '.join(herbs)

        reply_start = 'The recommended dosage of herbal tea for upset stomach is '
        prompt = f'''
            Write a 3-sentence paragraph about herbal tea for upset stomach.
            In sentence 1, tell me what is the recommended dosage.
            In sentence 2, tell me when you should drink herbal it.
            In sentence 3, tell me how many times a day you should drink it.
            {reply_start}
        '''
        reply = gen_reply(prompt).strip()

        if not reply.startswith('The'):
            reply = reply_start + reply
            reply = reply.replace('\n', '')
            reply = re.sub("\s\s+" , " ", reply)

            data["supplementary"][i]['content'] = reply

            json_write(article_filepath, data)
    i += 1

    # WORST HERBS
    title = supplementary_list[i]['title'].strip()
    content = supplementary_list[i]['content'].strip()

    if title != '' and content == '': 
        herbs_text = ', '.join(herbs)

        reply_start = 'The worst herbal teas for upset stomach are '
        prompt = f'''
            Write a paragraph answering the following question: What are the worst herbal teas for upset stomach? 
            Answer with a paragraph, don't use lists.
            Don't include the following: {herbs_text}. 
            Start with the following words: {reply_start}
        '''
        reply = gen_reply(prompt).strip()
        
        if not reply.startswith('The'):
            reply = reply_start + reply
            reply = reply.replace('\n', '')
            reply = re.sub("\s\s+" , " ", reply)

            data["supplementary"][i]['content'] = reply

            json_write(article_filepath, data)
    i += 1

    # SIDE EFFECTS
    title = supplementary_list[i]['title'].strip()
    content = supplementary_list[i]['content'].strip()

    if title != '' and content == '': 
        herbs_text = ', '.join(herbs)

        reply_start = 'The side effects of using herbal teas for upset stomach are '
        prompt = f'''
            Write a paragraph answering the following question: What are the side effects of using herbal teas for upset stomach?
            {reply_start}
        '''
        reply = gen_reply(prompt).strip()
        
        if not reply.startswith('The'):
            reply = reply_start + reply
            reply = reply.replace('\n', '')
            reply = re.sub("\s\s+" , " ", reply)

            data["supplementary"][i]['content'] = reply

            json_write(article_filepath, data)
    i += 1

    # PRECAUTIONS
    title = supplementary_list[i]['title'].strip()
    content = supplementary_list[i]['content'].strip()

    if title != '' and content == '': 
        herbs_text = ', '.join(herbs)

        # reply_start = 'The recommended dosage of herbal tea for upset stomach is '
        prompt = f'''
            What are the precautions to consider when using herbal teas for upset stomach?
            Answer in a 5-line paragraph without using lists.
            '''
            # {reply_start}
        reply = gen_reply(prompt).strip()

        if not reply.startswith('The'):
            # reply = reply_start + reply
            reply = reply.replace('\n', '')
            reply = re.sub("\s\s+" , " ", reply)

            data["supplementary"][i]['content'] = reply

            json_write(article_filepath, data)
    i += 1




if sys.argv[1] == 'remedy-intro':
    ai_gen_remedy_intro()
    winsound.Beep(freq, duration)


if sys.argv[1] == 'remedy-recipe':
    ai_gen_remedy_recipe()
    winsound.Beep(freq, duration)


if sys.argv[1] == 'remedy-all':
    ai_gen_remedy_intro()
    ai_gen_remedy_recipe()
    winsound.Beep(freq, duration)


if sys.argv[1] == 'supplementary':
    ai_gen_supplementary()
    winsound.Beep(freq, duration)



# scientific_names_check()



def json_init():
    content = file_read('_dump.md')

    remedies = []
    for herb in REMEDIES:
        remedies.append(
            {
                "herb": herb,
                "intro": "",
                "study": "",
                "recipe": []
            }
        )

    content = file_read(article_filepath)
    if content.strip() == '':
        data = {
            "remedy_num": REMEDY_NUM,
            "problem": PROBLEM,
            "preparation": PREPARATION,
            "title": TITLE,
            "intro_1": "",
            "intro_2": "",
            "remedies": remedies
        }
        json_append(article_filepath, data)





if sys.argv[1] == 'json-init':
    json_init()


if sys.argv[1] == 'name-check':
    scientific_names_check()



if sys.argv[1] == 'output-3':
    generate_output_3()


if sys.argv[1] == 'intro-2':
    generate_intro_2()





if sys.argv[1] == 'herbs':
    prob = 'anemia'
    query = f'herbal teas for {prob}'

    prompt = f'''
        Write a list of 30 of herbal teas for {prob}.
        Order them by effectiveness for {prob}.
        Write only the names, not the desciptions.
    '''
    reply = gen_reply(prompt).strip()

