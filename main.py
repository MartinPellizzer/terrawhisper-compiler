import os
import markdown
import shutil
import random
import glob



from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

import g
import util
import sitemap






IMAGE_FOLDER = 'C:/terrawhisper-assets/images'



try: os.makedirs('website/images')
except: pass


plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]
cols = {}
for i, item in enumerate(plants[0]):
    cols[item] = i
plants = plants[1:g.ARTICLES_NUM+1]



##############################################################################
# IMAGES
##############################################################################
def thumbnail_save(filepath_in, filepath_out):
    img = Image.open(filepath_in)
    img.thumbnail((768, 768), Image.Resampling.LANCZOS)
    img.save(filepath_out, format='JPEG', optimize=True, quality=50)

##############################################################################
# UTIL
##############################################################################

def lst_to_html_bold(lst):
    lst_html = '<ul>'
    for item in lst:
        item = item.split(': ')
        item_name = f'<strong>{item[0]}</strong>'
        item_desc = ': '.join(item[1:])
        item = f'{item_name}: {item_desc}'
        lst_html += f'<li>{item}</li>'
    lst_html += '</ul>'
    return lst_html


def gen_article_metadata(article_content):
    reading_time_html = str(len(article_content.split(' ')) // 200) + ' minutes'
    return f'''
        <div class="flex items-center justify-between mb-16">
            <div class="flex items-center gap-16">
                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
            </div>
            <span>{reading_time_html}</span>
        </div>
    '''


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
    return breadcrumbs





##############################################################################
# BLOCKS
##############################################################################

def generate_header_base():
    html = '''
        <header>
            <a class="text-stone-700" href="/">TerraWhisper</a>
            <nav class="flex gap-32">
                <a class="text-stone-700" href="/herbalism.html">Herbalism</a>
                <a class="text-stone-700" href="/herbalism/tea.html">Teas</a>
                <a class="text-stone-700" href="/top-herbs.html">Top Herbs</a>
                <a class="text-stone-700" href="/about.html">About</a>
            </nav>
        </header>
    '''
    return html


def gen_header_base_new():
    return '''
        <header>
            <a class="text-neutral-700" href="/">TerraWhisper</a>
            <nav>
                <input type="checkbox" class="toggle-menu">
                <div class="hamburger-dark"></div>
                <ul class="menu">
                    <li><a class="text-neutral-700" href="/">Home</a></li>
                    <li><a class="text-neutral-700" href="/herbalism.html">Herbalism</a></li>
                    <li><a class="text-neutral-700" href="/herbalism/tea.html">Teas</a></li>
                    <li><a class="text-neutral-700" href="/top-herbs.html">Top Herbs</a></li>
                    <li><a class="text-neutral-700" href="/about.html">About</a></li>
                </ul>
            </nav>
        </header>
    '''

def generate_header_light():
    header_html = gen_header_base_new()
    html = f'''
        <section class="header-divider">
            <div class="container-lg">
                {header_html}
            </div>
        </section>
    '''
    return html


def generate_header_transparent():
    header_html = gen_header_base_new()
    html = f'''
        <section class="header-divider">
            {header_html}
        </section>
    '''
    html = html.replace('text-neutral-700', 'text-white')
    html = html.replace('hamburger-dark', 'hamburger-white')
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





##############################################################################
# SITE
##############################################################################

def home():
    header = generate_header_transparent()

    template = util.file_read('templates/home.html')
            
    template = template.replace('[meta_title]', 'Herbalism & Natural Healing')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)

    util.file_write(f'website/index.html', template)


def about():
    header = generate_header_light()
    content = util.file_read(f'static/about.md')
    content = markdown.markdown(content, extensions=['markdown.extensions.tables'])
    
    template = util.file_read('templates/about.html')

    template = template.replace('[meta_title]', 'TerraWhisper | About')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[content]', content)

    util.file_write(f'website/about.html', template)


def top_herbs():
    articles_folderpath = 'database/articles/plants'
    articles_html = ''

    plants_primary_a = []
    plants_primary_b = []
    plants_primary_c = []
    plants_primary_d = []
    plants_primary_e = []
    plants_primary_f = []
    plants_primary_g = []
    plants_primary_h = []
    plants_primary_i = []
    plants_primary_j = []
    plants_primary_k = []
    plants_primary_l = []
    plants_primary_m = []
    plants_primary_n = []
    plants_primary_o = []
    plants_primary_p = []
    plants_primary_q = []
    plants_primary_r = []
    plants_primary_s = []
    plants_primary_t = []
    plants_primary_u = []
    plants_primary_v = []
    plants_primary_w = []
    plants_primary_x = []
    plants_primary_y = []
    plants_primary_z = []

    for plant in plants:
        latin_name = plant[0].strip().capitalize()
        entity = latin_name.lower().replace(' ', '-')
        filepath_in = f'{articles_folderpath}/{entity}.json'
        data = util.json_read(filepath_in)

        title = data['title']
        common_name = data['common_name']

        article_html = f'''
            <a href="{entity}.html">
                <div>
                    <img src="/images/{entity}-overview.jpg" alt="">
                    <h3 class="mt-0 mb-0">{latin_name} ({common_name})</h3>
                </div>
            </a>
        '''

        if entity[0] == 'a': plants_primary_a.append(article_html)
        if entity[0] == 'b': plants_primary_b.append(article_html)
        if entity[0] == 'c': plants_primary_c.append(article_html)
        if entity[0] == 'd': plants_primary_d.append(article_html)
        if entity[0] == 'e': plants_primary_e.append(article_html)
        if entity[0] == 'f': plants_primary_f.append(article_html)
        if entity[0] == 'g': plants_primary_g.append(article_html)
        if entity[0] == 'h': plants_primary_h.append(article_html)
        if entity[0] == 'i': plants_primary_i.append(article_html)
        if entity[0] == 'j': plants_primary_j.append(article_html)
        if entity[0] == 'k': plants_primary_k.append(article_html)
        if entity[0] == 'l': plants_primary_l.append(article_html)
        if entity[0] == 'm': plants_primary_m.append(article_html)
        if entity[0] == 'n': plants_primary_n.append(article_html)
        if entity[0] == 'o': plants_primary_o.append(article_html)
        if entity[0] == 'p': plants_primary_p.append(article_html)
        if entity[0] == 'q': plants_primary_q.append(article_html)
        if entity[0] == 'r': plants_primary_r.append(article_html)
        if entity[0] == 's': plants_primary_s.append(article_html)
        if entity[0] == 't': plants_primary_t.append(article_html)
        if entity[0] == 'u': plants_primary_u.append(article_html)
        if entity[0] == 'v': plants_primary_v.append(article_html)
        if entity[0] == 'w': plants_primary_w.append(article_html)
        if entity[0] == 'x': plants_primary_x.append(article_html)
        if entity[0] == 'y': plants_primary_y.append(article_html)
        if entity[0] == 'z': plants_primary_z.append(article_html)

    if plants_primary_a != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "a"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_a) + '</div>'
    if plants_primary_b != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "b"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_b) + '</div>'
    if plants_primary_c != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "c"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_c) + '</div>'
    if plants_primary_d != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "d"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_d) + '</div>'
    if plants_primary_e != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "e"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_e) + '</div>'
    if plants_primary_f != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "f"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_f) + '</div>'
    if plants_primary_g != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "g"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_g) + '</div>'
    if plants_primary_h != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "h"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_h) + '</div>'
    if plants_primary_i != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "i"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_i) + '</div>'
    if plants_primary_j != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "j"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_j) + '</div>'
    if plants_primary_k != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "k"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_k) + '</div>'
    if plants_primary_l != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "l"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_l) + '</div>'
    if plants_primary_m != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "m"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_m) + '</div>'
    if plants_primary_n != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "n"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_n) + '</div>'
    if plants_primary_o != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "o"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_o) + '</div>'
    if plants_primary_p != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "p"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_p) + '</div>'
    if plants_primary_q != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "q"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_q) + '</div>'
    if plants_primary_r != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "r"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_r) + '</div>'
    if plants_primary_s != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "s"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_s) + '</div>'
    if plants_primary_t != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "t"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_t) + '</div>'
    if plants_primary_u != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "u"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_u) + '</div>'
    if plants_primary_v != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "v"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_v) + '</div>'
    if plants_primary_w != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "w"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_w) + '</div>'
    if plants_primary_x != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "x"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_x) + '</div>'
    if plants_primary_y != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "y"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_y) + '</div>'
    if plants_primary_z != []: articles_html += '<h2 class="articles-alphabeta-title">' + 'Plants Starting With Letter: "z"'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_primary_z) + '</div>'


    plants_secondary = []
    rows = [row for row in util.csv_get_rows('database/tables/plants-secondary.csv')[1:]]
    for plant in rows:
        latin_name = plant[0].strip().capitalize()
        entity = latin_name.lower().replace(' ', '-')
        filepath_in = f'{articles_folderpath}/{entity}.json'
        data = util.json_read(filepath_in)

        title = data['title']
        common_name = data['common_name']

                    # <img src="/images/{entity}.jpg" alt="">
        article_html = f'''
            <a href="{entity}.html">
                <div>
                    <h3 class="mt-0 mb-0">{latin_name} ({common_name})</h3>
                </div>
            </a>
        '''
        plants_secondary.append(article_html)

    articles_html += '<h2 class="articles-alphabeta-title">' + 'Other Medicinal Plants Worthy Of Notice'.title() + '</h2>\n' + '<div class="articles">' +'\n'.join(plants_secondary) + '</div>'




    page_url = 'top-herbs'

    header = generate_header_light()

    page_html = util.file_read(f'templates/{page_url}.html')

    page_html = page_html.replace('[meta_title]', 'Herbs')
    page_html = page_html.replace('[google_tag]', g.GOOGLE_TAG)
    page_html = page_html.replace('[author_name]', g.AUTHOR_NAME)
    page_html = page_html.replace('[header]', header)
    page_html = page_html.replace('[articles]', articles_html)

    util.file_write(f'website/{page_url}.html', page_html)


