import os
import markdown
import shutil
import random
import glob



from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

import g
import util





IMAGE_FOLDER = 'C:/terrawhisper-assets/images'

AUTHOR_NAME = 'Martin Pellizzer'
GOOGLE_TAG = '''
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-9086LN3SRR"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-9086LN3SRR');
    </script>
'''

try: os.makedirs('website/images')
except: pass


plants = [row for row in util.csv_get_rows('database/tables/plants.csv')]
cols = {}
for i, item in enumerate(plants[0]):
    cols[item] = i
plants = plants[1:g.ARTICLES_NUM+1]



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
                <a class="text-stone-700" href="/herbs.html">Herbs</a>
                <a class="text-stone-700" href="/about.html">About</a>
            </nav>
        </header>
    '''
    return html


def generate_header_light():
    header_html = generate_header_base()
    html = f'''
        <section class="header-divider">
            <div class="container-lg">
                {header_html}
            </div>
        </section>
    '''
    return html


def generate_header_transparent():
    header_html = generate_header_base()
    html = f'''
        <section class="header-divider">
            {header_html}
        </section>
    '''
    html = html.replace('text-stone-700', 'fg-white')
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
# PAGES
##############################################################################

def generate_home():
    header = generate_header_transparent()
    print(header)

    template = util.file_read('templates/home.html')
            
    template = template.replace('[meta_title]', 'Herbalism & Natural Healing')
    template = template.replace('[google_tag]', GOOGLE_TAG)
    template = template.replace('[author_name]', AUTHOR_NAME)
    template = template.replace('[header]', header)

    util.file_write(f'website/index.html', template)


def generate_about():
    header = generate_header_light()
    content = util.file_read(f'static/about.md')
    content = markdown.markdown(content, extensions=['markdown.extensions.tables'])
    
    template = util.file_read('templates/about.html')

    template = template.replace('[meta_title]', 'TerraWhisper | About')
    template = template.replace('[google_tag]', GOOGLE_TAG)
    template = template.replace('[author_name]', AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[content]', content)

    util.file_write(f'website/about.html', template)


def generate_page_herbalism():
    page_url = 'herbalism'

    content = util.file_read(f'static/{page_url}.md')
    content = markdown.markdown(content, extensions=['markdown.extensions.tables'])

    header = generate_header_light()

    page_html = util.file_read(f'static/{page_url}.html')

    page_html = page_html.replace('[meta_title]', 'Herbalism')
    page_html = page_html.replace('[google_tag]', GOOGLE_TAG)
    page_html = page_html.replace('[author_name]', AUTHOR_NAME)
    page_html = page_html.replace('[header]', header)
    page_html = page_html.replace('[content]', content)

    util.file_write(f'website/{page_url}.html', page_html)


def generate_page_herbalism_tea():
    sections = []
    articles_folderpath = 'database/articles/herbalism/tea'
    for article_filename in os.listdir(articles_folderpath):
        article_filepath = f'{articles_folderpath}/{article_filename}'
        data = util.json_read(article_filepath)
        condition = data['condition']
        url = data['url']
        sections.append(f'<li><a href="/{url}.html">{condition}</a></li>')
    sections = '<ul>' + ''.join(sections) + '</ul>'

    page_url = 'herbalism/tea'

    header = generate_header_light()

    page_html = util.file_read(f'static/{page_url}.html')

    page_html = page_html.replace('[meta_title]', 'Herbalism')
    page_html = page_html.replace('[google_tag]', GOOGLE_TAG)
    page_html = page_html.replace('[author_name]', AUTHOR_NAME)
    page_html = page_html.replace('[header]', header)
    page_html = page_html.replace('[sections]', sections)

    util.file_write(f'website/{page_url}.html', page_html)


def generate_page_herbs():
    articles_folderpath = 'database/articles/plants'
    articles_html = ''
    for plant in plants:
        latin_name = plant[cols['latin_name']].strip().capitalize()
        entity = latin_name.lower().replace(' ', '-')
        filepath_in = f'{articles_folderpath}/{entity}.json'

        data = util.json_read(filepath_in)
        try: latin_name = data['latin_name']
        except: latin_name = ''

        if latin_name == '': continue

        latin_name_dash = latin_name.lower().replace(' ', '-')

        try: title = data['title']
        except: title = ''

        if title != '':
            articles_html += f'''
                <a href="{latin_name_dash}.html">
                    <div>
                        <img src="images/{latin_name_dash}.jpg" alt="">
                        <h2 class="mt-0 mb-0">{title}</h2>
                    </div>
                </a>
            '''

    page_url = 'herbs'

    header = generate_header_light()

    page_html = util.file_read(f'templates/{page_url}.html')

    page_html = page_html.replace('[meta_title]', 'Herbs')
    page_html = page_html.replace('[google_tag]', GOOGLE_TAG)
    page_html = page_html.replace('[author_name]', AUTHOR_NAME)
    page_html = page_html.replace('[header]', header)
    page_html = page_html.replace('[articles]', articles_html)

    util.file_write(f'website/{page_url}.html', page_html)





##############################################################################
# ARTICLES TEA
##############################################################################

# def generate_articles():
#     IMG_FOLDER_TEA = 'C:/terrawhisper-assets/images/tea'
#     img_folders_names = os.listdir(IMG_FOLDER_TEA)
#     img_dict = {}
#     for img_folder_name in img_folders_names:
#         img_folders_files = os.listdir(f'{IMG_FOLDER_TEA}/{img_folder_name}')
#         img_dict[img_folder_name] = img_folders_files


#     ARTICLES_FOLDERPATH_MD = 'output/herbalism/tea'
#     ARTICLES_FOLDERPATH_HTML = 'website/herbalism/tea'
#     ARTICLES_FOLDERPATH_JSON = 'database/articles/herbalism/tea'
#     for article_filename in os.listdir(ARTICLES_FOLDERPATH_MD):
#         article_filepath_in = f'{ARTICLES_FOLDERPATH_MD}/{article_filename}'
#         article_filepath_out = f'{ARTICLES_FOLDERPATH_HTML}/{article_filename}'.replace('.md', '.html')
#         article_filepath_json = f'{ARTICLES_FOLDERPATH_JSON}/{article_filename}'.replace('.md', '.json')
#         article_md = util.file_read(f'{article_filepath_in}')

#         md = markdown.Markdown(extensions=['meta'])
#         md.convert(article_md)
#         title = md.Meta['title'][0]
        
#         header_html = generate_header_light()

#         word_count = len(article_md.split(' '))
#         reading_time_html = str(word_count // 200) + ' minutes'

#         article_html = md.convert(article_md)
#         article_html = generate_toc(article_html)

#         html = f'''
#             <!DOCTYPE html>
#             <html lang="en">

