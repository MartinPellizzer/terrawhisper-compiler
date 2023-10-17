import json
import os
import markdown
import shutil
from PIL import Image, ImageFont, ImageDraw, ImageColor
import math
import re
import csv




with open("database/growing_zones.json", encoding='utf-8') as f:
    growing_zones_data = json.loads(f.read())


def generate_header():
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
    html = '''
    <header>
        <nav class="flex justify-between">
            <a class="fg-white" href="/">TerraWhisper</a>
            <a href="#"></a>
        </nav>
    </header>
    '''

    return html


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

    output_path = f'website/assets/images/{"-".join(image_path.split("/")[1:])}'
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
    output_path = f'website/assets/images/{output_filename}-taxonomy.jpg'
    
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
    output_path = f'website/assets/images/{output_filename}-cycle-of-life.jpg'

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
    output_path = f'website/assets/images/{output_filename}-{img_name}.jpg'
    img.save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path




######################################################################
def generate_html(article, entity, attribute):
    article_filepath = f'{entity}/{attribute}.md'
    with open(f'articles/{article_filepath}', 'w', encoding='utf-8') as f:
        f.write(article)

    article_html = markdown.markdown(article, extensions=['markdown.extensions.tables'])

    article_html = generate_toc(article_html)
    
    word_count = len(article.split(' '))
    reading_time_html = str(word_count // 200) + ' minutes'

    header = generate_header()

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
            {header}

            <section class="my-96">
                <div class="container">
                    <div class="flex justify-between mb-16">
                        <span>by Martin Pellizzer - 2023/10/02</span>
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


def generate_featured_image(entity, attribute):
    attribute_filename = attribute.replace('/', '-')
    featured_image_filename = f'{entity}-{attribute_filename}.jpg'
    featured_image_filpath = img_resize(f'articles-images/{featured_image_filename}')
    # print(featured_image_filpath)
    featured_image_filpath = '/' + '/'.join(featured_image_filpath.split('/')[1:])

    return featured_image_filpath



######################################################################
# FOLDERS
######################################################################

articles_folder = 'database/articles/'
articles_files = os.listdir(articles_folder)

try: shutil.rmtree('articles')
except: pass
try: shutil.rmtree('website')
except: pass

try: os.mkdir(f'articles')
except: pass
try: os.mkdir(f'website')
except: pass

try: os.mkdir(f'website/assets')
except: pass
try: os.mkdir(f'website/assets/images')
except: pass



articles_home = []

for f in articles_files:
    article_path = 'database/articles/' + f

    with open(article_path, encoding='utf-8') as f:
        data = json.loads(f.read())

    for item in data:

        state = item['state']
        post_type = item['post_type']
        latin_name = item['latin_name']
        most_common_name = item['common_name']

        if 'draft' == state.lower().strip(): continue

        # TODO: remove
        # if 'Allium sativum' != latin_name: continue
        # print(latin_name)

        entity = item["latin_name"].lower().replace(' ', '-')
        attribute = item['attribute']

        try: os.mkdir(f'articles/{entity}')
        except: pass
        try: os.mkdir(f'website/{entity}')
        except: pass

        folders = [x for x in attribute.split('/')]
        curr_path = ''
        for folder in folders:
            curr_path += folder + '/'
            try: os.mkdir(f'articles/{entity}/{curr_path}')
            except: pass
            try: os.mkdir(f'website/{entity}/{curr_path}')
            except: pass
        # try: os.mkdir(f'website/{entity}/{attribute_name}')
        # except: pass

        article = ''

        

        if 'list' == post_type:
            if 'morphology' in attribute.lower():
                main_content = item['main_content']

                title = f'What is the morphology of {latin_name}?'
                article += f'# {title}\n\n'
                
                featured_image_filpath = generate_featured_image(entity, attribute)
                article += f'![alt]({featured_image_filpath} "title")\n\n'

                for section in main_content:
                    title = section["title"]
                    if 'bulb' in title.lower():
                        article += f'### {title}\n\n'
                    else:
                        article += f'## {title}\n\n'
                    article += '\n\n'.join(section['content']) + '\n\n'
                    
                    # characteristics = section['characteristics']
                    article += f'| Characteristic | Description |\n'
                    article += f'| --- | --- |\n'
                    # for characteristic in characteristics:
                    #     article += f'| {characteristic["name"].title()} | {characteristic["desc"].capitalize()} |\n'
                    # article += f'\n'

                    lines = []
                    with open(f'database/tables/morphology/{section["title"].lower()}.csv') as f:
                        reader = csv.reader(f, delimiter="\\")
                        for i, line in enumerate(reader):
                            if i == 0:
                                lines.append(line)
                            else:
                                if line[0].strip() == entity.strip():
                                    lines.append(line)

                    # for line in lines:
                    #     print(line)
                    
                    for i in range(len(lines[0])):
                        if i == 0: continue
                        if lines[0][i].strip() == '': continue
                        try: 
                            if lines[1][i].strip() == '': continue
                        except: continue
                        article += f'| {lines[0][i].title()} | {lines[1][i].capitalize()} |\n'
                    article += f'\n'

                    # for line in lines:
                    #     print(line)
                    # quit()

            else:
                continue

                main_content = item['main_content']

                title = f'{len(main_content)} Benefits of {latin_name}'
                article += f'# {title}\n\n'

                for i, section in enumerate(main_content):
                    article += f'## {i+1}. {section["title"]}\n\n'
                    article += '\n\n'.join(section['content']) + '\n\n'


        else:
            #######################################################################################################
            #######################################################################################################
            #######################################################################################################
            # BOTANICAL
            #######################################################################################################
            #######################################################################################################
            #######################################################################################################
            if 'botanical' == attribute.lower():
                domain = item['domain']
            
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
                most_common_name_3 = item['common_names'][2].split(':')[0].lower()
                latin_name = f'{genus} {species}'
                latin_name_abb = f'{genus[0]}. {species}'

                common_names = item['common_names']
                regional_variations = item['regional_variations']
                
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

                #######################################################################################################
                # TITLE
                #######################################################################################################
                article += f'# {latin_name.title()} ({most_common_name.title()}) Botanical Guide\n\n'

                featured_image_filename = latin_name.lower().replace(' ', '-') + '.jpg'
                featured_image_filpath = img_resize(f'articles-images/{featured_image_filename}')
                featured_image_filpath = '/' + '/'.join(featured_image_filpath.split('/')[1:])
                article += f'![alt]({featured_image_filpath} "title")\n\n'


                #######################################################################################################
                # TAXONOMY/CLASSIFICATION
                #######################################################################################################
                # article += f'## What is the classification (taxonomy) of {most_common_name}?\n\n'
                article += f'## What is the botanical classification of {most_common_name}?\n\n'
                line = f'''
                    {most_common_name.title()}, with botanical name of **{latin_name}** ({latin_name_abb}), is a plant that belongs to the **{family}** family and the **{genus}** genus.

                    According to traditional classification (taxonomy), this plant is classified under the **{order}** order, the **{_class}** class, and the **{kingdom}** kingdom (in the {domain} domain).
                \n\n'''
                article += re.sub(' +', ' ', line)

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
                # img_path = img_cheasheet(latin_name, 'Classification and Variations of', lst, 'taxonomy')
                # img_path = '/' + '/'.join(img_path.split('/')[1:])
                # article += f'The following illustration shows you this classificaion visually.\n\n'
                # article += f'![alt]({img_path} "title")\n\n'

                # TAXONOMY
                lst_taxonomy.pop(0)
                article += f'Here is a list showing the full taxonomy of {latin_name_abb}, in hierarchical order.\n\n'
                article += lst_to_blt(lst_taxonomy)
                article += '\n\n'

                # COMMON NAMES
                article += f'### What are the common names of {latin_name}?\n\n'
                article += f'The most common name for this plant is **{most_common_name_1.title()}**, but other common names are **{most_common_name_2.title()}** and **{most_common_name_3.title()}**.\n\n'
                article += f'Here is a list of the most common names of {latin_name_abb} ordered by popularity, with a brief description of each name.\n\n'
                bld = bold_blt(common_names)
                article += lst_to_blt(bld)
                article += '\n\n'

                # REGIONAL VARIATIONS
                names = [item.split(':')[0] for item in regional_variations]
                intro = ''
                intro += f'**{names[0].split("(")[0].strip()}**, **{names[1].split("(")[0].strip()}**, and **{names[2].split("(")[0].strip()}**'
                article += f'### What are the regional variations of {latin_name}?\n\n'
                article += f'The most common regional variations (subspecies) of this plant are {intro}.\n\n'
                article += f'In the following list, you can find a more extensive list of common variations of {latin_name_abb}, with a brief description of their unique characteristics and their main regional location.\n\n'
                regional_variations = [variation for variation in regional_variations]
                bld = bold_blt(regional_variations)
                article += lst_to_blt(bld)
                article += '\n\n'


                #######################################################################################################
                # MORPHOLOGY
                #######################################################################################################
                article += f'## What is the morphology of {latin_name_abb}?\n\n'
                article += '\n\n'.join([x for x in item['botanical_morphology_intro']]) + '\n\n'
                article += f'### Roots\n\n'
                article += lst_to_blt(bold_blt(item['botanical_morphology_roots'])) + '\n\n'
                article += f'### Stems\n\n'
                article += lst_to_blt(bold_blt(item['botanical_morphology_stems'])) + '\n\n'
                article += f'### Leaves\n\n'
                article += lst_to_blt(bold_blt(item['botanical_morphology_leaves'])) + '\n\n'
                article += f'### Flowers\n\n'
                article += lst_to_blt(bold_blt(item['botanical_morphology_flowers'])) + '\n\n'
                article += f'### Fruits\n\n'
                article += lst_to_blt(bold_blt(item['botanical_morphology_fruits'])) + '\n\n'
                article += f'### Seeds\n\n'
                article += lst_to_blt(bold_blt(item['botanical_morphology_seeds'])) + '\n\n'

                
                #######################################################################################################
                # DISTRIBUTION
                #######################################################################################################
                article += f'## What is the geographic distribution of {latin_name}?\n\n'
                article += lst_to_blt(bold_blt(item['botanical_geographic_distribution'])) + '\n\n'

                #######################################################################################################
                # HABITAT TYPES
                #######################################################################################################
                article += f'## What are the habitat types for {latin_name}?\n\n'
                article += lst_to_blt(bold_blt(item['botanical_habitat_types'])) + '\n\n'

                #######################################################################################################
                # CLIMATE
                #######################################################################################################
                article += f'## What are the climate preferences of {latin_name}?\n\n'
                article += lst_to_blt(bold_blt(item['botanical_climate'])) + '\n\n'

                


                # GROWING ZONES
                # growing_zones = item['growing_zones']
                # gz_range = growing_zones.split('-')
                # gz_lst = [i for i in range(int(gz_range[0]), int(gz_range[1])+1)]
                # lst = []
                # for gz in gz_lst:
                #     for x in growing_zones_data:
                #         if x['zone'] == gz:
                #             zone = x['zone']
                #             temp_fahrenheit_from = x["temperature_from"]
                #             temp_fahrenheit_to = x["temperature_to"]
                #             temp_celsius_from = round((temp_fahrenheit_from - 32) * 5/9, 1)
                #             temp_celsius_to = round((temp_fahrenheit_to - 32) * 5/9, 1)
                #             lst.append(f'Zone {zone}: Minimum temperature of {temp_fahrenheit_from}°F to {temp_fahrenheit_to}°F ({temp_celsius_from}°C to {temp_celsius_to}°C)')
                #             break

                # article += f'### What are the growing zones for {most_common_name}?\n\n'
                # article += f'The best growing zones for {most_common_name} are **USDA Hardiness Zones {growing_zones}**.\n\n'
                # article += f'Here is a breakdown of these zones and their minimum temperatures.\n\n'
                # bld = bold_blt(lst)
                # article += lst_to_blt(bld)
                # article += '\n\n'
                

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

            elif 'morphology' in attribute.lower():
                #######################################################################################################
                # MORPHOLOGY
                #######################################################################################################
                title = f'What is the morphology of {latin_name}?'
                article += f'# {title}\n\n'

                featured_image_filpath = generate_featured_image(entity, attribute)
                article += f'![alt]({featured_image_filpath} "title")\n\n'
                article += '\n\n'.join([x for x in item['botanical_morphology_intro']]) + '\n\n'

                article += f'## {latin_name} roots morphology\n\n'.title()
                article += '\n\n'.join(item['botanical_morphology_roots_intro']) + '\n\n'
                article += f'The full description of the {latin_name} root morphology is given in the following list.' + '\n\n'
                article += lst_to_blt(bold_blt(item['botanical_morphology_roots'])) + '\n\n'

                try:
                    intro = item['botanical_morphology_rhizomes_intro']
                    article += f'## {latin_name} rhizomes morphology\n\n'.title()
                    article += '\n\n'.join(intro) + '\n\n'
                    article += f'The full description of the {latin_name} rhizomes morphology is given in the following list.' + '\n\n'
                    article += lst_to_blt(bold_blt(item['botanical_morphology_rhizomes'])) + '\n\n'
                except: pass

                try:
                    intro = item['botanical_morphology_stems_intro']
                    article += f'## {latin_name} stems morphology\n\n'.title()
                    article += '\n\n'.join(intro) + '\n\n'
                    article += f'The full description of the {latin_name} stems morphology is given in the following list.' + '\n\n'
                    article += lst_to_blt(bold_blt(item['botanical_morphology_stems'])) + '\n\n'
                except: pass
                
                try:
                    intro = item['botanical_morphology_leaves_intro']
                    article += f'## {latin_name} leaves morphology\n\n'.title()
                    article += '\n\n'.join(intro) + '\n\n'
                    article += f'The full description of the {latin_name} leaves morphology is given in the following list.' + '\n\n'
                    article += lst_to_blt(bold_blt(item['botanical_morphology_leaves'])) + '\n\n'
                except: pass

                try:
                    intro = item['botanical_morphology_inflorescence_intro']
                    article += f'## {latin_name} inflorescence morphology\n\n'.title()
                    article += '\n\n'.join(intro) + '\n\n'
                    article += f'The full description of the {latin_name} inflorescence morphology is given in the following list.' + '\n\n'
                    article += lst_to_blt(bold_blt(item['botanical_morphology_inflorescence'])) + '\n\n'
                except: pass
                
                # try:
                #     intro = item['botanical_morphology_spadix_intro']
                #     article += f'## spadix morphology\n\n'.title()
                #     article += '\n\n'.join(intro) + '\n\n'
                #     article += f'The full description of the {latin_name} spadix morphology is given in the following list.' + '\n\n'
                #     article += lst_to_blt(bold_blt(item['botanical_morphology_spadix'])) + '\n\n'
                # except: pass
                
                # try:
                #     intro = item['botanical_morphology_spathe_intro']
                #     article += f'## spathe morphology\n\n'.title()
                #     article += '\n\n'.join(intro) + '\n\n'
                #     article += f'The full description of the {latin_name} spathe morphology is given in the following list.' + '\n\n'
                #     article += lst_to_blt(bold_blt(item['botanical_morphology_spathe'])) + '\n\n'
                # except: pass
                
                try:
                    intro = item['botanical_morphology_flowers_intro']
                    article += f'## {latin_name} flowers morphology\n\n'.title()
                    article += '\n\n'.join(intro) + '\n\n'
                    article += f'The full description of the {latin_name} flowers morphology is given in the following list.' + '\n\n'
                    article += lst_to_blt(bold_blt(item['botanical_morphology_flowers'])) + '\n\n'
                except: pass
                
                article += f'## {latin_name} fruits morphology\n\n'.title()
                article += '\n\n'.join(item['botanical_morphology_fruits_intro']) + '\n\n'
                article += f'The full description of the {latin_name} fruits morphology is given in the following list.' + '\n\n'
                article += lst_to_blt(bold_blt(item['botanical_morphology_fruits'])) + '\n\n'
                
                article += f'## {latin_name} seeds morphology\n\n'.title()
                article += '\n\n'.join(item['botanical_morphology_seeds_intro']) + '\n\n'
                article += f'The full description of the {latin_name} seeds morphology is given in the following list.' + '\n\n'
                article += lst_to_blt(bold_blt(item['botanical_morphology_seeds'])) + '\n\n'

            else:
                
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

        article_filepath = generate_html(article, entity, attribute)

        articles_home.append(
            {
                'img': featured_image_filpath,
                'url': article_filepath,
                'name': most_common_name.title(),
                'title': title,
            }
        )




        

        


##################################################################################################
# PLANTS PAGE
##################################################################################################
# taxonomy = {}

# for article in articles_home:
#     article_folders = article['url'].split('/')

#     full_path_curr = ''
#     for i in range(len(article_folders)-1):
#         folder_curr = article_folders[i]
#         folder_next = article_folders[i+1]

#         full_path_curr += f'{folder_curr}/'

#         if full_path_curr not in taxonomy: 
#             taxonomy[full_path_curr] = [folder_next]
#         else: 
#             if folder_next not in taxonomy[full_path_curr]:
#                 taxonomy[full_path_curr].append(folder_next)

# for key, lst in taxonomy.items():
#     for val in lst:
#         if not os.path.exists(f'website/{key}/index.html'):
#             with open(f'website/{key}/index.html', 'w') as f:
#                 f.write(f'<p><a href="{val}">{val}</a></p>')
#         else: 
#             with open(f'website/{key}/index.html', 'a') as f:
#                 f.write(f'<p><a href="{val}">{val}</a></p>')





##################################################################################################
# HOME PAGE
##################################################################################################


# articles = ''
# for article in articles_home:
#     img = article['img']
#     url = article['url']
#     title = article['title']
#     name = article['name']
#     articles += f'''
#         <div class="flex gap-32">
#             <div class="flex-1">
#                 <img src="{img}" alt="">
#             </div>
#             <div class="flex-1">
#                 <h2 class="mt-0">{title}</h2>
#                 <p>
#                     Lorem ipsum, dolor sit amet consectetur adipisicing elit. Porro beatae consequatur ad
#                     quod,
#                     accusamus numquam velit nisi sint. Rerum eaque animi, enim ipsam laborum rem vitae
#                     repellendus
#                     vero
#                     quod corporis.
#                 </p>
#                 <a
#                     href="{url}">{name} Guide</a>
#             </div>
#         </div>
#         \n
#     '''
    
articles = ''
for article in articles_home:
    img = article['img']
    url = article['url']
    title = article['title']
    name = article['name']
    articles += f'''
        <a href="{url}">
            <div>
                <img src="{img}" alt="">
                <h2 class="mt-0">{title}</h2>
            </div>
        </a>
        \n
    '''


with_sidebar = f'''
    <section class="mt-96">
        <div class="container-lg">
            <div class="flex gap-32">
                <div class="articles flex-3 flex flex-col gap-32">
                    
                    {articles}

                </div>
                <div class="sidebar flex-1">
                    <div class="flex-1">
                        here goes the sidebar
                    </div>
                </div>
            </div>
        </div>
    </section>
'''

header = generate_header()

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
        <section class="hero-section">
            <div class="container-lg h-full">
                {header}
                <div class="flex justify-center items-center h-90">
                    <h1 class="fg-white text-center"><span class="size-96">Your Botanical Guide</span><br><span
                            class="size-36 weight-400">to Plant Taxonomy, Morphology, and Sensory Characteristics</span>
                    </h1>
                </div>
            </div>
        </section>



        <section class="my-96">
            <div class="container-lg">
                    <div class="articles">
                        {articles}
                    </div>
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
# <div class="articles flex-3 flex flex-col gap-32">
#                         {articles}
#                     </div>

# 

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
shutil.copy2('articles-images/hero.jpg', 'website/assets/images/hero.jpg')