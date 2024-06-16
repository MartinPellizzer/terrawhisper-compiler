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

trefle_rows = util.csv_get_rows(g.CSV_TREFLE_FILEPATH)
trefle_cols = util.csv_get_cols(trefle_rows)
trefle_rows = trefle_rows[1:]

herbs_auto_rows = util.csv_get_rows(g.CSV_HERBS_AUTO_FILEPATH)
herbs_auto_cols = util.csv_get_cols(herbs_auto_rows)
herbs_auto_rows = herbs_auto_rows[1:]

status_rows = util.csv_get_rows(g.CSV_STATUS_FILEPATH)
status_cols = util.csv_get_cols(status_rows)
status_rows = status_rows[1:]


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

herbs_benefits_rows = util.csv_get_rows(g.CSV_HERBS_BENEFITS_FILEPATH)
herbs_benefits_cols = util.csv_get_cols(herbs_benefits_rows)
herbs_benefits_rows = herbs_benefits_rows[1:]

herbs_names_common_rows = util.csv_get_rows(g.CSV_HERBS_NAMES_COMMON_FILEPATH)
herbs_names_common_cols = util.csv_get_cols(herbs_names_common_rows)
herbs_names_common_rows = herbs_names_common_rows[1:]

problems_herbs_auto_rows = util.csv_get_rows(g.CSV_PROBLEMS_HERBS_AUTO_FILEPATH)
problems_herbs_auto_cols = util.csv_get_cols(problems_herbs_auto_rows)
problems_herbs_auto_rows = problems_herbs_auto_rows[1:]


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

status_preparations_capsules_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_CAPSULES_FILEPATH)
status_preparations_capsules_cols = util.csv_get_cols(status_preparations_capsules_rows)
status_preparations_capsules_rows = status_preparations_capsules_rows[1:]

status_preparations_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_FILEPATH)
status_preparations_cols = util.csv_get_cols(status_preparations_rows)
status_preparations_rows = status_preparations_rows[1:]






