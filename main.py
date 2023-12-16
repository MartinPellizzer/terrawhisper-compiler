# TODO: fix parameters (unite) in function get_content('horticulture-conditions', f'database/articles/{entity}')
# TODO: add last line in intro (ex. this article will teach you...)
# TODO: add dates to articles


import json
import os
import markdown
import shutil
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
import math
import re
import csv
import sys
import utils
import random

entity_arg = None
REGEN_ALL_FORCED = False 
if len(sys.argv) == 2:
    if sys.argv[1] == 'force':
        REGEN_ALL_FORCED = True

website_img_path = 'website/images'

# vars
image_folder = 'H:/tw-images/auto'
image_folder_old = 'H:/tw-images/website'

# with open("database/growing_zones.json", encoding='utf-8') as f:
#     growing_zones_data = json.loads(f.read())


ARTICLES_CSV = 'articles.csv'


google_tag = '''
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-9086LN3SRR"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-9086LN3SRR');
    </script>
'''

lst_line_height = 40

# TODO: maybe unite folderpath + section
def get_content(section, folderpath):
    text = ''
    try: 
        filepath = f'{folderpath}/{section}.md'
        with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
        text += section_content + '\n\n'
    except: 
        print(f'WARNING: missing {section} text ({filepath})')

    return text

def get_content_2(filepath):
    text = ''
    try: 
        with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
        text += section_content + '\n\n'
    except: 
        print(f'WARNING: missing content - {filepath}')

    return text


######################################################################
# UTILS 
######################################################################

def normalize(text):
    return text.strip().lower()


def lst_to_txt(lst):
    txt = ''
    if len(lst) == 0: txt = ''
    elif len(lst) == 1: txt = lst[0]
    elif len(lst) == 2: txt = f'{lst[0]} and {lst[1]}'
    else: txt = f'{", ".join(lst[:-1])} and {lst[-1]}'
    return txt


def lst_to_blt(lst):
    txt = ''
    for item in lst:
        txt += f'- {item}\n'
    return txt.strip()


def bold_blt(lst):
    bld_lst = []
    for item in lst:
        if ':' in item:
            item_parts = item.split(":")
            bld_lst.append(f'**{item_parts[0]}**: {item_parts[1]}')
        else:
            bld_lst.append(f'{item}')
    return bld_lst


def is_row_not_empty(row):
    found = False
    for cell in row:
        if cell.strip() != '':
            found = True
            break
    return found





# def csv_get_rows_by_entity(filepath, entity):
#     rows = []
#     with open(filepath, encoding='utf-8', errors='ignore') as f:
#         reader = csv.reader(f, delimiter="|")
#         for i, line in enumerate(reader):
#             rows.append(line)
    
#     filtered_rows = [] 
#     for row in rows:
#         if row[0].strip() == entity[0].strip():
#             filtered_rows.append(row)
#     return rows
            

def sanitize_one_word(text):
    return text.split(',')[0].split(' ')[0]


def sanitize(text):
    return text.split('(')[0].split(',')[0]



######################################################################
# TABLE 
######################################################################

def csv_get_table_data(filepath):
    lines = []
    with open(filepath) as f:
        reader = csv.reader(f, delimiter="\\")
        for i, line in enumerate(reader):
            if i == 0:
                lines.append(line)
            else:
                if line[0].strip() == entity.strip():
                    lines.append(line)
    return lines


def csv_get_table_data_2(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    return content


def generate_table(lines):
    text = ''
    text += f'| Characteristic | Description |\n'
    text += f'| --- | --- |\n'
    for i in range(len(lines[0])):
        if i == 0: continue
        if lines[0][i].strip() == '': continue
        try: 
            if lines[1][i].strip() == '': continue
        except: continue
        text += f'| {lines[0][i].title()} | {lines[1][i].capitalize()} |\n'
    text += f'\n'
    return text


def csv_get_rows(filepath):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter="\\")
        for i, line in enumerate(reader):
            rows.append(line)
    return rows


def generate_table_grouped(rows):
    rows_grouped = []
    for row in rows:
        found = False
        for row_grouped in rows_grouped:
            if row[1].strip() == row_grouped[1].strip():
                found = True
                row_grouped.append(row[2])
                break
        if not found:
            rows_grouped.append(row)

    text = ''
    for i, row in enumerate(rows_grouped):
        if i == 0:
            text += f'|Continent|States|\n'
            text += f'|---|---|\n'
        else:
            col_1 = row[1]
            col_2 = ','.join(row[1:])
            text += f'|{col_1}|{col_2}|\n'
    return text
    

def generate_table_simple(rows):
    text = ''
    for i, row in enumerate(rows):
        if i == 0:
            text += f'|Continent|Distribution|\n'
            text += f'|---|---|\n'
        else:
            col_1 = row[1]
            col_2 = row[2]
            text += f'|{col_1}|{col_2}|\n'
    return text



######################################################################
# IMAGES 
######################################################################

def img_resize(image_path):
    w, h = 768, 578

    img = Image.open(image_path)

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    output_path = f'{website_img_path}/{"-".join(image_path.split("/")[1:])}'
    img.save(f'{output_path}')

    return output_path


