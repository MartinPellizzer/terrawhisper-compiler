import csv
import os
import re
from ctransformers import AutoModelForCausalLM
import sys
import utils
import json

sys_override = False
try: 
    if sys.argv[1] == 'override': sys_override = True
except: pass


SYSTEM_PROMPT = 'You are an expert botanist. You explain things write short and simple sentences. You write short paragraphs and add a new line every 2-3 sentences. You never write lists.'
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



num_articles = 20



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



# ################################################################
# MEDICINE
# ################################################################

def write_plant_medicine():
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:num_articles+1]):
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        print(f'{i+1}/{num_articles} - {entity}')

        create_folder(f'database/articles/{entity}/medicine')

        rows = utils.csv_get_rows_by_entity(f'database/tables/benefits.csv', entity)
        benefits_lst = [f'{x[1]}' for x in rows[:10]]
        benefits = ', '.join(benefits_lst)

        # override content
        out_filepath = f'database/articles/{entity}/medicine/benefits.md'
        if sys_override: found = False
        else: found = exists_content(out_filepath)

        if not found:
            starting_text = f'{common_name} has many health benefits, such as '
            prompt = f'''
                {SYSTEM_PROMPT}
                Explain in 300 words these health benefits of {common_name}: {benefits}. 
                Start with these words: {starting_text}
            '''

            reply = gen_reply(prompt)
            reply = reply.strip()
            reply = starting_text + reply

            paragraphs = reply.split('\n')
            paragraphs_lst = []
            for paragraph in paragraphs:
                paragraph.strip()
                if paragraph == '': continue
                if paragraph.endswith(':'): continue
                if paragraph[0].isdigit(): paragraph = ' '.join(paragraph.split(' ')[1:])
                if ':' in paragraph: paragraph = paragraph.split(':')[1]
                paragraphs_lst.append(paragraph)

            content = '\n\n'.join(paragraphs_lst)
            
            if sys_override:
                with open(out_filepath, 'w', encoding='utf-8') as f: 
                    f.write(content)
            else: 
                with open(out_filepath, 'a', encoding='utf-8') as f: 
                    f.write(content)
        


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
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine.csv', entity)
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
# MAIN
# ################################################################

# write_plant_medicine_benefits()

write_plant_medicine()