# def sanitize_herbs(line):
#     line = line.replace('licorice root', 'licorice')
#     line = line.replace('ginger root', 'ginger')
#     line = line.replace('marshmallow root', 'marshmallow')
#     line = line.replace('slippery elm bark', 'slippery elm')
#     line = line.replace('cloves', 'clove')
#     line = line.replace('tea tree oil', 'tea tree')
#     line = line.replace('wild oregano', 'oregano')
#     line = line.replace('raspberry leaf', 'raspberry')
#     line = line.replace('oak bark', 'oak')
#     if line == 'hop': line = 'hops'
#     if line == 'kava': line = 'kava kava'
#     if line == 'willow bark': line = 'willow'
#     if line == 'valerian root': line = 'valerian'
#     if line == 'eleuthero': line = 'siberian ginseng'
#     if line == 'milky oat seed': line = 'oat straw'
#     if line == 'milky oat tops': line = 'oat straw'
#     if line == 'milky oat': line = 'oat straw'
#     if line == 'rhodiola rosea': line = 'golden root'
#     if line == 'schisandra': line = 'magnolia vines'
#     if line == 'rhodiola': line = 'golden root'
#     if line == 'saint john\'s wort': line = 'st. john\'s wort'
#     if line == 'flaxseed': line = 'flax'
#     if line == 'black caraway': line = 'black seed'
#     if line == 'rehmannia': line = 'chinese foxglove'
#     if line == 'water-peony': line = 'peony'
#     if line == 'olive leaf': line = 'olive'
#     if line == 'viscum album': line = 'mistletoe'
#     if line == 'crataegus': line = 'hawthorn'
#     if line == 'fennel seed': line = 'fennel'
#     if line == 'red raspberry': line = 'raspberry'
#     if line == 'burdock root': line = 'burdock'
#     if line == 'aloe': line = 'aloe vera'
#     if line == 'cascara': line = 'cascara sagrada'
#     if line == 'osha root': line = 'osha'
#     if line == 'cayenne': line = 'cayenne pepper'
#     if line == 'wild cherry': line = 'cherry'
#     if line == 'wild cherry bark': line = 'cherry'
#     if line == 'grindelia': line = 'gumweed'
#     if line == 'aniseed': line = 'anise'
#     if line == 'cowslip': line = 'primrose'
#     if line == 'baptisia tinctoria': line = 'wild indigo'
#     if line == 'blackberry root': line = 'blackberry'
#     if line == 'blackberry leaf': line = 'blackberry'
#     if line == 'blueberry leaves': line = 'blueberry'
#     if line == 'blueberry leaf': line = 'blueberry'
#     if line == 'birch leaf': line = 'birch'
#     if line == 'strawberry leaf': line = 'strawberry'
#     if line == 'bearberry leaf': line = 'bearberry'
#     if line == 'oregon grape root': line = 'oregon grape'
#     if line == 'red raspberry leaves': line = 'raspberry'
#     if line == 'capsicum': line = 'cayenne pepper'
#     if line == 'boswellia': line = 'frankincense'
#     if line == 'stinging nettle': line = 'nettle'
#     if line == 'elderflower': line = 'elderberry'
#     if line == 'ginkgo': line = 'ginkgo biloba'
#     if line == 'gingko biloba': line = 'ginkgo biloba'
#     if line == 'poke': line = 'pokeweed'
#     if line == 'poke root': line = 'pokeweed'
#     if line == 'astragalus': line = 'milkvetch'
#     if line == 'baptisia': line = 'wild indigo'
#     if line == 'pleurisy root': line = 'butterfly weed'
#     if line == 'angelica root': line = 'angelica'
#     if line == 'linden flower': line = 'linden'
#     if line == 'linden flower': line = 'linden'
#     if line == 'celery seed': line = 'celery'
#     if line == 'cascara sagrada': line = 'cascara'
#     if line == 'artemisia': line = 'mugwort'
#     if line == 'ivy leaf': line = 'ivy'
#     if line == 'usnea': line = 'beard lichens'
#     if line == 'plantain leaf': line = 'plantain'
#     if line == 'chamomile flower': line = 'chamomile'
#     if line == 'chia seeds': line = 'chia'
#     if line == 'chia seed': line = 'chia'
#     if line == 'rosehips': line = 'rosehip'
#     if line == 'chicory root': line = 'chicory'
#     if line == 'dandelion root': line = 'dandelion'
#     if line == 'nettle leaf': line = 'nettle'
#     if line == 'uva ursi': line = 'bearberry'
#     if line == 'cornsilk': line = 'corn silk'
#     if line == 'artichoke leaf': line = 'artichoke'
#     if line == 'hawthorn berry': line = 'hawthorn'

#     return line


def herb_sanitize(line):
    if line == 'mentha piperita': line = 'mentha x piperita'
    if line == 'matricaria recutita': line = 'matricaria chamomilla'
    if line == 'chamomilla recutita': line = 'matricaria chamomilla'
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



