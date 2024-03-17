from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import time
import os
import csv
import pyperclip
import util

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path=r'C:\drivers\geckodriver.exe', options=options)
driver.get("https://www.pharmachoice.com/health-advice/medical-conditions/")
time.sleep(5) 

for i in range(100):
    elements = driver.find_elements(By.XPATH, '//h4[contains(@class, "elementor-heading-title")]')
    condition = {}
    print(i)
    for e in elements:
        if not e.text.startswith('('):
            if condition != {}:
                rows = util.csv_get_rows_by_entity('database/tables/_conditions.csv', condition['name'])
                if rows == []:
                    try: condition_name = condition['name']
                    except: condition_name = ''
                    try: condition_alias = condition['alias']
                    except: condition_alias = ''
                    util.csv_add_rows('database/tables/_conditions.csv', [[condition_name, condition_alias]])
                # print(condition)
            condition = {}
            condition['name'] = e.text
        else:
            condition['alias'] = e.text

    elements = driver.find_elements(By.XPATH, '//span[contains(text(), "LOAD MORE")]')
    if elements:
        for e in elements:
            e.click()
    else:
        print('no more elements to downoad')

    time.sleep(10)



# for i, row in enumerate(rows[ARTICLE_START:ARTICLE_END]):
#     entity = row[0].strip()
#     common_name = row[1].strip()
#     latin_name = get_latin_name(entity)

    
#     time.sleep(10) 

#     e = driver.find_element(By.XPATH, '//textarea[@id="input"]')
#     e.click()
#     e.send_keys(Keys.CONTROL, 'a')
#     e.send_keys(Keys.BACKSPACE)
#     time.sleep(5) 

#     e = driver.find_element(By.XPATH, '//textarea[@id="input"]')
#     e.send_keys(latin_name)
#     time.sleep(5) 

#     e = driver.find_element(By.XPATH, '//button[@id="tempSheet"]')
#     e.click()
#     time.sleep(5) 

#     time.sleep(SCRAPE_SECONDS)

#     e = driver.find_element(By.XPATH, '//button[@id="startjob"]')
#     e.click()
#     time.sleep(5) 

#     e = driver.find_element(By.XPATH, '//textarea[@id="input"]')
#     e.click()
#     e.send_keys(Keys.CONTROL, 'a')
#     e.send_keys(Keys.CONTROL, 'c')

#     s = pyperclip.paste() 
#     with open(f'keywords/plants/{entity}.txt', 'w', newline='', encoding='utf-8') as f:
#         f.write(s)

#     time.sleep(60)

