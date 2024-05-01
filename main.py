import os
import time
import shutil
import markdown

import g
import util
import utils_ai

problems_rows = util.csv_get_rows(g.CSV_PROBLEMS_FILEPATH)
problems_cols = util.csv_get_cols(problems_rows)
problems_rows = problems_rows[1:]

conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
conditions_cols = util.csv_get_cols(conditions_rows)
conditions_rows = conditions_rows[1:]

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]

herbs_rows = util.csv_get_rows(g.CSV_HERBS_FILEPATH)
herbs_cols = util.csv_get_cols(herbs_rows)
herbs_rows = herbs_rows[1:]

preparations_rows = util.csv_get_rows(g.CSV_PREPARATIONS_FILEPATH)
preparations_cols = util.csv_get_cols(preparations_rows)
preparations_rows = preparations_rows[1:]

# JUNCTIONS
problems_herbs_rows = util.csv_get_rows(g.CSV_PROBLEMS_HERBS_FILEPATH)
problems_herbs_cols = util.csv_get_cols(problems_herbs_rows)
problems_herbs_rows = problems_herbs_rows[1:]

problems_systems_rows = util.csv_get_rows(g.CSV_PROBLEMS_SYSTEMS_FILEPATH)
problems_systems_cols = util.csv_get_cols(problems_systems_rows)
problems_systems_rows = problems_systems_rows[1:]

problems_preparations_rows = util.csv_get_rows(g.CSV_PROBLEMS_PREPARATIONS_FILEPATH)
problems_preparations_cols = util.csv_get_cols(problems_preparations_rows)
problems_preparations_rows = problems_preparations_rows[1:]





# #########################################################
# CSVs
# #########################################################

def gen_csvs(id):
    for problem_row in problems_rows:
        problem_id = problem_row[problems_cols['problem_id']].strip().lower()
        problem_slug = problem_row[problems_cols['problem_slug']].strip().lower()
        problem_names = problem_row[problems_cols['problem_names']]
        problem_name = problem_names.split(',')[0].strip().lower()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        if problem_id != f'{id}': continue

        # herbs
        problems_herbs_rows = util.csv_get_rows_filtered(
            g.CSV_PROBLEMS_HERBS_FILEPATH, problems_herbs_cols['problem_id'], problem_id
        )

        if problems_herbs_rows == []:
            prompt = f'''
                Write a numbered list of 20 medicinal herbs for {problem_name}.
                Write only the names of the herbs, not the descriptions.
                Don't write the parts of the herbs.
            '''
            reply = utils_ai.gen_reply(prompt)

            lines = []
            for line in reply.split('\n'):
                line = line.strip().lower()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '.' not in line: continue
                line = '.'.join(line.split('.')[1:])
                line = line.strip()
                if line == '': continue

                herbs_rows_filtered = util.csv_get_rows_filtered(
                    g.CSV_HERBS_FILEPATH, herbs_cols['herb_name_common'], line
                )
                if herbs_rows_filtered != []:
                    herb_row = herbs_rows_filtered[0]
                    herb_id = herb_row[herbs_cols['herb_id']]
                else:
                    herb_id = ''

                lines.append([problem_id, problem_slug, herb_id, line])

            if len(lines) >= 10:
                print('***************************************************')
                print(lines)
                print('***************************************************')
                util.csv_add_rows(g.CSV_PROBLEMS_HERBS_FILEPATH, lines)

            print(problem_id, problem_slug, problem_name)
            time.sleep(g.PROMPT_DELAY_TIME)

        # preparations
        problems_preparations_rows = util.csv_get_rows_filtered(
            g.CSV_PROBLEMS_PREPARATIONS_FILEPATH, problems_preparations_cols['problem_id'], problem_id
        )

        if problems_preparations_rows == []:
            prompt = f'''
                Write a numbered list of the 10 most effective type of herbal preparations for {problem_name}.
                Write only the names of the types of the preparations, not the descriptions.
                Write only the names of the types of the preparations, not the herbs names.
                Example of types of preparations can be infusions and tinctures.
            '''
            reply = utils_ai.gen_reply(prompt)

            lines = []
            for line in reply.split('\n'):
                line = line.strip().lower()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '.' not in line: continue
                line = '.'.join(line.split('.')[1:])
                line = line.strip()
                if line == '': continue

                preparations_rows_filtered = util.csv_get_rows_filtered(
                    g.CSV_PREPARATIONS_FILEPATH, preparations_cols['preparation_name'], line
                )
                if preparations_rows_filtered != []:
                    preparation_row = preparations_rows_filtered[0]
                    preparation_id = preparation_row[preparations_cols['preparation_id']]
                else:
                    preparation_id = ''

                lines.append([problem_id, problem_slug, preparation_id, line])

            if len(lines) >= 10:
                print('***************************************************')
                print(lines)
                print('***************************************************')
                util.csv_add_rows(g.CSV_PROBLEMS_PREPARATIONS_FILEPATH, lines)

            time.sleep(g.PROMPT_DELAY_TIME)




