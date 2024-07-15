import os
import time
import random
import csv
from datetime import datetime
import re
from bs4 import BeautifulSoup
from ctransformers import AutoModelForCausalLM

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

import g
import data_csv
import util
import util_data
import pinterest_util

start_folder = '/home/ubuntu/vault/images'
proj_filepath_abs = '/home/ubuntu/proj/terrawhisper-compiler'

random_num = random.randint(-2, 2)
ARTICLES_NUM = 35 - random_num
WAIT_SECONDS = 500
NUM_TINCTURES = 8

# options = Options()
# options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# driver = webdriver.Firefox(executable_path=r'C:\drivers\geckodriver.exe', options=options)

driver = webdriver.Firefox()
driver.get('https://www.google.com')
driver.maximize_window()
driver.get("https://www.pinterest.com/login/")
time.sleep(10)
e = driver.find_element(By.XPATH, '//input[@id="email"]')
e.send_keys('leenrandell@gmail.com') 
time.sleep(10)
e = driver.find_element(By.XPATH, '//input[@id="password"]')
e.send_keys('Newoliark1') 
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
            g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id,
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



preparations_num = 3
pins_per_preparation = ARTICLES_NUM // preparations_num

random.shuffle(teas_articles_filepath)
teas_articles_filepath = teas_articles_filepath[:pins_per_preparation]

random.shuffle(tinctures_articles_filepath)
tinctures_articles_filepath = tinctures_articles_filepath[:pins_per_preparation]

random.shuffle(essential_oils_articles_filepath)
essential_oils_articles_filepath = essential_oils_articles_filepath[:pins_per_preparation]

articles_filepath = []
for filepath in teas_articles_filepath: articles_filepath.append(filepath)
for filepath in tinctures_articles_filepath: articles_filepath.append(filepath)
for filepath in essential_oils_articles_filepath: articles_filepath.append(filepath)

i = 0
for article_filepath in articles_filepath:
    i += 1
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')

for filename in os.listdir(g.PINTEREST_TMP_IMAGE_FOLDERPATH):
    os.remove(f'{g.PINTEREST_TMP_IMAGE_FOLDERPATH}/{filename}')
    
###########################################################################
# UTILS
###########################################################################

def pin_save(img, filename):
    img_filepath = f'{g.PINTEREST_TMP_IMAGE_FOLDERPATH}/{filename}.jpg'
    img.save(
        img_filepath,
        format='JPEG',
        subsampling=0,
        quality=100,
    )
    return img_filepath

###########################################################################
# BLOCKS
###########################################################################

def gen_text_num(img, line_list, num):
    if num == 0: return img
    text_pos_x = 200
    num = str(num)
    img_w, img_h = 1000, 1500
    draw.rectangle(((0, img_h//2 - 160), (img_w, img_h//2 + 160)), fill='#000000')
    circle_size = 300
    x = img_w//2-circle_size//2
    font_size = 240
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = num
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - 320), text, '#ffffff', font=font)
    text_pos_x = 50 + text_w
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = line_list[0]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - 50), text, '#ffffff', font=font)
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = line_list[1]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2), text, '#ffffff', font=font)
    return img
    
###########################################################################
# TEMPLATES
###########################################################################

