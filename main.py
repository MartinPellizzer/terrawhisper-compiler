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
TEST = False 
TEST_NUM = 1
if len(sys.argv) == 2:
    if sys.argv[1] == 'force':
        REGEN_ALL_FORCED = True
    if '-d' in sys.argv[1]:
        TEST = True
        TEST_NUM = int(sys.argv[1].split('d')[1])

website_img_path = 'website/images'
AUTHOR_NAME = 'Leen Randell'

# vars
lst_line_height = 40

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


# PATHS
ARTICLES_CSV = 'articles.csv'
image_folder = 'C:/tw-images/auto'
image_folder_old = 'C:/tw-images/website'


# INITS
articles = utils.csv_to_llst(ARTICLES_CSV)

# index col with dict
articles_dict = {}
for i, item in enumerate(articles[0]):
    articles_dict[item] = i

articles = articles[1:]



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



def img_resize(img):
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


def generate_featured_image(entity, common_name, attribute_lst, filename):
    img = Image.open(f'{image_folder}/{entity}/4x3/{filename}')
    img = img_resize(img)

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

    attributes = '-'.join(attribute_lst).lower()
    if attributes != '': attributes += '-'
    featured_image_filpath = f'website/images/{entity}-{attributes}introduction.jpg'
    # img.save(f'{featured_image_filpath}', format='JPEG', subsampling=0, quality=100)
    img.save(f'{featured_image_filpath}', format='JPEG', optimize=True, quality=50)
    featured_image_filpath = f'/images/{entity}-{attributes}introduction.jpg'

    return featured_image_filpath


def gen_img_lst(entity, common_name, image_filepath, attributes, subtitle, lst):
    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    # background
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
    subtitle = subtitle.split('(')[0]
    subtitle_w = font.getbbox(subtitle)[2]
    if subtitle_w > 475:
        character_len = len(subtitle)
        font_size = 800 // character_len
        font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
        subtitle_w = font.getbbox(subtitle)[2]

    if title_w > subtitle_w: divider_w = title_w
    else: divider_w = subtitle_w
    draw.rectangle(((50, 50 + line_h + 10), (50 + divider_w, 50 + line_h + 10 + 2)), '#ffffff')
    current_y += 50 + line_h + 10 + 2
    
    # Subtitle
    line = subtitle
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 10), line, '#ffffff', font=font)
    current_y += 50 + line_h


    # List
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    max_len = 0
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    for item in lst:
        line_w = font.getbbox(item)[2]
        if max_len < line_w: max_len = line_w
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
    for i, line in enumerate(lst):
        line = line.split('(')[0]
        draw.text((50, current_y + 10 + line_h * line_spacing * i), line, '#ffffff', font=font)
    current_y += 10 + line_h * line_spacing * i + line_h

    # copyright
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    draw.text((50, img_h - 50 - line_h), 'TerraWhisper.com', '#ffffff', font=font)

    img.thumbnail((768, 576), Image.Resampling.LANCZOS)

    # export
    attributes = attributes.lower().replace(' ', '-').replace('/', '-')
    out_filename = f'website/images/{entity}-{attributes}.jpg'
    img.save(out_filename, format='JPEG', optimize=True, quality=50)
    filepath = f'images/{entity}-{attributes}.jpg'

    # print(out_filename)
    # print(filepath)
    # quit()

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
                    <nav class="flex gap-16">
                        <a class="text-stone-700" href="/plants.html">All Plants</a>
                        <a class="text-stone-700" href="/about.html">About</a>
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


def generate_html(title, article, entity, attribute_lst):
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
            <meta name="author" content="{AUTHOR_NAME}">
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
                        <span>by {AUTHOR_NAME}</span>
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
    # - <time datetime="{date.replace("/", "-")}">{date}</time>

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

