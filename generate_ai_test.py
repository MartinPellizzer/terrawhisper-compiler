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


SYSTEM_PROMPT = 'You are an expert botanist who explains things using short and straightforward sentences, who never uses lists, and who separates paragraphs with a new line ever 2-3 sentences.'
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



num_articles = 30



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
    with open(filepath, 'a', newline='', encoding='utf-8') as csvfile: pass
    with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    
    if content.strip() == '': found = False
    else: found = True

    return found


def write_plant_medicine():
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:num_articles+1]):
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        create_folder(f'database/articles/{entity}/medicine')

        # TODO: find a way to change path to >> f'database/tables/medicine/benefits.csv',
        
        # benefits
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine.csv', entity)
        benefits_lst = [f'{x[1]}' for x in rows[:10]]
        benefits = ', '.join(benefits_lst)

        # override content
        filepath = f'database/articles/{entity}/medicine/benefits.md'
        if sys_override: found = False
        else: found = exists_content(filepath)

        if not found:
            prompt = f'''
                {SYSTEM_PROMPT}
                Explain in 300 words these health benefits of {common_name}: {benefits}. 
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
                with open(filepath, 'w', encoding='utf-8') as f: 
                    f.write(content)
            else: 
                with open(filepath, 'a', encoding='utf-8') as f: 
                    f.write(content)
        


# write_plant_medicine()



def write_plant_medicine_benefits():
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:num_articles+1]):
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        try: os.makedirs(f'database')
        except: pass
        try: os.makedirs(f'database/articles')
        except: pass
        try: os.makedirs(f'database/articles/{entity}')
        except: pass
        try: os.makedirs(f'database/articles/{entity}/medicine')
        except: pass
        try: os.makedirs(f'database/articles/{entity}/medicine/benefits')
        except: pass


        # TODO: find a way to change path to >> f'database/tables/medicine/benefits.csv',
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine.csv', entity)
        benefits = [f'{x[1]}' for x in rows[:10]]
        images_text = ''

        print(benefits)




        for i, benefit in enumerate(benefits):

            # definitions
            with open(f'database/articles/{entity}/medicine/benefits/definitions.csv', 'a', newline='', encoding='utf-8') as csvfile:
                pass

            found = False
            with open(f'database/articles/{entity}/medicine/benefits/definitions.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[1].lower().strip() == benefit.lower().strip():
                        print(line)
                        found = True
                        break

            if not found:
                prompt = f'''
                    {SYSTEM_PROMPT}
                    Define in detail in 1 sentence what "{common_name} {benefit}" means. 
                    Start the sentence with these words: "{common_name.title()}'s ability to {benefit.lower()} refers to ".
                    Fix grammatical errors.
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

                reply = reply.split('.')[0] + '.'
                reply = reply.replace('"', '')
                reply = reply.strip()
                with open(f'database/articles/{entity}/medicine/benefits/definitions.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter='|')
                    writer.writerow([entity, benefit, reply])




            # constituents_list
            with open(f'database/articles/{entity}/medicine/benefits/constituents_list.csv', 'a', newline='', encoding='utf-8') as csvfile:
                pass

            found = False
            with open(f'database/articles/{entity}/medicine/benefits/constituents_list.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    print(line)
                    if line[1].lower().strip() == benefit.lower().strip():
                        found = True
                        break

            if not found:
                prompt = f'''
                    {SYSTEM_PROMPT_LIST}
                    Write the 7 most important macro constituents of {common_name} that help with the following benefit: "{benefit}". 
                    Give me just the names of the constituents. Don't add descriptions.
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

                lines = reply.split('\n')
                constituents_list = []
                for line in lines:
                    formatted_line = ''
                    line = line.strip()
                    if line == '': continue
                    if line[0].isdigit(): formatted_line = ' '.join(line.split(' ')[1:])
                    if formatted_line != '': constituents_list.append(formatted_line)

                if len(constituents_list) >= 3:
                    with open(f'database/articles/{entity}/medicine/benefits/constituents_list.csv', 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile, delimiter='|')
                        for constituent in constituents_list:
                            writer.writerow([entity, benefit, constituent])





        # constituents_text
        for i, benefit in enumerate(benefits):
            with open(f'database/articles/{entity}/medicine/benefits/constituents_text.csv', 'a', newline='', encoding='utf-8') as csvfile:
                pass

            found = False
            with open(f'database/articles/{entity}/medicine/benefits/constituents_text.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[1].lower().strip() == benefit.lower().strip():
                        found = True
                        break

            if not found:
                # get constituent list
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

                lines = reply.split('\n')
                constituents_list = []
                for line in lines:
                    formatted_line = ''
                    line = line.strip()
                    if line == '': continue
                    if line[0].isdigit(): formatted_line = ' '.join(line.split(' ')[1:])
                    if formatted_line != '': constituents_list.append(formatted_line)

                reply = '. '.join(constituents_list)


                reply = reply.replace('"', '')
                reply = re.sub("\s\s+" , " ", reply)
                reply = reply.strip()
                with open(f'database/articles/{entity}/medicine/benefits/constituents_text.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter='|')
                    writer.writerow([entity, benefit, reply])
                




            # conditions_list
            with open(f'database/articles/{entity}/medicine/benefits/conditions_list.csv', 'a', newline='', encoding='utf-8') as csvfile:
                pass

            found = False
            with open(f'database/articles/{entity}/medicine/benefits/conditions_list.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[1].lower().strip() == benefit.lower().strip():
                        found = True
                        break

            if not found:
                prompt = f'''
                    {SYSTEM_PROMPT_LIST}
                    {common_name}'s benefit: {benefit}.
                    Write the 3-7 most important health conditions helped by this benefit.
                    Give me just the names of the conditions. Don't add descriptions.
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

                lines = reply.split('\n')
                constituents_list = []
                for line in lines:
                    formatted_line = ''
                    line = line.strip()
                    if line == '': continue
                    if line[0].isdigit(): formatted_line = ' '.join(line.split(' ')[1:])
                    if formatted_line != '': constituents_list.append(formatted_line)

                with open(f'database/articles/{entity}/medicine/benefits/conditions_list.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter='|')
                    for constituent in constituents_list[:7]:
                        writer.writerow([entity, benefit, constituent])




                        
        # conditions_text
        for i, benefit in enumerate(benefits):
            with open(f'database/articles/{entity}/medicine/benefits/conditions_text.csv', 'a', newline='', encoding='utf-8') as csvfile:
                pass

            found = False
            with open(f'database/articles/{entity}/medicine/benefits/conditions_text.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[1].lower().strip() == benefit.lower().strip():
                        found = True
                        break

            if not found:
                # get constituent list
                _lst = []
                with open(f'database/articles/{entity}/medicine/benefits/conditions_list.csv', 'r', encoding='utf-8') as f:
                    reader = csv.reader(f, delimiter="|")
                    for line in reader:
                        if line[1].lower().strip() == benefit.lower().strip():
                            _lst.append(line[2].lower().strip())

                # _lst = '- ' + '\n- '.join(_lst)
                _lst = ', '.join(_lst)

                prompt = f'''
                    Knowing that {common_name} {benefit.lower()}, explain in 100 words why this benefit helps the following health conditions: {_lst}.
                    Don't write lists.
                    Start with these words: {common_name.title()}'s ability to 
                '''
                # Start with these words: This benefit of {common_name} helps healing many conditions, such as

                # Start the paragraph with the following words: "The property of {common_name} to {benefit} helps you with many health conditions, such as ".

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

                reply = reply.replace('"', '')
                reply = re.sub("\s\s+" , " ", reply)
                reply = reply.strip()
                reply = f"{common_name.title()}'s ability to " + reply
                with open(f'database/articles/{entity}/medicine/benefits/conditions_text.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter='|')
                    writer.writerow([entity, benefit, reply])


write_plant_medicine_benefits()