def teas():
    article_html = ''
    article_html += '<div class="articles">'

    articles_folderpath = 'database/articles/herbalism/tea'
    for article_filename in os.listdir(articles_folderpath):
        condition = article_filename.split('.')[0].strip()
        condition_dash = condition.lower().replace(' ', '-')
        article_filepath = f'{articles_folderpath}/{article_filename}'
        data = util.json_read(article_filepath)

        article_html += f'''
            <a href="/herbalism/tea/{condition_dash}.html">
                <div>
                    <img src="/images/herbal-tea-for-{condition_dash}-overview.jpg" alt="herbal tea for {condition} overview">
                    <h3 class="mt-0 mb-0">{condition}</h3>
                </div>
            </a>
        '''

    article_html += '</div>'

    page_url = 'herbalism/tea'

    header = generate_header_light()

    page_html = util.file_read(f'templates/{page_url}.html')

    page_html = page_html.replace('[meta_title]', 'Herbalism')
    page_html = page_html.replace('[google_tag]', g.GOOGLE_TAG)
    page_html = page_html.replace('[author_name]', g.AUTHOR_NAME)
    page_html = page_html.replace('[header]', header)
    page_html = page_html.replace('[articles]', article_html)

    util.file_write(f'website/{page_url}.html', page_html)





##############################################################################
# HERBALISM
##############################################################################

def herbalism():
    page_url = 'herbalism'

    header = generate_header_light()
    
    content = util.file_read(f'static/{page_url}.md')
    content = markdown.markdown(content, extensions=['markdown.extensions.tables'])

    meta = gen_article_metadata(content)
    content = generate_toc(content)

    page_html = util.file_read(f'static/{page_url}.html')

    page_html = page_html.replace('[meta_title]', 'Herbalism')
    page_html = page_html.replace('[google_tag]', g.GOOGLE_TAG)
    page_html = page_html.replace('[author_name]', g.AUTHOR_NAME)

    page_html = page_html.replace('[header]', header)
    page_html = page_html.replace('[meta]', meta)
    page_html = page_html.replace('[content]', content)

    util.file_write(f'website/{page_url}.html', page_html)

    # GET IMAGES
    folderpath = f'{IMAGE_FOLDER}/herbalism'
    if os.path.exists(folderpath): 
        filenames = os.listdir(folderpath)
        filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]

        filepaths_out = [
            f'website/images/herbalism-overview.jpg',
            f'website/images/herbalism-what-is.jpg',
            f'website/images/herbalism-health-conditions.jpg',
            f'website/images/herbalism-common-herbs.jpg',
            f'website/images/herbalism-active-constituents.jpg',
            f'website/images/herbalism-medicinal-preparations.jpg',
            f'website/images/herbalism-primary-tools.jpg',
        ]

        for i, filepath_out in enumerate(filepaths_out):
            if os.path.exists(filepath_out): continue
            filepath_in = filepaths_in[i]
            thumbnail_save(filepath_in, filepath_out)
    else:
        print('MISSING >>>>> IMAGE FOLDER -> HERBALISM')



# def herbalism_tea():
#     # IMAGES
#     IMG_FOLDER_TEA = 'C:/terrawhisper-assets/images/tea'
#     img_folders_names = os.listdir(IMG_FOLDER_TEA)
#     img_dict = {}
#     for img_folder_name in img_folders_names:
#         img_folders_files = os.listdir(f'{IMG_FOLDER_TEA}/{img_folder_name}')
#         img_dict[img_folder_name] = img_folders_files

    
#     articles_folderpath = 'database/articles/herbalism/tea'
#     article_foldrpath_relative = f'herbalism/tea'
#     article_foldrpath_relative_dash = article_foldrpath_relative.replace('/', '-')
#     conditions = [row[0] for row in util.csv_get_rows('database/tables/conditions.csv')[1:]]
#     for condition in conditions[:10]:
#         condition_dash = condition.lower().strip().replace(' ', '-')
#         article_filename = f'{articles_folderpath}/{condition_dash}.json'
        
#         article_filepath_in = article_filename
#         article_filepath_out = article_filename.replace('database/articles', 'website').replace('.json', '.html')

#         data = util.json_read(article_filepath_in)
#         article_html = ''

#         title = ''
#         try: title = data['keyword'].title()
#         except: print(f'***** MISSING TITLE: {article_filepath_in}')
#         article_html += f'<h1>{title}</h1>' + '\n'
#         article_html += f'<p><img src="/images/herbal-tea-for-{condition_dash}-overview.jpg" alt="herbal teas for {condition} overview"></p>' + '\n'

#         remedies = []
#         try: remedies = data['remedies']
#         except: print(f'***** MISSING REMEDIES: {article_filepath_in}')
#         for index, remedy in enumerate(remedies[:10]):
#             remedy_name = remedy['remedy_name']
#             remedy_desc = remedy['remedy_desc']
#             remedy_name_dash = remedy_name.lower().strip().replace(' ', '-')
#             remedy_desc_formatted = util.text_format_1N1_html(remedy_desc)
#             article_html += f'<h2>{index+1}. {remedy_name}</h2>' + '\n'
#             article_html += f'<p><img src="/images/herbal-tea-for-{condition_dash}-{remedy_name_dash}.jpg" alt="herbal teas for {condition} {remedy_name.lower()}"></p>' + '\n'
#             article_html += f'<p>{remedy_desc_formatted}</p>' + '\n'

#         header_html = generate_header_light()
#         word_count = len(article_html.split(' '))
#         reading_time_html = str(word_count // 200) + ' minutes'

#         article_html = generate_toc(article_html)

#         html = f'''
#             <!DOCTYPE html>
#             <html lang="en">

#             <head>
#                 <meta charset="UTF-8">
#                 <meta name="viewport" content="width=device-width, initial-scale=1.0">
#                 <meta name="author" content="{g.AUTHOR_NAME}">
#                 <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
#                 <link rel="stylesheet" href="/style.css">
#                 <title>{title}</title>
#                 {g.GOOGLE_TAG}
                
#             </head>

#             <body>
#                 {header_html}
                
#                 <section class="article-section">
#                     <div class="container">
#                         <div class="flex items-center justify-between mb-16">
#                             <div class="flex items-center gap-16">
#                                 <img class="author-image" src="/martin-pellizzer.jpg" alt="">
#                                 <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
#                             </div>
#                             <span>{reading_time_html}</span>
#                         </div>
#                         {article_html}
#                     </div>
#                 </section>

#                 <footer>
#                     <div class="container-lg">
#                         <span>© TerraWhisper.com 2024 | All Rights Reserved
#                     </div>
#                 </footer>
#             </body>

#             </html>
#         '''

#         chunks = article_filepath_out.split('/')
#         chunk_curr = ''
#         for chunk in chunks[:-1]:
#             chunk_curr += chunk + '/'
#             try: os.makedirs(chunk_curr)
#             except: pass
#         util.file_write(f'{article_filepath_out}', html)

#         # GET IMAGES
#         data = util.json_read(article_filepath_in)
#         # print(article_filepath_in)
#         condition = data['condition']
#         preparation = data['preparation']
#         condition_dash = condition.lower().strip().replace(' ', '-')
#         preparation_dash = preparation.lower().strip().replace(' ', '-')
#         herbs = [remedy['remedy_name'] for remedy in data['remedies']]
        
#         # FEATURED IMAGE
#         featured_image_folder = herbs[0].lower().strip().replace(' ', '-')
#         try: img_name = img_dict[featured_image_folder].pop(0)
#         except: img_name = ''
#         if img_name != '':
#             image_path_in = f'{IMAGE_FOLDER}/{preparation_dash}/{featured_image_folder}/{img_name}'
#             image_path_out = f'website/images/herbal-{preparation_dash}-for-{condition_dash}-overview' + '.jpg'
#             if not os.path.exists(image_path_out):
#                 img = Image.open(image_path_in)
#                 img.thumbnail((768, 768), Image.Resampling.LANCZOS)
#                 img.save(image_path_out, format='JPEG', optimize=True, quality=50)
#         else:
#             try: scientific_name = util.get_scientific_name(featured_image_folder)
#             except: scientific_name = ''
#             print(article_filepath_in)
#             print(featured_image_folder)
#             print(f'*** MISSING: {featured_image_folder} ({scientific_name}) {preparation_dash} ***')
#             print()

