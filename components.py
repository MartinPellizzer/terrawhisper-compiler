import os

from oliark_io import json_read, json_write

import g
import utils

def html_head(title, stylesheet='/style.css'):
    html = f'''
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="{stylesheet}">
            <title>{title}</title>
            {g.GOOGLE_ADSENSE_AD_AUTO_TAG}
            {g.GOOGLE_ANALYTICS}
        </head>
    '''
    return html

def html_header():
    html = f'''
        <header>
            <div class="header container-xl">
                <div class="header-logo">
                    <a class="" href="/">
                        TerraWhisper
                        <!-- <img height="64" src="/images-static/terrawhisper-logo.png" alt="logo of terrawhisper"> -->
                    </a>
                </div>
                <nav class="navigation">
                    <input type="checkbox" class="toggle-menu">
                    <div class="hamburger"></div>
                    <ul class="menu">
                        <li><a href="/herbs.html">Herbs</a></li>
                        <li><a href="/remedies.html">Remedies</a></li>
                    </ul>
                </nav>
            </div>
        </header>
    '''
    return html

def html_header_2():
    html = f'''
        <header>
            <div class="header container-xl">
                <div class="header-logo">
                    <a class="" href="/">
                        <img height="80" src="/images-static/terrawhisper-logo.jpg" alt="logo of terrawhisper">
                    </a>
                </div>
                <nav class="navigation">
                    <input type="checkbox" class="toggle-menu">
                    <div class="hamburger"></div>
                    <ul class="menu">
                        <li><a href="/herbs.html">Herbs</a></li>
                        <li><a href="/remedies.html">Remedies</a></li>
                    </ul>
                </nav>
            </div>
        </header>
    '''
    return html

def html_footer():
    html = f'''
        <footer class="container-xl flex justify-between">
            <span>terrawhisper.com | all rights reserved</span>
            <nav class="flex gap-16">
                <a class="no-underline" href="/">About</a>
                <a class="no-underline" href="/">Contact</a>
            </nav>
        </footer>
    '''
    return html

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
    html_lst = ''
    html_lst += '<ul style="list-style: none;">'
    for item_toc in json_toc:
        index = item_toc['index']
        headline = item_toc['headline']
        html_lst += f'<li><a href="#{index}">{headline}</a></li>'
    html_lst += '</ul>'
    html_toc = ''
    html_toc += f'''
    <div class="toc">
        <div class="toc-header">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
            </svg>
            <p style="margin-bottom: 0;">Table of Contents</p>
        </div>
        {html_lst}
    </div>
    '''
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

# TODO: fix bad recommendations
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
        product_data = json_read(product_json_filepath)
        if 'reviews_score_total' in product_data:
            product_asin = product_json_filepath.split('/')[-1].replace('.json', '')
            reviews_score_total = float(product_data['reviews_score_total'])
            products_jsons.append({'product_asin': product_asin, 'reviews_score_total': reviews_score_total})
    products_jsons_ordered = sorted(products_jsons, key=lambda x: x['reviews_score_total'], reverse=True)
    products_jsons_filepaths_ordered = []
    for product_json in products_jsons_ordered:
        product_asin = product_json['product_asin']
        product_filepath = f'{products_jsons_folderpath}/{product_asin}.json'
        products_jsons_filepaths_ordered.append(product_filepath)
    products_jsons_filepaths_ordered = products_jsons_filepaths_ordered
    product_json_filepath = products_jsons_filepaths_ordered[0]
    json_product = json_read(product_json_filepath)
    affiliate_product = {
        'url': json_product['url'],
        'affiliate_link': json_product['affiliate_link'],
        'title': json_product['title'],
    }
    return affiliate_product

def checklist_html():
    with open('assets/newsletter/sign-in-form.txt') as f: sign_in_form_html = f.read()
    html = f'''
        <div class="bg-lightgray">
            <div class="container-sm pt-16 px-24">
                <p class="text-center mb-8">Also, you may be interested in...</p>
                <p class="text-48 helvetica-bold text-black text-center mb-8">Today Free Bonus!</p>
                <p class="text-24 helvetica-bold text-orange text-center mb-8"> The Ultimate Herb Drying Checklist<br>(For Long-Lasting Powerful Medicinal Effect)</p>
                <p class="text-center mb-0">How to easily dry herbs that don't mold and that keep their strong medicinal power for more than 1 year.</p>
                {sign_in_form_html}
            </div>
        </div>
    '''
    return html

def social_html():
    html = f'''
        <div class="border-0 border-b-4 border-solid border-black mb-24">
            <h2 class="h2-plain text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Stay Connected</h2>
        </div>
        <div class="flex flex-col">
            <div class="flex flex-col gap-16">
                <p class="">Follow Terrawhisper on the social medias below to get daily tips on how to use herbal remedies to improve your health.</p>
                <a href="https://www.pinterest.com/terrawhisper" target="_blank" class="inline-block flex items-center justify-between gap-16 no-underline">
                    <div class="flex items-center gap-8">
                        <img class="social-icon" src="/images-static/pinterest.png">
                        <p class="mb-0">@terrawhisper</p>
                    </div>
                    <p class="mb-0 hover-orange helvetica-bold">Follow</p>
                </a>
                <a href="https://www.x.com/terrawhisperx" target="_blank" class="inline-block flex items-center gap-16 justify-between no-underline">
                    <div class="flex items-center gap-8">
                        <img class="social-icon" src="/images-static/twitter.png">
                        <p class="mb-0">@terrawhisperx</p>
                    </div>
                    <p class="mb-0 hover-orange helvetica-bold">Follow</p>
                </a>
            </div>
        </div>
    '''
    return html

