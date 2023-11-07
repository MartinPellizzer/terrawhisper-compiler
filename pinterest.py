from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def pin_generate(entity, common_name):
    img_folder = f'G:\\tw-images\\pin\\{entity}'
    img_filenames = os.listdir(img_folder)
    img = Image.open(f'{img_folder}/{img_filenames[0]}')

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
    line = common_name
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

    img.show()

    img.save(f'tmp/{common_name}-guide.jpg', format='JPEG', subsampling=0, quality=100)


pin_generate('acorus-calamus', 'SWEET FLAG')

quit()

def pinterest_login():
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

pinterest_login()

# def pinterest_pin():
driver.get("https://www.pinterest.com/pin-creation-tool/")


e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
e.send_keys(r'C:\terrawhisper-compiler\tmp\yarrow-guide.jpg') 
time.sleep(3)

e = driver.find_element(By.XPATH, '//input[@id="storyboard-selector-title"]')
e.send_keys('Yarrow (Achillea millefolium): A Medicinal, Botanical, and Horticultural Guide')
time.sleep(3) 

text = 'Yarrow (Achillea millefolium) belongs to the domain Eukaryota within the kingdom Plantae. It is classified as an Angiosperm (Magnoliophyta) and falls under the Eudicots, a group of flowering plants. Within the order Asterales, this plant is part of the family Asteraceae. The genus name is Achillea, and the specific species is Achillea millefolium.'
e = driver.find_element(By.XPATH, "//div[@class='notranslate public-DraftEditor-content']")
for c in text:
    e.send_keys(c)
time.sleep(3)

e = driver.find_element(By.XPATH, '//input[@id="WebsiteField"]')
e.send_keys('https://terrawhisper.com/achillea-millefolium/') 
time.sleep(3)

e = driver.find_element(By.XPATH, '//button[@data-test-id="board-dropdown-select-button"]')
e.click()
time.sleep(5)

e = driver.find_element(By.XPATH, '//input[@id="pickerSearchField"]')
e.send_keys('yarrow') 
time.sleep(3)

e = driver.find_element(By.XPATH, '//div[@data-test-id="board-row-Yarrow (Achillea Millefolium)"]')
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
e.click() 

# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)

# driver.close()