#         # SECTIONS IMAGES
#         for herb in herbs:
#             herb_dash = herb.strip().lower().replace(' ', '-')
#             try: img_name = img_dict[herb_dash].pop(0)
#             except: img_name = ''
#             if img_name != '':
#                 image_path_in = f'{IMAGE_FOLDER}/{preparation_dash}/{herb_dash}/{img_name}'
#                 image_path_out = f'website/images/herbal-tea-for-{condition_dash}-{herb_dash}' + '.jpg'
#                 if not os.path.exists(image_path_out):
#                     img = Image.open(image_path_in)
#                     img.thumbnail((768, 768), Image.Resampling.LANCZOS)
#                     img.save(image_path_out, format='JPEG', optimize=True, quality=50)
#             else:
#                 try: scientific_name = util.get_scientific_name(herb)
#                 except: scientific_name = ''
#                 print(article_filepath_in)
#                 print(f'*** MISSING: {herb_dash} ({scientific_name}) {preparation_dash} ***')
#                 print()


def herbalism_tea_condition():
    # IMAGES
    IMG_FOLDER_TEA = 'C:/terrawhisper-assets/images/tea'
    img_folders_names = os.listdir(IMG_FOLDER_TEA)
    img_dict = {}
    for img_folder_name in img_folders_names:
        img_folders_files = os.listdir(f'{IMG_FOLDER_TEA}/{img_folder_name}')
        img_dict[img_folder_name] = img_folders_files

    articles_folderpath = 'database/articles/herbalism/tea'
    article_foldrpath_relative = f'herbalism/tea'
    article_foldrpath_relative_dash = article_foldrpath_relative.replace('/', '-')
    conditions = [row[0] for row in util.csv_get_rows('database/tables/conditions.csv')[1:]]
    for condition in conditions:
        print(condition)
        condition_dash = condition.lower().strip().replace(' ', '-')
        article_filename = f'{articles_folderpath}/{condition_dash}.json'

        article_filepath_in = article_filename
        article_filepath_out = article_filename.replace('database/articles', 'website').replace('.json', '.html')

        data = util.json_read(article_filepath_in)
        article_html = ''

        title = ''
        try: title = data['title'].title()
        except: print(f'***** MISSING TITLE: {article_filepath_in}')
        article_html += f'<h1>{title}</h1>' + '\n'
        article_html += f'<p><img src="/images/herbal-tea-for-{condition_dash}-overview.jpg" alt="herbal teas for {condition} overview"></p>' + '\n'
        try: article_html += f'<p>{util.text_format_1N1_html(data["intro"])}</p>\n'
        except: print(f'***** MISSING INTRO: {article_filepath_in}')

        remedies = []
        try: remedies = data['remedies']
        except: print(f'***** MISSING REMEDIES: {article_filepath_in}')
        for index, remedy in enumerate(remedies[:10]):
            remedy_name = remedy['remedy_name']
            remedy_desc = remedy['remedy_desc']
            remedy_recipe = remedy['remedy_recipe']
            remedy_name_dash = remedy_name.lower().strip().replace(' ', '-')
            remedy_desc_formatted = util.text_format_1N1_html(remedy_desc)
            article_html += f'<h2>{index+1}. {remedy_name.title()}</h2>' + '\n'
            article_html += f'<p><img src="/images/herbal-tea-for-{condition_dash}-{remedy_name_dash}.jpg" alt="herbal teas for {condition} {remedy_name.lower()}"></p>' + '\n'
            article_html += f'<p>{remedy_desc_formatted}</p>' + '\n'
            article_html += f'<p>The following procedure explaing how to make {remedy_name.lower()} tea for {condition}.</p>'
            article_html += f'<ol>' + '\n'
            for item in remedy_recipe:
                article_html += f'<li>{item}</li>' + '\n'
            article_html += f'</ol>' + '\n'

        header_html = generate_header_light()

        
        meta = gen_article_metadata(article_html)
        article_html = generate_toc(article_html)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                
                <section class="article-section">
                    <div class="container">
                        {meta}
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''

        chunks = article_filepath_out.split('/')
        chunk_curr = ''
        for chunk in chunks[:-1]:
            chunk_curr += chunk + '/'
            try: os.makedirs(chunk_curr)
            except: pass
        util.file_write(f'{article_filepath_out}', html)

        # GET IMAGES
        data = util.json_read(article_filepath_in)
        condition = data['condition']
        preparation = data['preparation']
        condition_dash = condition.lower().strip().replace(' ', '-')
        preparation_dash = preparation.lower().strip().replace(' ', '-')
        herbs = [remedy['remedy_name'] for remedy in data['remedies']]
        
        # FEATURED IMAGE
        featured_image_folder = herbs[0].lower().strip().replace(' ', '-')
        try: img_name = random.choice(img_dict[featured_image_folder])
        except: img_name = ''
        if img_name != '':
            image_path_in = f'{IMAGE_FOLDER}/{preparation_dash}/{featured_image_folder}/{img_name}'
            image_path_out = f'website/images/herbal-{preparation_dash}-for-{condition_dash}-overview' + '.jpg'
            if not os.path.exists(image_path_out):
                util.image_variate(image_path_in, image_path_out)
        else:
            try: scientific_name = util.get_scientific_name(featured_image_folder)
            except: scientific_name = ''
            print(article_filepath_in)
            print(featured_image_folder)
            print(f'*** MISSING: {featured_image_folder} ({scientific_name}) {preparation_dash} ***')
            print()
            
        # SECTIONS IMAGES
        for herb in herbs:
            herb_dash = herb.strip().lower().replace(' ', '-')
            try: img_name = random.choice(img_dict[herb_dash])
            except: img_name = ''
            if img_name != '':
                image_path_in = f'{IMAGE_FOLDER}/{preparation_dash}/{herb_dash}/{img_name}'
                image_path_out = f'website/images/herbal-tea-for-{condition_dash}-{herb_dash}' + '.jpg'
                if not os.path.exists(image_path_out):
                    util.image_variate(image_path_in, image_path_out)
            else:
                try: scientific_name = util.get_scientific_name(herb)
                except: scientific_name = ''
                print(article_filepath_in)
                print(f'*** MISSING: {herb_dash} ({scientific_name}) {preparation_dash} ***')
                print()





##############################################################################
# ARTICLES PLANTS
##############################################################################


