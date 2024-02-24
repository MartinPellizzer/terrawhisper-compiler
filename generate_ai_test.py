import csv
import os
import re
from ctransformers import AutoModelForCausalLM
import sys
import utils
import json
import time

sys_override = False
try: 
    if sys.argv[1] == 'override': sys_override = True
except: pass


SYSTEM_PROMPT = 'Act as an expert botanist. Write short, simple, and straightforward sentences.'
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


def clean_reply(reply):
    reply = reply.strip()
    lines = reply.split('\n')
    lines_formatted = []
    for line in lines:
        line = line.strip()
        if line == '': continue
        if line.strip().endswith(':'): continue
        if len(line.split('.')) < 2: 
            print('skipped: len < 2')
            continue
        if ':' in line: line = line.split(':')[1]
        if line == '': continue
        if line[0].isdigit(): 
            line = ' '.join(line.split(' ')[1:])
        if line[0] == '-': 
            line = ' '.join(line.split(' ')[1:])
        if 'in summary' in line.lower(): 
            print('skipped: in summary')
            continue
        if 'to summarize' in line.lower():
            print('skipped: to summarize') 
            continue
        if 'in conclusion' in line.lower():
            print('skipped: in conclusion') 
            continue
        # if 'overall' in line.lower(): 
        #     print('skipped: overall')
        #     continue
        lines_formatted.append(line)
    reply = '\n\n'.join(lines_formatted)

    return reply


num_items = 3

prompt_1 = f'''
    Write a 60 words paragraph about the medicinal [topic] of [plant].
    Include data from the following list: 
    [lst]

    Give details of each [topic].
    
    [starting-text]
'''

# Write 1 short sentence for each of these medicinal preparations of sweet flag:
# - Extracts
# - Powders
# - Essential oil
# - Tinctures
# - Pills

#     Sweet Flag can be prepared in many ways, such as extracts, powders, essential oil, tinctures, pills. Extracts


num_articles = 100

plants = csv_get_rows(f'plants.csv') 


# "C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-1.Q8_0.gguf", 
# "C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.1.Q8_0.gguf", 
llm = AutoModelForCausalLM.from_pretrained(
    "C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-1.Q8_0.gguf", 
    model_type="mistral", 
    context_length=1024, 
    max_new_tokens=1024,
    )


def create_folder(folderpath):
    chunks = folderpath.split('/')
    current_path = ''
    for chunk in chunks:
        current_path += f'{chunk}/'    
        try: os.makedirs(current_path)
        except: pass


def exists_content(filepath):
    with open(filepath, 'a', newline='', encoding='utf-8') as f: pass
    with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    
    if content.strip() == '': found = False
    else: found = True

    return found
    

def exists_subsection(filepath, subsection):
    with open(filepath, 'a', newline='', encoding='utf-8') as f: pass
    
    found = False
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="|")
        for line in reader:
            if line[1].lower().strip() == subsection.lower().strip():
                found = True
                break

    return found


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


def csv_update_override_cell(filepath, entity, benefit, value):
    rows = csv_get_rows(filepath)
    rows_new = []
    for row in rows:
        if row[1].strip().lower() == benefit.strip().lower():
            rows_new.append([entity, benefit, value])
        else:
            rows_new.append(row)

    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerows(rows_new)


def format_text(starting_text, text):
    text = text.strip()
    

    if starting_text.lower() not in text.lower():
        starting_text = starting_text.strip() + ' '
        text = starting_text + text

    text = text.replace('\n', '')
    # text = text.split('\n')[0]
    text = re.sub("\s\s+" , " ", text)

    return text




# ################################################################
# MAIN
# ################################################################

def gen_root_medicine(entity, common_name):
    latin_name = get_latin_name(entity)
    out_filepath = f'database/articles/{entity}/medicine-2.md'

    prompt = f'''
        {SYSTEM_PROMPT}
        Write 5 paragraphs in 400 words about the medicinal aspects {common_name} ({latin_name}).
        In paragraph 1, write about the health benefits and health conditions this plant helps, without mentioning constituents. Start paragraph 1 with the following words: "{common_name.capitalize()} ({latin_name}) has many health benefits, such as ".
        In paragraph 2, write about the medicinal constituents.
        In paragraph 3, write about the most used parts and medicinal preparations.
        In paragraph 4, write about the possible side effects.
        In paragraph 5, write about the precautions.
    '''
    reply = gen_reply(prompt)
    reply = clean_reply(reply)

    with open(out_filepath, 'w', encoding='utf-8') as f: 
        f.write(reply)