#             <head>
#                 <meta charset="UTF-8">
#                 <meta name="viewport" content="width=device-width, initial-scale=1.0">
#                 <meta name="author" content="{AUTHOR_NAME}">
#                 <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
#                 <link rel="stylesheet" href="/style.css">
#                 <title>{title}</title>
#                 {GOOGLE_TAG}
                
#             </head>

#             <body>
#                 {header_html}
                
#                 <section class="my-96">
#                     <div class="container">
#                         <div class="flex items-center justify-between mb-16">
#                             <div class="flex items-center gap-16">
#                                 <img class="author-image" src="/martin-pellizzer.jpg" alt="">
#                                 <address class="author">By <a rel="author" href="/about.html">{AUTHOR_NAME}</a></address>
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

#         curr_path = ''
#         for chunk in article_filepath_out.split('/')[:-1]:
#             curr_path += f'{chunk}/'
#             try: os.makedirs(f'{curr_path}')
#             except: pass
#         util.file_write(f'{article_filepath_out}', html)

#         # GET IMAGES
#         data = util.json_read(article_filepath_json)
#         condition = data['condition']
#         preparation = data['preparation']
#         condition_dash = condition.lower().strip().replace(' ', '-')
#         preparation_dash = preparation.lower().strip().replace(' ', '-')
#         herbs = [remedy['herb'] for remedy in data['remedies']]
        
#         # FEATURED IMAGE
#         featured_image_folder = herbs[0].lower().strip().replace(' ', '-')
#         try: img_name = img_dict[featured_image_folder].pop(0)
#         except: img_name = ''
#         if img_name != '':
#             image_path_in = f'{IMAGE_FOLDER}/{preparation_dash}/{featured_image_folder}/{img_name}'
#             image_path_out = f'website/images/herbal-{preparation_dash}-for-{condition_dash}' + '.jpg'
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
#                 image_path_out = f'website/images/{herb_dash}-{preparation_dash}-for-{condition_dash}' + '.jpg'
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


