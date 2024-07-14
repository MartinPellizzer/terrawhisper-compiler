import random

import g
import util
import data_csv

# TABLES
status_rows, status_cols = data_csv.status()

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]


# TABLES JUNCTIONS
status_systems_rows = util.csv_get_rows(g.CSV_STATUS_SYSTEMS_FILEPATH)
status_systems_cols = util.csv_get_cols(status_systems_rows)
status_systems_rows = status_systems_rows[1:]


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
    
    

def test_preparations(preparation_slug):
    parts_num_min = 999
    parts_num_max = 0
    parts_names = []
    parts_desc_num_words_min = 999
    parts_desc_num_words_max = 0
    part_desc_shortest = ''
    part_desc_longest = ''
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue
        json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/{preparation_slug}.json'
        data = util.json_read(json_filepath)
        print(f'-----------------------{status_name}-----------------------')
        print()
        for obj in data['remedies_list']:
            herb_name_common = obj['herb_name_common']
            if 'remedy_parts' in obj:
                remedy_parts = obj['remedy_parts']
                print(f'>>> {herb_name_common}')
                print()
                for remedy_part in remedy_parts:
                    print(remedy_part)
                    print()
                    remedy_part_name = remedy_part.split(':')[0]
                    remedy_part_desc = remedy_part.split(':')[1]
                    if remedy_part_name not in parts_names:
                        parts_names.append(remedy_part_name)
                    remedy_part_desc_words = remedy_part_desc.split(' ')
                    remedy_part_desc_num_words = len(remedy_part_desc_words)
                    if parts_desc_num_words_min > remedy_part_desc_num_words: 
                        parts_desc_num_words_min = remedy_part_desc_num_words
                        part_desc_shortest = remedy_part_desc
                    if parts_desc_num_words_max < remedy_part_desc_num_words: 
                        parts_desc_num_words_max = remedy_part_desc_num_words
                        part_desc_longest = remedy_part_desc
                print()
                print()
                parts_num = len(remedy_parts)
                if parts_num_min > parts_num: parts_num_min = parts_num
                if parts_num_max < parts_num: parts_num_max = parts_num
        print()
        print()
        print()
    print(f'parts_num_min: {parts_num_min}')
    print(f'parts_num_max: {parts_num_max}')
    print(f'parts_names: {parts_names}')
    print(f'parts_desc_num_words_min: {parts_desc_num_words_min}')
    print(f'parts_desc_num_words_max: {parts_desc_num_words_max}')
    print(f'part_desc_shortest: {part_desc_shortest}')
    print(f'part_desc_longest: {part_desc_longest}')