def gen_root_medicine_benefits_text(entity, common_name, override=False):
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
    lst = [f'{x[1]}' for x in rows[:num_items]]
    benefits_list = '- ' + '\n- '.join(lst)
    benefits_text = ', '.join(lst).lower()

    out_filepath = f'database/articles/{entity}/medicine-benefits-1.md'
    if sys_override: found = False
    else: found = exists_content(out_filepath)

    if not found or override:
        starting_text = f'{common_name.title()} has many health benefits, such as '
        prompt = prompt_1
        prompt = prompt.replace('[plant]', common_name) 
        prompt = prompt.replace('[topic]', 'benefit') 
        prompt = prompt.replace('[lst]', benefits_list) 
        prompt = prompt.replace('[starting-text]', starting_text) 

        reply = gen_reply(prompt)
        reply = format_text(starting_text, reply)
        with open(out_filepath, 'w', encoding='utf-8') as f: 
            f.write(reply)
    else:
        print(f"gen_root_medicine_benefits_text [{entity}]: ALREADY GENERATED")


def gen_root_medicine_constituents_text(entity, common_name, override=False):
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/constituents.csv', entity)
    lst = [f'{x[1]}' for x in rows[:num_items]]
    constituents_list = '- ' + '\n- '.join(lst)
    constituents_text = ', '.join(lst).lower()

    out_filepath = f'database/articles/{entity}/medicine-constituents.md'
    if sys_override: found = False
    else: found = exists_content(out_filepath)

    if not found or override:
        starting_text = f'{common_name.title()} has several medicinal constituents, such as {constituents_text}. {lst[0].capitalize()} '
        prompt = prompt_1
        prompt = prompt.replace('[plant]', common_name) 
        prompt = prompt.replace('[topic]', 'constituents') 
        prompt = prompt.replace('[lst]', constituents_list) 
        prompt = prompt.replace('[starting-text]', starting_text) 
        reply = gen_reply(prompt)
        reply = format_text(starting_text, reply)
        with open(out_filepath, 'w', encoding='utf-8') as f: 
            f.write(reply)
    else:
        print(f"gen_root_medicine_constituents_text [{entity}]: ALREADY GENERATED")


def gen_root_medicine_preparations_text(entity, common_name, override=False):
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/preparations.csv', entity)
    lst = [f'{x[1]}' for x in rows[:num_items]]
    preparations_list = (f'- {common_name} ' + f'\n- {common_name} '.join(lst)).title()
    preparations_text = (f'{common_name} ' + f', {common_name} '.join(lst)).title()

    out_filepath = f'database/articles/{entity}/medicine-preparations.md'
    if sys_override: found = False
    else: found = exists_content(out_filepath)

    if not found or override:
        starting_text = f'{common_name.title()} has many medicinal preparations, such as {preparations_text}. {common_name.title()} {lst[0]} '
        prompt = prompt_1
        prompt = prompt.replace('[plant]', common_name) 
        prompt = prompt.replace('[topic]', 'preparations') 
        prompt = prompt.replace('[lst]', preparations_list) 
        prompt = prompt.replace('[starting-text]', starting_text) 
        reply = gen_reply(prompt)
        reply = format_text(starting_text, reply)
        with open(out_filepath, 'w', encoding='utf-8') as f: 
            f.write(reply)
    else:
        print(f"gen_root_medicine_preparations_text [{entity}]: ALREADY GENERATED")


def gen_root_medicine_side_effects_text(entity, common_name, override=False):
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/side-effects.csv', entity)
    lst = [f'{x[1]}' for x in rows[:num_items]]
    lst = '- ' + '\n- '.join(lst)
    # lst = ', '.join(lst)

    out_filepath = f'database/articles/{entity}/medicine-side-effects.md'
    if sys_override: found = False
    else: found = exists_content(out_filepath)

    if not found or override:
        starting_text = f'If used improperly, {common_name.title()} '
        prompt = prompt_1
        prompt = prompt.replace('[plant]', common_name) 
        prompt = prompt.replace('[topic]', 'side effects') 
        prompt = prompt.replace('[lst]', lst) 
        prompt = prompt.replace('[starting-text]', starting_text) 
        reply = gen_reply(prompt)
        reply = format_text(starting_text, reply)
        with open(out_filepath, 'w', encoding='utf-8') as f: 
            f.write(reply)
    else:
        print(f"gen_root_medicine_side_effects_text [{entity}]: ALREADY GENERATED")


def gen_root_medicine_precautions_text(entity, common_name, override=False):
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/precautions.csv', entity)
    lst = [f'{x[1]}' for x in rows[:num_items]]
    lst = '- ' + '\n- '.join(lst)
    # lst = ', '.join(lst)

    out_filepath = f'database/articles/{entity}/medicine-precautions.md'
    if sys_override: found = False
    else: found = exists_content(out_filepath)

    if not found or override:
        starting_text = f'Before using {common_name.title()} '
        prompt = prompt_1
        prompt = prompt.replace('[plant]', common_name) 
        prompt = prompt.replace('[topic]', 'precautions') 
        prompt = prompt.replace('[lst]', lst) 
        prompt = prompt.replace('[starting-text]', starting_text) 
        reply = gen_reply(prompt)
        reply = format_text(starting_text, reply)
        with open(out_filepath, 'w', encoding='utf-8') as f: 
            f.write(reply)
    else:
        print(f"gen_root_medicine_precautions_text [{entity}]: ALREADY GENERATED")