def img_taxonomy(item):
    domain = item['domain']
    kingdom = item['kingdom']
    phylum = item['phylum']
    _class = item['class']
    order = item['order']
    family = item['family']
    genus = item['genus']
    species = item['species']
    latin_name = f'{genus} {species}'

    w, h = 768, 512
    img = Image.new(mode="RGB", size=(w, h), color='#047857')

    draw = ImageDraw.Draw(img)


    font_size = 40
    line_hight = 1.2
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    lines = [f'Taxonomy of {latin_name}']
    for i, line in enumerate(lines):
        line_w = font.getbbox(line)[2]
        draw.text(
            (w//2 - line_w//2, 30 + (font_size * line_hight * i)), 
            line, 
            (255,255,255), 
        font=font)

    cord_list = []    

    list_y = 160 
    list_y_off = 120
    pos_1 = 0.2
    pos_2 = 0.5
    pos_3 = 0.8 
    arrow_offset = 20
    arrow_point_size = 8

    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)

    line = domain
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((int(w * pos_1) - line_w//2, list_y), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_1) + line_w//2 + arrow_offset, list_y + line_h//2])

    line = kingdom
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_2) - line_w//2, list_y), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_2) - line_w//2 - arrow_offset, list_y + line_h//2])
    cord_list.append([int(w * pos_2) + line_w//2 + arrow_offset, list_y + line_h//2])

    line = phylum
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_3) - line_w//2, list_y), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_3) - line_w//2 - arrow_offset, list_y + line_h//2])
    cord_list.append([int(w * pos_3), list_y + line_h + arrow_offset])

    line = _class
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_3) - line_w//2, list_y + list_y_off), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_3), list_y + list_y_off - arrow_offset])
    cord_list.append([int(w * pos_3) - line_w//2 - arrow_offset, list_y + list_y_off + line_h//2])

    line = order
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_2) - line_w//2, list_y + list_y_off), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_2) + line_w//2 + arrow_offset, list_y + list_y_off + line_h//2])
    cord_list.append([int(w * pos_2) - line_w//2 - arrow_offset, list_y + list_y_off + line_h//2])

    line = family
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_1) - line_w//2, list_y + list_y_off), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_1) + line_w//2 + arrow_offset, list_y + list_y_off + line_h//2])
    cord_list.append([int(w * pos_1), list_y + list_y_off + line_h + arrow_offset])

    line = genus
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_1) - line_w//2, list_y + list_y_off * 2), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_1), list_y + list_y_off + list_y_off - arrow_offset])
    cord_list.append([int(w * pos_1) + line_w//2 + arrow_offset, list_y + list_y_off * 2 + line_h//2])

    line = species
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_2) - line_w//2, list_y + list_y_off * 2), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_2) - line_w//2 - arrow_offset, list_y + list_y_off * 2 + line_h//2])

    draw.line(((cord_list[0][0], cord_list[0][1]), (cord_list[1][0], cord_list[1][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[1][0], cord_list[1][1] - arrow_point_size), (cord_list[1][0] + arrow_point_size, cord_list[1][1]), (cord_list[1][0], cord_list[1][1] + arrow_point_size)], fill='#ffffff')
    draw.line(((cord_list[2][0], cord_list[2][1]), (cord_list[3][0], cord_list[3][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[3][0], cord_list[3][1] - arrow_point_size), (cord_list[3][0] + arrow_point_size, cord_list[3][1]), (cord_list[3][0], cord_list[3][1] + arrow_point_size)], fill='#ffffff')
    draw.line(((cord_list[4][0], cord_list[4][1]), (cord_list[5][0], cord_list[5][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[5][0] - arrow_point_size, cord_list[5][1]), (cord_list[5][0], cord_list[5][1] + arrow_point_size), (cord_list[5][0] + arrow_point_size, cord_list[5][1])], fill='#ffffff')
    draw.line(((cord_list[6][0], cord_list[6][1]), (cord_list[7][0], cord_list[7][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[7][0], cord_list[7][1] - arrow_point_size), (cord_list[7][0] - arrow_point_size, cord_list[7][1]), (cord_list[7][0], cord_list[7][1] + arrow_point_size)], fill='#ffffff')
    draw.line(((cord_list[8][0], cord_list[8][1]), (cord_list[9][0], cord_list[9][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[9][0], cord_list[9][1] - arrow_point_size), (cord_list[9][0] - arrow_point_size, cord_list[9][1]), (cord_list[9][0], cord_list[9][1] + arrow_point_size)], fill='#ffffff')
    
    draw.line(((cord_list[10][0], cord_list[10][1]), (cord_list[11][0], cord_list[11][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[11][0] - arrow_point_size, cord_list[11][1]), (cord_list[11][0], cord_list[11][1] + arrow_point_size), (cord_list[11][0] + arrow_point_size, cord_list[11][1])], fill='#ffffff')

    draw.line(((cord_list[12][0], cord_list[12][1]), (cord_list[13][0], cord_list[13][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[13][0], cord_list[13][1] - arrow_point_size), (cord_list[13][0] + arrow_point_size, cord_list[13][1]), (cord_list[13][0], cord_list[13][1] + arrow_point_size)], fill='#ffffff')

    output_filename = latin_name.lower().replace(' ', '-')
    output_path = f'{website_img_path}/{output_filename}-taxonomy.jpg'
    
    # img.show()
    img.save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path


def img_cycle_of_life(item):
    genus = item['genus']
    species = item['species']
    latin_name = f'{genus} {species}'

    bg_color = '#ecfdf5'
    fg_color = '#1c1917'

    resampler = 4
    w, h = 768 * resampler, 768 * resampler
    icon_size = (64 * resampler, 64 * resampler)
    img = Image.new(mode="RGBA", size=(w, h), color=bg_color)
    icon = Image.open("assets/icons/seeds.png")

    draw = ImageDraw.Draw(img)

    line_width = 0.02
    outer_circle_size = 0.8
    inner_circle_size = 0.15

    circle_radius = w//2 * outer_circle_size
    draw.ellipse((
        w//2 - circle_radius, h//2 - circle_radius, 
        w//2 + circle_radius, h//2 + circle_radius), 
        fill=fg_color)
    circle_radius = w//2 * (outer_circle_size - line_width)
    draw.ellipse((
        w//2 - circle_radius, h//2 - circle_radius, 
        w//2 + circle_radius, h//2 + circle_radius), 
        fill=bg_color)

    icon_circle_radius = w//2 * inner_circle_size
    draw.ellipse((
        w//2 - icon_circle_radius, h//2 - icon_circle_radius - circle_radius, 
        w//2 + icon_circle_radius, h//2 + icon_circle_radius - circle_radius), 
        fill=fg_color)
    icon_circle_radius = w//2 * (inner_circle_size - line_width)
    draw.ellipse((
        w//2 - icon_circle_radius, h//2 - icon_circle_radius - circle_radius, 
        w//2 + icon_circle_radius, h//2 + icon_circle_radius - circle_radius), 
        fill=bg_color)

    icon.thumbnail(icon_size, Image.Resampling.LANCZOS)
    img.paste(icon, (
        w//2 - icon_size[0]//2,
        h//2 - icon_size[1]//2 - int(circle_radius)
        ), icon)
        
    font_size = 96
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = 'Seed Germination'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((
        w//2 - line_w//2, 
        h//2 - line_h//2 - circle_radius + int(icon_circle_radius*1.6)), line, fg_color, font=font)

    output_filename = latin_name.lower().replace(' ', '-')
    output_path = f'{website_img_path}/{output_filename}-cycle-of-life.jpg'

    img.thumbnail((w//resampler, h//resampler), Image.Resampling.LANCZOS)
    
    img.convert('RGB').save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path


def draw_line(draw, e_x, e_y, t_x, t_y, line_spacing):
    if e_x >= t_x and e_y >= t_y:
        thickness = 6
        draw.line((e_x, e_y, e_x + (t_y - e_y) + line_spacing, e_y + (t_y - e_y) + line_spacing), fill='#ffffff', width=thickness)
        draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
        thickness = 2
        draw.line((e_x, e_y, e_x + (t_y - e_y) + line_spacing, e_y + (t_y - e_y) + line_spacing), fill='#000000', width=thickness)
        draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))
    elif e_x <= t_x and e_y >= t_y:
        thickness = 6
        draw.line((e_x, e_y, e_x - (t_y - e_y) - line_spacing, t_y + line_spacing), fill='#ffffff', width=thickness)
        draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
        thickness = 2
        draw.line((e_x, e_y, e_x - (t_y - e_y) - line_spacing, t_y + line_spacing), fill='#000000', width=thickness)
        draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))
    elif e_x >= t_x and e_y <= t_y:
        thickness = 6
        draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#ffffff', width=thickness)
        draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
        thickness = 2
        draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#000000', width=thickness)
        draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))
    elif e_x <= t_x and e_y <= t_y:
        thickness = 6
        draw.line((e_x, e_y, e_x + (t_y - e_y), t_y), fill='#ffffff', width=thickness)
        draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
        thickness = 2
        draw.line((e_x, e_y, e_x + (t_y - e_y), t_y), fill='#000000', width=thickness)
        draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))


def img_morphology_roots(row, latin_name, category, attribute, file):
    # for i, item in enumerate(row):
    #     print(f'{i} - {item}')

    img_w = 1024
    img_h = 1024
    img = Image.new(mode="RGBA", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)
    icon = Image.open("assets/icons/roots.png")

    icon_size = 384
    icon_size = 512
    icon.thumbnail((icon_size, icon_size), Image.Resampling.LANCZOS)
    img.paste(icon, (img_w//2 - icon_size//2, img_h//2 - icon_size//2), icon)
    
    font_size = 48
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'{latin_name} {file} morphology'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((
        img_w//2 - line_w//2, 
        30), line, '#000000', font=font)

    # y = img_h - 130
    # thickness = 8
    # draw.line((img_w//2 - icon_size//2, y, img_w//2 + icon_size//2, y), fill='#000000', width=thickness)
    # draw.line((img_w//2 - icon_size//2, y + 50//2, img_w//2 - icon_size//2, y - 50//2), fill='#000000', width=thickness)
    # draw.line((img_w//2 + icon_size//2, y + 50//2, img_w//2 + icon_size//2, y - 50//2), fill='#000000', width=thickness)

    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)

    # line = 'Width: ~20 cm'
    # line_w = font.getbbox(line)[2]
    # line_h = font.getbbox(line)[3]
    # draw.text((img_w//2 - line_w//2, y + line_h), line, '#000000', font=font)

    x = img_w - 130
    thickness = 8
    draw.line((x, img_h//2 - icon_size//3, x, img_h//2 + icon_size//3), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 - icon_size//3, x + 50//2, img_h//2 - icon_size//3), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 + icon_size//3, x + 50//2, img_h//2 + icon_size//3), fill='#000000', width=thickness)

    val = sanitize(row[8])
    line = f'Length: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    img_v = Image.new(mode="RGBA", size=(line_w, line_h), color='#ffffff')
    draw_v = ImageDraw.Draw(img_v)
    draw_v.text((0, 0), line, '#000000', font=font)
    img_v = img_v.rotate(90, expand=1)
    img.paste(img_v, (x + line_h, img_h//2 - line_w//2), img_v)

    val = sanitize_one_word(row[9])
    line = f'Color: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 200), line, '#000000', font=font)
    thickness = 6
    draw.line((200 + line_h + 10, 200 + line_h + 10, 475, 475), fill='#ffffff', width=thickness)
    draw.ellipse((475-thickness, 475-thickness, 475+thickness, 475+thickness), fill=(255,255,255,255))
    thickness = 2
    draw.line((200 + line_h + 10, 200 + line_h + 10, 475, 475), fill='#000000', width=thickness)
    # draw.line((50, 200 + line_h + 10, 200 + line_h + 10 + thickness//3, 200 + line_h + 10), fill='#000000', width=thickness)
    draw.ellipse((475-thickness-1, 475-thickness-1, 475+thickness+1, 475+thickness+1), fill=(0,0,0,255))


    e_x, e_y = 675, 625
    t_x, t_y = 675, 725
    val = sanitize(row[7])
    line = f'Diameter: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw.line((e_x, e_y, e_x + (t_y - e_y), t_y), fill='#ffffff', width=thickness)
    draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
    thickness = 2
    draw.line((e_x, e_y, e_x + (t_y - e_y), t_y), fill='#000000', width=thickness)
    draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))

    e_x, e_y = 585, 580
    t_x, t_y = 250, 825
    val = sanitize_one_word(row[10])
    line = f'Texture: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#ffffff', width=thickness)
    draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
    thickness = 2
    draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#000000', width=thickness)
    draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))

    e_x, e_y = 520, 400
    t_x, t_y = 600, 300
    val = sanitize_one_word(row[1])
    line = f'Type: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw.line((e_x, e_y, e_x - (t_y - e_y) - line_h, t_y + line_h), fill='#ffffff', width=thickness)
    draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
    thickness = 2
    draw.line((e_x, e_y, e_x - (t_y - e_y) - line_h, t_y + line_h), fill='#000000', width=thickness)
    draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))

    e_x, e_y = 295, 605
    t_x, t_y = 100, 700
    val = sanitize_one_word(row[4])
    line = f'Tips: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#ffffff', width=thickness)
    draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
    thickness = 2
    draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#000000', width=thickness)
    draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))


    attribute = attribute.replace('/', '-')
    featured_image_filename = f'website/images/{entity}-{category}-{attribute}-{file}.jpg'
    
    img = img.convert('RGB')
    # img = img.resize((768, 768))
    img.save(featured_image_filename, format='JPEG', subsampling=0, quality=100)

    # print(featured_image_filpath)
    filepath = '/' + '/'.join(featured_image_filename.split('/')[1:])

    # img.show()
    # quit()

    return filepath


def img_morphology_stems(row, latin_name, category, attribute, file):
    # with open('database/tables/morphology/stems.csv', encoding='utf-8') as f:
    #     rows = f.readlines()

    # for i, item in enumerate(rows[0].split('\\')):
    #     print(f'{i} - {item}')
    # for i, item in enumerate(row):
    #     print(f'{i} - {item}')

    img_w = 1024
    img_h = 1024
    img = Image.new(mode="RGBA", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)
    icon = Image.open("assets/icons/stems.png")

    icon_size = 384
    icon_size = 512
    icon.thumbnail((icon_size, icon_size), Image.Resampling.LANCZOS)
    img.paste(icon, (img_w//2 - icon_size//2, img_h//2 - icon_size//2), icon)
    
    font_size = 48
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'{latin_name} {file} morphology'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2,30), line, '#000000', font=font)
    
    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)

    y = img_h - 130
    thickness = 8
    div_h = 32
    draw.line((img_w//2 - icon_size//div_h, y, img_w//2 + icon_size//div_h, y), fill='#000000', width=thickness)
    draw.line((img_w//2 - icon_size//div_h, y + 50//2, img_w//2 - icon_size//div_h, y - 50//2), fill='#000000', width=thickness)
    draw.line((img_w//2 + icon_size//div_h, y + 50//2, img_w//2 + icon_size//div_h, y - 50//2), fill='#000000', width=thickness)

    val = sanitize(row[5])
    line = f'Diameter: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, y + line_h * 1.5), line, '#000000', font=font)

    x = img_w - 130
    thickness = 8
    div_h = 2
    draw.line((x, img_h//2 - icon_size//div_h, x, img_h//2 + icon_size//div_h), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 - icon_size//div_h, x + 50//2, img_h//2 - icon_size//div_h), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 + icon_size//div_h, x + 50//2, img_h//2 + icon_size//div_h), fill='#000000', width=thickness)


    val = sanitize(row[4])
    line = f'Height: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    img_v = Image.new(mode="RGBA", size=(line_w, line_h), color='#ffffff')
    draw_v = ImageDraw.Draw(img_v)
    draw_v.text((0, 0), line, '#000000', font=font)
    img_v = img_v.rotate(90, expand=1)
    img.paste(img_v, (x + line_h, img_h//2 - line_w//2), img_v)

    # e_x, e_y = 510, 750
    # t_x, t_y = 650, 950
    # val = sanitize(row[5])
    # line = f'Diameter: {val}'
    # line_w = font.getbbox(line)[2]
    # line_h = font.getbbox(line)[3]
    # line_spacing = line_h * 1.5
    # draw.text((t_x, t_y), line, '#000000', font=font)
    # thickness = 6
    # draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 425, 465
    t_x, t_y = 50, 200
    val = sanitize_one_word(row[6])
    line = f'Color: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 600, 285
    t_x, t_y = 601, 150
    val = sanitize_one_word(row[7])
    line = f'Texture: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 510, 450
    t_x, t_y = 50, 700
    val = sanitize_one_word(row[9])
    line = f'Node: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 510, 500
    t_x, t_y = 550, 600
    val = sanitize(row[10])
    line = f'Internode: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)

    e_x, e_y = 510, 650
    t_x, t_y = 200, 800
    val = sanitize_one_word(row[1])
    line = f'Type: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)


    attribute = attribute.replace('/', '-')
    featured_image_filename = f'website/images/{entity}-{category}-{attribute}-{file}.jpg'
    
    img = img.convert('RGB')
    # img = img.resize((768, 768))
    img.save(featured_image_filename, format='JPEG', subsampling=0, quality=100)

    # print(featured_image_filpath)
    filepath = '/' + '/'.join(featured_image_filename.split('/')[1:])

    # img.show()
    # quit()

    return filepath


def img_morphology_leaves(row, latin_name, category, attribute, file):
    # with open('database/tables/morphology/leaves.csv', encoding='utf-8') as f:
    #     rows = f.readlines()

    # for i, item in enumerate(rows[0].split('\\')):
    #     print(f'{i} - {item}')
    # for i, item in enumerate(row):
    #     print(f'{i} - {item}')

    img_w = 1024
    img_h = 1024
    img = Image.new(mode="RGBA", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)
    icon = Image.open("assets/icons/leaves.png")

    icon_size = 384
    icon_size = 384
    icon.thumbnail((icon_size, icon_size), Image.Resampling.LANCZOS)
    img.paste(icon, (img_w//2 - icon_size//2, img_h//2 - icon_size//2), icon)
    
    font_size = 48
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'{latin_name} {file} morphology'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2,30), line, '#000000', font=font)
    
    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)

    y = img_h - 130
    thickness = 8
    div_h = 2
    draw.line((img_w//2 - icon_size//div_h, y, img_w//2 + icon_size//div_h, y), fill='#000000', width=thickness)
    draw.line((img_w//2 - icon_size//div_h, y + 50//2, img_w//2 - icon_size//div_h, y - 50//2), fill='#000000', width=thickness)
    draw.line((img_w//2 + icon_size//div_h, y + 50//2, img_w//2 + icon_size//div_h, y - 50//2), fill='#000000', width=thickness)

    val = sanitize(row[6])
    line = f'Width: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, y + line_h * 1.5), line, '#000000', font=font)

    x = img_w - 130
    thickness = 8
    div_h = 2
    draw.line((x, img_h//2 - icon_size//div_h, x, img_h//2 + icon_size//div_h), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 - icon_size//div_h, x + 50//2, img_h//2 - icon_size//div_h), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 + icon_size//div_h, x + 50//2, img_h//2 + icon_size//div_h), fill='#000000', width=thickness)


    val = sanitize(row[5])
    line = f'Lenght: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    img_v = Image.new(mode="RGBA", size=(line_w, line_h), color='#ffffff')
    draw_v = ImageDraw.Draw(img_v)
    draw_v.text((0, 0), line, '#000000', font=font)
    img_v = img_v.rotate(90, expand=1)
    img.paste(img_v, (x + line_h, img_h//2 - line_w//2), img_v)

    e_x, e_y = 450, 490
    t_x, t_y = 50, 150
    val = sanitize_one_word(row[8])
    line = f'Color: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 650, 450
    t_x, t_y = 400, 250
    val = sanitize_one_word(row[9])
    line = f'Texture: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 600, 550
    t_x, t_y = 750, 800
    val = sanitize_one_word(row[2])
    line = f'Shape: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 535, 630
    t_x, t_y = 400, 700
    val = sanitize_one_word(row[13])
    line = f'Margin: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)

    e_x, e_y = 345, 680
    t_x, t_y = 100, 800
    val = sanitize_one_word(row[17])
    line = f'Attachment: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)


    attribute = attribute.replace('/', '-')
    featured_image_filename = f'website/images/{entity}-{category}-{attribute}-{file}.jpg'
    
    img = img.convert('RGB')
    # img = img.resize((768, 768))
    img.save(featured_image_filename, format='JPEG', subsampling=0, quality=100)

    # print(featured_image_filpath)
    filepath = '/' + '/'.join(featured_image_filename.split('/')[1:])

    # img.show()
    # quit()

    return filepath


def generate_image_habitat(entity):
    input_filepath = f'articles-images/{entity}-botany-habitat.jpg'
    outut_filepath = f'website/images/{entity}-botany-habitat.jpg'

    img = Image.open(input_filepath)
    img.save(outut_filepath, format='JPEG', subsampling=0, quality=100)

    image_filpath = '/' + '/'.join(outut_filepath.split('/')[1:])

    return image_filpath


def img_cheasheet(latin_name, title, lst, img_name):
    img_w, img_h = 768, 2000
    bg_dark_1 = "#047857"
    bg_light_1 = "#ecfdf5"
    bg_light_2 = "#d1fae5"
    bg_light_3 = "#a7f3d0"
    fg_light = '#ffffff'
    fg_dark = '#0f172a'

    img = Image.new(mode="RGB", size=(img_w, img_h), color=bg_light_1)
    draw = ImageDraw.Draw(img)

    rect_h = 0
    line_x = 50
    line_y = 20

    font_size = 36
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    lines = [title, latin_name]
    for i, line in enumerate(lines):
        rect_h += font.getbbox('y')[3]
    rect_h += line_y * 2
        
    draw.rectangle(((0, 0), (img_w, rect_h)), fill=bg_dark_1)
    for i, line in enumerate(lines):
        line_w = font.getbbox(line)[2]
        line_h = font.getbbox('y')[3]
        draw.text((img_w//2 - line_w//2, line_y + line_h * i), line, fg_light, font=font)

    font_size = 16
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    
    title_rect_h = rect_h
    line_y = title_rect_h + 50

    rect_h = 0

    full_len = len(lst)
    half_len_1 = math.ceil(full_len/2)
    half_len_2 = full_len - half_len_1
    sublist_1 = lst[:half_len_1]
    sublist_2 = lst[half_len_1:]

    for l in sublist_1:
        bg = 0
        for i, x in enumerate(l):
            line = x
            line_x = 50
            line_y += rect_h
            line_w = font.getbbox(line)[2]
            line_h = font.getbbox('y')[3]
            rect_x = line_x - 20
            rect_y = line_y - 10
            rect_w = img_w//2 - 50
            rect_h = line_h + 20
            if i == 0:
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_dark_1)
                draw.text((line_x, line_y), line, fg_light, font=font)
            elif bg == 0:
                bg = 1
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_2)
                draw.text((line_x, line_y), line, fg_dark, font=font)
            else:
                bg = 0
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_1)
                draw.text((line_x, line_y), line, fg_dark, font=font)
        line_y += rect_h
        rect_y = line_y - 10
        draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + 6)), fill=bg_dark_1) 

    max_height = line_y
    
    line_y = title_rect_h + 50

    rect_h = 0
    for l in sublist_2:
        bg = 0
        for i, x in enumerate(l):
            line = x
            line_x = img_w//2 + 36
            line_y += rect_h
            line_w = font.getbbox(line)[2]
            line_h = font.getbbox('y')[3]
            rect_x = line_x - 20
            rect_y = line_y - 10
            rect_w = img_w//2 - 50
            rect_h = line_h + 20
            if i == 0:
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_dark_1)
                draw.text((line_x, line_y), line, fg_light, font=font)
            elif bg == 0:
                bg = 1
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_2)
                draw.text((line_x, line_y), line, fg_dark, font=font)
            else:
                bg = 0
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_1)
                draw.text((line_x, line_y), line, fg_dark, font=font)
        line_y += rect_h
        rect_y = line_y - 10
        draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + 6)), fill=bg_dark_1) 

    if max_height < line_y : max_height = line_y

    area = (0, 0, img_w, max_height + 30)
    img = img.crop(area)

    
    output_filename = latin_name.lower().replace(' ', '-')
    output_path = f'{website_img_path}/{output_filename}-{img_name}.jpg'
    img.save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path


# def generate_featured_image(entity, attribute_lst, title):
#     attribute = '/'.join(attribute_lst)
#     attribute_filename = attribute.replace('/', '-')
#     featured_image_filename = f'{entity}-{attribute_filename}.jpg'
#     featured_image_filpath = img_resize(f'articles-images/{featured_image_filename}')

#     img = Image.open(featured_image_filpath)
#     # background  = Image.open("articles-images/acorus-calamus-botany-morphology-old.jpg")

#     w_banner = img.size[0]
#     y_banner = img.size[1] // 2
#     base = Image.new('RGBA', (w_banner, y_banner), (0, 0, 0, 0))
#     top = Image.new('RGBA', (w_banner, y_banner), (0, 0, 0, 255))
#     # base = Image.new('RGBA', (w_banner, y_banner), '#0f766e')
#     # top = Image.new('RGBA', (w_banner, y_banner), '#0f766e')
#     mask = Image.new('L', (w_banner, y_banner))
#     mask_data = []
#     for y in range(y_banner):
#         mask_data.extend([int(255 * (y / y_banner))] * w_banner)
#     mask.putdata(mask_data)
    
#     y_img = img.size[1]
#     base.paste(top, (0, 0), mask)

#     img.paste(base, (0, y_img - y_banner), base)

    
#     latin_name = entity.replace('-', ' ').capitalize()
#     line = f'{title}'
#     draw = ImageDraw.Draw(img)
#     font_size = 36
#     font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
#     line_w = font.getbbox(line)[2]
#     line_h = font.getbbox('y')[3]
#     draw.text((w_banner//2 - line_w//2, y_img - line_h - 30), line, '#ffffff', font=font)

#     img.save(f'{featured_image_filpath}', format='JPEG', subsampling=0, quality=100)

#     # print(featured_image_filpath)
#     featured_image_filpath = '/' + '/'.join(featured_image_filpath.split('/')[1:])

#     return featured_image_filpath


def generate_featured_image(entity, attribute_lst, title):
    attribute = '/'.join(attribute_lst)
    attribute_filename = attribute.replace('/', '-')
    featured_image_filpath = img_resize(f'articles-images/{entity}-{attribute_filename}.jpg')

    img = Image.open(featured_image_filpath)
    # background  = Image.open("articles-images/acorus-calamus-botany-morphology-old.jpg")

    w_banner = img.size[0]
    y_banner = img.size[1] // 2
    base = Image.new('RGBA', (w_banner, y_banner), (0, 0, 0, 0))
    top = Image.new('RGBA', (w_banner, y_banner), (0, 0, 0, 255))
    # base = Image.new('RGBA', (w_banner, y_banner), '#0f766e')
    # top = Image.new('RGBA', (w_banner, y_banner), '#0f766e')
    mask = Image.new('L', (w_banner, y_banner))
    mask_data = []
    for y in range(y_banner):
        mask_data.extend([int(255 * (y / y_banner))] * w_banner)
    mask.putdata(mask_data)
    
    y_img = img.size[1]
    base.paste(top, (0, 0), mask)

    img.paste(base, (0, y_img - y_banner), base)

    
    latin_name = entity.replace('-', ' ').capitalize()
    line = f'{title}'
    draw = ImageDraw.Draw(img)
    font_size = 36
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox('y')[3]
    draw.text((w_banner//2 - line_w//2, y_img - line_h - 30), line, '#ffffff', font=font)

    img.save(f'{featured_image_filpath}', format='JPEG', subsampling=0, quality=100)

    # print(featured_image_filpath)
    featured_image_filpath = '/' + '/'.join(featured_image_filpath.split('/')[1:])

    return featured_image_filpath


def generate_image_taxonomy(entity, attribute_lst, lst):
    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    
    img_background = Image.open(f"articles-images/{entity}-botanical-profile-3x4.jpg")

    # img_background_w = img_background.getbbox()[2]
    # print(img_background_w)

    polygon_w = 1024
    polygon_h = 768
    
    img_background_w = 576
    img_background_h = 768

    # polygon = Image.new(mode="RGBA", size=(polygon_w*2, polygon_h*2), color='#fafafa')
    # xy = [
    #     (0, 0,),
    #     (img_background_w*2, 0,),
    #     (img_w*2 - img_background_w*2, img_h*2,),
    #     (0, img_h*2,),
    # ]
    # draw.polygon(xy, fill ="#0f766e") 
    # polygon.thumbnail((polygon_w, polygon_h), Image.Resampling.LANCZOS)


    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    # img.paste(polygon, (img_w - img_background_w, 0), polygon)

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    
    latin_name = entity.replace('-', ' ').capitalize()

    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'{latin_name}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)
    
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'TAXONOMY'
    draw.text((50, 50 + line_h * line_spacing), line, '#ffffff', font=font)
    
    line_spacing = 1.5
    line_h = font.getbbox(lst[0])[3]
    for i, line in enumerate(lst):
        draw.text((50, 50 + line_h * line_spacing + 100 + lst_line_height * i), line, '#ffffff', font=font)

    draw.text((50, img_h - 50 - line_h), '© TerraWhisper.com', '#ffffff', font=font)
    
    # img.show()
    # quit()

    out_attr_lst = '-'.join(attribute_lst)
    out_filename = f'website/images/{entity}-{out_attr_lst}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = '/' + '/'.join(out_filename.split('/')[1:])

    # img.show()
    # quit()

    return filepath


def generate_image_history(entity, attribute_lst, lst):
    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    img_background = Image.open(f"articles-images/{entity}-history-3x4.jpg")
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    
    latin_name = entity.replace('-', ' ').capitalize()

    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'{latin_name}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)
    
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'HISTORICAL USES'
    draw.text((50, 50 + line_h * line_spacing), line, '#ffffff', font=font)
    
    line_spacing = 1.5
    line_h = font.getbbox(lst[0])[3]
    for i, line in enumerate(lst):
        draw.text((50, 50 + line_h * line_spacing + 100 + lst_line_height * i), line, '#ffffff', font=font)

    draw.text((50, img_h - 50 - line_h), '© TerraWhisper.com', '#ffffff', font=font)
    
    out_attr_lst = '-'.join(attribute_lst)
    out_filename = f'website/images/{entity}-{out_attr_lst}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = '/' + '/'.join(out_filename.split('/')[1:])

    return filepath


def generate_image_medicinal_properties(entity, attribute_lst, lst):
    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    img_background = Image.open(f"articles-images/{entity}-medicine-properties-3x4.jpg")
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    
    latin_name = entity.replace('-', ' ').capitalize()

    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'{latin_name}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)
    
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'MEDICINAL PROPERTIES'
    draw.text((50, 50 + line_h * line_spacing), line, '#ffffff', font=font)
    
    line_spacing = 1.5
    line_h = font.getbbox(lst[0])[3]
    for i, line in enumerate(lst):
        draw.text((50, 50 + line_h * line_spacing + 100 + lst_line_height * i), line, '#ffffff', font=font)

    draw.text((50, img_h - 50 - line_h), '© TerraWhisper.com', '#ffffff', font=font)
    
    out_attr_lst = '-'.join(attribute_lst)
    out_filename = f'website/images/{entity}-{out_attr_lst}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = '/' + '/'.join(out_filename.split('/')[1:])

    return filepath


def generate_image_medicinal_constituents(entity, attribute_lst, lst):
    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    img_background = Image.open(f"articles-images/{entity}-medicine-constituents-3x4.jpg")
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    
    latin_name = entity.replace('-', ' ').capitalize()

    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'{latin_name}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)
    
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'MEDICINAL CONSTITUENTS'
    draw.text((50, 50 + line_h * line_spacing), line, '#ffffff', font=font)
    
    line_spacing = 1.5
    line_h = font.getbbox(lst[0])[3]
    for i, line in enumerate(lst):
        draw.text((50, 50 + line_h * line_spacing + 100 + lst_line_height * i), line, '#ffffff', font=font)

    draw.text((50, img_h - 50 - line_h), '© TerraWhisper.com', '#ffffff', font=font)
    
    out_attr_lst = '-'.join(attribute_lst)
    out_filename = f'website/images/{entity}-{out_attr_lst}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = '/' + '/'.join(out_filename.split('/')[1:])

    return filepath


def generate_image_template_1(entity, attribute_lst, lst):
    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    attributes_path = '-'.join(attribute_lst)
    img_background = Image.open(f"articles-images/{entity}-{attributes_path}.jpg")

    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    latin_name = entity.replace('-', ' ').capitalize()

    current_y = 0

    # Title
    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.title()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)

    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    title_tmp = common_name.title()
    title_w = font.getbbox(title_tmp)[2]

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    subtitle_tmp = attribute_lst[-1].upper()
    subtitle_tmp = subtitle_tmp.split('(')[0]
    subtitle_w = font.getbbox(subtitle_tmp)[2]
    if subtitle_w > 475:
        character_len = len(subtitle_tmp)
        font_size = 800 // character_len
        font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
        subtitle_w = font.getbbox(subtitle_tmp)[2]

    if title_w > subtitle_w: divider_w = title_w
    else: divider_w = subtitle_w
    draw.rectangle(((50, 50 + line_h + 10), (50 + divider_w, 50 + line_h + 10 + 2)), '#ffffff')
    current_y += 50 + line_h + 10 + 2
    
    # Subtitle
    line = subtitle_tmp
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 10), line, '#ffffff', font=font)
    current_y += 50 + line_h
    
    line_spacing = 1.5
    line_h = font.getbbox(lst[0])[3]
    for i, line in enumerate(lst):
        line = line.split('(')[0]
        draw.text((50, 50 + line_h * line_spacing + 100 + lst_line_height * i), line, '#ffffff', font=font)

    draw.text((50, img_h - 50 - line_h), '© TerraWhisper.com', '#ffffff', font=font)
    
    out_attr_lst = '-'.join(attribute_lst)
    out_filename = f'website/images/{entity}-{out_attr_lst}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = '/' + '/'.join(out_filename.split('/')[1:])

    return filepath
    

def generate_image_template_no_cuisine(entity, attribute_lst):
    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGBA", size=(img_w, img_h), color='#fafafa')
    # img = img.convert("RGB")

    attributes_path = '-'.join(attribute_lst)
    try: img_background = Image.open(f"articles-images/{entity}-{attributes_path}.jpg")
    except: img_background = Image.open(f"articles-images/{entity}-{attributes_path}-3x4.jpg")

    img.paste(img_background, (0, 0))

    overlay = Image.new('RGBA', size=(img_w, img_h), color='#fafafa')
    draw_overlay = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    draw_overlay.rectangle(((0, 0), (img_w, img_h)), fill='#000000cc')

    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")

    # xy = [
    #     (0, 0,),
    #     (img_background_w, 0,),
    #     (img_w - img_background_w, img_h,),
    #     (0, img_h,),
    # ]
    # draw.polygon(xy, fill ="#0f766e") 

    draw = ImageDraw.Draw(img)
    latin_name = entity.replace('-', ' ').capitalize()

    current_y = 0

    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'{latin_name}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, 50), line, '#ffffff', font=font)
    current_y += 50 + line_h
    
    
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    attributes_subtitle = ' / '.join(attribute_lst).upper()
    line = attributes_subtitle
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, current_y + 10), 'CULINARY PROFILE', '#ffffff', font=font)
    
    font_size = 96
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = 'NOT EDIBLE'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h//2 - line_h//2), line, '#ffffff', font=font)

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = '© TerraWhisper.com'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h - 50 - line_h), line, '#ffffff', font=font)
    
    out_attr_lst = '-'.join(attribute_lst)
    out_filename = f'website/images/{entity}-{out_attr_lst}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = '/' + '/'.join(out_filename.split('/')[1:])

    return filepath

    
def generate_image_template_medicine_benefits(entity, common_name, image_filename, item):
    attribute_lst = ['medicine', 'benefits', item]

    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits/benefits.csv', entity)
    rows_constituents = [f'- {x[3].title()}' for x in rows if x[1] == item.lower().replace(' ', '-').strip() and x[2] == 'constituent']
    lst_constituents = rows_constituents[:3]
    rows_preparations = [f'- {x[3].title()}' for x in rows if x[1] == item.lower().replace(' ', '-').strip() and x[2] == 'preparation']
    lst_preparations = rows_preparations[:3]

    bg_image_path = f'{image_folder_old}/{entity}/medicine/benefits/{image_filename}'

    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    attributes_path = '-'.join(attribute_lst)
    img_background = Image.open(bg_image_path)
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    current_y = 0

    # Title
    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.title()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)

    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    title_tmp = common_name.title()
    title_w = font.getbbox(title_tmp)[2]

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    subtitle_tmp = attribute_lst[-1].upper()
    subtitle_tmp = subtitle_tmp.split('(')[0]
    subtitle_w = font.getbbox(subtitle_tmp)[2]
    if subtitle_w > 475:
        character_len = len(subtitle_tmp)
        font_size = 800 // character_len
        font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
        subtitle_w = font.getbbox(subtitle_tmp)[2]


    if title_w > subtitle_w: divider_w = title_w
    else: divider_w = subtitle_w
    draw.rectangle(((50, 50 + line_h + 10), (50 + divider_w, 50 + line_h + 10 + 2)), '#ffffff')
    current_y += 50 + line_h + 10 + 2
    
    # Subtitle
    line = subtitle_tmp
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 10), line, '#ffffff', font=font)
    current_y += 10 + line_h

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)

    # Constituents
    font = ImageFont.truetype("assets/fonts/arialbd.ttf", font_size)
    text = "Constituents:"
    line_h = font.getbbox(text)[3]
    draw.text((50, current_y + 50), text, '#ffffff', font=font)
    current_y += 50 + line_h
    
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_spacing = 1.3
    line_h = font.getbbox('y')[3]
    for i, line in enumerate(lst_constituents):
        draw.text((80, current_y + 10 + line_h * line_spacing * i), line, '#ffffff', font=font)
    current_y += 10 + line_h * line_spacing * i + line_h

    # Preparations
    font = ImageFont.truetype("assets/fonts/arialbd.ttf", font_size)
    text = "Preparations:"
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 30), text, '#ffffff', font=font)
    current_y += 30 + line_h
    
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_spacing = 1.3
    line_h = font.getbbox('y')[3]
    for i, line in enumerate(lst_preparations):
        draw.text((80, current_y + 10 + line_h * line_spacing * i), line, '#ffffff', font=font)
    current_y += 10 + line_h * line_spacing * i + line_h

    # Copy
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    draw.text((50, img_h - 50 - line_h), '© TerraWhisper.com', '#ffffff', font=font)

    img.thumbnail((768, 576), Image.Resampling.LANCZOS)
    
    # Export
    out_attr_lst = '-'.join(attribute_lst).lower().replace(' ', '-')
    out_filename = f'website/images/{entity}-{out_attr_lst}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = '/' + '/'.join(out_filename.split('/')[1:])

    return filepath

    
def generate_image_template_medicine_benefits_2(entity, common_name, image_filename, item):
    attribute_lst = ['medicine', 'benefits', item]

    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits/benefits.csv', entity)
    rows = [f'- {x[3].title()}' for x in rows if x[1] == item.lower().replace(' ', '-').strip() and x[2] == 'image']
    lst = rows[:10]

    bg_image_path = f'{image_folder_old}/{entity}/medicine/benefits/{image_filename}'

    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    attributes_path = '-'.join(attribute_lst)
    img_background = Image.open(bg_image_path)
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    current_y = 0

    # Title
    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.title()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)

    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    title_tmp = common_name.title()
    title_w = font.getbbox(title_tmp)[2]

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    subtitle_tmp = attribute_lst[-1].upper()
    subtitle_tmp = subtitle_tmp.split('(')[0]
    subtitle_w = font.getbbox(subtitle_tmp)[2]
    if subtitle_w > 475:
        character_len = len(subtitle_tmp)
        font_size = 800 // character_len
        font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
        subtitle_w = font.getbbox(subtitle_tmp)[2]

    if title_w > subtitle_w: divider_w = title_w
    else: divider_w = subtitle_w
    draw.rectangle(((50, 50 + line_h + 10), (50 + divider_w, 50 + line_h + 10 + 2)), '#ffffff')
    current_y += 50 + line_h + 10 + 2
    
    # Subtitle
    line = subtitle_tmp
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 10), line, '#ffffff', font=font)
    current_y += 50 + line_h

    # List
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_spacing = 1.3
    line_h = font.getbbox('y')[3]
    for i, line in enumerate(lst):
        line = line.split('(')[0]
        draw.text((50, current_y + 10 + line_h * line_spacing * i), line, '#ffffff', font=font)
    current_y += 10 + line_h * line_spacing * i + line_h

    # Copy
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    draw.text((50, img_h - 50 - line_h), '© TerraWhisper.com', '#ffffff', font=font)

    img.thumbnail((768, 576), Image.Resampling.LANCZOS)
    
    # Export
    out_attr_lst = '-'.join(attribute_lst).lower().replace(' ', '-')
    out_filename = f'website/images/{entity}-{out_attr_lst}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = '/' + '/'.join(out_filename.split('/')[1:])

    return filepath

    