shutil.copy2('style.css', 'website/style.css')
# shutil.copy2('articles-images/hero.jpg', f'{website_img_path}/hero.jpg')
# shutil.copy2('articles-images/medicinal-plants.jpg', f'{website_img_path}/medicinal-plants.jpg')
shutil.copy2('assets/images/medicinal-plants.jpg', f'{website_img_path}/medicinal-plants.jpg')
shutil.copy2('assets/images/leen-randell-profile-picture.jpg', f'{website_img_path}/leen-randell-profile-picture.jpg')
shutil.copy2('assets/images/leen-garden-medicinal-plants.jpg', f'{website_img_path}/leen-garden-medicinal-plants.jpg')



articles_home = []


for i, row in enumerate(articles):
    if TEST:
        if i >= TEST_NUM: break
    # print(f'{i+1}/{len(articles_master_rows[1:])} - {row}')

    entity = row[articles_dict['entity']].strip()
    common_name = row[articles_dict['common_name']].strip()
    latin_name = entity.replace('-', ' ').capitalize()

    root = row[articles_dict['root']].strip()
    medicine = row[articles_dict['medicine']].strip()
    medicine_benefits = row[articles_dict['medicine_benefits']].strip()
    medicine_preparations = row[articles_dict['medicine_preparations']].strip()

    try: os.mkdir(f'articles/{entity}')
    except: pass
    try: os.mkdir(f'articles/{entity}/medicine')
    except: pass
    try: os.mkdir(f'website/{entity}')
    except: pass
    try: os.mkdir(f'website/{entity}/medicine')
    except: pass

    article = ''
    featured_image_filpath = ''

    print(row)
    # root
    if root != '':
        article = ''
        attributes = ''

        # intro
        title = f'What to know before using {common_name} ({latin_name.capitalize()})'.title()
        article += f'<h1>{title}</h1>'
        
        attribute_lst = []
        image_title = f'{latin_name.title()} Overview'
        featured_image_filepath = generate_featured_image(
            entity, 
            common_name, 
            attribute_lst, 
            '0000.jpg')
        article += f'![{image_title}]({featured_image_filepath} "{image_title}")\n\n'



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

        _rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        lst = [_row[1] for _row in _rows]
        image_filename = images_filenames.pop()
        filepath = gen_img_lst(
            entity, 
            common_name, 
            image_filepath=f'{image_folder}/{entity}/3x4/{image_filename}', 
            attributes=section, 
            subtitle=section.title().replace('-', ' '), 
            lst=lst,
        )

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

        _rows = utils.csv_get_rows_by_entity(f'database/tables/cuisine.csv', entity)
        lst = [_row[1] for _row in _rows]
        image_filename = images_filenames.pop()
        filepath = gen_img_lst(
            entity, 
            common_name, 
            image_filepath=f'{image_folder}/{entity}/3x4/{image_filename}', 
            attributes=section, 
            subtitle=section.title().replace('-', ' '), 
            lst=lst,
        )

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

        _rows = utils.csv_get_rows_by_entity(f'database/tables/horticulture.csv', entity)
        lst = [_row[1] for _row in _rows]
        image_filename = images_filenames.pop()
        filepath = gen_img_lst(
            entity, 
            common_name, 
            image_filepath=f'{image_folder}/{entity}/3x4/{image_filename}', 
            attributes=section, 
            subtitle=section.title().replace('-', ' '), 
            lst=lst,
        )

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

        filepath = gen_img_lst(
            entity, 
            common_name, 
            image_filepath=f'{image_folder}/{entity}/3x4/{image_filename}', 
            attributes=section, 
            subtitle='Taxonomy', 
            lst=taxonomy_rows[1:],
        )

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

        _rows = utils.csv_get_rows_by_entity(f'database/tables/history.csv', entity)
        lst = [_row[1] for _row in _rows]
        image_filename = images_filenames.pop()
        filepath = gen_img_lst(
            entity, 
            common_name, 
            image_filepath=f'{image_folder}/{entity}/3x4/{image_filename}', 
            attributes=section, 
            subtitle=section.title().replace('-', ' '), 
            lst=lst,
        )

        section_title = f'What are the historical uses of {common_name}?'
        image_intro = f'The following illustration lists the most well known historical uses of {common_name}.'
        
        article += f'<h2>{section_title.title()}</h2>'
        article += f'<p>{paragraph_1}</p>'
        article += f'<p>{image_intro}</p>'
        article += f'<img src="images/{entity}-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        for paragraph in paragraph_rest:
            article += f'<p>{paragraph}</p>'
            
        article = article.replace('’', "'") 
        article = article.replace('..', ".") 

        attribute_lst = [x for x in attributes.split('/')]
        article_filepath = generate_html(title, article, entity, attribute_lst)
  
  
    # medicine
    if medicine != '':
        article = ''
        attributes = 'medicine'

        title = f'{common_name.capitalize()} ({latin_name.capitalize()}) Medicinal Guide: Benefits, Constituents, and Preparations'
        article += f'# {title}\n\n'
        
        attribute_lst = ['medicine']
        image_title = f'{latin_name.title()} Medicinal Guide'
        featured_image_filepath = generate_featured_image(
            entity, 
            common_name, 
            attribute_lst, 
            '0001.jpg',
        )
        article += f'![{image_title}]({featured_image_filepath} "{image_title}")\n\n'
        
        with open(f'database/articles/{entity}/intro.md', encoding='utf-8') as f: 
            content = f.read()

        article += content
        article += f'This article explains in details the medicinal properties of {common_name} and how to use this plant to boost your health.' + '\n\n'

        images_filenames = os.listdir(f'{image_folder}/{entity}/3x4')
        random.shuffle(images_filenames)

        # ----------------------------------------------------------
        section = 'benefits'
        with open(f'database/articles/{entity}/medicine/{section}.md', encoding='utf-8') as f: content = f.read()
        content_paragraphs = content.split('\n')
        content_paragraphs = [x for x in content_paragraphs if x.strip() != '']
        
        paragraph_1 = content_paragraphs[0]
        paragraph_rest = content_paragraphs[1:]

        _rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        lst = [_row[1] for _row in _rows]
                    
        image_filename = images_filenames.pop()
        filepath = gen_img_lst(
            entity, 
            common_name, 
            image_filepath=f'{image_folder}/{entity}/3x4/{image_filename}', 
            attributes=f'medicine/{section}', 
            subtitle=section.title().replace('-', ' '), 
            lst=lst,
        )

        section_title = f'What are the health benefits and medicinal properties of {common_name}?'
        image_intro = f'The following illustration shows the most important health benefits of {common_name}.'
        
        article += f'<h2>{section_title.title()}</h2>'
        article += f'<p>{paragraph_1}</p>'
        article += f'<p>{image_intro}</p>'
        article += f'<img src="/images/{entity}-medicine-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        for paragraph in paragraph_rest:
            article += f'<p>{paragraph}</p>'

        # ----------------------------------------------------------
        section = 'constituents'
        with open(f'database/articles/{entity}/medicine/{section}.md', encoding='utf-8') as f: content = f.read()
        content_paragraphs = content.split('\n')
        content_paragraphs = [x for x in content_paragraphs if x.strip() != '']
        
        paragraph_1 = content_paragraphs[0]
        paragraph_rest = content_paragraphs[1:]

        image_filename = images_filenames.pop()
        filepath = gen_img_lst(
            entity, 
            common_name, 
            image_filepath=f'{image_folder}/{entity}/3x4/{image_filename}', 
            attributes=f'medicine/{section}', 
            subtitle=section.title().replace('-', ' '), 
            lst=lst,
        )

        section_title = f'What are the key constituents of {common_name} for health purposes?'
        image_intro = f'The following illustration shows the most important active constituents of {common_name} for medicinal purposes.'
        
        article += f'<h2>{section_title.title()}</h2>'
        article += f'<p>{paragraph_1}</p>'
        article += f'<p>{image_intro}</p>'
        article += f'<img src="/images/{entity}-medicine-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        for paragraph in paragraph_rest:
            article += f'<p>{paragraph}</p>'

        # ----------------------------------------------------------
        section = 'preparations'
        with open(f'database/articles/{entity}/medicine/{section}.md', encoding='utf-8') as f: content = f.read()
        content_paragraphs = content.split('\n')
        content_paragraphs = [x for x in content_paragraphs if x.strip() != '']
        
        paragraph_1 = content_paragraphs[0]
        paragraph_rest = content_paragraphs[1:]

        image_filename = images_filenames.pop()
        filepath = gen_img_lst(
            entity, 
            common_name, 
            image_filepath=f'{image_folder}/{entity}/3x4/{image_filename}', 
            attributes=f'medicine/{section}', 
            subtitle=section.title().replace('-', ' '), 
            lst=lst,
        )

        section_title = f'What are the medicinal preparations of {common_name} for health purposes?'
        image_intro = f'The following illustration shows the most important medicinal preparations of {common_name}.'
        
        article += f'<h2>{section_title.title()}</h2>'
        article += f'<p>{paragraph_1}</p>'
        article += f'<p>{image_intro}</p>'
        article += f'<img src="/images/{entity}-medicine-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        for paragraph in paragraph_rest:
            article += f'<p>{paragraph}</p>'

        # ----------------------------------------------------------
        section = 'side-effects'
        with open(f'database/articles/{entity}/medicine/{section}.md', encoding='utf-8') as f: content = f.read()
        content_paragraphs = content.split('\n')
        content_paragraphs = [x for x in content_paragraphs if x.strip() != '']
        
        paragraph_1 = content_paragraphs[0]
        paragraph_rest = content_paragraphs[1:]

        image_filename = images_filenames.pop()
        filepath = gen_img_lst(
            entity, 
            common_name, 
            image_filepath=f'{image_folder}/{entity}/3x4/{image_filename}', 
            attributes=f'medicine/{section}', 
            subtitle=section.title().replace('-', ' '), 
            lst=lst,
        )

        section_title = f'What are the possible health side effects of {common_name}?'
        image_intro = f'The following illustration shows some possible health side effects of {common_name}.'
        
        article += f'<h2>{section_title.title()}</h2>'
        article += f'<p>{paragraph_1}</p>'
        article += f'<p>{image_intro}</p>'
        article += f'<img src="/images/{entity}-medicine-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        for paragraph in paragraph_rest:
            article += f'<p>{paragraph}</p>'

        # ----------------------------------------------------------
        section = 'precautions'
        with open(f'database/articles/{entity}/medicine/{section}.md', encoding='utf-8') as f: content = f.read()
        content_paragraphs = content.split('\n')
        content_paragraphs = [x for x in content_paragraphs if x.strip() != '']
        
        paragraph_1 = content_paragraphs[0]
        paragraph_rest = content_paragraphs[1:]

        image_filename = images_filenames.pop()
        filepath = gen_img_lst(
            entity, 
            common_name, 
            image_filepath=f'{image_folder}/{entity}/3x4/{image_filename}', 
            attributes=f'medicine/{section}', 
            subtitle=section.title().replace('-', ' '), 
            lst=lst,
        )

        section_title = f'What precautions should you take when using {common_name} as a medicine?'
        image_intro = f'The following illustration shows the most important precautions you must take when you use {common_name} as a medicine.'
        
        article += f'<h2>{section_title.title()}</h2>'
        article += f'<p>{paragraph_1}</p>'
        article += f'<p>{image_intro}</p>'
        article += f'<img src="/images/{entity}-medicine-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        for paragraph in paragraph_rest:
            article += f'<p>{paragraph}</p>'

        article = article.replace('’', "'") 
        article = article.replace('..', ".") 

        attribute_lst = [x for x in attributes.split('/')]
        article_filepath = generate_html(title, article, entity, attribute_lst)
            

    # medicine >> benefits
    if medicine_benefits != '':
        article = ''
        attributes = 'medicine/benefits'

        title = f'10 Health Benefits of {common_name.capitalize()} ({latin_name.capitalize()})'
        article += f'# {title}\n\n'

        attribute_lst = ['medicine', 'benefits']
        try:
            image_title = f'{common_name.capitalize()}\'s Medicinal Benefits'
            featured_image_filepath = generate_featured_image(
                entity, 
                common_name, 
                attribute_lst, 
                '0002.jpg'
            )
            article += f'![{image_title}]({featured_image_filepath} "{image_title}")\n\n'
        except: 
            pass

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
                filepath = gen_img_lst(
                    entity, 
                    common_name, 
                    f'{image_folder}/{entity}/3x4/{image_filename}', 
                    f'{benefit}', 
                    benefit, 
                    data_conditions_lst,
                )
            except:
                print(f'Missing Image: {entity} {benefit}') 
                filepath = ''

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

        article = article.replace('’', "'") 
        article = article.replace('..', ".") 

        attribute_lst = [x for x in attributes.split('/')]
        article_filepath = generate_html(title, article, entity, attribute_lst)
            

    # medicine >> preparations
    if medicine_preparations != '':
        article = ''
        attributes = 'medicine/preparations'

        title = f'10 Medicinal Preparations of {common_name.capitalize()} ({latin_name.capitalize()})'
        article += f'# {title}\n\n'
        
        attribute_lst = ['medicine', 'preparations']
        image_title = f'{common_name.capitalize()}\'s Medicinal Preparations'
        try:
            featured_image_filepath = generate_featured_image(
                entity, 
                common_name, 
                attribute_lst, 
                '0003.jpg'
            )
        except: pass
        article += f'![{image_title}]({featured_image_filepath} "{image_title}")\n\n'

        article += get_content('medicine/preparations/_intro', f'database/articles/{entity}')
        article += f'This article explains in details the most important and well recognized medicinal preparations of {common_name}.' + '\n\n'

        preparations = utils.csv_get_rows_by_entity(f'database/tables/medicine/preparations.csv', entity)
        preparations = [f'{x[1]}' for x in preparations]

        images_filenames = os.listdir(f'{image_folder}/{entity}/3x4')
        random.shuffle(images_filenames)

        for img_num, preparation in enumerate(preparations):
            data_title = f'## {img_num+1}. {common_name.title()} {preparation.title()}'
            
            data_definition = ''
            _rows = utils.csv_get_rows_by_entity(f'database/articles/{entity}/medicine/preparations/definitions.csv', entity)
            for _row in _rows:
                if _row[1] == preparation:
                    data_definition = _row[2]

            data_conditions_lst = [] 
            _rows = utils.csv_get_rows_by_entity(f'database/articles/{entity}/medicine/preparations/conditions_list.csv', entity)
            for _row in _rows:
                if _row[1] == preparation:
                    data_conditions_lst.append(_row[2])

            data_conditions_text = ''
            _rows = utils.csv_get_rows_by_entity(f'database/articles/{entity}/medicine/preparations/conditions_text.csv', entity)
            for _row in _rows:
                if _row[1] == preparation:
                    data_conditions_text = _row[2]

            image_filename = images_filenames.pop()
            filepath = gen_img_lst(
                entity, 
                common_name, 
                f'{image_folder}/{entity}/3x4/{image_filename}', 
                preparation, 
                preparation, 
                data_conditions_lst,
            )
            image_title = f'{common_name.title()} {item.title()}'
            image_section = f'![{image_title}](/{filepath} "{image_title}")'

            article += data_title + '\n\n'
            article += data_definition + '\n\n'

            article += f'The illustration below summarize some common health conditions that benefits from {latin_name} {preparation}.' + '\n\n'
            article += image_section + '\n\n'

            article += f'The following list includes the main conditions that {common_name} {preparation} helps to heal.' + '\n\n'
            article += lst_to_blt(data_conditions_lst) + '\n\n'
            
            article += data_conditions_text + '\n\n'

        article = article.replace('’', "'") 
        article = article.replace('..', ".") 

        attribute_lst = [x for x in attributes.split('/')]
        article_filepath = generate_html(title, article, entity, attribute_lst)