def test_preparations_descriptions(preparation_slug, purge):
    words_num_min = 999
    words_num_max = 0
    errors_wrong_plant = 0
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        system_row = get_system_by_status(status_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue
        json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/{preparation_slug}.json'
        data = util.json_read(json_filepath)
        for obj in data['remedies_list']:
            if 'remedy_desc' in obj:
                herb_name_common = obj['herb_name_common']
                remedy_desc = obj['remedy_desc']
                if not remedy_desc.lower().startswith(herb_name_common.lower()):
                    print(f'-----------------------{status_name}-----------------------')
                    print(f'>>> {herb_name_common}')
                    print(' '.join(remedy_desc.split(' ')[:10]))
                    print()
                    errors_wrong_plant += 1
                    if purge:
                        del obj['remedy_desc']
                words = remedy_desc.split(' ')
                words_num = len(words)
                if words_num_min > words_num: words_num_min = words_num
                if words_num_max < words_num: words_num_max = words_num
        util.json_write(json_filepath, data)
    print(f'words_num_min: {words_num_min}')
    print(f'words_num_max: {words_num_max}')
    print(f'errors_wrong_plant: {errors_wrong_plant}')


def test_preparations_properties(preparation_slug):
    parts_num_min = 999
    parts_num_max = 0
    parts_names = []
    parts_desc_num_words_min = 999
    parts_desc_num_words_max = 0
    part_desc_shortest = ''
    part_desc_longest = ''
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        system_row = get_system_by_status(status_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue
        json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/{preparation_slug}.json'
        print(json_filepath)
        data = util.json_read(json_filepath)
        print(f'-----------------------{status_name}-----------------------')
        print()
        for obj in data['remedies_list']:
            herb_name_common = obj['herb_name_common']
            if 'remedy_properties' in obj:
                remedy_parts = obj['remedy_properties']
                print(f'>>> {herb_name_common}')
                print()
                for remedy_part in remedy_parts:
                    print(remedy_part)
                    print()
                    remedy_part_name = remedy_part.split(':')[0]
                    remedy_part_desc = remedy_part.split(':')[1]
                    if remedy_part_name not in parts_names:
                        parts_names.append(remedy_part_name)
                    remedy_part_desc_words = remedy_part_desc.split(' ')
                    remedy_part_desc_num_words = len(remedy_part_desc_words)
                    if parts_desc_num_words_min > remedy_part_desc_num_words: 
                        parts_desc_num_words_min = remedy_part_desc_num_words
                        part_desc_shortest = remedy_part_desc
                    if parts_desc_num_words_max < remedy_part_desc_num_words: 
                        parts_desc_num_words_max = remedy_part_desc_num_words
                        part_desc_longest = remedy_part_desc
                print()
                print()
                parts_num = len(remedy_parts)
                if parts_num_min > parts_num: parts_num_min = parts_num
                if parts_num_max < parts_num: parts_num_max = parts_num
        print()
        print()
        print()
    print(f'parts_num_min: {parts_num_min}')
    print(f'parts_num_max: {parts_num_max}')
    print(f'parts_names: {parts_names}')
    print(f'parts_desc_num_words_min: {parts_desc_num_words_min}')
    print(f'parts_desc_num_words_max: {parts_desc_num_words_max}')
    print(f'part_desc_shortest: {part_desc_shortest}')
    print(f'part_desc_longest: {part_desc_longest}')

def test_preparations_recipe(preparation_slug, purge):
    item_words_num_min = 999
    item_words_num_max = 0
    item_smallest = ''
    item_longest = ''
    missing_obj_num = 0
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        system_row = get_system_by_status(status_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue
        json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/{preparation_slug}.json'
        print(json_filepath)
        data = util.json_read(json_filepath)
        print(f'-----------------------{status_name}-----------------------')
        print()
        for i, obj in enumerate(data['remedies_list']):
            herb_name_common = obj['herb_name_common']
            key = 'remedy_recipe'
            if key in obj:
                items = obj[key]
                print(f'>>> {herb_name_common}')
                print()
                to_delete = False
                for item in items:
                    print(item)
                    print()
                    item_words = item.split(' ')
                    item_words_num = len(item_words)
                    if item_words_num < 7:
                        to_delete = True
                    if item_words_num_min > item_words_num: 
                        item_words_num_min = item_words_num
                        item_smallest = item
                    if item_words_num_max < item_words_num: 
                        item_words_num_max = item_words_num
                        item_longest = item
                if purge and to_delete:
                    del obj[key]
                print()
                print()
            if i < 10:
                if key not in obj:
                    missing_obj_num += 1
        util.json_write(json_filepath, data)
        print()
        print()
        print()
    print(f'item_words_num_min: {item_words_num_min}')
    print(f'item_words_num_max: {item_words_num_max}')
    print(f'item_smallest: {item_smallest}')
    print(f'item_longest: {item_longest}')
    print(f'missing_obj_num: {missing_obj_num}')


# test_preparations('teas')
# test_preparations_descriptions('teas', purge=False)
# test_preparations_properties('teas')
# test_preparations_recipe('teas', purge=False)

#######################
# ;preparations
#######################

def test_preparation__intro(preparation_slug):
    VIEW_RANDOM_SAMPLE = False
    VIEW_RANDOM_SAMPLE_NUM = 3
    random_samples = []
    intro_desc_missing = 0
    intro_desc_words_max = 0
    intro_desc_words_min = 9999
    intro_desc_words_sum = 0
    intro_desc_words_avg = 0
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        system_row = get_system_by_status(status_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue
        json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/{preparation_slug}.json'
        data = util.json_read(json_filepath)
        if 'intro_desc' in data:
            intro_desc = data['intro_desc']
            random_samples.append(intro_desc)
            words = intro_desc.split(' ')
            if intro_desc_words_max < len(words): intro_desc_words_max = len(words)
            if intro_desc_words_min > len(words): intro_desc_words_min = len(words)
            intro_desc_words_sum += len(words)
        else:
            intro_desc_missing += 1
    intro_desc_words_avg = intro_desc_words_sum // len(status_rows)
    print(f'intro_desc_missing: {intro_desc_missing}')
    print(f'intro_desc_words_max: {intro_desc_words_max}')
    print(f'intro_desc_words_min: {intro_desc_words_min}')
    print(f'intro_desc_words_sum: {intro_desc_words_sum}')
    print(f'intro_desc_words_avg: {intro_desc_words_avg}')
    if VIEW_RANDOM_SAMPLE:
        random.shuffle(random_samples) 
        random_samples = random_samples[:VIEW_RANDOM_SAMPLE_NUM]
        for item in random_samples:
            print(f'\n{item}\n')
    print()

def test_preparation__remedy_desc(preparation_slug):
    VIEW_RANDOM_SAMPLE = True
    VIEW_RANDOM_SAMPLE_NUM = 3
    random_samples = []
    missing = 0
    words_max = 0
    words_min = 9999
    words_sum = 0
    words_avg = 0
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        system_row = get_system_by_status(status_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue
        json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/{preparation_slug}.json'
        data = util.json_read(json_filepath)
        if 'remedies_list' in data:
            remedies_list = data['remedies_list']
            for obj in remedies_list:
                if 'remedy_desc' in obj:
                    remedy_desc = obj['remedy_desc']
                    random_samples.append(remedy_desc)
                    words = remedy_desc.split(' ')
                    if words_max < len(words): words_max = len(words)
                    if words_min > len(words): words_min = len(words)
                    words_sum += len(words)
                else:
                    missing += 1
    words_avg = words_sum // (len(status_rows) * 10)
    print(f'remedy_desc_missing: {missing}')
    print(f'remedy_desc_words_max: {words_max}')
    print(f'remedy_desc_words_min: {words_min}')
    print(f'remedy_desc_words_sum: {words_sum}')
    print(f'remedy_desc_words_avg: {words_avg}')
    if VIEW_RANDOM_SAMPLE:
        random.shuffle(random_samples) 
        random_samples = random_samples[:VIEW_RANDOM_SAMPLE_NUM]
        for item in random_samples:
            print(f'\n{item}\n')
    print()

'''
test_preparation__intro('teas')
test_preparation__intro('tinctures')
test_preparation__intro('decoctions')
test_preparation__intro('essential-oils')
test_preparation__intro('capsules')
'''
test_preparation__remedy_desc('teas')
