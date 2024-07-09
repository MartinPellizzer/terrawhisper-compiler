import time

import g
import util
import utils_ai

herbs_rows = util.csv_get_rows(g.CSV_HERBS_FILEPATH)
herbs_cols = util.csv_get_cols(herbs_rows)
herbs_rows = herbs_rows[1:]

preparations_rows = util.csv_get_rows(g.CSV_PREPARATIONS_FILEPATH)
preparations_cols = util.csv_get_cols(preparations_rows)
preparations_rows = preparations_rows[1:]

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]

trefle_rows = util.csv_get_rows(g.CSV_TREFLE_FILEPATH)
trefle_cols = util.csv_get_cols(trefle_rows)
trefle_rows = trefle_rows[1:]

herbs_auto_rows = util.csv_get_rows(g.CSV_HERBS_AUTO_FILEPATH)
herbs_auto_cols = util.csv_get_cols(herbs_auto_rows)
herbs_auto_rows = herbs_auto_rows[1:]

status_rows = util.csv_get_rows(g.CSV_STATUS_FILEPATH)
status_cols = util.csv_get_cols(status_rows)
status_rows = status_rows[1:]


herbs_benefits_rows = util.csv_get_rows(g.CSV_HERBS_BENEFITS_FILEPATH)
herbs_benefits_cols = util.csv_get_cols(herbs_benefits_rows)
herbs_benefits_rows = herbs_benefits_rows[1:]

herbs_names_common_rows = util.csv_get_rows(g.CSV_HERBS_NAMES_COMMON_FILEPATH)
herbs_names_common_cols = util.csv_get_cols(herbs_names_common_rows)
herbs_names_common_rows = herbs_names_common_rows[1:]


status_systems_rows = util.csv_get_rows(g.CSV_STATUS_SYSTEMS_FILEPATH)
status_systems_cols = util.csv_get_cols(status_systems_rows)
status_systems_rows = status_systems_rows[1:]

status_herbs_rows = util.csv_get_rows(g.CSV_STATUS_HERBS_FILEPATH)
status_herbs_cols = util.csv_get_cols(status_herbs_rows)
status_herbs_rows = status_herbs_rows[1:]

status_preparations_teas_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_TEAS_FILEPATH)
status_preparations_teas_cols = util.csv_get_cols(status_preparations_teas_rows)
status_preparations_teas_rows = status_preparations_teas_rows[1:]

status_preparations_tinctures_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_TINCTURES_FILEPATH)
status_preparations_tinctures_cols = util.csv_get_cols(status_preparations_tinctures_rows)
status_preparations_tinctures_rows = status_preparations_tinctures_rows[1:]

status_preparations_decoctions_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_DECOCTIONS_FILEPATH)
status_preparations_decoctions_cols = util.csv_get_cols(status_preparations_decoctions_rows)
status_preparations_decoctions_rows = status_preparations_decoctions_rows[1:]

status_preparations_essential_oils_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_ESSENTIAL_OILS_FILEPATH)
status_preparations_essential_oils_cols = util.csv_get_cols(status_preparations_essential_oils_rows)
status_preparations_essential_oils_rows = status_preparations_essential_oils_rows[1:]

status_preparations_capsules_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_CAPSULES_FILEPATH)
status_preparations_capsules_cols = util.csv_get_cols(status_preparations_capsules_rows)
status_preparations_capsules_rows = status_preparations_capsules_rows[1:]

status_preparations_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_FILEPATH)
status_preparations_cols = util.csv_get_cols(status_preparations_rows)
status_preparations_rows = status_preparations_rows[1:]






def herb_sanitize(line):
    line = line.replace('mentha piperita', 'mentha x piperita')
    line = line.replace('matricaria recutita', 'matricaria chamomilla')
    line = line.replace('chamomilla recutita', 'matricaria chamomilla')
    return line


def herbs_auto_id_next():
    herbs_auto_rows = util.csv_get_rows(g.CSV_HERBS_AUTO_FILEPATH)
    herbs_auto_cols = util.csv_get_cols(herbs_auto_rows)
    herbs_auto_rows = herbs_auto_rows[1:]

    id_last = 0
    for herb_auto_row in herbs_auto_rows:
        _id = herb_auto_row[herbs_auto_cols['herb_id']]
        if id_last < int(_id):
            id_last = int(_id)
    id_next = id_last + 1
    return id_next



##################################################################################
# ;PREPARATIONS
##################################################################################

