import os
import time
import shutil
import markdown
import random

import g
import util
import utils_ai
import sitemap

ART_NUM = 1

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

problems_teas_rows = util.csv_get_rows(g.CSV_PROBLEMS_TEAS_FILEPATH)
problems_teas_cols = util.csv_get_cols(problems_teas_rows)
problems_teas_rows = problems_teas_rows[1:]

problems_related_rows = util.csv_get_rows(g.CSV_PROBLEMS_RELATED_FILEPATH)
problems_related_cols = util.csv_get_cols(problems_related_rows)
problems_related_rows = problems_related_rows[1:]


teas_num = 10


# #########################################################
# CSVs
# #########################################################

def csv_gen_teas_for_problem(problem_row):
    problem_id = problem_row[problems_cols['problem_id']]
    problem_slug = problem_row[problems_cols['problem_slug']]
    problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

    problems_teas_rows = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_TEAS_FILEPATH, problems_teas_cols['problem_id'], problem_id
    )

    if problems_teas_rows == []:
        teas_num = 15
        prompt = f'''
            Write a numbered list of the {teas_num} best herbal teas for {problem_name}.
            Order the herbs in the list by effectiveness in treating {problem_name}.
            Write only the names of the herbs, not the descriptions.
            Include only 1 herb name for each list item, without mentioning the herb part.
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
                g.CSV_HERBS_FILEPATH, herbs_cols['herb_name'], line
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

        time.sleep(g.PROMPT_DELAY_TIME)


def csv_gen_related_for_problem(problem_row):
    problem_id = problem_row[problems_cols['problem_id']]
    problem_slug = problem_row[problems_cols['problem_slug']]
    problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

    problems_related_rows = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_RELATED_FILEPATH, problems_related_cols['problem_id'], problem_id
    )

    if problems_related_rows == []:
        prompt = f'''
            Write a numbered list of the most common symptoms people may also experience when they have {problem_name}.
            Write only the names, not the descriptions.
            Use as few words as possible.
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

            problems_rows_filtered = []
            for problem_row in problems_rows:
                problem_names = problem_row[problems_cols['problem_names']].split(',')
                for problem_name in problem_names:
                    if problem_name.strip() == line.strip():
                        problems_rows_filtered.append(problem_row)

            if problems_rows_filtered != []:
                problem_row = problems_rows_filtered[0]
                related_id = problem_row[problems_cols['problem_id']]
            else:
                related_id = ''

            lines.append([problem_id, problem_slug, related_id, line])

        if len(lines) >= 10:
            print('***************************************************')
            print(lines)
            print('***************************************************')
            util.csv_add_rows(g.CSV_PROBLEMS_RELATED_FILEPATH, lines)

        time.sleep(g.PROMPT_DELAY_TIME)


def csv_gen_herbs_for_problem(problem_row):
    problem_id = problem_row[problems_cols['problem_id']]
    problem_slug = problem_row[problems_cols['problem_slug']]
    problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

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


def csv_gen_preparations_for_problem(problem_row):
    problem_id = problem_row[problems_cols['problem_id']]
    problem_slug = problem_row[problems_cols['problem_slug']]
    problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

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


def gen_csvs():
    for problem_row in problems_rows[:ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']].strip().lower()
        problem_slug = problem_row[problems_cols['problem_slug']].strip().lower()
        problem_names = problem_row[problems_cols['problem_names']]
        problem_name = problem_names.split(',')[0].strip().lower()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        print(f'> {problem_row}')

        # JSON
        csv_gen_teas_for_problem(problem_row)
        csv_gen_related_for_problem(problem_row)
        csv_gen_herbs_for_problem(problem_row)
        csv_gen_preparations_for_problem(problem_row)

        



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


def csv_get_teas_by_problem(problem_id):
    problems_teas_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_TEAS_FILEPATH, problems_teas_cols['problem_id'], problem_id,
    )

    herbs_rows_filtered = []
    for problem_tea_row in problems_teas_rows_filtered:
        jun_tea_id = problem_tea_row[problems_teas_cols['tea_id']]

        for herb_row in herbs_rows:
            herb_id = herb_row[herbs_cols['herb_id']]

            if herb_id == jun_tea_id:
                herbs_rows_filtered.append(herb_row)

            
    return herbs_rows_filtered


