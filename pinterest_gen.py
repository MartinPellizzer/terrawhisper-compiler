import os
import time
import random
import csv
from datetime import datetime
import re
from bs4 import BeautifulSoup

import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

import g
import data_csv
import util
import util_data

from oliark_io import json_write, json_read

vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'

checkpoint_filepath = f'{vault}/stable-diffusion/checkpoints/juggernautXL_juggXIByRundiffusion.safetensors'
checkpoint_filepath = f'{vault}/stable-diffusion/checkpoints/Juggernaut_X_RunDiffusion.safetensors'

proj_filepath_abs = '/home/ubuntu/proj/tw/terrawhisper-compiler'

random_num = random.randint(-2, 2)
ARTICLES_NUM = 35 - random_num
NUM_TINCTURES = 8

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

herbs_rows, herbs_cols = data_csv.herbs()
herbs_names_scientific = [herb[herbs_cols['herb_name_scientific']] for herb in herbs_rows]

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

    
###########################################################################
# UTILS
###########################################################################

def pin_save(img, filename):
    img_filepath = f'pinterest/images/{filename}.jpg'
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

def template_text_backup(data, images_file_paths, export_file_name):
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
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
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

    # circle
    circle_size = 300
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=bg_color)

    # draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    
    ## text split
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    text = f'{status_name}'.upper()
    #text = 'Breastfeeding pain'.upper()
    #text = 'Breastfeeding'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)

    if text_w > pin_w - 80:
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        _, _, text_w, text_h = font.getbbox(line_1)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2), line_1, text_color, font=font)
        _, _, text_w, text_h = font.getbbox(line_2)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + text_h), line_2, text_color, font=font)

        remedies_num = data['remedies_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.5), text, text_color, font=font)

        text = str(data['remedies_num'])
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    else:
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + 16), text, text_color, font=font)

        remedies_num = data['remedies_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.2), text, text_color, font=font)

        text = '10'
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)

    # text

    export_file_path = pin_save(img, export_file_name)
    return export_file_path


def template_text_2(data, images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 320
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
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

    # circle
    circle_size = 300
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=bg_color)

    # draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    
    ## text split
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    text = f'{status_name}'.upper()
    #text = 'Breastfeeding pain'.upper()
    #text = 'Breastfeeding'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)

    if text_w > pin_w - 80:
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        _, _, text_w, text_h = font.getbbox(line_1)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2), line_1, text_color, font=font)
        _, _, text_w, text_h = font.getbbox(line_2)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + text_h), line_2, text_color, font=font)

        remedies_num = data['remedies_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.5), text, text_color, font=font)

        text = str(data['remedies_num'])
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    else:
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + 16), text, text_color, font=font)

        remedies_num = data['remedies_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.2), text, text_color, font=font)

        text = '10'
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)

    # text

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


