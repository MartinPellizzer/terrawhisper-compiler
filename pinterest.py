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
from bs4 import BeautifulSoup
from ctransformers import AutoModelForCausalLM


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


C_LUNAR_GREEN = '#324030'
C_OFF_WHITE = '#F5F5F5'
C_OIL = '#271C13'
C_SWIRL = '#D8D1CB'


pinterest_content_path = f'social-media/pinterest'


driver = webdriver.Firefox()
driver.get("https://www.pinterest.com/login/")
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


def csv_to_llst_2(filepath):
    llst = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            if is_row_not_empty(row):
                llst.append(row)
    return llst


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

    draw.rectangle(((0, img_h - 50), (img_w, img_h)), fill='#0f766e')

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





###########################################################################
# IMG TEMPLATES
###########################################################################


def pin_save(img, filename):
    img_filepath = f'{pinterest_content_path}/{filename}.jpg'
    img.save(
        img_filepath,
        format='JPEG',
        subsampling=0,
        quality=100,
    )
    return img_filepath


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

    if num != 0:
        gen_text_num(img, line_list, num)
    else:
        gen_text(img, line_list)
    # img.show()

    img_filepath = pin_save(img, out_filename)
    return img_filepath
    

def gen_img_template_1(line_list, img_list_1, img_list_2, out_filename, num=0,):
    img_w, img_h = 1000, 1500
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#e7e5e4')
    
    img1 = Image.open(img_list_1[0])
    img2 = Image.open(img_list_1[1])
    img3 = Image.open(img_list_2[0])

    img1.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img1 = ImageOps.mirror(img1)
    img1_w, img1_h = img1.size
    img2.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img2 = ImageOps.mirror(img2)
    img2_w, img2_h = img2.size
    img3.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img3 = ImageOps.mirror(img3)
    img3_w, img3_h = img3.size

    img_num = random.randint(3, 3)
    if img_num == 2:
        img.paste(img1, (0, 0 - int(img1_h*0.25)))
        img.paste(img3, (0, img_h - int(img3_h)))
    if img_num == 3:
        if random.randint(0, 100) < 50:
            img.paste(img3, (0, 0))
            img.paste(img2, (0 - int(img2_h*0.50), img_h - int(img2_h*0.75)))
            img.paste(img1, (0 + int(img1_h*0.50), img_h - int(img1_h*0.75)))
            draw = ImageDraw.Draw(img)
            draw.rectangle(((img_w//2 - 4, img_h//2 + 160), (img_w//2 + 4, img_h)), fill="#e7e5e4")
        else:
            img.paste(img1, (0 - int(img1_h*0.50), 0))
            img.paste(img2, (0 + int(img2_h*0.50), 0))
            img.paste(img3, (0, img_h - int(img3_h)))
            draw = ImageDraw.Draw(img)
            draw.rectangle(((img_w//2 - 4, 0), (img_w//2 + 4, img_h//2 - 160)), fill="#e7e5e4")

    if num != 0:
        gen_text_num(img, line_list, num)
    else:
        gen_text(img, line_list)
    # img.show()

    img_filepath = pin_save(img, out_filename)
    return img_filepath


def gen_text_num(img, line_list, num):
    if num == 0: return img

    num = str(num)
    img_w, img_h = 1000, 1500
    
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, img_h//2 - 160), (img_w, img_h//2 + 160)), fill=C_OFF_WHITE)

    circle_size = 300
    x = img_w//2-circle_size//2
    draw.ellipse(
        (
            img_w//2-circle_size//2, img_h//2 - circle_size//2 - 160, 
            img_w//2+circle_size//2, img_h//2 + circle_size//2 - 160,
        ), 
        fill=C_OFF_WHITE)

    
    font_size = 160
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = num
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - 200 - font_size//2), text, C_LUNAR_GREEN, font=font)


    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, 64)
    text = line_list[0]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 - text_h*0.7), text, C_OIL, font=font)

    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, 96)
    text = line_list[1]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + text_h*0.4), text, C_LUNAR_GREEN, font=font)

    return img


