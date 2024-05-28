import time

import g
import util
import utils_ai


problems_rows = util.csv_get_rows(g.CSV_PROBLEMS_FILEPATH)
problems_cols = util.csv_get_cols(problems_rows)
problems_rows = problems_rows[1:]

herbs_rows = util.csv_get_rows(g.CSV_HERBS_FILEPATH)
herbs_cols = util.csv_get_cols(herbs_rows)
herbs_rows = herbs_rows[1:]

preparations_rows = util.csv_get_rows(g.CSV_PREPARATIONS_FILEPATH)
preparations_cols = util.csv_get_cols(preparations_rows)
preparations_rows = preparations_rows[1:]

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]

# JUNCTIONS
problems_herbs_rows = util.csv_get_rows(g.CSV_PROBLEMS_HERBS_FILEPATH)
problems_herbs_cols = util.csv_get_cols(problems_herbs_rows)
problems_herbs_rows = problems_herbs_rows[1:]

problems_preparations_rows = util.csv_get_rows(g.CSV_PROBLEMS_PREPARATIONS_FILEPATH)
problems_preparations_cols = util.csv_get_cols(problems_preparations_rows)
problems_preparations_rows = problems_preparations_rows[1:]

problems_systems_rows = util.csv_get_rows(g.CSV_PROBLEMS_SYSTEMS_FILEPATH)
problems_systems_cols = util.csv_get_cols(problems_systems_rows)
problems_systems_rows = problems_systems_rows[1:]

problems_teas_rows = util.csv_get_rows(g.CSV_PROBLEMS_TEAS_FILEPATH)
problems_teas_cols = util.csv_get_cols(problems_teas_rows)
problems_teas_rows = problems_teas_rows[1:]

problems_related_rows = util.csv_get_rows(g.CSV_PROBLEMS_RELATED_FILEPATH)
problems_related_cols = util.csv_get_cols(problems_related_rows)
problems_related_rows = problems_related_rows[1:]

problems_tinctures_rows = util.csv_get_rows(g.CSV_PROBLEMS_TINCTURES_FILEPATH)
problems_tinctures_cols = util.csv_get_cols(problems_tinctures_rows)
problems_tinctures_rows = problems_tinctures_rows[1:]

problems_capsules_rows = util.csv_get_rows(g.CSV_PROBLEMS_CAPSULES_FILEPATH)
problems_capsules_cols = util.csv_get_cols(problems_capsules_rows)
problems_capsules_rows = problems_capsules_rows[1:]