def gen_plant_medicine_benefits(plant):
    filepath = f'database/tables/medicine/benefits.csv'

    entity = plant[0].strip()
    common_name = plant[1].strip()
    latin_name = get_latin_name(entity)

    if sys_override: found = False
    else:    
        tmp_rows = csv_get_rows(filepath)
        tmp_entities = [tmp_row[0] for tmp_row in tmp_rows]
        if entity in tmp_entities: found = True
        else: found = False 

    if not found:
        prompt = f"""
            Write a numbered list of the 10 primary medicinal benefits of {common_name} ({latin_name}).
            Write just the names. Don't add descriptions.
            Write each list item in a new line.
        """
        
        start_time = time.time()
        reply = gen_reply(prompt)
        end_time = time.time()
        print(f"--- {(end_time - start_time)} seconds ---")

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
                line = line.replace('.', '')
                line = line.split(':')[0]
                line = line.split(' - ')[0]
            elif line[0] == '*':
                line = line.replace('*', '')
                line = line.split(':')[0]
                line = line.split(' - ')[0]
            else:
                continue
            lines_formatted.append(line.strip())
                
        if sys_override:
            filtered_rows = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[0].lower().strip() != entity.lower().strip():
                        filtered_rows.append(line)
                        
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerows(filtered_rows)
                        
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for line in lines_formatted:
                    writer.writerow([entity, line])
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for line in lines_formatted:
                    writer.writerow([entity, line])


def gen_plant_medicine_constituents(plant):
    filepath = f'database/tables/medicine/constituents.csv'

    entity = plant[0].strip()
    common_name = plant[1].strip()
    latin_name = get_latin_name(entity)

    if sys_override: found = False
    else:    
        tmp_rows = csv_get_rows(filepath)
        tmp_entities = [tmp_row[0] for tmp_row in tmp_rows]
        if entity in tmp_entities: found = True
        else: found = False 

    if not found:
        prompt = f"""
            Write a numbered list of the 10 primary medicinal constituents of {common_name} ({latin_name}).
            Write just the names. Don't add descriptions.
            Write each list item in a new line.
        """
        
        start_time = time.time()
        reply = gen_reply(prompt)
        end_time = time.time()
        print(f"--- {(end_time - start_time)} seconds ---")

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
                line = line.replace('.', '')
                line = line.split(':')[0]
                line = line.split(' - ')[0]
            elif line[0] == '*':
                line = line.replace('*', '')
                line = line.split(':')[0]
                line = line.split(' - ')[0]
            else:
                continue
            lines_formatted.append(line.strip())
                
        if sys_override:
            filtered_rows = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[0].lower().strip() != entity.lower().strip():
                        filtered_rows.append(line)
                        
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerows(filtered_rows)
                        
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for line in lines_formatted:
                    writer.writerow([entity, line])
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for line in lines_formatted:
                    writer.writerow([entity, line])


def gen_plant_medicine_preparations(plant):
    filepath = f'database/tables/medicine/preparations.csv'

    entity = plant[0].strip()
    common_name = plant[1].strip()
    latin_name = get_latin_name(entity)

    if sys_override: found = False
    else:    
        tmp_rows = csv_get_rows(filepath)
        tmp_entities = [tmp_row[0] for tmp_row in tmp_rows]
        if entity in tmp_entities: found = True
        else: found = False 

    if not found:
        prompt = f"""
            Write a numbered list of the 10 most important preparations of {common_name} ({latin_name}) for medicinal purposes (ex. tea, etc...).
            Write just the names of the preparations. Don't add descriptions.
            Write each name of the praparations in 1 or 2 words max.
            Write each list item in a new line.
        """
        
        start_time = time.time()
        reply = gen_reply(prompt)
        end_time = time.time()
        print(f"--- {(end_time - start_time)} seconds ---")

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
                line = line.replace('.', '')
                line = line.split(':')[0]
                line = line.split(' - ')[0]
            elif line[0] == '*':
                line = line.replace('*', '')
                line = line.split(':')[0]
                line = line.split(' - ')[0]
            else:
                continue
            lines_formatted.append(line.strip())
                
        if sys_override:
            filtered_rows = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[0].lower().strip() != entity.lower().strip():
                        filtered_rows.append(line)
                        
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerows(filtered_rows)
                        
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for line in lines_formatted:
                    writer.writerow([entity, line])
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for line in lines_formatted:
                    writer.writerow([entity, line])
                    

