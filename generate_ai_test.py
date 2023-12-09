import csv
import os
import re
from ctransformers import AutoModelForCausalLM
import sys
import utils
import json

sys_arg_override = False
try: 
    if sys.argv[1] == 'override': sys_arg_override = True
except: pass


SYSTEM_PROMPT = 'You are an expert botanist who explain things using simple, short, straightforward sentences and use correct grammar and puntuation.'
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



num_articles = 1



llm = AutoModelForCausalLM.from_pretrained(
    "C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-1.Q8_0.gguf", 
    model_type="mistral", 
    context_length=1024, 
    max_new_tokens=1024,
    )

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

        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        benefits = [f'{x[1]}' for x in rows[:10]]
        images_text = ''





        for i, benefit in enumerate(benefits):
            with open(f'database/articles/{entity}/medicine/benefits/definitions.csv', 'a', newline='', encoding='utf-8') as csvfile:
                pass

            found = False
            with open(f'database/articles/{entity}/medicine/benefits/definitions.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[1].lower().strip() == benefit.lower().strip():
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





            with open(f'database/articles/{entity}/medicine/benefits/constituents_list.csv', 'a', newline='', encoding='utf-8') as csvfile:
                pass

            found = False
            with open(f'database/articles/{entity}/medicine/benefits/constituents_list.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter="|")
                for line in reader:
                    if line[1].lower().strip() == benefit.lower().strip():
                        found = True
                        break

            if not found:
                prompt = f'''
                    {SYSTEM_PROMPT_LIST}
                    Write the 3-7 most important macro constituents of {common_name} that help with the following benefit: "{benefit}". 
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
                    if line[0].isdigit(): formatted_line = ' '.join(line.split(' ')[1:])
                    if formatted_line != '': constituents_list.append(formatted_line)

                with open(f'database/articles/{entity}/medicine/benefits/constituents_list.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter='|')
                    for constituent in constituents_list:
                        writer.writerow([entity, benefit, constituent])





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
                # print(constituents)
                # continue

                # prompt = f'''
                #     Write 100 words about what constituents in {common_name} {benefit} and explain why.
                #     Include these constituents: {constituents}.
                #     Write only 1 short sentence per constituent.
                # '''
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

                reply = reply.replace('"', '')
                reply = re.sub("\s\s+" , " ", reply)
                reply = reply.strip()
                with open(f'database/articles/{entity}/medicine/benefits/constituents_text.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter='|')
                    writer.writerow([entity, benefit, reply])
                




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
                    Start with these words: This benefit of {common_name} helps healing many conditions, such as
                '''
                #Start with these words: {common_name.title()}'s ability to 
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