# #########################################################
# ARTICLES - PROBLEMS
# #########################################################

def csv_get_herbs_by_problem(problem_id):
    problems_herbs_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_HERBS_FILEPATH, problems_herbs_cols['problem_id'], problem_id,
    )

    problems_herbs_ids = [
        row[problems_herbs_cols['herb_id']] 
        for row in problems_herbs_rows_filtered
        if row[problems_herbs_cols['problem_id']] == problem_id
    ]

    herbs_rows_filtered = []
    for herb_row in herbs_rows:
        herb_id = herb_row[herbs_cols['herb_id']]
        if herb_id in problems_herbs_ids:
            herbs_rows_filtered.append(herb_row)
            
    return herbs_rows_filtered


def csv_get_preparations_by_problem(problem_id):
    problems_preparations_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_PREPARATIONS_FILEPATH, problems_preparations_cols['problem_id'], problem_id,
    )

    problems_preparations_ids = [
        row[problems_preparations_cols['preparation_id']] 
        for row in problems_preparations_rows_filtered
        if row[problems_preparations_cols['problem_id']] == problem_id
    ]

    preparations_rows_filtered = []
    for herb_row in preparations_rows:
        herb_id = herb_row[preparations_cols['preparation_id']]
        if herb_id in problems_preparations_ids:
            preparations_rows_filtered.append(herb_row)
            
    return preparations_rows_filtered





def art_problems_intro(json_filepath, data):
    key = 'intro'
    if key not in data:
        problem_name = data['problem_name']
        prompt = f'''
            Write 1 paragraph about the best herbal teas for {problem_name}.
            Include a brief definition of: {problem_name}.
            Include the negative impacts of {problem_name} in people lives. 
            Include the causes of {problem_name}. 
            Include the medicinal herbs and they preparations for {problem_name}. 
            Include the precautions when using herbs medicinally for {problem_name}. 
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)
        reply = utils_ai.reply_to_paragraphs(reply)
        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply[0]
            util.json_write(json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)


def art_problems_definition(json_filepath, data):
    key = 'definition'
    if key not in data:
        problem_name = data['problem_name']
        prompt = f'''
            Write 1 paragraph explaining what is {problem_name} and include many examples on how it affects negatively your life.
            Don't mention the casuses of {problem_name}.
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)
        reply = utils_ai.reply_to_paragraphs(reply)
        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply[0]
            util.json_write(json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)


