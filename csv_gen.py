import time

import g
import util
import utils_ai

ART_NUM = 2

problems_rows = util.csv_get_rows(g.CSV_PROBLEMS_FILEPATH)
problems_cols = util.csv_get_cols(problems_rows)
problems_rows = problems_rows[1:]

herbs_rows = util.csv_get_rows(g.CSV_HERBS_FILEPATH)
herbs_cols = util.csv_get_cols(herbs_rows)
herbs_rows = herbs_rows[1:]

# JUNCTIONS
problems_herbs_rows = util.csv_get_rows(g.CSV_PROBLEMS_HERBS_FILEPATH)
problems_herbs_cols = util.csv_get_cols(problems_herbs_rows)
problems_herbs_rows = problems_herbs_rows[1:]

problems_preparations_rows = util.csv_get_rows(g.CSV_PROBLEMS_PREPARATIONS_FILEPATH)
problems_preparations_cols = util.csv_get_cols(problems_preparations_rows)
problems_preparations_rows = problems_preparations_rows[1:]

problems_teas_rows = util.csv_get_rows(g.CSV_PROBLEMS_TEAS_FILEPATH)
problems_teas_cols = util.csv_get_cols(problems_teas_rows)
problems_teas_rows = problems_teas_rows[1:]

problems_related_rows = util.csv_get_rows(g.CSV_PROBLEMS_RELATED_FILEPATH)
problems_related_cols = util.csv_get_cols(problems_related_rows)
problems_related_rows = problems_related_rows[1:]

problems_tinctures_rows = util.csv_get_rows(g.CSV_PROBLEMS_TINCTURES_FILEPATH)
problems_tinctures_cols = util.csv_get_cols(problems_tinctures_rows)
problems_tinctures_rows = problems_tinctures_rows[1:]


##################################################
# TEAS
##################################################
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

            line = line.replace('licorice root', 'licorice')

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
            util.csv_add_rows(g.CSV_PROBLEMS_TEAS_FILEPATH, lines)

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

            line = line.replicace('licorice root', 'licorice')
            line = line.replicace('ginger root', 'ginger')
            line = line.replicace('marshmallow root', 'marshmallow')
            line = line.replicace('slippery elm bark', 'slippery elm')

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
            
            if line == 'teas':
                if 'infusions' in lines:
                    continue

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



##################################################
# TINCTURES
##################################################

def csv_gen_tinctures_for_problem(problem_row):
    problem_id = problem_row[problems_cols['problem_id']]
    problem_slug = problem_row[problems_cols['problem_slug']]
    problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

    problems_tinctures_rows = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_TINCTURES_FILEPATH, problems_tinctures_cols['problem_id'], problem_id
    )

    if problems_tinctures_rows == []:
        items_num = 15
        prompt = f'''
            Write a numbered list of the {items_num} best herbal tinctures for {problem_name}.
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

            line = line.replace('licorice root', 'licorice')
            line = line.replace('marshmallow root', 'marshmallow')
            line = line.replace('slippery elm bark', 'slippery elm')
            line = line.replace('raspberry leaf', 'raspberry')

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
            util.csv_add_rows(g.CSV_PROBLEMS_TINCTURES_FILEPATH, lines)

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

        # teas
        csv_gen_herbs_for_problem(problem_row)
        csv_gen_preparations_for_problem(problem_row)
        csv_gen_teas_for_problem(problem_row)
        csv_gen_related_for_problem(problem_row)

        # tinctures
        csv_gen_tinctures_for_problem(problem_row)


gen_csvs()