def generate_image_template_medicine_preparations(entity, common_name, image_filename, item):
    attribute_lst = ['medicine', 'preparations', item]

    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/preparations/preparations.csv', entity)
    rows_constituents = [f'- {x[3].title()}' for x in rows if x[1] == item.lower().replace(' ', '-').strip() and x[2] == 'image']
    lst_constituents = rows_constituents[:10]

    bg_image_path = f'{image_folder_old}/{entity}/medicine/preparations/{image_filename}'

    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    attributes_path = '-'.join(attribute_lst)
    img_background = Image.open(bg_image_path)
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    current_y = 0

    # Title
    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.title()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)

    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    title_tmp = common_name.title()
    title_w = font.getbbox(title_tmp)[2]

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    subtitle_tmp = attribute_lst[-1].upper()
    subtitle_tmp = subtitle_tmp.split('(')[0]
    subtitle_w = font.getbbox(subtitle_tmp)[2]
    if subtitle_w > 475:
        character_len = len(subtitle_tmp)
        font_size = 800 // character_len
        font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
        subtitle_w = font.getbbox(subtitle_tmp)[2]

    if title_w > subtitle_w: divider_w = title_w
    else: divider_w = subtitle_w
    draw.rectangle(((50, 50 + line_h + 10), (50 + divider_w, 50 + line_h + 10 + 2)), '#ffffff')
    current_y += 50 + line_h + 10 + 2
    
    # Subtitle
    line = subtitle_tmp
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 10), line, '#ffffff', font=font)
    current_y += 50 + line_h

    # List
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    max_len = 0
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    for item in lst_constituents:
        line_w = font.getbbox(item)[2]
        if max_len < line_w: max_len = line_w
    # print(max_len)
    if max_len > 450:
        font_size = 20
        line_spacing = 1.5
    elif max_len > 500:
        font_size = 18
        line_spacing = 1.7
    else:
        line_spacing = 1.3
    

    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_h = font.getbbox('y')[3]
    for i, line in enumerate(lst_constituents):
        line = line.split('(')[0]
        draw.text((50, current_y + 10 + line_h * line_spacing * i), line, '#ffffff', font=font)
    current_y += 10 + line_h * line_spacing * i + line_h

    # Copy
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    draw.text((50, img_h - 50 - line_h), '© TerraWhisper.com', '#ffffff', font=font)

    img.thumbnail((768, 576), Image.Resampling.LANCZOS)
    
    # Export
    out_attr_lst = '-'.join(attribute_lst).lower().replace(' ', '-')
    out_filename = f'website/images/{entity}-{out_attr_lst}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = '/' + '/'.join(out_filename.split('/')[1:])

    return filepath