def csv_get_problems_by_system(system_id):
    problems_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_SYSTEMS_FILEPATH, problems_systems_cols['system_id'], system_id,
    )

    junction_problems_ids = [
        row[problems_systems_cols['problem_id']] 
        for row in problems_systems_rows_filtered
        if row[problems_systems_cols['system_id']] == system_id
    ]

    problems_rows_filtered = []
    for problem_row in problems_rows:
        problem_id = problem_row[problems_cols['problem_id']]
        if problem_id in junction_problems_ids:
            problems_rows_filtered.append(problem_row)
        
    return problems_rows_filtered


def csv_get_system_by_problem(problem_id):
    problems_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_SYSTEMS_FILEPATH, problems_systems_cols['problem_id'], problem_id,
    )
    problem_system_row = problems_systems_rows_filtered[0]
    system_id = problem_system_row[problems_systems_cols['system_id']]

    systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id,
    )
    system_row = systems_rows_filtered[0]

    return system_row


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



# #########################################################
# ARTICLES - PROBLEMS
# #########################################################




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
    for problem_row in problems_rows[:ART_NUM]:
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







# #########################################################
# AILMENTS
# #########################################################

def art_ailments_intro(json_filepath, data):
    key = 'intro_desc'
    if key not in data:
        prompt = f'''
            Write 1 intro paragraph for an article about ailments an healing herbs.
            Start by explaining what are the impacts of ailments on people lives.
            Then explain why healing herbs can help with the most common ailments. 
            Finally explain that the rest of the article will reveal the most common ailments for each body system and what are the best herbs to get rid of those ailments.
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


def art_ailments_definition(json_filepath, data):
    key = 'definition_desc'
    if key not in data:
        prompt = f'''
            Write 1 paragraph explaining what are ailments.
            Include a detailed definition of the word "ailments".
            Include an explanation on how ailments can affect your life.
            Include examples.
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


def art_ailments_systems(json_filepath, data):
    key = 'systems'
    if key not in data: data[key] = []
    for system_row in systems_rows:
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        found = False
        for system_obj in data[key]:
            if system_obj['system_id'] == system_id:
                found = True
                break
        
        if not found:
            data[key].append({'system_id': system_id, 'system_slug': system_slug, 'system_name': system_name})

    util.json_write(json_filepath, data)

    key = 'system_desc'
    for system_obj in data['systems']:
        if key not in system_obj:
            system_id = system_obj['system_id']
            system_name = system_obj['system_name']

            problems_rows_filtered = csv_get_problems_by_system(system_id)
            if len(problems_rows_filtered) > 0:
                problems_names = [row[problems_cols['problem_names']].split(',')[0].strip() for row in problems_rows_filtered]
                problems_names_prompt = ', '.join(problems_names)
                problems_names_prompt = f'Include the following common ailments: {problems_names_prompt}'
            else:
                problems_names_prompt = ''

            prompt = f'''
                Write 1 paragraph about the most common ailments of the {system_name} and how they affect your life.
                {problems_names_prompt}.
                Include what herbs and herbal remedies to use to help the {system_name}.
                Start the reply with the following words: The most common ailments of the {system_name} are .
                Never use the following words: can, may, might.
            '''
            reply = utils_ai.gen_reply(prompt)

            reply = utils_ai.reply_to_paragraphs(reply)

            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                system_obj[key] = reply[0]
                util.json_write(json_filepath, data)

            time.sleep(g.PROMPT_DELAY_TIME)