def generate_articles_herbalism_tea():
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
    for condition in conditions[:10]:
        condition_dash = condition.lower().strip().replace(' ', '-')
        article_filename = f'{articles_folderpath}/{condition_dash}.json'
        
        article_filepath_in = article_filename
        article_filepath_out = article_filename.replace('database/articles', 'website').replace('.json', '.html')

        data = util.json_read(article_filepath_in)
        article_html = ''

        title = ''
        try: title = data['keyword'].title()
        except: print(f'***** MISSING TITLE: {article_filepath_in}')
        article_html += f'<h1>{title}</h1>' + '\n'
        article_html += f'<p><img src="/images/herbal-tea-for-{condition_dash}-overview.jpg" alt="herbal teas for {condition} overview"></p>' + '\n'

        remedies = []
        try: remedies = data['remedies']
        except: print(f'***** MISSING REMEDIES: {article_filepath_in}')
        for index, remedy in enumerate(remedies[:10]):
            remedy_name = remedy['remedy_name']
            remedy_desc = remedy['remedy_desc']
            remedy_name_dash = remedy_name.lower().strip().replace(' ', '-')
            remedy_desc_formatted = util.text_format_1N1_html(remedy_desc)
            article_html += f'<h2>{index+1}. {remedy_name}</h2>' + '\n'
            article_html += f'<p><img src="/images/herbal-tea-for-{condition_dash}-{remedy_name_dash}.jpg" alt="herbal teas for {condition} {remedy_name.lower()}"></p>' + '\n'
            article_html += f'<p>{remedy_desc_formatted}</p>' + '\n'

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
                <meta name="author" content="{AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                
                <section class="my-96">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{AUTHOR_NAME}</a></address>
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

        chunks = article_filepath_out.split('/')
        chunk_curr = ''
        for chunk in chunks[:-1]:
            chunk_curr += chunk + '/'
            try: os.makedirs(chunk_curr)
            except: pass
        util.file_write(f'{article_filepath_out}', html)

        # GET IMAGES
        data = util.json_read(article_filepath_in)
        # print(article_filepath_in)
        condition = data['condition']
        preparation = data['preparation']
        condition_dash = condition.lower().strip().replace(' ', '-')
        preparation_dash = preparation.lower().strip().replace(' ', '-')
        herbs = [remedy['remedy_name'] for remedy in data['remedies']]
        
        # FEATURED IMAGE
        featured_image_folder = herbs[0].lower().strip().replace(' ', '-')
        try: img_name = img_dict[featured_image_folder].pop(0)
        except: img_name = ''
        if img_name != '':
            image_path_in = f'{IMAGE_FOLDER}/{preparation_dash}/{featured_image_folder}/{img_name}'
            image_path_out = f'website/images/herbal-{preparation_dash}-for-{condition_dash}-overview' + '.jpg'
            if not os.path.exists(image_path_out):
                img = Image.open(image_path_in)
                img.thumbnail((768, 768), Image.Resampling.LANCZOS)
                img.save(image_path_out, format='JPEG', optimize=True, quality=50)
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
            try: img_name = img_dict[herb_dash].pop(0)
            except: img_name = ''
            if img_name != '':
                image_path_in = f'{IMAGE_FOLDER}/{preparation_dash}/{herb_dash}/{img_name}'
                image_path_out = f'website/images/herbal-tea-for-{condition_dash}-{herb_dash}' + '.jpg'
                if not os.path.exists(image_path_out):
                    img = Image.open(image_path_in)
                    img.thumbnail((768, 768), Image.Resampling.LANCZOS)
                    img.save(image_path_out, format='JPEG', optimize=True, quality=50)
            else:
                try: scientific_name = util.get_scientific_name(herb)
                except: scientific_name = ''
                print(article_filepath_in)
                print(f'*** MISSING: {herb_dash} ({scientific_name}) {preparation_dash} ***')
                print()


def generate_articles_herbalism_tea_2():
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

        remedies = []
        try: remedies = data['remedies']
        except: print(f'***** MISSING REMEDIES: {article_filepath_in}')
        for index, remedy in enumerate(remedies[:10]):
            remedy_name = remedy['remedy_name']
            remedy_desc = remedy['remedy_desc']
            remedy_recipe = remedy['remedy_recipe']
            remedy_name_dash = remedy_name.lower().strip().replace(' ', '-')
            remedy_desc_formatted = util.text_format_1N1_html(remedy_desc)
            article_html += f'<h2>{index+1}. {remedy_name}</h2>' + '\n'
            article_html += f'<p><img src="/images/herbal-tea-for-{condition_dash}-{remedy_name_dash}.jpg" alt="herbal teas for {condition} {remedy_name.lower()}"></p>' + '\n'
            article_html += f'<p>{remedy_desc_formatted}</p>' + '\n'
            article_html += f'<ol>' + '\n'
            for item in remedy_recipe:
                article_html += f'<li>{item}</li>' + '\n'
            article_html += f'</ol>' + '\n'

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
                <meta name="author" content="{AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                
                <section class="my-96">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{AUTHOR_NAME}</a></address>
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

