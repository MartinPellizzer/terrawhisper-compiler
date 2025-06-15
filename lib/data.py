import os

from lib import g
from lib import io
from lib import utils

def herbs_books_get():
    herbs_0000 = io.csv_to_dict(f'database/herbs-book-0000.csv')
    with open('database/herbs/books/medical-herbalism.txt') as f: herbs_0001 = f.read().split('\n')
    ###
    herbs = []
    for herb in herbs_0000: herbs.append(herb['latin_name'].strip().lower())
    for herb in herbs_0001: herbs.append(herb.strip().lower())
    herbs = list(set(herbs))
    herbs = sorted(herbs)
    return herbs

def herbs_wcvp_get():
    herbs_0000 = io.csv_to_dict(f'{g.VAULT_TMP}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    ###
    herbs = []
    for herb in herbs_0000: herbs.append(herb['scientfiicname'].strip().lower())
    herbs = list(set(herbs))
    herbs = sorted(herbs)
    return herbs

def herb_medicine_poison_get(url):
    json_article_filepath = f'{g.ENTITIES_FOLDERPATH}/{url}.json'
    json_article = io.json_read(json_article_filepath)
    medicine_or_poison = json_article['medicine_or_poison']
    medicine = {'medicine_or_poison': 'medicine', 'total_score': 0}
    for _obj in medicine_or_poison:
        if 'medicine' in _obj['answer']: 
            medicine = _obj
            break
    poison = {'medicine_or_poison': 'poison', 'total_score': 0}
    for _obj in medicine_or_poison:
        if 'poison' in _obj['answer']: 
            poison = _obj
            break
    inert = {'medicine_or_poison': 'inert', 'total_score': 0}
    for _obj in medicine_or_poison:
        if 'inert' in _obj['answer']: 
            inert = _obj
            break
    if medicine['total_score'] > poison['total_score'] and medicine['total_score'] > inert['total_score']: 
        return 'medicine'
    elif poison['total_score'] > medicine['total_score'] and poison['total_score'] > inert['total_score']: 
        return 'poison'
    else: 
        return 'inert'

def preparations_popular_100_get(entity_slug):
    herb_list = []
    for ailment in os.listdir(f'{g.JSONS_AILMENTS_FOLDERPATH}'):
        if os.path.isdir(f'{g.JSONS_AILMENTS_FOLDERPATH}/{ailment}'):
            for filename in os.listdir(f'{g.JSONS_AILMENTS_FOLDERPATH}/{ailment}'):
                if filename == f'{entity_slug}.json':
                    json_article_filepath = f'{g.JSONS_AILMENTS_FOLDERPATH}/{ailment}/{filename}'
                    json_article = io.json_read(json_article_filepath)
                    preparation_list = json_article['preparations']
                    for preparation in preparation_list:
                        herb_name_scientific = preparation['herb_name_scientific']
                        herb_slug = utils.sluggify(herb_name_scientific)
                        herb_total_score = preparation['herb_total_score']
                        found = False
                        for herb in herb_list:
                            if herb['herb_slug'] == herb_slug:
                                herb['herb_total_score'] += herb_total_score
                                found = True
                                break
                        if not found:
                            herb_list.append({
                                'herb_slug': herb_slug,
                                'herb_name_scientific': herb_name_scientific,
                                'herb_total_score': herb_total_score,
                            })
    herb_list = sorted(herb_list, key=lambda x: x['herb_total_score'], reverse=True)
    return herb_list[:100]