def generate_image_template_2(entity, common_name, image_filename, attribute_lst, table):
    item = attribute_lst[-1]

    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/{table}/{table}.csv', entity)
    rows_constituents = [f'- {x[3].title()}' for x in rows if x[1] == item.lower().replace(' ', '-').strip() and x[2] == 'image']
    lst_constituents = rows_constituents[:10]

    bg_image_path = f'{image_folder_old}/{entity}/medicine/{table}/{image_filename}'

    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    attributes_path = '-'.join(attribute_lst)
    img_background = Image.open(bg_image_path)
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    current_y = 0

    # Title
    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.title()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)

    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    title_tmp = common_name.title()
    title_w = font.getbbox(title_tmp)[2]

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    subtitle_tmp = attribute_lst[-1].upper()
    subtitle_tmp = subtitle_tmp.split('(')[0]
    subtitle_w = font.getbbox(subtitle_tmp)[2]
    if subtitle_w > 475:
        character_len = len(subtitle_tmp)
        font_size = 800 // character_len
        font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
        subtitle_w = font.getbbox(subtitle_tmp)[2]

    if title_w > subtitle_w: divider_w = title_w
    else: divider_w = subtitle_w
    draw.rectangle(((50, 50 + line_h + 10), (50 + divider_w, 50 + line_h + 10 + 2)), '#ffffff')
    current_y += 50 + line_h + 10 + 2
    
    # Subtitle
    line = subtitle_tmp
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 10), line, '#ffffff', font=font)
    current_y += 50 + line_h

    # List
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    max_len = 0
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    for item in lst_constituents:
        line_w = font.getbbox(item)[2]
        if max_len < line_w: max_len = line_w
    # print(max_len)
    if max_len > 450:
        font_size = 20
        line_spacing = 1.5
    elif max_len > 500:
        font_size = 18
        line_spacing = 1.7
    else:
        line_spacing = 1.3
    

    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_h = font.getbbox('y')[3]
    for i, line in enumerate(lst_constituents):
        line = line.split('(')[0]
        draw.text((50, current_y + 10 + line_h * line_spacing * i), line, '#ffffff', font=font)
    current_y += 10 + line_h * line_spacing * i + line_h

    # Copy
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    draw.text((50, img_h - 50 - line_h), '© TerraWhisper.com', '#ffffff', font=font)

    img.thumbnail((768, 576), Image.Resampling.LANCZOS)
    
    # Export
    out_attr_lst = '-'.join(attribute_lst).lower().replace(' ', '-')
    out_filename = f'website/images/{entity}-{out_attr_lst}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = '/' + '/'.join(out_filename.split('/')[1:])

    return filepath


def img_resize_2(img):
    w, h = 768, 578

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    return img


def generate_featured_image_2(entity, common_name, attribute_lst, filename):
    img = Image.open(f'{image_folder}/{entity}/4x3/{filename}')
    img = img_resize_2(img)

    w_banner = img.size[0]
    y_banner = img.size[1] // 2
    base = Image.new('RGBA', (w_banner, y_banner), (0, 0, 0, 0))
    top = Image.new('RGBA', (w_banner, y_banner), (0, 0, 0, 255))
    mask = Image.new('L', (w_banner, y_banner))
    mask_data = []
    for y in range(y_banner):
        mask_data.extend([int(255 * (y / y_banner))] * w_banner)
    mask.putdata(mask_data)
    y_img = img.size[1]
    base.paste(top, (0, 0), mask)
    img.paste(base, (0, y_img - y_banner), base)

    attributes = ' '.join(attribute_lst).title()
    if attributes != '': attributes += ' '
    line = f'{common_name.title()}\'s {attributes}Overview'
    draw = ImageDraw.Draw(img)
    font_size = 36
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox('y')[3]
    draw.text((w_banner//2 - line_w//2, y_img - line_h - 30), line, '#ffffff', font=font)

    attributes = '-'.join(attribute_lst)
    if attributes != '': attributes += '-'
    featured_image_filpath = f'website/images/{entity}-{attributes}overview.jpg'
    img.save(f'{featured_image_filpath}', format='JPEG', subsampling=0, quality=100)
    featured_image_filpath = f'/images/{entity}-{attributes}overview.jpg'

    return featured_image_filpath


def generate_image_template_3(entity, common_name, image_filepath, attribute, table_filepath):
    rows = utils.csv_get_rows_by_entity(table_filepath, entity)
    rows = [f'- {x[1].title()}' for x in rows]
    rows = rows[:10]

    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    img_background = Image.open(image_filepath)
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    current_y = 0

    # Title
    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.title()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)

    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    title_tmp = common_name.title()
    title_w = font.getbbox(title_tmp)[2]

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    subtitle_tmp = ''
    if attribute == 'medicine': subtitle_tmp = 'Medicinal Uses'
    elif attribute == 'cuisine': subtitle_tmp = 'Culinary Uses'
    elif attribute == 'horticulture': subtitle_tmp = 'Horticultural Tips'
    elif attribute == 'botany': subtitle_tmp = 'Botanical Profile'
    elif attribute == 'history': subtitle_tmp = 'Historical Uses'
    subtitle_tmp = subtitle_tmp.split('(')[0]
    subtitle_w = font.getbbox(subtitle_tmp)[2]
    if subtitle_w > 475:
        character_len = len(subtitle_tmp)
        font_size = 800 // character_len
        font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
        subtitle_w = font.getbbox(subtitle_tmp)[2]

    if title_w > subtitle_w: divider_w = title_w
    else: divider_w = subtitle_w
    draw.rectangle(((50, 50 + line_h + 10), (50 + divider_w, 50 + line_h + 10 + 2)), '#ffffff')
    current_y += 50 + line_h + 10 + 2
    
    # Subtitle
    line = subtitle_tmp
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 10), line, '#ffffff', font=font)
    current_y += 50 + line_h


    # List
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    max_len = 0
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    for item in rows:
        line_w = font.getbbox(item)[2]
        if max_len < line_w: max_len = line_w
    # print(max_len)
    if max_len > 450:
        font_size = 20
        line_spacing = 1.5
    elif max_len > 500:
        font_size = 18
        line_spacing = 1.7
    else:
        line_spacing = 1.3
    

    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_h = font.getbbox('y')[3]
    for i, line in enumerate(rows):
        line = line.split('(')[0]
        draw.text((50, current_y + 10 + line_h * line_spacing * i), line, '#ffffff', font=font)
    current_y += 10 + line_h * line_spacing * i + line_h

    # Copy
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    draw.text((50, img_h - 50 - line_h), 'TerraWhisper.com', '#ffffff', font=font)

    img.thumbnail((768, 576), Image.Resampling.LANCZOS)

    # Export
    out_filename = f'website/images/{entity}-{attribute}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = f'images/{entity}-{attribute}.jpg'

    return filepath


