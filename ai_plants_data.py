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

    status_effect = ''
    try: status_effect = data['status_effect']
    except: data['status_effect'] = status_effect
    if status_effect == '':
        prompt = f'''
            Is {scientific_name} mostly considered a medicinal, toxic, or neutral plant for the human body? 
            Reply using only 1 of these 3 words:
            - Medicinal
            - Toxic
            - Neutral
            Your reply must be only 1 word long.
        '''
        reply = utils_ai.gen_reply(prompt)

        if 'medicinal' in reply.strip().lower():
            data['status_effect'] = 'medicinal'
        elif 'toxic' in reply.strip().lower():
            data['status_effect'] = 'toxic'
        elif 'neutral' in reply.strip().lower():
            data['status_effect'] = 'neutral'
        else:
            data['status_effect'] = ''
        
        if data['status_effect'] != '':
            print('--------------------------')
            print(data['status_effect'])
            print('--------------------------')
            util.json_write(json_filepath, data)

        time.sleep(30)