def plants_primary_secondary():
    articles_folderpath = 'database/articles/plants'

    plants_primary = [row for row in util.csv_get_rows('database/tables/plants.csv')[1:]]
    plants_secondary = [row for row in util.csv_get_rows('database/tables/plants-secondary.csv')[1:]]

    plants = []
    for plant in plants_primary: plants.append(plant)
    for plant in plants_secondary: plants.append(plant)

    for plant in plants:
        latin_name = plant[cols['latin_name']].strip().capitalize()
        entity = latin_name.lower().replace(' ', '-').replace('.', '')
        article_filepath_in = f'{articles_folderpath}/{entity}.json'
        article_filepath_out = f'website/plants/{entity}.html'

        print(article_filepath_in)
        data = util.json_read(article_filepath_in)
        title = data['title']
        latin_name = data['latin_name']
        latin_name_dash = latin_name.lower().replace(' ', '-')
        article_html = ''

        article_html += f'<h1>{title}</h1>' + '\n'
        article_html += f'<p><img src="/images/{latin_name_dash}-overview.jpg" alt="{latin_name} overview"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["intro_desc"][0])}</p>' + '\n'

        article_html += f'<h2>What are the medicinal uses of {latin_name}?</h2>' + '\n'
        article_html += f'<p><img src="/images/{latin_name_dash}-medicine.jpg" alt="{latin_name} medicine"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["medicine_intro"][0])}</p>\n'
        article_html += f'<p>Here are the most important <a href="/{entity}/medicine.html">medicinal aspects of {latin_name}</a>.</p>' + '\n'
        article_html += f'<ul>' + '\n'
        article_html += f'<li>Health benefits</li>' + '\n'
        article_html += f'<li>Active constituents</li>' + '\n'
        article_html += f'<li>Medicinal preparations</li>' + '\n'
        article_html += f'<li>Side effects</li>' + '\n'
        article_html += f'<li>Precautions</li>' + '\n'
        article_html += f'</ul>' + '\n'
        article_html += f'<h3>What are the health benefits of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["benefits_desc"][0])}</p>\n'
        article_html += f'<h3>What are the active constituents of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["constituents_desc"][0])}</p>\n'
        article_html += f'<h3>What are the medicinal preparations of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["preparations_desc"][0])}</p>\n'
        article_html += f'<h3>What are the possible side effects of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["side_effects_desc"][0])}</p>\n'
        article_html += f'<h3>What are the precautions to take when using {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["precautions_desc"][0])}</p>\n'

        article_html += f'<h2>What are the horticultural conditions of {latin_name}?</h2>' + '\n'
        article_html += f'<p><img src="/images/{latin_name_dash}-horticulture.jpg" alt="{latin_name} horticulture"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["horticulture_intro"][0])}</p>\n'
        article_html += f'<p>Here are the most important horticultural aspects of {latin_name}.</p>' + '\n'
        article_html += f'<ul>' + '\n'
        article_html += f'<li>Growth Requirements</li>' + '\n'
        article_html += f'<li>Planting Tips</li>' + '\n'
        article_html += f'<li>Caring Tips</li>' + '\n'
        article_html += f'<li>Harvesting Tips</li>' + '\n'
        article_html += f'<li>Pests and Diseases</li>' + '\n'
        article_html += f'</ul>' + '\n'
        article_html += f'<h3>What are the growth requirements uses of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["horticulture_desc"][0])}</p>' + '\n'
        article_html += f'<h3>What are the planting tips of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["horticulture_desc"][1])}</p>' + '\n'
        article_html += f'<h3>What are the caring tips of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["horticulture_desc"][2])}</p>' + '\n'
        article_html += f'<h3>What are the harvesting tips of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["horticulture_desc"][3])}</p>' + '\n'
        article_html += f'<h3>What are the pests and diseases of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["horticulture_desc"][4])}</p>' + '\n'

        article_html += f'<h2>What are the botanical characteristics of {latin_name}?</h2>' + '\n'
        article_html += f'<p><img src="/images/{latin_name_dash}-botany.jpg" alt="{latin_name} medicine"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["botany_intro"][0])}</p>\n'
        article_html += f'<p>Here are the most important botanical characteristics of {latin_name}.</p>' + '\n'
        article_html += f'<ul>' + '\n'
        article_html += f'<li>Taxonomy</li>' + '\n'
        article_html += f'<li>Morphology</li>' + '\n'
        article_html += f'<li>Variants Names and Differences</li>' + '\n'
        article_html += f'<li>Geographic Distribution and Natural Habitats</li>' + '\n'
        article_html += f'<li>Life-Cycle</li>' + '\n'
        article_html += f'</ul>' + '\n'
        article_html += f'<h3>What is the taxonomy of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["botany_desc"][0])}</p>' + '\n'
        article_html += f'<h3>What is the morphology of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["botany_desc"][1])}</p>' + '\n'
        article_html += f'<h3>What are the variants of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["botany_desc"][2])}</p>' + '\n'
        article_html += f'<h3>What is the geographic distribution of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["botany_desc"][3])}</p>' + '\n'
        article_html += f'<h3>What is the life-cycle of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["botany_desc"][4])}</p>' + '\n'

        article_html += f'<h2>What are the historical references of {latin_name}?</h2>' + '\n'
        article_html += f'<p><img src="/images/{latin_name_dash}-history.jpg" alt="{latin_name} history"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["history_intro"][0])}</p>\n'
        article_html += f'<p>Here are the most important historical references of {latin_name}.</p>' + '\n'
        article_html += f'<ul>' + '\n'
        article_html += f'<li>Historical Medicinal Uses</li>' + '\n'
        article_html += f'<li>Mythology</li>' + '\n'
        article_html += f'<li>Ancient Rituals</li>' + '\n'
        article_html += f'<li>Literature</li>' + '\n'
        article_html += f'<li>Symbolism</li>' + '\n'
        article_html += f'</ul>' + '\n'
        article_html += f'<h3>What are the historical medicinal uses of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["history_desc"][0])}</p>' + '\n'
        article_html += f'<h3>What are the mythological references of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["history_desc"][1])}</p>' + '\n'
        article_html += f'<h3>What are the ancient rituals of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["history_desc"][2])}</p>' + '\n'
        article_html += f'<h3>What are the literature references of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["history_desc"][3])}</p>' + '\n'
        article_html += f'<h3>What are the symbolic aspects of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["history_desc"][4])}</p>' + '\n'

        header_html = generate_header_light()
        meta = gen_article_metadata(article_html)
        article_html = generate_toc(article_html)

        breadcrumbs_html = breadcrumbs(article_filepath_out)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                <section class="container-lg">
                    {breadcrumbs_html}
                </section>
                
                <section class="article-section">
                    <div class="container">
                        {meta}
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''

        util.file_write(f'{article_filepath_out}', html)


        # GET IMAGES
        folderpath = f'{IMAGE_FOLDER}/plants/{entity}'
        if not os.path.exists(folderpath): 
            print('MISSING >>>>> IMAGE FOLDER')
            continue
        filenames = os.listdir(folderpath)
        filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]
        random.shuffle(filepaths_in)

        # GENERATE IMAGES IF NEW
        filepaths_out = [
            f'website/images/{entity}-overview.jpg',
            f'website/images/{entity}-medicine.jpg',
            f'website/images/{entity}-horticulture.jpg',
            f'website/images/{entity}-botany.jpg',
            f'website/images/{entity}-history.jpg',
        ]

        for i, filepath_out in enumerate(filepaths_out):
            if os.path.exists(filepath_out): continue
            filepath_in = filepaths_in[i]
            img = Image.open(filepath_in)
            img.thumbnail((768, 768), Image.Resampling.LANCZOS)
            img.save(filepath_out, format='JPEG', optimize=True, quality=50)


# def plants_secondary():
#     plants_secondary = [row for row in util.csv_get_rows('database/tables/plants-secondary.csv')[1:]]
#     for plant in plants_secondary:
#         latin_name = plant[0].strip().capitalize()
#         entity = latin_name.lower().replace(' ', '-').replace('.', '')
#         article_filepath_in = f'database/articles/plants/{entity}.json'
#         article_filepath_out = f'website/{entity}.html'

#         print(article_filepath_in)
#         data = util.json_read(article_filepath_in)
#         title = data['title']
#         latin_name = data['latin_name']
#         latin_name_dash = latin_name.lower().replace(' ', '-')
#         article_html = ''

#         article_html += f'<h1>{title}</h1>' + '\n'
#         article_html += f'<p><img src="/images/{latin_name_dash}-overview.jpg" alt="{latin_name}"></p>' + '\n'
#         article_html += util.text_format_1N1_html(data['intro_desc'][0]) + '\n'

#         article_html += f'<h2>What are the medicinal uses of {latin_name}?</h2>' + '\n'
#         article_html += f'<p><img src="/images/{latin_name_dash}-medicine.jpg" alt="{latin_name} medicine"></p>' + '\n'
#         article_html += f'<p>{util.text_format_1N1_html(data["medicine_intro"][0])}</p>\n'

#         # article_html += f'<p>{medicine_desc[0]}</p>' + '\n'
#         # article_html += f'<p>{medicine_desc[1]}</p>' + '\n'
#         # article_html += f'<p>{medicine_desc[2]}</p>' + '\n'
#         # article_html += f'<p>{medicine_desc[3]}</p>' + '\n'
#         # article_html += f'<p>{medicine_desc[4]}</p>' + '\n'
#         article_html += f'<h3>What are the health benefits of {latin_name}?</h3>' + '\n'
#         article_html += f'<p>{util.text_format_1N1_html(data["benefits_desc"][0])}</p>\n'
#         article_html += f'<h3>What are the active constituents of {latin_name}?</h3>' + '\n'
#         article_html += f'<p>{util.text_format_1N1_html(data["constituents_desc"][0])}</p>\n'
#         article_html += f'<h3>What are the medicinal preparations of {latin_name}?</h3>' + '\n'
#         article_html += f'<p>{util.text_format_1N1_html(data["preparations_desc"][0])}</p>\n'
#         article_html += f'<h3>What are the possible side effects of {latin_name}?</h3>' + '\n'
#         article_html += f'<p>{util.text_format_1N1_html(data["side_effects_desc"][0])}</p>\n'
#         article_html += f'<h3>What are the precautions to take when using {latin_name}?</h3>' + '\n'
#         article_html += f'<p>{util.text_format_1N1_html(data["precautions_desc"][0])}</p>\n'

#         article_html += f'<p>Here\'s an article explaining in detail the <a href="/{entity}/medicine.html">medicinal aspects of {latin_name}</a>.</p>' + '\n'
#         article_html += f'<h2>What are the horticultural conditions of {latin_name}?</h2>' + '\n'
#         article_html += f'<p><img src="/images/{latin_name_dash}-horticulture.jpg" alt="{latin_name} medicine"></p>' + '\n'
#         article_html += f'<p>{data["horticulture_desc"][0]}</p>' + '\n'
#         article_html += f'<p>{data["horticulture_desc"][1]}</p>' + '\n'
#         article_html += f'<p>{data["horticulture_desc"][2]}</p>' + '\n'
#         article_html += f'<p>{data["horticulture_desc"][3]}</p>' + '\n'
#         article_html += f'<p>{data["horticulture_desc"][4]}</p>' + '\n'
#         article_html += f'<h2>What are the botanical characteristics of {latin_name}?</h2>' + '\n'
#         article_html += f'<p><img src="/images/{latin_name_dash}-botany.jpg" alt="{latin_name} medicine"></p>' + '\n'
#         article_html += f'<p>{data["botany_desc"][0]}</p>' + '\n'
#         article_html += f'<p>{data["botany_desc"][1]}</p>' + '\n'
#         article_html += f'<p>{data["botany_desc"][2]}</p>' + '\n'
#         article_html += f'<p>{data["botany_desc"][3]}</p>' + '\n'
#         article_html += f'<p>{data["botany_desc"][4]}</p>' + '\n'

