import csv
import os
import re
from ctransformers import AutoModelForCausalLM


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
llm = AutoModelForCausalLM.from_pretrained("C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-1.Q8_0.gguf", model_type="mistral", context_length=1024, max_new_tokens=1024)

num_articles = 20


def write_section(section):
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:num_articles+1]):
        print(f'{i+1}')
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        try: os.makedirs(f'database')
        except: pass
        try: os.makedirs(f'database/articles')
        except: pass
        try: os.makedirs(f'database/articles/{entity}')
        except: pass

        try:
            with open(f'database/articles/{entity}/{section}.md', 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            content = ''
        if content.strip() != '': continue
        
        if section == 'intro':
            prompt = f'''
                Act as an expert botanist. Write 3 paragraphs in less than 200 words about {common_name} ({latin_name}).
                In paragraph 1, write about the medicinal and culinary aspects of this plant. Also, start paragraph 1 with the following words: "{common_name}, scientifically know as {latin_name}, is ".
                In paragraph 2, write about the horticultural and ornamental aspects of this plant.
                In paragraph 3, write about the botanical and historical aspects of this plant.
                Don't add final conclusions or summaries.
            '''
        elif section == 'medicine':
            prompt = f'''
                Act as an expert doctor. Write 5 paragraphs about the medicinal aspect {common_name} ({latin_name}).
                In paragraph 1, write about the health benefits and health conditions this plant helps (don't mention constituents in this paragraph).
                In paragraph 2, write about the medicinal constituents.
                In paragraph 3, write about the most used parts and medicinal preparations.
                In paragraph 4, write about the possible side effects.
                In paragraph 5, write about the precautions.
                Include as much data as possible in as few words as possible.
                Include only proven data.
                Don't write lists.
            '''
        elif section == 'cuisine':
            prompt = f'''
                Act as an expert chef. Write 5 paragraphs about the culinary aspect of {common_name} ({latin_name}).
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
                Act as an expert gardener. Write 3 paragraphs about the horticultural aspect of {common_name} ({latin_name}).
                In paragraph 1, write about how to grow this plant.
                In paragraph 2, write about the ideal growing conditions.
                In paragraph 3, write about the maintenance.
                Include as much data as possible in as few words as possible.
                Use the metric system.
                Don't write lists.
            '''
        elif section == 'botany':
            prompt = f'''
                Act as an expert botanist. Write 5 paragraphs about the botanical aspect of {common_name} ({latin_name}).
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
                Act as an expert historian. Write 3 paragraphs about the historical aspect of {common_name} ({latin_name}).
                In paragraph 1, write about the traditional medicine.
                In paragraph 2, write about the uses in divination.
                In paragraph 3, write about the legends.
                Include as much data as possible in as few words as possible.
                Don't write lists.
            '''
        

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
            lines_formatted.append(line)
        
        reply = '\n\n'.join(lines_formatted)

        with open(f'database/articles/{entity}/{section}.md', 'w', newline='', encoding='utf-8') as f:
            f.write(reply)


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
        # print()

        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        # skip if entity list already found
        tmp_rows = csv_get_rows(f'database/tables/{section}.csv')
        tmp_entities = [tmp_row[0] for tmp_row in tmp_rows]
        if entity in tmp_entities: continue 

        if section == 'benefits':
            prompt = f"""
                Write a numbered list of the 10 most important health benefits of {common_name} ({latin_name}).
                Start each health benefit with a third-person singular verb.
                Write only the health benefits, don't add descriptions.
                Write each health benefit in less than 5 words.
                Write each health benefit in a new line.
            """
        elif section == 'cuisine':
            prompt = f"""
                Write a numbered list of 10 culinary uses of {common_name} ({latin_name}).
                Give me only the 10 list items, nothing else.
                Start each culinary uses with a verb.
                Each list item must be less than 5 words.
                Write each list item in a new line.
                Don't mention health uses.
            """
        elif section == 'horticulture':
            prompt = f"""
                Write a numbered list of 10 tips for growing {common_name} ({latin_name}).
                Start each list item with a second-person singular verb.
                Write each list item using less than 5 words.
                Write each list item in a new line.
            """
        elif section == 'botany':
            prompt = f"""
                Write a numbered list of 10 morphological characteristics of {common_name} ({latin_name}).
                Give me only the 10 list items, don't add descriptions.
                Write each list item using less than 5 words.
                Write each list item in a new line.
            """
        elif section == 'history':
            prompt = f"""
                Write a numbered list of 10 historical uses of {common_name} ({latin_name}).
                Give me only the 10 list items, don't add descriptions.
                Each list item must be less than 5 words.
                Write each list item in a new line.
            """
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


write_list('medicine')
write_list('cuisine')
write_list('horticulture')
write_list('botany')
write_list('history')