def generate_articles_plants():
    articles_folderpath = 'database/articles/plants'
    for plant in plants:
        latin_name = plant[cols['latin_name']].strip().capitalize()
        entity = latin_name.lower().replace(' ', '-')
        article_filepath_in = f'{articles_folderpath}/{entity}.json'
        article_filepath_out = f'website/{entity}.html'

        data = util.json_read(article_filepath_in)
        try: title = data['title']
        except: title = ''
        if title == '':
            print(f'MISSING TITLE: {article_filepath_in}')
            continue
        latin_name = data['latin_name']
        latin_name_dash = latin_name.lower().replace(' ', '-')
        intro = data['intro']
        medicine = data['medicine']
        horticulture = data['horticulture']
        botany = data['botany']

        article_html = ''
        title_html = f'<h1>{title}</h1>'
        image_featured_html = f'<p><img src="/images/{latin_name_dash}.jpg" alt="{latin_name}"></p>'
        intro_html = '\n'.join([f'<p>{paragraph}</p>' for paragraph in intro])
        medicine_title_html = f'<h2>What are the medicinal properties of {latin_name}?</h2>'
        medicine_image_html = f'<p><img src="/images/{latin_name_dash}-medicine.jpg" alt="{latin_name} medicine"></p>'
        medicine_paragraphs_html = ''.join([f'<p>{paragraph}</p>' for paragraph in medicine])
        medicine_link_html = f'<p>Here\'s an article explaining in detail the <a href="/{entity}/medicine.html">medicinal aspects of {latin_name}</a>.</p>'
        horticulture_title_html = f'<h2>What are the horticultural conditions of {latin_name}?</h2>'
        horticulture_image_html = f'<p><img src="/images/{latin_name_dash}-horticulture.jpg" alt="{latin_name} horticulture"></p>'
        horticulture_paragraphs_html = ''.join([f'<p>{paragraph}</p>' for paragraph in horticulture])
        botany_title_html = f'<h2>What are the botanical characteristics of {latin_name}?</h2>'
        botany_image_html = f'<p><img src="/images/{latin_name_dash}-botany.jpg" alt="{latin_name} botany"></p>'
        botany_paragraphs_html = ''.join([f'<p>{paragraph}</p>' for paragraph in botany])

        article_html += title_html + '\n'
        article_html += image_featured_html + '\n'
        article_html += intro_html + '\n'
        article_html += medicine_title_html + '\n'
        article_html += medicine_image_html + '\n'
        article_html += medicine_paragraphs_html + '\n'
        article_html += medicine_link_html + '\n'
        article_html += horticulture_title_html + '\n'
        article_html += horticulture_image_html + '\n'
        article_html += horticulture_paragraphs_html + '\n'
        article_html += botany_title_html + '\n'
        article_html += botany_image_html + '\n'
        article_html += botany_paragraphs_html + '\n'

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
                <meta name="author" content="{AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                
                <section class="my-96">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{AUTHOR_NAME}</a></address>
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
        folderpath = f'{IMAGE_FOLDER}/plants/{latin_name_dash}'
        filenames = os.listdir(folderpath)
        filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]

        filepath_in = filepaths_in[0]
        filepath_out = f'website/images/{latin_name_dash}.jpg'
        img = Image.open(filepath_in)
        img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        img.save(filepath_out, format='JPEG', optimize=True, quality=50)

        filepath_in = filepaths_in[1]
        filepath_out = f'website/images/{latin_name_dash}-medicine.jpg'
        img = Image.open(filepath_in)
        img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        img.save(filepath_out, format='JPEG', optimize=True, quality=50)

        filepath_in = filepaths_in[2]
        filepath_out = f'website/images/{latin_name_dash}-horticulture.jpg'
        img = Image.open(filepath_in)
        img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        img.save(filepath_out, format='JPEG', optimize=True, quality=50)

        filepath_in = filepaths_in[3]
        filepath_out = f'website/images/{latin_name_dash}-botany.jpg'
        img = Image.open(filepath_in)
        img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        img.save(filepath_out, format='JPEG', optimize=True, quality=50)

        # quit()


