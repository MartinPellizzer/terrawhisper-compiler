from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import util
import csv
from datetime import datetime
import re
from bs4 import BeautifulSoup
from ctransformers import AutoModelForCausalLM
import pinterest_util
import util

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
import random


ARTICLES_NUM = 16



driver = webdriver.Firefox()
driver.get("https://www.pinterest.com/login/")
driver.maximize_window()
time.sleep(3)

e = driver.find_element(By.XPATH, '//input[@id="email"]')
# e.send_keys('martinpellizzer@gmail.com') 
e.send_keys('leenrandell@gmail.com') 
time.sleep(3)

e = driver.find_element(By.XPATH, '//input[@id="password"]')
# e.send_keys('Newoliark1') 
e.send_keys('Newoliark1') 
time.sleep(3)

e = driver.find_element(By.XPATH, '//div[text()="Log in"]')
e.click()
time.sleep(10)





# GET RANDOM ARTICLES TO PIN
articles_filename = os.listdir('database/articles/herbalism/tea')
articles_filepath = [
    f'database/articles/herbalism/tea/{article_filename}'
    for article_filename in articles_filename
]    
random.shuffle(articles_filepath)
articles_filepath = articles_filepath[:ARTICLES_NUM]

# START PINNING
for article_filepath in articles_filepath:
    data = util.json_read(article_filepath)

    remedy_num = data['remedy_num']
    keyword = data['keyword']
    condition = data['condition']
    preparation = data['preparation']
    url = data['url']
    remedies = data['remedies']

    filename_out = url.replace('/', '-')
    remedies_descriptions = []
    for remedy in remedies:
        try: remedies_descriptions.append(remedy['remedy_desc'])
        except: pass

    # GET ALL IMAGE IN IMAGES/TEA FOLDER
    start_folder = 'C:/terrawhisper-assets/images/tea'
    img_teas_folders = os.listdir(start_folder)
    img_teas_filepaths = []
    for folder in img_teas_folders:
        img_filepaths = os.listdir(f'{start_folder}/{folder}')
        for img_filepath in img_filepaths:
            img_teas_filepaths.append(f'{start_folder}/{folder}/{img_filepath}')

    # GENERATE PIN WITH RANDOM IMAGES
    random.shuffle(img_teas_filepaths)
    images = img_teas_filepaths
    line_1 = f'best herbal teas for'.title()
    line_2 = f'{condition}'.title()
    line_list = [line_1, line_2]
    img_filepath = pinterest_util.gen_img_template(
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
    print(keyword)
    print(condition)
    print(preparation)
    print(url)
    print(filename_out)
    print(description)
    print(images[:4])
    print()

    url = f'https://terrawhisper.com/{url}.html'
    title = f'{remedy_num} {keyword.title()}'
    board_name = 'Herbal Tea'

    driver.get("https://www.pinterest.com/pin-creation-tool/")
    time.sleep(10)

    e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
    img_filepath_formatted = img_filepath.replace("/", "\\")
    e.send_keys(f'C:\\terrawhisper-compiler\\{img_filepath_formatted}') 
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

    time.sleep(30)

    driver.get("https://www.google.com/")

    time.sleep(300)





# articles_rows = util.csv_get_rows('static-articles.csv')
# articles_dict = {}
# for i, item in enumerate(articles_rows[0]):
#     articles_dict[item] = i

# for i, row in enumerate(articles_rows[1:]):
#     day_last_pinned = row[articles_dict['day_last_pinned']].strip()
#     url = row[articles_dict['url']].strip()
#     line_1 = 'best herbal teas for'
#     line_2 = row[articles_dict['problem']].strip()
#     num = int(row[articles_dict['num']].strip())
#     pin_title = str(num).strip() + ' ' + row[articles_dict['title']].strip()
#     out_filename = url.split('/')[-1].strip()

#     board_name = 'Herbal Tea'

#     if str(day_last_pinned).strip() == str(datetime.today().day).strip():
#         continue

#     print(day_last_pinned)
#     print(pin_title)
#     print(url)
#     print(line_1)
#     print(line_2)


#     _start_folder = 'C:/terrawhisper-assets/images/tea'
#     _img_teas_folders = os.listdir(_start_folder)
#     _img_teas_filepaths = []
#     for _folder in _img_teas_folders:
#         _img_filepaths = os.listdir(f'{_start_folder}/{_folder}')
#         for _img_filepath in _img_filepaths:
#             _img_teas_filepaths.append(f'{_start_folder}/{_folder}/{_img_filepath}')


#     random.shuffle(_img_teas_filepaths)

#     images = _img_teas_filepaths
#     line_list = [line_1, line_2]
#     img_filepath = pinterest_util.gen_img_template(
#         line_list,
#         images,
#         out_filename,
#         num,
#     )

#     print(img_filepath)



#     url = f'https://terrawhisper.com/{url}.html'
#     url_description = url.replace('https://terrawhisper.com/', 'C:/terrawhisper-compiler/website/')
#     with open(url_description) as fp:
#         soup = BeautifulSoup(fp, 'html.parser')

#     content = soup.find_all('p')
#     lines = [p.getText() for p in content]
#     random.shuffle(lines)
#     description = '. '.join(lines[:3])
#     description = re.sub("\s\s+" , " ", description)
#     print(description)

#     description = description[:500]



