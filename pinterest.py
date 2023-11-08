from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def pin_generate(entity, common_name, filename):
    img = Image.open(f'{img_folder}/{filename}')

    img_w = 600
    img_h = 900
    img = img.resize((600, 900), Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(img)
    rect_h = 200
    draw.rectangle(((0, img_h//2 - rect_h//2), (img_w, img_h//2 + rect_h//2)), fill ="#0f766e") 
    draw.rectangle(((0, 350), (600, 550)), fill ="#0c0a09") 
    draw.rectangle(((0, 350), (600, 550)), fill ="#1c1917") 

    offset_center_y = 0
    font_size = 72
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.upper()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h//2 - line_h - 20 + offset_center_y), line, '#ffffff', font=font)
    
    draw.rectangle(((0 + 50, img_h//2 - 1 + offset_center_y), (img_w - 50, img_h//2 + 1 + offset_center_y)), fill ="#ffffff") 

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = 'A Medicinal, Botanical, and Horticultural Guide'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h//2 + 20 + offset_center_y), line, '#ffffff', font=font)
    # line = ''
    # line_w = font.getbbox(line)[2]
    # line_h = font.getbbox(line)[3]
    # draw.text((img_w//2 - line_w//2, img_h//2 - line_h//2 + 56), line, '#ffffff', font=font)
    
    font_size = 14
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = '© TerraWhisper.com'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    # draw.rectangle(((0, img_h - 50), (600, img_h)), fill ="#1c1917") 

    draw.text((img_w//2 - line_w//2, img_h//2 + 60 + offset_center_y), line, '#ffffff', font=font)

    # img.show()

    common_name = common_name.lower().replace(' ', '-')
    img.save(f'tmp/{common_name}-guide.jpg', format='JPEG', subsampling=0, quality=100)


entity = 'achillea-millefolium'
common_name = 'Yarrow'

img_folder = f'G:\\tw-images\\pin\\{entity}'
img_filenames = os.listdir(img_folder)
# print(img_filenames)
pin_generate(entity, common_name, img_filenames[1])






latin_name = entity.replace('-', ' ').capitalize()
common_name = 'yarrow'
common_name_title = common_name.title()
common_name_formatted = common_name.lower().replace(' ', '-')
attribute = 'guide'
title = f'{common_name_title} ({latin_name}): Medicinal, Botanical, and Horticultural Guide'
description = "Achillea millefolium has many common names, but the most common is Yarrow. Other common names are Common yarrow, Milfoil, Thousand-leaf, Soldier's woundwort, Nosebleed plant, Old man's pepper, Staunchweed, Sanguinary, Western yarrow, and Knight's milfoil. A. millefolium also has many variants, such as Red Velvet, Paprika, Cerise Queen, Moonshine, Summer Pastels, Lilac Beauty, Coronation Gold, Saucy Seduction, Apple Blossom, and the Colorado Mix."

driver.get("https://www.pinterest.com/pin-creation-tool/")
time.sleep(3)

e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
e.send_keys(f'C:\\terrawhisper-compiler\\tmp\\{common_name_formatted}-{attribute}.jpg') 
time.sleep(3)

e = driver.find_element(By.XPATH, '//input[@id="storyboard-selector-title"]')
e.send_keys(title)
time.sleep(3) 

e = driver.find_element(By.XPATH, "//div[@class='notranslate public-DraftEditor-content']")
for c in description:
    e.send_keys(c)
time.sleep(3)

e = driver.find_element(By.XPATH, '//input[@id="WebsiteField"]')
e.send_keys(f'https://terrawhisper.com/{entity}/') 
time.sleep(3)

e = driver.find_element(By.XPATH, '//button[@data-test-id="board-dropdown-select-button"]')
e.click()
time.sleep(5)

e = driver.find_element(By.XPATH, '//input[@id="pickerSearchField"]')
e.send_keys(common_name_title) 
time.sleep(3)

e = driver.find_element(By.XPATH, f'//div[@data-test-id="board-row-{common_name_title} ({latin_name})"]')
e.click()
time.sleep(3)

e = driver.find_element(By.XPATH, '//div[@data-test-id="storyboard-creation-nav-done"]/..')
e.click()



# WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
#     (By.XPATH, "//div[@class='DraftEditor-editorContainer']/div[@class='notranslate public-DraftEditor-content' and starts-with(@aria-describedby, 'placeholder')]")
#     )).send_keys("Abdul Moiz")

# e.clear()
# e.send_keys('test') 
# e.hover() 
# e.click() 

# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)

# driver.close()
