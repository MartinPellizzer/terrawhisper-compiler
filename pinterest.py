from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
import os
import random
import utils
import csv
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# images from leonardo 768x864 per pins

driver = webdriver.Firefox()
driver.get("https://www.pinterest.com/login/")
time.sleep(3)

e = driver.find_element(By.XPATH, '//input[@id="email"]')
e.send_keys('martinpellizzer@gmail.com') 
time.sleep(3)

e = driver.find_element(By.XPATH, '//input[@id="password"]')
e.send_keys('Newoliark1') 
time.sleep(3)

e = driver.find_element(By.XPATH, '//div[text()="Log in"]')
e.click()
time.sleep(3)


def is_row_not_empty(row):
    found = False
    for cell in row:
        if cell.strip() != '':
            found = True
            break
    return found

    
def csv_to_llst(filepath):
    llst = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f, delimiter='\\')
        for row in reader:
            if is_row_not_empty(row):
                llst.append(row)
    return llst



def pin_generate_2(entity, common_name, filename, image_name, subtitle):
    img_w, img_h = 600, 900

    img_background = Image.open(f'{img_folder}/{filename}')
    
    img_background.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    img_background_size = img_background.size

    img = Image.new(mode="RGB", size=(img_w, img_h), color='#1c1917')
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#0f766e')
    img.paste(img_background, (0, 250))

    draw = ImageDraw.Draw(img)

    line_1 = '10'
    if image_name == 'medicinal-preparations': line_2 = 'Medicinal Preparations'
    elif image_name == 'medicinal-benefits': line_2 = 'Health Benefits'
    line_3 = f'of {common_name.title()}'

    max_len = len(line_1)
    if max_len < len(line_2): max_len = len(line_2)
    if max_len < len(line_3): max_len = len(line_3)

    font_size = 1100 // max_len
    if font_size > 64: font_size = 64

    font = ImageFont.truetype("assets/fonts/arialbd.ttf", font_size)
    tot_y = font.getbbox('y')[3] * 3

    current_y = (250 - tot_y) // 2

    # font_size = 48
    line_height = 1.0
    font = ImageFont.truetype("assets/fonts/arialbd.ttf", font_size)
    line = line_1
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox('y')[3]
    draw.text((img_w//2 - line_w//2, current_y), line, '#ffffff', font=font)
    current_y += line_h * line_height
    
    font = ImageFont.truetype("assets/fonts/arialbd.ttf", font_size)
    line = line_2
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox('y')[3]
    draw.text((img_w//2 - line_w//2, current_y), line, '#ffffff', font=font)
    current_y += line_h * line_height
    
    font = ImageFont.truetype("assets/fonts/arialbd.ttf", font_size)
    line = line_3
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox('y')[3]
    draw.text((img_w//2 - line_w//2, current_y), line, '#ffffff', font=font)
    current_y += line_h

    font_size = 18
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = 'TerraWhisper.com'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h - 36), line, '#ffffff', font=font)

    common_name_fotmatted = common_name.lower().replace(' ', '-')
    img.save(f'pinterest/tmp/{common_name_fotmatted}-{image_name}.jpg', format='JPEG', subsampling=0, quality=100)



# articles rows
articles_master_rows = csv_to_llst('pinterest/articles.csv')

# articles indexes
articles_dict = {}
for i, item in enumerate(articles_master_rows[0]):
    articles_dict[item] = i

for i, row in enumerate(articles_master_rows[1:]):
    print(f'{i}/{len(articles_master_rows[1:])}')
    
    to_pin = row[articles_dict['to_pin']].strip()
    entity = row[articles_dict['entity']].strip()
    common_name = row[articles_dict['common_name']].strip()
    org = row[articles_dict['org']].strip()
    url = row[articles_dict['url']].strip()
    title = row[articles_dict['title']].strip()
    subtitle = row[articles_dict['subtitle']].strip()
    last_day = row[articles_dict['last_day']].strip()
    current_image = row[articles_dict['current_image']].strip()
    image_name = row[articles_dict['image_name']].strip()
    image_subfolder = row[articles_dict['image_subfolder']].strip()
    description_folder = row[articles_dict['description_folder']].strip()
    # print(image_name)

    if to_pin.strip() != 'x': continue

    today_day = datetime.now().day
    if int(last_day) == int(today_day): 
        print(f'>> skipped {entity} {url}')
        continue

    latin_name = entity.replace('-', ' ').capitalize()
    common_name_title = common_name.title()
    common_name_formatted = common_name.lower().replace(' ', '-')

    img_folder = f'G:\\tw-images\\pin\\{entity}-2\\{image_subfolder}'
    img_filenames = os.listdir(f'{img_folder}')
    img_filename = img_filenames[int(current_image)]
    pin_generate_2(entity, common_name_title, img_filename, image_name, subtitle)

    folderpath = f'database/articles/{entity}'
    if description_folder.strip() != '': folderpath += '/' + description_folder.replace('-', '/')

    files = [f for f in os.listdir(folderpath) if f.endswith('.md')]
    description = []
    for file in files:
        with open(f'{folderpath}/{file}', encoding="utf-8") as f:
            content = f.read()
        content = content.split('\n')
        for p in content:
            if p.strip() != '':
                description.append(p) 

    description = ''.join(description)
    description = description.split('. ')
    random.shuffle(description)
    description = '. '.join(description[:3])
    words = description.split(' ')
    description = ''
    for word in words:
        if len(description) + len(word) + 1 < 460:
            description += word + ' '
        else:
            break
    description = description.strip() + '... '
    description += 'Click the pin link to learn more.'

    print(entity)
    print(common_name_title)
    print(img_filename)
    print(image_name)
    print(subtitle)
    print(title)
    print(description)
    print(url)
    print()



    driver.get("https://www.pinterest.com/pin-creation-tool/")
    time.sleep(3)

    e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
    e.send_keys(f'C:\\terrawhisper-compiler\\pinterest\\tmp\\{common_name_formatted}-{image_name}.jpg') 
    time.sleep(3)

    e = driver.find_element(By.XPATH, '//input[@id="storyboard-selector-title"]')
    e.send_keys(title)
    time.sleep(3) 

    e = driver.find_element(By.XPATH, "//div[@class='notranslate public-DraftEditor-content']")
    for c in description:
        e.send_keys(c)
    time.sleep(3)

    e = driver.find_element(By.XPATH, '//input[@id="WebsiteField"]')
    e.send_keys(url) 
    time.sleep(3)

    e = driver.find_element(By.XPATH, '//button[@data-test-id="board-dropdown-select-button"]')
    e.click()
    time.sleep(5)

    e = driver.find_element(By.XPATH, '//input[@id="pickerSearchField"]')
    # e.send_keys(common_name_title) 
    e.send_keys('Medicinal Plants') 
    time.sleep(3)

    # e = driver.find_element(By.XPATH, f'//div[@data-test-id="board-row-{common_name_title} ({latin_name})"]')
    e = driver.find_element(By.XPATH, f'//div[@data-test-id="board-row-Medicinal Plants"]')
    e.click()
    time.sleep(3)

    e = driver.find_element(By.XPATH, '//div[@data-test-id="storyboard-creation-nav-done"]/..')
    e.click()

    time.sleep(300)

driver.get("https://www.google.com/")