def gen_preparations(preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        prompts = [
            f'''
                Write a numbered list of the 20 best herbal {preparation_name} for {status_name}.
                Follow the GUIDELINES below.
                ## GUIDELINES
                List only the herbs that are the most common, used, safe, and legal.
                Don't list herbs that are considered toxic, poisonous, dangerous, and considered illegal in many countries.
                For each herb in the list, write both the scientific (botanical, latin) name and the common name.
                Also, for each herbs explain why it's good for {status_name} in as few words as possible.
                Don't includ additional content, reply only with the list.
                Order the herbs from the most effective with {status_name} to the least.
            ''', 
        ]
        for prompt in prompts:
            if preparation_slug == 'teas':
                filepath = g.CSV_STATUS_PREPARATIONS_TEAS_FILEPATH
                preparations_rows = util.csv_get_rows_filtered(
                    filepath, status_preparations_teas_cols['status_id'], status_id
                )
            elif preparation_slug == 'tinctures':
                filepath = g.CSV_STATUS_PREPARATIONS_TINCTURES_FILEPATH
                preparations_rows = util.csv_get_rows_filtered(
                    filepath, status_preparations_tinctures_cols['status_id'], status_id
                )
            elif preparation_slug == 'decoctions':
                filepath = g.CSV_STATUS_PREPARATIONS_DECOCTIONS_FILEPATH
                preparations_rows = util.csv_get_rows_filtered(
                    filepath, status_preparations_decoctions_cols['status_id'], status_id
                )
            elif preparation_slug == 'essential-oils':
                filepath = g.CSV_STATUS_PREPARATIONS_ESSENTIAL_OILS_FILEPATH
                preparations_rows = util.csv_get_rows_filtered(
                    filepath, status_preparations_essential_oils_cols['status_id'], status_id
                )
            elif preparation_slug == 'capsules':
                filepath = g.CSV_STATUS_PREPARATIONS_CAPSULES_FILEPATH
                preparations_rows = util.csv_get_rows_filtered(
                    filepath, status_preparations_capsules_cols['status_id'], status_id
                )
            else:
                print('preparation not managed')
                quit()
            if preparations_rows == []:
                print(f'> {status_row}')
                print(prompts[0])
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
                    line = herb_sanitize(line)
                    # check if line "in" trefle csv
                    trefle_found = False
                    for trefle_row in trefle_rows:
                        trefle_slug = trefle_row[trefle_cols['herb_slug']]
                        trefle_name_scientific = trefle_row[trefle_cols['herb_name_scientific']]
                        trefle_words = trefle_slug.split('-')
                        found = True
                        for word in trefle_words:
                            if word not in line:
                                found = False
                                break
                        if found:
                            print(trefle_slug, '>>', line)
                            trefle_found = True
                            break
                    if trefle_found: 
                        # check if not duplicate elements in same reply
                        old_line_found = False
                        for line_old in lines:
                            if line_old[status_preparations_teas_cols['remedy_slug']] == trefle_slug:
                                old_line_found = True
                        # check if herb is in database and has id, if not create
                        if not old_line_found:
                            herbs_auto_rows_filtered = util.csv_get_rows_filtered(
                                g.CSV_HERBS_AUTO_FILEPATH, herbs_auto_cols['herb_slug'], trefle_slug
                            )
                            herb_auto_id = 0
                            if herbs_auto_rows_filtered != []:
                                herb_auto_row = herbs_auto_rows_filtered[0]
                                herb_auto_id = herb_auto_row[herbs_auto_cols['herb_id']]
                            else:
                                herb_auto_id = herbs_auto_id_next()
                                util.csv_add_rows(
                                    g.CSV_HERBS_AUTO_FILEPATH, 
                                    [[herb_auto_id, trefle_slug, trefle_name_scientific]]
                                )
                            lines.append([status_id, status_slug, herb_auto_id, trefle_slug])
                    else:
                        util.file_append('LOG_CSV_STATUS_PREPARATIONS_TEAS_FILEPATH.txt', f'{line}\n')
                if len(lines) >= 10:
                    print('***************************************************')
                    print(lines)
                    print('***************************************************')
                    util.csv_add_rows(filepath, lines)





##################################################
# ;STATUS
##################################################

def gen_status__herbs():
    i = 0
    for status_row in status_rows:
        if i >= 1: break
        status_exe = status_row[status_cols['status_exe']].strip().lower()
        status_id = status_row[status_cols['status_id']].strip().lower()
        status_slug = status_row[status_cols['status_slug']].strip().lower()
        status_name = status_row[status_cols['status_names']].split(',')[0].strip().lower()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        status_herbs_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_STATUS_HERBS_FILEPATH, status_herbs_cols['status_id'], status_id,
        )
        if status_herbs_rows_filtered == []:
            print(f'> {status_row}')
            prompts = [
                f'''
                    Write a numbered list of the 20 best herbs for {status_name}.
                    GUIDELINES
                    List only the most common, used, safe, and legal herbs.
                    Don't list potentially poisonous herbs.
                    Don't list herbs that are illegal in many countries.
                    Write only the scientific (botanical, latin) names of the herbs first and then the common name.
                    Don't add descriptions of the herbs.
                    Order the herbs from the most effective with {status_name} to the least.
                ''',
            ]
            prompt = prompts[0]
            print(prompts[0])
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
                line = herb_sanitize(line)
                # check if line "in" trefle csv
                trefle_found = False
                for trefle_row in trefle_rows:
                    trefle_slug = trefle_row[trefle_cols['herb_slug']]
                    trefle_name_scientific = trefle_row[trefle_cols['herb_name_scientific']]
                    trefle_words = trefle_slug.split('-')
                    found = True
                    for word in trefle_words:
                        if word not in line:
                            found = False
                            break
                    if found:
                        print(trefle_slug, '>>', line)
                        trefle_found = True
                        break
                if trefle_found: 
                    # check if not duplicate elements in same reply
                    old_line_found = False
                    for line_old in lines:
                        if line_old[status_preparations_teas_cols['remedy_slug']] == trefle_slug:
                            old_line_found = True
                    # check if herb is in database and has id, if not create
                    if not old_line_found:
                        herbs_auto_rows_filtered = util.csv_get_rows_filtered(
                            g.CSV_HERBS_AUTO_FILEPATH, herbs_auto_cols['herb_slug'], trefle_slug
                        )
                        herb_auto_id = 0
                        if herbs_auto_rows_filtered != []:
                            herb_auto_row = herbs_auto_rows_filtered[0]
                            herb_auto_id = herb_auto_row[herbs_auto_cols['herb_id']]
                        else:
                            herb_auto_id = herbs_auto_id_next()
                            util.csv_add_rows(
                                g.CSV_HERBS_AUTO_FILEPATH, 
                                [[herb_auto_id, trefle_slug, trefle_name_scientific]]
                            )
                        lines.append([status_id, status_slug, herb_auto_id, trefle_slug])
                else:
                    util.file_append('LOG_CSV_STATUS__HERBS.txt', f'{line}\n')
            if len(lines) >= 10:
                print('***************************************************')
                print(lines)
                print('***************************************************')
                util.csv_add_rows(g.CSV_STATUS_HERBS_FILEPATH, lines)


    
        
        