def pin_gen_backup(article_filepath, preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    data = util.json_read(article_filepath)
    remedy_num = data['remedies_num']
    title = data['title']
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    url = data['url']
    remedies = data['remedies_list']
    filename_out = url.replace('/', '-')

    # get image
    print(f'{vault}/terrawhisper/images/{preparation_slug}/2x3')
    images_folder = f'{vault}/terrawhisper/images/{preparation_slug}/2x3'
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


def pin_gen(article_filepath, article_i, preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    data = util.json_read(article_filepath)
    remedy_num = data['remedies_num']
    title = data['title']
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    # url = f'https://terrawhisper.com/{data["url"]}.html'
    url = data["url"]
    img_slug = url.replace('/', '-')
    filename_out = url.replace('/', '-')
    if 'remedies_list' in data:
        remedies = data['remedies_list']
    else:
        remedies = data['remedies']
    remedies_descriptions = []
    for remedy in remedies:
        remedies_descriptions.append(remedy['remedy_desc'])
    if remedies_descriptions:
        random.shuffle(remedies_descriptions)
        description = remedies_descriptions[0][:490] + '...'
    else:
        description = ''
    board_name = f'herbal {preparation_name}'.title()
    
    styles = ['', 'website']
    image_style = random.choice(styles)

    herbs_rows, herbs_cols = data_csv.herbs()
    herbs_names_scientific = [herb[herbs_cols['herb_name_scientific']] for herb in herbs_rows]
    images = []
    for i in range(4):
        rnd_herb_name_scientific = random.choice(herbs_names_scientific).strip()
        if preparation_name[-1] == 's': preparation_name_singular = preparation_name[:-1]
        else: preparation_name_singular = preparation_name

        preparation_container = ''
        if preparation_name_singular == 'tea': preparation_container = 'a cup of'
        if preparation_name_singular == 'tincture': preparation_container = 'a bottle of'
        if preparation_name_singular == 'cream': preparation_container = 'a jar of'
        if preparation_name_singular == 'essential oil': preparation_container = 'a bottle of'

        if image_style == 'website':
            prompt_juggernaut_xi = f'''
                {preparation_container} herbal {preparation_name} made with dry {rnd_herb_name_scientific} herb on a wooden table,
                indoor, 
                natural window light,
                earth tones,
                neutral colors,
                soft focus,
                warm tones,
                vintage,
                high resolution,
                cinematic
            '''.replace('  ', ' ')
        elif image_style == 'watercolor':
            prompt_juggernaut_xi = f'''
                close-up of {preparation_container} herbal {preparation_name},
                on a woodent, table, surrounded by {rnd_herb_name_scientific},
                watercolor illustration,  
                depth of field,
                detailed textures, high resolution, cinematic
            '''.replace('  ', ' ')
        else: 
            prompt_juggernaut_xi = f'''
                herbal {preparation_name} on a wooden table indoor surrounded with {rnd_herb_name_scientific}, 
                vibrant colors, 
                depth of field, bokeh, 
                detailed textures, high resolution, cinematic
            '''
            prompt_juggernaut_xi = f'''
                beautiful {preparation_container} {rnd_herb_name_scientific} herbal {preparation_name},
                on a wooden table surrounded by medicinal herbs, 
                portrait, close-up, high resolution, cinematic
            '''
            prompt_juggernaut_x = f'''
                beautiful{preparation_container} of {rnd_herb_name_scientific} herbal {preparation_name},
                on a wooden table surrounded by medicinal herbs, 
                portrait, close-up, high resolution, cinematic
            '''
        prompt = prompt_juggernaut_xi
        print(prompt)
        # image = pipe(prompt=prompt, num_inference_steps=30).images[0]
        # 1024x1024 square
        # 832x1216  portrait
        # 1216x832  landscape
        image = pipe(prompt=prompt, width=832, height=1216, num_inference_steps=30, guidance_scale=7.0).images[0]
        image.save(f'pinterest/tmp/img-{i}.jpg')
        images.append(f'pinterest/tmp/img-{i}.jpg')

    # gen pins
    rand_template = random.randint(0, 100)
    if rand_template >= 0 and rand_template <= 80:
        img_filepath = template_text(data, images, filename_out)
    else:
        img_filepath = template_plain(images, filename_out)

    obj = {
        'title': title,
        'status_name': status_name,
        'preparation_slug': preparation_slug,
        'url': url,
        'description': description,
        'img_filepath': img_filepath,
        'board_name': board_name
    }
    json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{article_i}.json', obj)


def pin_gen_2(article_filepath, article_i, preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    data = util.json_read(article_filepath)

    title = data['title']
    status_name = data['ailment_name']
    url = data["url"]
    img_slug = url.replace('/', '-')
    filename_out = url.replace('/', '-')
    remedies = data['remedies']
    remedies_descriptions = []

    for remedy in remedies:
        remedies_descriptions.append(remedy['remedy_desc'])

    if remedies_descriptions:
        random.shuffle(remedies_descriptions)
        description = remedies_descriptions[0][:490] + '...'
    else:
        description = ''

    board_name = f'herbal {preparation_name}'.title()
    
    styles = ['', 'website']
    image_style = random.choice(styles)

    herbs_rows, herbs_cols = data_csv.herbs()
    herbs_names_scientific = [herb[herbs_cols['herb_name_scientific']] for herb in herbs_rows]
    images = []

    for i in range(2):
        rnd_herb_name_scientific = random.choice(herbs_names_scientific).strip()
        if preparation_name[-1] == 's': preparation_name_singular = preparation_name[:-1]
        else: preparation_name_singular = preparation_name

        preparation_container = ''
        if preparation_name_singular == 'tea': preparation_container = 'a cup of'
        if preparation_name_singular == 'tincture': preparation_container = 'a bottle of'
        if preparation_name_singular == 'cream': preparation_container = 'a jar of'
        if preparation_name_singular == 'essential oil': preparation_container = 'a bottle of'

        if image_style == 'website':
            prompt_juggernaut_xi = f'''
                close-up of {preparation_container} herbal {preparation_name},
                on a wooden table, 
                surrounded by dry {rnd_herb_name_scientific} herbs,
                indoor, 
                natural window light,
                earth tones,
                neutral colors,
                soft focus,
                warm tones,
                vintage,
                high resolution,
                cinematic
            '''.replace('  ', ' ')
        else: 
            prompt_juggernaut_xi = f'''
                beautiful {preparation_container} {rnd_herb_name_scientific} herbal {preparation_name},
                on a wooden table surrounded by medicinal herbs, 
                portrait, close-up, high resolution, cinematic
            '''
        prompt = prompt_juggernaut_xi
        print(prompt)
        # image = pipe(prompt=prompt, num_inference_steps=30).images[0]
        # 1024x1024 square
        # 832x1216  portrait
        # 1216x832  landscape
        # image = pipe(prompt=prompt, width=832, height=1216, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = pipe(prompt=prompt, width=1216, height=832, num_inference_steps=30, guidance_scale=7.0).images[0]
        image.save(f'pinterest/tmp/img-{i}.jpg')
        images.append(f'pinterest/tmp/img-{i}.jpg')

    # gen pins
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 320

    img_0000 = Image.open(images[0])
    img_0001 = Image.open(images[1])

    img_0000 = util.img_resize(img_0000, int(pin_w*1), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*1), int(pin_h*0.5))

    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (0, int(pin_h*0.5) + gap))
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'

    # rect
    draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)

    # circle
    circle_size = 300
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=bg_color)

    # draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    
    ## text split
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    text = f'{status_name}'.upper()
    #text = 'Breastfeeding pain'.upper()
    #text = 'Breastfeeding'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)

    if text_w > pin_w - 80:
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        _, _, text_w, text_h = font.getbbox(line_1)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2), line_1, text_color, font=font)
        _, _, text_w, text_h = font.getbbox(line_2)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + text_h), line_2, text_color, font=font)

        remedies_num = data['remedies_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.5), text, text_color, font=font)

        text = str(data['remedies_num'])
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    else:
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + 16), text, text_color, font=font)

        remedies_num = data['remedies_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.2), text, text_color, font=font)

        text = '10'
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)

    # text

    img_filepath = pin_save(img, filename_out)

    obj = {
        'title': title,
        'status_name': status_name,
        'preparation_slug': preparation_slug,
        'url': url,
        'description': description,
        'img_filepath': img_filepath,
        'board_name': board_name
    }
    json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{article_i}.json', obj)


