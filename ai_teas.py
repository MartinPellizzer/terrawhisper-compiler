import time
import re

from groq import Groq

import util
import utils_ai
import prompts


NUM_REMEDIES = 10



######################################################################
# UTILS
######################################################################
def reply_to_paragraphs(reply):
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
        if ":" in line:
            line = ': '.join(line.split(':')[1:]).strip()
            if line == '': continue
        line = line.replace('...', '')
        line = re.sub("\s\s+" , " ", line)
        reply_formatted.append(line)
    return reply_formatted


def reply_to_list(reply):
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        
        line = '. '.join(line.split('. ')[1:]).strip()
        if line == '': continue

        if len(line.split(' ')) < 10: continue

        reply_formatted.append(line)

    return reply_formatted


def reply_to_list_column(reply):
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        
        line = '. '.join(line.split('. ')[1:]).strip()
        if line == '': continue

        if len(line.split(' ')) < 10: continue

        line = line.replace('*', '')

        if ':' not in line: continue
        line_chunks = line.split(':')
        chunk_1 = line_chunks[0].split('(')[0].strip()
        chunk_2 = line_chunks[1].strip()
        line = f'{chunk_1}: {chunk_2}'

        reply_formatted.append(line)

    return reply_formatted


def csv_get_header_dict(rows):
    cols = {}
    for i, val in enumerate(rows[0]):
        cols[val] = i
    return cols


def field_delete(filepath, key): 
    data = util.json_read(filepath)
    del data[key]
    util.json_write(filepath, data)