def gen_plant_medicine_side_effects(plant):
    filepath = f'database/tables/medicine/side-effects.csv'
    with open(filepath, 'a', encoding='utf-8') as f: pass

    entity = plant[0].strip()
    common_name = plant[1].strip()
    latin_name = get_latin_name(entity)

    if sys_override: found = False
    else:    
        tmp_rows = csv_get_rows(filepath)
        tmp_entities = [tmp_row[0] for tmp_row in tmp_rows]
        if entity in tmp_entities: found = True
        else: found = False 

    if not found:
        prompt = f"""
            Write a numbered list of 10 negative effects of {common_name} ({latin_name}).
            Write each list item in 3 words or less.
            Start each list item with a verb.
            Write each list item in a new line.
            Don't add descriptions.
        """
        
        start_time = time.time()
        reply = gen_reply(prompt)
        end_time = time.time()
        print(f"--- {(end_time - start_time)} seconds ---")

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
                line = line.replace('.', '')
                line = line.split(':')[0]
                line = line.split(' - ')[0]
            elif line[0] == '*':
                line = line.replace('*', '')
                line = line.split(':')[0]
                line = line.split(' - ')[0]
            else:
                continue
            lines_formatted.append(line.strip())
                
        if sys_override:
            filtered_rows = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[0].lower().strip() != entity.lower().strip():
                        filtered_rows.append(line)
                        
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerows(filtered_rows)
                        
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for line in lines_formatted:
                    writer.writerow([entity, line])
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for line in lines_formatted:
                    writer.writerow([entity, line])


def gen_plant_medicine_precautions(plant):
    filepath = f'database/tables/medicine/precautions.csv'
    with open(filepath, 'a', encoding='utf-8') as f: pass

    entity = plant[0].strip()
    common_name = plant[1].strip()
    latin_name = get_latin_name(entity)

    if sys_override: found = False
    else:    
        tmp_rows = csv_get_rows(filepath)
        tmp_entities = [tmp_row[0] for tmp_row in tmp_rows]
        if entity in tmp_entities: found = True
        else: found = False 

    if not found:
        prompt = f"""
            Write a numbered list of 10 precautions to take when using {common_name} ({latin_name}) as a medicine.
            Write each list item in a new line.
            Write each list item using less than 5 words.
            Don't add descriptions.
        """
        
        start_time = time.time()
        reply = gen_reply(prompt)
        end_time = time.time()
        print(f"--- {(end_time - start_time)} seconds ---")

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
                line = line.replace('.', '')
                line = line.split(':')[0]
                line = line.split(' - ')[0]
            elif line[0] == '*':
                line = line.replace('*', '')
                line = line.split(':')[0]
                line = line.split(' - ')[0]
            else:
                continue
            lines_formatted.append(line.strip())
                
        if sys_override:
            filtered_rows = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[0].lower().strip() != entity.lower().strip():
                        filtered_rows.append(line)
                        
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerows(filtered_rows)
                        
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for line in lines_formatted:
                    writer.writerow([entity, line])
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for line in lines_formatted:
                    writer.writerow([entity, line])





# ################################################################
# MEDICINE
# ################################################################

def gen_medicine_benefits_text(entity, common_name):
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
    lst = [f'{x[1]}' for x in rows[:10]]
    # benefits = ', '.join(benefits_lst)
    lst = '- ' + '\n- '.join(lst)

    out_filepath = f'database/articles/{entity}/medicine/benefits.md'
    if sys_override: found = False
    else: found = exists_content(out_filepath)

    if not found:

        starting_text = f'{common_name.title()} has many health benefits, such as '
        # starting_text = f'1) {common_name.title()} '
        # prompt = f'''
        #     For each benefit of {common_name} in the following list:
        #     {benefits}

        #     Write a short paragraph explaing that benefit.
        #     All paragraph must be 2-3 sentences long.
        #     Add a new empty line after every paragraph.
        #     Write about 400 words of content.
        #     Start with these words: {starting_text}

        # '''

        prompt = f'''
            Explain in 400 words these health benefits of {common_name}: {lst}. 
            Start with these words: {starting_text}
        '''

        reply = gen_reply(prompt)
        reply = reply.strip()
        paragraphs = reply.split('\n')
        paragraphs_lst = []
        for paragraph in paragraphs:
            paragraph.strip()
            if paragraph == '': continue
            if paragraph.endswith(':'): continue
            if paragraph[0].isdigit(): paragraph = ' '.join(paragraph.split(' ')[1:])
            if ':' in paragraph: paragraph = paragraph.split(':')[1]
            paragraph = re.sub("\s\s+" , " ", paragraph)
            paragraphs_lst.append(paragraph)
        content = '\n\n'.join(paragraphs_lst)
        if not reply.strip()[0].isdigit():
            content = starting_text + content
        
        if sys_override:
            with open(out_filepath, 'w', encoding='utf-8') as f: 
                f.write(content)
        else: 
            with open(out_filepath, 'a', encoding='utf-8') as f: 
                f.write(content)