#         header_html = generate_header_light()
#         word_count = len(article_html.split(' '))
#         reading_time_html = str(word_count // 200) + ' minutes'

#         article_html = generate_toc(article_html)

#         html = f'''
#             <!DOCTYPE html>
#             <html lang="en">

#             <head>
#                 <meta charset="UTF-8">
#                 <meta name="viewport" content="width=device-width, initial-scale=1.0">
#                 <meta name="author" content="{g.AUTHOR_NAME}">
#                 <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
#                 <link rel="stylesheet" href="/style.css">
#                 <title>{title}</title>
#                 {g.GOOGLE_TAG}
                
#             </head>

#             <body>
#                 {header_html}
                
#                 <section class="article-section">
#                     <div class="container">
#                         <div class="flex items-center justify-between mb-16">
#                             <div class="flex items-center gap-16">
#                                 <img class="author-image" src="/martin-pellizzer.jpg" alt="">
#                                 <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
#                             </div>
#                             <span>{reading_time_html}</span>
#                         </div>
#                         {article_html}
#                     </div>
#                 </section>

#                 <footer>
#                     <div class="container-lg">
#                         <span>© TerraWhisper.com 2024 | All Rights Reserved
#                     </div>
#                 </footer>
#             </body>

#             </html>
#         '''

#         util.file_write(f'{article_filepath_out}', html)


#         # # GET IMAGES
#         # folderpath = f'{IMAGE_FOLDER}/plants/{entity}'
#         # if not os.path.exists(folderpath): 
#         #     print('MISSING >>>>> IMAGE FOLDER')
#         #     continue
#         # filenames = os.listdir(folderpath)
#         # filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]
#         # random.shuffle(filepaths_in)

#         # # GENERATE IMAGES IF NEW
#         # filepaths_out = [
#         #     f'website/images/{entity}-overview.jpg',
#         #     f'website/images/{entity}-medicine.jpg',
#         #     f'website/images/{entity}-horticulture.jpg',
#         #     f'website/images/{entity}-botany.jpg',
#         # ]

#         # for i, filepath_out in enumerate(filepaths_out):
#         #     if os.path.exists(filepath_out): continue
#         #     filepath_in = filepaths_in[i]
#         #     img = Image.open(filepath_in)
#         #     img.thumbnail((768, 768), Image.Resampling.LANCZOS)
#         #     img.save(filepath_out, format='JPEG', optimize=True, quality=50)



#         # IMAGES
#         # folderpath = f'{IMAGE_FOLDER}/plants/{latin_name_dash}'
#         # filenames = os.listdir(folderpath)
#         # filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]

#         # filepath_in = filepaths_in[0]
#         # filepath_out = f'website/images/{latin_name_dash}.jpg'
#         # img = Image.open(filepath_in)
#         # img.thumbnail((768, 768), Image.Resampling.LANCZOS)
#         # img.save(filepath_out, format='JPEG', optimize=True, quality=50)

#         # filepath_in = filepaths_in[1]
#         # filepath_out = f'website/images/{latin_name_dash}-medicine.jpg'
#         # img = Image.open(filepath_in)
#         # img.thumbnail((768, 768), Image.Resampling.LANCZOS)
#         # img.save(filepath_out, format='JPEG', optimize=True, quality=50)

#         # filepath_in = filepaths_in[2]
#         # filepath_out = f'website/images/{latin_name_dash}-horticulture.jpg'
#         # img = Image.open(filepath_in)
#         # img.thumbnail((768, 768), Image.Resampling.LANCZOS)
#         # img.save(filepath_out, format='JPEG', optimize=True, quality=50)

#         # filepath_in = filepaths_in[3]
#         # filepath_out = f'website/images/{latin_name_dash}-botany.jpg'
#         # img = Image.open(filepath_in)
#         # img.thumbnail((768, 768), Image.Resampling.LANCZOS)
#         # img.save(filepath_out, format='JPEG', optimize=True, quality=50)

#         # quit()





def articles_medicine():
    articles_folderpath = 'database/articles/plants'
    for plant in plants:
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-').replace('.', '')
        article_filepath = f'{articles_folderpath}/{entity}/medicine.json'

        if not os.path.exists(article_filepath): continue
        print(article_filepath)

        article_filepath_in = article_filepath
        article_filepath_out = article_filepath.replace(articles_folderpath, 'website').replace('.json', '.html')

        data = util.json_read(article_filepath_in)
        article_html = ''

        try: title = data["title"]
        except: title = ''
        if title != '': article_html += f'<h1>{data["title"]}</h1>' + '\n'
        else: print('MISSING >>>>> TITLE\n')
        
        article_html += f'<p><img src="/images/{entity}-medicine-overview.jpg" alt="{latin_name}"></p>' + '\n'
        
        try: article_html += util.text_format_1N1_html(data['intro']) + '\n'
        except: print('MISSING >>>>> INTRO\n')

        article_html += f'<h2>What are the health benefits of {latin_name} ({common_name})?</h2>' + '\n'
        article_html += f'<p><img src="/images/{entity}-medicine-benefits.jpg" alt="{latin_name}"></p>' + '\n'
        try: article_html += util.text_format_1N1_html(data['benefits_text']) + '\n'
        except: print('MISSING >>>>> BENEFITS TEXT\n')
        try:
            article_html += f'<p>The following list shows the <a href="/{entity}/medicine/benefits.html">health benefits of {latin_name}</a>.</p>' + '\n' 
            article_html += lst_to_html_bold(data['benefits_list']) + '\n'
        except: print('MISSING >>>>> BENEFITS LIST\n')

        article_html += f'<h2>What are the active constituents of {latin_name} ({common_name})?</h2>' + '\n'
        article_html += f'<p><img src="/images/{entity}-medicine-constituents.jpg" alt="{latin_name}"></p>' + '\n'
        try: article_html += util.text_format_1N1_html(data['constituents_text']) + '\n'
        except: print('MISSING >>>>> CONSTITUENTS TEXT\n')
        try:
            article_html += f'<p>The following list shows the <a href="/{entity}/medicine/constituents.html">active constituents of {latin_name}</a>.</p>' + '\n'
            article_html += lst_to_html_bold(data['constituents_list']) + '\n'
        except: print('MISSING >>>>> CONSTITUENTS LIST\n')

        article_html += f'<h2>What are the medicinal preparations of {latin_name} ({common_name})?</h2>' + '\n'
        article_html += f'<p><img src="/images/{entity}-medicine-preparations.jpg" alt="{latin_name}"></p>' + '\n'
        try: article_html += util.text_format_1N1_html(data['preparations_text']) + '\n'
        except: print('MISSING >>>>> PREPARATIONS TEXT\n')
        try:
            article_html += f'<p>The following list shows the <a href="/{entity}/medicine/preparations.html">medicinal preparations of {latin_name}</a>.</p>' + '\n'
            article_html += lst_to_html_bold(data['preparations_list']) + '\n'
        except: print('MISSING >>>>> PREPARATIONS LIST\n')

        article_html += f'<h2>What are the possible side effects of using {latin_name} ({common_name}) for medicinal purposes?</h2>' + '\n'
        article_html += f'<p><img src="/images/{entity}-medicine-side-effects.jpg" alt="{latin_name}"></p>' + '\n'
        try: article_html += util.text_format_1N1_html(data['side_effects_text']) + '\n'
        except: print('MISSING >>>>> SIDE EFFECTS TEXT\n')
        try:
            article_html += f'<p>The following list shows the possible side effects of {latin_name} for medicinal purposes.</p>' + '\n'
            article_html += lst_to_html_bold(data['side_effects_list']) + '\n'
        except: print('MISSING >>>>> SIDE EFFECTS LIST\n')

        article_html += f'<h2>What are the precautions to take when using {latin_name} ({common_name}) medicinally?</h2>' + '\n'
        article_html += f'<p><img src="/images/{entity}-medicine-precautions.jpg" alt="{latin_name}"></p>' + '\n'
        try: article_html += util.text_format_1N1_html(data['precautions_text']) + '\n'
        except: print('MISSING >>>>> PRECAUTIONS TEXT\n')
        try:
            article_html += f'<p>The following list shows the precautions to take when using {latin_name} medicinally.</p>' + '\n'
            article_html += lst_to_html_bold(data['precautions_list']) + '\n'
        except: print('MISSING >>>>> PRECAUTIONS LIST\n')

        header_html = generate_header_light()
        word_count = len(article_html.split(' '))
        reading_time_html = str(word_count // 200) + ' minutes'

        article_html = generate_toc(article_html)
        breadcrumbs_html = breadcrumbs(article_filepath_out)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                <section class="container-lg">
                    {breadcrumbs_html}
                </section>
                
                <section class="article-section">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
                            </div>
                            <span>{reading_time_html}</span>
                        </div>
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''

        util.file_write(f'{article_filepath_out}', html)

        # IMAGES
        folderpath = f'{IMAGE_FOLDER}/plants/{entity}'
        if not os.path.exists(folderpath): 
            print('MISSING >>>>> IMAGE FOLDER')
            continue
        filenames = os.listdir(folderpath)
        filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]

        random.shuffle(filepaths_in)

        filepaths_out = [
            f'website/images/{entity}-medicine-overview.jpg',
            f'website/images/{entity}-medicine-benefits.jpg',
            f'website/images/{entity}-medicine-constituents.jpg',
            f'website/images/{entity}-medicine-preparations.jpg',
            f'website/images/{entity}-medicine-side-effects.jpg',
            f'website/images/{entity}-medicine-precautions.jpg',
        ]

        for i, filepath_out in enumerate(filepaths_out):
            if os.path.exists(filepath_out): continue
            filepath_in = filepaths_in[i]
            img = Image.open(filepath_in)
            img.thumbnail((768, 768), Image.Resampling.LANCZOS)
            img.save(filepath_out, format='JPEG', optimize=True, quality=50)