def art_ailments():
    json_filepath = f'database/json/ailments.json'

    util.create_folder_for_filepath(json_filepath)
    util.json_generate_if_not_exists(json_filepath)
    data = util.json_read(json_filepath)

    lastmod = util.date_now()
    if 'lastmod' not in data: data['lastmod'] = lastmod
    else: lastmod = data['lastmod'] 

    title = f'What are the most common ailments and how to cure them with medicinal herbs'
    data['title'] = title

    util.json_write(json_filepath, data)

    # json art sections
    art_ailments_intro(json_filepath, data)
    art_ailments_definition(json_filepath, data)
    art_ailments_systems(json_filepath, data)
    


    html_filepath = 'website/ailments.html'

    data = util.json_read(json_filepath)

    article_html = ''
    
    article_html += f'<h1>{title}</h1>\n'
    article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'

    article_html += f'<h2>What are ailments and how they affect your life?</h2>\n'
    article_html += f'{util.text_format_1N1_html(data["definition_desc"])}\n'

    for system_obj in data['systems']:
        system_id = system_obj['system_id']
        system_slug = system_obj['system_slug']
        system_name = system_obj['system_name']
        system_desc = system_obj['system_desc']

        article_html += f'<h2>{system_name.capitalize()} ailments</h2>\n'
        article_html += f'{util.text_format_1N1_html(system_desc)}\n'

        problems_rows_filtered = csv_get_problems_by_system(system_id)
        if len(problems_rows_filtered) > 0:
            article_html += f'The following link shows the <a href="/ailments/{system_slug}.html">most common ailments of the {system_name}</a> that you can alleviate with medicinal herbs.\n'

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
            <link rel="stylesheet" href="/util.css">
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

    
    

def art_systems_intro(json_filepath, data):
    key = 'intro_desc'
    if key not in data:
        system_name = data['system_name']
        prompt = f'''
            Write 1 intro paragraph for an article about {system_name} ailments an healing herbs.
            Start by explaining what are the impacts of the {system_name} ailments on people lives.
            Then explain why healing herbs can help with the most common {system_name} ailments. 
            Finally explain that the rest of the article will reveal the most common {system_name} ailments and what are the best herbs to get rid of those ailments.
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


def art_systems_definition(json_filepath, data):
    key = 'definition_desc'
    if key not in data:
        system_name = data['system_name']
        prompt = f'''
            Write 1 paragraph explaining what are {system_name} ailments.
            Include a detailed definition of "{system_name} ailments".
            Include an explanation on how {system_name} ailments can affect your life.
            Include examples of {system_name} ailments.
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


def art_systems_problems(json_filepath, data):
    key = 'problems'
    if key not in data: data[key] = []
    for problem_row in problems_rows:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        found = False
        for problem_obj in data[key]:
            if problem_obj['problem_id'] == problem_id:
                found = True
                break
        
        if not found:
            data[key].append({'problem_id': problem_id, 'problem_slug': problem_slug, 'problem_name': problem_name})

    util.json_write(json_filepath, data)
        
    key = 'problem_desc'
    for problem_obj in data['problems']:
        # if key in problem_obj: del problem_obj[key]
        if key not in problem_obj:
            problem_id = problem_obj['problem_id']
            problem_name = problem_obj['problem_name']

            prompt = f'''
                Write 1 paragraph about what is {problem_name}, how it affects your life, and what are the medicinal herbs for {problem_name}.
                Start the reply with the following words: {problem_name.capitalize()} is .
                Never use the words "can", "may", and "might".
            '''
            reply = utils_ai.gen_reply(prompt)

            reply = utils_ai.reply_to_paragraphs(reply)

            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                problem_obj[key] = reply[0]
                util.json_write(json_filepath, data)

            time.sleep(g.PROMPT_DELAY_TIME)


def art_systems():
    for system_row in systems_rows:
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        problems_rows_filtered = csv_get_problems_by_system(system_id)
        problems_num = len(problems_rows_filtered)

        if problems_num == 0: continue

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

        title = f'{problems_num} Most common {system_name} ailments and how to treat them with herbal medicine'
        data['title'] = title

        util.json_write(json_filepath, data)

        # ai
        art_systems_intro(json_filepath, data)
        art_systems_definition(json_filepath, data)
        art_systems_problems(json_filepath, data)

       

        # html
        html_filepath = f'website/ailments/{system_slug}.html'

        data = util.json_read(json_filepath)

        article_html = ''
        article_html += f'<h1>{title}</h1>\n'
        article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'

        for i, problem_obj in enumerate(data['problems']):
            problem_id = problem_obj['problem_id']
            problem_slug = problem_obj['problem_slug']
            problem_name = problem_obj['problem_name']
            problem_desc = problem_obj['problem_desc']

            problem_desc = problem_desc.replace(
                problem_name.capitalize(),
                f'<a href="/ailments/{system_slug}/{problem_slug}.html">{problem_name.capitalize()}</a>',
                1
            )

            article_html += f'<h2>{i+1}. {problem_name.capitalize()}</h2>\n'
            article_html += f'{util.text_format_1N1_html(problem_desc)}\n'


        article_html += f'<h2>What are {system_name} ailments and how they affect your life?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["definition_desc"])}\n'

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





