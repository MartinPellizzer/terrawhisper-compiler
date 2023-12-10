import csv
import os
import re
from ctransformers import AutoModelForCausalLM
import sys
import utils
import json
import time


sys_arg_override = False
try: 
    if sys.argv[1] == 'override': sys_arg_override = True
except: pass


SYSTEM_PROMPT = 'You are an expert botanist who explain things using simple, coincise, straightforward sentences.'
SYSTEM_PROMPT_LIST = 'You are an expert botanist who only write numbered lists and nothing else.'

def csv_get_rows(filepath):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter="|")
        for i, line in enumerate(reader):
            rows.append(line)
    return rows


def get_latin_name(entity):
    entity_words = entity.capitalize().split('-')
    first_word = entity_words[0]
    rest_words = '-'.join(entity_words[1:])
    latin_name = ' '.join([first_word, rest_words])
    return latin_name




# llm = AutoModelForCausalLM.from_pretrained("mistral-7b-instruct-v0.1.Q8_0.gguf", model_type="mistral", max_new_tokens=1024, context_length=1024)
# llm = AutoModelForCausalLM.from_pretrained("C:\\Users\\admin\\Desktop\\models\\openhermes-2.5-mistral-7b.Q8_0.gguf", model_type="mistral", context_length=1024, max_new_tokens=1024)
# llm = AutoModelForCausalLM.from_pretrained("C:\\Users\\admin\\Desktop\\models\\dolphin-2.2.1-mistral-7b.Q8_0.gguf", model_type="mistral", context_length=1024, max_new_tokens=1024)
llm = AutoModelForCausalLM.from_pretrained(
    "C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-1.Q8_0.gguf", 
    model_type="mistral", 
    context_length=1024, 
    max_new_tokens=1024, 
    temperature=1, 
    repetition_penalty=1.5
    )
# llm = AutoModelForCausalLM.from_pretrained("C:\\Users\\admin\\Desktop\\models\\dolphin-2.1-mistral-7b.Q8_0.gguf", model_type="mistral", context_length=1024, max_new_tokens=1024)

num_articles = 60