def gen_medicine_constituents_text(entity, common_name):
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/constituents.csv', entity)
    lst = [f'{x[1]}' for x in rows[:10]]
    lst = ', '.join(lst)

    out_filepath = f'database/articles/{entity}/medicine/constituents.md'
    if sys_override: found = False
    else: found = exists_content(out_filepath)

    if not found:
        starting_text = f'{common_name.title()} has many medicinal constituents, such as '
        prompt = f'''
            Explain in 400 words these medicinal constituents of {common_name}: {lst}. 
            Start with these words: {starting_text}
        '''

        
        reply = gen_reply(prompt)
        reply = reply.strip()
        paragraphs = reply.split('\n')
        paragraphs_lst = []
        for paragraph in paragraphs:
            paragraph.strip()
            if paragraph == '': continue
            if paragraph.endswith(':'): continue
            if paragraph[0].isdigit(): paragraph = ' '.join(paragraph.split(' ')[1:])
            if ':' in paragraph: paragraph = paragraph.split(':')[1]
            paragraph = re.sub("\s\s+" , " ", paragraph)
            paragraphs_lst.append(paragraph)
        content = '\n\n'.join(paragraphs_lst)
        if not reply.strip()[0].isdigit():
            content = starting_text + content
        
        if sys_override:
            with open(out_filepath, 'w', encoding='utf-8') as f: 
                f.write(content)
        else: 
            with open(out_filepath, 'a', encoding='utf-8') as f: 
                f.write(content)


def gen_medicine_preparations_text(entity, common_name):
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/preparations.csv', entity)
    lst = [f'{x[1]}' for x in rows[:10]]
    lst = ', '.join(lst)

    out_filepath = f'database/articles/{entity}/medicine/preparations.md'
    if sys_override: found = False
    else: found = exists_content(out_filepath)

    if not found:
        starting_text = f'{common_name.title()} has many medicinal preparations, such as '
        # prompt = f'''
        #     {SYSTEM_PROMPT}
        #     Explain in 400 words these medicinal preparations of {common_name}: {lst}. 
        #     Use numbered paragraphs that are 2-3 sentences long.
        #     Start with these words: {starting_text}
        # '''
        
        prompt = f'''
            Explain in 400 words these medicinal preparations of {common_name}: {lst}. 
            Start with these words: {starting_text}
        '''
        # Add a new empty line after every paragraph.

        reply = gen_reply(prompt)
        reply = reply.strip()
        reply = starting_text + reply

        reply = gen_reply(prompt)
        reply = reply.strip()
        paragraphs = reply.split('\n')
        paragraphs_lst = []
        for paragraph in paragraphs:
            paragraph.strip()
            if paragraph == '': continue
            if paragraph.endswith(':'): continue
            if paragraph[0].isdigit(): paragraph = ' '.join(paragraph.split(' ')[1:])
            if ':' in paragraph: paragraph = paragraph.split(':')[1]
            paragraph = re.sub("\s\s+" , " ", paragraph)
            paragraphs_lst.append(paragraph)
        content = '\n\n'.join(paragraphs_lst)
        if not reply.strip()[0].isdigit():
            content = starting_text + content
                    
        if sys_override:
            with open(out_filepath, 'w', encoding='utf-8') as f: 
                f.write(content)
        else: 
            with open(out_filepath, 'a', encoding='utf-8') as f: 
                f.write(content)


def gen_medicine_side_effects_text(entity, common_name):
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/side-effects.csv', entity)
    lst = [f'{x[1]}' for x in rows[:10]]
    lst = '-' + '\n- '.join(lst)

    out_filepath = f'database/articles/{entity}/medicine/side-effects.md'
    if sys_override: found = False
    else: found = exists_content(out_filepath)

    if not found:
        starting_text = f'{common_name.title()} can have some side effects if used improperly, such as '
        # prompt = f'''
        #     {SYSTEM_PROMPT}

        #     Explain in 400 words these negative effects of {common_name}: 
        #     {lst} 

        #     Write paragraphs that are 2-3 sentences long.
        #     Start with these words: {starting_text}
        # '''
        
        prompt = f'''
            Explain in 400 words these negative effects of {common_name}: {lst}. 
            Start with these words: {starting_text}
        '''

        
        reply = gen_reply(prompt)
        reply = reply.strip()
        paragraphs = reply.split('\n')
        paragraphs_lst = []
        for paragraph in paragraphs:
            paragraph.strip()
            if paragraph == '': continue
            if paragraph.endswith(':'): continue
            if paragraph[0].isdigit(): paragraph = ' '.join(paragraph.split(' ')[1:])
            if ':' in paragraph: paragraph = paragraph.split(':')[1]
            paragraph = re.sub("\s\s+" , " ", paragraph)
            paragraphs_lst.append(paragraph)
        content = '\n\n'.join(paragraphs_lst)
        if not reply.strip()[0].isdigit():
            content = starting_text + content
                    
        if sys_override:
            with open(out_filepath, 'w', encoding='utf-8') as f: 
                f.write(content)
        else: 
            with open(out_filepath, 'a', encoding='utf-8') as f: 
                f.write(content)


