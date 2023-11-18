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


def pin_generate_2(entity, common_name, filepath, attribute, subtitle):
    img_w, img_h = 600, 900

    img_background = Image.open(filepath)
    
    img_background.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    img_background_size = img_background.size

    img = Image.new(mode="RGB", size=(img_w, img_h), color='#1c1917')
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#0f766e')
    img.paste(img_background, (0, 250))

    draw = ImageDraw.Draw(img)

    line_1 = '10'
    line_2 = 'Medicinal Preparations'
    # line_2 = 'Health Benefits'
    line_3 = f'of {common_name.title()}'

    max_len = len(line_1)
    if max_len < len(line_2): max_len = len(line_2)
    if max_len < len(line_3): max_len = len(line_3)


    font_size = 1100 // max_len
    if font_size > 64: font_size = 64

    font = ImageFont.truetype("assets/fonts/arialbd.ttf", font_size)
    tot_y = font.getbbox('y')[3] * 3
    print(tot_y)

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



    img.show()
    print(img.size)


def pin_generate_3(entity, common_name, filepath, attribute, text):
    img_w, img_h = 600, 900

    img_background = Image.open(filepath)
    
    img_background.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    img_background_size = img_background.size

    img = Image.new(mode="RGB", size=(img_w, img_h), color='#1c1917')
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#0f766e')
    img.paste(img_background, (0, 250))

    draw = ImageDraw.Draw(img)

    font_size = 48
    font = ImageFont.truetype("assets/fonts/arialbd.ttf", font_size)
    current_y = 0

    words = text.split(' ')
    lines = []
    curr_line = ''
    for word in words:
        if font.getbbox(curr_line)[2] + font.getbbox(word)[2] < img_w:
            curr_line += word + ' '
        else:
            lines.append(curr_line.strip())
            curr_line = word + ' '
    lines.append(curr_line)

    line_h = font.getbbox('y')[3]
    lines_h = line_h * len(lines)
    print(lines_h)
    current_y = (250 - lines_h) // 2

    for i, line in enumerate(lines):
        line_w = font.getbbox(line)[2]
        draw.text((img_w//2 - line_w//2, current_y + line_h * i), line, '#ffffff', font=font)



    print(lines)


    # font_size = 48
    # line_height = 1.0
    # font = ImageFont.truetype("assets/fonts/arialbd.ttf", font_size)
    # line = text
    # print(line)
    # line_w = font.getbbox(line)[2]
    # line_h = font.getbbox('y')[3]
    # draw.text((0, current_y), line, '#ffffff', font=font)
    # current_y += line_h * line_height
    
    font_size = 18
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = 'TerraWhisper.com'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h - 36), line, '#ffffff', font=font)



    # img.show()
    print(img.size)

    common_name_fotmatted = common_name.lower().replace(' ', '-')
    img.save(f'pinterest/test/{common_name_fotmatted}-{text.lower().replace(" ", "-")}.jpg', format='JPEG', subsampling=0, quality=100)



# pin_generate_2(
#     'achillea-millefolium', 
#     'horse chestnut', 
#     f'G:\\tw-images\\pin\\achillea-millefolium\\medicine-benefits\\0000.jpg', 
#     'medicinal-benefits',
#     '10 best health benefits of this plant')


articles_master_rows = utils.csv_to_llst('database/tables/articles.csv')

# index col with dict
articles_dict = {}
for i, item in enumerate(articles_master_rows[0]):
    articles_dict[item] = i

for i, row in enumerate(articles_master_rows[1:]):
    print(f'{i+1}/{len(articles_master_rows[1:])} - {row}')
    
    entity = row[articles_dict['entity']].strip()
    attribute_1 = row[articles_dict['attribute_1']].strip()
    attribute_2 = row[articles_dict['attribute_2']].strip()
    date = row[articles_dict['date']].strip()
    state = row[articles_dict['state']].strip()
    done = row[articles_dict['done']].strip()
    cuisine_col = row[articles_dict['cuisine']].strip()
    latin_name = entity.replace('-', ' ').capitalize()
    
    common_names = utils.csv_get_rows_by_entity('database/tables/botany/common-names.csv', entity)
    common_name = common_names[0][1].lower()


    if attribute_2 == 'benefits':
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]

        for row in rows_filtered:
            pin_generate_3(
                entity,
                common_name,
                f'G:\\tw-images\\pin\\{entity}\\medicine-benefits\\0000.jpg', 
                'medicinal-benefits',
                f'How {common_name.title()} {row}')

        break