##################################################
# ;HERBS
##################################################

def gen_herbs_medicine_benefits():
    for herb_row in herbs_auto_rows:
        herbs_benefits_rows = util.csv_get_rows(g.CSV_HERBS_BENEFITS_FILEPATH)
        herbs_benefits_cols = util.csv_get_cols(herbs_benefits_rows)
        herbs_benefits_headers = herbs_benefits_rows[0]
        herbs_benefits_rows = herbs_benefits_rows[1:]

        herb_id = herb_row[herbs_auto_cols['herb_id']].strip().lower()
        herb_slug = herb_row[herbs_auto_cols['herb_slug']].strip().lower()
        herb_name_scientific = herb_row[herbs_auto_cols['herb_name_scientific']].strip().lower()

        if herb_id == '': continue
        if herb_slug == '': continue
        if herb_name_scientific == '': continue

        # print(f'> {herb_row}')

        herbs_names_common_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_HERBS_NAMES_COMMON_FILEPATH, herbs_names_common_cols['herb_id'], herb_id
        )
        herb_name_common = herbs_names_common_rows_filtered[0][herbs_names_common_cols['herb_name_common']]

        herbs_benefits_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_HERBS_BENEFITS_FILEPATH, herbs_benefits_cols['herb_id'], herb_id
        )

        # exists?
        if herbs_benefits_rows_filtered != []:
            # to remove?
            to_remove = False
            for herb_benefit_row in herbs_benefits_rows_filtered:
                benefit_name = herb_benefit_row[herbs_benefits_cols['benefit_name']]
                if len(benefit_name.split(' ')) > 5:
                    to_remove = True
                    break

            if to_remove:
                herbs_benefits_rows_to_keep = [herbs_benefits_headers]
                herbs_benefits_rows_to_remove = []

                for herb_benefit_row in herbs_benefits_rows:
                    herb_id_to_filter = herb_benefit_row[herbs_benefits_cols['herb_id']]
                    if herb_id_to_filter == herb_id:
                        herbs_benefits_rows_to_remove.append(herb_benefit_row)
                    else:
                        herbs_benefits_rows_to_keep.append(herb_benefit_row)

                util.csv_set_rows(g.CSV_HERBS_BENEFITS_FILEPATH, herbs_benefits_rows_to_keep)



        herbs_benefits_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_HERBS_BENEFITS_FILEPATH, herbs_benefits_cols['herb_id'], herb_id
        )

        if herbs_benefits_rows_filtered == []:
            prompt = f'''
                Write a numbered list of the 15 best health benefits of the herb {herb_name_common} ({herb_name_scientific}).
                Write only the names of the benefits, not the descriptions.
                Write as few words as possible.
                Write each benefit in less than 5 words.
                Start each list item with a third person singular action verb.
                Include only proven factual benefits.
                Don't include the following words: can, may, might.
            '''
            reply = utils_ai.gen_reply(prompt)

            lines = []
            for line in reply.split('\n'):
                line = line.strip().lower()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '-' in line: continue
                if '.' not in line: continue
                line = '.'.join(line.split('.')[1:])
                if ':' in line: line = line.split(':')[0]
                if line == '': continue
                line = line.split('(')[0]
                line = line.replace('.', '')
                line = line.strip()
                if line.split(' ')[0][-1] != 's': continue
                if line == '': continue
                if len(line.split(' ')) > 5: continue
                lines.append([herb_id, herb_name_scientific, line])

            if len(lines) >= 10:
                print('***************************************************')
                print(lines)
                print('***************************************************')
                util.csv_add_rows(g.CSV_HERBS_BENEFITS_FILEPATH, lines)

            time.sleep(g.PROMPT_DELAY_TIME)


