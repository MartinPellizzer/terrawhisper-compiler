from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import time
import util

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path=r'C:\drivers\geckodriver.exe', options=options)
driver.get("https://powo.science.kew.org/")
time.sleep(10)


rows = util.csv_get_rows('database/tables/plants/trefle.csv')
i = 0
for row in rows[1:]:
    i += 1
    entity = row[0]
    scientific_name = row[1]

    print(f'{i}/?????? - {scientific_name}')
    
    json_filepath = f'database/plants/{entity}.json'
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
    time.sleep(10)
    
    # break
    