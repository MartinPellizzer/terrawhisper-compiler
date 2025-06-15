import os

import urllib.request
from bs4 import BeautifulSoup

import g
import util

# import re
# import nltk
# from nltk.corpus import words
# nltk.download('words')



problems_rows = util.csv_get_rows(g.CSV_PROBLEMS_FILEPATH)
problems_cols = util.csv_get_cols(problems_rows)
problems_rows = problems_rows[1:]

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]

problems_systems_rows = util.csv_get_rows(g.CSV_PROBLEMS_SYSTEMS_FILEPATH)
problems_systems_cols = util.csv_get_cols(problems_systems_rows)
problems_systems_rows = systems_rows[1:]

problems_teas_rows = util.csv_get_rows(g.CSV_TEAS_FILEPATH)
problems_teas_cols = util.csv_get_cols(problems_teas_rows)
problems_teas_rows = problems_teas_rows[1:]



def csv_get_system_by_problem(problem_id):
    system_row = []

    problems_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_SYSTEMS_FILEPATH, problems_systems_cols['problem_id'], problem_id,
    )

    if problems_systems_rows_filtered != []:
        problem_system_row = problems_systems_rows_filtered[0]
        system_id = problem_system_row[problems_systems_cols['system_id']]

        systems_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id,
        )

        if systems_rows_filtered != []:
            system_row = systems_rows_filtered[0]

    return system_row


def simulate_intros():
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]

        system_row = csv_get_system_by_problem(problem_id)
        system_slug = system_row[systems_cols['system_slug']]

        json_filepath = f'database/json/herbalism/tea/{system_slug}/{problem_slug}.json'
        print(f'>> {json_filepath}')

        data = util.json_read(json_filepath)
        intro_desc = data['intro_desc']
        
        print(intro_desc)
        print()
        print()
        print()


def validate_links():
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]

        system_row = csv_get_system_by_problem(problem_id)
        system_slug = system_row[systems_cols['system_slug']]

        html_filepath = f'website/herbalism/tea/{system_slug}/{problem_slug}.html'
        

        # html_page = urllib.request.urlopen(html_filepath)

        if os.path.exists(html_filepath):
            with open(html_filepath) as fp: soup = BeautifulSoup(fp, 'html.parser')

            for link in soup.findAll('a'):
                href = link.get('href')
                if '.html' in href:
                    href_filepath = f'website{href}'
                    if os.path.exists(href_filepath):
                        # print(f'EXISTS: {href_filepath}')
                        pass
                    else:
                        print(f'DONT EXISTS:')
                        print(f'        {html_filepath}')
                        print(f'        {href_filepath}')
                        print()


def spellchecker():
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        system_row = csv_get_system_by_problem(problem_id)

        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        print(problem_row)

        json_filepath = f'database/json/remedies/{system_slug}/{problem_slug}/capsules.json'
        if os.path.exists(json_filepath):
            data = util.json_read(json_filepath)

            # key = 'intro_desc'
            # if key in data:
            #     print('\n***********************************************\n')
            #     print(data[key])
            #     print('\n***********************************************\n')

            # if 'remedies_list' in data:
            #     for remedy_obj in data['remedies_list']:
            #         # print(remedy_obj)
            #         if 'remedy_desc' in remedy_obj:
            #             print('\n***********************************************\n')
            #             remedy_desc = remedy_obj['remedy_desc']
            #             if remedy_desc[-1] == '.': print(remedy_desc)
            #             else: print(f'!!!! {remedy_desc}')
            #             print('\n***********************************************\n')
            
            # if 'remedies_list' in data:
            #     for remedy_obj in data['remedies_list']:
            #         # print(remedy_obj)
            #         if 'remedy_properties' in remedy_obj:
            #             print('\n***********************************************\n')
            #             for remedy_property in remedy_obj['remedy_properties']:
            #                 if remedy_property[-1] == '.': print(remedy_property)
            #                 else: print(f'!!!! {remedy_property}')
            #             print('\n***********************************************\n')

            # if 'remedies_list' in data:
            #     for remedy_obj in data['remedies_list']:
            #         # print(remedy_obj)
            #         if 'remedy_parts' in remedy_obj:
            #             print('\n***********************************************\n')
            #             for remedy_property in remedy_obj['remedy_parts']:
            #                 if remedy_property[-1] == '.': print(remedy_property)
            #                 else: print(f'!!!! {remedy_property}')
            #             print('\n***********************************************\n')

            if 'remedies_list' in data:
                for remedy_obj in data['remedies_list']:
                    # print(remedy_obj)
                    if 'remedy_recipe' in remedy_obj:
                        print('\n***********************************************\n')
                        for remedy_property in remedy_obj['remedy_recipe']:
                            if remedy_property[-1] == '.': print(remedy_property)
                            else: print(f'!!!! {remedy_property}')
                        print('\n***********************************************\n')

            
            # content = intro_desc
            # errors = []
            # has_errors = False
            # for word in content.split(' '):
            #     if re.sub(r"[^\w]", '', word.lower()) not in words.words():
            #         has_errors = True
            #         errors.append(word)

            # print(intro_desc)
            # if has_errors:
                # print('***********************************************')
                # print('ERRORS FOUND:')
                # for error in errors:
                #     print(error)
                # print('***********************************************')
            
            # quit()



# validate_links()


spellchecker()