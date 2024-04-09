from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import datetime
import time

import util
import utils_ai


options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path=r'C:\drivers\geckodriver.exe', options=options)
driver.get("https://google.com/")
time.sleep(10)

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

    # MEDICINAL/TOXIC    
    data = util.json_read(json_filepath)
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

    # TAXONOMY
    print(f'{i}/?????? - {scientific_name}')
    
    json_filepath = f'database/plants/{slug}.json'
    data = util.json_read(json_filepath)
    try: 
        data['kingdom']
        continue
    except: pass

    driver.get("https://powo.science.kew.org/")
    time.sleep(10)
    e = driver.find_element(By.XPATH, '//input[@id="refine-tokenfield"]')
    e.clear()
    e.send_keys(scientific_name) 
    time.sleep(2)
    e.send_keys(Keys.RETURN) 
    time.sleep(5)

    try: e = driver.find_element(By.XPATH, '//article')
    except: continue
    e.click() 
    time.sleep(5)

    elements = driver.find_elements(By.XPATH, '//ul[contains(@class, "classification")]/li')
    data['kingdom'] = 'NA'
    data['phylum'] = 'NA'
    data['class'] = 'NA'
    data['order'] = 'NA'
    data['family'] = 'NA'
    data['genus'] = 'NA'
    data['species'] = 'NA'
    for e in elements:
        spans = e.find_elements(By.XPATH, './/span')
        var = spans[0].text.strip().lower()
        val = spans[1].text.strip()
        
        if val == '': continue
        if var == 'kingdom': data['kingdom'] = val
        if var == 'phylum': data['phylum'] = val
        if var == 'class': data['class'] = val
        if var == 'order': data['order'] = val
        if var == 'family': data['family'] = val
        if var == 'genus': data['genus'] = val
        if var == 'species': data['species'] = val
            
        print(spans[0].text.strip(), spans[1].text.strip())
    
    util.json_write(json_filepath, data)
    driver.get("https://google.com/")
    time.sleep(10)
        