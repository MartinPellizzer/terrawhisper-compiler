
sudo snap remove firefox
sudo install -d -m 0755 /etc/apt/keyrings
wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | sudo tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | sudo tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
echo '
Package: *
Pin: origin packages.mozilla.org
Pin-Priority: 1000
' | sudo tee /etc/apt/preferences.d/mozilla
sudo apt update && sudo apt install firefox


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

import g
import data_csv
import util
import util_data

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

def template_plain(images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.open(images_file_paths[0])
    img = util.img_resize(img, pin_w, pin_h)
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def template_mosaic(images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    gap = 8
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0002 = Image.open(images_file_paths[2])
    img_0003 = Image.open(images_file_paths[3])
    img_0000 = util.img_resize(img_0000, int(pin_w*0.66), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*0.66), int(pin_h*0.5))
    img_0002 = util.img_resize(img_0002, int(pin_w*0.66), int(pin_h*0.5))
    img_0003 = util.img_resize(img_0003, int(pin_w*0.66), int(pin_h*0.5))
    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (int(pin_w*0.66) + gap, 0))
    img.paste(img_0002, (-int(pin_w*0.32), int(pin_h*0.5) + gap))
    img.paste(img_0003, (int(pin_w*0.34) + gap, int(pin_h*0.5) + gap))
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def template_mosaic_inverted(images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    gap = 8
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0002 = Image.open(images_file_paths[2])
    img_0003 = Image.open(images_file_paths[3])
    img_0000 = util.img_resize(img_0000, int(pin_w*0.66), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*0.66), int(pin_h*0.5))
    img_0002 = util.img_resize(img_0002, int(pin_w*0.66), int(pin_h*0.5))
    img_0003 = util.img_resize(img_0003, int(pin_w*0.66), int(pin_h*0.5))
    img.paste(img_0000, (-int(pin_w*0.32), 0))
    img.paste(img_0001, (int(pin_w*0.34) + gap, 0))
    img.paste(img_0002, (0, int(pin_h*0.5) + gap))
    img.paste(img_0003, (int(pin_w*0.66) + gap, int(pin_h*0.5) + gap))
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def template_text(data, images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 320
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0002 = Image.open(images_file_paths[2])
    img_0003 = Image.open(images_file_paths[3])
    img_0000 = util.img_resize(img_0000, int(pin_w*1), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*1), int(pin_h*0.5))
    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (0, int(pin_h*0.5) + gap))
    random_theme = random.randint(0, 2)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    elif random_theme == 1:
        text_color = '#ffffff'
        bg_color = '#a21caf'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    # rect
    draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    # line
    # draw.line((0, pin_h//2, pin_w, pin_h//2), fill='#ff00ff')
    # data
    status_name = data['status_name']
    text = f'{status_name}'.upper()
    words = text.split(' ')
    lines = []
    if len(words) > 2:
        lines.append(' '.join(words[:2]))
        lines.append(' '.join(words[2:]))
    else:
        lines.append(' '.join(words))
    len_lines_max = 0
    for line in lines:
        if len_lines_max < len(line): len_lines_max = len(line)
    font_size = 64
    font_step_size = 12
    font_start_size = 48
    if len_lines_max < 8: font_size = font_start_size + font_step_size*6
    elif len_lines_max < 12: font_size = font_start_size + font_step_size*5
    elif len_lines_max < 16: font_size = font_start_size + font_step_size*4
    elif len_lines_max < 20: font_size = font_start_size + font_step_size*3
    elif len_lines_max < 24: font_size = font_start_size + font_step_size*2
    elif len_lines_max < 28: font_size = font_start_size + font_step_size*1
    else: font_size = font_start_size + font_step_size*0
    if len(lines) > 1: ml_off_y = int(font_size*0.66)
    else: ml_off_y = 0
    
    # text
    remedies_num = data['remedies_num']
    preparation_name = data['preparation_name']
    text = f'{remedies_num} best herbal {preparation_name} for'.title()
    preparations_font_size = 48
    offset_y = int(preparations_font_size*0.2)
    line_spacing = int(preparations_font_size*0.75)
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, preparations_font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - offset_y - line_spacing- ml_off_y), text, text_color, font=font)
    # text status
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(lines[0])
    draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - offset_y + line_spacing - ml_off_y), lines[0], text_color, font=font)
    if len(lines) > 1:
        _, _, text_w, text_h = font.getbbox(lines[1])
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - offset_y + line_spacing + text_h - ml_off_y), lines[1], text_color, font=font)
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

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


