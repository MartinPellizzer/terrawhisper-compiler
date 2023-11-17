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
    img.paste(img_background, (0, 180))

    draw = ImageDraw.Draw(img)

    current_y = 20

    font_size = 64
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = '10 Health Benefits'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, current_y), line, '#ffffff', font=font)
    current_y += line_h * 1.1
    
    font_size = 64
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'of {common_name}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, current_y), line, '#ffffff', font=font)
    current_y += line_h

    font_size = 18
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = '© TerraWhisper.com'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h - 32), line, '#ffffff', font=font)



    img.show()
    print(img.size)


pin_generate_2(
    'achillea-millefolium', 
    'horse chestnut', 
    f'G:\\tw-images\\pin\\achillea-millefolium-3\\medicine-benefits\\0001.jpg', 
    'medicinal-benefits',
    '10 best health benefits of this plant')