def art_problems_causes(json_filepath, data):
    key = 'causes_desc'
    if key not in data:
        problem_name = data['problem_name']
        prompt = f'''
            Write 1 paragraph explaining what are the main causes of {problem_name}.
            Start the reply with the following words: The main causes of {problem_name} are .
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line[0].isdigit(): continue
            if ':' in line: continue
            lines_formatted.append(line)

        if len(lines_formatted) == 1:
            print('***************************************')
            print(lines_formatted[0])
            print('***************************************')
            data[key] = lines_formatted[0]
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)
        
    causes_num = 10
    key = 'causes_list'
    if key not in data:
        problem_name = data['problem_name']

        prompt = f'''
            Write a numbered list of the most common causes of {problem_name}.
            Include a short description for each cause.
            Reply with the following format: [cause name]: [description].
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            line = line.replace('*', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            if not line[0].isdigit(): continue
            if '.' not in line: continue
            if ':' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)

        if len(lines_formatted) == causes_num:
            print('***************************************')
            print(lines_formatted)
            print('***************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def art_problems_herbs(json_filepath, data):
    herbs_num = 10

    key = 'herbs_desc'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

        herbs_rows_filtered = csv_get_herbs_by_problem(problem_id)
        herbs_common_names = [row[herbs_cols['herb_name_common']] for row in herbs_rows_filtered]
        herbs_common_names_prompt = ', '.join(herbs_common_names[:5])

        prompt = f'''
            Write 1 paragraph explaining what medicinal herbs helps with {problem_name} and why.
            Include some of the following herbs: {herbs_common_names_prompt}.
            Start the reply with the following words: The best medicinal herbs for {problem_name} are .
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)
        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line[0].isdigit(): continue
            if ':' in line: continue
            lines_formatted.append(line)

        if len(lines_formatted) == 1:
            print('***************************************')
            print(lines_formatted[0])
            print('***************************************')
            data[key] = lines_formatted[0]
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)

    key = 'herbs_list'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

        herbs_rows_filtered = csv_get_herbs_by_problem(problem_id)
        herbs_common_names = [row[herbs_cols['herb_name_common']] for row in herbs_rows_filtered]
        herbs_common_names_prompt = ''
        for i, herb_common_name in enumerate(herbs_common_names[:herbs_num]):
            herbs_common_names_prompt += f'{i+1}. {herb_common_name.capitalize()}\n'

        prompt = f'''
            Here is a list of medicinal herbs for {problem_name}:
            {herbs_common_names_prompt}

            For each medicinal herb in the list above, explain in 1 sentence why that herb helps with {problem_name}.
            Reply with a numbered list using the following format: [herb name]: [description].
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            line = line.replace('*', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            if not line[0].isdigit(): continue
            if '.' not in line: continue
            if ':' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)

        if len(lines_formatted) == herbs_num:
            print('***************************************')
            print(lines_formatted)
            print('***************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def art_problems_preparations(json_filepath, data):
    key = 'preparations_desc'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

        preparations_rows_filtered = csv_get_preparations_by_problem(problem_id)
        preparations_names = [row[preparations_cols['preparation_name']] for row in preparations_rows_filtered]
        preparations_names_prompt = ', '.join(preparations_names[:5])

        prompt = f'''
            Write 1 paragraph about the what are the best types of herbal preparations for {problem_name}.
            Include the following types of herbal preparations: {preparations_names_prompt}.
            Explain why each preparation helps with {problem_name}.
            Don't include names of herbs.
            Don't include definitions for the preparations.
            Don't include how to make the preparations.
            Start the reply with the following words: The most effective herbal preparations for {problem_name} are .
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if line[0].isdigit(): continue
            if ':' in line: continue
            lines_formatted.append(line)

        if len(lines_formatted) == 1:
            print('***************************************')
            print(lines_formatted[0])
            print('***************************************')
            data[key] = lines_formatted[0]
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)

    key = 'preparations_list'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

        preparations_rows_filtered = csv_get_preparations_by_problem(problem_id)
        preparations_names = [row[preparations_cols['preparation_name']] for row in preparations_rows_filtered]
        preparations_names_prompt = ''
        for i, preparation_name in enumerate(preparations_names[:10]):
            preparations_names_prompt += f'{i+1}. {preparation_name.capitalize()}\n'

        prompt = f'''
            Here is a list of the types of herbal preparations for {problem_name}:
            {preparations_names_prompt}

            For each type of herbal preparation in the list above, explain in 1 detailed sentence how and why that preparation helps with {problem_name}.
            Don't include names of herbs.
            Don't include definitions for the preparations.
            Don't explain the making process of the preparations.
            Reply with a numbered list using the following format: [preparation name]: [description].
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            line = line.replace('*', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            if not line[0].isdigit(): continue
            if '.' not in line: continue
            if ':' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)

        if len(lines_formatted) >= 4:
            print('***************************************')
            print(lines_formatted)
            print('***************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def art_problems_precautions(json_filepath, data):
    key = 'precautions_desc'
    if key not in data:
        problem_name = data['problem_name']
        prompt = f'''
            Write 1 paragraph about the precautions to take when using herbal remedies for {problem_name}.
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)
        reply = utils_ai.reply_to_paragraphs(reply)
        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply[0]
            util.json_write(json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)

    key = 'precautions_list'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

        prompt = f'''
            Write a numbered list of precautions to take when using herbal remedies for {problem_name}.
            Start each precaution with an action verb.
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            line = line.replace('*', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            if not line[0].isdigit(): continue
            if '.' not in line: continue
            if ':' in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)

        if len(lines_formatted) >= 4:
            print('***************************************')
            print(lines_formatted)
            print('***************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)
        

def art_problems_other_remedies(json_filepath, data):
    key = 'other_remedies_desc'
    if key not in data:
        problem_name = data['problem_name']
        prompt = f'''
            Write 1 paragraph about the natural remedies for {problem_name}, without including herbal remedies.
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)
        reply = utils_ai.reply_to_paragraphs(reply)
        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply[0]
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)

    items_num = 10
    key = 'other_remedies_list'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

        prompt = f'''
            Write a numbered list of the {items_num} most effective natural remedies for {problem_name}, without including herbal remedies.
            Start each natural remedy with an action verb.
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)

        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            line = line.replace('*', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            if not line[0].isdigit(): continue
            if '.' not in line: continue
            if ':' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)

        if len(lines_formatted) == items_num:
            print('***************************************')
            print(lines_formatted)
            print('***************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def art_problems():
    for problem_row in problems_rows:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        print(f'>> {problem_id} - {problem_name}')
        
        problem_system_row = util.csv_get_rows_filtered(
            g.CSV_PROBLEMS_SYSTEMS_FILEPATH, 
            problems_systems_cols['problem_id'], 
            problem_id
        )[0]

        system_row = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_NEW_FILEPATH, 
            systems_cols['system_id'], 
            problem_system_row[problems_systems_cols['system_id']]
        )[0]

        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        print(f'    {system_id} - {system_name}')



        # json
        json_filepath = f'database/json/problems/{system_slug}/{problem_slug}.json'

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)

        data['problem_id'] = problem_id
        data['problem_slug'] = problem_slug
        data['problem_name'] = problem_name

        data['system_id'] = system_id
        data['system_slug'] = system_slug
        data['system_name'] = system_name

        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 

        title = f'What to know about {problem_name} before treating it with medicinal herbs'
        data['title'] = title

        util.json_write(json_filepath, data)



        # sections
        art_problems_intro(json_filepath, data)
        art_problems_definition(json_filepath, data)
        art_problems_causes(json_filepath, data)
        art_problems_herbs(json_filepath, data)

        art_problems_preparations(json_filepath, data)
        art_problems_precautions(json_filepath, data)
        art_problems_other_remedies(json_filepath, data)



        # html
        html_filepath = f'website/ailments/{system_slug}/{problem_slug}.html'

        data = util.json_read(json_filepath)

        article_html = ''
        article_html += f'<h1>{title}</h1>\n'
        article_html += f'{util.text_format_1N1_html(data["intro"])}\n'
        article_html += f'<p>This article explains in detail what is {problem_name}, how it affects your life and what are its causes. Then, it lists what medicinal herbs to use to relieve this problem and how to prepare these herbs to get the best results. Lastly, it revals what other natural remedies to use in conjunction with herbal medicine to aid with this problem.</p>\n'

        article_html += f'<h2>What is {problem_name} and how it affects your life?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["definition"])}\n'
        
        article_html += f'<h2>What are the main causes of {problem_name}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["causes_desc"])}\n'
        article_html += f'<p>The most common causes of {problem_name} are listed below.</p>\n'
        article_html += f'<ul>\n'
        for item in data['causes_list']:
            chunks = item.split(':')
            chunk_1 = f'<strong>{chunks[0]}</strong>\n'
            chunk_2 = ':'.join(chunks[1:])
            article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
        article_html += f'</ul>\n'
        
        article_html += f'<h2>What are the best medicinal herbs for {problem_name}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["herbs_desc"])}\n'
        article_html += f'<p>The most effective medicinal herbs that help with {problem_name} are listed below.</p>\n'
        article_html += f'<ul>\n'
        for item in data['herbs_list']:
            chunks = item.split(':')
            chunk_1 = f'<strong>{chunks[0]}</strong>\n'
            chunk_2 = ':'.join(chunks[1:])
            article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
        article_html += f'</ul>\n'
        
        article_html += f'<h2>What are the most effective herbal preparations for {problem_name}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["preparations_desc"])}\n'
        article_html += f'<p>The most used herbal preparations that help with {problem_name} are listed below.</p>\n'
        article_html += f'<ul>\n'
        for item in data['preparations_list']:
            chunks = item.split(':')
            chunk_1 = chunks[0]
            chunk_2 = ':'.join(chunks[1:])
            if chunk_1.lower().strip() == 'infusion':
                chunk_1 = f'<strong><a href="/herbalism/tea/{system_slug}/{problem_slug}.html">{chunk_1}</a></strong>'
            else:
                chunk_1 = f'<strong>{chunk_1}</strong>'
            article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
        article_html += f'</ul>\n'


        article_html += f'<h2>What precautions to take when using herbal remedies for {problem_name}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["precautions_desc"])}\n'
        article_html += f'<p>The most important precautions to take when using herbal remedits for {problem_name} are listed below.</p>\n'
        article_html += f'<ul>\n'
        for item in data['precautions_list']:
            article_html += f'<li>{item}</li>\n'
        article_html += f'</ul>\n'

        article_html += f'<h2>What natural remedies to use with medicinal herbs for {problem_name}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["other_remedies_desc"])}\n'
        article_html += f'<p>The most effective natural remedies to use in conjunction with herbal medicine that help with {problem_name} are listed below.</p>\n'
        article_html += f'<ul>\n'
        for item in data['other_remedies_list']:
            chunks = item.split(':')
            chunk_1 = f'<strong>{chunks[0]}</strong>\n'
            chunk_2 = ':'.join(chunks[1:])
            article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
        article_html += f'</ul>\n'

        header_html = util.header_default()
        breadcrumbs_html = util.breadcrumbs(html_filepath)
        meta_html = util.article_meta(article_html, lastmod)
        article_html = util.article_toc(article_html)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                {breadcrumbs_html}
                
                <section class="article-section">
                    <div class="container">
                        {meta_html}
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''

        util.file_write(html_filepath, html)

        break





def art_systems():
    for system_row in systems_rows:
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue



        # json
        json_filepath = f'database/json/problems/{system_slug}.json'

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)

        data['system_id'] = system_id
        data['system_slug'] = system_slug
        data['system_name'] = system_name

        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 

        title = f'{system_name}'
        data['title'] = title

        util.json_write(json_filepath, data)



        # html
        html_filepath = f'website/ailments/{system_slug}.html'

        article_html = ''
        article_html += f'<h1>{system_name}</h1>\n'

        header_html = util.header_default()
        breadcrumbs_html = util.breadcrumbs(html_filepath)
        meta_html = util.article_meta(article_html, lastmod)
        article_html = util.article_toc(article_html)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                {breadcrumbs_html}
                
                <section class="article-section">
                    <div class="container">
                        {meta_html}
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''

        util.file_write(html_filepath, html)

        break


def art_ailments():
    title = 'What are the most common ailments and how to heal them with herbs'




# #########################################################
# PAGES
# #########################################################

def page_home():
    header = util.header_default()
    
    teas_articles_html = ''
    for condition_row in conditions_rows[:6]:
        condition_name = condition_row[conditions_cols['condition_names']].split(',')[0].strip().lower()
        condition_slug = condition_row[conditions_cols['condition_slugs_prev']].split(',')[0].strip().lower()

        if condition_name == '': continue

        condition_system_id = condition_row[conditions_cols['system_id']].split(',')[0].strip().lower()
        condition_system_slug = util.csv_get_rows_filtered(g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], condition_system_id)[0][systems_cols['system_slug']]

        imagepath = f'/images/herbal-tea-for-{condition_slug}-overview.jpg'
        teas_articles_html += f'''
            <a href="/herbalism/tea/{condition_system_slug}/{condition_slug}.html">
                <div class="card">
                    <img class="card-image"
                        src="{imagepath}" alt=""
                        width="400" height="300">
                    <h3 class="px-16 mt-16">10 Best Herbal Teas For {condition_name.title()}</h3>
                    <p class="px-16 mt-16">Boosts the immune system and fights infections.</p>
                </div>
            </a>
        '''

    

    slug = 'index'

    template = util.file_read(f'templates/{slug}.html')

    template = template.replace('[meta_title]', 'Herbalism & Natural Healing')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[teas_articles]', teas_articles_html)

    util.file_write(f'website/{slug}.html', template)
    
    