def articles_benefits():
    articles_folderpath = 'database/articles/plants'
    articles_filepath = []
    for plant in plants:
        latin_name = plant[cols['latin_name']].strip()
        entity = latin_name.lower().replace(' ', '-')
        article_filepath = f'{articles_folderpath}/{entity}/medicine/benefits.json'

        if not os.path.exists(article_filepath): continue

        article_filepath_in = article_filepath
        article_filepath_out = article_filepath.replace(articles_folderpath, 'website').replace('.json', '.html')

        data = util.json_read(article_filepath_in)
        article_html = ''

        try: title = data["title"]
        except: title = ''
        if title != '': article_html += f'<h1>{title}</h1>' + '\n'
        else: print('MISSING >>>>> TITLE\n')

        article_html += f'<p><img src="/images/{entity}.jpg" alt="{latin_name}"></p>' + '\n'
        
        try: article_html += util.text_format_1N1_html(data['intro']) + '\n'
        except: print('MISSING >>>>> INTRO\n')
        # images_plant_foldername = f'{IMAGE_FOLDER}/plants/{entity}'
        # try: images_plant_filename = os.listdir(images_plant_foldername)
        # except: images_plant_filename = None
        
        # images_filepath = []
        # if images_plant_filename:
        #     images_filepath = [f'{images_plant_foldername}/{filename}' for filename in images_plant_filename]

        try: benefits = data['benefits']
        except: benefits = []
        for i, benefit in enumerate(benefits[:10]):
            benefit_name = benefit['benefit_name'].strip()
            benefit_name_dash = benefit_name.lower().replace(' ' , '-')

            article_html += f'<h2>{i+1}. {benefit_name}</h2>' + '\n'
            article_html += f'<p><img src="/images/{entity}-medicine-benefits-{benefit["benefit_name"].strip().lower().replace(" ", "-")}.jpg" alt="{latin_name}"></p>' + '\n'
            try: article_html += util.text_format_1N1_html(benefit['benefit_desc']) + '\n'
            except: print(f'MISSING DESCRIPTION: {article_filepath_in} >> {benefit_name}')
            article_html += f'<p>{latin_name} {benefit_name.lower()} thanks to the active constituents listed below.</p>' + '\n'
            try: article_html += util.lst_to_html(benefit['constituents_list']) + '\n'
            except: print(f'MISSING CONSTITUENTS: {article_filepath_in} >> {benefit_name}')

        header_html = generate_header_light()
        word_count = len(article_html.split(' '))
        reading_time_html = str(word_count // 200) + ' minutes'

        article_html = generate_toc(article_html)
        breadcrumbs_html = breadcrumbs(article_filepath_out)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                <section class="container-lg">
                    {breadcrumbs_html}
                </section>
                
                <section class="article-section">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
                            </div>
                            <span>{reading_time_html}</span>
                        </div>
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''

        util.file_write(f'{article_filepath_out}', html)

        # IMAGES
        folderpath = f'{IMAGE_FOLDER}/plants/{entity}'
        if not os.path.exists(folderpath): 
            print('MISSING >>>>> IMAGE FOLDER')
            continue
        filenames = os.listdir(folderpath)
        filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]

        random.shuffle(filepaths_in)

        filepath_out = f'website/images/{entity}-medicine-benefits-overview.jpg',
        if not os.path.exists(filepaths_in[3]):
            try: filepath_in = filepaths_in[3]
            except: 
                print(f'MISSING IMAGE: {entity} >> {i}')
                continue
            img = Image.open(filepath_in)
            img.thumbnail((768, 768), Image.Resampling.LANCZOS)
            img.save(filepath_out, format='JPEG', optimize=True, quality=50)


        # filepaths_out = [
        #     f'website/images/{entity}-medicine-benefits-{benefits[0]["benefit_name"].strip().lower().replace(" ", "-")}.jpg',
        #     f'website/images/{entity}-medicine-benefits-{benefits[1]["benefit_name"].strip().lower().replace(" ", "-")}.jpg',
        #     f'website/images/{entity}-medicine-benefits-{benefits[2]["benefit_name"].strip().lower().replace(" ", "-")}.jpg',
        #     f'website/images/{entity}-medicine-benefits-{benefits[3]["benefit_name"].strip().lower().replace(" ", "-")}.jpg',
        #     f'website/images/{entity}-medicine-benefits-{benefits[4]["benefit_name"].strip().lower().replace(" ", "-")}.jpg',
        #     f'website/images/{entity}-medicine-benefits-{benefits[5]["benefit_name"].strip().lower().replace(" ", "-")}.jpg',
        #     f'website/images/{entity}-medicine-benefits-{benefits[6]["benefit_name"].strip().lower().replace(" ", "-")}.jpg',
        #     f'website/images/{entity}-medicine-benefits-{benefits[7]["benefit_name"].strip().lower().replace(" ", "-")}.jpg',
        #     f'website/images/{entity}-medicine-benefits-{benefits[8]["benefit_name"].strip().lower().replace(" ", "-")}.jpg',
        #     f'website/images/{entity}-medicine-benefits-{benefits[9]["benefit_name"].strip().lower().replace(" ", "-")}.jpg',
        # ]

        for i, benefit in enumerate(benefits[:10]):
            filepath_out = f'website/images/{entity}-medicine-benefits-{benefit["benefit_name"].strip().lower().replace(" ", "-")}.jpg'
            if os.path.exists(filepath_out): continue
            print(filepath_out)
            try: filepath_in = filepaths_in[i]
            except: 
                print(f'MISSING IMAGE: {entity} >> {i}')
                continue
            img = Image.open(filepath_in)
            img.thumbnail((768, 768), Image.Resampling.LANCZOS)
            img.save(filepath_out, format='JPEG', optimize=True, quality=50)


def articles_constituents():
    articles_folderpath = 'database/articles/plants'
    articles_type = 'constituents'

    for plant in plants:
        latin_name = plant[cols['latin_name']].strip()
        entity = latin_name.lower().replace(' ', '-')

        article_filepath = f'{articles_folderpath}/{entity}/medicine/constituents.json'
        article_filepath_in = article_filepath
        article_filepath_out = article_filepath.replace(articles_folderpath, 'website').replace('.json', '.html')

        if not os.path.exists(article_filepath): continue

        data = util.json_read(article_filepath_in)

        article_html = ''

        try: title = data["title"]
        except: title = ''
        if title != '': article_html += f'<h1>{title}</h1>' + '\n'
        else: print('MISSING >>>>> TITLE\n')

        article_html += f'<p><img src="/images/{entity}-medicine-constituents-overview.jpg" alt="{latin_name} medicine constituents overview"></p>' + '\n'
        
        try: article_html += util.text_format_1N1_html(data['intro']) + '\n'
        except: print('MISSING >>>>> INTRO\n')

        try: constituents = data['constituents']
        except: constituents = []
        for i, item in enumerate(constituents[:10]):
            try: item_name = item['constituent_name'].strip()
            except:
                print('MISSING >>>>> CONSTITUENT NAME\n')
                continue
            item_name_dash = item_name.lower().replace(' ' , '-')

            article_html += f'<h2>{i+1}. {item_name}</h2>' + '\n'
            article_html += f'<p><img src="/images/{entity}-medicine-constituents-{item["constituent_name"].strip().lower().replace(" ", "-")}.jpg" alt="{latin_name}"></p>' + '\n'
            try: article_html += util.text_format_1N1_html(item['constituent_desc']) + '\n'
            except: print(f'MISSING DESCRIPTION: {article_filepath_in} >> {item_name}')
            # article_html += f'<p>{latin_name} {item_name.lower()} thanks to the active constituents listed below.</p>' + '\n'
            # try: article_html += util.lst_to_html(item['constituents_list']) + '\n'
            # except: print(f'MISSING CONSTITUENTS: {article_filepath_in} >> {item_name}')

        header_html = generate_header_light()
        word_count = len(article_html.split(' '))
        reading_time_html = str(word_count // 200) + ' minutes'

        article_html = generate_toc(article_html)
        breadcrumbs_html = breadcrumbs(article_filepath_out)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                <section class="container-lg">
                    {breadcrumbs_html}
                </section>
                
                <section class="article-section">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
                            </div>
                            <span>{reading_time_html}</span>
                        </div>
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''

        util.file_write(f'{article_filepath_out}', html)

        # IMAGES
        folderpath = f'{IMAGE_FOLDER}/plants/{entity}'
        if not os.path.exists(folderpath): 
            print('MISSING >>>>> IMAGE FOLDER')
            continue
        filenames = os.listdir(folderpath)
        filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]

        random.shuffle(filepaths_in)

        filepath_out = f'website/images/{entity}-medicine-constituents-overview.jpg'
        if not os.path.exists(filepath_out):
            try: 
                filepath_in = filepaths_in[3]
                img = Image.open(filepath_in)
                img.thumbnail((768, 768), Image.Resampling.LANCZOS)
                img.save(filepath_out, format='JPEG', optimize=True, quality=50)
            except: 
                print(f'MISSING IMAGE: {entity} >> {i}')
                continue

        for i, item in enumerate(constituents[:10]):
            filepath_out = f'website/images/{entity}-medicine-constituents-{item["constituent_name"].strip().lower().replace(" ", "-")}.jpg'
            if os.path.exists(filepath_out): continue
            print(filepath_out)
            try: filepath_in = filepaths_in[i]
            except: 
                print(f'MISSING IMAGE: {entity} >> {i}')
                continue
            img = Image.open(filepath_in)
            img.thumbnail((768, 768), Image.Resampling.LANCZOS)
            img.save(filepath_out, format='JPEG', optimize=True, quality=50)