def gen_herbs_names_common():
    herbs_auto_rows = util.csv_get_rows(g.CSV_HERBS_AUTO_FILEPATH)
    herbs_auto_cols = util.csv_get_cols(herbs_auto_rows)
    herbs_auto_rows = herbs_auto_rows[1:]
    for herb_row in herbs_auto_rows:
        herb_id = herb_row[herbs_auto_cols['herb_id']].strip()
        herb_slug = herb_row[herbs_auto_cols['herb_slug']].strip()
        herb_name_scientific = herb_row[herbs_auto_cols['herb_name_scientific']].strip()
        if herb_id == '': continue
        if herb_slug == '': continue
        if herb_name_scientific == '': continue
        herbs_names_common_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_HERBS_NAMES_COMMON_FILEPATH, herbs_names_common_cols['herb_id'], herb_id
        )
        if herbs_names_common_rows_filtered == []:
            print(f'> {herb_row}')
            prompt = f'''
                Write a numbered list of the common names of the herb: {herb_name_scientific}.
                Follow the GUIDELINES below.

                GUIDELINES
                Write only the names, not the descriptions.
                Write only the most used common names.
                List the common names from the most used to the least.
                Write as few words as possible.
                Don't write scientific names, only common names.
                Include less than 10 common names.
            '''
            reply = utils_ai.gen_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip().lower()
                if line == '': continue
                if ':' in line: continue
                if not line[0].isdigit(): continue
                if '.' not in line: continue
                line = '.'.join(line.split('.')[1:])
                line = line.split('(')[0]
                line = line.replace('.', '')
                line = line.strip()
                if line == '': continue
                lines.append([herb_id, herb_slug, line])
            if len(lines) >= 1:
                print('***************************************************')
                print(lines)
                print('***************************************************')
                util.csv_add_rows(g.CSV_HERBS_NAMES_COMMON_FILEPATH, lines)


def get_system_by_status(status_id):
    system_row = []

    status_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_STATUS_SYSTEMS_FILEPATH, status_systems_cols['status_id'], status_id,
    )

    if status_systems_rows_filtered != []:
        status_system_row = status_systems_rows_filtered[0]
        system_id = status_system_row[status_systems_cols['system_id']]

        systems_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id,
        )

        if systems_rows_filtered != []:
            system_row = systems_rows_filtered[0]

    return system_row


