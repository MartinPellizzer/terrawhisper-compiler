import os

from lib import g
from lib import io
from lib import utils


def html_head(meta_title, meta_description='', stylesheet='/style.css'):
    html = f'''
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="{stylesheet}">
            <title>{meta_title}</title>
            <meta name="description" content="{meta_description}">
            {g.GOOGLE_ADSENSE_AD_AUTO_TAG}
            {g.GOOGLE_ANALYTICS}
        </head>
    '''
    return html

##############################################
# ;header
##############################################
def html_header():
    html = f'''
        <header>
            <div class="header container-xl">
                <div class="logo">
                    <a href="/">TERRA WHISPER</a>
                </div>
                <nav class="navigation">
                    <input type="checkbox" class="toggle-menu">
                    <div class="hamburger"></div>
                    <ul class="menu">
                        <li><a href="/herbs.html">HERBS</a></li>
                        <li><a href="/preparations.html">PREPARATIONS</a></li>
                        <li><a href="/ailments.html">AILMENTS</a></li>
                        <li><a href="/equipment.html">EQUIPMENT</a></li>
                        <li><a href="/shop.html">SHOP</a></li>
                    </ul>
                </nav>
            </div>
        </header>
    '''
    return html


def html_footer():
    html = f'''
        <footer> 
            <div class="footer">
                <span>terrawhisper.com | all rights reserved</span>
                <nav class="flex gap-16">
                    <a class="no-underline" href="/">About</a>
                    <a class="no-underline" href="/">Contact</a>
                </nav>
            </div>
        </footer>
    '''
    return html

def footer():
    html = f'''
        <footer class="footer">
            <span>© TerraWhisper.com 2024 | All Rights Reserved</span>
            <div class="flex gap-24">
                <a href="/privacy-policy.html">Privacy Policy</a>
                <a href="/cookie-policy.html">Cookie Policy</a>
            </div>
        </footer>
    '''
    return html

def footer_2():
    html = f'''
        <footer class="footer-2">
            <span>© TerraWhisper.com 2024 | All Rights Reserved</span>
            <div class="flex gap-24">
                <a href="/privacy-policy.html">Privacy Policy</a>
                <a href="/cookie-policy.html">Cookie Policy</a>
            </div>
        </footer>
    '''
    return html

def table_of_contents(content_html):
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
    toc_li = []
    table_of_contents_html += '<div class="toc">'
    table_of_contents_html += '<p class="toc-title">Table of Contents</p>'
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

def toc(html_in):
    html_out = ''
    json_toc = []
    index = 0
    for line in html_in.split('\n'):
        line = line.strip()
        if line.startswith('<h2'):
            json_toc.append({
                'tag': 'h2',
                'index': index,
                'headline': line.split('>')[1].split('<')[0],
            })
            line = (line.replace('<h2', f'<h2 id="{index}"'))
            index +=1
        html_out += line
        html_out += '\n'
    return html_out, json_toc

def toc_json_to_html_article(json_toc):
    html_toc = ''
    html_toc += '<ul>'
    for item_toc in json_toc:
        index = item_toc['index']
        headline = item_toc['headline']
        html_toc += f'<li><a href="#{index}">{headline}</a></li>'
    html_toc += '</ul>'
    return html_toc

def toc_json_to_html_sidebar(json_toc):
    html_toc_list = ''
    html_toc_list += '<ul>'
    for item_toc in json_toc:
        index = item_toc['index']
        headline = item_toc['headline']
        html_toc_list += f'''
            <li><a href="#{index}">{headline}</a></li>
        '''
    html_toc_list += '</ul>'
    html_toc = ''
    html_toc += f'''
        <div class="sidebar-toc">
            <div class="sidebar-toc-header">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>
                <p>On this page</p>
            </div>
                {html_toc_list}
            </ul>
        </div>
    '''
    return html_toc