def articles_preparations():
    articles_folderpath = 'database/articles/plants'
    articles_type = 'preparations'

    for plant in plants:
        latin_name = plant[cols['latin_name']].strip()
        entity = latin_name.lower().replace(' ', '-')

        article_filepath = f'{articles_folderpath}/{entity}/medicine/preparations.json'
        article_filepath_in = article_filepath
        article_filepath_out = article_filepath.replace(articles_folderpath, 'website').replace('.json', '.html')

        if not os.path.exists(article_filepath): continue

        data = util.json_read(article_filepath_in)

        article_html = ''

        try: title = data["title"]
        except: title = ''
        if title != '': article_html += f'<h1>{title}</h1>' + '\n'
        else: print('MISSING >>>>> TITLE\n')

        article_html += f'<p><img src="/images/{entity}-medicine-preparations-overview.jpg" alt="{latin_name} medicine preparations overview"></p>' + '\n'
        
        try: article_html += util.text_format_1N1_html(data['intro']) + '\n'
        except: print('MISSING >>>>> INTRO\n')

        try: preparations = data['preparations']
        except: preparations = []
        for i, item in enumerate(preparations[:10]):
            try: item_name = item['preparation_name'].strip()
            except:
                print('MISSING >>>>> PREPARATION NAME\n')
                continue
            item_name_dash = item_name.lower().replace(' ' , '-')

            article_html += f'<h2>{i+1}. {item_name}</h2>' + '\n'
            article_html += f'<p><img src="/images/{entity}-medicine-preparations-{item["preparation_name"].strip().lower().replace(" ", "-")}.jpg" alt="{latin_name}"></p>' + '\n'
            try: article_html += util.text_format_1N1_html(item['constituent_desc']) + '\n'
            except: print(f'MISSING DESCRIPTION: {article_filepath_in} >> {item_name}')
            # article_html += f'<p>{latin_name} {item_name.lower()} thanks to the active preparations listed below.</p>' + '\n'

        header_html = generate_header_light()
        word_count = len(article_html.split(' '))
        reading_time_html = str(word_count // 200) + ' minutes'

        article_html = generate_toc(article_html)
        breadcrumbs_html = breadcrumbs(article_filepath_out)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                <section class="container-lg">
                    {breadcrumbs_html}
                </section>
                
                <section class="article-section">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
                            </div>
                            <span>{reading_time_html}</span>
                        </div>
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''

        util.file_write(f'{article_filepath_out}', html)

        # IMAGES
        folderpath = f'{IMAGE_FOLDER}/plants/{entity}'
        if not os.path.exists(folderpath): 
            print(f'MISSING >>>>> IMAGE FOLDER --- {entity}')
            continue
        filenames = os.listdir(folderpath)
        filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]

        random.shuffle(filepaths_in)

        filepath_out = f'website/images/{entity}-medicine-preparations-overview.jpg'
        if not os.path.exists(filepath_out):
            try: 
                filepath_in = filepaths_in[3]
                img = Image.open(filepath_in)
                img.thumbnail((768, 768), Image.Resampling.LANCZOS)
                img.save(filepath_out, format='JPEG', optimize=True, quality=50)
            except: 
                print(f'MISSING IMAGE: {entity} >> {i}')
                continue

        for i, item in enumerate(preparations[:10]):
            filepath_out = f'website/images/{entity}-medicine-preparations-{item["preparation_name"].strip().lower().replace(" ", "-")}.jpg'
            if os.path.exists(filepath_out): continue
            print(filepath_out)
            try: filepath_in = filepaths_in[i]
            except: 
                print(f'MISSING IMAGE: {entity} >> {i}')
                continue
            img = Image.open(filepath_in)
            img.thumbnail((768, 768), Image.Resampling.LANCZOS)
            img.save(filepath_out, format='JPEG', optimize=True, quality=50)




##############################################################################
# ARTICLES TREFLE
##############################################################################

def gen_articles_trefle():
    articles_folderpath = 'database/articles/plants_trefle'
    plants_filenames = os.listdir(articles_folderpath)
    for plant_filename in plants_filenames:
        plant_filename_no_ext = plant_filename.replace('.json', '')
        article_filepath_in = f'{articles_folderpath}/{plant_filename_no_ext}.json'
        article_filepath_out = f'website/plants/{plant_filename_no_ext}.html'

        try: data = util.json_read(article_filepath_in)
        except: continue

        print(article_filepath_in)

        title = data['title']
        latin_name = data['latin_name']
        entity = data['entity']
        article_html = ''

        article_html += f'<h1>{title}</h1>' + '\n'
        article_html += f'<p><img src="/images/{entity}-overview.jpg" alt="{latin_name}"></p>' + '\n'
        article_html += util.text_format_1N1_html(data['intro_desc'][0]) + '\n'

        article_html += f'<h2>What are the medicinal uses of {latin_name}?</h2>' + '\n'
        article_html += f'<p><img src="/images/{entity}-medicine.jpg" alt="{latin_name} medicine"></p>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["medicine_desc"][0])}</p>\n'
        article_html += f'<p>Here are the most important <a href="/{entity}/medicine.html">medicinal aspects of {latin_name}</a>.</p>' + '\n'
        article_html += f'<ul>' + '\n'
        article_html += f'<li>Health benefits</li>' + '\n'
        article_html += f'<li>Active constituents</li>' + '\n'
        article_html += f'<li>Medicinal preparations</li>' + '\n'
        article_html += f'<li>Side effects</li>' + '\n'
        article_html += f'<li>Precautions</li>' + '\n'
        article_html += f'</ul>' + '\n'
        
        article_html += f'<h3>What are the health benefits of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["medicine_desc"][0])}</p>\n'
        article_html += f'<h3>What are the active constituents of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["medicine_desc"][1])}</p>\n'
        article_html += f'<h3>What are the medicinal preparations of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["medicine_desc"][2])}</p>\n'
        article_html += f'<h3>What are the possible side effects of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["medicine_desc"][3])}</p>\n'
        article_html += f'<h3>What are the precautions to take when using {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["medicine_desc"][4])}</p>\n'

        article_html += f'<h2>What are the horticultural conditions of {latin_name}?</h2>' + '\n'
        article_html += f'<p><img src="/images/{entity}-horticulture.jpg" alt="{latin_name} medicine"></p>' + '\n'
        article_html += f'<h3>What are the growth requirements uses of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["horticulture_desc"][0])}</p>' + '\n'
        article_html += f'<h3>What are the planting tips of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["horticulture_desc"][1])}</p>' + '\n'
        article_html += f'<h3>What are the caring tips of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["horticulture_desc"][2])}</p>' + '\n'
        article_html += f'<h3>What are the harvesting tips of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["horticulture_desc"][3])}</p>' + '\n'
        article_html += f'<h3>What are the pests and diseases of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["horticulture_desc"][4])}</p>' + '\n'

        article_html += f'<h2>What are the botanical characteristics of {latin_name}?</h2>' + '\n'
        article_html += f'<p><img src="/images/{entity}-botany.jpg" alt="{latin_name} medicine"></p>' + '\n'
        article_html += f'<h3>What is the taxonomy of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["botany_desc"][0])}</p>' + '\n'
        article_html += f'<h3>What is the morphology of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["botany_desc"][1])}</p>' + '\n'
        article_html += f'<h3>What are the variants of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["botany_desc"][2])}</p>' + '\n'
        article_html += f'<h3>What is the geographic distribution of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["botany_desc"][3])}</p>' + '\n'
        article_html += f'<h3>What is the life-cycle of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["botany_desc"][4])}</p>' + '\n'

        article_html += f'<h2>What is the history of {latin_name}?</h2>' + '\n'
        article_html += f'<p><img src="/images/{entity}-history.jpg" alt="{latin_name} history"></p>' + '\n'
        article_html += f'<h3>What are the historical medicinal uses of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["history_desc"][0])}</p>' + '\n'
        article_html += f'<h3>What are the mythological references of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["history_desc"][1])}</p>' + '\n'
        article_html += f'<h3>What are the ancient rituals of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["history_desc"][2])}</p>' + '\n'
        article_html += f'<h3>What are the literature references of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["history_desc"][3])}</p>' + '\n'
        article_html += f'<h3>What are the symbolic aspects of {latin_name}?</h3>' + '\n'
        article_html += f'<p>{util.text_format_1N1_html(data["history_desc"][4])}</p>' + '\n'

        header_html = generate_header_light()
        meta = gen_article_metadata(article_html)
        article_html = generate_toc(article_html)

        breadcrumbs_html = breadcrumbs(article_filepath_out)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                <section class="container-lg">
                    {breadcrumbs_html}
                </section>
                
                <section class="article-section">
                    <div class="container">
                        {meta}
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''

        util.file_write(f'{article_filepath_out}', html)


        # GET IMAGES
        folderpath = f'{IMAGE_FOLDER}/plants/{entity}'
        if not os.path.exists(folderpath): 
            print('MISSING >>>>> IMAGE FOLDER')
            continue
        filenames = os.listdir(folderpath)
        filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]
        random.shuffle(filepaths_in)

        # GENERATE IMAGES IF NEW
        filepaths_out = [
            f'website/images/{entity}-overview.jpg',
            f'website/images/{entity}-medicine.jpg',
            f'website/images/{entity}-horticulture.jpg',
            f'website/images/{entity}-botany.jpg',
            f'website/images/{entity}-history.jpg',
        ]

        for i, filepath_out in enumerate(filepaths_out):
            if os.path.exists(filepath_out): continue
            filepath_in = filepaths_in[i]
            img = Image.open(filepath_in)
            img.thumbnail((768, 768), Image.Resampling.LANCZOS)
            img.save(filepath_out, format='JPEG', optimize=True, quality=50)