def gen_system_for_status():
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']].strip().lower()
        status_id = status_row[status_cols['status_id']].strip().lower()
        status_slug = status_row[status_cols['status_slug']].strip().lower()
        status_name = status_row[status_cols['status_names']].split(',')[0].strip().lower()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        status_systems_rows = get_system_by_status(status_id)
        if status_systems_rows == []:
            print(f'> {status_row}')
            systems_names = [row[systems_cols['system_name']] for row in systems_rows]
            systems_names_prompt = ', '.join(systems_names)
            prompt = f'''
                In which body system would you classify the following problem: {status_name}.
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
                util.csv_add_rows(
                    g.CSV_STATUS_SYSTEMS_FILEPATH, 
                    [[status_id, status_name, system_id, system_name]]
                )

def gen_status__preparations():
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']].strip().lower()
        status_id = status_row[status_cols['status_id']].strip().lower()
        status_slug = status_row[status_cols['status_slug']].strip().lower()
        status_name = status_row[status_cols['status_names']].split(',')[0].strip().lower()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        rows_filtered = util.csv_get_rows_filtered(
            g.CSV_STATUS_PREPARATIONS_FILEPATH, status_preparations_cols['status_id'], status_id
        )
        if rows_filtered == []:
            print(f'> {status_row}')
            prompt = f'''
                Write a numbered list of the 20 most effective type of herbal preparations for {status_name}.
                ## GUIDELINES
                Write only the names of the types of the preparations, not the descriptions, not the herbs names.
                Write the names of the types of the preparations in plural.
                Example of types of preparations can be teas, decoctions and tinctures.
                Order the list items from the most common and easy to make preparation, to the least.
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
                if line == 'infusions': continue 
                preparations_rows_filtered = util.csv_get_rows_filtered(
                    g.CSV_PREPARATIONS_FILEPATH, preparations_cols['preparation_name'], line
                )
                if preparations_rows_filtered != []:
                    preparation_row = preparations_rows_filtered[0]
                    preparation_id = preparation_row[preparations_cols['preparation_id']]
                    lines.append([status_id, status_name, preparation_id, line])
                else:
                    util.file_append('logs/preparations_not_in_database.txt', f'{line}\n')
            if len(lines) >= 10:
                print('***************************************************')
                print(lines)
                print('***************************************************')
                util.csv_add_rows(g.CSV_STATUS_PREPARATIONS_FILEPATH, lines)



def redirect_old_plants():
    plants_primary_rows = util.csv_get_rows('database/tables/plants.csv')
    plants_secondary_rows = util.csv_get_rows('database/tables/plants-secondary.csv')
    plants_rows = []
    for plant_row in plants_primary_rows:
        plants_rows.append(plant_row)
    for plant_row in plants_secondary_rows:
        plants_rows.append(plant_row)
    for plant_row in plants_rows[1:]:
        plant_name_scientific = plant_row[0].capitalize()      
        plant_slug = plant_name_scientific.strip().lower().replace(' ', '-')
        '''
        found = False
        for trefle_row in trefle_rows:
            trefle_name_scientific = trefle_row[trefle_cols['herb_name_scientific']]
            if plant_name_scientific.lower().strip() == trefle_name_scientific.lower().strip():
                found = True
        '''
        found = False
        for herb_auto_row in herbs_auto_rows:
            herb_name_scientific = herb_auto_row[herbs_auto_cols['herb_name_scientific']]
            if plant_name_scientific.lower().strip() == herb_name_scientific.lower().strip():
                found = True
                print(herb_auto_row)
                break
        if found:
            print(f'- {plant_name_scientific}')
        else:
            herb_auto_id = herbs_auto_id_next()
            util.csv_add_rows(
                g.CSV_HERBS_AUTO_FILEPATH, 
                [[herb_auto_id, plant_slug, plant_name_scientific]]
            )
            print(f'X {plant_name_scientific}')



##################################################
# EXE
##################################################

# redirect_old_plants() ## TODO: did one time, don't do it again

gen_system_for_status()

gen_status__herbs()
gen_status__preparations()
# quit()

# gen_csvs()

gen_preparations('teas')
gen_preparations('decoctions')
gen_preparations('tinctures')
gen_preparations(preparation_slug='essential-oils')
gen_preparations('capsules')

gen_herbs_names_common()

# gen_herbs_medicine_benefits()