# #########################################################
# TEAS
# #########################################################

def json_tea_systems_problems_intro(json_filepath, data):
    key = 'intro'
    # if key in data: del data[key]
    if key not in data:
        problem_id = data['problem_id']
        problem_slug = data['problem_slug']
        problem_name = data['problem_name']

        herbs_rows_filtered = csv_get_teas_by_problem(problem_id)[:teas_num]
        herbs_names = [row[herbs_cols['herb_name_common']] for row in herbs_rows_filtered]
        herbs_names_prompt = ', '.join(herbs_names)

        prompt = f'''
            Write 1 paragraph on the best herbal teas for {problem_name}.
            Write the names of the best herbal teas for {problem_name} that are {herbs_names_prompt}.
            Explain what are the primary properties of herbal teas that help with {problem_name}.
            Explain how herbal teas can improve the lives of people with {problem_name} and include examples.
            Start the reply with the following words: The best herbal teas for {problem_name} are .
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


def json_tea_systems_problems_list(json_filepath, data):
    problem_id = data['problem_id']
    problem_name = data['problem_name']
    problem_slug = data['problem_slug']
    teas_num = data['teas_num']

    herbs_rows_filtered = csv_get_teas_by_problem(problem_id)

    key = 'teas_list'
    if key not in data: data[key] = []
    for herb_row in herbs_rows_filtered:
        herb_id = herb_row[herbs_cols['herb_id']].strip()
        herb_slug = herb_row[herbs_cols['herb_slug']].strip()
        herb_name_common = herb_row[herbs_cols['herb_name_common']].strip()
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']].strip()

        if herb_id == '': continue
        if herb_slug == '': continue
        if herb_name_common == '': continue
        if herb_name_scientific == '': continue

        found = False
        for tea_obj in data[key]:
            if tea_obj['herb_id'] == herb_id: 
                found = True
                break

        if not found:
            data[key].append({
                'herb_id': herb_id,
                'herb_slug': herb_slug,
                'herb_name_common': herb_name_common,
                'herb_name_scientific': herb_name_scientific,
            })

    util.json_write(json_filepath, data)

    # # del old
    # data_filtered = []
    # for tea_obj in data['teas']: 
    #     found = False
    #     for tea_row in teas_rows[1:]:
    #         tea_condition_id = tea_row[teas_cols['condition_id']].strip().lower()
    #         tea_name = tea_row[teas_cols['tea_name']].strip().lower()
    #         if tea_condition_id != condition_id: continue
    #         if tea_obj['tea_name'] == tea_name: 
    #             found = True
    #             break
    #     if found:
    #         data_filtered.append(tea_obj)

    # data['teas'] = data_filtered
    # util.json_write(json_filepath, data)

    # AI
    for tea_obj in data['teas_list'][:teas_num]:
        tea_name = tea_obj["herb_name_common"].strip().lower()
        tea_name = f'{tea_name} tea'.replace(' tea tea', ' tea')

        if 'tea_desc' not in tea_obj or tea_obj['tea_desc'] == []:
            prompt = f'''
                Explain 1 paragraph on why {tea_name} helps with {problem_name}.
                Start the reply with the following words: {tea_name.capitalize()} helps with {problem_name} because .
                Never use the following words: can, may, might.
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_paragraphs(reply)
            if len(reply) == 1 and reply != '':
                print('********************************')
                print(reply)
                print('********************************')
                tea_obj['tea_desc'] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
            
        if 'tea_constituents' not in tea_obj or tea_obj['tea_constituents'] == []:
            prompt = f'''
                Write a numbered list of the most important medicinal constituents of {tea_name} that help with {problem_name}.
                Include 1 short sentence description for each of these medicinal constituents, explaining why that medicinal contituent is good for {problem_name}.
                Include only medicinal constituents that have short names.
                Don't include the name of the plant in the constituents names.
                Write each list element using the following format: [constituent name]: [constituent description].
                Never use the following words: can, may, might.
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_list_column(reply)
            reply = [line.replace('[', '').replace(']', '') for line in reply]
            if reply != '' and reply != []:
                print('********************************')
                print(reply)
                print('********************************')
                tea_obj['tea_constituents'] = reply
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)

        if 'tea_parts' not in tea_obj or tea_obj['tea_parts'] == []:
            prompt = f'''
                Write a numbered list of the most used parts of the {tea_name} plant that are used to make medicinal tea for {problem_name}.
                Reply by only selecting parts from the following list:
                - Roots
                - Rhyzomes
                - Stems
                - Leaves
                - Flowers
                - Seeds
                - Buds
                - Bark
                Never include aerial parts.
                Never repeat the same part twice and never include similar parts.
                Include 1 short sentence description for each of these part, explaining why that part is good for making medicinal tea for {problem_name}.
                Write each list element using the following format: [part name]: [part description].
                Never use the following words: can, may, might.
            '''     
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_list_column(reply)
            if reply != '' and reply != []:
                print('********************************')
                print(reply)
                print('********************************')
                tea_obj['tea_parts'] = reply
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)

        if 'tea_recipe' not in tea_obj or tea_obj['tea_recipe'] == []:
            prompt = f'''
                Write a 5-step recipe in list format to make {tea_name} for {problem_name}.
                Include ingredients dosages and preparations times.
                Write only 1 sentence for each step.
                Start each step in the list with an action verb.
                Don't include optional steps.
                Never use the following words: can, may, might.
            '''  
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_list(reply)
            if reply != '' and reply != [] and len(reply) == 5:
                print('********************************')
                print(reply)
                print('********************************')
                tea_obj['tea_recipe'] = reply
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)

        # TODO: gen study


def json_tea_systems_problems_supplementary(json_filepath, data):
    problem_id = data['problem_id']
    problem_slug = data['problem_slug']
    problem_name = data['problem_name']

    key = 'problem_definition'
    if key not in data:
        prompt = f'''
            Write 1 paragraph explaining what is {problem_name} and how it impacts people lives.
            Start the reply with the following words: {problem_name} is .
            Never use these words: "can", "may", and "might".
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

    key = 'problems_related'
    if key not in data:
        problems_related_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_PROBLEMS_RELATED_FILEPATH, problems_related_cols['problem_id'], problem_id,
        )

        problems_rows_filtered = []
        for problem_related_row in problems_related_rows_filtered:
            jun_related_id = problem_related_row[problems_related_cols['related_id']]
            jun_related_name = problem_related_row[problems_related_cols['related_name']]
            for problem_row in problems_rows:
                problem_id = problem_row[problems_cols['problem_id']]
                problem_slug = problem_row[problems_cols['problem_slug']]
                problem_names = problem_row[problems_cols['problem_names']]
                if jun_related_id == problem_id:
                    problems_rows_filtered.append({
                        'problem_id': problem_id, 
                        'problem_slug': problem_slug, 
                        'problem_names': problem_names, 
                        'related_name': jun_related_name, 
                    })
                    break

        related_names = [row['related_name'] for row in problems_rows_filtered]
        related_names_prompt = ''
        for related_name in related_names:
            related_names_prompt += f'- {related_name}\n'

        prompt = f'''
            Write a numbered list explaining why people with {problem_name} also experience the following problems:
            {related_names_prompt}.
            Write the list items using the following structure: [related problem]: [explanation].
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)
        
        reply = utils_ai.reply_to_list_column(reply)

        if reply != []:
            print('********************************')
            print(reply)
            print('********************************')
            data[key] = reply
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)
    
    # key = 'other_remedies'
    # if key not in data:
    #     prompt = f'''
    #         Write 1 detailed paragraph about what are the most common and effective natural remedies for {condition_name}.
    #         Don't include herbal teas.
    #         Never use the following words: can, may, might.
    #     '''
    #     reply = utils_ai.gen_reply(prompt)
    #     reply = utils_ai.reply_to_paragraphs(reply)
    #     if reply != [] and len(reply) == 1:
    #         print('********************************')
    #         print(reply)
    #         print('********************************')
    #         data[key] = reply[0]
    #         util.json_write(json_filepath, data)
    #     time.sleep(g.PROMPT_DELAY_TIME)