def pin_gen(article_filepath, preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    data = util.json_read(article_filepath)
    remedy_num = data['remedies_num']
    title = data['title']
    status_name = data['status_name']
    url = data['url']
    remedies = data['remedies_list']
    filename_out = url.replace('/', '-')

    # get image
    images_folder = f'{start_folder}/2x3/{preparation_slug}'
    img_creams_folders = os.listdir(images_folder)
    img_creams_filepaths = []
    for folder in img_creams_folders:
        img_filepaths = os.listdir(f'{images_folder}/{folder}')
        for img_filepath in img_filepaths:
            img_creams_filepaths.append(f'{images_folder}/{folder}/{img_filepath}')

    # gen pins
    random.shuffle(img_creams_filepaths)
    images = img_creams_filepaths
    line_1 = f'best herbal {preparation_name} for'.title()
    line_2 = f'{status_name}'.title()
    line_list = [line_1, line_2]

    rand_template = random.randint(0, 2)
    # rand_template = 2
    if rand_template == 0:
        img_filepath = template_plain(images, filename_out)
    elif rand_template == 1:
        if random.randint(0, 1) == 0:
            img_filepath = template_mosaic(images, filename_out)
        else:
            img_filepath = template_mosaic_inverted(images, filename_out)
    else:
        img_filepath = template_text(data, images, filename_out)

# PINS TEAS
for i, article_filepath in enumerate(teas_articles_filepath):
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_gen(article_filepath, 'teas')

# PINS TINCTURES
for i, article_filepath in enumerate(tinctures_articles_filepath):
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_gen(article_filepath, 'tinctures')

# PINS ESSENTIAL OILS
for i, article_filepath in enumerate(essential_oils_articles_filepath):
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_gen(article_filepath, 'essential-oils')

# PINS CREAMS
for i, article_filepath in enumerate(creams_articles_filepath):
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_gen(article_filepath, 'creams')

def pin_post(article_filepath, preparation_slug):
    data = util.json_read(article_filepath)
    preparation_name = preparation_slug.replace('-', ' ')

    remedy_num = data['remedies_num']
    title = data['title'].title()
    status_name = data['status_name']
    url = data["url"]
    image_slug = url.replace('/', '-')

    img_filepath = f'{g.PINTEREST_TMP_IMAGE_FOLDERPATH}/{image_slug}.jpg'

    remedies = data['remedies_list']
    remedies_descriptions = []
    for remedy in remedies:
        remedies_descriptions.append(remedy['remedy_desc'])
    if remedies_descriptions:
        random.shuffle(remedies_descriptions)
        description = remedies_descriptions[0][:490] + '...'
    else:
        description = ''

    board_name = f'herbal {preparation_name}'.title()
    url = f'https://terrawhisper.com/{data["url"]}.html'

    # LOG
    print('ARTICLE_FILEPATH: ' + article_filepath)
    print('REMEDY_NUM: ' + str(remedy_num))
    print('TITLE: ' + title)
    print('URL: ' + url)
    print('IMG_FILEPATH: ' + img_filepath)
    print('DESCRIPTION: ' + description)

    driver.get("https://www.pinterest.com/pin-creation-tool/")
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


# POST TEAS
for i, article_filepath in enumerate(teas_articles_filepath):
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_post(article_filepath, 'teas')

# POST TINCTURES
for i, article_filepath in enumerate(tinctures_articles_filepath):
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_post(article_filepath, 'tinctures')

# POST ESSENTIAL OILS
for i, article_filepath in enumerate(essential_oils_articles_filepath):
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_post(article_filepath, 'essential-oils')

# POST CREAMS
for i, article_filepath in enumerate(creams_articles_filepath):
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_post(article_filepath, 'creams')