def meta(content, lastmod):
    year = lastmod.split('-')[0]
    month = lastmod.split('-')[1]
    if month == '01': month = "Jan"
    if month == '02': month = "Feb"
    if month == '03': month = "Mar"
    if month == '04': month = "Apr"
    if month == '05': month = "May"
    if month == '06': month = "Jun"
    if month == '07': month = "Jul"
    if month == '08': month = "Aug"
    if month == '09': month = "Sep"
    if month == '10': month = "Oct"
    if month == '11': month = "Nov"
    if month == '12': month = "Dec"
    day = lastmod.split('-')[2]
    reading_time = str(len(content.split(' ')) // 200) + ' minutes'
    if False:
        html = f'''
            <div class="flex items-center justify-between mb-8">
                <div class="flex items-center gap-16">
                    <img src="/images-static/leen-randell.jpg" alt="profile picture of leen randell">
                    <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
                </div>
                <span>{reading_time}</span>
            </div>
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-16">
                    <p>Last updated: {month} {day}, {year}</p>
                </div>
                <span></span>
            </div>
        '''
    if 0:
        html = f'''
            <div class="flex items-center justify-between mb-16">
                <div class="flex items-center gap-8">
                    <img class="profile-pic-meta" width=64 height=64 src="/images-static/leen-randell.jpg" alt="profile picture of leen randell">
                    <p class="mb-0">By <a class="uppercase text-black no-underline font-bold" rel="author" href="">{g.AUTHOR_NAME}</a></p>
                </div>
                <p class="mb-0">Updated: {month} {day}, {year}</p>
            </div>
        '''
    if 1:
        html = f'''
            <div class="flex items-center justify-between mb-16">
                <div class="flex items-center gap-8">
                    <p class="mb-0 text-14">By <a class="uppercase text-black no-underline font-bold" rel="author" href="">{g.AUTHOR_NAME}</a></p>
                </div>
                <p class="mb-0">Updated: {month} {day}, {year}</p>
            </div>
        '''
    return html


#########################################################################
# ;study
#########################################################################
def study_snippet_html_1(study_snippet_text):
    html += f'''
        <div class="study" style="margin-bottom: 16px;">
            <div class="study-header">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
                </svg>
                <p>Related Study</p>
            </div>
            <p>
                {study_snippet_text}
            </p>
        </div>
    '''
    return html

def study_snippet_html(study_snippet_text):
    html = f'''
        <div class="study" style="margin-bottom: 16px;">
            <p>
                {study_snippet_text}
            </p>
        </div>
    '''
    return html

#########################################################################
# ;breadcrumbs
#########################################################################
def breadcrumbs(filepath):
    breadcrumbs = ['<a href="/"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"/></svg></a>']
    breadcrumbs_path = filepath.replace('website/', '')
    chunks = breadcrumbs_path.split('/')
    filepath_curr = ''
    for chunk in chunks[:-1]:
        filepath_curr += f'/{chunk}'
        chunk = chunk.strip().replace('-', ' ').title()
        breadcrumbs.append(f'<a href="{filepath_curr}.html">{chunk}</a>')
    breadcrumbs = '<span> > </span>'.join(breadcrumbs)
    breadcrumbs += f'<span> > {chunks[-1].strip().replace(".html", "").replace("-", " ").title()}</span>'
    breadcrumbs_section = f'''
        <section class="breadcrumbs">
            {breadcrumbs}
        </section>
    '''
    
    return breadcrumbs_section

###########################################
# lead magnet
###########################################
def lead_magnet_html_0000():
    with open('assets/newsletter/bundle_herb-drying-checklist_herb-card-pk1_herb-tea-shopping-list.txt') as f: sign_in_form_html = f.read()
    html = f'''
        <div class="bg-lightgray">
            <div class="container-sm pt-16 px-24">
                <p class="text-center mb-8">Also you may be interested in...</p>
                <p class="text-32 helvetica-bold text-orange text-center mb-8">TODAY'S FREE BOUNDLE</p>
                <p class="text-24 helvetica-bold text-center mb-8">Herb Drying Checklist + </br>Herbal Tea Shopping List + </br>Medicinal Herbs Flashcards</p>
                <p class="text-center">Enter you best email address below to receive this bundle (3 product valued $19.95) for FREE + exclusive access to The Aphotecary Letter.</p>
                <p class="text-24 helvetica-bold text-center mb-0"><s>$19.95</s> -> $0.00</p>
                {sign_in_form_html}
            </div>
        </div>
    '''
    return html

def lead_magnet_html_0001():
    with open('assets/newsletter/bundle_herb-drying-checklist_herb-card-pk1_herb-tea-shopping-list.txt') as f: 
        sign_in_form_html = f.read()
    title = 'The Ultimate Herb Drying Checklist'
    description = 'How to easily dry herbs, that don\'t grow mold, and keep their medicinal power for 1+ year.'
    html = f'''
        <div style="margin-top: 24px;" class="bg-lightgray">
            <div style="padding: 24px;" class="mob-flex gap-24">
                <div class="flex-1" style="margin-bottom: 16px;">
                    <p style="font-size: 20px;" class="helvetica-bold text-center mb-8">FREE</p>
                    <p style="font-size: 40px; line-height: 1;" class="helvetica-bold text-center mb-8">{title}</p>
                    <p class="text-center">{description}</p>
                    <p style="margin-bottom: 0;" class="text-center">Enter your best email below to receive your free checklist.</p>
                    {sign_in_form_html}
                </div>
                <div class="flex-1">
                    <img src="/images/shop/herb-drying-checklist-blurred.jpg" alt="">
                </div>
            </div>
        </div>
    '''
    return html

def lead_magnet_html():
    with open('assets/newsletter/herb-drying-checklist-js.txt') as f: 
        sign_in_script = f.read()
    with open('assets/newsletter/herb-drying-checklist-component.txt') as f: 
        sign_in_form = f.read()
    title = 'The Ultimate Herb Drying Checklist'
    description = 'How to easily dry herbs, that don\'t grow mold, and keep their medicinal power for 1+ year.'
    html = f'''
        <div style="margin-top: 24px;" class="bg-lightgray">
            <div style="padding: 24px;" class="mob-flex gap-24">
                <div class="flex-1" style="margin-bottom: 16px;">
                    <p style="font-size: 20px;" class="helvetica-bold text-center mb-8">FREE</p>
                    <p style="font-size: 40px; line-height: 1;" class="helvetica-bold text-center mb-8">{title}</p>
                    <p class="text-center">{description}</p>
                    <p style="margin-bottom: 0;" class="text-center">Enter your best email below to receive your free checklist.</p>
                    {sign_in_script}
                    {sign_in_form}
                </div>
                <div class="flex-1">
                    <img src="/images/shop/herb-drying-checklist-blurred.jpg" alt="">
                </div>
            </div>
        </div>
    '''
    return html

################################################
# ;card
################################################
def card_art_html(href, src, title):
    html = f'''
        <a class="article-card no-underline text-black" href="{href}">
            <img class="mb-16" src="{src}" alt="herb drying checklist">
            <h2 class="h2-plain text-18 mb-12">{title}</h2>
        </a>
    '''
    return html

################################################
# ;amazon
################################################
def amazon_json(obj, preparation_slug):
    plant_slug = utils.sluggify(obj['herb_name_scientific'])
    products_jsons_folderpath = f'{g.VAULT}/amazon/{preparation_slug}/json/{plant_slug}' 
    if not os.path.exists(products_jsons_folderpath): 
        return ''
    products_jsons_filepaths = [
        f'{products_jsons_folderpath}/{x}' 
        for x in os.listdir(products_jsons_folderpath)
    ]
    # order filepaths by popularity
    products_jsons = []
    for i, product_json_filepath in enumerate(products_jsons_filepaths):
        product_data = io.json_read(product_json_filepath)
        if 'reviews_score_total' in product_data:
            product_asin = product_json_filepath.split('/')[-1].replace('.json', '')
            reviews_num = int(product_data['reviews_num'].replace('(', '').replace(')', ''))
            reviews_score = float(product_data['reviews_score'])
            reviews_score_total = reviews_num * reviews_score
            products_jsons.append({
                'product_asin': product_asin, 
                'reviews_score_total': reviews_score_total
            })
    products_jsons_ordered = sorted(products_jsons, key=lambda x: x['reviews_score_total'], reverse=True)
    products_jsons_filepaths_ordered = []
    for product_json in products_jsons_ordered:
        product_asin = product_json['product_asin']
        product_filepath = f'{products_jsons_folderpath}/{product_asin}.json'
        products_jsons_filepaths_ordered.append(product_filepath)
    products_jsons_filepaths_ordered = products_jsons_filepaths_ordered
    product_json_filepath = products_jsons_filepaths_ordered[0]
    json_product = io.json_read(product_json_filepath)
    affiliate_product = {
        'url': json_product['url'],
        'affiliate_link': json_product['affiliate_link'],
        'title': json_product['title'],
    }
    return affiliate_product

def amazon_html(obj):
    if 'preparation_amazon' in obj and obj['preparation_amazon'] != '':
        herb_name_scientific = obj['herb_name_scientific']
        url = obj['preparation_amazon']['affiliate_link']
        title = obj['preparation_amazon']['title']
        html = ''
        html += f'<div class="bg-lightgray">\n'
        html += f'<div class="container-sm py-16 px-24">\n'
        html += f'<p class="text-32 text-black text-center mb-8">{herb_name_scientific.title()} Tea on Amazon</p>\n'
        html += f'<p class="text-16 text-black helvetica-bold text-center">{title}</p>\n'
        html += f'<div class="text-center">\n'
        html += f'<a class="button-amazon mb-16" href="{url}" target="_blank">Buy on Amazon</a>\n'
        html += f'</div>\n'
        html += f'<p class="text-14 text-center mb-0"><i>Disclaimer: We earn a commission if you click this link and make a purchase at no additional cost to you.</i></p>\n'
        html += f'</div>\n'
        html += f'</div>\n'
        return html
    else:
        return ''

