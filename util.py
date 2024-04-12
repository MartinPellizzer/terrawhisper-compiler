import os
import csv
import json
import random
import datetime
from PIL import Image, ImageColor, ImageEnhance

import g



def create_folder_for_filepath(filepath):
    chunks = filepath.split('/')
    chunk_curr = ''
    for chunk in chunks[:-1]:
        chunk_curr += chunk + '/'
        try: os.makedirs(chunk_curr)
        except: pass


###################################
# CSV
###################################

def csv_get_rows(filepath, delimiter='\\'):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, line in enumerate(reader):
            rows.append(line)
    return rows


def csv_add_rows(filepath, rows, delimiter='\\'):
    with open(filepath, 'a', encoding='utf-8', errors='ignore', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(rows)


def csv_set_rows(filepath, rows, delimiter='\\'):
    with open(filepath, 'w', encoding='utf-8', errors='ignore', newline='') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(rows)
        

def csv_get_rows_by_entity(filepath, entity, delimiter='\\', num_col=0):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, line in enumerate(reader):
            if line[num_col].lower().strip() == entity.lower().strip():
                rows.append(line)
    return rows


def folder_create(path):
    if not os.path.exists(path): os.makedirs(path)


def csv_get_header_dict(rows):
    cols = {}
    for i, val in enumerate(rows[0]):
        cols[val] = i
    return cols





###################################
# FILE
###################################

def file_read(filepath):
    with open(filepath, 'a', encoding='utf-8') as f: pass
    with open(filepath, 'r', encoding='utf-8') as f: 
        text = f.read()
    return text


def file_append(filepath, text):
    with open(filepath, 'a', encoding='utf-8') as f: 
        f.write(text)


def file_write(filepath, text):
    create_folder_for_filepath(filepath)
    with open(filepath, 'w', encoding='utf-8') as f: f.write(text)





###################################
# JSON
###################################

def json_generate_if_not_exists(filepath):
    if not os.path.exists(filepath):
        file_append(filepath, '')

    if file_read(filepath).strip() == '':
        file_append(filepath, '{}')


def json_append(filepath, data):
    with open(filepath, 'a', encoding='utf-8') as f:
        json.dump(data, f)


def json_read(filepath):
    # if not os.path.exists(filepath):
    #     file_append(filepath, '')

    # if file_read(filepath).strip() == '':
    #     file_append(filepath, '{}')
    
    with open(filepath, 'r', encoding='utf-8') as f: 
        return json.load(f)


def json_write(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f)





###################################
# FORMAT
###################################

def text_format_131(text):
    text_formatted = ''
    lines = text.split('. ')
    line_0 = lines[0]
    line_1 = '. '.join(lines[1:-1])
    line_2 = lines[-1]
    text_formatted += f'{line_0}.\n\n'
    text_formatted += f'{line_1}.\n\n'
    text_formatted += f'{line_2}.\n\n'
    text_formatted = text_formatted.replace('..', '.')
    return text_formatted

    
def text_format_131_html(text):
    text_formatted = ''
    lines = text.split('. ')
    line_0 = lines[0]
    line_1 = '. '.join(lines[1:-1])
    line_2 = lines[-1]
    text_formatted += f'<p>{line_0}.</p>' + '\n'
    text_formatted += f'<p>{line_1}.</p>' + '\n'
    text_formatted += f'<p>{line_2}.</p>' + '\n'
    text_formatted = text_formatted.replace('..', '.')
    return text_formatted


def text_format_1N1_html(text):
    text_formatted = ''
    lines = text.split('. ')
    lines_num = len(lines[1:-1])
    paragraphs = []
    paragraphs.append(lines[0])
    if lines_num > 3: 
        paragraphs.append('. '.join(lines[1:lines_num//2+1]))
        paragraphs.append('. '.join(lines[lines_num//2+1:-1]))
    else:
        paragraphs.append('. '.join(lines[1:-1]))
    paragraphs.append(lines[-1])
    for paragraph in paragraphs:
        text_formatted += f'<p>{paragraph}.</p>' + '\n'
    text_formatted = text_formatted.replace('..', '.')
    return text_formatted


def lst_to_html(lst):
    lst_html = '<ul>' + '\n'
    for item in lst: lst_html += f'<li>{item}</li>' + '\n'
    lst_html += '</ul>' + '\n'
    return lst_html





###################################
# DATE
###################################


def date_now():
    return str(datetime.date.today())




###################################
# SCIENTIFIC NAME
###################################

def get_scientific_name(common_name, delimiter='\\'):
    rows = csv_get_rows('plants.csv', delimiter=delimiter)
    rows = [
        row 
        for row in rows 
        if row[1].lower().strip().replace(' ', '-') == common_name.lower().strip().replace(' ', '-')]
    scientific_name = rows[0][0].replace('-', ' ')
    return scientific_name


def get_common_name(entity, delimiter='\\'):
    rows = csv_get_rows('plants.csv', delimiter=delimiter)
    rows = [
        row 
        for row in rows 
        if row[0].lower().strip().replace(' ', '-') == entity.lower().strip().replace(' ', '-')]
    name = rows[0][1].replace('-', ' ')
    return name





###################################
# IMAGES
###################################

def img_resize(img, w=768, h=578):
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


def image_variate(filepath_in, filepath_out):
    w, h = 1024, 1024
    
    image = Image.open(filepath_in)

    random_enhancer_val = random.uniform(0.9, 1.1)
    image_enhancer = ImageEnhance.Color(image)
    image = image_enhancer.enhance(random_enhancer_val)
    random_enhancer_val = random.uniform(0.9, 1.1)
    image_enhancer = ImageEnhance.Contrast(image)
    image = image_enhancer.enhance(random_enhancer_val)
    random_enhancer_val = random.uniform(0.9, 1.1)
    image_enhancer = ImageEnhance.Brightness(image)
    image = image_enhancer.enhance(random_enhancer_val)
    random_enhancer_val = random.uniform(0.9, 1.1)
    image_enhancer = ImageEnhance.Sharpness(image)
    image = image_enhancer.enhance(random_enhancer_val)


    random_val_x1 = random.randint(50, 100)
    random_val_y1 = random.randint(50, 100)
    random_val_x2 = random.randint(50, 100)
    random_val_y2 = random.randint(50, 100)
    image = image.crop((random_val_x1, random_val_y1, w-random_val_x2, h-random_val_y2))
    image = image.resize((w, h), Image.Resampling.LANCZOS)

    image.thumbnail((768, 768), Image.Resampling.LANCZOS)
    image.save(filepath_out, format='JPEG', optimize=True, quality=50)





###################################
# ARTICLES
###################################

def article_meta(content, date):
    reading_time = str(len(content.split(' ')) // 200) + ' minutes'
    return f'''
        <div class="flex items-center justify-between mb-16">
            <div class="flex items-center gap-16">
                <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
                <p>Last updated: Feb 14, 2018</p>
            </div>
            <span>{reading_time}</span>
        </div>
    '''

    
def header_base():
    return '''
        <header>
            <a class="text-white" href="/">TerraWhisper</a>
            <nav>
                <input type="checkbox" class="toggle-menu">
                <div class="hamburger"></div>
                <ul class="menu">
                    <li><a class="text-white" href="/">Home</a></li>
                    <li><a class="text-white" href="/start-here.html">Start Here</a></li>
                    <li><a class="text-white" href="/herbalism.html">Herbalism</a></li>
                    <li><a class="text-white" href="/conditions.html">Conditions</a></li>
                    <li><a class="text-white" href="/plants.html">Plants</a></li>
                    <li><a class="text-white" href="/about.html">About</a></li>
                </ul>
            </nav>
        </header>
    '''


def header_default():
    header_html = header_base()
    html = f'''
        <section class="header">
            <div class="container-lg">
                {header_html}
            </div>
        </section>
    '''
    return html


def header_transparent():
    header_html = header_base()
    html = f'''
        <section>
            <div class="container-lg">
                {header_html}
            </div>
        </section>
    '''
    return html


def article_toc(content_html):
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


def breadcrumbs(filepath):
    breadcrumbs = ['<a href="/">Home</a>']
    breadcrumbs_path = filepath.replace('website/', '')
    chunks = breadcrumbs_path.split('/')
    filepath_curr = ''
    for chunk in chunks[:-1]:
        filepath_curr += f'/{chunk}'
        chunk = chunk.strip().replace('-', ' ').title()
        breadcrumbs.append(f'<a href="{filepath_curr}.html">{chunk}</a>')
    breadcrumbs = ' > '.join(breadcrumbs)
    breadcrumbs += f' > {chunks[-1].strip().replace(".html", "").replace("-", " ").title()}'
    breadcrumbs_section = f'''
        <section class="container-lg mt-16">
            {breadcrumbs}
        </section>
    '''
    return breadcrumbs_section