def sanitize_herbs(line):
    line = line.replace('licorice root', 'licorice')
    line = line.replace('ginger root', 'ginger')
    line = line.replace('marshmallow root', 'marshmallow')
    line = line.replace('slippery elm bark', 'slippery elm')
    line = line.replace('cloves', 'clove')
    line = line.replace('tea tree oil', 'tea tree')
    line = line.replace('wild oregano', 'oregano')
    line = line.replace('raspberry leaf', 'raspberry')
    line = line.replace('oak bark', 'oak')
    if line == 'hop': line = 'hops'
    if line == 'kava': line = 'kava kava'
    if line == 'willow bark': line = 'willow'
    if line == 'valerian root': line = 'valerian'
    if line == 'eleuthero': line = 'siberian ginseng'
    if line == 'milky oat seed': line = 'oat straw'
    if line == 'milky oat tops': line = 'oat straw'
    if line == 'milky oat': line = 'oat straw'
    if line == 'rhodiola rosea': line = 'golden root'
    if line == 'schisandra': line = 'magnolia vines'
    if line == 'rhodiola': line = 'golden root'
    if line == 'saint john\'s wort': line = 'st. john\'s wort'
    if line == 'flaxseed': line = 'flax'
    if line == 'black caraway': line = 'black seed'
    if line == 'rehmannia': line = 'chinese foxglove'
    if line == 'water-peony': line = 'peony'
    if line == 'olive leaf': line = 'olive'
    if line == 'viscum album': line = 'mistletoe'
    if line == 'crataegus': line = 'hawthorn'
    if line == 'fennel seed': line = 'fennel'
    if line == 'red raspberry': line = 'raspberry'
    if line == 'burdock root': line = 'burdock'
    if line == 'aloe': line = 'aloe vera'
    if line == 'cascara': line = 'cascara sagrada'
    if line == 'osha root': line = 'osha'
    if line == 'cayenne': line = 'cayenne pepper'
    if line == 'wild cherry': line = 'cherry'
    if line == 'wild cherry bark': line = 'cherry'
    if line == 'grindelia': line = 'gumweed'
    if line == 'aniseed': line = 'anise'
    if line == 'cowslip': line = 'primrose'
    if line == 'baptisia tinctoria': line = 'wild indigo'
    if line == 'blackberry root': line = 'blackberry'
    if line == 'blackberry leaf': line = 'blackberry'
    if line == 'blueberry leaves': line = 'blueberry'
    if line == 'blueberry leaf': line = 'blueberry'
    if line == 'birch leaf': line = 'birch'
    if line == 'strawberry leaf': line = 'strawberry'
    if line == 'bearberry leaf': line = 'bearberry'
    if line == 'oregon grape root': line = 'oregon grape'
    if line == 'red raspberry leaves': line = 'raspberry'
    if line == 'capsicum': line = 'cayenne pepper'
    if line == 'boswellia': line = 'frankincense'
    if line == 'stinging nettle': line = 'nettle'
    if line == 'elderflower': line = 'elderberry'
    if line == 'ginkgo': line = 'ginkgo biloba'
    if line == 'poke': line = 'pokeweed'
    if line == 'poke root': line = 'pokeweed'
    if line == 'astragalus': line = 'milkvetch'
    if line == 'baptisia': line = 'wild indigo'
    if line == 'pleurisy root': line = 'butterfly weed'
    if line == 'angelica root': line = 'angelica'
    if line == 'linden flower': line = 'linden'
    if line == 'linden flower': line = 'linden'
    if line == 'celery seed': line = 'celery'
    if line == 'cascara sagrada': line = 'cascara'
    if line == 'artemisia': line = 'mugwort'
    if line == 'ivy leaf': line = 'ivy'
    if line == 'usnea': line = 'beard lichens'
    if line == 'plantain leaf': line = 'plantain'
    if line == 'chamomile flower': line = 'chamomile'

    return line



def csv_gen_system_for_problem(problem_row):
    problem_id = problem_row[problems_cols['problem_id']]
    problem_slug = problem_row[problems_cols['problem_slug']]
    problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

    problems_systems_rows = csv_get_system_by_problem(problem_id)

    if problems_systems_rows == []:
        systems_names = [row[systems_cols['system_name']] for row in systems_rows]
        systems_names_prompt = ', '.join(systems_names)

        prompt = f'''
            In which body system would you classify the following problem: {problem_name}.
            Choose only 1 body system among the followings: {systems_names_prompt}.
            Reply in only 1 word.
        '''
        reply = utils_ai.gen_reply(prompt)

        reply = reply.lower()
        systems_names_1_word = [
            row[systems_cols['system_name']].lower().replace('system', '').strip()
            for row in systems_rows
        ]
        system_name = ''
        for system_name_1_word in systems_names_1_word:
            if system_name_1_word in reply:
                system_name = system_name_1_word
                break

        if system_name != '':
            system_name = f'{system_name} system'

            print('***************************************************')
            print(system_name)
            print('***************************************************')

            system_id = ''
            for system_row in systems_rows:
                system_id_csv = system_row[systems_cols['system_id']].lower().strip()
                system_name_csv = system_row[systems_cols['system_name']].lower().strip()
                if system_name == system_name_csv:
                    system_id = system_id_csv
                    break

            util.csv_add_rows(g.CSV_PROBLEMS_SYSTEMS_FILEPATH, [[problem_id, problem_name, system_id, system_name]])

        time.sleep(g.PROMPT_DELAY_TIME)
        

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
            line = line.split('(')[0]
            line = line.strip()
            if line == '': continue

            line = sanitize_herbs(line)

            found = False
            for line_added in lines:
                # print(line, line_added)
                if line == line_added[3]:
                    found = True
                    break
            # print('found')
            if found: continue

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
            line = line.split('(')[0]
            line = line.strip()
            if line == '': continue

            line = sanitize_herbs(line)

            found = False
            for line_added in lines:
                if line == line_added[3]:
                    found = True
                    break
            if found: continue

            herbs_rows_filtered = util.csv_get_rows_filtered(
                g.CSV_HERBS_FILEPATH, herbs_cols['herb_name_common'], line
            )
            if herbs_rows_filtered != []:
                herb_row = herbs_rows_filtered[0]
                herb_id = herb_row[herbs_cols['herb_id']]
            else:
                herb_id = ''

            for item in lines:
                if item[3] == line:
                    continue

            lines.append([problem_id, problem_slug, herb_id, line])

        if len(lines) >= 10:
            print('***************************************************')
            print(lines)
            print('***************************************************')
            util.csv_add_rows(g.CSV_PROBLEMS_HERBS_FILEPATH, lines)

        print(problem_id, problem_slug, problem_name)
        time.sleep(g.PROMPT_DELAY_TIME)


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


