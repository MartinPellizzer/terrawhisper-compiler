import os
import time
import requests

import util


ACCESS_KEY = util.file_read('C:/api/trefle.txt')

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
        try: _id = item["id"].strip()
        except: _id = ''
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
            util.csv_add_rows(filepath, [[slug, _id, scientific_name, common_name, genus, family]]) 
    
    time.sleep(5)

    util.file_write('log.txt', str(page_index))