def generate_image_template_4(entity, common_name, image_filepath, attribute, subtitle, rows):
    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    img_background = Image.open(image_filepath)
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    current_y = 0

    # Title
    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.title()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)

    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    title_tmp = common_name.title()
    title_w = font.getbbox(title_tmp)[2]

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    subtitle_tmp = subtitle
    subtitle_tmp = subtitle_tmp.split('(')[0]
    subtitle_w = font.getbbox(subtitle_tmp)[2]
    if subtitle_w > 475:
        character_len = len(subtitle_tmp)
        font_size = 800 // character_len
        font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
        subtitle_w = font.getbbox(subtitle_tmp)[2]

    if title_w > subtitle_w: divider_w = title_w
    else: divider_w = subtitle_w
    draw.rectangle(((50, 50 + line_h + 10), (50 + divider_w, 50 + line_h + 10 + 2)), '#ffffff')
    current_y += 50 + line_h + 10 + 2
    
    # Subtitle
    line = subtitle_tmp
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 10), line, '#ffffff', font=font)
    current_y += 50 + line_h


    # List
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    max_len = 0
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    for item in rows:
        line_w = font.getbbox(item)[2]
        if max_len < line_w: max_len = line_w
    # print(max_len)
    if max_len > 450:
        font_size = 20
        line_spacing = 1.5
    elif max_len > 500:
        font_size = 18
        line_spacing = 1.7
    else:
        line_spacing = 1.3
    

    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_h = font.getbbox('y')[3]
    for i, line in enumerate(rows):
        line = line.split('(')[0]
        draw.text((50, current_y + 10 + line_h * line_spacing * i), line, '#ffffff', font=font)
    current_y += 10 + line_h * line_spacing * i + line_h

    # Copy
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    draw.text((50, img_h - 50 - line_h), 'TerraWhisper.com', '#ffffff', font=font)

    img.thumbnail((768, 576), Image.Resampling.LANCZOS)

    # Export
    attribute = attribute.lower().replace(' ', '-')
    out_filename = f'website/images/{entity}-{attribute}.jpg'
    img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    filepath = f'images/{entity}-{attribute}.jpg'

    return filepath





######################################################################
# HTML 
######################################################################

def generate_header_light():
    html = '''
        <section class="header-divider">
            <div class="container-lg">
                <header>
                    <a class="text-stone-700" href="/">TerraWhisper</a>
                    <nav>
                        <a class="text-stone-700" href="/plants.html">All Plants</a>
                    </nav>
                </header>
            </div>
        </section>
    '''
    return html
    

def generate_header_transparent():
    html = '''
    <header>
        <nav class="flex justify-between">
            <a class="fg-white" href="/">TerraWhisper</a>
            <a href="#"></a>
        </nav>
    </header>
    '''
    return html


def generate_toc(content_html):
    table_of_contents_html = ''

    headers = []
    content_html_with_ids = ''
    current_id = 0
    for line in content_html.split('\n'):
        if '<h2>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h2>', f'<h2 id="{current_id}">'))
            current_id +=1
        elif '<h3>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h3>', f'<h3 id="{current_id}">'))
            current_id +=1
        elif '<h4>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h4>', f'<h4 id="{current_id}">'))
            current_id +=1
        elif '<h5>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h5>', f'<h5 id="{current_id}">'))
            current_id +=1
        elif '<h6>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h6>', f'<h6 id="{current_id}">'))
            current_id +=1
        else:
            content_html_with_ids += (line)
        content_html_with_ids += '\n'

    # generate table
    toc_li = []

    table_of_contents_html += '<div class="toc">'
    table_of_contents_html += '<span class="toc-title">Table of Contents</span>'
    table_of_contents_html += '<ul>'
    
    last_header = '<h2>'
    for i, line in enumerate(headers):
        insert_open_ul = False
        insert_close_ul = False

        if '<h2>' in line: 
            if last_header != '<h2>': 
                if int('<h2>'[2]) > int(last_header[2]): insert_open_ul = True
                else: insert_close_ul = True
            last_header = '<h2>'
            line = line.replace('<h2>', '').replace('</h2>', '')

        elif '<h3>' in line:
            if last_header != '<h3>':
                if int('<h3>'[2]) > int(last_header[2]): insert_open_ul = True
                else: insert_close_ul = True

            last_header = '<h3>'
            line = line.replace('<h3>', '').replace('</h3>', '')

        if insert_open_ul: table_of_contents_html += f'<ul>'
        if insert_close_ul: table_of_contents_html += f'</ul>'
        table_of_contents_html += f'<li><a href="#{i}">{line}</a></li>'

    table_of_contents_html += '</ul>'
    table_of_contents_html += '</div>'

    # insert table in article
    content_html_formatted = ''

    toc_inserted = False
    for line in content_html_with_ids.split('\n'):
        if not toc_inserted:
            if '<h2' in line:
                toc_inserted = True
                content_html_formatted += table_of_contents_html
                content_html_formatted += line
                continue
        content_html_formatted += line

    return content_html_formatted


def generate_breadcrumbs(filepath_chunks):
    # breadcrumbs = [f for f in filepath_chunks[:-1]]
    breadcrumbs = filepath_chunks
    
    breadcrumbs_hrefs = []
    total_path = ''
    for b in breadcrumbs:
        total_path += b + '/'
        breadcrumbs_hrefs.append('/' + total_path[:-1].lower() + '.html')

    breadcrumbs_text = total_path.split('/')

    breadcrumbs_lst = []
    for i in range(len(breadcrumbs_hrefs)):
        html = f'<a href="{breadcrumbs_hrefs[i]}">{breadcrumbs_text[i].capitalize().replace("-", " ")}</a>'
        breadcrumbs_lst.append(html)

    # breadcrumbs_html_formatted = [f' > {f}' for f in breadcrumbs_html]

    return breadcrumbs_lst