def gen_medicine_precautions_text(entity, common_name):
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/precautions.csv', entity)
    lst = [f'{x[1]}' for x in rows[:10]]
    lst = '-' + '\n- '.join(lst)

    out_filepath = f'database/articles/{entity}/medicine/precautions.md'
    if sys_override: found = False
    else: found = exists_content(out_filepath)

    if not found:
        starting_text = f'It\'s important to take precautions when using {common_name.title()} medicinally, such as '
        # prompt = f'''
        #     {SYSTEM_PROMPT}

        #     Explain in 400 words the following precautions you must take when using {common_name} medicinally: 
        #     {lst} 

        #     Write paragraphs that are 2-3 sentences long.
        #     Start with these words: {starting_text}
        # '''
        
        prompt = f'''
            Explain in 400 words these precautions when using {common_name}: {lst}. 
            Start with these words: {starting_text}
        '''

        reply = gen_reply(prompt)

        reply = gen_reply(prompt)
        reply = reply.strip()
        paragraphs = reply.split('\n')
        paragraphs_lst = []
        for paragraph in paragraphs:
            paragraph.strip()
            if paragraph == '': continue
            if paragraph.endswith(':'): continue
            if paragraph[0].isdigit(): paragraph = ' '.join(paragraph.split(' ')[1:])
            if ':' in paragraph: paragraph = paragraph.split(':')[1]
            paragraph = re.sub("\s\s+" , " ", paragraph)
            paragraphs_lst.append(paragraph)
        content = '\n\n'.join(paragraphs_lst)
        if not reply.strip()[0].isdigit():
            content = starting_text + content
                    
        if sys_override:
            with open(out_filepath, 'w', encoding='utf-8') as f: 
                f.write(content)
        else: 
            with open(out_filepath, 'a', encoding='utf-8') as f: 
                f.write(content)


def write_plant_medicine():
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:num_articles+1]):
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        create_folder(f'database/articles/{entity}/medicine')

        print(f'{i+1}/{num_articles} - {entity}')
        gen_medicine_benefits_text(entity, common_name)
        print(f'{i+1}/{num_articles} - {entity}')
        gen_medicine_constituents_text(entity, common_name)
        print(f'{i+1}/{num_articles} - {entity}')
        gen_medicine_preparations_text(entity, common_name)
        print(f'{i+1}/{num_articles} - {entity}')
        gen_medicine_side_effects_text(entity, common_name)
        print(f'{i+1}/{num_articles} - {entity}')
        gen_medicine_precautions_text(entity, common_name)

        
        






# ################################################################
# MEDICINE >> BENEFITS
# ################################################################

# sys_override = True
# entity = 'achillea-millefolium'
# common_name = 'yarrow'
# benefit = 'Reduces inflammation'

def gen_medicine_benefit_definition(entity, common_name, benefit):
    folderpath = f'database/articles/{entity}/medicine/benefits'
    filepath = f'database/articles/{entity}/medicine/benefits/definitions.csv'

    create_folder(folderpath)
    if sys_override: found = False
    else: found = exists_subsection(filepath, benefit)

    if not found:
        starting_text = f'"{common_name.title()} {benefit.lower()}" refers to its '
        prompt = f'''
            {SYSTEM_PROMPT}
            Define in detail in 1 sentence what "{common_name} {benefit}" means. 
            Start the sentence with these words: {starting_text}
        '''

        reply = gen_reply(prompt)

        reply = reply.split('.')[0] + '.'
        reply = reply.replace('"', '')
        reply = reply.strip()
        reply = starting_text + reply


        if sys_override:
            csv_update_override_cell(filepath, entity, benefit, reply)
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerow([entity, benefit, reply])


def gen_medicine_benefit_constituents_list(entity, common_name, benefit):
    folderpath = f'database/articles/{entity}/medicine/benefits'
    filepath = f'database/articles/{entity}/medicine/benefits/constituents_list.csv'

    create_folder(folderpath)
    if sys_override: found = False
    else: found = exists_subsection(filepath, benefit)

    if not found:
        prompt = f'''
            {SYSTEM_PROMPT_LIST}
            Write the 7 most important macro constituents of {common_name} that help with the following benefit: "{benefit}". 
            Give me just the names of the constituents. Don't add descriptions.
        '''

        reply = gen_reply(prompt)

        lines = reply.split('\n')
        constituents_list = []
        for line in lines:
            formatted_line = ''
            line = line.strip()
            if line == '': continue
            if line[0].isdigit(): formatted_line = ' '.join(line.split(' ')[1:])
            if formatted_line != '': constituents_list.append(formatted_line)

        if sys_override:
            filtered_rows = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[1].lower().strip() != benefit.lower().strip():
                        filtered_rows.append(line)
                        
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerows(filtered_rows)
                        
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for constituent in constituents_list:
                    writer.writerow([entity, benefit, constituent])
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for constituent in constituents_list:
                    writer.writerow([entity, benefit, constituent])


