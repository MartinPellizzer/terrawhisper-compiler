import os
import time
import requests

import util


ACCESS_KEY = util.file_read('C:/api/trefle.txt')

import datetime
import time

import util
import utils_ai

plants_rows = util.csv_get_rows('database/tables/plants/trefle.csv')
i = 0
for plant_row in plants_rows[1:]:
    i += 1
    print(f'{i}/{len(plants_rows)} - {plant_row}')

    slug = plant_row[0].strip().lower()
    scientific_name = plant_row[1].strip().capitalize()
    common_name = plant_row[2].strip().capitalize()
    genus = plant_row[3].strip().capitalize()
    family = plant_row[4].strip().capitalize()
    
    json_filepath = f'database/plants/{slug}.json'
    
    util.folder_create('database/plants')
    util.json_generate_if_not_exists(json_filepath)
    data = util.json_read(json_filepath)
    data['slug'] = slug
    data['scientific_name'] = scientific_name
    data['common_name'] = common_name
    data['genus'] = genus
    data['family'] = family
    try: lastmod = data['lastmod']
    except: data['lastmod'] = str(datetime.datetime.now().date())
    util.json_write(json_filepath, data)

    try: 
        url = f'https://trefle.io/api/v1/plants/{slug}?token={ACCESS_KEY}'
        response = requests.get(url)
    except:
        time.sleep(5)
        print('response failed!!!')
        continue

    data = response.json()
    util.json_write('json_format.json', data)
    quit()

    time.sleep(30)



try: page_index = int(util.file_read('log.txt').strip())
except: page_index = 1

running = True
while running:
    print(f"scraped page >> {page_index}")
    try: 
        url = f'https://trefle.io/api/v1/plants?token={ACCESS_KEY}&page={page_index}'
        print(url)
        response = requests.get(url)
        page_index += 1
    except:
        time.sleep(5)
        continue

    data = response.json()

    for i, item in enumerate(data["data"]):

        try: slug = item["slug"].strip()
        except: slug = ''
        try: scientific_name = item["scientific_name"].strip()
        except: scientific_name = ''
        try: common_name = item["common_name"].strip()
        except: common_name = ''
        try: genus = item["genus"].strip()
        except: genus = ''
        try: family = item["family"].strip()
        except: family = ''
        print(slug, '--', family)
        # print(scientific_name)
        # print(common_name)
        # print()

        filepath = 'database/tables/_plants_all_new.csv'
        rows = util.csv_get_rows_by_entity(filepath, slug)
        if not rows:
            util.csv_add_rows(filepath, [[slug, scientific_name, common_name, genus, family]]) 
    
    time.sleep(5)

    util.file_write('log.txt', str(page_index))
