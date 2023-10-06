import json
import os
import markdown
import shutil
from PIL import Image, ImageFont, ImageDraw, ImageColor
import math

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


with open("database.json", encoding='utf-8') as f:
    data = json.loads(f.read())

def lst_to_txt(lst):
    txt = ''
    if len(lst) == 0: txt = ''
    elif len(lst) == 1: txt = lst[0]
    elif len(lst) == 2: txt = f'{lst[0]} e {lst[1]}'
    else: txt = f'{", ".join(lst[:-1])} e {lst[-1]}'
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


def generate_toc(content_html):
    table_of_contents_html = ''

    # get list of headers and generate IDs
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
                # print(line)
                toc_inserted = True
                content_html_formatted += table_of_contents_html
                content_html_formatted += line
                continue
        content_html_formatted += line

    return content_html_formatted



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

    output_path = f'public/assets/images/{"-".join(image_path.split("/")[1:])}'
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
    output_path = f'public/assets/images/{output_filename}-taxonomy.jpg'
    
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
    output_path = f'public/assets/images/{output_filename}-cycle-of-life.jpg'

    img.thumbnail((w//resampler, h//resampler), Image.Resampling.LANCZOS)
    
    img.convert('RGB').save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path


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
    output_path = f'public/assets/images/{output_filename}-{img_name}.jpg'
    img.save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path


######################################################################
# FOLDERS
######################################################################

def generate_folders():
    for item in data:
        domain = item['domain'].lower()
        kingdom = item['kingdom'].lower()
        phylum = item['phylum'].lower()
        _class = item['class'].lower()
        order = item['order'].lower()
        family = item['family'].lower()
        genus = item['genus'].lower()
        species = item['species'].lower()

        try: os.mkdir(f'articles/{domain}')
        except: pass
        try: os.mkdir(f'articles/{domain}/{kingdom}')
        except: pass
        try: os.mkdir(f'articles/{domain}/{kingdom}/{phylum}')
        except: pass
        try: os.mkdir(f'articles/{domain}/{kingdom}/{phylum}/{_class}')
        except: pass
        try: os.mkdir(f'articles/{domain}/{kingdom}/{phylum}/{_class}/{order}')
        except: pass
        try: os.mkdir(f'articles/{domain}/{kingdom}/{phylum}/{_class}/{order}/{family}')
        except: pass
        try: os.mkdir(f'articles/{domain}/{kingdom}/{phylum}/{_class}/{order}/{family}/{genus}')
        except: pass

        try: os.mkdir(f'public/{domain}')
        except: pass
        try: os.mkdir(f'public/{domain}/{kingdom}')
        except: pass
        try: os.mkdir(f'public/{domain}/{kingdom}/{phylum}')
        except: pass
        try: os.mkdir(f'public/{domain}/{kingdom}/{phylum}/{_class}')
        except: pass
        try: os.mkdir(f'public/{domain}/{kingdom}/{phylum}/{_class}/{order}')
        except: pass
        try: os.mkdir(f'public/{domain}/{kingdom}/{phylum}/{_class}/{order}/{family}')
        except: pass
        try: os.mkdir(f'public/{domain}/{kingdom}/{phylum}/{_class}/{order}/{family}/{genus}')
        except: pass
        try: os.mkdir(f'public/assets')
        except: pass
        try: os.mkdir(f'public/assets/images')
        except: pass


generate_folders()





for item in data:
    article = ''
    
    domain = item['domain']
    kingdom = item['kingdom']
    phylum = item['phylum']
    _class = item['class']
    order = item['order']
    family = item['family']
    genus = item['genus']
    species = item['species']

    most_common_name = item['common_names'][0].split(':')[0].lower()
    most_common_name_1 = item['common_names'][0].split(':')[0].lower()
    most_common_name_2 = item['common_names'][1].split(':')[0].lower()
    latin_name = f'{genus} {species}'
    latin_name_abb = f'{genus[0]}. {species}'

    common_names = item['common_names']
    regional_variations = item['regional_variations']
    
    distribution_table = item['distribution_table']
    distribution = item['distribution']
    
    habitat = item['habitat']
    morphology = item['morphology']
    life_cycle = item['life_cycle']
    reproduction = item['reproduction']

    history = item['history']
    history_medicinal_uses = item['history_medicinal_uses']
    history_culinary_uses = item['history_culinary_uses']
    history_spiritual_uses = item['history_spiritual_uses']
        
    culinary_uses = item['culinary_uses']
    beverage_uses = item['beverage_uses']
    sensory_characteristics = item['sensory_characteristics']
    
    horticultural_cultivation = item['horticultural_cultivation']
    environmental_requirements = item['environmental_requirements']
    pests = item['pests']
    diseases = item['diseases']

    article += f'# {latin_name} ({most_common_name}) guide\n\n'

    img_filename = latin_name.lower().replace(' ', '-') + '.jpg'
    img_filepath = img_resize(f'articles-images/{img_filename}')
    img_filepath = '/' + '/'.join(img_filepath.split('/')[1:])
    article += f'![alt]({img_filepath} "title")\n\n'


    #######################################################################################################
    # TAXONOMY/CLASSIFICATION
    #######################################################################################################
    # article += f'## What is the classification (taxonomy) of {most_common_name}?\n\n'
    article += f'## What is {latin_name} and how is it classified?\n\n'
    article += f'{latin_name} (or {latin_name_abb}), commonly known as {most_common_name}, is a plant that belong to the {family} family.\n\n'
    
    lst = []
    lst_taxonomy = []
    lst_taxonomy.append(f'Domain: {domain}')
    lst_taxonomy.append(f'Kingdom: {kingdom}')
    lst_taxonomy.append(f'Phylum: {phylum}')
    lst_taxonomy.append(f'Class: {_class}')
    lst_taxonomy.append(f'Order: {order}')
    lst_taxonomy.append(f'Family: {family}')
    lst_taxonomy.append(f'Genus: {genus}')
    lst_taxonomy.append(f'Species: {species}')
    lst_taxonomy.insert(0, 'Taxonomy')
    lst.append(lst_taxonomy)

    lst_common_names = [x.split(':')[0] for x in common_names]
    lst_common_names.insert(0, 'Common Names')
    lst.append(lst_common_names)

    lst_regional_variations = [item.split(':')[0] for item in regional_variations]
    lst_regional_variations.insert(0, 'Regional Variations')
    lst.append(lst_regional_variations)

    # CHEAT SHEET
    img_path = img_cheasheet(latin_name, 'Classification and Variations of', lst, 'taxonomy')
    img_path = '/' + '/'.join(img_path.split('/')[1:])
    article += f'The following illustration shows you this classificaion visually.\n\n'
    article += f'![alt]({img_path} "title")\n\n'

    # TAXONOMY
    lst_taxonomy.pop(0)
    article += f'Right below you can find the full classification (taxonomy) of this plant.\n\n'
    bld = bold_blt(lst_taxonomy)
    article += lst_to_blt(bld)
    article += '\n\n'

    # COMMON NAMES
    article += f'### What are its common names?\n\n'
    article += f'The most frequent common names for this plant are **{most_common_name_1.title()}** and **{most_common_name_2.title()}**.\n\n'
    article += f'Here is a list of the common names of this plant and a brief description of each name.\n\n'
    bld = bold_blt(common_names)
    article += lst_to_blt(bld[:7])
    article += '\n\n'

    # REGIONAL VARIATIONS
    names = [item.split(':')[0] for item in regional_variations]
    intro = ''
    intro += f'**{names[0].split("(")[0].strip()}**, **{names[1].split("(")[0].strip()}**, and **{names[2].split("(")[0].strip()}**'
    article += f'### What are its regional variations?\n\n'
    article += f'This plant has several regional variations (subspecies), like {intro}.\n\n'
    article += f'Here\'s a list of some subspecies (subsp.) of this plant.\n\n'
    regional_variations = [variation for variation in regional_variations]
    bld = bold_blt(regional_variations)
    article += lst_to_blt(bld)
    article += '\n\n'


    #######################################################################################################
    # WHERE
    #######################################################################################################
    article += f'## Where does {latin_name} grow?\n\n'

    # CONTINENTAL DISTRIBUTION
    # article += f'### Continental distribution\n\n'
    quick_answer = f'The {latin_name} is mainly present in **{distribution_table[0][0]}** and in **{distribution_table[1][0]}**.\n\n'
    article += f'{quick_answer}\n'

    article += f'In the following table, you can find the estimated distribution of this plant in each continent (ordered from highest to lowest).\n\n'

    article += f'| Continent | Estimated Distribution |\n'
    article += f'| --- | --- |\n'
    for row in distribution_table:
        if int(row[1]) >= 7: value = 'Abundant' 
        elif int(row[1]) >= 4: value = 'Common' 
        else: value = 'Scarce' 
        article += f'| {row[0]} | {value} |\n'
    article += '\n'

    article += f'Here\'s a list of the regional distribution of this plant.\n\n'
    bld = bold_blt(distribution)
    article += lst_to_blt(bld)
    article += '\n\n'

    # HABITAT
    names = [item.split(':')[0] for item in habitat]
    intro = f'**{names[0].lower()}**, **{names[1].lower()}**, and **{names[2].lower()}**'
    article += f'### What\'s its favorite habitat?\n\n'
    article += f'This plant mainly grows in {intro}, but it can be also found in many other places.\n\n'
    article += f'Here\'s a list of the habitats that this plant prefers.\n\n'
    bld = bold_blt(habitat)
    article += lst_to_blt(bld)
    article += '\n\n'

    #######################################################################################################
    # BOTANICAL CHARACTERISTICS
    #######################################################################################################
    article += f'## What are the botanical characteristics of {latin_name}?\n\n'


    # CHEAT SHEET
    lst = []
    tmp_lst = [f'{x.split(":")[0]}' for x in morphology]
    tmp_lst.insert(0, 'Morphology')
    lst.append(tmp_lst)
    tmp_lst = [f'{x.split(":")[0]}' for x in life_cycle]
    tmp_lst.insert(0, 'Life Cycle')
    lst.append(tmp_lst)
    tmp_lst = [f'{x.split(":")[0]}' for x in reproduction]
    tmp_lst.insert(0, 'Reproduction')
    lst.append(tmp_lst)

    img_path = img_cheasheet(latin_name, 'Botanical Properties of', lst, 'botanical-characteristics')
    img_path = '/' + '/'.join(img_path.split('/')[1:])
    article += f'The following illustration shows you this classificaion visually.\n\n'
    article += f'![alt]({img_path} "title")\n\n'
    
    
    # MORPHOLOGY
    article += f'### Morphology\n\n'
    lst = [item.split(':')[0].lower() for item in morphology]
    intro = lst_to_txt(lst)
    article += f'This plant is composed of {intro}.\n\n'
    article += f'Here\'s a brief description of each part.\n\n'
    bld = bold_blt(morphology)
    article += lst_to_blt(bld)
    article += '\n\n'

    # LIFE CYCLE
    article += f'### Life cycle\n\n'
    lst = [item.split(':')[0].lower() for item in life_cycle]
    intro = lst_to_txt(lst)
    article += f'The life cycle phases of this plant are {intro}.\n\n'
    article += f'Here\'s a brief description of each phase.\n\n'
    bld = bold_blt(life_cycle)
    article += lst_to_blt(bld)
    article += '\n\n'

    # REPRODUCTION
    article += f'### Reproduction\n\n'
    article += f'Here\'s listed the different ways {most_common_name} reproduce and propagate.\n\n'
    bld = bold_blt(reproduction)
    article += lst_to_blt(bld)
    article += '\n\n'

    
    ##################################################################################################
    # HISTORICAL USES
    ##################################################################################################
    article += f'## What are the historical uses of {latin_name}?\n\n'

    # ### HISTORY ETHNOBOTANICAL USES
    # article += f'### What is the ethnobotanical history of {most_common_name}?\n\n'
    # article += f'Here\'s listed some ethnobotanical history references about {most_common_name}.\n\n'
    # bld = bold_blt(history)
    # article += lst_to_blt(bld)
    # article += '\n\n'
    
    # CHEAT SHEET
    lst = []
    tmp_lst = [f'{x.split(":")[0]}' for x in history_medicinal_uses]
    tmp_lst.insert(0, 'Medicinal Uses')
    lst.append(tmp_lst)
    tmp_lst = [f'{x.split(":")[0]}' for x in history_culinary_uses]
    tmp_lst.insert(0, 'Culinary Uses')
    lst.append(tmp_lst)
    tmp_lst = [f'{x.split(":")[0]}' for x in history_spiritual_uses]
    tmp_lst.insert(0, 'Spiritual Uses')
    lst.append(tmp_lst)

    img_path = img_cheasheet(latin_name, 'Historical Uses of', lst, 'historical-uses')
    img_path = '/' + '/'.join(img_path.split('/')[1:])
    article += f'The following illustration shows you this classificaion visually.\n\n'
    article += f'![alt]({img_path} "title")\n\n'
    
    # MEDICINAL USES
    article += f'### Medical Uses\n\n'
    article += f'Here\'s listed some medicinal uses of this plant in ancient cultures.\n\n'
    bld = bold_blt(history_medicinal_uses)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    # CULINARY USES
    article += f'### Culinary Uses\n\n'
    article += f'Here\'s listed some culinary uses of this plant in ancient cultures.\n\n'
    bld = bold_blt(history_culinary_uses)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    # SPIRITUAL USES
    article += f'### Spiritual Uses\n\n'
    article += f'Here\'s listed some spiritual uses of this plant in ancient cultures.\n\n'
    bld = bold_blt(history_spiritual_uses)
    article += lst_to_blt(bld)
    article += '\n\n'



    ##################################################################################################
    # COMPOSITION
    ##################################################################################################
    article += f'## What is the chemical composition of this plant?\n\n'
    article += f'### Phytochemicals\n\n'
    article += f'Here\'s a list of the phytochemicals.\n\n'
    bld = bold_blt(item['phytochemicals'])
    article += lst_to_blt(bld)
    article += '\n\n'



    ## Medicinal Benefits
    article += f'## What are the medicinal benefits of this plant?\n\n'
    article += f'Here\'s a list of the traditional remedies of this plant.\n\n'
    bld = bold_blt(item['medicinal_uses'])
    article += lst_to_blt(bld)
    article += '\n\n'

    
    
    ## Culinary and Beverage Uses
    article += f'## What are the culinary and beverage uses of {most_common_name}?\n\n'

    ### culinary_uses
    article += f'### culinary uses \n\n'.title()
    article += f'Here\'s a list of culinary uses of {most_common_name}.\n\n'
    bld = bold_blt(culinary_uses)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    ### beverage_uses
    article += f'### beverage uses \n\n'.title()
    article += f'Here\'s a list of beverage uses of {most_common_name}.\n\n'
    bld = bold_blt(beverage_uses)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    ### sensory_characteristics
    article += f'### sensory characteristics \n\n'.title()
    article += f'Here\'s a list of sensory characteristics of {most_common_name}.\n\n'
    bld = bold_blt(sensory_characteristics)
    article += lst_to_blt(bld)
    article += '\n\n'

    
    ## horticultural considerations
    article += f'## What are the horticultural considerations of {most_common_name}?\n\n'
    
    ### horticultural_cultivation
    article += f'### horticultural cultivation\n\n'.title()
    article += f'Here\'s a list of horticultural tips to cultivate {most_common_name}.\n\n'
    bld = bold_blt(horticultural_cultivation)
    article += lst_to_blt(bld)
    article += '\n\n'
    
    ### environmental_requirements
    article += f'### environmental requirements\n\n'.title()
    article += f'Here\'s a list of environmental requirements to cultivate {most_common_name}.\n\n'
    bld = bold_blt(environmental_requirements)
    article += lst_to_blt(bld)
    article += '\n\n'

    ### pests
    article += f'### pests\n\n'.title()
    article += f'Here\'s a list of common pests of {most_common_name}.\n\n'
    bld = bold_blt(pests)
    article += lst_to_blt(bld)
    article += '\n\n'

    ### diseases
    article += f'### diseases\n\n'.title()
    article += f'Here\'s a list of common diseases of {most_common_name}.\n\n'
    bld = bold_blt(diseases)
    article += lst_to_blt(bld)
    article += '\n\n'




    
    # try: os.mkdir(f'articles/{domain}/{kingdom}/{phylum}/{_class}/{order}/{family}/{genus}/{species}')
    # except: pass

    article_filename = latin_name.lower().replace(' ', '-')
    with open(f'articles/{domain}/{kingdom}/{phylum}/{_class}/{order}/{family}/{genus}/{species}.md', 'w', encoding='utf-8') as f:
        f.write(article)
    # print(item)

    article_html = markdown.markdown(article, extensions=['markdown.extensions.tables'])

    
    # article_html = article_html.replace('<img', '<img class="img-featured"')
    
    # ADD TABLE OF CONTENTS ----------------------------------------
    article_html = generate_toc(article_html)
    
    word_count = len(article.split(' '))
    reading_time_html = str(word_count // 200) + ' minutes'
    word_count_html = str(word_count) + ' words'

    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/style.css">
            <title>Document</title>
        </head>

        <body>
            <section class="my-96">
                <div class="container">
                    <div class="flex justify-between mb-16">
                        <span>by Martin Pellizzer - 2023/10/02</span>
                        <span>{reading_time_html} ({word_count_html})</span>
                    </div>
                    {article_html}
                </div>
            </section>
        </body>

        </html>
    '''


    

    with open(f'public/{domain}/{kingdom}/{phylum}/{_class}/{order}/{family}/{genus}/{species}.html', 'w', encoding='utf-8') as f:
        f.write(html)


with open(f'article-viewer.html', 'w') as f:
    f.write(html)





# VIEWER
with open(f'articles/eukarya/plantae/angiosperms/eudicots/asterales/asteraceae/achillea/millefolium.md') as f:
    article_md = f.read()

word_count = len(article_md.split(' '))
reading_time_html = str(word_count // 200) + ' minutes'

article_html = markdown.markdown(article_md, extensions=['markdown.extensions.tables'])

article_html = article_html.replace('<img', '<img class="img-featured"')
article_html = article_html.replace('src="/assets/', 'src="public/assets/')


# ADD TABLE OF CONTENTS ----------------------------------------
article_html = generate_toc(article_html)


html = f'''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="style.css">
        <title>Document</title>
    </head>

    <body>
        <section>
            <div class="container">
                {word_count}
                {reading_time_html}
                {article_html}
            </div>
        </section>
    </body>

    </html>
'''

with open(f'article-viewer.html', 'w') as f:
    f.write(html)



shutil.copy2('style.css', 'public/style.css')
shutil.copy2('index.html', 'public/index.html')