def gen_medicine_benefit_constituents_text(entity, common_name, benefit):
    folderpath = f'database/articles/{entity}/medicine/benefits'
    filepath = f'database/articles/{entity}/medicine/benefits/constituents_text.csv'

    create_folder(folderpath)
    if sys_override: found = False
    else: found = exists_subsection(filepath, benefit)

    if not found:
        constituents_lst = []
        with open(f'database/articles/{entity}/medicine/benefits/constituents_list.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter="|")
            for line in reader:
                if line[1].lower().strip() == benefit.lower().strip():
                    constituents_lst.append(line[2].lower().strip())

        constituents = '- ' + '\n- '.join(constituents_lst)

        prompt = f'''
            For each constituent in the following list:
            {constituents}

            Write 1 short sentence explaining why that constituent in {common_name} {benefit}.
        '''

        reply = gen_reply(prompt)

        lines = reply.split('\n')
        constituents_list = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line[0].isdigit(): line = ' '.join(line.split(' ')[1:])
            if line != '': constituents_list.append(line)
        reply = '. '.join(constituents_list)
        reply = reply.replace('"', '')
        reply = re.sub("\s\s+" , " ", reply)
        reply = reply.strip()
        
        if sys_override:
            csv_update_override_cell(filepath, entity, benefit, reply)
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerow([entity, benefit, reply])


def gen_medicine_benefit_conditions_list(entity, common_name, benefit):
    folderpath = f'database/articles/{entity}/medicine/benefits'
    filepath = f'database/articles/{entity}/medicine/benefits/conditions_list.csv'

    create_folder(folderpath)
    if sys_override: found = False
    else: found = exists_subsection(filepath, benefit)

    if not found:
        prompt = f'''
            {SYSTEM_PROMPT_LIST}
            {common_name}'s benefit: {benefit}.
            Write the 7 most important health conditions helped by this benefit.
            Give me just the names of the conditions. Don't add descriptions.
        '''

        reply = gen_reply(prompt)

        lines = reply.split('\n')
        lst = []
        for line in lines:
            formatted_line = ''
            line = line.strip()
            if line == '': continue
            if line[0].isdigit(): formatted_line = ' '.join(line.split(' ')[1:])
            if formatted_line != '': lst.append(formatted_line)

        if sys_override:
            filtered_rows = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[1].lower().strip() != benefit.lower().strip():
                        filtered_rows.append(line)
                        
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerows(filtered_rows)
                        
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for item in lst:
                    writer.writerow([entity, benefit, item])
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for item in lst:
                    writer.writerow([entity, benefit, item])


def gen_medicine_benefit_conditions_text(entity, common_name, benefit):
    folderpath = f'database/articles/{entity}/medicine/benefits'
    filepath = f'database/articles/{entity}/medicine/benefits/conditions_text.csv'

    create_folder(folderpath)
    if sys_override: found = False
    else: found = exists_subsection(filepath, benefit)

    if not found:
        lst = []
        with open(f'database/articles/{entity}/medicine/benefits/conditions_list.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter="|")
            for line in reader:
                if line[1].lower().strip() == benefit.lower().strip():
                    lst.append(line[2].lower().strip())

        lst = '- ' + '\n- '.join(lst)

        prompt = f'''
            Knowing that {common_name} {benefit.lower()}, explain in 100 words why this benefit helps the following health conditions: {lst}.
            Don't write lists.
            Start with these words: {common_name.title()}'s ability to 
        '''

        reply = gen_reply(prompt)

        lines = reply.split('\n')
        constituents_list = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line[0].isdigit(): line = ' '.join(line.split(' ')[1:])
            if line != '': constituents_list.append(line)
        reply = '. '.join(constituents_list)
        reply = reply.replace('"', '')
        reply = re.sub("\s\s+" , " ", reply)
        reply = reply.strip()
        
        if sys_override:
            csv_update_override_cell(filepath, entity, benefit, reply)
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerow([entity, benefit, reply])


def write_plant_medicine_benefits():
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:num_articles+1]):
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        create_folder(f'database/articles/{entity}/medicine/benefits')

        # TODO: find a way to change path to >> f'database/tables/medicine/benefits.csv',
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        benefits = [f'{x[1]}' for x in rows[:10]]

        for benefit in benefits:
            print(f'{i}/{num_articles} - {entity}')
            gen_medicine_benefit_definition(entity, common_name, benefit)
            print(f'{i}/{num_articles} - {entity}')
            gen_medicine_benefit_constituents_list(entity, common_name, benefit)
            print(f'{i}/{num_articles} - {entity}')
            gen_medicine_benefit_constituents_text(entity, common_name, benefit)
            print(f'{i}/{num_articles} - {entity}')
            gen_medicine_benefit_conditions_list(entity, common_name, benefit)
            print(f'{i}/{num_articles} - {entity}')
            gen_medicine_benefit_conditions_text(entity, common_name, benefit)




# ################################################################
# MEDICINE >> PREPARATIONS
# ################################################################

