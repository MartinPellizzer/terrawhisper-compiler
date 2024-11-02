from oliark_io import csv_read_rows_to_json
from oliark_io import json_read

ailments = csv_read_rows_to_json('systems-organs-ailments.csv', debug=True)

def get_popular_herbs():
    _herbs = []
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        data = json_read(json_filepath, create=True)
        for obj in data['herbs']:
            found = False
            for herb in _herbs:
                if obj['plant_name_scientific'] == herb['plant_name_scientific']:
                    herb['confidence_score'] += obj['confidence_score']
                    found = True
                    break
            if not found:
                _herbs.append(obj)
    _herbs = sorted(_herbs, key=lambda x: x['confidence_score'], reverse=True)
    return _herbs

def analyze_paragraphs(key):
    herbs = get_popular_herbs()
    min_words = 9999
    max_words = 0
    sum_words = 0
    avg_words = 0
    num_paragraphs_found = 0
    num_paragraphs_missing = 0
    for herb_i, herb in enumerate(herbs[:]):
        herb_name_scientific = herb['plant_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        url = f'herbs/{herb_slug}'
        json_filepath = f'database/json/{url}.json'
        data = json_read(json_filepath, create=True)
        if key in data:
            text = data[key]
            words = text.split(' ')
            if min_words > len(words): min_words = len(words)
            if max_words < len(words): max_words = len(words)
            sum_words += len(words)
            num_paragraphs_found += 1   
        else:
            num_paragraphs_missing += 1   
    avg_words = sum_words // num_paragraphs_found
    print(f'################################################')
    print(f'PARAGRAPHS: {key}')
    print(f'MIN WORDS: {min_words}')
    print(f'MAX WORDS: {max_words}')
    print(f'AVG WORDS: {avg_words}')
    print(f'NUM PARAGRAPHS FOUND: {num_paragraphs_found}')
    print(f'NUM PARAGRAPHS MISSING: {num_paragraphs_missing}')
    print(f'################################################')
    print(f'\n\n')

def analyze_studies():
    herbs = get_popular_herbs()
    min_words = 9999
    max_words = 0
    sum_words = 0
    avg_words = 0
    num_paragraphs_found = 0
    num_paragraphs_missing = 0
    for herb_i, herb in enumerate(herbs[:]):
        herb_name_scientific = herb['plant_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
        url = f'herbs/{herb_slug}'
        json_filepath = f'database/json/{url}.json'
        data = json_read(json_filepath, create=True)
        key = 'intro_study'
        if key in data:
            text = data[key][0]
            words = text.split(' ')
            if min_words > len(words): min_words = len(words)
            if max_words < len(words): max_words = len(words)
            sum_words += len(words)
            num_paragraphs_found += 1   
        else:
            num_paragraphs_missing += 1   
    avg_words = sum_words // num_paragraphs_found
    print(f'################################################')
    print(f'PARAGRAPHS: {key}')
    print(f'MIN WORDS: {min_words}')
    print(f'MAX WORDS: {max_words}')
    print(f'AVG WORDS: {avg_words}')
    print(f'NUM PARAGRAPHS FOUND: {num_paragraphs_found}')
    print(f'NUM PARAGRAPHS MISSING: {num_paragraphs_missing}')
    print(f'################################################')
    print(f'\n\n')

# analyze_paragraphs(key='intro_description')
# analyze_paragraphs(key='intro_study')
analyze_studies()
