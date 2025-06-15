import os
import time
import random
import csv
from datetime import datetime
import re
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler

import g
import data_csv
import util
import util_data

from oliark_io import json_write, json_read

with open('/home/ubuntu/vault/terrawhisper/accounts/pinterest-2-username.txt') as f: username = f.read().strip()
with open('/home/ubuntu/vault/terrawhisper/accounts/pinterest-2-password.txt') as f: password = f.read().strip()

vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'

proj_filepath_abs = '/home/ubuntu/proj/terrawhisper-compiler'

random_num = random.randint(-2, 2)
ARTICLES_NUM = 40 - random_num
WAIT_SECONDS = 400
NUM_TINCTURES = 8

# options = Options()
# options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# driver = webdriver.Firefox(executable_path=r'C:\drivers\geckodriver.exe', options=options)

driver = webdriver.Firefox()
driver.get('https://www.google.com')
driver.maximize_window()
driver.get("https://www.pinterest.com/login/")
time.sleep(10)
'''
e = driver.find_element(By.XPATH, '//input[@type="email"]')
e.send_keys(username) 
time.sleep(10)
e = driver.find_element(By.XPATH, '//button[@type="submit"]')
e.click()
time.sleep(10)
e = driver.find_element(By.XPATH, '//div[text()="Continue with password"]')
e.click()
time.sleep(10)
'''

e = driver.find_element(By.XPATH, '//input[@type="email"]')
e.send_keys(username) 
time.sleep(10)
e = driver.find_element(By.XPATH, '//input[@id="password"]')
e.send_keys(password) 
time.sleep(10)
e = driver.find_element(By.XPATH, '//div[text()="Log in"]')
e.click()
time.sleep(30)






preparations_rows = util.csv_get_rows(g.CSV_PREPARATIONS_FILEPATH)
preparations_cols = util.csv_get_cols(preparations_rows)
preparations_rows = preparations_rows[1:]



status_rows, status_cols = data_csv.status()

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]

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
            g.CSV_SYSTEMS_NEW_FILEPATH, systems_cols['system_id'], system_id,
        )
        if systems_rows_filtered != []:
            system_row = systems_rows_filtered[0]
    return system_row

def get_preparations_by_status(status_id):
    util_data.j_status_preparations_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_STATUS_PREPARATIONS_FILEPATH, util_data.j_status_preparations_cols['status_id'], status_id,
    )

    status_preparations_ids = [
        row[util_data.j_status_preparations_cols['preparation_id']] 
        for row in util_data.j_status_preparations_rows_filtered
        if row[util_data.j_status_preparations_cols['status_id']] == status_id
    ]

    preparations_rows_filtered = []
    for preparation_row in preparations_rows:
        herb_id = preparation_row[preparations_cols['preparation_id']]
        if herb_id in status_preparations_ids:
            preparations_rows_filtered.append(preparation_row)
            
    return preparations_rows_filtered


teas_articles_filepath = []
tinctures_articles_filepath = []
essential_oils_articles_filepath = []
creams_articles_filepath = []
for status_row in status_rows:
    status_exe = status_row[status_cols['status_exe']]
    status_id = status_row[status_cols['status_id']]
    status_slug = status_row[status_cols['status_slug']]
    status_name = status_row[status_cols['status_names']].split(',')[0].strip()
    if status_exe == '': continue
    if status_id == '': continue
    if status_slug == '': continue
    if status_name == '': continue
    print(f'>> {status_id} - {status_name}')
    system_row = get_system_by_status(status_id)
    system_id = system_row[systems_cols['system_id']]
    system_slug = system_row[systems_cols['system_slug']]
    system_name = system_row[systems_cols['system_name']]
    if system_id == '': continue
    if system_slug == '': continue
    if system_name == '': continue
    print(f'    {system_id} - {system_name}')
    preparations = get_preparations_by_status(status_id)[:10]
    preparations_names = [row[preparations_cols['preparation_name']] for row in preparations]
    print(preparations_names)
    json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/teas.json'
    if 'teas' in preparations_names:
        if os.path.exists(json_filepath): 
            print(f'ok: {json_filepath}')
            teas_articles_filepath.append(json_filepath)
        else: print(f'NOT FOUND: {json_filepath}')
    else: print(f'NOT PREPARATION OF STATUS: {json_filepath}')
    json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/tinctures.json'
    if 'tinctures' in preparations_names:
        if os.path.exists(json_filepath): 
            print(f'ok: {json_filepath}')
            tinctures_articles_filepath.append(json_filepath)
        else: print(f'NOT FOUND: {json_filepath}')
    else: print(f'NOT PREPARATION OF STATUS: {json_filepath}')
    json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/essential-oils.json'
    if 'essential oils' in preparations_names:
        if os.path.exists(json_filepath): 
            print(f'ok: {json_filepath}')
            essential_oils_articles_filepath.append(json_filepath)
        else: print(f'NOT FOUND: {json_filepath}')
    else: print(f'NOT PREPARATION OF STATUS: {json_filepath}')
    json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/creams.json'
    if 'creams' in preparations_names:
        if os.path.exists(json_filepath): 
            print(f'ok: {json_filepath}')
            creams_articles_filepath.append(json_filepath)
        else: print(f'NOT FOUND: {json_filepath}')
    else: print(f'NOT PREPARATION OF STATUS: {json_filepath}')