def articles_plants():
    articles_folderpath = 'database/articles/plants'
    for plant in plants:
        latin_name = plant[cols['latin_name']].strip().capitalize()
        entity = latin_name.lower().replace(' ', '-').replace('.', '')
        article_filepath_in = f'{articles_folderpath}/{entity}.json'
        article_filepath_out = f'website/{entity}.html'

        print(article_filepath_in)
        data = util.json_read(article_filepath_in)
        try: title = data['title']
        except: title = ''
        if title == '':
            print(f'MISSING TITLE: {article_filepath_in}')
            continue
        latin_name = data['latin_name']
        latin_name_dash = latin_name.lower().replace(' ', '-')
        intro = data['intro']
        medicine_desc = data['medicine_desc']
        horticulture_desc = data['horticulture_desc']
        botany_desc = data['botany_desc']

        article_html = ''

        article_html += f'<h1>{title}</h1>' + '\n'
        article_html += f'<p><img src="/images/{latin_name_dash}-overview.jpg" alt="{latin_name}"></p>' + '\n'
        article_html += util.text_format_1N1_html(intro) + '\n'
        article_html += f'<h2>What are the medicinal properties of {latin_name}?</h2>' + '\n'
        article_html += f'<p><img src="/images/{latin_name_dash}-medicine.jpg" alt="{latin_name} medicine"></p>' + '\n'
        article_html += f'<p>{medicine_desc[0]}</p>' + '\n'
        article_html += f'<p>{medicine_desc[1]}</p>' + '\n'
        article_html += f'<p>{medicine_desc[2]}</p>' + '\n'
        article_html += f'<p>{medicine_desc[3]}</p>' + '\n'
        article_html += f'<p>{medicine_desc[4]}</p>' + '\n'
        article_html += f'<p>Here\'s an article explaining in detail the <a href="/{entity}/medicine.html">medicinal aspects of {latin_name}</a>.</p>' + '\n'
        article_html += f'<h2>What are the horticultural conditions of {latin_name}?</h2>' + '\n'
        article_html += f'<p><img src="/images/{latin_name_dash}-horticulture.jpg" alt="{latin_name} medicine"></p>' + '\n'
        article_html += f'<p>{horticulture_desc[0]}</p>' + '\n'
        article_html += f'<p>{horticulture_desc[1]}</p>' + '\n'
        article_html += f'<p>{horticulture_desc[2]}</p>' + '\n'
        article_html += f'<p>{horticulture_desc[3]}</p>' + '\n'
        article_html += f'<p>{horticulture_desc[4]}</p>' + '\n'
        article_html += f'<h2>What are the botanical characteristics of {latin_name}?</h2>' + '\n'
        article_html += f'<p><img src="/images/{latin_name_dash}-botany.jpg" alt="{latin_name} medicine"></p>' + '\n'
        article_html += f'<p>{botany_desc[0]}</p>' + '\n'
        article_html += f'<p>{botany_desc[1]}</p>' + '\n'
        article_html += f'<p>{botany_desc[2]}</p>' + '\n'
        article_html += f'<p>{botany_desc[3]}</p>' + '\n'
        article_html += f'<p>{botany_desc[4]}</p>' + '\n'

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
                <meta name="author" content="{AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                
                <section class="my-96">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{AUTHOR_NAME}</a></address>
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
        ]

        for i, filepath_out in enumerate(filepaths_out):
            if os.path.exists(filepath_out): continue
            filepath_in = filepaths_in[i]
            img = Image.open(filepath_in)
            img.thumbnail((768, 768), Image.Resampling.LANCZOS)
            img.save(filepath_out, format='JPEG', optimize=True, quality=50)



        # IMAGES
        # folderpath = f'{IMAGE_FOLDER}/plants/{latin_name_dash}'
        # filenames = os.listdir(folderpath)
        # filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]

        # filepath_in = filepaths_in[0]
        # filepath_out = f'website/images/{latin_name_dash}.jpg'
        # img = Image.open(filepath_in)
        # img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        # img.save(filepath_out, format='JPEG', optimize=True, quality=50)

        # filepath_in = filepaths_in[1]
        # filepath_out = f'website/images/{latin_name_dash}-medicine.jpg'
        # img = Image.open(filepath_in)
        # img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        # img.save(filepath_out, format='JPEG', optimize=True, quality=50)

        # filepath_in = filepaths_in[2]
        # filepath_out = f'website/images/{latin_name_dash}-horticulture.jpg'
        # img = Image.open(filepath_in)
        # img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        # img.save(filepath_out, format='JPEG', optimize=True, quality=50)

        # filepath_in = filepaths_in[3]
        # filepath_out = f'website/images/{latin_name_dash}-botany.jpg'
        # img = Image.open(filepath_in)
        # img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        # img.save(filepath_out, format='JPEG', optimize=True, quality=50)

        # quit()