def generate_html(date, title, article, entity, attribute_lst):
    attributes = '/'.join(attribute_lst)

    if attributes != '':
        article_filepath = f'{entity}/{attributes}.md'
    else:
        article_filepath = f'{entity}.md'

    with open(f'articles/{article_filepath}', 'w', encoding='utf-8') as f:
        f.write(article)


    article_html = markdown.markdown(article, extensions=['markdown.extensions.tables'])

    # breadcrumbs --------------------------------------------------------
    attributes_breadcrumbs = [x.replace(' ', '-').lower().strip() for x in attribute_lst]
    attributes_breadcrumbs.insert(0, entity)
    breadcrumbs_lst = generate_breadcrumbs(attributes_breadcrumbs)[:-1]
    breadcrumbs_lst.insert(0, f'<a href="/">Home</a>')
    breadcrumbs_lst.append(f'<span>{attributes_breadcrumbs[-1].title().replace("-", " ")}</span>')

    breadcrumbs_html = ' > '.join(breadcrumbs_lst)

    article_html = generate_toc(article_html)
    
    word_count = len(article.split(' '))
    reading_time_html = str(word_count // 200) + ' minutes'

    header = generate_header_light()

    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="Martin Pellizzer">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>{title}</title>
            {google_tag}
            
        </head>

        <body>
            {header}
            
            <section class="py-16">
                <div class="container-lg">
                    {breadcrumbs_html}
                </div>
            </section>

            <section class="my-96">
                <div class="container">
                    <div class="flex justify-between mb-16">
                        <span>by Martin Pellizzer - <time datetime="{date.replace("/", "-")}">{date}</time></span>
                        <span>{reading_time_html}</span>
                    </div>
                    {article_html}
                </div>
            </section>

            <footer>
                <div class="container-lg">
                    <span>© TerraWhisper.com 2023 | All Rights Reserved
                </div>
            </footer>
        </body>

        </html>
    '''

    if len(attributes) != 0: path = '/'.join([entity, attributes])
    else: path = entity
    article_filepath = f'{path}.html'
    
    with open(f'website/{article_filepath}', 'w', encoding='utf-8') as f:
        f.write(html)

    return article_filepath




######################################################################
# FOLDERS
######################################################################

articles_folder = 'database/articles/'
articles_files = [x for x in os.listdir(articles_folder) if x.endswith('.json')]

try: shutil.rmtree('articles')
except: pass
# try: shutil.rmtree('website')
# except: pass

try: os.mkdir(f'articles')
except: pass
# try: os.mkdir(f'website')
# except: pass

chunks = website_img_path.split('/')
curr_chunk = ''
for chunk in chunks:
    curr_chunk += chunk + '/'
    try: os.mkdir(curr_chunk)
    except: pass



######################################################################
# MAIN
######################################################################

shutil.copy2('style.css', 'website/style.css')
shutil.copy2('index.html', 'website/index.html')
# shutil.copy2('articles-images/hero.jpg', f'{website_img_path}/hero.jpg')
# shutil.copy2('articles-images/medicinal-plants.jpg', f'{website_img_path}/medicinal-plants.jpg')
shutil.copy2('images/medicinal-plants.jpg', f'{website_img_path}/medicinal-plants.jpg')



articles_home = []

articles_master_rows = utils.csv_to_llst(ARTICLES_CSV)

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
    update = row[articles_dict['update']].strip()
    latin_name = entity.replace('-', ' ').capitalize()

    if not REGEN_ALL_FORCED:
        if update.strip() == '': continue

    if entity_arg:
        if entity_arg.strip() != entity:
            continue

    if state != 'published': continue

    try:
        common_names = utils.csv_get_rows_by_entity('plants.csv', entity)
        common_name = common_names[0][1].lower().strip()
    except:
        common_names = []
        common_name = ''

    try: os.mkdir(f'articles/{entity}')
    except: pass
    try: os.mkdir(f'articles/{entity}/{attribute_1}')
    except: pass
    try: os.mkdir(f'articles/{entity}/{attribute_1}/{attribute_2}')
    except: pass
    try: os.mkdir(f'website/{entity}')
    except: pass
    try: os.mkdir(f'website/{entity}/{attribute_1}')
    except: pass
    try: os.mkdir(f'website/{entity}/{attribute_1}/{attribute_2}')
    except: pass

    article = ''
    featured_image_filpath = ''

    # root
    if attribute_1.strip() == '':
        # intro
        title = f'What to know before using {common_name} ({latin_name.capitalize()})'.title()
        article += f'<h1>{title}</h1>'
        
        attribute_lst = []
        try:
            image_title = f'{latin_name.title()} Overview'
            featured_image_filepath = generate_featured_image_2(entity, common_name, attribute_lst, '0000.jpg')
            article += f'![{image_title}]({featured_image_filepath} "{image_title}")\n\n'
        except: pass

        with open(f'database/articles/{entity}/intro.md', encoding='utf-8') as f: 
            content = f.read()

        article += f'{content}\n\n'
        article += f'In this article, you will discover what are the medicinal and culinary uses of {common_name}. Then, you\'ll learn how to cultivate it, what is its botanical profile, and how it was used historically.\n\n'

        images_filenames = os.listdir(f'{image_folder}/{entity}/3x4')
        random.shuffle(images_filenames)

        # ----------------------------------
        section = 'medicine'
        with open(f'database/articles/{entity}/{section}.md', encoding='utf-8') as f: content = f.read()
        content_paragraphs = content.split('\n')
        content_paragraphs = [x for x in content_paragraphs if x.strip() != '']
        
        paragraph_1 = content_paragraphs[0]
        paragraph_rest = content_paragraphs[1:]

        image_filename = images_filenames.pop()
        try:
            filepath = generate_image_template_3(
                entity, 
                common_name, 
                f'{image_folder}/{entity}/3x4/{image_filename}', 
                f'{section}', 
                f'database/tables/{section}.csv'
            )
        except:
            print(f'Missing Image: {entity} {section}') 
            filepath = ''

        section_title = f'What are the medicinal uses of {common_name}?'

        try:
            with open(f'database/articles/{entity}/medicine/_intro.md') as f: intro_content = f.read()
        except: intro_content = ''
        if intro_content.strip() != '': image_intro = f'The following illustration lists the most important uses of <a href="/{entity}/medicine.html">{common_name} in medicine</a>.'
        else: image_intro = f'The following illustration lists the most important uses of {common_name} in medicine.'
        
        article += f'<h2>{section_title.title()}</h2>'
        article += f'<p>{paragraph_1}</p>'
        article += f'<p>{image_intro}</p>'
        article += f'<img src="images/{entity}-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        for paragraph in paragraph_rest:
            article += f'<p>{paragraph}</p>'
            
        # ----------------------------------
        section = 'cuisine'
        with open(f'database/articles/{entity}/{section}.md', encoding='utf-8') as f: content = f.read()
        content_paragraphs = content.split('\n')
        content_paragraphs = [x for x in content_paragraphs if x.strip() != '']
        
        paragraph_1 = content_paragraphs[0]
        paragraph_rest = content_paragraphs[1:]

        image_filename = images_filenames.pop()
        try: filepath = generate_image_template_3(
            entity, 
            common_name, 
            f'{image_folder}/{entity}/3x4/{image_filename}', 
            f'{section}', 
            f'database/tables/{section}.csv'
        )
        except:
            print(f'Missing Image: {entity} {section}') 
            filepath = ''

        section_title = f'What are the culinary uses of {common_name}?'
        image_intro = f'The following illustration lists the most common uses of {common_name} for culinary purposes.'
        
        article += f'<h2>{section_title.title()}</h2>'
        article += f'<p>{paragraph_1}</p>'
        article += f'<p>{image_intro}</p>'
        article += f'<img src="images/{entity}-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        for paragraph in paragraph_rest:
            article += f'<p>{paragraph}</p>'
            
        # ----------------------------------
        section = 'horticulture'
        with open(f'database/articles/{entity}/{section}.md', encoding='utf-8') as f: content = f.read()
        content_paragraphs = content.split('\n')
        content_paragraphs = [x for x in content_paragraphs if x.strip() != '']
        
        paragraph_1 = content_paragraphs[0]
        paragraph_rest = content_paragraphs[1:]

        image_filename = images_filenames.pop()
        try: filepath = generate_image_template_3(
            entity, 
            common_name, 
            f'{image_folder}/{entity}/3x4/{image_filename}', 
            f'{section}', 
            f'database/tables/{section}.csv'
        )
        except:
            print(f'Missing Image: {entity} {section}') 
            filepath = ''

        section_title = f'How to cultivate {common_name} in your garden?'
        image_intro = f'The following illustration lists the most important tips to cutlitvate {common_name}.'
        
        article += f'<h2>{section_title.title()}</h2>'
        article += f'<p>{paragraph_1}</p>'
        article += f'<p>{image_intro}</p>'
        article += f'<img src="images/{entity}-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        for paragraph in paragraph_rest:
            article += f'<p>{paragraph}</p>'
            
        # ----------------------------------
        section = 'botany'
        with open(f'database/articles/{entity}/{section}.md', encoding='utf-8') as f: content = f.read()
        content_paragraphs = content.split('\n')
        content_paragraphs = [x for x in content_paragraphs if x.strip() != '']
        
        paragraph_1 = content_paragraphs[0]
        paragraph_rest = content_paragraphs[1:]

        taxonomy_rows = utils.csv_get_rows_by_entity(f'database/tables/botany/taxonomy.csv', entity)[0]
        taxonomy_rows[0] = f'Entity: {taxonomy_rows[0].capitalize()}'
        taxonomy_rows[1] = f'Domain: {taxonomy_rows[1].capitalize()}'
        taxonomy_rows[2] = f'Kingdom: {taxonomy_rows[2].capitalize()}'
        taxonomy_rows[3] = f'Phylum: {taxonomy_rows[3].capitalize()}'
        taxonomy_rows[4] = f'Class: {taxonomy_rows[4].capitalize()}'
        taxonomy_rows[5] = f'Order: {taxonomy_rows[5].capitalize()}'
        taxonomy_rows[6] = f'Family: {taxonomy_rows[6].capitalize()}'
        taxonomy_rows[7] = f'Genus: {taxonomy_rows[7].capitalize()}'
        taxonomy_rows[8] = f'Species: {taxonomy_rows[8]}'

        image_filename = images_filenames.pop()
        try: filepath = generate_image_template_4(
            entity, 
            common_name, 
            f'{image_folder}/{entity}/3x4/{image_filename}', 
            f'{section}', 
            'Taxonomy', 
            taxonomy_rows[1:],
        )
        except:
            print(f'Missing Image: {entity} {section}') 
            filepath = ''

        section_title = f'What is the botanical profile of {common_name}?'
        image_intro = f'The following illustration display the botanical profile of {common_name}.'
        
        article += f'<h2>{section_title.title()}</h2>'
        article += f'<p>{paragraph_1}</p>'
        article += f'<p>{image_intro}</p>'
        article += f'<img src="images/{entity}-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        for paragraph in paragraph_rest:
            article += f'<p>{paragraph}</p>'
            
        # ----------------------------------
        section = 'history'
        with open(f'database/articles/{entity}/{section}.md', encoding='utf-8') as f: content = f.read()
        content_paragraphs = content.split('\n')
        content_paragraphs = [x for x in content_paragraphs if x.strip() != '']
        
        paragraph_1 = content_paragraphs[0]
        paragraph_rest = content_paragraphs[1:]

        image_filename = images_filenames.pop()
        try: filepath = generate_image_template_3(
            entity, 
            common_name, 
            f'{image_folder}/{entity}/3x4/{image_filename}', 
            f'{section}', 
            f'database/tables/{section}.csv'
        )
        except:
            print(f'Missing Image: {entity} {section}') 
            filepath = ''

        section_title = f'What are the historical uses of {common_name}?'
        image_intro = f'The following illustration lists the most well known historical uses of {common_name}.'
        
        article += f'<h2>{section_title.title()}</h2>'
        article += f'<p>{paragraph_1}</p>'
        article += f'<p>{image_intro}</p>'
        article += f'<img src="images/{entity}-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        for paragraph in paragraph_rest:
            article += f'<p>{paragraph}</p>'
  
    # medicine
    elif 'medicine' in attribute_1.lower() and attribute_2.strip() == '':
        title = f'{common_name.capitalize()} ({latin_name.capitalize()}) Medicinal Guide: Benefits, Constituents, and Preparations'
        article += f'# {title}\n\n'

        attribute_lst = ['medicine', 'overview']
        image_title = f'{common_name.capitalize()} Medicinal Guide'
        image_filepath = generate_featured_image(entity, attribute_lst, image_title)
        try:
            article += f'![{image_title}]({image_filepath} "{image_title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article += get_content('medicine/_intro', f'database/articles/{entity}')
        article += f'This article explains in details the medicinal properties of {common_name} and how to use this plant to boost your health.' + '\n\n'



        # benefits
        title_section = f'## What are the health benefits and medicinal properties of {common_name}?\n\n'

        content_paragraphs = get_content('medicine/benefits', f'database/articles/{entity}').strip().split('\n')

        tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']].strip() == entity]
        tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'benefits']
        if tmp_rows: image_intro = f'\n\nThe following illustration shows the most important [health benefits of {common_name}](/{entity}/{attribute_1.lower()}/benefits.html).\n\n'
        else: image_intro = f'\n\nThe following illustration shows the most important health benefits of {common_name}.\n\n'

        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]

        image_title = f'{latin_name.capitalize()} Medicinal Benefits'
        image_filepath = generate_image_template_1(
            entity, 
            ['medicine', 'benefits'], 
            rows_filtered,
        )

        lst_intro = f'The following list summarizes the 10 most important health benefits of {common_name}.\n\n'
        lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
        lst_formatted = lst_to_blt(bold_blt(lst_filtered))

        article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'



        # constituents
        title_section = f'## What are the key constituents of {common_name} for health purposes?\n\n'
        
        content_paragraphs = get_content('medicine/constituents', f'database/articles/{entity}').strip().split('\n')

        tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
        tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'constituents']
        if tmp_rows: image_intro = f'\n\nThe following illustration shows the most important [active constituents of {common_name}](/{entity}/{attribute_1.lower()}/constituents.html) for medicinal purposes.\n\n'
        else: image_intro = f'\n\nThe following illustration shows the most important active constituents of {common_name} for medicinal purposes.\n\n'

        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/constituents.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]

        image_title = f'{latin_name.capitalize()} Medicinal Constituents'
        image_filepath = generate_image_template_1(
            entity, 
            ['medicine', 'constituents'], 
            rows_filtered,
        )

        lst_intro = f'The following list summarizes the 10 most important active constituents of {common_name} for medicinal purposes.\n\n'
        lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
        lst_formatted = lst_to_blt(bold_blt(lst_filtered))
        
        article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'



        # preparations
        title_section = f'## What are the medicinal preparations of {common_name} for health purposes?\n\n'
        
        content_paragraphs = get_content('medicine/preparations', f'database/articles/{entity}').strip().split('\n')

        tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
        tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'preparations']
        if tmp_rows: image_intro = f'\n\nThe following illustration shows the most important [medicinal preparations of {common_name}](/{entity}/{attribute_1.lower()}/preparations.html).\n\n'
        else: image_intro = f'\n\nThe following illustration shows the most important medicinal preparations of {common_name}.\n\n'

        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/preparations.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]

        image_title = f'{latin_name.capitalize()} Medicinal Preparations'
        image_filepath = generate_image_template_1(
            entity, 
            ['medicine', 'preparations'], 
            rows_filtered,
        )

        lst_intro = f'The following list summarizes the 10 most important preparations of {common_name} to boost your health.\n\n'
        lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
        lst_formatted = lst_to_blt(bold_blt(lst_filtered))
        
        article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'


        # side-effects
        
        try:
            title_section = f'## What are the possible health side effects of {common_name}?\n\n'
            content_paragraphs = get_content('medicine/side-effects', f'database/articles/{entity}').strip().split('\n')

            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'side-effects']
            if tmp_rows: image_intro = f'\n\nThe following illustration shows some possible [health side effects of {common_name}](/{entity}/{attribute_1.lower()}/side-effects.html).\n\n'
            else: image_intro = f'\n\nThe following illustration shows some possible health side effects of {common_name}.\n\n'

            rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/side-effects.csv', entity)
            rows_filtered = [f'{x[1]}' for x in rows[:10]]

            image_title = f'{latin_name.capitalize()} Health Side Effects'
            image_filepath = generate_image_template_1(
                entity, 
                ['medicine', 'side-effects'], 
                rows_filtered,
            )

            lst_intro = f'The following list summarizes the 10 most common health side effects of {common_name} if misused.\n\n'
            lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
            lst_formatted = lst_to_blt(bold_blt(lst_filtered))
            
            article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'


            # precautions
            title_section = f'## What precautions should you take when using {common_name} as a medicine?\n\n'
            
            content_paragraphs = get_content('medicine/precautions', f'database/articles/{entity}').strip().split('\n')

            image_intro = f'\n\nThe following illustration shows the most important precautions you must take when you use {common_name} as a medicine.\n\n'

            rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/precautions.csv', entity)
            rows_filtered = [f'{x[1]}' for x in rows[:10]]

            image_title = f'{latin_name.capitalize()} Medicinal Precautions'
            image_filepath = generate_image_template_1(
                entity, 
                ['medicine', 'precautions'], 
                rows_filtered,
            )

            lst_intro = f'The following list summarizes the 10 most important precautions you must take when you use {common_name} as a medicine.\n\n'
            lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
            lst_formatted = lst_to_blt(bold_blt(lst_filtered))
            
            article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'
        except:
            pass

    # medicine >> benefits
    elif 'medicine' in attribute_1.lower() and attribute_2.strip() == 'benefits':
        title = f'10 Health Benefits of {common_name.capitalize()} ({latin_name.capitalize()})'
        article += f'# {title}\n\n'

        attribute_lst = ['medicine', 'benefits']
        try:
            image_title = f'{common_name.capitalize()}\'s Medicinal Benefits'
            featured_image_filepath = generate_featured_image_2(
                entity, 
                common_name, 
                attribute_lst, 
                '0001.jpg'
            )
            article += f'![{image_title}]({featured_image_filepath} "{image_title}")\n\n'
        except: 
            pass

        # image_filepath = generate_featured_image(entity, attribute_lst, image_title)

        article += get_content('medicine/benefits/_intro', f'database/articles/{entity}')
        article += f'This article explains in details the most important and well recognized health benefits of {common_name}, including what constituents are responsible for those benefits and what health condititions they can help.' + '\n\n'

        benefits_rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        benefits = [f'{x[1]}' for x in benefits_rows]

        images_filenames = os.listdir(f'{image_folder}/{entity}/3x4')
        random.shuffle(images_filenames)

        for img_num, benefit in enumerate(benefits):
            data_title = f'## {img_num+1}. {benefit}'
            data_definition = ''
            
            benefits_rows = utils.csv_get_rows_by_entity(f'database/articles/{entity}/medicine/benefits/definitions.csv', entity)
            for benefit_row in benefits_rows:
                if benefit_row[1] == benefit:
                    data_definition = benefit_row[2]
                    
            _rows = utils.csv_get_rows_by_entity(f'database/articles/{entity}/medicine/benefits/constituents_list.csv', entity)
            data_constituents_lst = [] 
            for _row in _rows:
                if _row[1] == benefit:
                    data_constituents_lst.append(_row[2])
                    
            _rows = utils.csv_get_rows_by_entity(f'database/articles/{entity}/medicine/benefits/constituents_text.csv', entity)
            data_constituents_text = ''
            for _row in _rows:
                if _row[1] == benefit:
                    data_constituents_text = _row[2]
                    
            _rows = utils.csv_get_rows_by_entity(f'database/articles/{entity}/medicine/benefits/conditions_list.csv', entity)
            data_conditions_lst = [] 
            for _row in _rows:
                if _row[1] == benefit:
                    data_conditions_lst.append(_row[2])
                    
            _rows = utils.csv_get_rows_by_entity(f'database/articles/{entity}/medicine/benefits/conditions_text.csv', entity)
            data_conditions_text = ''
            for _row in _rows:
                if _row[1] == benefit:
                    data_conditions_text = _row[2]

            _rows = utils.csv_get_rows_by_entity(f'database/articles/{entity}/medicine/benefits/conditions_list.csv', entity)
            data_conditions_lst = [] 
            for _row in _rows:
                if _row[1] == benefit:
                    data_conditions_lst.append(_row[2].title())

            image_filename = images_filenames.pop()
            try: 
                filepath = generate_image_template_4(
                entity, 
                common_name, 
                f'{image_folder}/{entity}/3x4/{image_filename}', 
                f'{benefit}', 
                benefit, 
                data_conditions_lst,)
            except:
                print(f'Missing Image: {entity} {benefit}') 
                filepath = ''

            # print(filepath)
            
            image_title = f'{common_name.title()} {item.title()}'
            image_section = f'![{image_title}](/{filepath} "{image_title}")'
                    

            article += data_title + '\n\n'
            article += data_definition + '\n\n'
            
            article += f'The following list includes the main medicinal constituents that give {latin_name} this benefit.' + '\n\n'
            article += lst_to_blt(data_constituents_lst) + '\n\n'
            article += data_constituents_text + '\n\n'
            
            article += f'The illustration below shows some common health conditions that benefits from the fact that {common_name} {benefit.lower()}.' + '\n\n'
            article += image_section + '\n\n'
            article += data_conditions_text + '\n\n'
            # article += lst_to_blt(data_conditions_lst) + '\n\n'
            

        






















    # medicine >> constituents
    elif 'medicine' in attribute_1.lower() and 'constituents' in attribute_2.strip():
        title = f'10 Active Constituents of {common_name.capitalize()} ({latin_name.capitalize()}): Dosage, Benefits, and Side Effects'
        article += f'# {title}\n\n'

        attribute_lst = ['medicine', 'constituents', 'overview']
        image_title = f'{common_name.capitalize()}\'s Active Constituents'
        image_filepath = generate_featured_image(entity, attribute_lst, image_title)
        try:
            article += f'![{image_title}]({image_filepath} "{image_title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article += get_content('medicine/constituents/_intro', f'database/articles/{entity}')
        article += f'This article lists the key constituents of {common_name} and how what are their positive and negative effect on health.' + '\n\n'



        # constituents
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/constituents.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]
        images_filenames = os.listdir(f'{image_folder_old}/{entity}/medicine/constituents')
        for i, item in enumerate(rows_filtered):
            if i < 10: num = f'0{i}'
            else: num = f'{i}'

            title_section = f'## {i+1}. {item.title()}\n\n'
            item_formatted = item.replace(' ', '-').lower()
            filename = f'{num}-{item_formatted}'
            filepath = f'medicine/constituents/{filename}'

            content_section = get_content(f'{filepath}', f'database/articles/{entity}').strip()

            # image            
            image_filepath = generate_image_template_2(entity, common_name, images_filenames[i], 
                ['medicine', 'constituents', item], 'constituents',
            )
            image_title = f'{item.title()}'
            image_section = f'![{image_title}]({image_filepath} "{image_title}")\n\n'

            item_words = item.split(' ')
            item_no_s = item_words[0][:-1] + ' ' + ' '.join(item_words[1:])
            image_intro_line = f'The following illustration show a list of the health benefits of {item}.'  + '\n\n'

            section_1 = content_section.split('\n')[0]  + '\n\n'
            section_rest = '\n'.join(content_section.split('\n')[1:])  + '\n\n'

            article += title_section + section_1 + image_intro_line + image_section + section_rest
            
        content = get_content_2(f'database/articles/{entity}/medicine/constituents/parts.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What parts of {common_name} have the highest concentration of biochemical compounds?' + '\n\n'
            article += content + '\n\n'

        content = get_content_2(f'database/articles/{entity}/medicine/constituents/preparations.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What medicinal preparations of {common_name} have the most constituents?' + '\n\n'
            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'preparations']
            if tmp_rows: content = content.replace(f'medicinal preparations of {common_name.title()}', f'[medicinal preparations of {common_name.title()}](/{entity}/{attribute_1.lower()}/preparations.html)')
            article += content + '\n\n'
            
        content = get_content_2(f'database/articles/{entity}/medicine/constituents/benefits.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What are the most important health benefits {common_name}\'s constituents can give you?' + '\n\n'
            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'benefits']
            if tmp_rows: content = content.replace(f'{common_name.title()}\'s constituents bring many health benefits', f'[{common_name.title()}\'s constituents bring many health benefits](/{entity}/{attribute_1.lower()}/benefits.html)')
            article += content + '\n\n'
            
        content = get_content_2(f'database/articles/{entity}/medicine/constituents/side-effects.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What are the possible side effects of an overdose of {common_name}\'s active compounds?' + '\n\n'
            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'benefits']
            if tmp_rows: content = content.replace(f'Overdosing {common_name.title()}\'s constituents may cause side effects', f'[Overdosing {common_name.title()}\'s constituents may cause side effects](/{entity}/{attribute_1.lower()}/benefits.html)')
            article += content + '\n\n'
            

    # medicine >> preparations
    elif 'medicine' in attribute_1.lower() and 'preparations' in attribute_2.strip():
        title = f'10 Medicinal Preparations of {common_name.capitalize()} ({latin_name.capitalize()}) and Their Uses to Promote Health'
        article += f'# {title}\n\n'

        attribute_lst = ['medicine', 'preparations', 'overview']
        image_title = f'{common_name.capitalize()}\'s Medicinal Preparations'
        image_filepath = generate_featured_image(entity, attribute_lst, image_title)
        try:
            article += f'![{image_title}]({image_filepath} "{image_title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article += get_content('medicine/preparations/_intro', f'database/articles/{entity}')
        article += f'This article lists the medicinal preparations of {common_name} and how to use them to achieve health benefits without experiencing side-effects.' + '\n\n'



        # preparations
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/preparations.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]
        images_filenames = os.listdir(f'{image_folder_old}/{entity}/medicine/preparations')
        for i, item in enumerate(rows_filtered):
            if i < 10: num = f'0{i}'
            else: num = f'{i}'

            title_section = f'## {i+1}. {item.title()}\n\n'
            item_formatted = item.replace(' ', '-').lower()
            filename = f'{num}-{item_formatted}'
            filepath = f'medicine/preparations/{filename}'

            content_section = get_content(f'{filepath}', f'database/articles/{entity}').strip()

            # image            
            image_filepath = generate_image_template_2(entity, common_name, images_filenames[i], 
                ['medicine', 'preparations', item], 'preparations',
            )
            image_title = f'{item.title()}'
            image_section = f'![{image_title}]({image_filepath} "{image_title}")\n\n'

            item_words = item.split(' ')
            item_no_s = item_words[0][:-1] + ' ' + ' '.join(item_words[1:])
            image_intro_line = f'The following illustration give a quick overview about the health benefits of {item}, how to prepare it and what precautions to take.'  + '\n\n'

            section_1 = content_section.split('\n')[0]  + '\n\n'
            section_rest = '\n'.join(content_section.split('\n')[1:])  + '\n\n'

            article += title_section + section_1 + image_intro_line + image_section + section_rest

        content = get_content_2(f'database/articles/{entity}/medicine/preparations/combination.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What combination of {common_name} medicinal preparations work the best for general health?' + '\n\n'
            article += content + '\n\n'
            
        content = get_content_2(f'database/articles/{entity}/medicine/preparations/safest.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What\'s the safest {common_name} medicinal preparations to use?' + '\n\n'
            article += content + '\n\n'
            
        content = get_content_2(f'database/articles/{entity}/medicine/preparations/most-dangerous.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What can be the most dangerous {common_name} medicinal preparations to use?' + '\n\n'
            article += content + '\n\n'
            
        content = get_content_2(f'database/articles/{entity}/medicine/preparations/animals.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## Can you use {common_name} medicinal preparations on animals?' + '\n\n'
            article += content + '\n\n'


    # medicine >> effects
    elif 'medicine' in attribute_1.lower() and 'side-effects' in attribute_2.strip():
        title = f'10 Possible Health Side Effects of {common_name.capitalize()} ({latin_name.capitalize()}): Reasons, Dosages, and Precautions'
        article += f'# {title}\n\n'

        attribute_lst = ['medicine', 'side-effects', 'overview']
        image_title = f'{common_name.capitalize()}\'s Health Side Effects'
        image_filepath = generate_featured_image(entity, attribute_lst, image_title)
        try:
            article += f'![{image_title}]({image_filepath} "{image_title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article += get_content('medicine/side-effects/_intro', f'database/articles/{entity}')
        article += f'This article lists the possible health side effects of {common_name} and how to avoid them.' + '\n\n'



        # list
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/side-effects.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]
        images_filenames = os.listdir(f'{image_folder_old}/{entity}/medicine/side-effects')
        for i, item in enumerate(rows_filtered):
            if i < 10: num = f'0{i}'
            else: num = f'{i}'

            title_section = f'## {i+1}. {item}\n\n'
            item_formatted = item.replace(' ', '-').lower()
            filename = f'{num}-{item_formatted}'
            filepath = f'medicine/side-effects/{filename}'

            content_section = get_content(f'{filepath}', f'database/articles/{entity}').strip()

            # image            
            image_filepath = generate_image_template_2(entity, common_name, images_filenames[i], 
                ['medicine', 'side-effects', item], 'side-effects',
            )
            image_title = f'{common_name.title()} {item.title()}'
            image_section = f'![{image_title}]({image_filepath} "{image_title}")\n\n'

            item_words = item.split(' ')
            item_no_first_word = ' '.join(item_words[1:])
            image_intro_line = f'{common_name.title()}\'s ability to {item_no_first_word.lower()} can aggravate many health conditions, like the ones shown in the illustration below.'  + '\n\n'

            section_1 = content_section.split('\n')[0]  + '\n\n'
            section_rest = '\n'.join(content_section.split('\n')[1:])  + '\n\n'

            article += title_section + section_1 + image_intro_line + image_section + section_rest

        content = get_content_2(f'database/articles/{entity}/medicine/side-effects/benefits.md')
        if content.strip() != '':
            article += f'## What are the benefits of {common_name} if used correctly?' + '\n\n'
            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'benefits']
            if tmp_rows: 
                if f'health benefits of {common_name.lower()}' in content:
                    content = content.replace(f'health benefits of {common_name.lower()}', f'[health benefits of {common_name.lower()}](/{entity}/{attribute_1.lower()}/benefits.html)')
                else:
                    content = content.replace(f'health benefits of {common_name.title()}', f'[health benefits of {common_name.title()}](/{entity}/{attribute_1.lower()}/benefits.html)')
            article += content + '\n\n'
  


  
    elif 'cuisine' in attribute_1.lower() and attribute_2.strip() == '':

        title = f'{common_name} ({latin_name.capitalize()}) Culinary Guide: Uses, Flavor Profile, and Tips'
        article += f'# {title}\n\n'

        attribute_lst = ['cuisine']
        image_title = f'{latin_name.capitalize()} Culinary Guide'
        image_filepath = generate_featured_image(entity, attribute_lst, image_title)
        try:
            article += f'![{image_title}]({image_filepath} "{image_title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article += get_content('cuisine/_intro', f'database/articles/{entity}')



        # uses
        title_section = f'## What are the culinary uses of {common_name}?\n\n'

        content_paragraphs = get_content('cuisine/uses', f'database/articles/{entity}').split('\n')

        image_intro = f'\n\nThe following illustration shows the most common culinary uses of yarrow.\n\n'

        rows = utils.csv_get_rows_by_entity(f'database/tables/cuisine/uses.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]

        image_title = f'{latin_name.capitalize()} Culinary Uses'
        image_filepath = generate_image_template_1(
            entity, 
            ['cuisine', 'uses'], 
            rows_filtered,
        )

        lst_intro = f'The following list summarizes the 10 most common culinary uses of {latin_name}.\n\n'
        lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
        lst_formatted = lst_to_blt(bold_blt(lst_filtered))

        article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'


    elif 'botany' in attribute_1.lower() and attribute_2.strip() == '':
        title = f'{common_name.title()} ({latin_name.capitalize()}) Botanical Profile: Taxonomy, Morphology, and Distribution'
        article += f'# {title}\n\n'
        
        try:
            attribute_lst = ['botany']
            image_title = f'{latin_name.capitalize()} Botany'
            featured_image_filpath = generate_featured_image(entity, attribute_lst, image_title)
            article += f'![{title}]({featured_image_filpath} "{title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article_folderpath = f'database/articles/{entity}/{attribute_1}'
        table_folderpath = f'database/tables/{attribute_1}'



        # try: 
        #     with open(f'{article_folderpath}/_intro.md', encoding='utf-8') as f: section_content = f.read()
        #     article += section_content + '\n\n'
        # except: 
        #     print(f'WARNING: missing intro ({entity}/{attribute_1}/{attribute_2})')

        section = 'taxonomy'
        try: 
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the taxonomy and classification of {latin_name}?'
            article += f'## {title}\n\n'
            article += section_content + '\n\n'
        except: 
            print(f'WARNING: missing {section} text ({filepath})')

        try: 
            filepath = f'{table_folderpath}/{section}.csv'
            lines = csv_get_table_data(f'{filepath}')
            article += generate_table(lines)
        except: 
            print(f'WARNING: missing {section} table ({filepath})')



        section = 'common-names'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What are the common names of {latin_name}?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            rows = csv_get_rows(f'{filepath}')
            article += f'Here\'s a list of the most common names of {latin_name} with a brief description for each name.\n\n'
            rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
            article += lst_to_blt(bold_blt(rows_filtered))
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')



        section = 'varieties'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What are the varieties of {latin_name}?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            rows = csv_get_rows(f'{filepath}')
            article += f'Here\'s a list of the most common varieties of {latin_name} with a brief description for each variety.\n\n'
            rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
            article += lst_to_blt(bold_blt(rows_filtered))
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')

            

        section = 'morphology'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the morphology of {latin_name}?'
            article += f'## {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')



        section = 'distribution'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the geographical distribution of {latin_name}?'
            article += f'## {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            article += f'The following table gives list of continents and the distribution of {latin_name} for each continent.\n\n'
            rows = utils.csv_get_rows_by_entity(f'{filepath}', entity)
            article += generate_table_simple(rows)
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')



        section = 'native'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the native range of {latin_name}?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        
        try:
            filepath = f'{table_folderpath}/{section}.csv'
            article += f'The following table gives a detailed list of continents and states where {latin_name} is native, according to the United States Department of Agriculture (USDA) and other governative resources around the world.\n\n'
            rows = utils.csv_get_rows_by_entity(f'{filepath}', entity)
            article += generate_table_grouped(rows)
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')



        section = 'habitat'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the habitat of {latin_name}?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            rows = csv_get_rows(f'{filepath}')
            article += f'Here\'s a list of the most common habitats of {latin_name} with a brief description for each one.\n\n'
            rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
            article += lst_to_blt(bold_blt(rows_filtered))
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')



        # invasive --------------------------------------------------------------------
        section = 'invasive'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'Is {latin_name} invasive?'
            article += f'## {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            rows = csv_get_rows(f'{filepath}')
            article += f'Here\'s a list of the most common habitats of {latin_name} with a brief description for each one.\n\n'
            rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
            article += lst_to_blt(bold_blt(rows_filtered))
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')



        section = 'invasive-impact'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What\'s the impact of {latin_name} as an invasive species?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')



        section = 'invasive-control'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'How to manage and control invasive {latin_name}?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

            

        # life-cycle --------------------------------------------------------------------
        section = 'life-cycle'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the life cycle of {latin_name}?'
            article += f'## {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            rows = csv_get_rows(f'{filepath}')
            article += f'The following list gives a detailed step-by-step description of the life-cycle of {latin_name}.\n\n'
            rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
            article += lst_to_blt(bold_blt(rows_filtered))
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')
            


        section = 'perennial'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'Is {common_name.lower()} annual or perennial?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')
            

    else:
        if 'morphology' in attribute_2.lower():
            title = f'{latin_name.capitalize()} morphology'
            article += f'# {title}\n\n'

            try:
                attribute_lst = ['botany', 'morphology']
                image_title = f'{latin_name.capitalize()} Morphology'
                featured_image_filpath = generate_featured_image(entity, attribute_lst, image_title)
                article += f'![{title}]({featured_image_filpath} "{title}")\n\n'
            except:
                print(f'WARNING: missing image ({entity})')

            path = f'database/articles/{entity}/botany/morphology'

            with open(f'{path}/_intro.md', encoding='utf-8') as f:  
                section_content = f.read()
            article += section_content + '\n\n'
            
            article += f'In this article you will learn about the morphology of {latin_name} by analyzing the main parts of this plant and their characteristics.' + '\n\n'

            files = ['roots', 'stems', 'leaves', 'flowers', 'fruits', 'seeds']
            for file in files:
                with open(f'{path}/{file}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                
                if section_content.strip() != '':
                    section_title = file.split('.')[0].capitalize()
                    article += f'## {section_title}\n\n'
                    article += '\n\n' + section_content + '\n\n'
                    article += f'The following table shows in detail the morphological characteristics of {latin_name} {file}.\n\n'
                    lines = csv_get_table_data(f'database/tables/morphology/{section_title.lower()}.csv')
                    article += generate_table(lines)

                if file.strip() == 'roots':
                    filepath = img_morphology_roots(lines[1], latin_name, attribute_1, attribute_2, file)
                    article += f'![none]({filepath} "none")\n\n'
                elif file.strip() == 'stems':
                    filepath = img_morphology_stems(lines[1], latin_name, attribute_1, attribute_2, file)
                    article += f'![none]({filepath} "none")\n\n'
                elif file.strip() == 'leaves':
                    filepath = img_morphology_leaves(lines[1], latin_name, attribute_1, attribute_2, file)
                    article += f'![none]({filepath} "none")\n\n'

        elif 'taxonomy' in attribute_2.lower():

            title = f'{latin_name.capitalize()} taxonomy'
            article += f'# {title}\n\n'
            
            try: 
                attribute_lst = ['botany', 'taxonomy']
                image_title = f'{latin_name.capitalize()} Taxonomy'
                featured_image_filpath = generate_featured_image(entity, attribute_lst, image_title)
                article += f'![alt]({featured_image_filpath} "title")\n\n'
            except:
                print(f'WARNING: missing image ({entity} -> {attribute_1}/{attribute_2})')

            # intro
            path = f'database/articles/{entity}/botany/{attribute_2}'
            with open(f'{path}/_intro.md', encoding='utf-8') as f: 
                section_content = f.read()
            article += section_content + '\n\n'

            article += f'This article gives a detailed explanation of the taxonomy, common names, and varieties of {latin_name}.' + '\n\n'

            try:
                path = f'database/articles/{entity}/botany/taxonomy'
                files = ['taxonomy']

                for file in files:
                    with open(f'{path}/{file}.md', encoding='utf-8') as f: 
                        section_content = f.read()
                    
                    if section_content.strip() != '':
                        section_title = file.split('.')[0].capitalize()
                        article += f'## {section_title}\n\n'
                        article += '\n\n' + section_content + '\n\n'
                        lines = csv_get_table_data(f'database/tables/taxonomy/{section_title.lower()}.csv')
                        article += generate_table(lines)
            except:
                print(f'WARNING: missing taxonomy stuff')
            
            
            # common names section
            try:
                article += f'## Common Names\n\n'
                filepath = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/common-names.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
                
                rows = csv_get_rows('database/tables/common-names/common-names.csv')
                # rows_filtered = [f'{row[1]}' for row in rows if entity == row[0].strip()]
                # article += lst_to_blt(rows_filtered)
                article += f'Here\'s a list of the most common names of {latin_name} with a brief description for each name.\n\n'
                rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
                article += lst_to_blt(bold_blt(rows_filtered))
                article += '\n\n'
            except:
                print(f'WARNING: missing common names stuff')


            
            # varieties
            try:
                article += f'## Varieties\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/varieties.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
                
                rows = csv_get_rows('database/tables/varieties/varieties.csv')
                article += f'Here\'s a list of the most common varieties of {latin_name} with a brief description for each variety.\n\n'
                rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
                article += lst_to_blt(bold_blt(rows_filtered))
                article += '\n\n'
            except:
                print(f'WARNING: missing varieties stuff')

            
            # morphology
            try:
                article += f'## Morphology\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/morphology.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
            except:
                print(f'WARNING: missing morphology stuff')
            
        elif 'distribution' in attribute_2.lower():

            title = f'{latin_name.capitalize()} distribution'
            article += f'# {title}\n\n'
            
            try:
                attribute_lst = ['botany', 'distribution']
                image_title = f'{latin_name.capitalize()} Distribution'
                featured_image_filpath = generate_featured_image(entity, attribute_lst, image_title)
                article += f'![alt]({featured_image_filpath} "title")\n\n'
            except: 
                print(f'WARNING: missing image ({entity} -> {attribute_1}/{attribute_2})')

            # intro
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/_intro.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'

            # article += f'This article gives a detailed explanation of the taxonomy, common names, and varieties of {latin_name}.' + '\n\n'
            
            # habitat
            try:
                article += f'## What is the natural habitat of {latin_name}?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/habitat.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'

                rows = csv_get_rows('database/tables/habitat/habitat.csv')
                article += f'Here\'s a list of the most common habitats of {latin_name} with a brief description for each one.\n\n'
                rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
                article += lst_to_blt(bold_blt(rows_filtered))
                article += '\n\n'
            except:
                print(f'WARNING: missing habitat stuff')

            # native
            try:
                section = 'native'
                article += f'## In which regions {latin_name} is native?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/{section}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'

                article += f'The following table gives a detailed list of continents and states where {latin_name} is native, according to the United States Department of Agriculture (USDA) and other governative resources around the world.\n\n'

                lines = csv_get_table_data(f'database/tables/botany/{section}.csv')
                rows = utils.csv_get_rows_by_entity(f'database/tables/botany/{section}.csv', entity)
                article += generate_table_grouped(rows)
                article += '\n\n'
            except:
                print(f'WARNING: missing native stuff')
            
            # distribution
            try:
                section = 'distribution'
                article += f'## What is the global distribution of {latin_name}?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/{section}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'

                article += f'The following table gives list of continents and the distribution of {latin_name} for each continent.\n\n'
                lines = csv_get_table_data(f'database/tables/botany/{section}.csv')
                rows = utils.csv_get_rows_by_entity(f'database/tables/botany/{section}.csv', entity)
                article += generate_table_simple(rows)
                article += '\n\n'
            except:
                print(f'WARNING: missing distribution stuff')

            
            # invasive
            try:
                section = 'invasive'
                article += f'## Is {latin_name} invasive?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/{section}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
                
                article += f'Here\'s a list of the most common habitats of {latin_name} with a brief description for each one.\n\n'
                rows = csv_get_rows(f'database/tables/botany/{section}.csv')
                rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
                article += lst_to_blt(bold_blt(rows_filtered))
                article += '\n\n'
            except:
                print(f'WARNING: missing distribution stuff')

            # invasive impact
            try:
                section = 'invasive-impact'
                article += f'### What\'s the impact of {latin_name} as an invasive species?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/{section}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
                article += '\n\n'
            except:
                print(f'WARNING: missing distribution stuff')

            # invasive control
            try:
                section = 'invasive-control'
                article += f'### How to manage and control invasive {latin_name}?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/{section}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
            except:
                print(f'WARNING: missing distribution stuff')


            # article += f'The following table gives list of continents and the distribution of {latin_name} for each continent.\n\n'
            # lines = csv_get_table_data(f'database/tables/botany/{section}.csv')
            # rows = utils.csv_get_rows_by_entity(f'database/tables/botany/{section}.csv', entity)
            # article += generate_table_simple(rows)
            # article += '\n\n'

    
    article = article.replace('’', "'") 
    attribute_lst = [x for x in [attribute_1, attribute_2] if x.strip() != '']
    article_filepath = generate_html(date, title, article, entity, attribute_lst)



##################################################################################################
# HOME PAGE
##################################################################################################

articles = utils.csv_to_llst(ARTICLES_CSV)[1:]

articles_morphology_html = ''
articles_taxonomy_html = ''
articles_distribution_html = ''
articles_main_html = ''
articles_home_benefits_html = ''
articles_home_preparations_html = ''

for article in articles:
    
    entity = normalize(article[articles_dict['entity']]).strip()
    attribute_1 = normalize(article[articles_dict['attribute_1']]).strip()
    attribute_2 = normalize(article[articles_dict['attribute_2']]).strip()
    date = normalize(article[articles_dict['date']]).strip()
    state = normalize(article[articles_dict['state']]).strip()
    done = normalize(article[articles_dict['done']]).strip()

    if state != 'published': continue

    latin_name = entity.replace('-', ' ').capitalize()
    
    try:
        common_names = utils.csv_get_rows_by_entity('database/tables/botany/common-names.csv', entity)
        common_name = common_names[0][1].lower()
    except:
        common_names = []
        common_name = ''

    if attribute_2 == 'morphology':
        img = f'images/{entity}-{attribute_1}-{attribute_2}.jpg'
        url = f'{entity}/{attribute_1}/{attribute_2}.html'
        title = f'{common_name} ({latin_name}) {attribute_2}'
        articles_morphology_html += f'''
            <a href="{url}">
                <div>
                    <img src="{img}" alt="">
                    <h2 class="mt-0 mb-0">{title}</h2>
                </div>
            </a>
            \n
        '''
    elif attribute_1 == 'medicine':
        if attribute_2 == 'benefits':
            img = f'images/{entity}-{attribute_1}-{attribute_2}-overview.jpg'
            url = f'{entity}/{attribute_1}/{attribute_2}.html'
            title = f'10 Health Benefits of {common_name.capitalize()} ({latin_name.capitalize()})'
            articles_home_benefits_html += f'''
                <a href="{url}">
                    <div>
                        <img src="{img}" alt="">
                        <h2 class="mt-0 mb-0">{title}</h2>
                    </div>
                </a>
                \n
            '''
        elif attribute_2 == 'preparations':
            img = f'images/{entity}-{attribute_1}-{attribute_2}-overview.jpg'
            url = f'{entity}/{attribute_1}/{attribute_2}.html'
            title = f'10 Medicinal Preparations of {common_name.capitalize()} ({latin_name.capitalize()})'
            articles_home_preparations_html += f'''
                <a href="{url}">
                    <div>
                        <img src="{img}" alt="">
                        <h2 class="mt-0 mb-0">{title}</h2>
                    </div>
                </a>
                \n
            '''

    elif attribute_1 == '' and attribute_2 == '':
        img = f'images/{entity}-guide.jpg'
        url = f'{entity}/index.html'
        title = f'{common_name.capitalize()} ({latin_name.capitalize()}) General Guide'
        articles_main_html += f'''
            <a href="{url}">
                <div>
                    <img src="{img}" alt="">
                    <h2 class="mt-0 mb-0">{title}</h2>
                </div>
            </a>
            \n
        '''


header = generate_header_transparent()


articles_section_main_html = ''
if normalize(articles_main_html) != '':
    articles_section_main_html = f'''
    <section class="my-96">
        <div class="container-lg">
            <h2 class="text-center mb-16">General Guides on Plants</h2>
            <p class="text-center mb-48">Learn everything about plants: from medicinal uses to botanical profiles.</p>
            <div class="articles">
                {articles_main_html}
            </div>
        </div>
    </section>
    '''
    
articles_home_section_benefits_html = ''
if normalize(articles_home_benefits_html) != '':
    articles_home_section_benefits_html = f'''
    <section class="my-96">
        <div class="container-lg">
            <h2 class="text-center mb-16">Guides on Medicinal Plants' Benefits</h2>
            <p class="text-center mb-48">Learn which are the most important plants' benefits to improve your health.</p>
            <div class="articles">
                {articles_home_benefits_html}
            </div>
        </div>
    </section>
    '''
    
articles_home_section_preparations_html = ''
if normalize(articles_home_preparations_html) != '':
    articles_home_section_preparations_html = f'''
    <section class="my-96">
        <div class="container-lg">
            <h2 class="text-center mb-16">Guides on Medicinal Plants' Preparations</h2>
            <p class="text-center mb-48">Find out what are the most useful plants' preparations and how to use them as remedies.</p>
            <div class="articles">
                {articles_home_preparations_html}
            </div>
        </div>
    </section>
    '''


html = f'''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="author" content="Martin Pellizzer">
        <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
        <link rel="stylesheet" href="style.css">
        <title>Medicinal Plants | TerraWhisper</title>
        {google_tag}
        
    </head>

    <body>
        <section class="hero-section">
            <div class="container-lg h-full">

                <section>
                    <div class="container-lg">
                        <header>
                            <a class="fg-white" href="/">TerraWhisper</a>
                            <nav>
                                <a class="fg-white" href="/plants.html">All Plants</a>
                            </nav>
                        </header>
                    </div>
                </section>

                <div class="flex flex-col justify-center items-center h-90">
                    <h1 class="fg-white text-center size-72 weight-400">Learn how to use plants to improve your life</h1>

                    <div class="container">
                        <p class="fg-white text-center">If you are interested in healing herbs and natural remedies, welcome
                            to the tribe. Here you will find out what are the best plants to boost your health and how to
                            use them correctly to improve results.</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="my-96">
            <div class="container">
                <h2 class="text-center mb-16">Embrace Scientific Herbalism</h2>
                <p class="text-center mb-16">The medicinal properties of herbs are well recognized by science and 1000+ new
                    scientific studies are conducted every year to document it. In fact, more than 75% of modern medicinals
                    are made by synthesizing and extracting biochemical compounds from plants all around the world, and the
                    number is increasing day by day.</p>
                <p class="text-center mb-16">If you are looking for a science-based approach to herbalism, and not a
                    "magical" one, enjoy our articles packed with tons of scientific data on plants' healing effects.</p>
            </div>
        </section>

        {articles_home_section_benefits_html}
        {articles_home_section_preparations_html}
        
        <footer>
            <div class="container-lg">
                <span>© TerraWhisper.com 2023 | All Rights Reserved
            </div>
        </footer>

    </body>

    </html>
'''

# {articles_section_main_html}
# {articles_section_morphology_html}
# {articles_section_taxonomy_html}
# {articles_section_distribution_html}
with open(f'index.html', 'w', encoding='utf-8') as f:
    f.write(html)



# <br><span class="size-36 weight-400">Medicine, Cuisine, Horticulture, and Botany</span>


##################################################################################################
# VIEWER
##################################################################################################

# with open(f'index_viewer.html', 'w') as f:
#     f.write(html)


# with open(f'article-viewer.html', 'w') as f:
#     f.write(html)


# with open(f'articles/achillea-millefolium/botanical.md') as f:
#     article_md = f.read()

# word_count = len(article_md.split(' '))
# reading_time_html = str(word_count // 200) + ' minutes'

# article_html = markdown.markdown(article_md, extensions=['markdown.extensions.tables'])

# # article_html = article_html.replace('<img', '<img class="img-featured"')
# # article_html = article_html.replace('src="/assets/', 'src="website/assets/')

# article_html = generate_toc(article_html)


# html = f'''
#     <!DOCTYPE html>
#     <html lang="en">

#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <link rel="stylesheet" href="style.css">
#         <title>Document</title>
#     </head>

#     <body>
#         <section>
#             <div class="container">
#                 {word_count}
#                 {reading_time_html}
#                 {article_html}
#             </div>
#         </section>
#     </body>

#     </html>
# '''

# with open(f'article-viewer.html', 'w') as f:
#     f.write(html)


##################################################################################################
# GENERAL
##################################################################################################
shutil.copy2('style.css', 'website/style.css')
shutil.copy2('index.html', 'website/index.html')
# shutil.copy2('articles-images/hero.jpg', f'{website_img_path}/hero.jpg')
# shutil.copy2('articles-images/medicinal-plants.jpg', f'{website_img_path}/medicinal-plants.jpg')
shutil.copy2('images/medicinal-plants.jpg', f'{website_img_path}/medicinal-plants.jpg')