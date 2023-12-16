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
import re

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


def pin_generate_3(entity, common_name, filepath, text, attribute):
    img_w, img_h = 600, 900

    img_background = Image.open(filepath)
    
    img_background.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    img_background_size = img_background.size

    img = Image.new(mode="RGB", size=(img_w, img_h), color='#1c1917')
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#0f766e')
    img.paste(img_background, (0, 250))

    draw = ImageDraw.Draw(img)

    font_size_title = 48
    px = 30
    current_y = 0

    for i in range(10):
        font = ImageFont.truetype("assets/fonts/arialbd.ttf", font_size_title)
        words = text.split(' ')
        lines = []
        curr_line = ''
        for word in words:
            if font.getbbox(curr_line)[2] + font.getbbox(word)[2] < img_w - (px * 2):
                curr_line += word + ' '
            else:
                lines.append(curr_line.strip())
                curr_line = word + ' '
        if len(curr_line.strip()) != 0:
            lines.append(curr_line)
        if len(lines) < 4:
            break
        font_size_title -= 2

    max_w = 0
    for i, line in enumerate(lines):
        line_w = font.getbbox(line)[2]
        if max_w < line_w: max_w = line_w

    total_h = 0
    div_off = 10
    div_h = 2
    cta_off = 10

    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size_title)
    line_h = font.getbbox('y')[3] * len(lines)
    total_h += line_h

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_h = font.getbbox('y')[3]
    total_h += line_h

    current_y = (250 - total_h - div_off - div_h - cta_off) // 2

    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size_title)
    line_h = font.getbbox('y')[3]
    for i, line in enumerate(lines):
        line_w = font.getbbox(line)[2]
        draw.text((img_w//2 - line_w//2, current_y + line_h * i), line, '#ffffff', font=font)
    current_y += line_h * (i + 1)

    draw.rectangle(((img_w//2 - max_w//2, current_y + div_off), (img_w//2 + max_w//2, current_y + div_off + div_h)), fill='#ffffff')
    current_y += div_off + div_h
        
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = 'LEARN HOW TO USE IT >>'
    line_w = font.getbbox(line)[2]
    draw.text((img_w//2 - line_w//2, current_y + cta_off), line, '#ffffff', font=font)
    current_y += cta_off

    print(lines)

    font_size = 18
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = 'TerraWhisper.com'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h - 36), line, '#ffffff', font=font)



    # img.show()
    print(img.size)

    common_name_fotmatted = common_name.lower().replace(' ', '-')
    img.save(f'pinterest/tmp/{common_name_fotmatted}-{attribute.lower().replace(" ", "-")}.jpg', format='JPEG', subsampling=0, quality=100)





master_rows = utils.csv_to_llst('pinterest/articles.csv')

# index col with dict
articles_dict = {}
for i, item in enumerate(master_rows[0]):
    articles_dict[item] = i

for i, row in enumerate(master_rows[1:]):
    # print(f'{i+1}/{len(master_rows[1:])} - {row}')
    
    to_pin = row[articles_dict['to_pin']].strip()
    entity = row[articles_dict['entity']].strip()
    common_name = row[articles_dict['common_name']].strip()
    org = row[articles_dict['org']].strip()
    last_day = row[articles_dict['last_day']].strip()
    current_image = row[articles_dict['current_image']].strip()
    image_name = row[articles_dict['image_name']].strip()
    description_folder = row[articles_dict['description_folder']].strip()

    common_names = utils.csv_get_rows_by_entity('database/tables/botany/common-names.csv', entity)
    common_name = common_names[0][1].lower()
    common_name_formatted = common_name.lower().replace(' ', '-')

    today_day = datetime.now().day
    if int(last_day) == int(today_day): 
        print(f'>> skipped {entity} {url}')
        continue

    # 10 health benefits of yarrow (Achillea millefolium)
    # 10 medicinal preparations of yarrow (Achillea millefolium)
    # num_benefit = int(current_image) % 10

    random_row = ''
    if org.strip() == 'medicine/benefits':
        rows = utils.csv_get_rows_by_entity(f'database/articles/{entity}/medicine/benefits/conditions_text.csv', entity)
        random_row = random.choice(rows)
        benefit = random_row[1].title()

        title = f'{common_name.title()} {benefit}: How to Use It'
        img_title = f'{common_name.title()} {benefit}'

        # print(rows)
        # print(title)
        # print(img_title)
    else:
        continue

    # elif org.strip() == 'medicine/preparations':
    #     rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/preparations.csv', entity)
    #     attributes = [f'{x[1]}' for x in rows[:10]]
    #     attribute = random.choice(attributes)
    #     title = f'{attribute}: Uses, Benefits, and Preparation'
    #     img_title = f'{attribute} Preparation and Benefits'

    url = f'http://terrawhisper.com/{entity}/{org}.html'

    description = random_row[2]

    # description

    # folderpath = f'database/articles/{entity}/{org}'
    # num_benefit = random.randint(0, 9)
    # num_benefit = f'0{num_benefit}'
    # file = []
    # print(folderpath)
    # for f in os.listdir(folderpath):
    #     print(f)
    #     if f.startswith(f'{num_benefit}')[0]:
    #         file.append(f)
    # with open(f'{folderpath}/{file}', encoding="utf-8") as f:
    #         description = f.read()
    
    description = description.replace('\n', ' ')
    description = re.sub("\s\s+" , " ", description)

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
    description = description.replace('..', '.')
    description = description.strip() + '... '
    description += 'Click the pin link to learn more.'

    images = os.listdir(f'H:\\tw-images\\pin\\{entity}')
    image_filename = random.choice(images) 
    img_filepath = f'H:\\tw-images\\pin\\{entity}\\{image_filename}'
    # pin_generate_2(entity, common_name_title, img_filename, image_name, subtitle)

    # pin_generate_3(entity, common_name, filepath, text, filename)
    attribute = random_row[1]
    pin_generate_3(
        entity,
        common_name,
        img_filepath,
        img_title,
        attribute,
    )

    print(title)
    print(description)
    # break
    # continue

    driver.get("https://www.pinterest.com/pin-creation-tool/")
    time.sleep(10)

    e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
    e.send_keys(f'C:\\terrawhisper-compiler\\pinterest\\tmp\\{common_name_formatted}-{attribute.lower().replace(" ", "-")}.jpg') 
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
    e.send_keys('Medicinal Plants') 
    time.sleep(5)

    e = driver.find_element(By.XPATH, f'//div[@data-test-id="board-row-Medicinal Plants"]')
    e.click()
    time.sleep(5)

    e = driver.find_element(By.XPATH, '//div[@data-test-id="storyboard-creation-nav-done"]/..')
    e.click()

    time.sleep(30)

    driver.get("https://www.google.com/")

    new_rows = []
    for new_row in master_rows:
        curr_entity = new_row[articles_dict['entity']].strip()
        curr_org = new_row[articles_dict['org']].strip()
        print(org, curr_org)

        if entity == curr_entity and org == curr_org:
            new_row[articles_dict['last_day']] = str(int(today_day))
            new_row[articles_dict['current_image']] = str(int(new_row[articles_dict['current_image']]) + 1)
            new_rows.append(new_row)
        else:
            new_rows.append(new_row)
    # for row in new_rows:
    #     print(row)

    with open('pinterest/articles.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\\')
        writer.writerows(new_rows)

    time.sleep(300)


driver.get("https://www.google.com/")