def csv_gen_preparations_for_problem(problem_row):
    problem_id = problem_row[problems_cols['problem_id']]
    problem_slug = problem_row[problems_cols['problem_slug']]
    problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

    problems_preparations_rows = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_PREPARATIONS_FILEPATH, problems_preparations_cols['problem_id'], problem_id
    )

    if problems_preparations_rows == []:
        prompt = f'''
            Write a numbered list of the 15 most effective type of herbal preparations for {problem_name}.
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
            
            if 'tea' in line: continue
                # if 'infusions' in lines:
                #     continue

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
            line = line.split('(')[0]
            line = line.strip()
            if line == '': continue

            line = sanitize_herbs(line)
            
            found = False
            for line_added in lines:
                if line == line_added[3]:
                    found = True
                    break
            if found: continue

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


def csv_gen_capsules_for_problem(problem_row):
    problem_id = problem_row[problems_cols['problem_id']]
    problem_slug = problem_row[problems_cols['problem_slug']]
    problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

    problems_capsules_rows = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_CAPSULES_FILEPATH, problems_capsules_cols['problem_id'], problem_id
    )

    if problems_capsules_rows == []:
        items_num = 15
        prompt = f'''
            Write a numbered list of the {items_num} best herbal capsules for {problem_name}.
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
            line = line.split('(')[0]
            line = line.strip()
            if line == '': continue

            line = sanitize_herbs(line)
            
            found = False
            for line_added in lines:
                if line == line_added[3]:
                    found = True
                    break
            if found: continue

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
            util.csv_add_rows(g.CSV_PROBLEMS_CAPSULES_FILEPATH, lines)

        time.sleep(g.PROMPT_DELAY_TIME)



##################################################
# EXE
##################################################

def gen_csvs(problems_num=0):
    if problems_num < 0: return
    
    problems_num_selected = 0
    if problems_num != 0: problems_num_selected = problems_num
    else: problems_num_selected = g.ART_NUM

    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']].strip().lower()
        problem_slug = problem_row[problems_cols['problem_slug']].strip().lower()
        problem_names = problem_row[problems_cols['problem_names']]
        problem_name = problem_names.split(',')[0].strip().lower()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        print(f'> {problem_row}')

        # TODO
        csv_gen_system_for_problem(problem_row)
        
        csv_gen_herbs_for_problem(problem_row)
        csv_gen_preparations_for_problem(problem_row)

        csv_gen_teas_for_problem(problem_row)
        csv_gen_tinctures_for_problem(problem_row)
        csv_gen_capsules_for_problem(problem_row)


gen_csvs(1)