##############################################################################
# PAGES PLANTS (TAXONOMY)
##############################################################################

def gen_pages_taxonomy():
    try: shutil.rmtree('website/taxonomy')
    except: pass
    try: os.remove('website/taxonomy.html')
    except: pass
    
    rows = util.csv_get_rows('database/tables/taxonomy.csv')

    kingdoms = []
    phylums = []
    classes = []
    for row in rows[1:]:
        entity = row[0]
        kingdom = row[1]
        phylum = row[2]
        clss = row[3]
        order = row[4]
        family = row[5]
        genus = row[6]
        species = row[7]

        full_path = f'{kingdom}/{phylum}/{clss}/{order}/{family}/{genus}/{species}'

        if kingdoms == []: 
            kingdoms = [[kingdom, phylum]]
        else:
            found = False
            for kingdom_old in kingdoms:
                if kingdom_old[0] == kingdom:
                    if phylum not in kingdom_old:
                        kingdom_old.append(phylum)
                    found = True
                    break
            if not found:
                kingdoms.append([kingdom, phylum])
                
        if phylums == []: 
            phylums = [[phylum, clss]]
        else:
            found = False
            for phylum_old in phylums:
                if phylum_old[0] == phylum:
                    if clss not in phylum_old:
                        phylum_old.append(clss)
                    found = True
                    break
            if not found:
                phylums.append([phylum, clss])

        if classes == []: 
            classes = [[clss, order]]
        else:
            found = False
            for clss_old in classes:
                if clss_old[0] == clss:
                    if order not in clss_old:
                        clss_old.append(order)
                    found = True
                    break
            if not found:
                classes.append([clss, order])

    
    for kingdom in kingdoms:
        print(kingdom)
    print()
    print()
    print()
    for phylum in phylums:
        print(phylum)
    print()
    print()
    print()
    for clss in classes:
        print(clss)
    print()
    print()
    print()
    quit()

    for kingdom in kingdoms:
        title = kingdom[0]

        article_html = ''
        kingdom_slug = kingdom[0].lower().strip().replace(' ', '-')
        for phylum in kingdom[1:]:
            phylum_slug = phylum.lower().strip().replace(' ', '-')
            article_html += f'<p><a href="/taxonomy/{kingdom_slug}/{phylum_slug}.html">{phylum}</a></p>'
        
        header_html = generate_header_light()
        word_count = len(article_html.split(' '))
        reading_time_html = str(word_count // 200) + ' minutes'
        article_html = generate_toc(article_html)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
            </head>

            <body>
                {header_html}
                
                <section class="article-section">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
                            </div>
                            <span>{reading_time_html}</span>
                        </div>
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''
        article_filepath_out = f'website/taxonomy/{kingdom_slug}.html'
        util.file_write(f'{article_filepath_out}', html)

        for phylum in phylums:
            title = phylum[0]

            article_html = ''
            phylum_slug = phylum[0].lower().strip().replace(' ', '-')
            for clss in phylum[1:]:
                clss_slug = clss.lower().strip().replace(' ', '-')
                article_html += f'<p><a href="/taxonomy/{kingdom_slug}/{phylum_slug}/{clss_slug}.html">{clss}</a></p>'
            
            header_html = generate_header_light()
            word_count = len(article_html.split(' '))
            reading_time_html = str(word_count // 200) + ' minutes'
            article_html = generate_toc(article_html)

            html = f'''
                <!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta name="author" content="{g.AUTHOR_NAME}">
                    <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                    <link rel="stylesheet" href="/style.css">
                    <title>{title}</title>
                    {g.GOOGLE_TAG}
                </head>

                <body>
                    {header_html}
                    
                    <section class="article-section">
                        <div class="container">
                            <div class="flex items-center justify-between mb-16">
                                <div class="flex items-center gap-16">
                                    <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                    <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
                                </div>
                                <span>{reading_time_html}</span>
                            </div>
                            {article_html}
                        </div>
                    </section>

                    <footer>
                        <div class="container-lg">
                            <span>© TerraWhisper.com 2024 | All Rights Reserved
                        </div>
                    </footer>
                </body>

                </html>
            '''

            article_filepath_out = f'website/taxonomy/{kingdom_slug}/{phylum_slug}.html'
            util.file_write(f'{article_filepath_out}', html)


    article_html = ''
    title = 'taxonomy'

    header_html = generate_header_light()
    word_count = len(article_html.split(' '))
    reading_time_html = str(word_count // 200) + ' minutes'
    article_html = generate_toc(article_html)

    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{g.AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>{title}</title>
            {g.GOOGLE_TAG}
        </head>

        <body>
            {header_html}
            
            <section class="article-section">
                <div class="container">
                    <div class="flex items-center justify-between mb-16">
                        <div class="flex items-center gap-16">
                            <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                            <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
                        </div>
                        <span>{reading_time_html}</span>
                    </div>
                    <a href="/taxonomy/plantae.html">Plantae</a>
                </div>
            </section>

            <footer>
                <div class="container-lg">
                    <span>© TerraWhisper.com 2024 | All Rights Reserved
                </div>
            </footer>
        </body>

        </html>
    '''

    article_filepath_out = f'website/taxonomy.html'
    util.file_write(f'{article_filepath_out}', html)


def taxonomy():
    rows = util.csv_get_rows('database/tables/_plants_all_new.csv')

    families = [row[4] for row in rows if row[4].strip() != ''][1:]
    families = list(set(families))
    families = sorted(families)
    families_html = ''
    for i, family in enumerate(families):
        print(f'{i}/{len(families)} - {family}')
        families_html += f'<p><a href="/taxonomy/{family}.html">{family}</a></p>'

        rows = util.csv_get_rows_by_entity('database/tables/_plants_all_new.csv', family, num_col=4)
        genuses = [row[3] for row in rows][1:]
        genuses = list(set(genuses))
        genuses = sorted(genuses)
        genuses_html = ''
        for genus in genuses:
            genuses_html += f'<p><a href="#">{genus}</a></p>'

        util.file_write(f'website/taxonomy/{family}.html', genuses_html)

    util.file_write('website/taxonomy.html', families_html)

    
    





##############################################################################
# STATIC FILES
##############################################################################

# TRANSFER STATIC FILES
shutil.copy2('style.css', 'website/style.css')
shutil.copy2('sitemap.xml', 'website/sitemap.xml')
shutil.copy2('robots.txt', 'website/robots.txt')

# COMPRESS AND TRASFER IMAGES
img = Image.open('assets/images/medicinal-herbs.png')
img = util.img_resize(img, 1920, 1080)
img.save(f'website/images/herbalism-natural-remedies.jpg', format='JPEG', optimize=True, quality=50)

img = Image.open('assets/images/woman-frustrated-with-modern-medicinals.png')
img = util.img_resize(img, 768, 768)
img.save(f'website/images/woman-frustrated-with-modern-medicinals.jpg', format='JPEG', optimize=True, quality=50)

shutil.copy2('assets/images/martin-pellizzer-300x300.jpg', f'website/images/martin-pellizzer-300x300.jpg')




##############################################################################
# RUN
##############################################################################

home()
teas()
top_herbs()
about()

herbalism()
# herbalism_tea()
herbalism_tea_condition()

# plant()
plants_primary_secondary()
# plants_secondary()

# articles_medicine()

# articles_benefits()
# articles_constituents()
# articles_preparations()



# gen_pages_taxonomy()

# sitemap.sitemap_main()

# gen_articles_trefle()

# taxonomy()