def write_section(section, action='default'):
    rows = csv_get_rows(f'plants.csv')
    for i, row in enumerate(rows[1:num_articles+1]):

        start_time = time.time()

        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        try: os.makedirs(f'database')
        except: pass
        try: os.makedirs(f'database/articles')
        except: pass
        try: os.makedirs(f'database/articles/{entity}')
        except: pass

        # if not sys_arg_override:
        #     try:
        #         with open(f'database/articles/{entity}/{section}.md', 'r', encoding='utf-8') as f:
        #             content = f.read()
        #     except:
        #         content = ''
        #     if content.strip() != '': continue

        # if action == 'default' or action == 'test': 
        try:
            with open(f'database/articles/{entity}/{section}.md', 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            content = ''
        if content.strip() != '': continue

        if section == 'intro':
            prompt = f'''
                Write 3 paragraphs in 300 words about {common_name} ({latin_name}).
                In paragraph 1, write about the medicinal and culinary aspects of this plant. Also, start paragraph 1 with the following words: "{common_name}, scientifically know as {latin_name}, is ".
                In paragraph 2, write about the horticultural and ornamental aspects of this plant.
                In paragraph 3, write about the botanical and historical aspects of this plant.
            '''
        elif section == 'medicine':
            prompt = f'''
                Write 5 paragraphs in 400 words about the medicinal aspects {common_name} ({latin_name}).
                In paragraph 1, write about the health benefits and health conditions this plant helps, without mentioning constituents. Start paragraph 1 with the following words: "{common_name.capitalize()} ({latin_name}) has many health benefits, such as ".
                In paragraph 2, write about the medicinal constituents.
                In paragraph 3, write about the most used parts and medicinal preparations.
                In paragraph 4, write about the possible side effects.
                In paragraph 5, write about the precautions.
            '''
        elif section == 'cuisine':
            prompt = f'''
                Write 5 paragraphs in 400 words about the culinary aspects of {common_name} ({latin_name}).
                In paragraph 1, write about the culinary uses.
                In paragraph 2, write about the flavor profile.
                In paragraph 3, write about the edible parts.
                In paragraph 4, write about the culinary tips.
                In paragraph 5, write about the possible side effects and toxicity.
                Include as much data as possible in as few words as possible.
                Don't include medicinal aspects.
                Don't write lists.
            '''
        elif section == 'horticulture':
            prompt = f'''
                Write 5 paragraphs in 400 words about the horticultural aspects of {common_name} ({latin_name}).
                In paragraph 1, write what are the growth requirements.
                In paragraph 2, write what are the planting tips.
                In paragraph 3, write what are the caring tips.
                In paragraph 4, write what are the harvesting tips.
                In paragraph 5, write what are the pests and diseases.
                Include as much data as possible in as few words as possible.
                Use the metric system.
                Don't write lists.
            '''
        elif section == 'botany':
            prompt = f'''
                Write 5 paragraphs in 400 words about the botanical aspects of {common_name} ({latin_name}).
                In paragraph 1, tell me the taxonomy, including domain, kingdom, phylum, class, order, family, genus, species. Then, tell me the common names. Also, start paragraph 1 with the following words: "{common_name}, with botanical name {latin_name}, belongs to the domain ".
                In paragraph 3, tell me the morphology.
                In paragraph 2, tell me the variants names and their differences.
                In paragraph 4, tell me the geographic distribution and natural habitats.
                In paragraph 5, tell me the life-cycle.
                Include as much data as possible in as few words as possible.
                Don't write lists.
            '''
        elif section == 'history':
            prompt = f'''
                Write 5 paragraphs in 400 words about the historical aspects of {common_name} ({latin_name}).
                In paragraph 1, write about the origin and etymology of the word "{common_name}". Start paragraph 1 with the following words: The etymology of "{common_name}" originates from .
                In paragraph 2, write about the cultural significances.
                In paragraph 3, write about the myths and legends.
                In paragraph 4, write about the references in literature.
                In paragraph 5, write about the folkloristic uses.
                Don't write lists.
            '''




        print()
        print(f"Q: {i+1}/{num_articles}")
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

        # clean text
        reply = reply.strip()
        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line.strip().endswith(':'): continue
            if len(line.split('.')) < 2: continue
            if ':' in line: line = line.split(':')[1]
            if line[0].isdigit(): line = ' '.join(line.split(' ')[1:])
            if line[0] == '-': line = ' '.join(line.split(' ')[1:])
            if 'in summary' in line.lower(): continue
            if 'to summarize' in line.lower(): continue
            if 'in conclusion' in line.lower(): continue
            if 'overall' in line.lower(): continue
            lines_formatted.append(line)
        reply = '\n\n'.join(lines_formatted)

        # calculate lenght text
        tot_words = 0
        num_paragraphs = 0
        paragraphs = reply.split('\n')
        for paragraph in paragraphs:
            if paragraph.strip() != '':
                paragraph = paragraph.split(' ')
                tot_words += len(paragraph)
                num_paragraphs += 1
        agv_words = tot_words//num_paragraphs
        print(f'Tot Length: {tot_words}')
        print(f'Avg Length: {agv_words}')
        print(f'Num Paragraphs: {num_paragraphs}')
        if section == 'intro':
            if tot_words < 200:
                print() 
                print("ABORT: Too few words *****************************") 
                continue
        else:
            if tot_words < 200:
                print() 
                print("ABORT: Too few words *****************************") 
                continue
        if num_paragraphs < 3 or num_paragraphs > 5:
            print() 
            print("ABORT: Wrong num paragraphs *****************************") 
            continue
        print()
        print()
        print()

        # if action == 'default' or action == 'override':
        with open(f'database/articles/{entity}/{section}.md', 'w', newline='', encoding='utf-8') as f:
            f.write(reply)

        print(f"--- {(time.time() - start_time)} seconds ---")


for i in range(3):
    write_section('intro')
    write_section('medicine')
    write_section('cuisine')
    write_section('horticulture')
    write_section('botany')
    write_section('history')









llm = AutoModelForCausalLM.from_pretrained("C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.1.Q8_0.gguf", model_type="mistral", context_length=1024, max_new_tokens=256)


def write_list(section):
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:num_articles+1]):

        start_time = time.time()
        # print()

        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)


        if not sys_arg_override:
            # skip if entity list already found
            tmp_rows = csv_get_rows(f'database/tables/{section}.csv')
            tmp_entities = [tmp_row[0] for tmp_row in tmp_rows]
            if entity in tmp_entities: continue 

        
        prompt_template = f"""
            Write a list of 10 <att_1> of {common_name} ({latin_name}).
            Write each list item in less than 5 words.
            Start each list item with a verb.
            Write each list item in a new line.
            Don't add descriptions.
        """

        if section == 'benefits':
            prompt = prompt_template.replace('<att_1>', 'health benefits')
        elif section == 'cuisine':
            prompt = prompt_template.replace('<att_1>', 'culinary uses')
        elif section == 'horticulture':
            prompt = prompt_template.replace('<att_1>', 'tips for growing')
        # elif section == 'botany':
            # prompt = prompt_template.replace('<att_1>', 'morphological characteristics')
        elif section == 'history':
            prompt = prompt_template.replace('<att_1>', 'historical uses')
        else: 
            prompt = ''

        if prompt == '': continue
        
        print()
        print(f"Q: {i+1}/{num_articles}")
        print()
        print(prompt)
        print()
        print("A:")
        print()
        reply = ''
        for text in llm(prompt, stream=True):
            reply += text
            print(text, end="", flush=True)
        # print(reply)
        print()
        print()

        lines = reply.split('\n')

        lines_formatted = []
        abort = False
        for line in lines:
            tmp_line = line.strip()
            if tmp_line == '': continue
            if tmp_line[0].isdigit():
                tmp_line = ' '.join(tmp_line.split(' ')[1:])
                tmp_line = tmp_line.replace('.', '')
                tmp_line = tmp_line.strip()
                tmp_line = tmp_line.split(':')[0]
                tmp_line = tmp_line.split(' - ')[0]
                lines_formatted.append([entity, tmp_line])
            elif tmp_line[0] == '*':
                tmp_line = tmp_line.replace('*', '')
                tmp_line = tmp_line.strip()
                tmp_line = tmp_line.split(':')[0]
                tmp_line = tmp_line.split(' - ')[0]
                lines_formatted.append([entity, tmp_line])
            else:
                continue
            if len(line.strip().split(' ')) > 10:
                abort = True
                break
        if abort:
            print('ABORTED ************************') 
            continue
        lines_formatted = lines_formatted[:10]
        print(len(lines_formatted))
        if len(lines_formatted) != 10: 
            print('WRONG LINE NUMBER ************************') 
            continue

        with open(f'database/tables/{section}.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='|')
            for line in lines_formatted:
                writer.writerow(line)
                
        print(f"--- {(time.time() - start_time)} seconds ---")


for i in range(3):
    write_list('medicine')
    write_list('cuisine')
    write_list('horticulture')
    # write_list('botany')
    write_list('history')


llm = AutoModelForCausalLM.from_pretrained(
    "C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.1.Q8_0.gguf", 
    model_type="mistral", 
    context_length=1024, 
    max_new_tokens=256, 
)



def get_taxonomy():
    if not os.path.exists(f'database/tables/botany/taxonomy.csv'):
        with open(f'database/tables/botany/taxonomy.csv', 'w', newline='', encoding='utf-8') as f: 
            writer = csv.writer(f, delimiter='|')
            writer.writerow([
            'entity',
            'domain',
            'kingdom',
            'phylum',
            'class',
            'order',
            'family',
            'genus',
            'species',
            ])

    rows = csv_get_rows(f'plants.csv') 

    for i, row in enumerate(rows[1:num_articles+1]):
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        tmp_rows = csv_get_rows(f'database/tables/botany/taxonomy.csv')
        if len(tmp_rows) != 0:
            tmp_entities = [tmp_row[0] for tmp_row in tmp_rows]
            if entity in tmp_entities:
                print('skipped') 
                continue
            else:
                print('added')

        prompt = f'''
            Give me the linnaean taxonomy of {common_name} ({latin_name}).
            Write it using the following format:
            - Domain
            - Kingdom
            - Phylum
            - Class
            - Order
            - Family
            - Genus
            - Species
        '''

        print()
        print(f"Q: {i+1}/{len(rows)}")
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
        print()
        print()
        print()

        # format data
        lines = reply.split('\n')
        data = {
            'domain': '',
            'kingdom': '',
            'phylum': '',
            'class': '',
            'order': '',
            'family': '',
            'genus': '',
            'species': ''
        }
        for line in lines:
            words = line.split(':')
            if len(words) < 2: continue
            value = words[-1].split('(')[0].strip().lower()
            if 'domain' in line.lower(): data['domain'] = value
            if 'kingdom' in line.lower(): data['kingdom'] = value
            if 'phylum' in line.lower(): data['phylum'] = value
            if 'class' in line.lower(): data['class'] = value
            if 'order' in line.lower(): data['order'] = value
            if 'family' in line.lower(): data['family'] = value
            if 'genus' in line.lower(): data['genus'] = value
            if 'species' in line.lower(): data['species'] = value

        # check missing data
        if data['domain'].strip() == '': continue
        if data['kingdom'].strip() == '': continue
        if data['phylum'].strip() == '': continue
        if data['class'].strip() == '': continue
        if data['order'].strip() == '': continue
        if data['family'].strip() == '': continue
        if data['genus'].strip() == '': continue
        if data['species'].strip() == '': continue

        # save
        with open(f'database/tables/botany/taxonomy.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='|')
            row = [
                entity,
                data['domain'].strip(),
                data['kingdom'].strip(),
                data['phylum'].strip(),
                data['class'].strip(),
                data['order'].strip(),
                data['family'].strip(),
                data['genus'].strip(),
                data['species'].strip(),
            ]
            writer.writerow(row)

for _ in range(3):
    get_taxonomy()