def page_start_here():
    slug = 'start-here'
    filepath_in = f'templates/{slug}.html'
    filepath_out = f'website/{slug}.html'

    header = util.header_default()
    breadcrumbs_html = util.breadcrumbs(filepath_out)

    template = util.file_read(filepath_in)
    template = template.replace('[title]', 'Start Your Herbalism Journey Here At TerraWhisper')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    util.file_write(filepath_out, template)


def page_about():
    page_url = 'about'
    article_filepath_out = f'website/{page_url}.html'

    header = util.header_default()
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)
    content = util.file_read(f'static/about.md')
    content = markdown.markdown(content, extensions=['markdown.extensions.tables'])
    
    template = util.file_read('templates/about.html')

    template = template.replace('[title]', 'TerraWhisper | About')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[content]', content)

    util.file_write(article_filepath_out, template)


def page_top_herbs():
    articles_folderpath = 'database/articles/plants'
    plants = util.csv_get_rows('database/tables/plants.csv')
    articles_html = ''

    plants_primary = []
    for plant in plants[1:]:
        latin_name = plant[0].strip().capitalize()
        entity = latin_name.lower().replace(' ', '-')
        filepath_in = f'{articles_folderpath}/{entity}.json'
        data = util.json_read(filepath_in)

        title = data['title']
        common_name = data['common_name']

        article_html = f'''
            <a href="/plants/{entity}.html">
                <div>
                    <img src="/images/{entity}-overview.jpg" alt="">
                    <h3 class="mt-0 mb-0">{latin_name} ({common_name})</h3>
                </div>
            </a>
        '''
        plants_primary.append(article_html)

    articles_html += '<div class="articles">' +'\n'.join(plants_primary) + '</div>'

    page_url = 'top-herbs'
    article_filepath_out = f'website/{page_url}.html'

    header = util.header_default()
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)

    template = util.file_read(f'templates/{page_url}.html')
    template = template.replace('[meta_title]', 'Herbs')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[articles]', articles_html)

    util.file_write(article_filepath_out, template)