preparations_num = 4
pins_per_preparation = ARTICLES_NUM // preparations_num

random.shuffle(teas_articles_filepath)
teas_articles_filepath = teas_articles_filepath[:pins_per_preparation]

random.shuffle(tinctures_articles_filepath)
tinctures_articles_filepath = tinctures_articles_filepath[:pins_per_preparation]

random.shuffle(essential_oils_articles_filepath)
essential_oils_articles_filepath = essential_oils_articles_filepath[:pins_per_preparation]

random.shuffle(creams_articles_filepath)
creams_articles_filepath = creams_articles_filepath[:pins_per_preparation]

articles_filepath = []
for filepath in teas_articles_filepath: articles_filepath.append(filepath)
for filepath in tinctures_articles_filepath: articles_filepath.append(filepath)
for filepath in essential_oils_articles_filepath: articles_filepath.append(filepath)
for filepath in creams_articles_filepath: articles_filepath.append(filepath)

    
def pin_post(article_filepath):
    data = json_read(article_filepath)
    title = data['title'].title()
    url = data["url"]
    img_filepath = data['img_filepath']
    description = data['description']
    board_name = data['board_name']
    # LOG
    print('ARTICLE_FILEPATH: ' + article_filepath)
    print('TITLE: ' + title)
    print('URL: ' + url)
    print('IMG_FILEPATH: ' + img_filepath)
    print('DESCRIPTION: ' + description)
    try: driver.get("https://www.pinterest.com/pin-creation-tool/")
    except: return
    time.sleep(10)
    e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
    img_filepath_formatted = img_filepath
    e.send_keys(f'{proj_filepath_abs}/{img_filepath_formatted}') 
    time.sleep(10)
    e = driver.find_element(By.XPATH, '//input[@id="storyboard-selector-title"]')
    e.send_keys(title)
    time.sleep(5) 
    e = driver.find_element(By.XPATH, "//div[@class='notranslate public-DraftEditor-content']")
    for c in description:
        e.send_keys(c)
    time.sleep(5)
    e = driver.find_element(By.XPATH, '//input[@id="WebsiteField"]')
    e.send_keys(url) 
    time.sleep(5)
    e = driver.find_element(By.XPATH, '//div[@data-test-id="board-dropdown-select-button"]')
    e.click()
    time.sleep(5)
    e = driver.find_element(By.XPATH, '//input[@id="pickerSearchField"]')
    e.send_keys(board_name) 
    time.sleep(5)
    e = driver.find_element(By.XPATH, f'//div[@data-test-id="board-row-{board_name}"]')
    e.click()
    time.sleep(5)
    e = driver.find_element(By.XPATH, '//div[@data-test-id="storyboard-creation-nav-done"]/..')
    e.click()
    time.sleep(60)



jsons_filenames = os.listdir(f'pinterest/pins')
for i in range(len(jsons_filenames)): 
    # if i < 3: continue
    found = False
    article_filename = ''
    for _json_filename in jsons_filenames:
        json_n = int(_json_filename.split('.')[0])
        if json_n == i:
            found = True
            article_filename = _json_filename
            break
    if found and article_filename != '':
        article_filepath = f'pinterest/pins/{article_filename}'
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        pin_post(article_filepath)
        ###
        random_time_to_wait = random.randint(-60, 60)
        time_to_wait = WAIT_SECONDS + random_time_to_wait
        time.sleep(time_to_wait)