def gen_image(images, i, preparation_name, image_style, width, height):
    rnd_herb_name_scientific = random.choice(herbs_names_scientific).strip()
    if preparation_name[-1] == 's': preparation_name_singular = preparation_name[:-1]
    else: preparation_name_singular = preparation_name

    preparation_container = ''
    if preparation_name_singular == 'tea': preparation_container = 'a cup of'
    if preparation_name_singular == 'tincture': preparation_container = 'a bottle of'
    if preparation_name_singular == 'cream': preparation_container = 'a jar of'
    if preparation_name_singular == 'essential oil': preparation_container = 'a bottle of'

    if image_style == 'website':
        prompt_juggernaut_xi = f'''
            close-up of {preparation_container} herbal {preparation_name},
            on a wooden table, 
            surrounded by dry {rnd_herb_name_scientific} herbs,
            indoor, 
            natural light,
            earth tones,
            neutral colors,
            soft focus,
            warm tones,
            vintage,
            high resolution,
            cinematic
        '''.replace('  ', ' ')
    else: 
        prompt_juggernaut_xi = f'''
            beautiful {preparation_container} {rnd_herb_name_scientific} herbal {preparation_name},
            on a wooden table surrounded by medicinal herbs, 
            portrait, close-up, high resolution, cinematic
        '''
    prompt = prompt_juggernaut_xi
    print(prompt)
    image = pipe(prompt=prompt, width=width, height=height, num_inference_steps=30, guidance_scale=7.0).images[0]
    image.save(f'pinterest/tmp/img-{i}.jpg')
    images.append(f'pinterest/tmp/img-{i}.jpg')

