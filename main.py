# TODO: make template for second post type (list to table (common name))
# TODO: make image for root, (draw line)

import json
import os
import markdown
import shutil
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
import math
import re
import csv




# with open("database/growing_zones.json", encoding='utf-8') as f:
#     growing_zones_data = json.loads(f.read())

website_img_path = 'website/images'


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


def csv_to_llst(filepath):
    llst = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f, delimiter='\\')
        for row in reader:
            llst.append(row)
    return llst



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


# def csv_get_

######################################################################
# IMAGES 
######################################################################
def img_resize(image_path):
    w, h = 768, 512

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


def img_morphology_root(row, atin_name, category, attribute, file):
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
    line = f'Achillea millefolium {file} morphology'
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

    val = row[6].split('(')[0]
    line = f'Depth: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    img_v = Image.new(mode="RGBA", size=(line_w, line_h), color='#ffffff')
    draw_v = ImageDraw.Draw(img_v)
    draw_v.text((0, 0), line, '#000000', font=font)
    img_v = img_v.rotate(90, expand=1)
    img.paste(img_v, (x + line_h, img_h//2 - line_w//2), img_v)

    val = row[9].split('(')[0]
    line = f'Color: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 200), line, '#000000', font=font)
    thickness = 6
    draw.line((200 + line_h + 10, 200 + line_h + 10, 475, 475), fill='#ffffff', width=thickness)
    draw.ellipse((475-thickness, 475-thickness, 475+thickness, 475+thickness), fill=(255,255,255,255))
    thickness = 2
    draw.line((200 + line_h + 10, 200 + line_h + 10, 475, 475), fill='#000000', width=thickness)
    draw.line((50, 200 + line_h + 10, 200 + line_h + 10 + thickness//3, 200 + line_h + 10), fill='#000000', width=thickness)
    draw.ellipse((475-thickness-1, 475-thickness-1, 475+thickness+1, 475+thickness+1), fill=(0,0,0,255))

    attribute = attribute.replace('/', '-')
    featured_image_filename = f'website/images/{entity}-{category}-{attribute}-{file}.jpg'
    
    img = img.convert('RGB')
    img = img.resize((768, 768))
    img.save(featured_image_filename, format='JPEG', subsampling=0, quality=100)

    # print(featured_image_filpath)
    filepath = '/' + '/'.join(featured_image_filename.split('/')[1:])

    return filepath
    # img.show()
    # quit()


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


def generate_featured_image(entity, attribute):
    attribute_filename = attribute.replace('/', '-')
    featured_image_filename = f'{entity}-{attribute_filename}.jpg'
    featured_image_filpath = img_resize(f'articles-images/{featured_image_filename}')

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
    line = f'{latin_name} morphology'
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




######################################################################
# HTML 
######################################################################
def generate_header_light():
    html = '''
    <header>
        <div class="container-lg">
            <nav class="flex justify-between">
                <a href="/">TerraWhisper</a>
                <a href="#"></a>
            </nav>
        </div>
    </header>
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


def generate_html(date, title, article, entity, attribute):
    article_filepath = f'{entity}/{attribute}.md'
    with open(f'articles/{article_filepath}', 'w', encoding='utf-8') as f:
        f.write(article)

    article_html = markdown.markdown(article, extensions=['markdown.extensions.tables'])

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
            <link rel="stylesheet" href="/style.css">
            <title>{title}</title>

            {google_tag}
        </head>

        <body>
            {header}

            <section class="my-96">
                <div class="container">
                    <div class="flex justify-between mb-16">
                        <span>by Martin Pellizzer - {date}</span>
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

    article_filepath = f'{entity}/{attribute}.html'
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
try: shutil.rmtree('website')
except: pass

try: os.mkdir(f'articles')
except: pass
try: os.mkdir(f'website')
except: pass

chunks = website_img_path.split('/')
curr_chunk = ''
for chunk in chunks:
    curr_chunk += chunk + '/'
    try: os.mkdir(curr_chunk)
    except: pass



######################################################################
# MAIN
######################################################################

articles_home = []

articles_master_rows = csv_to_llst('database/tables/articles.csv')[1:]

for i, row in enumerate(articles_master_rows):
    print(f'{i}/{len(articles_master_rows)}')
    entity = row[0].strip()
    category = row[1].strip()
    attribute = row[2].strip()
    date = row[3].strip()
    state = row[4].strip()
    done = row[5].strip()
    latin_name = entity.replace('-', ' ').capitalize()

    try: os.mkdir(f'articles/{entity}')
    except: pass
    try: os.mkdir(f'articles/{entity}/{category}')
    except: pass
    try: os.mkdir(f'articles/{entity}/{category}/{attribute}')
    except: pass
    try: os.mkdir(f'website/{entity}')
    except: pass
    try: os.mkdir(f'website/{entity}/{category}')
    except: pass
    try: os.mkdir(f'website/{entity}/{category}/{attribute}')
    except: pass

    article = ''
    if 'morphology' in attribute.lower():
        title = f'{latin_name.capitalize()} morphology'
        article += f'# {title}\n\n'

        try:
            featured_image_filpath = generate_featured_image(entity, f'{category}/{attribute}')
            article += f'![{title}]({featured_image_filpath} "{title}")\n\n'
        except:
            print(f'WARNING: missing image ({entity})')

        # img_title = 'Morphology of'
        # llst = []
        # csv_lines = []
        # for file in os.listdir(f'database/tables/morphology'):
        #     tmp_lst = []
        #     first_line = []
        #     with open(f'database/tables/morphology/{file}', encoding='utf-8', errors='ignore') as f:
        #         reader = csv.reader(f, delimiter="\\")
        #         for i, line in enumerate(reader):
        #             if i == 0: first_line = line
        #             if entity.strip() == line[0].strip():
        #                 for i in range(len(line[:5])):
        #                     tmp_lst.append(f'{first_line[i]}: {line[i]}')
        #                 llst.append(tmp_lst)

        # filepath = img_cheasheet(latin_name, img_title, llst, 'test')
        # print(filepath)

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

            # filepath = img_morphology_root(lines[1], latin_name, category, attribute, file)
            # article += f'![none]({filepath} "none")\n\n'

    elif 'taxonomy' in attribute.lower():

        title = f'{latin_name.capitalize()} taxonomy'
        article += f'# {title}\n\n'
        
        featured_image_filpath = generate_featured_image(entity, f'{category}/{attribute}')
        article += f'![alt]({featured_image_filpath} "title")\n\n'

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
        
        # common names section
        article += f'## Common Names\n\n'
        path = f'database/articles/{entity}/botany/common-names'
        with open(f'{path}/common-names.md', encoding='utf-8') as f: 
            section_content = f.read()
        article += section_content + '\n\n'

        rows = csv_get_rows('database/tables/common-names/common-names.csv')
        # rows_filtered = [f'{row[1]}' for row in rows if entity == row[0].strip()]
        # article += lst_to_blt(rows_filtered)
        article += f'Here\'s a list of the most common names of {latin_name} with a brief description for each name.\n\n'
        rows_filtered = [f'{row[1]}: {row[2]}' for row in rows if entity == row[0].strip()]
        article += lst_to_blt(bold_blt(rows_filtered))
        article += '\n\n'

        
        # varieties
        article += f'## Varieties\n\n'
        path = f'database/articles/{entity}/botany/varieties'
        with open(f'{path}/varieties.md', encoding='utf-8') as f: 
            section_content = f.read()
        article += section_content + '\n\n'
        
        rows = csv_get_rows('database/tables/varieties/varieties.csv')
        article += f'Here\'s a list of the most common varieties of {latin_name} with a brief description for each variety.\n\n'
        rows_filtered = [f'{row[1]}: {row[2]}' for row in rows if entity == row[0].strip()]
        article += lst_to_blt(bold_blt(rows_filtered))
        article += '\n\n'


        
        # article += lst_to_blt(bold_blt(lines))

    # print(attribute.lower())
    article_filepath = generate_html(date, title, article, entity, f'{category}/{attribute}')
    
    if state == 'published':
        articles_home.append(
            {
                'img': featured_image_filpath,
                'url': article_filepath,
                'name': '',
                'title': title,
            }
        )





##################################################################################################
# HOME PAGE
##################################################################################################

articles = csv_to_llst('database/tables/articles.csv')[1:]

articles_morphology_html = ''
articles_taxonomy_html = ''

for article in articles:
    entity = normalize(article[0])
    category = normalize(article[1])
    attribute = normalize(article[2])
    date = normalize(article[3])
    state = normalize(article[4])
    done = normalize(article[5])
    if state != 'published': continue

    latin_name = entity.replace('-', ' ').capitalize()
    if attribute == 'morphology':
        img = f'images/{entity}-{category}-{attribute}.jpg'
        url = f'{entity}/{category}/{attribute}.html'
        title = f'{latin_name} {attribute}'
        articles_morphology_html += f'''
            <a href="{url}">
                <div>
                    <img src="{img}" alt="">
                    <h2 class="mt-0 mb-0">{title}</h2>
                </div>
            </a>
            \n
        '''
    elif attribute == 'taxonomy':
        img = f'images/{entity}-{category}-{attribute}.jpg'
        url = f'{entity}/{category}/{attribute}.html'
        title = f'{latin_name} {attribute}'
        articles_taxonomy_html += f'''
            <a href="{url}">
                <div>
                    <img src="{img}" alt="">
                    <h2 class="mt-0 mb-0">{title}</h2>
                </div>
            </a>
            \n
        '''


header = generate_header_transparent()

articles_section_taxonomy_html = ''
if normalize(articles_taxonomy_html) != '':
    articles_section_taxonomy_html = f'''
    <section class="my-96">
        <div class="container-lg">
            <h2 class="text-center mb-16">Latest Articles on Plant Taxonomy</h2>
            <p class="text-center mb-48">Learn everything about plant taxonomy, classification, common names, and varieties</p>
            <div class="articles">
                {articles_taxonomy_html}
            </div>
        </div>
    </section>
    '''
    
articles_section_morphology_html = ''
if normalize(articles_morphology_html) != '':
    articles_section_morphology_html = f'''
    <section class="my-96">
        <div class="container-lg">
            <h2 class="text-center mb-16">Latest Articles on Plant Morphology</h2>
            <p class="text-center mb-48">Learn everything about plant roots, stems, leaves, flowers, fruits, seeds, and other parts.</p>
            <div class="articles">
                {articles_morphology_html}
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
        <link rel="stylesheet" href="style.css">
        <title>Your Botanical Guide | TerraWhisper</title>
        {google_tag}
        
    </head>

    <body>
        <section class="hero-section">
            <div class="container-lg h-full">
                {header}
                <div class="flex justify-center items-center h-90">
                    <h1 class="fg-white text-center"><span class="size-96">Your Botanical Guide:</span><br><span
                            class="size-36 weight-400">Plant Taxonomy, Morphology, and Sensory Characteristics</span>
                    </h1>
                </div>
            </div>
        </section>cd
        {articles_section_morphology_html}
        {articles_section_taxonomy_html}
        <footer>
            <div class="container-lg">
                <span>© TerraWhisper.com 2023 | All Rights Reserved
            </div>
        </footer>
    </body>

    </html>
'''

with open(f'index.html', 'w', encoding='utf-8') as f:
    f.write(html)





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
shutil.copy2('articles-images/hero.jpg', f'{website_img_path}/hero.jpg')