def gen_text(img, line_list):
    img_w, img_h = 1000, 1500
    
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, img_h//2 - 160), (img_w, img_h//2 + 160)), fill='C_OFF_WHITE')

    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, 64)
    text = line_list[0]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 - text_h*0.9), text, C_OIL, font=font)

    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, 96)
    text = line_list[1]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + text_h*0.4), text, C_LUNAR_GREEN, font=font)

    # font_family, font_weight = 'Lato', 'Regular'
    # font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    # font = ImageFont.truetype(font_path, 64)
    # text = line_list[2]
    # text_w = font.getbbox(text)[2]
    # text_h = font.getbbox(text)[3]
    # draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + text_h*1.4), text, C_OIL, font=font)

    return img








# articles_rows = utils.csv_to_llst('articles-handwritten.csv')
articles_rows = utils.csv_to_llst('static-articles.csv')
articles_dict = {}
for i, item in enumerate(articles_rows[0]):
    articles_dict[item] = i

for i, row in enumerate(articles_rows[1:]):
    day_last_pinned = row[articles_dict['day_last_pinned']].strip()
    url = row[articles_dict['url']].strip()
    line_1 = 'best herbal teas for'
    line_2 = row[articles_dict['problem']].strip()
    num = int(row[articles_dict['num']].strip())
    pin_title = str(num).strip() + ' ' + row[articles_dict['title']].strip()
    out_filename = url.split('/')[-1].strip()

    board_name = 'Herbal Tea'

    if str(day_last_pinned).strip() == str(datetime.today().day).strip():
        continue

    print(day_last_pinned)
    print(pin_title)
    print(url)
    print(line_1)
    print(line_2)

    if 'headaches' in pin_title.lower():
        img_folderpath_1 = 'C:/tw-images/preparations/tea'
        img_folderpath_2 = 'C:/terrawhisper-assets/images/conditions/headache/5x3'
        images_teas = []
        images_headaches = []

        folder_list = [f'{img_folderpath_1}/{folder}' for folder in os.listdir(img_folderpath_1)]
        random.shuffle(folder_list)
        for folder in folder_list:
            tmp_images = os.listdir(folder)
            random.shuffle(tmp_images)
            tmp_image = tmp_images.pop()
            images_teas.append(f'{folder}/{tmp_image}')

        images_headaches = [f'{img_folderpath_2}/{folder}' for folder in os.listdir(img_folderpath_2)]
        random.shuffle(images_headaches)

        line_list = [line_1, line_2]
        img_filepath = gen_img_template_1(
            line_list,
            images_teas,
            images_headaches,
            out_filename,
            num,
        )

        print(img_filepath)

    else:

        _start_folder = 'C:/terrawhisper-assets/images/tea'
        _img_teas_folders = os.listdir(_start_folder)
        _img_teas_filepaths = []
        for _folder in _img_teas_folders:
            _img_filepaths = os.listdir(f'{_start_folder}/{_folder}')
            for _img_filepath in _img_filepaths:
                _img_teas_filepaths.append(f'{_start_folder}/{_folder}/{_img_filepath}')


        random.shuffle(_img_teas_filepaths)

        images = _img_teas_filepaths
        line_list = [line_1, line_2]
        img_filepath = gen_img_template(
            line_list,
            images,
            out_filename,
            num,
        )

        print(img_filepath)



    url = f'https://terrawhisper.com/{url}.html'
    url_description = url.replace('https://terrawhisper.com/', 'C:/terrawhisper-compiler/website/')
    with open(url_description) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    content = soup.find_all('p')
    lines = [p.getText() for p in content]
    random.shuffle(lines)
    description = '. '.join(lines[:3])
    description = re.sub("\s\s+" , " ", description)
    print(description)

    description = description[:500]




    driver.get("https://www.pinterest.com/pin-creation-tool/")
    time.sleep(10)

    e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
    img_filepath_formatted = img_filepath.replace("/", "\\")
    e.send_keys(f'C:\\terrawhisper-compiler\\{img_filepath_formatted}') 
    time.sleep(10)

    e = driver.find_element(By.XPATH, '//input[@id="storyboard-selector-title"]')
    e.send_keys(pin_title)
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