##################################################################################################
# ALL PLANTS PAGE
##################################################################################################

all_plants_grid = []
for i, plant_row in enumerate(articles):
    if TEST:
        if i >= TEST_NUM: break

    print(f'{i+1}/{len(articles[1:])} - {plant_row}')
    entity = plant_row[articles_dict['entity']].strip()
    common_name = plant_row[articles_dict['common_name']].strip().lower()
    latin_name = entity.capitalize().replace('-', ' ')

    root = plant_row[articles_dict['root']].strip().lower()

    if root == '': continue

    if os.path.exists(f'website/{entity}.html'):
        all_plants_grid.append(
            [
                entity,
                common_name,
                latin_name,
                f'images/{entity}-introduction.jpg',
            ]
        )

articles_html = ''
for home_article in all_plants_grid:
    title = f'{home_article[1]} ({home_article[2]}) Guide'.title()
    articles_html += f'''
        <div>
            <img src="{home_article[3]}">
            <h2 class="grid-articles-title"><a href="{home_article[0]}.html">{title}</a></h2>
        </div>
    '''

html = f'''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="author" content="{AUTHOR_NAME}">
        <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042" />
        <link rel="stylesheet" href="style.css">
        <title>All Plant | TerraWhisper</title>
        {google_tag}
    </head>

    <body>
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

        <section class="container-lg mt-96 grid gap-48 grid-3">
            {articles_html}
        </section>

        
        <footer>
            <div class="container-lg">
                <span>© TerraWhisper.com 2023 | All Rights Reserved
            </div>
        </footer>
    </body>
    

    </html>
'''