def art_tea_systems_problems():
    for problem_row in problems_rows[:ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        print(f'> {problem_name}')

        system_row = csv_get_system_by_problem(problem_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        print(f'  > {system_name}')

        json_filepath = f'database/json/herbalism/tea/{system_slug}/{problem_slug}.json'

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['problem_id'] = problem_id
        data['problem_slug'] = problem_slug
        data['problem_name'] = problem_name

        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 

        data['teas_num'] = teas_num
        title = f'{teas_num} Best herbal teas for {problem_name}'
        data['title'] = title

        util.json_write(json_filepath, data)

        # JSON
        json_tea_systems_problems_intro(json_filepath, data)
        json_tea_systems_problems_list(json_filepath, data)
        json_tea_systems_problems_supplementary(json_filepath, data)

        # HTML
        html_filepath = f'website/herbalism/tea/{system_slug}/{problem_slug}.html'

        data = util.json_read(json_filepath)

        article_html = ''
        article_html += f'<h1>{title}</h1>\n'

        # # pil image
        # tea_obj = data['teas'][0]
        # tea_name = tea_obj['tea_name'].strip().lower()
        # tea_slug = tea_name.replace(' ', '-').replace("'", '-').replace('.', '-')

        # images_folderpath = f'C:/terrawhisper-assets/images/tea/{tea_slug}'
        # if os.path.exists(images_folderpath):
        #     images_filepaths = [f'{images_folderpath}/{filename}' for filename in os.listdir(images_folderpath)] 
        #     image_filepath = random.choice(images_filepaths)
        #     if image_filepath != '':
        #         image_condition_slug = condition_slug.split('/')[-1]
        #         image_filepath_out = f'website/images/herbal-tea-for-{image_condition_slug}-overview.jpg'
        #         if not os.path.exists(image_filepath_out):
        #             util.image_variate(image_filepath, image_filepath_out)
        # else:
        #     print(f'IMG FOLDER MISSING: {images_folderpath}')
        
        # # html image
        # tea_image_url = f'/images/herbal-tea-for-{image_condition_slug}-overview.jpg'
        # if os.path.exists(f'website{tea_image_url}'):
        #     article_html += f'<p><img src="{tea_image_url}"><p>\n'
        # else:
        #     print(f'IMG MISSING: {tea_slug}')

        try: article_html += f'{util.text_format_1N1_html(data["intro"])}\n'
        except: print(f'MISSING INTRO: {html_filepath} >> {problem_name}')

        
        for i, tea_obj in enumerate(data['teas_list'][:teas_num]):
            herb_slug = tea_obj['herb_slug'].strip().lower()
            herb_name_common = tea_obj['herb_name_common'].strip().lower()
            tea_name = tea_obj["herb_name_common"].strip().lower()
            tea_name = f'{tea_name} tea'.replace(' tea tea', ' tea')

            article_html += f'<h2>{i+1}. {tea_name.capitalize()}</h2>\n'
            try: article_html += f'<p>{util.text_format_1N1_html(tea_obj["tea_desc"])}</p>\n'
            except: print(f'MISSING TEA DESC: {html_filepath} >> {problem_name} >> {tea_name}')


        #     # img
        #     images_folderpath = f'C:/terrawhisper-assets/images/tea/{tea_slug}'
        #     if os.path.exists(images_folderpath):
        #         images_filepaths = [f'{images_folderpath}/{filename}' for filename in os.listdir(images_folderpath)] 
        #         image_filepath = random.choice(images_filepaths)
        #         if image_filepath != '':
        #             image_condition_slug = condition_slug.split('/')[-1]
        #             image_filepath_out = f'website/images/herbal-tea-for-{image_condition_slug}-{tea_slug}.jpg'
        #             if not os.path.exists(image_filepath_out):
        #                 util.image_variate(image_filepath, image_filepath_out)
        #     else:
        #         print(f'IMG FOLDER MISSING: {images_folderpath}')
        #     tea_image_url = f'/images/herbal-tea-for-{image_condition_slug}-{tea_slug}.jpg'
        #     if os.path.exists(f'website{tea_image_url}'):
        #         article_html += f'<p><img src="{tea_image_url}"><p>\n'
        #     else:
        #         print(f'MISSING TEA IMAGE: {condition_name} >> {tea_name}')
                
                
            try:
                tea_constituents = tea_obj['tea_constituents']
                # article_html += f'<h3>Constituents</h3>\n'
                article_html += f'<p>The list below shows the primary active constituents in {tea_name} that aid with {problem_name}.</p>\n'
                article_html += '<ul>\n'
                for tea_constituent in tea_constituents:
                    chunk_1 = tea_constituent.split(': ')[0]
                    chunk_2 = ': '.join(tea_constituent.split(': ')[1:])
                    article_html += f'<li><strong>{chunk_1.capitalize()}</strong>: {chunk_2}</li>\n'
                article_html += '</ul>\n'
            except: print(f'MISSING TEA CONSTITUENTS: {problem_name} >> {tea_name}')

            try:
                tea_parts = tea_obj['tea_parts']
                # article_html += f'<h3>Parts</h3>\n'
                article_html += f'<p>Right below you will find a list of the most important parts in {tea_name} that help with {problem_name}.</p>\n'
                article_html += '<ul>\n'
                for tea_part in tea_parts:
                    chunk_1 = tea_part.split(': ')[0]
                    chunk_2 = ': '.join(tea_part.split(': ')[1:])
                    article_html += f'<li><strong>{chunk_1.capitalize()}</strong>: {chunk_2}</li>\n'
                article_html += '</ul>\n'
            except: print(f'MISSING TEA PARTS: {problem_name} >> {tea_name}')

            try:
                tea_recipe = tea_obj['tea_recipe']
                # article_html += f'<h3>Recipe</h3>\n'
                article_html += f'<p>The following recipe gives a procedure to make a basic {tea_name} for {problem_name}.</p>\n'
                article_html += '<ol>\n'
                for step in tea_recipe:
                    article_html += f'<li>{step}</li>\n'
                article_html += '</ol>\n'
            except: print(f'MISSING TEA RECIPE: {problem_name} >> {tea_name}')
 
        # if condition_classification != 'demography' and condition_classification != 'animal':
        #     key = 'definition'
        #     if key in data:
        #         article_html += f'<h2>What is {condition_name} and how can it affect your life?</h2>\n'
        #         definition = data[key]
        #         if os.path.exists(f'ailments/{system_slug}/{condition_slug}.html'):
        #             pass
        #         article_html += f'<p>{util.text_format_1N1_html(definition)}</p>\n'
        #     else:
        #         print(f'MISSING DEFINITION: {condition_name}')

        #     key = 'other_remedies'
        #     if key in data:
        #         article_html += f'<h2>What other natural remedies help with {condition_name}?</h2>\n'
        #         article_html += f'<p>{util.text_format_1N1_html(data[key])}</p>\n'
        #     else:
        #         print(f'MISSING OTHER REMEDIES: {condition_name}')
                
        #     key = 'related_problems'
        #     if key in data:
        #         article_html += f'<h2>What other health issues people with {condition_name} are likely to experience?</h2>\n'
        #         article_html += f'<p>The issues people with {condition_name} are likely to experiece are listed below.</p>\n'
        #         article_html += '<ul>\n'
        #         for item in data[key]:
        #             chunk_1 = item.split(': ')[0]

        #             # get related condition link
        #             condition_slug_link = ''
        #             for condition_row_tmp in conditions_rows[1:]:
        #                 condition_names_tmp = condition_row_tmp[conditions_cols['condition_names']].strip().lower().split(', ')
        #                 condition_slug_tmp = condition_row_tmp[conditions_cols['condition_slug']].strip().lower()
        #                 if chunk_1.strip().lower() in condition_names_tmp:
        #                     condition_slug_link = condition_slug_tmp
        #                     break

        #             chunk_2 = ': '.join(item.split(': ')[1:])
        #             if condition_slug_link != '': article_html += f'<li><a href="/herbalism/tea/{condition_slug_link}.html"><strong>{chunk_1}</strong></a>: {chunk_2}</li>\n'
        #             else: article_html += f'<li><strong>{chunk_1}</strong>: {chunk_2}</li>\n'
        #         article_html += '</ul>\n'
        #     else:
        #         print(f'MISSING RELATED PROBLEMS: {condition_name}')


        problem_definition = data["problem_definition"]
        if os.path.exists(f'website/ailments/{system_slug}/{problem_slug}.html'):
            problem_definition = problem_definition.replace(
                problem_name.capitalize(),
                f'<a href="/ailments/{system_slug}/{problem_slug}.html">{problem_name.capitalize()}</a>',
                1
            )
        article_html += f'<h2>What is bad breath and why is important to treat it?</h2>\n'
        try: article_html += f'{util.text_format_1N1_html(problem_definition)}\n'
        except: print(f'MISSING INTRO: {html_filepath} >> {problem_name}')

        key = 'problems_related'
        if key in data:
            article_html += f'<h2>What other health problems are likely to experience people when they have {problem_name}?</h2>\n'
            article_html += f'<p>When people have {problem_name}, they are also likely to experience the health problems listed below.</p>\n'
            article_html += '<ul>\n'
            for item in data[key]:
                chunk_1 = item.split(': ')[0]
                chunk_2 = ': '.join(item.split(': ')[1:])
                article_html += f'<li><strong>{chunk_1.capitalize()}</strong>: {chunk_2}</li>\n'
            article_html += '</ul>\n'


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

        # # GEN TEAS HTML TOO FOR OLD REDIRECTS
        # condition_slug_old = condition_slug.split('/')[-1].strip()
        # html_filepath = f'website/herbalism/teas/{condition_slug_old}.html'

        # header_html = util.header_default()
        # breadcrumbs_html = util.breadcrumbs(html_filepath)
        # meta_html = util.article_meta(article_html, lastmod)
        # article_html = util.article_toc(article_html)

        # html = f'''
        #     <!DOCTYPE html>
        #     <html lang="en">

        #     <head>
        #         <head>\n<meta http-equiv="refresh" content="0; url=https://terrawhisper.com/herbalism/tea/{condition_slug}.html">
        #         <meta charset="UTF-8">
        #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
        #         <meta name="author" content="{g.AUTHOR_NAME}">
        #         <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
        #         <link rel="stylesheet" href="/style.css">
        #         <title>{title}</title>
        #         {g.GOOGLE_TAG}
                
        #     </head>

        #     <body>
        #         {header_html}
        #         {breadcrumbs_html}
                
        #         <section class="article-section">
        #             <div class="container">
        #                 {meta_html}
        #                 {article_html}
        #             </div>
        #         </section>

        #         <footer>
        #             <div class="container-lg">
        #                 <span>© TerraWhisper.com 2024 | All Rights Reserved
        #             </div>
        #         </footer>
        #     </body>

        #     </html>
        # '''
        # util.file_write(html_filepath, html)


        # # REDIRECTS
        # condition_slugs_prev_list = condition_slugs_prev.split(',')
        # for condition_slug_prev in condition_slugs_prev_list:
        #     print(condition_slug_prev)
        #     if condition_slug_prev == condition_slug: continue
        #     html_filepath_out = f'website/herbalism/tea/{condition_slug_prev}.html'
        #     html_filepath_web = f'https://terrawhisper.com/herbalism/tea/{condition_slug}.html'
        #     html = util.file_read(html_filepath_out)
        #     if os.path.exists(html_filepath_out):
        #         if f'<meta http-equiv="refresh" content="0; url={html_filepath_web}">' not in html:
        #             html = html.replace(
        #                 '<head>',
        #                 f'<head>\n<meta http-equiv="refresh" content="0; url={html_filepath_web}">'
        #             )
        #     util.file_write(html_filepath_out, html)


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


def page_herbalism():
    header = util.header_default()

    page_url = 'herbalism'
    article_filepath_out = f'website/{page_url}.html'

    template = util.file_read(f'templates/{page_url}.html')
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)

    template = template.replace('[meta_title]', 'Herbalism & Natural Healing')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[title]', 'Herbalism: Herbal Medicine and Preparations')
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)

    util.file_write(article_filepath_out, template)
    

    
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
# page_herbalism()
# page_top_herbs()
# page_plants(regen_csv=False)
# page_about()
# page_start_here()


# art_ailments()
# art_systems()
# art_problems()





gen_csvs()
# art_tea_systems_problems()



# sitemap.sitemap_all()
# shutil.copy2('sitemap.xml', 'website/sitemap.xml')


# shutil.copy2('style.css', 'website/style.css')
# shutil.copy2('util.css', 'website/util.css')
# shutil.copy2('assets/images/healing-herbs.jpg', 'website/images/healing-herbs.jpg')