def gen_medicine_preparation_definition(entity, common_name, item):
    folderpath = f'database/articles/{entity}/medicine/preparations'
    filepath = f'database/articles/{entity}/medicine/preparations/definitions.csv'

    create_folder(folderpath)
    if sys_override: found = False
    else: found = exists_subsection(filepath, item)

    if not found:
        starting_text = f'{common_name.title()} {item.title()} is '
        prompt = f'''
            Write 1 sentece to define in detail what "{common_name} {item}" is. 
            Start the sentence with these words: {starting_text}
        '''

        reply = gen_reply(prompt)

        reply = reply.strip()
        reply = reply.split('.')[0] + '.'
        reply = reply.replace('"', '')
        if not reply[0].isupper():
            reply = starting_text + reply


        if sys_override:
            with open(filepath, 'a', newline='', encoding='utf-8') as f: pass
            csv_update_override_cell(filepath, entity, item, reply)
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerow([entity, item, reply])


def gen_medicine_preparations_conditions_list(entity, common_name, item):
    filepath = f'database/articles/{entity}/medicine/preparations/conditions_list.csv'

    if sys_override: found = False
    else: found = exists_subsection(filepath, item)

    if not found:
        prompt = f'''
            Write a numbered list of the most important conditions that {common_name} {item} helps to heal. 
            Write one condition per line.
            Give me just the names of the conditions. Don't add descriptions.
        '''

        reply = gen_reply(prompt)

        lines = reply.split('\n')
        constituents_list = []
        for line in lines:
            formatted_line = ''
            line = line.strip()
            if line == '': continue
            if line[0].isdigit(): formatted_line = ' '.join(line.split(' ')[1:])
            if formatted_line != '': constituents_list.append(formatted_line)

        if sys_override:
            filtered_rows = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[1].lower().strip() != item.lower().strip():
                        filtered_rows.append(line)
                        
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerows(filtered_rows)
                        
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for constituent in constituents_list:
                    writer.writerow([entity, item, constituent])
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for constituent in constituents_list:
                    writer.writerow([entity, item, constituent])


def gen_medicine_preparations_conditions_text(entity, common_name, item):
    filepath = f'database/articles/{entity}/medicine/preparations/conditions_text.csv'

    if sys_override: found = False
    else: found = exists_subsection(filepath, item)

    if not found:
        conditions_lst = []
        with open(f'database/articles/{entity}/medicine/preparations/conditions_list.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter="|")
            for line in reader:
                if line[1].lower().strip() == item.lower().strip():
                    conditions_lst.append(line[2].lower().strip())

        conditions = '- ' + '\n- '.join(conditions_lst)

        starting_text = f'{common_name.title()} {item.title()} helps '
        prompt = f'''
            Write 200 words explainin why {common_name} {item} helps the following conditions:
            {conditions}

            Start with the following words: {starting_text}

        '''
        # f'{common_name.title()} {item.title()} is used '

        reply = gen_reply(prompt)

        lines = reply.split('\n')
        conditions_list = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line[0].isdigit(): line = ' '.join(line.split(' ')[1:])
            if line != '': conditions_list.append(line)
        reply = '. '.join(conditions_list)
        reply = reply.replace('"', '')
        reply = re.sub("\s\s+" , " ", reply)
        reply = reply.strip()
        if not reply[0].isupper():
            reply = starting_text + reply
        
        if sys_override:
            csv_update_override_cell(filepath, entity, item, reply)
        else:
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                writer.writerow([entity, item, reply])


def write_plant_medicine_preparations():
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:num_articles+1]):
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        create_folder(f'database/articles/{entity}/medicine/preparations')

        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/preparations.csv', entity)
        items = [f'{x[1]}' for x in rows[:10]]

        for item in items:
            print(f'{i}/{num_articles} - {entity}')
            gen_medicine_preparation_definition(entity, common_name, item)
            print(f'{i}/{num_articles} - {entity}')
            gen_medicine_preparations_conditions_list(entity, common_name, item)
            print(f'{i}/{num_articles} - {entity}')
            gen_medicine_preparations_conditions_text(entity, common_name, item)


# ################################################################
# MAIN
# ################################################################

# for i, plant in enumerate(plants[1:num_articles+1]):
for i, plant in enumerate(plants[8:9+1]):
    entity = plant[0]
    common_name = plant[1]
    # print(f'{i+1}/{num_articles} - {entity}')
    # gen_plant_medicine_constituents(plant)

    # print(f'{i+1}/{num_articles} - {entity}')
    # # TODO: remove plant names in preparations
    # gen_plant_medicine_preparations(plant)

    # print(f'{i+1}/{num_articles} - {entity}')
    # gen_plant_medicine_side_effects(plant)

    # print(f'{i+1}/{num_articles} - {entity}')
    # gen_plant_medicine_precautions(plant)

    # gen_root_medicine_benefits_text(entity, common_name)
    # gen_root_medicine_constituents_text(entity, common_name, override=True)
    # gen_root_medicine_preparations_text(entity, common_name, override=True)
    # gen_root_medicine_side_effects_text(entity, common_name, override=True)
    # gen_root_medicine_precautions_text(entity, common_name, override=True)

    gen_root_medicine(entity, common_name)

    # quit()

# write_plant_medicine()
# write_plant_medicine_benefits()
# write_plant_medicine_preparations()
        