def gen_img_template(line_list, img_list, out_filename, num=0,):
    img_w, img_h = 1000, 1500
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#e7e5e4')
    img1 = Image.open(img_list[0])
    img2 = Image.open(img_list[1])
    img3 = Image.open(img_list[2])
    img4 = Image.open(img_list[3])
    img1.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img1 = ImageOps.mirror(img1)
    img1_w, img1_h = img1.size
    img2.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img2 = ImageOps.mirror(img2)
    img2_w, img2_h = img2.size
    img3.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img3 = ImageOps.mirror(img3)
    img3_w, img3_h = img3.size
    img4.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img4 = ImageOps.mirror(img4)
    img4_w, img4_h = img4.size
    img_num = random.randint(2, 4)
    if img_num == 2:
        img.paste(img1, (0, 0 - int(img1_h*0.25)))
        img.paste(img2, (0, img_h - int(img2_h*0.75)))
    if img_num == 3:
        if random.randint(0, 100) < 50:
            img.paste(img1, (0, 0 - int(img1_h*0.25)))
            img.paste(img2, (0 - int(img2_h*0.50), img_h - int(img2_h*0.75)))
            img.paste(img3, (0 + int(img3_h*0.50), img_h - int(img3_h*0.75)))
            draw = ImageDraw.Draw(img)
            draw.rectangle(((img_w//2 - 4, img_h//2 + 160), (img_w//2 + 4, img_h)), fill="#e7e5e4")
        else:
            img.paste(img2, (0 - int(img2_h*0.50), 0))
            img.paste(img3, (0 + int(img3_h*0.50), 0))
            img.paste(img1, (0, img_h - int(img1_h*0.75)))
            draw = ImageDraw.Draw(img)
            draw.rectangle(((img_w//2 - 4, 0), (img_w//2 + 4, img_h//2 - 160)), fill="#e7e5e4")
    if img_num == 4:
        img.paste(img1, (0 - int(img1_h*0.50), 0))
        img.paste(img2, (0 + int(img2_h*0.50), 0))
        img.paste(img3, (0 - int(img3_h*0.50), img_h - int(img3_h*0.75)))
        img.paste(img4, (0 + int(img4_h*0.50), img_h - int(img4_h*0.75)))
        draw = ImageDraw.Draw(img)
        draw.rectangle(((img_w//2 - 4, 0), (img_w//2 + 4, img_h//2 - 160)), fill="#e7e5e4")
        draw.rectangle(((img_w//2 - 4, img_h//2 + 160), (img_w//2 + 4, img_h)), fill="#e7e5e4")
    text_pos_x = 200
    num = str(num)
    img_w, img_h = 1000, 1500
    
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, img_h//2 - 160), (img_w, img_h//2 + 160)), fill='#ffffff')
    circle_size = 300
    x = img_w//2-circle_size//2
    draw.ellipse((img_w//2 - circle_size//2, img_h//2 - 160 - circle_size//2, img_w//2 + circle_size//2, img_h//2 - 160 + circle_size//2), fill = "#ffffff")
    font_size = 160
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = num
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - 280), text, '#000000', font=font)
    text_pos_x = 50 + text_w
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = line_list[0]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - 80), text, '#000000', font=font)
    text = line_list[1]
    font_size = 96
    if len(text) < 20: 
        font_size = 96
        text_y = img_h//2 - 30
    elif len(text) < 30: 
        font_size = 64
        text_y = img_h//2 - 20
    elif len(text) < 40: 
        font_size = 48
        text_y = img_h//2 - 10
    else: 
        font_size = 32
        text_y = img_h//2 - 0 
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, text_y), text, '#000000', font=font)
    img_filepath = pin_save(img, out_filename)
    return img_filepath

# PIN ESSENTIAL OILS
i = 0
for article_filepath in essential_oils_articles_filepath:
    i += 1
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    data = util.json_read(article_filepath)

    remedy_num = data['remedies_num']
    title = data['title']
    problem_name = data['status_name']
    preparation = 'essential oils'
    url = data['url']
    remedies = data['remedies_list']
    filename_out = url.replace('/', '-')

    remedies_descriptions = []
    for remedy in remedies:
        try: remedies_descriptions.append(remedy['remedy_desc'])
        except: print(f'### missing remedies desc in {article_filepath}')

    # GET ALL IMAGE IN PREPARATION FOLDER
    images_folder = f'{start_folder}/essential-oils'
    img_teas_folders = os.listdir(images_folder)
    img_teas_filepaths = []
    for folder in img_teas_folders:
        img_filepaths = os.listdir(f'{images_folder}/{folder}')
        for img_filepath in img_filepaths:
            img_teas_filepaths.append(f'{images_folder}/{folder}/{img_filepath}')

    # GENERATE PIN WITH RANDOM IMAGES
    random.shuffle(img_teas_filepaths)
    images = img_teas_filepaths
    line_1 = f'best herbal essential oils for'.title()
    line_2 = f'{problem_name}'.title()
    line_list = [line_1, line_2]
    img_filepath = gen_img_template(
        line_list,
        images,
        filename_out,
        remedy_num,
    )

    # GET RANDOM DESCRIPTION
    if remedies_descriptions:
        random.shuffle(remedies_descriptions)
        description = remedies_descriptions[0][:490] + '...'
    else:
        description = ''

    # LOG
    print(article_filepath)
    print(remedy_num)
    print(title)
    print(problem_name)
    print(preparation)
    print(url)
    print(filename_out)
    print(description)
    print(images[:4])
    print()

    url = f'https://terrawhisper.com/{url}.html'
    title = f'{title.title()}'
    # title = f'{remedy_num} {title.title()}'
    board_name = 'Herbal Essential Oils'

    driver.get("https://www.pinterest.com/pin-creation-tool/")
    time.sleep(10)

    e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
    # img_filepath_formatted = img_filepath.replace("/", "\\")
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

    e = driver.find_element(By.XPATH, '//button[@data-test-id="board-dropdown-select-button"]')
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

    random_time_to_wait = random.randint(-60, 60)
    time_to_wait = WAIT_SECONDS + random_time_to_wait
    time.sleep(time_to_wait)
    
    
# START PINNING TICTURES
i = 0
for article_filepath in tinctures_articles_filepath:
    i += 1
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    data = util.json_read(article_filepath)

    remedy_num = data['remedies_num']
    title = data['title']
    problem_name = data['status_name']
    preparation = 'tinctures'
    url = data['url']
    remedies = data['remedies_list']
    filename_out = url.replace('/', '-')

    remedies_descriptions = []
    for remedy in remedies:
        try: remedies_descriptions.append(remedy['tincture_desc'])
        except: pass

    # GET ALL IMAGE IN IMAGES/TEA FOLDER
    images_folder = f'{start_folder}/tinctures'
    img_teas_folders = os.listdir(images_folder)
    img_teas_filepaths = []
    for folder in img_teas_folders:
        img_filepaths = os.listdir(f'{images_folder}/{folder}')
        for img_filepath in img_filepaths:
            img_teas_filepaths.append(f'{images_folder}/{folder}/{img_filepath}')

    # GENERATE PIN WITH RANDOM IMAGES
    random.shuffle(img_teas_filepaths)
    images = img_teas_filepaths
    line_1 = f'best herbal tinctures for'.title()
    line_2 = f'{problem_name}'.title()
    line_list = [line_1, line_2]
    img_filepath = gen_img_template(
        line_list,
        images,
        filename_out,
        remedy_num,
    )

    '''
    img_filepath = pinterest_util.gen_img_template_0001(
        line_list,
        images,
        filename_out,
        remedy_num,
    )
    '''

    # GET RANDOM DESCRIPTION
    if remedies_descriptions:
        random.shuffle(remedies_descriptions)
        description = remedies_descriptions[0][:490] + '...'
    else:
        description = ''

    # LOG
    print(article_filepath)
    print(remedy_num)
    print(title)
    print(problem_name)
    print(preparation)
    print(url)
    print(filename_out)
    print(description)
    print(images[:4])
    print()

    url = f'https://terrawhisper.com/{url}.html'
    title = f'{title.title()}'
    # title = f'{remedy_num} {title.title()}'
    board_name = 'Herbal Tinctures'

    driver.get("https://www.pinterest.com/pin-creation-tool/")
    time.sleep(10)

    e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
    # img_filepath_formatted = img_filepath.replace("/", "\\")
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

    e = driver.find_element(By.XPATH, '//button[@data-test-id="board-dropdown-select-button"]')
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

    # driver.get("https://www.google.com/")

    # break

    
    random_time_to_wait = random.randint(-60, 60)
    time_to_wait = WAIT_SECONDS + random_time_to_wait
    time.sleep(time_to_wait)


# START PINNING TEAS
i = 0
for article_filepath in teas_articles_filepath:
    i += 1
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    data = util.json_read(article_filepath)

    try: remedy_num = data['remedy_num']
    except: remedy_num = data['remedies_num']
    title = data['title']
    try: condition_name = data['condition_name']
    except: condition_name = data['status_name']
    preparation = 'teas'
    url = data['url']
    try: remedies = data['teas']
    except: remedies = data['remedies_list']
    filename_out = url.replace('/', '-')

    remedies_descriptions = []
    for remedy in remedies:
        try: remedies_descriptions.append(remedy['tea_desc'])
        except:
            try: remedies_descriptions.append(remedy['remedy_desc'])
            except: pass

    # GET ALL IMAGE IN IMAGES/TEA FOLDER
    images_folder = f'{start_folder}/teas'
    img_teas_folders = os.listdir(images_folder)
    img_teas_filepaths = []
    for folder in img_teas_folders:
        img_filepaths = os.listdir(f'{images_folder}/{folder}')
        for img_filepath in img_filepaths:
            img_teas_filepaths.append(f'{images_folder}/{folder}/{img_filepath}')

    # GENERATE PIN WITH RANDOM IMAGES
    random.shuffle(img_teas_filepaths)
    images = img_teas_filepaths
    line_1 = f'best herbal teas for'.title()
    line_2 = f'{condition_name}'.title()
    line_list = [line_1, line_2]
    img_filepath = gen_img_template(
        line_list,
        images,
        filename_out,
        remedy_num,
    )
    
    '''
    img_filepath = pinterest_util.gen_img_template_0001(
        line_list,
        images,
        filename_out,
        remedy_num,
    )
    '''

    # GET RANDOM DESCRIPTION
    if remedies_descriptions:
        random.shuffle(remedies_descriptions)
        description = remedies_descriptions[0][:490] + '...'
    else:
        description = ''

    # LOG
    print(article_filepath)
    print(remedy_num)
    print(title)
    print(condition_name)
    print(preparation)
    print(url)
    print(filename_out)
    print(description)
    print(images[:4])
    print()

    url = f'https://terrawhisper.com/{url}.html'
    title = f'{title.title()}'
    # title = f'{remedy_num} {title.title()}'
    board_name = 'Herbal Teas'

    driver.get("https://www.pinterest.com/pin-creation-tool/")
    time.sleep(10)

    e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
    # img_filepath_formatted = img_filepath.replace("/", "\\")
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

    e = driver.find_element(By.XPATH, '//button[@data-test-id="board-dropdown-select-button"]')
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

    # driver.get("https://www.google.com/")

    # break

    
    random_time_to_wait = random.randint(-60, 60)
    time_to_wait = WAIT_SECONDS + random_time_to_wait
    time.sleep(time_to_wait)