def remedies_systems_status_preparations(preparation_slug):
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

        print(f'> {status_row}')

        prompts = [
            f'''
                Write a numbered list of the 30 best scientific name (botanical latin binomial) of herbal {preparation_name} for {status_name}.
                Write only the scientific names of the plants, not the descriptions.
                Don't write the common name.
            ''', 
            f'''
                Write a numbered list of the 30 best scientific name of herbal {preparation_name} for {status_name}.
                Write only the scientific names of the plants, not the descriptions.
                Don't write the common name.
            ''', 
            f'''
                Write a numbered list of the 20 best scientific name (botanical latin binomial) of herbal {preparation_name} for {status_name}.
                Write only the scientific names of the plants, not the descriptions.
                Don't write the common name.
            ''', 
            f'''
                Write a list of the 30 best of herbal {preparation_name} that help with {status_name}.
                Write only the scientific names of the herbs, not the descriptions.
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
            elif preparation_slug == 'capsules':
                filepath = g.CSV_STATUS_PREPARATIONS_CAPSULES_FILEPATH
                preparations_rows = util.csv_get_rows_filtered(
                    filepath, status_preparations_capsules_cols['status_id'], status_id
                )
            else:
                print('preparation not managed')
                quit()
            
            if preparations_rows == []:
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

                time.sleep(g.PROMPT_DELAY_TIME)



# def csv_gen_herbs_for_problem(problem_row):
#     problem_id = problem_row[problems_cols['problem_id']]
#     problem_slug = problem_row[problems_cols['problem_slug']]
#     problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

#     problems_herbs_rows = util.csv_get_rows_filtered(
#         g.CSV_PROBLEMS_HERBS_FILEPATH, problems_herbs_cols['problem_id'], problem_id
#     )

#     if problems_herbs_rows == []:
#         prompt = f'''
#             Write a numbered list of 20 medicinal herbs for {problem_name}.
#             Write only the names of the herbs, not the descriptions.
#             Don't write the parts of the herbs.
#         '''
#         reply = utils_ai.gen_reply(prompt)

#         lines = []
#         for line in reply.split('\n'):
#             line = line.strip().lower()
#             if line == '': continue
#             if not line[0].isdigit(): continue
#             if '.' not in line: continue
#             line = '.'.join(line.split('.')[1:])
#             line = line.split('(')[0]
#             line = line.strip()
#             if line == '': continue

#             line = sanitize_herbs(line)

#             found = False
#             for line_added in lines:
#                 if line == line_added[3]:
#                     found = True
#                     break
#             if found: continue

#             herbs_rows_filtered = util.csv_get_rows_filtered(
#                 g.CSV_HERBS_FILEPATH, herbs_cols['herb_name_common'], line
#             )
#             if herbs_rows_filtered != []:
#                 herb_row = herbs_rows_filtered[0]
#                 herb_id = herb_row[herbs_cols['herb_id']]
#             else:
#                 herb_id = ''

#             for item in lines:
#                 if item[3] == line:
#                     continue

#             lines.append([problem_id, problem_slug, herb_id, line])

#         if len(lines) >= 10:
#             print('***************************************************')
#             print(lines)
#             print('***************************************************')
#             util.csv_add_rows(g.CSV_PROBLEMS_HERBS_FILEPATH, lines)

#         print(problem_id, problem_slug, problem_name)
#         time.sleep(g.PROMPT_DELAY_TIME)


# def csv_get_system_by_problem(problem_id):
#     system_row = []

#     problems_systems_rows_filtered = util.csv_get_rows_filtered(
#         g.CSV_PROBLEMS_SYSTEMS_FILEPATH, problems_systems_cols['problem_id'], problem_id,
#     )

#     if problems_systems_rows_filtered != []:
#         problem_system_row = problems_systems_rows_filtered[0]
#         system_id = problem_system_row[problems_systems_cols['system_id']]

#         systems_rows_filtered = util.csv_get_rows_filtered(
#             g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id,
#         )

#         if systems_rows_filtered != []:
#             system_row = systems_rows_filtered[0]

#     return system_row


# def csv_gen_preparations_for_problem(problem_row):
#     problem_id = problem_row[problems_cols['problem_id']]
#     problem_slug = problem_row[problems_cols['problem_slug']]
#     problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

#     problems_preparations_rows = util.csv_get_rows_filtered(
#         g.CSV_PROBLEMS_PREPARATIONS_FILEPATH, problems_preparations_cols['problem_id'], problem_id
#     )

#     if problems_preparations_rows == []:
#         prompt = f'''
#             Write a numbered list of the 15 most effective type of herbal preparations for {problem_name}.
#             Write only the names of the types of the preparations, not the descriptions.
#             Write only the names of the types of the preparations, not the herbs names.
#             Example of types of preparations can be infusions and tinctures.
#         '''
#         reply = utils_ai.gen_reply(prompt)

#         lines = []
#         for line in reply.split('\n'):
#             line = line.strip().lower()
#             if line == '': continue
#             if not line[0].isdigit(): continue
#             if '.' not in line: continue
#             line = '.'.join(line.split('.')[1:])
#             line = line.strip()
#             if line == '': continue
            
#             if 'tea' in line: continue
#                 # if 'infusions' in lines:
#                 #     continue

#             preparations_rows_filtered = util.csv_get_rows_filtered(
#                 g.CSV_PREPARATIONS_FILEPATH, preparations_cols['preparation_name'], line
#             )
#             if preparations_rows_filtered != []:
#                 preparation_row = preparations_rows_filtered[0]
#                 preparation_id = preparation_row[preparations_cols['preparation_id']]
#             else:
#                 preparation_id = ''

#             lines.append([problem_id, problem_slug, preparation_id, line])

#         if len(lines) >= 10:
#             print('***************************************************')
#             print(lines)
#             print('***************************************************')
#             util.csv_add_rows(g.CSV_PROBLEMS_PREPARATIONS_FILEPATH, lines)

#         time.sleep(g.PROMPT_DELAY_TIME)




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

        print(f'> {herb_row}')

        herbs_names_common_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_HERBS_NAMES_COMMON_FILEPATH, herbs_names_common_cols['herb_id'], herb_id
        )

        if herbs_names_common_rows_filtered == []:
            prompt = f'''
                Write a numbered list of the most common names of {herb_name_scientific}.
                Write only the names, not the descriptions.
                Write as few words as possible.
                Don't write scientific names.
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

            time.sleep(g.PROMPT_DELAY_TIME)
        



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


def gen_system_for_status(status_row):
    status_id = status_row[status_cols['status_id']]
    status_slug = status_row[status_cols['status_slug']]
    status_name = status_row[status_cols['status_names']].split(',')[0].strip()

    status_systems_rows = get_system_by_status(status_id)

    if status_systems_rows == []:
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

        time.sleep(g.PROMPT_DELAY_TIME)


# def gen_preparations_for_status(status_row):
#     status_id = status_row[status_cols['status_id']]
#     status_slug = status_row[status_cols['status_slug']]
#     status_name = status_row[status_cols['status_names']].split(',')[0].strip()

#     rows_filtered = util.csv_get_rows_filtered(
#         g.CSV_STATUS_PREPARATIONS_FILEPATH, status_preparations_cols['status_id'], status_id
#     )

#     if rows_filtered == []:
#         prompt = f'''
#             Write a numbered list of the 20 most effective type of herbal preparations for {status_name}.
#             Write only the names of the types of the preparations, not the descriptions.
#             Write only the names of the types of the preparations, not the herbs names.
#             Write the names of the types of the preparations in plural.
#             Example of types of preparations can be teas, decoctions and tinctures.
#         '''
#         reply = utils_ai.gen_reply(prompt)