with open(f'website/plants.html', 'w', encoding='utf-8') as f:
    f.write(html)


##################################################################################################
# HOME PAGE
##################################################################################################


articles_home_benefits_html = ''
articles_home_preparations_html = ''
for i, article in enumerate(articles):
    if TEST:
        if i >= TEST_NUM: break
    entity = article[articles_dict['entity']]
    common_name = article[articles_dict['common_name']]
    latin_name = entity.replace('-', ' ').capitalize()
    
    medicine_benefits = article[articles_dict['medicine_benefits']]
    medicine_preparations = article[articles_dict['medicine_preparations']]

    if medicine_benefits != '':
        print(article)
        img = f'images/{entity}-medicine-benefits-introduction.jpg'
        url = f'{entity}/medicine/benefits.html'
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
        
    if medicine_preparations != '':
        print(article)
        img = f'images/{entity}-medicine-preparations-introduction.jpg'
        url = f'{entity}/medicine/preparations.html'
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
        <meta name="author" content="{AUTHOR_NAME}">
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

with open(f'website/index.html', 'w', encoding='utf-8') as f:
    f.write(html)


##################################################################################################
# ABOUT
##################################################################################################
with open(f'static/about.md', 'r', encoding='utf-8') as f:
    article = f.read()


article_html = markdown.markdown(article, extensions=['markdown.extensions.tables'])

header = generate_header_light()
html = f'''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="author" content="{AUTHOR_NAME}">
        <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042" />
        <link rel="stylesheet" href="style.css">
        <title>TerraWhisper | About</title>
        {google_tag}

    </head>

    <body>
        {header}

        <section class="my-96">
            <div class="container-lg flex gap-96">
                <div class="flex-2">
                    {article_html}
                </div>
                <div class="flex-1">
                    <div class="profile-box">
                        <img class="profile-pic mb-16" src="/images/leen-randell-profile-picture.jpg">
                        <p class="profile-name text-center">Leen Randell</p>
                        <p class="text-center mb-0">Herbalist, Botanist, Biologist, Scientist, and Self-Proclaimed Alchemist - Lover of Nature, Plants, and Chickens 🐣</p>
                    </div>
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
# <p class="text-center mb-0">Herbalist, Botanist, and Self-Proclaimed Alchemist. Lover of Seas, Skyes, and Everything in Between.</p>


with open(f'website/about.html', 'w', encoding='utf-8') as f:
    f.write(html)

quit()

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
        <meta name="author" content="{AUTHOR_NAME}">
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
shutil.copy2('assets/images/medicinal-plants.jpg', f'{website_img_path}/medicinal-plants.jpg')