def page_plants(regen_csv=False):
    json_filenames_plants_primary_secondary = [filename.lower().strip() for filename in os.listdir('database/articles/plants') if filename.endswith('.json')]
    # json_filenames_plants_treffle = [filename.lower().strip() for filename in os.listdir('database/articles/plants_trefle') if filename.endswith('.json')]
    
    json_filepaths_plants = [] 
    for filename in json_filenames_plants_primary_secondary: json_filepaths_plants.append(f'database/articles/plants/{filename}')
    # for filename in json_filenames_plants_treffle: json_filepaths_plants.append(f'database/articles/plants_trefle/{filename}')

    plants_list = []
    for filepath in json_filepaths_plants:
        filepath_in = f'{filepath}'
        data = util.json_read(filepath_in)
        plant_name = data['latin_name']
        plant_slug = data['entity']
        plants_list.append(f'<a href="/plants/{plant_slug}.html">{plant_name}</a>')

    plants_list = sorted(plants_list)
    plants_html = ''.join(plants_list)

    page_url = 'plants'
    article_filepath_out = f'website/{page_url}.html'
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)

    template = util.file_read(f'templates/{page_url}.html')
    template = template.replace('[title]', 'Plants')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', util.header_default())
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[plants_num]', str(len(json_filepaths_plants)))
    template = template.replace('[items]', plants_html)
    util.file_write(article_filepath_out, template)

    # GENERATE CSV TO DOWNLOAD
    if regen_csv:
        rows = []
        for filepath in json_filepaths_plants:
            slug = filepath.split('/')[-1].split('.')[0].strip().lower()
            rows.append([slug])

        csv_plants_primary = util.csv_get_rows('database/tables/plants.csv')
        csv_plants_secondary = util.csv_get_rows('database/tables/plants-secondary.csv')
        csv_plants_trefle = util.csv_get_rows('database/tables/plants/trefle.csv')

        csv_plants = [] 
        for row in csv_plants_primary: csv_plants.append(row)
        for row in csv_plants_secondary: csv_plants.append(row)
        for row in csv_plants_trefle: csv_plants.append(row)

        rows_final = [['slug', 'scientific_name', 'common_name', 'genus', 'family']]
        for row in rows:
            for csv_plant in csv_plants:
                if csv_plant[0].strip().lower() == row[0].strip().lower():
                    rows_final.append(csv_plant)
                    break

        util.csv_set_rows('website/plants.csv', rows_final, delimiter=',')




# #########################################################
# EXE
# #########################################################

# page_home()
# page_start_here()
# page_about()
# page_top_herbs()
# page_plants(regen_csv=False)

art_problems()
# art_systems()

# gen_csvs(2)


# shutil.copy2('style.css', 'website/style.css')
# shutil.copy2('util.css', 'website/util.css')
# shutil.copy2('assets/images/healing-herbs.jpg', 'website/images/healing-herbs.jpg')