#         lines = []
#         for line in reply.split('\n'):
#             line = line.strip().lower()
#             if line == '': continue
#             if not line[0].isdigit(): continue
#             if '.' not in line: continue
#             line = '.'.join(line.split('.')[1:])
#             line = line.strip()
#             if line == '': continue

#             if line == 'infusions': continue 
#                 # line = 'teas'
#             # if line in lines: continue

#             preparations_rows_filtered = util.csv_get_rows_filtered(
#                 g.CSV_PREPARATIONS_FILEPATH, preparations_cols['preparation_name'], line
#             )
#             if preparations_rows_filtered != []:
#                 preparation_row = preparations_rows_filtered[0]
#                 preparation_id = preparation_row[preparations_cols['preparation_id']]
#                 lines.append([status_id, status_name, preparation_id, line])
#             else:
#                 util.file_append('logs/preparations_not_in_database.txt', f'{line}\n')

#         if len(lines) >= 10:
#             print('***************************************************')
#             print(lines)
#             print('***************************************************')
#             util.csv_add_rows(g.CSV_STATUS_PREPARATIONS_FILEPATH, lines)

#         time.sleep(g.PROMPT_DELAY_TIME)





##################################################
# EXE
##################################################

def gen_csvs():
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']].strip().lower()
        status_id = status_row[status_cols['status_id']].strip().lower()
        status_slug = status_row[status_cols['status_slug']].strip().lower()
        status_name = status_row[status_cols['status_names']].split(',')[0].strip().lower()

        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue

        print(f'> {status_row}')

        gen_system_for_status(status_row)




gen_csvs()

remedies_systems_status_preparations('teas')
remedies_systems_status_preparations('tinctures')
remedies_systems_status_preparations('capsules')

gen_herbs_names_common()

gen_herbs_medicine_benefits()