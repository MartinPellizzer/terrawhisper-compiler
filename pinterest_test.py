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


pin_generate_2(
    'achillea-millefolium', 
    'horse chestnut', 
    f'G:\\tw-images\\pin\\achillea-millefolium-2\\medicine-benefits\\0000.jpg', 
    'medicinal-benefits',
    '10 best health benefits of this plant')