def gen_template_1_img_b(data, images_file_paths, export_file_name):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'

    pin_w = 1000
    pin_h = 1500
    gap = 8
    rect_h = 500

    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    img_0000 = Image.open(images_file_paths[0])
    img_0000 = util.img_resize(img_0000, pin_w, pin_w)
    img.paste(img_0000, (0, pin_h//3))


    # draw.rectangle(((0, 0), (img_w, img_h//3)), fill=bg_color)

    ## text split
    try: ailment_name = data['ailment_name']
    except: pass
    try: ailment_name = data['status_name']
    except: pass
    ailment_text = f'{ailment_name}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, ailment_w, ailment_h = font.getbbox(ailment_text)

    ailment_lines = []
    if ailment_w > pin_w - 80:
        '''
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
        '''
        words = ailment_text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        ailment_lines.append(line_1)
        ailment_lines.append(line_2)
    else:
        ailment_lines.append(ailment_text)

    # number
    y_start = 0
    if len(ailment_lines) == 2:
        y_start = 0
    elif len(ailment_lines) == 1:
        y_start = 50
    y_cur = y_start
    y_cur += 0

    text = str(data['remedies_num'])
    font_size = 160
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # preparations
    preparation_name = data['preparation_name']
    text = f'best herbal {preparation_name} for'.title()
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # ailment
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    for line in ailment_lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size

    print('****************************************')
    print(data['remedies_num'])
    print(data['preparation_name'])
    print(ailment_lines)
    print(x1)
    print(y_cur)
    print('****************************************')


    '''
    if len(ailment_lines) == 2:
        # preparations
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
        y_cur += font_size*1.5

        # ailment
        font_size = 96
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        line_1 = ailment_lines[0]
        line_2 = ailment_lines[1]
        _, _, line_1_w, line_1_h = font.getbbox(line_1)
        _, _, line_2_w, line_2_h = font.getbbox(line_2)
        y_ailment = rect_h//2 - line_1_h//2
        draw.text((pin_w//2 - line_1_w//2, y_ailment), line_1, text_color, font=font)
        draw.text((pin_w//2 - line_2_w//2, y_ailment + line_2_h), line_2, text_color, font=font)

    if len(ailment_lines) == 1:
        # preparations
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
        y_cur += font_size*1.5

        # ailment
        font_size = 96
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        line_1 = ailment_lines[0]
        _, _, line_1_w, line_1_h = font.getbbox(line_1)
        y_ailment = rect_h//2 - line_1_h//2
        draw.text((pin_w//2 - line_1_w//2, y_ailment), line_1, text_color, font=font)


    '''
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def pin_gen_3(article_filepath, article_i, preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    data = util.json_read(article_filepath)

    title = data['title']
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    url = data["url"]
    img_slug = url.replace('/', '-')
    filename_out = url.replace('/', '-')
    remedies = data['remedies']
    remedies_descriptions = []

    for remedy in remedies:
        remedies_descriptions.append(remedy['remedy_desc'])

    if remedies_descriptions:
        random.shuffle(remedies_descriptions)
        description = remedies_descriptions[0][:490] + '...'
    else:
        description = ''

    board_name = f'herbal {preparation_name}'.title()
    
    styles = ['website']
    templates = ['1_img_b', '']
    image_style = random.choice(styles)
    template = random.choice(templates)

    images = []

    width = 0
    height = 0
    if template == '1_img_b': 
        width = 1024
        height = 1024
        gen_image(images, 0, preparation_name, image_style, width, height)
    else:
        for i in range(2):
            gen_image(images, i, preparation_name, image_style, width, height)
        width = 1216
        height = 832


    # gen pins
    if template == '1_img_b':
        img_filepath = gen_template_1_img_b(data, images, filename_out)
    else:
        img_filepath = template_text_2(data, images, filename_out)

    obj = {
        'title': title,
        'status_name': status_name,
        'preparation_slug': preparation_slug,
        'url': url,
        'description': description,
        'img_filepath': img_filepath,
        'board_name': board_name
    }
    json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{article_i}.json', obj)
       

i = 0
for article_filepath in articles_filepath:
    i += 1
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')

for filename in os.listdir(g.PINTEREST_TMP_IMAGE_FOLDERPATH):
    os.remove(f'{g.PINTEREST_TMP_IMAGE_FOLDERPATH}/{filename}')
    
for filename in os.listdir(g.PINTEREST_PINS_IMAGE_FOLDERPATH):
    os.remove(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{filename}')
    
for filename in os.listdir('pinterest/images'):
    os.remove(f'pinterest/images/{filename}')

pipe = StableDiffusionXLPipeline.from_single_file(
    checkpoint_filepath, 
    torch_dtype=torch.float16, 
    use_safetensors=True, 
    variant="fp16"
).to('cuda')
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

i = 0
# PINS TEAS
for article_filepath in teas_articles_filepath:
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    # pin_gen(article_filepath, i, 'teas')
    pin_gen_3(article_filepath, i, 'teas')
    i += 1

# PINS TINCTURES
for article_filepath in tinctures_articles_filepath:
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    # pin_gen_2(article_filepath, i, 'tinctures')
    pin_gen_3(article_filepath, i, 'teas')
    i += 1

# PINS ESSENTIAL OILS
for article_filepath in essential_oils_articles_filepath:
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    # pin_gen_2(article_filepath, i, 'essential-oils')
    pin_gen_3(article_filepath, i, 'teas')
    i += 1

# PINS CREAMS
for article_filepath in creams_articles_filepath:
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    # pin_gen_2(article_filepath, i, 'creams')
    pin_gen_3(article_filepath, i, 'teas')
    i += 1