def ai_entity(json_filepath, section, paragraph_num, prompt, aka=True, save=True):
    var_val = []
    var_name = f'{section}'

    data = util.json_read(json_filepath)

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != []: return
    
    reply = utils_ai.gen_reply(prompt)
    if reply != '': 
        if not aka: 
            reply = reply_remove_aka(reply, data['common_name'])
            if "also known as" in reply:
                chunks = reply.split(',')
                reply = chunks[0] + ', '.join(chunks[2:])
        reply = reply_to_paragraphs(reply)

        print(len(reply))
        if len(reply) == paragraph_num:
            p = reply
            print('***************************************')
            print(p)
            print('***************************************')
            data[var_name] = p
            data['lastmod'] = str(date_now())
            if save: util.json_write(json_filepath, data)
            else: print('### NOT SAVED - TEST MODE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    time.sleep(30)



######################################################################
# GENERATE
######################################################################

def ai_herbalism_teas_conditions_csv(condition, condition_i):
    filepath = 'database/tables/herbalism-teas-conditions.csv'
    rows = util.csv_get_rows_by_entity(filepath, condition)

    print(condition)
    if rows != []: return

    prompt_paragraphs_num = 19
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} best herbal teas for {condition}.
        Write only the names of the herbs, not the descriptions.
        Include only 1 herb for each list item.
        Don't specify the part of the herb.
    '''

    reply = utils_ai.gen_reply(prompt)

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' in line: continue 
        if line[0].isdigit():
            if '. ' in line: line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            if line.endswith('.'): line = line[0:-1]
            reply_formatted.append([condition, line, ''])

    if prompt_paragraphs_num == len(reply_formatted):
        print('***************************************')
        for line in reply_formatted:
            print(line)
        print('***************************************')

        util.csv_add_rows(filepath, reply_formatted)
        
    time.sleep(30)


def ai_herbalism_teas_conditions_csv_to_json(condition, slug):
    # IF ALREADY REMEDIES: SKIP CONDITION
    json_filepath = f'database/articles/herbalism/tea/{slug}.json'
    data = util.json_read(json_filepath)
    data_remedies = []
    try: data_remedies = data['remedies']
    except: data['remedies'] = data_remedies
    if data_remedies != []: 
        print(f'{condition}: data already present')
        return

    # IF NOT REMEDIES: SKIP CONDITION
    filepath = 'database/tables/herbalism-teas-conditions.csv'
    rows = util.csv_get_rows_by_entity(filepath, condition)
    if rows == []:
        print(f'{condition}: no remedy found') 
        return

    # INSERT REMEDIES IN JSON
    remedies = []
    for row in rows:
        remedies.append(
            {
                'remedy_name': row[1],
            }
        )
    data['remedies'] = remedies
    util.json_write(json_filepath, data)


def ai_herbalism_teas_conditions_description(condition, slug, condition_i):
    filepath = f'database/articles/herbalism/tea/{slug}.json'
    data = util.json_read(filepath)

    for index, remedy in enumerate(data['remedies'][:NUM_REMEDIES]):
        remedy_name = remedy['remedy_name']

        remedy_desc = ''
        try: remedy_desc = remedy['remedy_desc']
        except: remedy['remedy_desc'] = ''

        if remedy_desc != '': continue

        remedy_name_formatted = remedy_name.lower().strip() + ' tea'
        remedy_name_formatted = remedy_name_formatted.replace(' tea tea', ' tea')
        starting_text = f'{remedy_name_formatted.capitalize()} helps with {condition.lower()} because '
        prompt = f'''
            Explain in a 5-sentence paragraph why {remedy_name_formatted} helps with {condition.lower()}.
            Start with these words: {starting_text}
        '''     
        reply = utils_ai.gen_reply(prompt)
        reply_formatted = reply_to_paragraphs(reply)
       

        if reply_formatted == '' or len(reply_formatted) == 1:
            print('***************************************')
            for paragraph in reply_formatted:
                print(paragraph)
            print('***************************************')

            data['remedies'][index]['remedy_desc'] = reply_formatted[0]
            util.json_write(filepath, data)

        time.sleep(30)


def ai_herbalism_teas_conditions_parts(condition, slug, condition_i):
    filepath = f'database/articles/herbalism/tea/{slug}.json'
    data = util.json_read(filepath)

    for index, remedy in enumerate(data['remedies'][:NUM_REMEDIES]):
        remedy_name = remedy['remedy_name'].lower().strip()

        var_val = ''
        var_name = 'remedy_parts'
        try: var_val = remedy[var_name]
        except: remedy[var_name] = var_val
        if var_val != '': continue

        remedy_name_formatted = remedy_name + ' tea'
        remedy_name_formatted = remedy_name_formatted.replace(' tea tea', ' tea')

        starting_text = f'{remedy_name_formatted.capitalize()} helps with {condition.lower()} because '
        prompt = f'''
            Write a numbered list of the most used parts of the {remedy_name} plant that are used to make medicinal tea for {condition.lower()}.
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
            Include 1 short sentence description for each of these part, explaining why that part is good for making medicinal tea for {condition.lower()}.
        '''     
        reply = utils_ai.gen_reply(prompt)
        reply_formatted = reply_to_list_column(reply)
       
        if reply_formatted != '':
            print('***************************************')
            for paragraph in reply_formatted:
                print(paragraph)
            print('***************************************')

            data['remedies'][index][var_name] = reply_formatted
            util.json_write(filepath, data)

        time.sleep(30)


def ai_herbalism_teas_conditions_constituents(condition, slug, condition_i):
    filepath = f'database/articles/herbalism/tea/{slug}.json'
    data = util.json_read(filepath)

    for index, remedy in enumerate(data['remedies'][:NUM_REMEDIES]):
        remedy_name = remedy['remedy_name'].lower().strip()

        var_val = ''
        var_name = 'remedy_constituents'
        try: var_val = remedy[var_name]
        except: remedy[var_name] = var_val
        if var_val != '': continue

        remedy_name_formatted = remedy_name + ' tea'
        remedy_name_formatted = remedy_name_formatted.replace(' tea tea', ' tea')

        prompt = f'''
            Write a numbered list of the most important medicinal constituents of {remedy_name} that help with {condition.lower()}.
            Include 1 short sentence description for each of these medicinal constituents, explaining why that medicinal contituent is good for {condition.lower()}.
            Include only medicinal constituents that have short names.
        '''
        reply = utils_ai.gen_reply(prompt)
        reply_formatted = reply_to_list_column(reply)
       
        if reply_formatted != '':
            print('***************************************')
            for paragraph in reply_formatted:
                print(paragraph)
            print('***************************************')

            data['remedies'][index][var_name] = reply_formatted
            util.json_write(filepath, data)

        time.sleep(30)


def ai_herbalism_teas_conditions_recipe(condition, slug, condition_i):
    filepath = f'database/articles/herbalism/tea/{slug}.json'
    data = util.json_read(filepath)

    for index, remedy in enumerate(data['remedies'][:NUM_REMEDIES]):
        remedy_name = remedy['remedy_name'].lower().strip()

        var_val = ''
        var_name = 'remedy_recipe'
        try: var_val = remedy[var_name]
        except: remedy[var_name] = var_val
        if var_val != '': continue

        remedy_name_formatted = remedy_name + ' tea'
        remedy_name_formatted = remedy_name_formatted.replace(' tea tea', ' tea')

        prompt = f'''
            Write a 5-step recipe in list format to make {remedy_name_formatted.lower()} for {condition.lower()}.
            Include ingredients dosages and preparations times.
            Write only 1 sentence for each step.
            Start each step in the list with an action verb.
        '''  
        reply = utils_ai.gen_reply(prompt)
        reply_formatted = reply_to_list(reply)
       
        if reply_formatted != '':
            print('***************************************')
            for paragraph in reply_formatted:
                print(paragraph)
            print('***************************************')

            data['remedies'][index][var_name] = reply_formatted
            util.json_write(filepath, data)

        time.sleep(30)


# def ai_recipe(condition, prompt):
#     condition_dash = condition.strip().lower().replace(' ', '-')
#     filepath = f'database/articles/herbalism/tea/{condition_dash}.json'
#     data = util.json_read(filepath)

#     if not data: return

#     for index, remedy in enumerate(data['remedies'][:NUM_REMEDIES]):
#         remedy_name = remedy['remedy_name']

#         remedy_recipe = []
#         try: remedy_recipe = remedy['remedy_recipe']
#         except: remedy['remedy_recipe'] = []

#         if remedy_recipe != []: continue

#         remedy_name_formatted = remedy_name.lower().strip() + ' tea'
#         remedy_name_formatted = remedy_name_formatted.replace(' tea tea', ' tea')
#         prompt = prompt.replace('<remedy_name_formatted>', remedy_name_formatted)

#         reply = utils_ai.gen_reply(prompt)
#         reply_formatted = reply_to_list(reply)

#         print(len(reply_formatted))
#         if reply_formatted == '' or len(reply_formatted) == 5:
#             print('***************************************')
#             for paragraph in reply_formatted:
#                 print(paragraph)
#             print('***************************************')

#             data['remedies'][index]['remedy_recipe'] = reply_formatted
#             util.json_write(filepath, data)

#         time.sleep(30)


# def ai_herbalism_tea_condition():
#     rows = util.csv_get_rows('database/tables/conditions/conditions.csv')

#     cols = {}
#     for i, val in enumerate(rows[0]):
#         cols[val] = i

#     for row in rows[1:]:
#         if row[cols['condition']] == '': continue

#         pinned = row[cols['pinned']].strip().lower()
#         condition = row[cols['condition']].strip().lower()
#         slug = row[cols['slug']].strip().lower()
#         system_id = row[cols['system_id']].strip().lower()
#         organ = row[cols['organ']].strip().lower()
#         synonyms = row[cols['synonyms']].strip().lower()

#         # TODO: remove next line, only used for testing
#         if condition != 'cough': continue 
        
#         json_filepath = f'database/articles/herbalism/tea/{condition}.json'
#         util.json_generate_if_not_exists(json_filepath)
#         data = util.json_read(json_filepath)
#         data['title'] = f'best herbal teas for {condition}'
#         try: data['lastmod']
#         except: data['lastmod'] = str(date_now())
#         try: data['remedies']
#         except: data['remedies'] = []
#         util.json_write(json_filepath, data)

#         print(condition)





def ai_intro(condition):
    condition_dash = condition.strip().lower().replace(' ', '-')
    filepath = f'database/articles/herbalism/tea/{condition_dash}.json'
    data = util.json_read(filepath)

    data_intro = ''
    try: data_intro = data['intro']
    except: data['intro'] = data_intro
    if data_intro != '': return

    prompt = f'''
        Explain in a 5-sentence paragraph why herbal teas helps with {condition.lower()}.
    '''
    reply = utils_ai.gen_reply(prompt) 
    reply_formatted = reply_to_paragraphs(reply)

    if reply_formatted == '' or len(reply_formatted) == 1:
        print('***************************************')
        for paragraph in reply_formatted:
            print(paragraph)
        print('***************************************')

        data['intro'] = reply_formatted[0]
        util.json_write(filepath, data)

    time.sleep(30)



######################################################################
# MAIN
######################################################################

def ai_herbalism_teas_conditions_main():
    rows = util.csv_get_rows('database/tables/conditions/conditions.csv')
    cols = csv_get_header_dict(rows)

    for i, row in enumerate(rows):
        condition = row[cols['condition']].lower().strip()
        slug = row[cols['slug']].lower().strip()
        classification = row[cols['classification']].lower().strip()
        system_id = row[cols['system_id']].lower().strip()

        if condition == '': continue
        if classification != 'symptom': continue
        if system_id != '0': continue

        print(f'{i+1}/{len(rows)} -- {condition}')

        json_filepath = f'database/articles/herbalism/tea/{slug}.json'
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['condition'] = condition
        data['preparation'] = 'tea'
        data['title'] = f'{10} best herbal teas for {condition}'
        data['url'] = f'herbalism/tea/{slug}'
        data['remedy_num'] = 10
        util.json_write(json_filepath, data)

        # try: field_delete(f'database/articles/herbalism/tea/{slug}.json', 'remedies')
        # except: pass
        # continue

        # STEP 1: AI GEN HERBAL TEAS FOR CONDITION (TO CLEAN)
        ai_herbalism_teas_conditions_csv(condition, i)

        # STEP 2: GEN JSON FROM AI GEN HERBAL TEAS (AFTER CLEANING)
        ai_herbalism_teas_conditions_csv_to_json(condition, slug)

        # STEP 3: AI GEN DESCRIPTIONS FOR HERBAL TEAS
        ai_herbalism_teas_conditions_description(condition, slug, i)
        ai_herbalism_teas_conditions_parts(condition, slug, i)
        ai_herbalism_teas_conditions_constituents(condition, slug, i)
        ai_herbalism_teas_conditions_recipe(condition, slug, i)
        continue




##################################################################
##################################################################
# HERBALISM
##################################################################
##################################################################

# TEAS
# ----------------------------------------------------------------

def ai_herbalism_teas():
    json_filepath = f'database/articles/herbalism/tea.json'
    
    util.json_generate_if_not_exists(json_filepath)
    data = util.json_read(json_filepath)
    data['title'] = f'Herbal Teas: Definition, Properties, Health Conditions They Help and Preparation'
    try: data['lastmod']
    except: data['lastmod'] = str(date_now())
    try: data['systems']
    except: data['systems'] = []
    util.json_write(json_filepath, data)

    # INTRO
    for prompt in prompts.tea_intro:
        ai_entity(json_filepath, 'intro_desc', 1, prompt, save=True)
        
    # DEFINITION
    for prompt in prompts.tea_definition:
        ai_entity(json_filepath, 'definition_desc', 1, prompt, save=False)

    # SYSTEMS
    systems_rows = util.csv_get_rows('database/tables/conditions/systems.csv')
    for i, system_row in enumerate(systems_rows[1:]):
        if system_row[0].strip() == '': continue

        system_id = system_row[0].strip().lower()
        system_name = system_row[1].strip().lower()

        data = util.json_read(json_filepath)
        data_systems = data['systems']

        found = False
        for data_system in data_systems:
            data_system_name = ''
            try: data_system_name = data_system['name']
            except: pass
            if data_system_name.lower().strip() == system_name.lower().strip():
                found = True
                break

        if not found:
            data['systems'].append({'name': system_name})

        util.json_write(json_filepath, data)

    # CONDITIONS
    conditions_rows = util.csv_get_rows('database/tables/conditions/conditions.csv')
    conditions_cols = util.csv_get_header_dict(conditions_rows)
    for condition_row in conditions_rows[1:]:
        condition_name = condition_row[conditions_cols['condition']].strip().lower()
        condition_slug = condition_row[conditions_cols['slug']].strip().lower()
        condition_classification = condition_row[conditions_cols['classification']].strip().lower()
        system_id = condition_row[conditions_cols['system_id']].strip().lower()
        try: system_name = util.csv_get_rows_by_entity('database/tables/conditions/systems.csv', system_id, num_col=0)[0][1].strip().lower()
        except: continue

        # TODO: remove next condition or differentiate between symptoms, conditions, general health?
        if condition_classification != 'symptom': continue

        data = util.json_read(json_filepath)
        for system in data['systems']:
            data_system_name = system['name']
            if data_system_name.lower().strip() == system_name.lower().strip():
                try: json_conditions = system['conditions']
                except: json_conditions = []
                found = False
                for json_condition in json_conditions:
                    if json_condition['name'].strip().lower() == condition_name.strip().lower():
                        found = True
                if not found:
                    try: system['conditions'].append({'name': condition_name, 'slug': condition_slug})
                    except: system['conditions'] = [{'name': condition_name, 'slug': condition_slug}]
        
        util.json_write(json_filepath, data)

    # CONDITIONS AI
    data = util.json_read(json_filepath)
    for system in data['systems']:

        conditions = []
        try: conditions = system['conditions']
        except: pass
        for condition in conditions:
            condition_name = condition['name']
            condition_desc = []
            try: condition_desc = condition['desc']
            except: pass

            # DESC
            if condition_desc == []:
                prompt = f'''
                    Write 1 sentence explaining what is {condition_name} and what herbal teas can help with this problem.
                '''
                reply = utils_ai.gen_reply(prompt)
                if reply != '': 
                    reply = reply_to_paragraphs(reply)

                    print(len(reply))
                    if len(reply) == 1:
                        p = reply
                        print('***************************************')
                        print(p)
                        print('***************************************')
                        condition['desc'] = p
                        data['lastmod'] = str(util.date_now())
                        util.json_write(json_filepath, data)

                time.sleep(30)
                
            # print(condition)

    # TODO: DELETE SYSTEMS/CONDITIONS IF MISSING FROM CSV




ai_herbalism_teas()
# ai_herbalism_teas_conditions_main()