def gen_articles_plant_medicine():
    articles_folderpath = 'database/articles/plants'
    for plant in plants:
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')
        article_filepath = f'{articles_folderpath}/{entity}/medicine.json'

        # DEBUG
        # if entity != 'apium-graveolens': continue

        # if not os.path.exists(article_filepath): continue

        article_filepath_in = article_filepath
        article_filepath_out = article_filepath.replace(articles_folderpath, 'website').replace('.json', '.html')

        data = util.json_read(article_filepath_in)
        article_html = ''

        try: title = data['title']
        except: title = ''
        article_html += f'<h1>{title}</h1>' + '\n'
        article_html += f'<p><img src="/images/{entity}-medicine-overview.jpg" alt="{latin_name}"></p>' + '\n'

        try: intro = data['intro']
        except: intro = ''
        intro_html = '\n'.join([f'<p>{paragraph}</p>' for paragraph in intro]) + '\n'
        intro_html_start = intro_html.split('. ')[0]
        intro_html_mid = '. '.join(intro_html.split('. ')[1: -1])
        intro_html_end = intro_html.split('. ')[-1]
        article_html += f'<p>{intro_html_start}.</p>' + '\n'
        article_html += f'<p>{intro_html_mid}.</p>' + '\n'
        article_html += f'<p>{intro_html_end}</p>' + '\n'

        article_html += f'<h2>What are the health benefits of {latin_name} ({common_name})?</h2>' + '\n'
        article_html += f'<p><img src="/images/{entity}-medicine-benefits.jpg" alt="{latin_name}"></p>' + '\n'
        try: benefits_text = data['benefits_text'][0]
        except: benefits_text = ''
        if benefits_text:
            article_html += util.text_format_1N1_html(benefits_text)
        try: benefits_list = data['benefits_list']
        except: benefits_list = []
        if benefits_list:
            article_html += f'<p>The following list shows the <a href="/{entity}/medicine/benefits.html">health benefits of {latin_name}</a>.</p>' + '\n'
            benefits_list_html = lst_to_html_bold(benefits_list)
            article_html += benefits_list_html + '\n'

        try: constituents_list = data['constituents_list']
        except: constituents_list = []
        if constituents_list:
            article_html += f'<h2>What are the active constituents of {latin_name} ({common_name})?</h2>' + '\n'
            article_html += f'<p><img src="/images/{entity}-medicine-constituents.jpg" alt="{latin_name}"></p>' + '\n'
            article_html += f'<p>The following list shows the active constituents of {latin_name}.</p>' + '\n'
            constituents_list_html = lst_to_html_bold(constituents_list)
            article_html += constituents_list_html + '\n'

        try: preparations_list = data['preparations_list']
        except: preparations_list = []
        if preparations_list:
            article_html += f'<h2>What are the medicinal preparations of {latin_name} ({common_name})?</h2>' + '\n'
            article_html += f'<p><img src="/images/{entity}-medicine-preparations.jpg" alt="{latin_name}"></p>' + '\n'
            article_html += f'<p>The following list shows the medicinal preparations of {latin_name}.</p>' + '\n'
            preparations_list_html = lst_to_html_bold(preparations_list)
            article_html += preparations_list_html + '\n'

        try: side_effects_list = data['side_effects_list']
        except: side_effects_list = []
        if side_effects_list:
            article_html += f'<h2>What are the possible side effects of using {latin_name} ({common_name}) for medicinal purposes?</h2>' + '\n'
            article_html += f'<p><img src="/images/{entity}-medicine-side-effects.jpg" alt="{latin_name}"></p>' + '\n'
            article_html += f'<p>The following list shows the possible side effects of {latin_name} for medicinal purposes.</p>' + '\n'
            side_effects_list_html = lst_to_html_bold(side_effects_list)
            article_html += side_effects_list_html + '\n'

        try: precautions_list = data['precautions_list']
        except: precautions_list = []
        if precautions_list:
            article_html += f'<h2>What are the precautions to take when using {latin_name} ({common_name}) medicinally?</h2>' + '\n'
            article_html += f'<p><img src="/images/{entity}-medicine-precautions.jpg" alt="{latin_name}"></p>' + '\n'
            article_html += f'<p>The following list shows the precautions to take when using {latin_name} medicinally.</p>' + '\n'
            precautions_list_html = lst_to_html_bold(precautions_list)
            article_html += precautions_list_html + '\n'
        
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
                <meta name="author" content="{AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                
                <section class="my-96">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{AUTHOR_NAME}</a></address>
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

        chunks = article_filepath_out.split('/')
        chunk_curr = ''
        for chunk in chunks[:-1]:
            chunk_curr += chunk + '/'
            try: os.makedirs(chunk_curr)
            except: pass

        util.file_write(f'{article_filepath_out}', html)

        # IMAGES
        folderpath = f'{IMAGE_FOLDER}/plants/{entity}'
        filenames = os.listdir(folderpath)
        filepaths_in = [f'{folderpath}/{filename}' for filename in filenames]

        random.shuffle(filepaths_in)

        filepath_in = filepaths_in[0]
        filepath_out = f'website/images/{entity}-medicine-overview.jpg'
        img = Image.open(filepath_in)
        img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        img.save(filepath_out, format='JPEG', optimize=True, quality=50)

        filepath_in = filepaths_in[1]
        filepath_out = f'website/images/{entity}-medicine-benefits.jpg'
        img = Image.open(filepath_in)
        img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        img.save(filepath_out, format='JPEG', optimize=True, quality=50)

        filepath_in = filepaths_in[2]
        filepath_out = f'website/images/{entity}-medicine-constituents.jpg'
        img = Image.open(filepath_in)
        img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        img.save(filepath_out, format='JPEG', optimize=True, quality=50)

        filepath_in = filepaths_in[3]
        filepath_out = f'website/images/{entity}-medicine-preparations.jpg'
        img = Image.open(filepath_in)
        img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        img.save(filepath_out, format='JPEG', optimize=True, quality=50)
        
        filepath_in = filepaths_in[4]
        filepath_out = f'website/images/{entity}-medicine-side-effects.jpg'
        img = Image.open(filepath_in)
        img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        img.save(filepath_out, format='JPEG', optimize=True, quality=50)
        
        filepath_in = filepaths_in[5]
        filepath_out = f'website/images/{entity}-medicine-precautions.jpg'
        img = Image.open(filepath_in)
        img.thumbnail((768, 768), Image.Resampling.LANCZOS)
        img.save(filepath_out, format='JPEG', optimize=True, quality=50)


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
            article_html += f'<p>The following list shows the active constituents of {latin_name}.</p>' + '\n'
            article_html += lst_to_html_bold(data['constituents_list']) + '\n'
        except: print('MISSING >>>>> CONSTITUENTS LIST\n')

        article_html += f'<h2>What are the medicinal preparations of {latin_name} ({common_name})?</h2>' + '\n'
        article_html += f'<p><img src="/images/{entity}-medicine-preparations.jpg" alt="{latin_name}"></p>' + '\n'
        try: article_html += util.text_format_1N1_html(data['preparations_text']) + '\n'
        except: print('MISSING >>>>> PREPARATIONS TEXT\n')
        try:
            article_html += f'<p>The following list shows the medicinal preparations of {latin_name}.</p>' + '\n'
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
                {GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                
                <section class="my-96">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{AUTHOR_NAME}</a></address>
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


def gen_articles_plant_medicine_benefits():
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

        try: title = data['title']
        except: title = ''

        try: benefits = data['benefits']
        except: benefits = []

        article_html = ''
        article_html += f'<h1>{title}</h1>' + '\n'
        article_html += f'<p><img src="/images/{entity}.jpg" alt="{latin_name}"></p>' + '\n'

        images_plant_foldername = f'{IMAGE_FOLDER}/plants/{entity}'
        try: images_plant_filename = os.listdir(images_plant_foldername)
        except: images_plant_filename = None
        
        images_filepath = []
        if images_plant_filename:
            images_filepath = [f'{images_plant_foldername}/{filename}' for filename in images_plant_filename]

        for i, benefit in enumerate(benefits[:10]):
            benefit_name = benefit['name'].strip()
            benefit_name_dash = benefit_name.lower().replace(' ' , '-')
            article_html += f'<h2>{i+1}. {benefit_name}</h2>' + '\n'

            try: definition = benefit['definition']
            except: definition = ''
            if definition != '': article_html += f'<p>{definition}</p>' + '\n'
            else: print(f'MISSING DEFINITION: {article_filepath_in} >> {benefit_name}')

            constituents_list_intro_html = f'<p>{latin_name} {benefit_name.lower()} thanks to the active constituents listed below.</p>'
            article_html += constituents_list_intro_html + '\n'

            try: constituents = benefit['constituents']
            except: constituents = []
            constituents_list_html = ''
            constituents_list_html += '<ul>'
            for constituent in constituents:
                constituents_list_html += f'<li>{constituent}</li>'
            constituents_list_html += '</ul>'
            article_html += constituents_list_html + '\n'

            try: constituents_text = benefit['constituents_text']
            except: constituents_text = ''
            if constituents_text != '':
                constituents_text_html = ''
                sentences = constituents_text.split('. ')
                constituents_text_html += f'<p>{sentences[0]}.</p>'
                central_section = ". ".join(sentences[1:-1])
                if central_section != '':
                    constituents_text_html += f'<p>{central_section}.</p>'
                constituents_text_html += f'<p>{sentences[-1]}</p>'
                article_html += constituents_text_html + '\n'
            else: print(f'MISSING ARTICLE CONSTITUENTS TEXT: {article_filepath_in} >> {benefit_name}')

            if images_filepath:
                image_filepath_in = images_filepath.pop(0)
                image_filepath_out = f'website/images/{entity}-medicine-{benefit_name_dash}.jpg'
                if not os.path.exists(image_filepath_out):
                    img = Image.open(image_filepath_in)
                    img.thumbnail((768, 768), Image.Resampling.LANCZOS)
                    img.save(image_filepath_out, format='JPEG', optimize=True, quality=50)
                article_html += f'<p><img src="/images/{entity}-medicine-{benefit_name_dash}.jpg" alt="{latin_name} medicine {benefit_name.lower()}"></p>' + '\n'

            conditions_list_intro_html = f'<p>The following list shows some health problems that can be relieved by {latin_name} thanks to the fact that it {benefit_name.lower()}.</p>'
            article_html += conditions_list_intro_html + '\n'

            try: conditions = benefit['conditions']
            except: conditions = []
            conditions_list_html = ''
            conditions_list_html += '<ul>'
            for condition in conditions:
                conditions_list_html += f'<li>{condition}</li>'
            conditions_list_html += '</ul>'
            article_html += conditions_list_html + '\n'

            try: conditions_text = benefit['conditions_text']
            except: conditions_text = ''
            if conditions_text != '':
                conditions_text_html = ''
                sentences = conditions_text.split('. ')
                conditions_text_html += f'<p>{sentences[0]}.</p>'
                central_section = ". ".join(sentences[1:-1])
                if central_section != '':
                    conditions_text_html += f'<p>{central_section}.</p>'
                conditions_text_html += f'<p>{sentences[-1]}</p>'
                article_html += conditions_text_html + '\n'
            else: print(f'MISSING ARTICLE CONDITIONS TEXT: {article_filepath_in} >> {benefit_name}')



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
                <meta name="author" content="{AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                
                <section class="my-96">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{AUTHOR_NAME}</a></address>
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

        chunks = article_filepath_out.split('/')
        chunk_curr = ''
        for chunk in chunks[:-1]:
            chunk_curr += chunk + '/'
            try: os.makedirs(chunk_curr)
            except: pass

        util.file_write(f'{article_filepath_out}', html)


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
                <meta name="author" content="{AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                
                <section class="my-96">
                    <div class="container">
                        <div class="flex items-center justify-between mb-16">
                            <div class="flex items-center gap-16">
                                <img class="author-image" src="/martin-pellizzer.jpg" alt="">
                                <address class="author">By <a rel="author" href="/about.html">{AUTHOR_NAME}</a></address>
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





##############################################################################
# STATIC FILES
##############################################################################

# TRANSFER STATIC FILES
shutil.copy2('style.css', 'website/style.css')

# COMPRESS AND TRASFER IMAGES
img = Image.open('assets/images/medicinal-herbs.png')
img = util.img_resize(img, 1920, 1080)
img.save(f'website/images/herbalism-natural-remedies.jpg', format='JPEG', optimize=True, quality=50)

img = Image.open('assets/images/woman-frustrated-with-modern-medicinals.png')
img = util.img_resize(img, 768, 768)
img.save(f'website/images/woman-frustrated-with-modern-medicinals.jpg', format='JPEG', optimize=True, quality=50)

shutil.copy2('assets/images/martin-pellizzer-300x300.jpg', f'website/images/martin-pellizzer-300x300.jpg')





# generate_articles_herbalism_tea_2()
# generate_articles_plants()
articles_plants()
articles_medicine()
articles_benefits()

generate_home()
generate_page_herbs()
generate_about()

# generate_page_herbalism()
# generate_page_herbalism_tea()


