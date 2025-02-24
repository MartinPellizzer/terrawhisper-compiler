import os
import json
import random
import shutil
import datetime

import torch
from diffusers import DiffusionPipeline
from diffusers import StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image, ImageFont, ImageDraw

import util

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read
from oliark_llm import llm_reply
from oliark import img_resize

from lib import components
from lib import templates

import g

##########################################################################
# FLAGS
##########################################################################

ads_manual = False
HERBS_TO_GEN_NUM = 1000000

vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'
website_folderpath = f'{vault}/terrawhisper/website/terrawhisper'
website_folderpath = f'website-2'

model_8b = f'/home/ubuntu/vault-tmp/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
model_validator_filepath = f'llms/Llama-3-Partonus-Lynx-8B-Instruct-Q4_K_M.gguf'
model = model_8b

AUTHOR_NAME = 'Leen Randell'
# AUTHOR_NAME = 'Martin Pellizzer'
AUTHOR_SLUG = AUTHOR_NAME.strip().lower().replace(' ', '-')

plants_wcvp = []
if plants_wcvp == []:
    plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    plants_wcvp = [plant for plant in plants_wcvp if ('var.' not in plant['scientfiicname'] and 'f.' not in plant['scientfiicname'] and 'subsp.' not in plant['scientfiicname'] and 'proles' not in plant['scientfiicname']  and 'stirps' not in plant['scientfiicname'] and 'monstr.' not in plant['scientfiicname'])]
# for plant in plants_wcvp[:100]:
    # print(plant['scientfiicname'])
# quit()

vertices_plants = json_read(f'{vault}/herbalism/vertices-plants.json')
vertices_divisions = json_read(f'{vault}/herbalism/vertices-divisions.json')
vertices_classes = json_read(f'{vault}/herbalism/vertices-classes.json')
vertices_subclasses = json_read(f'{vault}/herbalism/vertices-subclasses.json')
vertices_orders = json_read(f'{vault}/herbalism/vertices-orders.json')
vertices_families = json_read(f'{vault}/herbalism/vertices-families.json')
    
edges_classes_divisions = json_read(f'{vault}/herbalism/edges-classes-divisions.json')
edges_subclasses_classes = json_read(f'{vault}/herbalism/edges-subclasses-classes.json')
edges_orders_subclasses = json_read(f'{vault}/herbalism/edges-orders-subclasses.json')
edges_families_orders = json_read(f'{vault}/herbalism/edges-families-orders.json')

def json_write(filepath, dictionary):
    j = json.dumps(dictionary, indent=4)
    with open(filepath, 'w') as f:
        print(j, file=f)

with open(f'assets/affiliates/amazon/link-by-keyword.txt') as f: 
    aff_links_rows = [row.strip() for row in f.read().strip().split('\n') if row.strip() != '']

def affiliate_disclaimer_gen():
    html = ''
    html += f'''
        <p class="text-14 mb-0"><i>Disclaimer: We earn a commission if you click this link and make a purchase at no additional cost to you.</i></p>
    '''
    return html

def ai_paragraph_gen(filepath, data, obj, key, prompt, regen=False, print_prompt=False):
    if key not in obj: obj[key] = ''
    if regen: obj[key] = ''
    if obj[key] == '':
        if print_prompt: print(prompt)
        reply = llm_reply(prompt)
        if reply.strip() != '':
            if 'can\'t' in reply: reply = 'Info not available yet.'
            if 'couldn\'t' in reply: 'Info not available yet.'
            if 'cannot' in reply: 'Info not available yet.'
            obj[key] = reply
            json_write(filepath, data)

def get_popular_herbs_from_teas_articles():
    output = []
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}/teas'
        json_filepath = f'database/json/{url}.json'
        if os.path.exists(json_filepath):
            data = json_read(json_filepath, create=True)
            for obj in data['remedies']:
                found = False
                for item in output:
                    if obj['herb_name_scientific'] == item['herb_name_scientific']:
                        item['herb_total_score'] += obj['herb_total_score']
                        found = True
                        break
                if not found:
                    output.append({
                        'herb_name_scientific': obj['herb_name_scientific'],
                        'herb_total_score': obj['herb_total_score'],
                    })
    output = sorted(output, key=lambda x: x['herb_total_score'], reverse=True)
    return output

def get_popular_teas():
    output = []
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}/teas'
        json_filepath = f'database/json/{url}.json'
        if os.path.exists(json_filepath):
            data = json_read(json_filepath, create=True)
            for obj in data['remedies']:
                found = False
                for item in output:
                    if obj['herb_name_scientific'] == item['herb_name_scientific']:
                        item['herb_total_score'] += obj['herb_total_score']
                        found = True
                        break
                if not found:
                    output.append({
                        'herb_name_scientific': obj['herb_name_scientific'],
                        'herb_total_score': obj['herb_total_score'],
                    })
    output = sorted(output, key=lambda x: x['herb_total_score'], reverse=True)
    return output

def checklist_gen(sign_in_form_html):
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

def amazon_buy_button(url, img_filepath=''):
    try:
        with open(img_filepath) as f: html_img = f.read()
    except: 
        html_img = ''
    affiliate_disclaimer_html = affiliate_disclaimer_gen()
    if html_img == '':
        html = f'''
            <div class="bg-lightgray px-24 py-32">
                <a class="button-amazon mb-16 mt-16" href="{url}" target="_blank">Buy On Amazon</a>
                {affiliate_disclaimer_html}
            </div>
        '''
    else:
        html = f'''
            <div class="bg-lightgray px-24 pb-48">
                <div class="mob-flex gap-48 items-center">
                    <div>
                        {html_img}
                    </div>
                    <div>
                        <a class="button-amazon mb-16" href="{url}" target="_blank">Buy On Amazon</a>
                        {affiliate_disclaimer_html}
                    </div>
                </div>
            </div>
        '''
    return html


def gen_aff_html(url, title, herb_name_common):
    html = ''
    html += f'<div class="bg-lightgray">\n'
    html += f'<div class="container-sm py-16 px-24">\n'
    html += f'<p class="text-32 text-black text-center mb-8">{herb_name_common.title()} Tea on Amazon</p>\n'
    html += f'<p class="text-16 text-black helvetica-bold text-center">{title}</p>\n'
    html += f'<div class="text-center">\n'
    html += f'<a class="button-amazon mb-16" href="{url}" target="_blank">Buy</a>\n'
    html += f'</div>\n'
    html += f'<p class="text-14 text-center mb-0"><i>Disclaimer: We earn a commission if you click this link and make a purchase at no additional cost to you.</i></p>\n'
    html += f'</div>\n'
    html += f'</div>\n'
    return html

def affiliate_gen(data):
    link = data[0]
    title = data[2]
    affiliate_link_html = ''
    affiliate_link_html += f'<div class="bg-lightgray">\n'
    affiliate_link_html += f'<div class="container-sm py-16 px-24">\n'
    affiliate_link_html += f'<p class="text-32 text-black text-center mb-0">Amazon Finds</p>\n'
    affiliate_link_html += f'<p class="text-center">(for the apothecary)</p>\n'
    affiliate_link_html += f'<p class="text-black helvetica-bold text-center">{title}</p>\n'
    affiliate_link_html += f'<div class="text-center">\n'
    affiliate_link_html += f'<a class="button-amazon mb-16" href="{link}">Buy</a>\n'
    affiliate_link_html += f'</div>\n'
    affiliate_link_html += f'<p class="text-14 text-center mb-0"><i>Disclaimer: We earn a commission if you click this link and make a purchase at no additional cost to you.</i></p>\n'
    affiliate_link_html += f'</div>\n'
    affiliate_link_html += f'</div>\n'
    return affiliate_link_html

def gen_meta(content, lastmod):
    year = lastmod.split('-')[0]
    month = lastmod.split('-')[1]
    if str(month) == '1': month = "Jan"
    if str(month) == '2': month = "Feb"
    if str(month) == '3': month = "Mar"
    if str(month) == '4': month = "Apr"
    if str(month) == '5': month = "May"
    if str(month) == '6': month = "Jun"
    if str(month) == '7': month = "Jul"
    if str(month) == '8': month = "Aug"
    if str(month) == '9': month = "Sep"
    if str(month) == '10': month = "Oct"
    if str(month) == '11': month = "Nov"
    if str(month) == '12': month = "Dec"
    day = lastmod.split('-')[2]
    reading_time = str(len(content.split(' ')) // 200) + ' minutes'
    html = f'''
        <div class="flex items-center justify-between mb-16">
            <div class="flex items-center gap-8">
                <p class="mb-0 text-14">By <a class="uppercase text-black no-underline font-bold" rel="author" href="">{AUTHOR_NAME}</a></p>
            </div>
            <p class="mb-0">Updated: {month} {day}, {year}</p>
        </div>
    '''
    return html

def breadcrumbs_gen(filepath):
    breadcrumbs = ['<a class="no-underline article-card text-black" href="/">Home</a>']
    breadcrumbs_path = filepath.replace('website/', '')
    chunks = breadcrumbs_path.split('/')
    filepath_curr = ''
    for chunk in chunks[:-1]:
        filepath_curr += f'/{chunk}'
        chunk = chunk.strip().replace('-', ' ').title()
        breadcrumbs.append(f'<a class="no-underline article-card text-black" href="{filepath_curr}.html">{chunk}</a>')
    breadcrumbs = ' | '.join(breadcrumbs)
    breadcrumbs += f' | {chunks[-1].strip().replace(".html", "").replace("-", " ").title()}'
    breadcrumbs_section = f'''
        <section class="container-xl">
            {breadcrumbs}
        </section>
    '''
    return breadcrumbs_section

if 0:
    if 0:
        prompt = f'''
            write an outline for an article with the following title:
            10 herbal teas for dry hair
        '''
        reply = llm_reply(prompt)
        quit()
    if 0:
        prompt = f'''
            heres the title of my article title: 10 herbal teas for dry hair
            this article has an intro paragraph and 10 sub sections, one for each of the 10 herbal tea.
            give me a list of other supplementary things i can write about at the bottom of the article that a target reader would be very intereste in.
            reply only with the supplementary content.
        '''
        reply = llm_reply(prompt)
        quit()
    quit()

checkpoint_filepath = f'{vault}/stable-diffusion/checkpoints/xl/juggernautXL_juggXIByRundiffusion.safetensors'
pipe = None
def pipe_init():
    global pipe
    if not pipe:
        pipe = StableDiffusionXLPipeline.from_single_file(
            checkpoint_filepath, 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

def today():
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    day = today.day
    today = f'{year}-{month}-{day}'
    print(today)
    return today

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
with open('assets/scripts/google-adsense.txt') as f: GOOGLE_ADSENSE_TAG = f.read()
with open('assets/scripts/google-adsense-ad-auto.txt') as f: GOOGLE_ADSENSE_AD_AUTO_TAG = f.read()
with open('assets/scripts/google-adsense-display-ad-square.txt') as f: GOOGLE_ADSENSE_DISPLAY_AD_SQUARE = f.read()

top_bar_html = f'''
    <section class="bg-black">
        <div class="container-xl">
            <div class="flex justify-between items-center top-bar">
                <span class="text-white text-14">Terrawhisper</span>
                <div class="flex gap-16">
                    <a href="https://www.pinterest.com/terrawhisper" target="_blank" class="inline-block">
                        <img class="social-icon-16" src="/images-static/pinterest-small-white.png">
                    </a>
                    <a href="https://www.x.com/terrawhisperx" target="_blank" class="inline-block">
                        <img class="social-icon-16" src="/images-static/twitter-small-white.png">
                    </a>
                </div>
            </div>
        </div>
    </section>
'''

header_html = ''
header_html += top_bar_html
if 1:
    header_html += f'''
        <header class="header">
            <a class="" href="/"><img height="64" src="/images-static/terrawhisper-logo.png" alt="logo of terrawhisper"></a>
            <nav class="header-nav">
                <a class="text-black no-underline text-16 menu-item" href="/herbs.html">HERBS</a>
                <a class="text-black no-underline text-16 menu-item" href="/remedies.html">REMEDIES</a>
                <a class="text-black no-underline text-16 menu-item" href="/equipments.html">EQUIPMENTS</a>
            </nav>
        </header>
    '''
            # <a class="button-green-fill" href="/herbs.html">View Herbs</a>
if 0:
    header_html += f'''
        <header style="border-bottom: 1px solid #d4d4d4;" class="header-2 container-xl">
            <div class="logo">
                <a class="" href="/">
                    <img height="64" src="/images-static/terrawhisper-logo.png" alt="logo of terrawhisper">
                </a>
            </div>
            <div class="navigation">
                <input type="checkbox" class="toggle-menu">
                <div class="hamburger"></div>
                <ul class="menu">
                    <li><a href="/herbs.html">HERBS</a></li>
                    <li><a href="/remedies.html">REMEDIES</a></li>
                    <li><a href="/equipments.html">EQUIPMENTS</a></li>
                </ul>
            </div>
        </header>
    '''

header_html_2 = f'''
    <header style="position: sticky; top: 0px;">
        <section style="background-color: #101010; padding: 8px 0;">
            <div class="container-xl">
                <div style="text-align: center;">
                    <span style="display: inline-block; color: #ffffff;">Free: How to dry herbs in 7 minutes or less</span>
                    <a style="display: inline-block; color: #101010; background-color: #ffffff; text-decoration: none; padding: 4px 16px; border-radius: 9999px; margin-left: 8px;">Download Cheatsheet</a>
                </div>
            </div>
        </section>
        <section>
            <div style="background-color: #ffffff;" class="header">
                <a class="text-black no-underline text-16 menu-item" href="/herbs.html">TERRAWHISPER</a>
                <nav class="header-nav">
                    <a class="text-black no-underline text-16 menu-item" href="/herbs.html">HERBS</a>
                    <a class="text-black no-underline text-16 menu-item" href="/remedies.html">REMEDIES</a>
                    <a class="text-black no-underline text-16 menu-item" href="/equipments.html">EQUIPMENTS</a>
                </nav>
            </div>
        </section>
    </header>
'''

sidebar_html_2 = f'''
    <section>
        <div style="position: sticky; top: 144px;">
            <h2>Table of Contents</h2>
        </div>
    </section>
'''

footer_html = f'''
    <footer class="footer">
        <span>© TerraWhisper.com 2024 | All Rights Reserved</span>
        <div class="flex gap-24">
            <a class="text-black no-underline text-16 menu-item" href="/about.html">About</a></li>
            <a class="text-black no-underline text-16 menu-item" href="/contacts.html">Contacts</a></li>
            <a class="text-black no-underline text-16 menu-item" href="/privacy-policy.html">Privacy Policy</a>
            <a class="text-black no-underline text-16 menu-item" href="/cookie-policy.html">Cookie Policy</a>
        </div>
    </footer>
'''

        # <img src="images-static/{AUTHOR_SLUG}.jpg" class="avatar">
author_block_html = f'''
    <div class="border-0 border-b-4 border-solid border-black mb-24">
        <h2 class="h2-plain text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Stay Connected</h2>
    </div>
    <div class="flex flex-col items-center">
        <p class="helvetica-bold">{AUTHOR_NAME}</p>
        <p class="">Herbalist and Botanist. Lover of medicinal plants and natural remedies. Healing herbs are your first line of defence against common ailments, use them wisely.</p>
        <p class="">Follow Terrawhisper on the social medias below to get daily tips on how to use herbal remedies to improve your health.</p>
        <div class="flex flex-col gap-16">
            <a href="https://www.pinterest.com/terrawhisper" target="_blank" class="inline-block flex items-center gap-16 no-underline">
                <img class="social-icon" src="images-static/pinterest.png">
            </a>
            <a href="https://www.x.com/terrawhisperx" target="_blank" class="inline-block flex items-center gap-16 no-underline">
                <img class="social-icon" src="images-static/twitter.png">
            </a>
        </div>
    </div>
'''

def head_html_generate(title, css_filepath):
    head_html = f'''
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="{css_filepath}">
            <title>{title}</title>
            {GOOGLE_TAG}
            {GOOGLE_ADSENSE_AD_AUTO_TAG}
        </head>
    '''
    return head_html

def html_article_layout(main_html, sidebar_html):
    layout_html = f'''
        <div class="container-xl mt-48 mob-flex gap-96">
            <div class="flex-2">
                {main_html}
            </div>
            <div class="flex-1">
                {sidebar_html}
            </div>
        </div>
    '''
    return layout_html

def html_article_main(meta_html, article_html, related_html, affiliate_disclaimer_html=''):
    main_html = f'''
        <main>
            {affiliate_disclaimer_html}
            {meta_html}
            {article_html}
            {related_html}
        </main>
    '''
    return main_html

def html_article_related(related_blocks_html):
    related_html = f'''
        <div class="border-0 border-b-4 border-solid border-black mb-24 mt-48">
            <h2 class="h2-plain text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Related Articles</h2>
        </div>
        <div class="grid grid-3 gap-16">
            {related_blocks_html}
        </div>
    '''
    return related_html

def html_article_popular_blocks(sidebar_populars):
    html = ''
    for popular in sidebar_populars:
        html += f'''
            <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{popular['href']}">
                <div class="">
                    <div class="relative mb-16">
                        <img class="object-cover" height="180" src="{popular['src']}">
                    </div>
                    <h3 class="h3-plain text-14 mb-8">
                        {popular['title']}
                    </h3>
                </div>
            </a>
        '''
    return html

def html_article_popular(category, sidebar_blocks_html):
    html = f'''
        <div>
            <div class="border-0 border-b-4 border-solid border-black mb-24">
                <h2 class="h2-plain text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">popular in {category}</h2>
            </div>
        </div>
        <div class="flex flex-col gap-24">
            <div class="flex flex-col gap-24">
                {sidebar_blocks_html}
            </div>
        </div>
    '''
    return html
        
def html_article_social():
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

def html_article_sidebar(popular_html, social_html):
    if ads_manual:
        ad_html = f'''
            <div class="mb-48">
                {GOOGLE_ADSENSE_DISPLAY_AD_SQUARE}
            </div>
        '''
    else:
        ad_html = ''
    html = f'''
        <div class="sidebar">
            {ad_html}
            <div class="mb-48">
                {social_html}
            </div>
            {popular_html}
        </div>
    '''
    return html

def articles_ailments_2():
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    with open(f'keywords/herbal-tea-for.txt') as f: 
        keywords_teas = [x for x in f.read().strip().split('\n') if x != '']

    for ailment_i, ailment in enumerate(ailments):
        print(f'\n>> {ailment_i}/{len(ailments)}')
        print(f'    >> {ailment}')
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/remedies'): 
            os.mkdir(f'{website_folderpath}/remedies')
        if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system'): 
            os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system')

        # if os.path.exists(json_filepath): os.remove(json_filepath)
        # continue

        data = json_read(json_filepath, create=True)
        data['ailment_slug'] = ailment_slug
        data['ailment_name'] = ailment_name
        data['system_slug'] = system_slug
        data['organ_slug'] = organ_slug
        data['url'] = url
        if 'lastmod' not in data: data['lastmod'] = today()

        if 'title' not in data: data['title'] = ''
        # data['title'] = ''
        if data['title'] == '':
            prompt = f'''
                Rewrite the following title in 10 different ways: {ailment_name}: Causes, Medicinal Herbs And Herbal Preparations.
                Write only the titles.
                Include the following words in each title: {ailment_name}.
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '. ' not in line: continue
                line = '. '.join(line.split('. ')[1:])
                line = line.replace('*', '')
                if line.endswith('.'): line = line[:-1]
                line = line.strip()
                if line == '': continue
                lines.append(line)
            line = random.choice(lines)
            data['title'] = line
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;intro
        ## ------------------------------------
        if 0:
            key = 'intro_desc'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write a short paragraph about herbal remedies for {ailment_name}.
                Include the following:
                - what is {ailment_name} and how it effects your life.
                - the causes of {ailment_name}.
                - the healing herbs for {ailment_name}.
                - the herbal preparations for {ailment_name} (ex. teas).
                Use simple and short words, and a simple writing style.
                Don't write lists.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;causes
        ## ------------------------------------
        if 0:
            key = 'causes'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'causes'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            prompt = f'''
                List the names of the 20 most common causes of {ailment_name}.
                Also, for each cause name give a confidence score from 1 to 10, indicating how sure you are that is a cause of {ailment_name}.
                Write only the names of the causes, don't add descriptions.
                Write the names of the causes using as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"cause_name": "name of cause 1", "confidence_score": 10}}, 
                    {{"cause_name": "name of cause 2", "confidence_score": 5}}, 
                    {{"cause_name": "name of cause 3", "confidence_score": 7}} 
                ]
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                outputs = []
                for item in json_data:
                    try: item['cause_name']
                    except: continue
                    try: item['confidence_score']
                    except: continue
                    outputs.append({
                        'cause_name': item['cause_name'], 
                        'cause_confidence_score': int(item['confidence_score']),
                    })
            outputs = sorted(outputs, key=lambda x: x['cause_confidence_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output in outputs:
                print(output)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = outputs[:10]
            json_write(json_filepath, data)

        question = f'What are the causes of {ailment_name}?'
        key = 'causes_header'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Rewrite in 10 different ways the following question: {question}
                Write only the questions.
                Don't change the meaning of the original question in your rewrites.
                Make sure you never change the following word: {ailment_name}.
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '. ' not in line: continue
                line = '. '.join(line.split('. ')[1:])
                line = line.replace('*', '')
                if line.endswith('.'): line = line[:-1]
                line = line.strip()
                if line == '': continue
                # if ailment_name.lower() not in line.lower(): continue
                lines.append(line)
            if len(lines) != 0:
                line = random.choice(lines)
                data[key] = line
                json_write(json_filepath, data)

        random_causes_num = random.randint(4, 6)
        key = 'causes_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            causes_names = [x['cause_name'] for x in data['causes'][:random_causes_num]]
            causes_names = ', '.join(causes_names)
            prompt = f'''
                Write a detailed paragraph explaining what are the main causes of {ailment_name}.
                Include the following causes and explain why: {causes_names}.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                Start with the following words: The main causes of {ailment_name} are .
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        key = 'causes_list'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            causes_names = [x['cause_name'] for x in data['causes'][:random_causes_num]]
            causes_names = ', '.join(causes_names)
            prompt = f'''
                Write a short sentence for each of the following causes of {ailment_name}, explaining why it causes this ailment.
                Include the following causes and explain why: {causes_names}.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"cause_name": "name of cause 1", "cause_description": "explain why this is a cause"}}, 
                    {{"cause_name": "name of cause 2", "cause_description": "explain why this is a cause"}}, 
                    {{"cause_name": "name of cause 3", "cause_description": "explain why this is a cause"}} 
                ]
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                outputs = []
                for item in json_data:
                    try: item['cause_name']
                    except: continue
                    try: item['cause_description']
                    except: continue
                    outputs.append({
                        'cause_name': item['cause_name'], 
                        'cause_description': item['cause_description'],
                    })
            data[key] = outputs[:10]
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;benefits
        ## ------------------------------------
        question = f'What are the benefits of using herbs for {ailment_name}?'
        key = 'benefits_header'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Rewrite in 10 different ways the following question: {question}
                Write only the questions.
                Don't change the meaning of the original question in your rewrites.
                Make sure you never change the following word: {ailment_name}.
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '. ' not in line: continue
                line = '. '.join(line.split('. ')[1:])
                line = line.replace('*', '')
                if line.endswith('.'): line = line[:-1]
                line = line.strip()
                if line == '': continue
                # if ailment_name.lower() not in line.lower(): continue
                lines.append(line)
            if len(lines) != 0:
                line = random.choice(lines)
                data[key] = line
                json_write(json_filepath, data)

        key = 'benefits_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write a detailed paragraph explaining what are the main benefits of using herbs for {ailment_name}.
                Don't write the names of the herbs.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;herbs
        ## ------------------------------------
        if 0:
            key = 'herbs'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'herbs'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            items_num = 20
            output_plants = []
            for i in range(5):
                print(f'{ailment_i}/{len(ailments)} - {i}/20: {ailment}')
                prompt = f'''
                    List the best herbs to relieve {ailment_name}.
                    Also, for each herb name give a confidence score from 1 to 10, indicating how sure you are that herb is effective to relieve {ailment_name}.
                    Write only the scientific names (botanical names) of the herbs, don't add descriptions or common names.
                    Write the names of the herbs using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"herb_name_scientific": "scientific name of herb 1 used for preparation", "confidence_score": "10"}}, 
                        {{"herb_name_scientific": "scientific name of herb 2 used for preparation", "confidence_score": "5"}}, 
                        {{"herb_name_scientific": "scientific name of herb 3 used for preparation", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names_scientific = []
                    for item in json_data:
                        try: line = item['herb_name_scientific']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        print(line)
                        for plant in plants_wcvp:
                            name_scientific = plant['scientfiicname']
                            if name_scientific.lower().strip() in line.lower().strip():
                                if len(name_scientific.split(' ')) > 1:
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    print(name_scientific)
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    names_scientific.append({
                                        "name": name_scientific, 
                                        "score": score,
                                    })
                                    break
                        ## exceptions
                        if line.lower().strip() == 'mentha piperita':
                                names_scientific.append({"name": 'Mentha x piperita', "score": score})
                    for obj in names_scientific:
                        name = obj['name']
                        score = obj['score']
                        found = False
                        for output_plant in output_plants:
                            print(output_plant)
                            print(name, '->', output_plant['herb_name_scientific'])
                            if name in output_plant['herb_name_scientific']: 
                                output_plant['herb_mentions'] += 1
                                output_plant['herb_confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            output_plants.append({
                                'herb_name_scientific': name, 
                                'herb_mentions': 1, 
                                'herb_confidence_score': int(score), 
                            })
            output_plants_final = []
            for output_plant in output_plants:
                output_plants_final.append({
                    'herb_name_scientific': output_plant['herb_name_scientific'],
                    'herb_mentions': int(output_plant['herb_mentions']),
                    'herb_confidence_score': int(output_plant['herb_confidence_score']),
                    'herb_total_score': int(output_plant['herb_mentions']) * int(output_plant['herb_confidence_score']),
                })
            output_plants_final = sorted(output_plants_final, key=lambda x: x['herb_total_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output_plant in output_plants_final:
                print(output_plant)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = output_plants_final[:10]
            json_write(json_filepath, data)

        question = f'What are the main medicial herbs for {ailment_name}?'
        key = 'herbs_header'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Rewrite in 10 different ways the following question: {question}
                Write only the questions.
                Don't change the meaning of the original question in your rewrites.
                Make sure you never change the following word: {ailment_name}.
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '. ' not in line: continue
                line = '. '.join(line.split('. ')[1:])
                line = line.replace('*', '')
                if line.endswith('.'): line = line[:-1]
                line = line.strip()
                if line == '': continue
                # if ailment_name.lower() not in line.lower(): continue
                lines.append(line)
            if len(lines) != 0:
                line = random.choice(lines)
                data[key] = line
                json_write(json_filepath, data)

        # herbs img
        for herb_i, herb in enumerate(data['herbs']):
            herb_name_scientific = herb['herb_name_scientific']
            herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
            output_filepath = f'{website_folderpath}/images/ailments/herbs/{herb_slug}.jpg'
            src = f'/images/ailments/herbs/{herb_slug}.jpg'
            alt = f'{herb_name_scientific} for {ailment_name}'
            if not os.path.exists(output_filepath):
                prompt = f'''
                    dry {herb_name_scientific} herb on a wooden table,
                    indoor, 
                    natural window light,
                    earth tones,
                    neutral colors,
                    soft focus,
                    warm tones,
                    vintage,
                    high resolution,
                    cinematic
                '''
                negative_prompt = f'''
                    text, watermark 
                '''
                print(prompt)
                pipe_init()
                image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                image = img_resize(image, w=768, h=768)
                image.save(output_filepath)
            if herb_i == 0:
                herb['image_src'] = src
                herb['image_alt'] = alt
                json_write(json_filepath, data)

        key = 'herbs_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['herbs'][:5]]
            herbs_names = ', '.join(herbs_names)
            prompt = f'''
                Write a detailed paragraph explaining why herbs are good for {ailment_name}.
                Include the following herbs and expalin why they are good: {herbs_names}.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;preparations
        ## ------------------------------------
        if 0:
            key = 'preparations'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'preparations'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            items_num = 20
            data_output = []
            for i in range(5):
                print(f'{ailment_i}/{len(ailments)}: {ailment}')
                prompt = f'''
                    Write a numbered list of the 10 most common herbal preparation used for {ailment_name}.
                    Also, give a confidence score in number format from 1 to 10 for each preparation representing how much you believe that herbal preparation is effective for the ailment.
                    For reference, examples of types of herbal preparations are: tea, decoction, tincture, creams, capsules, etc. 
                    Don't include herbs names in the praparations, just write the type of the preparation.
                    Write the names of the preparations using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"preparation_name": "name of preparation 1", "confidence_score": "10"}}, {{"preparation_name": "name of preparation 2", "confidence_score": "5"}}, 
                        {{"preparation_name": "name of preparation 3", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    preparations = []
                    for item in json_data:
                        try: name = item['preparation_name']
                        except: continue
                        try: 
                            score = item['confidence_score']
                            int(score)
                        except: continue
                        preparations.append({"name": name, "score": score})
                    for obj in preparations:
                        name = obj['name']
                        score = obj['score']
                        found = False
                        for obj in data_output:
                            if name in obj['name']: 
                                obj['mentions'] += 1
                                obj['score'] += int(score)
                                found = True
                                break
                        if not found:
                            data_output.append({
                                'name': name, 
                                'mentions': 1, 
                                'score': int(score), 
                            })
            data_output_final = []
            for obj in data_output:
                data_output_final.append({
                    'preparation_name': obj['name'],
                    'preparation_mentions': int(obj['mentions']),
                    'preparation_confidence_score': int(obj['score']),
                    'preparation_total_score': int(obj['mentions']) * int(obj['score']),
                })
            data_output_final = sorted(data_output_final, key=lambda x: x['preparation_total_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for obj in data_output_final:
                print(obj)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = data_output_final[:10]
            json_write(json_filepath, data)

        question = f'What are the most used herbal preparations for {ailment_name}?'
        key = 'preparations_header'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Rewrite in 10 different ways the following question: {question}
                Write only the questions.
                Don't change the meaning of the original question in your rewrites.
                Make sure you never change the following word: {ailment_name}.
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '. ' not in line: continue
                line = '. '.join(line.split('. ')[1:])
                line = line.replace('*', '')
                if line.endswith('.'): line = line[:-1]
                line = line.strip()
                if line == '': continue
                # if ailment_name.lower() not in line.lower(): continue
                lines.append(line)
            if len(lines) != 0:
                line = random.choice(lines)
                data[key] = line
                json_write(json_filepath, data)

        key = 'preparations_img'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            images_filepaths = []
            for preparation in data['preparations'][:5]:
                preparation_name = preparation['preparation_name']
                preparation_check = ''
                if 'tea' in preparation_name.lower(): preparation_check = 'teas'
                if 'tincture' in preparation_name.lower(): preparation_check = 'tinctures'
                if 'cream' in preparation_name.lower(): preparation_check = 'creams'
                if 'essential' in preparation_name.lower(): preparation_check = 'essential-oils'
                if preparation_name[-1] != 's': preparation_name += 's'
                preparation_link_out = f'{website_folderpath}/{url}/{preparation_check}.html'
                found = False
                if preparation_check != '':
                    if os.path.exists(preparation_link_out): 
                        found = True
                if found:
                    _json_filepath = f'database/json/{url}/{preparation_check}.json'
                    _data = json_read(_json_filepath)
                    images_filepaths.append(f'{website_folderpath}' + _data['intro_image_src'])
            pin_w = 768
            pin_h = 768
            img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
            gap = 8
            if len(images_filepaths) >= 4:
                img_0000 = Image.open(images_filepaths[0])
                img_0001 = Image.open(images_filepaths[1])
                img_0002 = Image.open(images_filepaths[2])
                img_0003 = Image.open(images_filepaths[3])
                img_0000 = util.img_resize(img_0000, int(pin_w*0.50), int(pin_h*0.5))
                img_0001 = util.img_resize(img_0001, int(pin_w*0.50), int(pin_h*0.5))
                img_0002 = util.img_resize(img_0002, int(pin_w*0.50), int(pin_h*0.5))
                img_0003 = util.img_resize(img_0003, int(pin_w*0.50), int(pin_h*0.5))
                img.paste(img_0000, (0, 0))
                img.paste(img_0001, (int(pin_w*0.50) + gap, 0))
                img.paste(img_0002, (0, int(pin_h*0.5) + gap))
                img.paste(img_0003, (int(pin_w*0.50) + gap, int(pin_h*0.5) + gap))
            elif len(images_filepaths) >= 3:
                img_0000 = Image.open(images_filepaths[0])
                img_0001 = Image.open(images_filepaths[1])
                img_0002 = Image.open(images_filepaths[2])
                img_0000 = util.img_resize(img_0000, int(pin_w*0.50), int(pin_h*0.5))
                img_0001 = util.img_resize(img_0001, int(pin_w*0.50), int(pin_h*0.5))
                img_0002 = util.img_resize(img_0002, int(pin_w*1.00), int(pin_h*0.5))
                img.paste(img_0000, (0, 0))
                img.paste(img_0001, (int(pin_w*0.50) + gap, 0))
                img.paste(img_0002, (0, int(pin_h*0.5) + gap))
            elif len(images_filepaths) >= 2:
                img_0000 = Image.open(images_filepaths[0])
                img_0001 = Image.open(images_filepaths[1])
                img_0000 = util.img_resize(img_0000, int(pin_w*0.50), int(pin_h*1.0))
                img_0001 = util.img_resize(img_0001, int(pin_w*0.50), int(pin_h*1.0))
                img.paste(img_0000, (0, 0))
                img.paste(img_0001, (int(pin_w*0.50) + gap, 0))
            elif len(images_filepaths) >= 1:
                img_0000 = Image.open(images_filepaths[0])
                img_0000 = util.img_resize(img_0000, int(pin_w*1.0), int(pin_h*1.0))
                img.paste(img_0000, (0, 0))
            if len(images_filepaths) >= 1:
                image_out_filepath = f'{website_folderpath}/images/ailments/{ailment_slug}-herbal-preparations.jpg'
                image_src_filepath = f'/images/ailments/{ailment_slug}-herbal-preparations.jpg'
                img.save(
                    image_out_filepath,
                    format='JPEG',
                    subsampling=0,
                    quality=70,
                )
            data[key] = image_src_filepath
            json_write(json_filepath, data)

        key = 'preparations_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            preparations_names = [x['preparation_name'] for x in data['preparations'][:5]]
            prompt = f'''
                Write a detailed paragraph explaining why herbal preparations are good for {ailment_name}.
                Include the following preparations and explain why they are good: {preparations_names}.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;herbs_avoid
        ## ------------------------------------
        if 0:
            key = 'herbs_avoid'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'herbs_avoid'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            items_num = 20
            output_plants = []
            herbs_names = [x['herb_name_scientific'] for x in data['herbs'][:5]]
            for i in range(5):
                print(f'{ailment_i}/{len(ailments)} - {i}: {ailment}')
                prompt = f'''
                    List the best herbs to avoid if you have {ailment_name}.
                    Don't include the following herbs: {herbs_names}.
                    Also, for each herb name give a confidence score from 1 to 10, indicating how sure you are that herb must be avoide if you have {ailment_name}.
                    Write only the scientific names (botanical names) of the herbs, don't add descriptions or common names.
                    Write the names of the herbs using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"herb_name_scientific": "scientific name of herb 1", "confidence_score": "10"}}, 
                        {{"herb_name_scientific": "scientific name of herb 2", "confidence_score": "5"}}, 
                        {{"herb_name_scientific": "scientific name of herb 3", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names_scientific = []
                    for item in json_data:
                        try: line = item['herb_name_scientific']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        if line.lower().strip() in [x.lower().strip() for x in herbs_names]: continue
                        print(line)
                        for plant in plants_wcvp:
                            name_scientific = plant['scientfiicname']
                            if name_scientific.lower().strip() in line.lower().strip():
                                if len(name_scientific.split(' ')) > 1:
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    print(name_scientific)
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    names_scientific.append({
                                        "name": name_scientific, 
                                        "score": score,
                                    })
                                    break
                        ## exceptions
                        if line.lower().strip() == 'mentha piperita':
                                names_scientific.append({"name": 'Mentha x piperita', "score": score})
                    for obj in names_scientific:
                        name = obj['name']
                        score = obj['score']
                        found = False
                        for output_plant in output_plants:
                            print(output_plant)
                            print(name, '->', output_plant['herb_name_scientific'])
                            if name in output_plant['herb_name_scientific']: 
                                output_plant['herb_mentions'] += 1
                                output_plant['herb_confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            output_plants.append({
                                'herb_name_scientific': name, 
                                'herb_mentions': 1, 
                                'herb_confidence_score': int(score), 
                            })
            output_plants_final = []
            for output_plant in output_plants:
                output_plants_final.append({
                    'herb_name_scientific': output_plant['herb_name_scientific'],
                    'herb_mentions': int(output_plant['herb_mentions']),
                    'herb_confidence_score': int(output_plant['herb_confidence_score']),
                    'herb_total_score': int(output_plant['herb_mentions']) * int(output_plant['herb_confidence_score']),
                })
            output_plants_final = sorted(output_plants_final, key=lambda x: x['herb_total_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output_plant in output_plants_final:
                print(output_plant)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = output_plants_final[:10]
            json_write(json_filepath, data)

        question = f'What herbs should you avoid if you have {ailment_name}?'
        key = 'herbs_avoid_header'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Rewrite in 10 different ways the following question: {question}
                Write only the questions.
                Don't change the meaning of the original question in your rewrites.
                Make sure you never change the following word: {ailment_name}.
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '. ' not in line: continue
                line = '. '.join(line.split('. ')[1:])
                line = line.replace('*', '')
                if line.endswith('.'): line = line[:-1]
                line = line.strip()
                if line == '': continue
                # if ailment_name.lower() not in line.lower(): continue
                lines.append(line)
            if len(lines) != 0:
                line = random.choice(lines)
                data[key] = line
                json_write(json_filepath, data)


        key = 'herbs_avoid_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['herbs_avoid'][:5]]
            herbs_names = ', '.join(herbs_names)
            prompt = f'''
                Write a detailed paragraph explaining why your should avoid the following herbs if you have {ailment_name}: {herbs_names}.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write lists.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;faq
        ## ------------------------------------
        faqs = [
            {'key': 'faq_prevent', 'question': f'Are there any specific herbs that can prevent {ailment_name}?',},
            {'key': 'faq_pregnant', 'question': f'Is it safe to use herbal remedies for {ailment_name} during pregnancy?',},
            {'key': 'faq_frequency', 'question': f'Are there any herbs that can reduce the frequency of {ailment_name}?',},
            {'key': 'faq_combination', 'question': f'Can I combine different herbal remedies for {ailment_name}?',},
            {'key': 'faq_children', 'question': f'What herbal remedies are safe for children with {ailment_name}?',},
            {'key': 'faq_side_effects', 'question': f'Are there any side effects associated with herbal {ailment_name} remedies?',},
            {'key': 'faq_how_long', 'question': f'How long does it take for herbal remedies to relieve {ailment_name}?',},
        ]
        for faq in faqs:
            key = faq['key']
            question = faq['question']
            if key not in data: data[key] = ''
            # data[key] = ''
            if data[key] == '':
                prompt = f'''
                    Write a short paragraph in less than 60 words that answer the following question: {question}
                    Use simple and short words, and a simple writing style.
                    Use a conversational and fluid writing style.
                    Don't write lists.
                    Don't write fluff.
                    Don't allucinate.
                    Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                    Don't mention consulting a doctor, healthcare professional or similar.
                '''
                reply = llm_reply(prompt).strip()
                reply = [line.strip() for line in reply.split('\n')]
                reply = ' '.join(reply)
                data[key] = reply
                json_write(json_filepath, data)


        #######################################################
        # ;image
        #######################################################
        if 1:
            herbs_names = [x['herb_name_scientific'] for x in data['herbs'][:5]]
            herb = random.choice(herbs_names)
            _herb_slug = herb.lower().strip().replace(' ', '-')
            output_filepath = f'{website_folderpath}/images/ailments/herbs/{_herb_slug}.jpg'
            src = f'/images/ailments/herbs/{herb_slug}.jpg'
            alt = f'herbal remedies for {ailment_name}'
            if not os.path.exists(output_filepath):
            # if system_slug == 'cardiovascular':
            # if True:
                prompt = f'''
                    dry {herb} herb on a wooden table,
                    indoor, 
                    natural window light,
                    earth tones,
                    neutral colors,
                    soft focus,
                    warm tones,
                    vintage,
                    high resolution,
                    cinematic
                '''
                negative_prompt = f'''
                    text, watermark 
                '''
                print(prompt)
                pipe_init()
                image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                image = img_resize(image, w=768, h=768)
                image.save(output_filepath)
            data['intro_image_src'] = src
            data['intro_image_alt'] = alt
            json_write(json_filepath, data)

        #######################################################
        # ;html
        #######################################################
        article_html = ''
        article_html += f'<h1 class="">{data["title"]}</h1>\n'
        src = data['intro_image_src']
        alt = data['intro_image_alt']
        article_html += f'<img class="article-img" src="{src}" alt="{alt}">\n'
        article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'

        article_html += f'<h2>{data["causes_header"]}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["causes_desc"])}\n'
        '''
        article_html += f'<p>The following list summarizes the main causes of {ailment_name}.</p>\n'
        article_html += f'<ul>\n'
        for item in data['causes_list']:
            cause_name = item['cause_name'] 
            cause_description = item['cause_description'] 
            article_html += f'<li><strong>{cause_name}</strong>: {cause_description}</li>\n'
        article_html += f'</ul>\n'
        '''

        article_html += f'<h2>{data["benefits_header"]}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["benefits_desc"])}\n'

        article_html += f'<h2>{data["herbs_header"]}</h2>\n'
        herb = data['herbs'][0]
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
        output_filepath = f'{website_folderpath}/images/ailments/herbs/{herb_slug}.jpg'
        src = f'/images/ailments/herbs/{herb_slug}.jpg'
        alt = f'{herb_name_scientific} for {ailment_name}'
        article_html += f'<img class="article-img" src="{src}" alt="{alt}">\n'
        _herbs_names = [x['herb_name_scientific'] for x in data['herbs']]
        _herbs_desc = data['herbs_desc']
        for _herb_name in _herbs_names:
            _herbs_desc = _herbs_desc.replace(_herb_name.strip(), f'<strong class="text-black">{_herb_name.strip()}</strong>', 1)
        article_html += f'{util.text_format_1N1_html(_herbs_desc)}\n'

        article_html += f'<h2>{data["preparations_header"]}</h2>\n'
        src = data['preparations_img']
        article_html += f'<img class="article-img" src="{src}" alt="{alt}">\n'
        _preparations_names = [x['preparation_name'] for x in data['preparations']]
        _preparations_desc = data['preparations_desc']
        '''
        for _preparation_name in _preparations_names:
            _preparations_desc = _preparations_desc.replace(_preparation_name.strip(), f'<strong class="text-black">{_preparation_name.strip()}</strong>', 1)
        '''
        article_html += f'{util.text_format_1N1_html(_preparations_desc)}\n'

        # preparations resources
        article_html += f'<p>Additional Resources:</p>\n'
        article_html += f'<ul>\n'

        # teas
        keyword_found = False
        for keyword in keywords_teas:
            if ailment_name.lower().strip() in keyword.lower().strip():
                keyword_found = True
                break
        if keyword_found:
            _json_filepath = f'database/json/{url}/teas.json'
            _data = json_read(_json_filepath)
            _title = _data['title']
            preparation_link_html = f'/{url}/teas.html'
            article_html += f'<li><a href="{preparation_link_html}">{_title.capitalize()}</a></li>\n'

        for preparation in data['preparations'][:5]:
            preparation_name = preparation['preparation_name']
            preparation_check = ''
            if not keyword_found:
                if 'tea' in preparation_name.lower(): preparation_check = 'teas'
            if 'tincture' in preparation_name.lower(): preparation_check = 'tinctures'
            if 'cream' in preparation_name.lower(): preparation_check = 'creams'
            if 'essential' in preparation_name.lower(): preparation_check = 'essential-oils'
            if preparation_name[-1] != 's': preparation_name += 's'
            preparation_link_out = f'{website_folderpath}/{url}/{preparation_check}.html'
            found = False
            if preparation_check != '':
                if os.path.exists(preparation_link_out): 
                    found = True
            if found:
                _json_filepath = f'database/json/{url}/{preparation_check}.json'
                _data = json_read(_json_filepath)
                _title = _data['title']
                preparation_link_html = f'/{url}/{preparation_check}.html'
                article_html += f'<li><a href="{preparation_link_html}">{_title.capitalize()}</a></li>\n'
        article_html += f'</ul>\n'

        # avoid
        article_html += f'<h2>{data["herbs_avoid_header"]}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["herbs_avoid_desc"])}\n'

        article_html += f'<h2>FAQ</h2>\n'
        faqs = faqs[:random.randint(3, 4)]
        for faq in faqs:
            key = faq['key']
            question = faq['question']
            article_html += f'<h3>{question.capitalize()}</h3>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
        ailments_slugs = []
        for ailment in ailments:
            _system_slug = ailment['system_slug']
            _ailment_slug = ailment['ailment_slug']
            if _system_slug == system_slug:
                ailments_slugs.append(_ailment_slug)
        random.shuffle(ailments_slugs)

        sidebar_populars = []
        for _ailment_slug in ailments_slugs[6:9]:
            _url = f'remedies/{system_slug}-system/{_ailment_slug}'
            _json_filepath = f'database/json/{_url}.json'
            _html_filepath = f'{website_folderpath}/{_url}.html'
            _data = json_read(_json_filepath)
            _ailment_name = _data['ailment_name']
            _title = _data['title']
            _src = f'/images/ailments/{_ailment_slug}-herbal-remedies.jpg'
            _alt = f'herbal remedies for {_ailment_name}'
            sidebar_populars.append({
                'src': _src,
                'title': _title,
                'href': f'/{_url}.html',
            })

        related_blocks_html = ''
        for _ailment_slug in ailments_slugs[:6]:
            _url = f'remedies/{system_slug}-system/{_ailment_slug}'
            _json_filepath = f'database/json/{_url}.json'
            _html_filepath = f'{website_folderpath}/{_url}.html'
            _data = json_read(_json_filepath)
            _ailment_name = _data['ailment_name']
            _title = _data['title']
            _src = f'/images/ailments/{_ailment_slug}-herbal-remedies.jpg'
            _alt = f'herbal remedies for {_ailment_name}'
            _href = f'/{_url}.html'
            related_blocks_html += f'''
                <a class="no-underline text-black" href="{_href}">
                    <div>
                        <img src="{_src}" alt="{_alt}">
                        <h3 class="h3-plain hover-orange text-14 mt-16">{_title}<h3>
                    </div>
                </a>
            '''

        breadcrumbs_html_filepath = f'{url}.html'
        breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
        meta_html = gen_meta(article_html, data["lastmod"])
        article_html = components.table_of_contents(article_html)
        head_html = head_html_generate(data['title'], '/style.css')

        social_html = html_article_social()
        popular_blocks_html = html_article_popular_blocks(sidebar_populars)
        popular_html = html_article_popular(f'{system_slug} system', popular_blocks_html)
        sidebar_html = html_article_sidebar(popular_html, social_html)

        related_html = html_article_related(related_blocks_html)
        main_html = html_article_main(meta_html, article_html, related_html)
        layout_html = html_article_layout(main_html, sidebar_html)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                {breadcrumbs_html}
                {layout_html}
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)
        print(f'\n')
        print(html_filepath)
        # quit()

def articles_ailments():
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        print(f'\n>> {ailment_i}/{len(ailments)}')
        print(f'    >> {ailment}')
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/remedies'): 
            os.mkdir(f'{website_folderpath}/remedies')
        if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system'): 
            os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system')

        # if os.path.exists(json_filepath): os.remove(json_filepath)
        # continue

        data = json_read(json_filepath, create=True)
        data['ailment_slug'] = ailment_slug
        data['ailment_name'] = ailment_name
        data['system_slug'] = system_slug
        data['organ_slug'] = organ_slug
        data['url'] = url
        if 'lastmod' not in data: data['lastmod'] = today()

        if 'remedies_num' not in data: data['remedies_num'] = ''
        # data['remedies_num'] = ''
        if data['remedies_num'] == '': data['remedies_num'] = random.randint(7, 11)
        remedies_num = data['remedies_num']

        if 'preparations_num' not in data: data['preparations_num'] = ''
        # data['preparations_num'] = ''
        if data['preparations_num'] == '': data['preparations_num'] = random.randint(5, 9)
        preparations_num = data['preparations_num']

        if 'causes_num' not in data: data['causes_num'] = ''
        # data['causes_num'] = ''
        if data['causes_num'] == '': data['causes_num'] = random.randint(5, 7)
        causes_num = data['causes_num']

        if 'title' not in data: data['title'] = ''
        # data['title'] = ''
        if data['title'] == '':
            prompt = f'''
                Rewrite the following title in 10 different ways: {ailment_name}: Causes, Medicinal Herbs And Herbal Preparations.
                Write only the titles.
                Include the following words in each title: {ailment_name}.
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '. ' not in line: continue
                line = '. '.join(line.split('. ')[1:])
                line = line.replace('*', '')
                if line.endswith('.'): line = line[:-1]
                line = line.strip()
                if line == '': continue
                lines.append(line)
            line = random.choice(lines)
            data['title'] = line
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;causes
        ## ------------------------------------
        if 0:
            key = 'causes'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'causes'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            prompt = f'''
                List the names of the 20 most common causes of {ailment_name}.
                Also, for each cause name give a confidence score from 1 to 10, indicating how sure you are that is a cause of {ailment_name}.
                Write only the names of the causes, don't add descriptions.
                Write the names of the causes using as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"cause_name": "name of cause 1", "confidence_score": 10}}, 
                    {{"cause_name": "name of cause 2", "confidence_score": 5}}, 
                    {{"cause_name": "name of cause 3", "confidence_score": 7}} 
                ]
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                outputs = []
                for item in json_data:
                    try: item['cause_name']
                    except: continue
                    try: item['confidence_score']
                    except: continue
                    outputs.append({
                        'cause_name': item['cause_name'], 
                        'cause_confidence_score': int(item['confidence_score']),
                    })
            outputs = sorted(outputs, key=lambda x: x['cause_confidence_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output in outputs:
                print(output)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = outputs[:causes_num]
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;remedies
        ## ------------------------------------
        if 0:
            key = 'remedies'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'remedies'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            items_num = 20
            output_plants = []
            for i in range(20):
                print(f'{ailment_i}/{len(ailments)} - {i}/20: {ailment}')
                prompt = f'''
                    List the best herbs to relieve {ailment_name}.
                    Also, for each herb name give a confidence score from 1 to 10, indicating how sure you are that herb is effective to relieve {ailment_name}.
                    Write only the scientific names (botanical names) of the herbs, don't add descriptions or common names.
                    Write the names of the herbs using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"herb_name_scientific": "scientific name of herb 1 used for preparation", "confidence_score": "10"}}, 
                        {{"herb_name_scientific": "scientific name of herb 2 used for preparation", "confidence_score": "5"}}, 
                        {{"herb_name_scientific": "scientific name of herb 3 used for preparation", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names_scientific = []
                    for item in json_data:
                        try: line = item['herb_name_scientific']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        print(line)
                        for plant in plants_wcvp:
                            name_scientific = plant['scientfiicname']
                            if name_scientific.lower().strip() in line.lower().strip():
                                if len(name_scientific.split(' ')) > 1:
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    print(name_scientific)
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    names_scientific.append({
                                        "name": name_scientific, 
                                        "score": score,
                                    })
                                    break
                        ## exceptions
                        if line.lower().strip() == 'mentha piperita':
                                names_scientific.append({"name": 'Mentha x piperita', "score": score})
                    for obj in names_scientific:
                        name = obj['name']
                        score = obj['score']
                        found = False
                        for output_plant in output_plants:
                            print(output_plant)
                            print(name, '->', output_plant['herb_name_scientific'])
                            if name in output_plant['herb_name_scientific']: 
                                output_plant['herb_mentions'] += 1
                                output_plant['herb_confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            output_plants.append({
                                'herb_name_scientific': name, 
                                'herb_mentions': 1, 
                                'herb_confidence_score': int(score), 
                            })
            output_plants_final = []
            for output_plant in output_plants:
                output_plants_final.append({
                    'herb_name_scientific': output_plant['herb_name_scientific'],
                    'herb_mentions': int(output_plant['herb_mentions']),
                    'herb_confidence_score': int(output_plant['herb_confidence_score']),
                    'herb_total_score': int(output_plant['herb_mentions']) * int(output_plant['herb_confidence_score']),
                })
            output_plants_final = sorted(output_plants_final, key=lambda x: x['herb_total_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output_plant in output_plants_final:
                print(output_plant)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = output_plants_final[:items_num]
            json_write(json_filepath, data)

        ## preparations
        key = 'preparations'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            items_num = 20
            data_output = []
            for i in range(20):
                print(f'{ailment_i}/{len(ailments)}: {ailment}')
                prompt = f'''
                    Write a numbered list of the 10 most common herbal preparation used for {ailment_name}.
                    Also, give a confidence score in number format from 1 to 10 for each preparation representing how much you believe that herbal preparation is effective for the ailment.
                    For reference, examples of types of herbal preparations are: tea, decoction, tincture, creams, capsules, etc. 
                    Don't include herbs names in the praparations, just write the type of the preparation.
                    Write the names of the preparations using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"preparation_name": "name of preparation 1", "confidence_score": "10"}}, 
                        {{"preparation_name": "name of preparation 2", "confidence_score": "5"}}, 
                        {{"preparation_name": "name of preparation 3", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    preparations = []
                    for item in json_data:
                        try: name = item['preparation_name']
                        except: continue
                        try: 
                            score = item['confidence_score']
                            int(score)
                        except: continue
                        preparations.append({"name": name, "score": score})
                    for obj in preparations:
                        name = obj['name']
                        score = obj['score']
                        found = False
                        for obj in data_output:
                            if name in obj['name']: 
                                obj['mentions'] += 1
                                obj['score'] += int(score)
                                found = True
                                break
                        if not found:
                            data_output.append({
                                'name': name, 
                                'mentions': 1, 
                                'score': int(score), 
                            })
            data_output_final = []
            for obj in data_output:
                data_output_final.append({
                    'preparation_name': obj['name'],
                    'preparation_mentions': int(obj['mentions']),
                    'preparation_confidence_score': int(obj['score']),
                    'preparation_total_score': int(obj['mentions']) * int(obj['score']),
                })
            data_output_final = sorted(data_output_final, key=lambda x: x['preparation_total_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for obj in data_output_final:
                print(obj)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = data_output_final[:items_num]
            json_write(json_filepath, data)

        ########################################
        ########################################
        ########################################
        key = 'intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies'][:3]]
            preparations_names = [x['preparation_name'] for x in data['preparations'][:3]]
            prompt = f'''
                Write a detailed paragraph explaining why herbs and herbal preparations are good for {ailment_name}.
                Include the following herbs: {herbs_names}.
                Include the following herbal preparations: {preparations_names}.
                Include why it's important to deal with {ailment_name} and what are the consequences if you don't do it.
                Start with a definition of {ailment_name}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                Start with the following words: {ailment_name} is .
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        key = 'causes_intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            causes_names = [x['cause_name'] for x in data['causes'][:3]]
            prompt = f'''
                Write a detailed paragraph explaining what are the main causes of {ailment_name}.
                Include the following causes and explain why: {causes_names}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        for obj_i, obj in enumerate(data['causes'][:causes_num]):
            print(f'{ailment_i}/{len(ailments)} - {obj_i}/{causes_num} - {obj}')
            key = 'cause_desc'
            if key not in obj: obj[key] = ''
            # obj[key] = ''
            if obj[key] == '':
                cause_name = obj['cause_name']
                prompt = f'''
                    Write 1 detailed sentence explaining why {cause_name} is a cause of {ailment_name}.
                    Use simple and short words, and a simple writing style.
                '''
                reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
                obj[key] = reply
                json_write(json_filepath, data)

        key = 'remedies_intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies'][:3]]
            prompt = f'''
                Write a detailed paragraph explaining why herbs are good for {ailment_name}.
                Include the following herbs and expalin why they are good: {herbs_names}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        for remedy_i, obj in enumerate(data['remedies'][:remedies_num]):
            print(f'{ailment_i}/{len(ailments)} - {remedy_i}/{remedies_num} - {obj}')
            key = 'remedy_desc'
            if key not in obj: obj[key] = ''
            # obj[key] = ''
            if obj[key] == '':
                herb_name = obj['herb_name_scientific']
                prompt = f'''
                    Write a detailed paragraph explaining why {herb_name} is good for {ailment_name}.
                    Use simple and short words, and a simple writing style.
                    Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                '''
                reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
                obj[key] = reply
                json_write(json_filepath, data)

        key = 'preparations_intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            preparations_names = [x['preparation_name'] for x in data['preparations'][:3]]
            prompt = f'''
                Write a detailed paragraph explaining why herbal preparations are good for {ailment_name}.
                Include the following herbal preparations and explain why they are good: {preparations_names}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)
    
        for obj_i, obj in enumerate(data['preparations'][:preparations_num]):
            print(f'{ailment_i}/{len(ailments)} - {obj_i}/{remedies_num} - {obj}')
            key = 'preparation_desc'
            if key not in obj: obj[key] = ''
            # obj[key] = ''
            if obj[key] == '':
                preparation_name = obj['preparation_name']
                prompt = f'''
                    Write a detailed paragraph explaining why herbal {preparation_name} is good for {ailment_name}.
                    Use simple and short words, and a simple writing style.
                    Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                '''
                reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
                obj[key] = reply
                json_write(json_filepath, data)

        key = 'supplementary_avoid'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies'][:3]]
            prompt = f'''
                Write a detailed paragraph explaining what herbs to avoid if you have {ailment_name} and why.
                Never include the following herbs: {herbs_names}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        ########################################
        # ;html
        ########################################
        title = data['title']
        print(title)

        article_html = ''

        article_html += f'<h1>{title}</h1>\n'
        obj = data['remedies'][remedies_num-1]
        herb_name_scientific = obj['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
        out = f'{website_folderpath}/images/herbs/{herb_slug}-plant.jpg'
        src = f'/images/herbs/{herb_slug}-plant.jpg'
        if os.path.exists(out):
            article_html += f'<img src="{src}">\n'
        article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'
        article_html += f'<p>The following article lists the main herbal remedies used to treat {ailment_name}.</p>\n'

        # causes
        sub_title = f'What are the main causes of {ailment_name}?'.title()
        article_html += f'<h2>{sub_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["causes_intro_desc"])}\n'
        article_html += f'<p>Below are the main causes of {ailment_name}.</p>\n'
        article_html += f'<ul>\n'
        for obj_i, obj in enumerate(data['causes'][:causes_num]):
            cause_name = obj['cause_name']
            cause_desc = obj['cause_desc']
            article_html += f'<li><strong>{cause_name}</strong>: {cause_desc}</li>\n'
        article_html += f'</ul>\n'

        sub_title = f'{remedies_num} herbs for {ailment_name}'.title()
        article_html += f'<h2>{sub_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["remedies_intro_desc"])}\n'
        article_html += f'<p>Below are {remedies_num} healing hebs for {ailment_name}.</p>\n'
        for obj_i, obj in enumerate(data['remedies'][:remedies_num]):
            herb_name_scientific = obj['herb_name_scientific']
            herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
            remedy_desc = obj['remedy_desc']
            article_html += f'<h3>{obj_i+1}. {herb_name_scientific}</h3>\n'
            out = f'{website_folderpath}/images/herbs/{herb_slug}-plant.jpg'
            src = f'/images/herbs/{herb_slug}-plant.jpg'
            if os.path.exists(out):
                article_html += f'<img src="{src}">\n'
            article_html += f'{util.text_format_1N1_html(remedy_desc)}\n'

        sub_title = f'{preparations_num} herbal preparations for {ailment_name}'.title()
        article_html += f'<h2>{sub_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["preparations_intro_desc"])}\n'
        article_html += f'<p>Below are {preparations_num} effective hebal preparations for {ailment_name}.</p>\n'
        for obj_i, obj in enumerate(data['preparations'][:preparations_num]):
            preparation_name = obj['preparation_name']
            preparation_desc = obj['preparation_desc']
            preparation_slug_2 = preparation_name.strip().lower().replace(' ', '-') + 's'
            article_html += f'<h3>{obj_i+1}. {preparation_name}</h3>\n'
            out = f'{website_folderpath}/images/preparations/{ailment_slug}-herbal-{preparation_slug_2}.jpg'
            src = f'/images/preparations/{ailment_slug}-herbal-{preparation_slug_2}.jpg'
            if os.path.exists(out):
                article_html += f'<img src="{src}">\n'
            article_html += f'{util.text_format_1N1_html(preparation_desc)}\n'

        # supplementary avoid
        sub_title = f'What herbs to avoid if you have {ailment_name}?'.title()
        article_html += f'<h2>{sub_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["supplementary_avoid"])}\n'

        head_html = head_html_generate(title, '/style-article.css')
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                <main class="container-md">
                    {article_html}
                </main>
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)
        print(f'\n')
        print(html_filepath)
        # quit()

def articles_titles_check(preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    while 1:
        for ailment_i, ailment in enumerate(ailments):
            system_slug = ailment['system_slug']
            organ_slug = ailment['organ_slug']
            ailment_slug = ailment['ailment_slug']
            ailment_name = ailment['ailment_name']
            url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
            json_filepath = f'database/json/{url}.json'
            html_filepath = f'{website_folderpath}/{url}.html'
            if not os.path.exists(f'{website_folderpath}/remedies'): os.mkdir(f'{website_folderpath}/remedies')
            if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system'): os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system')
            if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system/{ailment_slug}'): os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system/{ailment_slug}')

            data = json_read(json_filepath, create=True)
            data['ailment_slug'] = ailment_slug
            data['ailment_name'] = ailment_name
            data['system_slug'] = system_slug
            data['organ_slug'] = organ_slug
            data['preparation_slug'] = preparation_slug
            data['preparation_name'] = preparation_name
            data['url'] = url
            if 'lastmod' not in data: data['lastmod'] = today()

            if 'remedies_num' not in data: data['remedies_num'] = ''
            # data['remedies_num'] = ''
            if data['remedies_num'] == '': data['remedies_num'] = random.randint(7, 11)
            remedies_num = data['remedies_num']
            
            print(f'{ailment_i}. {data["title"]}')

        '''
        valid = input('>> (x/v)')
        if valid == 'x':
            if os.path.exists(json_filepath): os.remove(json_filepath)
        '''
        break

def articles_preparations(preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        print(f'\n>> {ailment_i}/{len(ailments)} - preparation: {preparation_name}')
        print(f'    >> {ailment}')
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/remedies'): 
            os.mkdir(f'{website_folderpath}/remedies')
        if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system'): 
            os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system')
        if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system/{ailment_slug}'): 
            os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system/{ailment_slug}')
        # if os.path.exists(json_filepath): os.remove(json_filepath)
        # continue

        ################################################################################
        # ;json
        ################################################################################
        data = json_read(json_filepath, create=True)
        data['ailment_slug'] = ailment_slug
        data['ailment_name'] = ailment_name
        data['system_slug'] = system_slug
        data['organ_slug'] = organ_slug
        data['preparation_slug'] = preparation_slug
        data['preparation_name'] = preparation_name
        data['url'] = url
        if 'lastmod' not in data: data['lastmod'] = today()
        if 'remedies_num' not in data: data['remedies_num'] = ''
        # data['remedies_num'] = ''
        if data['remedies_num'] == '': data['remedies_num'] = random.choice(7, 9, 11)
        remedies_num = data['remedies_num']
        if 'title_2' not in data: data['title_2'] = data['title']
        data['title'] = f'{remedies_num} herbal {preparation_name} for {ailment_name}'.title()
        json_write(json_filepath, data)

        # ;remedies
        # generate herbs for article
        key = 'remedies'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            output_plants = []
            for i in range(10):
                print(f'{ailment_i}/{len(ailments)} - {i}: {ailment}')
                prompt = f'''
                    List the 15 best herbs to make herbal {preparation_name} to relieve {ailment_name} for {data["audience"]}.
                    Also, for each herb name give a confidence score from 1 to 10, indicating how sure you are that herbal {preparation_name} made with that herb is effective to relieve {ailment_name}.
                    Write only the scientific names (botanical names) of the plants used for the preparation, don't add descriptions or common names.
                    Write the names of the plants using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"herb_name_scientific": "scientific name of herb 1 used for preparation", "confidence_score": "10"}}, 
                        {{"herb_name_scientific": "scientific name of herb 2 used for preparation", "confidence_score": "5"}}, 
                        {{"herb_name_scientific": "scientific name of herb 3 used for preparation", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names_scientific = []
                    for item in json_data:
                        try: line = item['herb_name_scientific']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        print(line)
                        for plant in plants_wcvp:
                            name_scientific = plant['scientfiicname']
                            if name_scientific.lower().strip() in line.lower().strip():
                                if len(name_scientific.split(' ')) > 1:
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    print(name_scientific)
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    names_scientific.append({
                                        "name": name_scientific, 
                                        "score": score,
                                    })
                                    break
                        ## exceptions
                        if line.lower().strip() == 'mentha piperita':
                                names_scientific.append({"name": 'Mentha x piperita', "score": score})
                    for obj in names_scientific:
                        name = obj['name']
                        score = obj['score']
                        found = False
                        for output_plant in output_plants:
                            print(output_plant)
                            print(name, '->', output_plant['herb_name_scientific'])
                            if name in output_plant['herb_name_scientific']: 
                                output_plant['herb_mentions'] += 1
                                output_plant['herb_confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            output_plants.append({
                                'herb_name_scientific': name, 
                                'herb_mentions': 1, 
                                'herb_confidence_score': int(score), 
                            })
                output_plants_final = []
                for output_plant in output_plants:
                    output_plants_final.append({
                        'herb_name_scientific': output_plant['herb_name_scientific'],
                        'herb_mentions': int(output_plant['herb_mentions']),
                        'herb_confidence_score': int(output_plant['herb_confidence_score']),
                        'herb_total_score': int(output_plant['herb_mentions']) * int(output_plant['herb_confidence_score']),
                    })
                output_plants_final = sorted(output_plants_final, key=lambda x: x['herb_confidence_score'], reverse=True)
                print('***********************')
                print('***********************')
                print('***********************')
                for output_plant in output_plants_final:
                    print(output_plant)
                print('***********************')
                print('***********************')
                print('***********************')
                data[key] = output_plants_final[:remedies_num]
                json_write(json_filepath, data)
        # ;remedies (desc)
        for remedy_i, obj in enumerate(data['remedies']):
            print(f'{ailment_i}/{len(ailments)} - {remedy_i} - {preparation_name} - {obj}')
            key = 'remedy_desc'
            if key not in obj: obj[key] = ''
            # obj[key] = ''
            if obj[key] == '':
                herb_name = obj['herb_name_scientific']
                prompt = f'''
                    Write a 5-sentence paragraph explaining why {herb_name} {preparation_name} is good for {ailment_name}.
                    Include the boiactive constituents and the properties that help with this problem.
                    Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                    Use simple and short words, and a simple writing style.
                    Use a conversational and fluid writing style.
                    Don't write fluff.
                    Don't allucinate.
                    Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                    Start with the following words: {herb_name} {preparation_name} contains .
                '''
                reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
                obj[key] = reply
                json_write(json_filepath, data)
        # remedies (procedure)
        for remedy_i, obj in enumerate(data['remedies']):
            print(f'{ailment_i}/{len(ailments)} - {remedy_i} - {preparation_name} - {obj}')
            key = 'remedy_procedure'
            if key not in obj: obj[key] = ''
            # obj[key] = ''
            if obj[key] == '':
                herb_name = obj['herb_name_scientific']
                prompt = f'''
                    Write a 5-step procedure on how to make {herb_name} {preparation_name} for {ailment_name}.
                    Make the procedure easy to do and actionable.
                    Use simple and short words, and a simple writing style.
                    Write short and concise steps.
                    Use tablespoon, cup of, etc. as unit of measure.
                    Don't write fluff.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    {{
                        "step_1": "write step 1 here", 
                        "step_2": "write step 2 here", 
                        "step_3": "write step 3 here",
                        "step_4": "write step 4 here",
                        "step_5": "write step 5 here"
                    }} 
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    try: step_1 = json_data['step_1']
                    except: step_1 = ''
                    try: step_2 = json_data['step_2']
                    except: step_2 = ''
                    try: step_3 = json_data['step_3']
                    except: step_3 = ''
                    try: step_4 = json_data['step_4']
                    except: step_4 = ''
                    try: step_5 = json_data['step_5']
                    except: step_5 = ''
                    if step_1 != '' and step_2 != '' and step_3 != '' and step_4 != '' and step_5 != '':
                        obj[key] = [
                            step_1,
                            step_2,
                            step_3,
                            step_4,
                            step_5,
                        ]
                        json_write(json_filepath, data)
        if 0: # TODO: remove if condition
            # remedies (amazon)
            for remedy_i, obj in enumerate(data['remedies']):
                print(f'{ailment_i}/{len(ailments)} - {remedy_i} - {preparation_name} - {obj}')
                key = 'remedy_amazon'
                if key not in obj: obj[key] = ''
                # obj[key] = ''
                if obj[key] == '':
                    plant_slug = obj['herb_name_scientific'].lower().strip().replace(' ', '-')
                    # ;amazon
                    products_jsons_folderpath = f'{vault}/amazon/{preparation_slug}/json/{plant_slug}' 
                    if not os.path.exists(products_jsons_folderpath): continue
                    products_jsons_filepaths = [
                        f'{products_jsons_folderpath}/{x}' 
                        for x in os.listdir(products_jsons_folderpath)
                    ]
                    # order filepaths by popularity
                    products_jsons = []
                    for i, product_json_filepath in enumerate(products_jsons_filepaths):
                        product_data = json_read(product_json_filepath)
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
                    obj[key] = affiliate_product
                    json_write(json_filepath, data)

        # ;intro (desc)
        key = 'intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies']]
            herbs_names_prompt = ', '.join(herbs_names[:3])
            prompt = f'''
                Write a detailed paragraph about: herbal {data["preparation_name"]} for {data["ailment_name"]}.
                Explaining why herbal teas relieve {data["ailment_name"]} and what benefits this brings to your life.
                Mention the following herbs as an example: {herbs_names_prompt}.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)
        ## ------------------------------------
        ## ;faq
        ## ------------------------------------
        faqs = [
            {'key': 'faq_prevent', 'question': f'Can drinking herbal tea prevent {ailment_name} from forming?',},
            {'key': 'faq_safe', 'question': f'Is it safe to consume herbal teas for {ailment_name} every day?',},
            {'key': 'faq_timeline', 'question': f'How long does it take for herbal teas to show results in {ailment_name}?',},
            {'key': 'faq_time', 'question': f'What time of day is best to drink herbal tea for {ailment_name}?',},
            {'key': 'faq_time', 'question': f'What time of day is best to drink herbal tea for {ailment_name}?',},
            {'key': 'faq_interaction', 'question': f'Can herbal teas interact with prescription medications for {ailment_name}?',},
            {'key': 'faq_pregnant', 'question': f'Is it safe to cunsume herbal teas for {ailment_name} while pregnant?',},
            {'key': 'faq_breastfeeding', 'question': f'Is it safe to cunsume herbal teas for {ailment_name} while breastfeeding?',},
        ]
        for faq in faqs:
            key = faq['key']
            question = faq['question']
            if key not in data: data[key] = ''
            # data[key] = ''
            if data[key] == '':
                prompt = f'''
                    Write a short paragraph in less than 60 words that answer the following question: {question}
                    Use simple and short words, and a simple writing style.
                    Use a conversational and fluid writing style.
                    Don't write lists.
                    Don't write fluff.
                    Don't allucinate.
                    Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                    Don't mention consulting a doctor, healthcare professional or similar.
                '''
                reply = llm_reply(prompt).strip()
                reply = [line.strip() for line in reply.split('\n')]
                reply = ' '.join(reply)
                data[key] = reply
                json_write(json_filepath, data)

        ########################################
        # ;html
        ########################################
        title = data['title']
        article_html = ''
        article_html += f'<h1>{title}</h1>\n'
        src = data['intro_image_src']
        alt = data['intro_image_alt']
        article_html += f'<img class="article-img" src="{src}" alt="{alt}">\n'
        article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'
        if ads_manual:
            ad_html = f'''
                <div class="mb-48">
                    {GOOGLE_ADSENSE_DISPLAY_AD_SQUARE}
                </div>
            '''
        else:
            ad_html = ''
        article_html += f'{ad_html}\n'
        # article_html += '[checklist]\n'
        article_html += '[toc]\n'
        for remedy_i, remedy in enumerate(data['remedies']):
            article_html += f'<h2>{remedy_i+1}. {remedy["herb_name_scientific"]}</h2>\n'
            src = remedy['image_src']
            alt = remedy['image_alt']
            article_html += f'<img class="article-img" src="{src}" alt="{alt}">\n'
            article_html += f'{util.text_format_1N1_html(remedy["remedy_desc"])}\n'
            article_html += f'<ol>\n'
            for step in remedy['remedy_procedure']:
                article_html += f'<li>\n'
                article_html += f'{step}\n'
                article_html += f'</li>\n'
            article_html += f'</ol>\n'
            # amazon affiliate card (if exists)
            if 'remedy_amazon' in remedy and remedy['remedy_amazon'] != '':
                herb_name_scientific = remedy['herb_name_scientific']
                aff_link_url = remedy['remedy_amazon']['affiliate_link']
                aff_link_title = remedy['remedy_amazon']['title']
                _html = gen_aff_html(aff_link_url, aff_link_title, herb_name_scientific)
                article_html += _html
        related_blocks_html = ''
        sidebar_populars = []
        if 0:
            article_html += f'<h2>FAQ</h2>\n'
            faqs = faqs[:random.randint(3, 4)]
            for faq in faqs:
                key = faq['key']
                question = faq['question']
                article_html += f'<h3>{question.capitalize()}</h3>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'
            
            ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
            ailments_slugs = []
            for ailment in ailments:
                _system_slug = ailment['system_slug']
                _ailment_slug = ailment['ailment_slug']
                if _system_slug == system_slug:
                    ailments_slugs.append(_ailment_slug)
            random.shuffle(ailments_slugs)
            for _ailment_slug in ailments_slugs[6:9]:
                _url = f'remedies/{system_slug}-system/{_ailment_slug}'
                _json_filepath = f'database/json/{_url}.json'
                _html_filepath = f'{website_folderpath}/{_url}.html'
                _data = json_read(_json_filepath)
                _ailment_name = _data['ailment_name']
                _title = _data['title']
                _src = f'/images/ailments/{_ailment_slug}-herbal-remedies.jpg'
                _alt = f'herbal remedies for {_ailment_name}'
                sidebar_populars.append({
                    'src': _src,
                    'title': _title,
                    'href': f'/{_url}.html',
                })
            for _ailment_slug in ailments_slugs[:6]:
                _url = f'remedies/{system_slug}-system/{_ailment_slug}'
                _json_filepath = f'database/json/{_url}.json'
                _html_filepath = f'{website_folderpath}/{_url}.html'
                _data = json_read(_json_filepath)
                _ailment_name = _data['ailment_name']
                _title = _data['title']
                _src = f'/images/ailments/{_ailment_slug}-herbal-remedies.jpg'
                _alt = f'herbal remedies for {_ailment_name}'
                _href = f'/{_url}.html'
                related_blocks_html += f'''
                    <a class="no-underline text-black" href="{_href}">
                        <div>
                            <img src="{_src}" alt="{_alt}">
                            <h3 class="h3-plain hover-orange text-14 mt-16">{_title}<h3>
                        </div>
                    </a>
                '''
        breadcrumbs_html_filepath = f'{url}.html'
        breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
        meta_html = gen_meta(article_html, data["lastmod"])
        # article_html = components.table_of_contents(article_html)
        toc_html = components.table_of_contents_2(article_html)
        article_html = article_html.replace('[toc]', toc_html)
        # checklist
        with open('assets/newsletter/sign-in-form.txt') as f: sign_in_form_html = f.read()
        _html = checklist_gen(sign_in_form_html)
        article_html = article_html.replace('[checklist]', _html)
        head_html = head_html_generate(data['title'], '/style.css')
        social_html = html_article_social()
        popular_blocks_html = html_article_popular_blocks(sidebar_populars)
        popular_html = html_article_popular(f'{system_slug} system', popular_blocks_html)
        sidebar_html = html_article_sidebar(popular_html, social_html)
        related_html = html_article_related(related_blocks_html)
        related_html = ''
        main_html = html_article_main(meta_html, article_html, related_html)
        layout_html = html_article_layout(main_html, '')
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                {layout_html}
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)
        print(f'\n')
        print(html_filepath)
        # quit()

def gen_ai_data(json_filepath, data, key, prompt, herb_i, outputs_num=20):
    if key not in data: data[key] = []
    # data[key] = []
    if data[key] == []:
        outputs = []
        for i in range(20):
            print(f'{herb_i} - {data["herb_name_scientific"]}')
            reply = llm_reply(prompt, model).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = []
                for item in json_data:
                    try: name = item['name'].lower().strip()
                    except: continue
                    try: score = item['confidence_score']
                    except: continue
                    _objs.append({
                        "name": name, 
                        "score": score,
                    })
                for _obj in _objs:
                    name = _obj['name']
                    score = _obj['score']
                    found = False
                    for output in outputs:
                        if name in output['name']: 
                            output['mentions'] += 1
                            output['confidence_score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'name': name, 
                            'mentions': 1, 
                            'confidence_score': int(score), 
                        })
        outputs_final = []
        for output in outputs:
            outputs_final.append({
                'name': output['name'],
                'mentions': int(output['mentions']),
                'confidence_score': int(output['confidence_score']),
                'total_score': int(output['mentions']) * int(output['confidence_score']),
            })
        outputs_final = sorted(outputs_final, key=lambda x: x['confidence_score'], reverse=True)
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs_final:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        data[key] = outputs_final[:outputs_num]
        json_write(json_filepath, data)

def a_herbs_popular():
    popular_herbs = get_popular_herbs_from_teas_articles()
    for herb_i, herb in enumerate(popular_herbs[:]):
        print(f'{herb_i} - {herb}')
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        family_name = ''
        family_slug = family_name.strip().lower().replace(' ', '-').replace('.', '')
        url = f'herbs/{herb_slug}'
        title = herb_name_scientific
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/herbs'): os.mkdir(f'{website_folderpath}/herbs')

        # if os.path.exists(json_filepath): os.remove(json_filepath)
        # continue

        data = json_read(json_filepath, create=True)
        data['title'] = title
        data['herb_slug'] = herb_slug
        data['herb_name_scientific'] = herb_name_scientific
        data['family_slug'] = family_slug
        data['family_name'] = family_name
        data['url'] = url
        if 'lastmod' not in data: data['lastmod'] = today()
        json_write(json_filepath, data)

        # ;common_names
        gen_ai_data(
            json_filepath,
            data=data, 
            key='herb_names_common', 
            prompt = f'''
                Write a list of the 10 most common names the herb with the following botanical (scientific) name: {herb_name_scientific}.
                Also, give a confidence score from 1 to 10 for each common name, indicating how sure you are about that common name.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"name": <write the common name 1 here>, "confidence_score": 8}},
                    {{"name": <write the common name 2 here>, "confidence_score": 6}},
                    {{"name": <write the common name 3 here>, "confidence_score": 9}}
                ]
                Only reply with the JSON, don't add additional info.
                Don't include notes, reply ONLY with the JSON.
            ''',
            herb_i=herb_i,
        )

        key = 'medicine_or_poison'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            outputs = []
            for i in range(20):
                print(f'{herb_i} - {herb}')
                prompt = f'''
                    Tell me if the following herb is considered medicinal or poisonous: {herb_name_scientific}.
                    Also, tell give a confidence score from 1 to 10, indicating how sure you are about your answer.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"medicine_or_poison": <write "medicine" or "poison" here>, "confidence_score": 8}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                    Don't include notes, reply ONLY with the JSON.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    _objs = []
                    for item in json_data:
                        try: name = item['medicine_or_poison']
                        except: 
                            print('FAILEDE: name ********************')
                            continue
                        try: score = item['confidence_score']
                        except: 
                            print('FAILEDE: score ********************')
                            continue
                        _objs.append({
                            "name": name, 
                            "score": score,
                        })
                    for _obj in _objs:
                        name = _obj['name']
                        score = _obj['score']
                        found = False
                        for output in outputs:
                            # print(output)
                            # print(name, '->', output['constituent_name'])
                            if name in output['medicine_or_poison']: 
                                output['mentions'] += 1
                                output['confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            outputs.append({
                                'medicine_or_poison': name, 
                                'mentions': 1, 
                                'confidence_score': int(score), 
                            })
            outputs_final = []
            for output in outputs:
                outputs_final.append({
                    'medicine_or_poison': output['medicine_or_poison'],
                    'mentions': int(output['mentions']),
                    'confidence_score': int(output['confidence_score']),
                    'total_score': int(output['mentions']) * int(output['confidence_score']),
                })
            outputs_final = sorted(outputs_final, key=lambda x: x['confidence_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output in outputs_final:
                print(output)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = outputs_final
            json_write(json_filepath, data)

        medicine_or_poison = data['medicine_or_poison']
        medicine = {'medicine_or_poison': 'medicine', 'total_score': 0}
        for _obj in medicine_or_poison:
            if 'medicine' in _obj['medicine_or_poison']: 
                medicine = _obj
                break
        poison = {'medicine_or_poison': 'poison', 'total_score': 0}
        for _obj in medicine_or_poison:
            if 'poison' in _obj['medicine_or_poison']: 
                poison = _obj
                break

        if medicine['total_score'] <= poison['total_score']: continue

        # what is it
        key = 'what_description'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            print(f'{herb_i} - {herb}')
            family_name = data['family_name'].strip()
            if family_name != '': family_prompt = f'Include the fact that it belongs to the family: {family_name}'
            else: family_prompt = ''
            prompt = f'''
                Write 1 detailed paragraph about what is the plant {herb_name_scientific}.
                Include botanical characteristics.
                Include the fact that it belongs to the family: {family_name}.
                Pack as much information in as few words as possible.
                Don't write fluff, only proven data.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Don't allucinate.
                Write the paragraph in 5 sentences.
                Write only the paragraph, don't add additional info.
                Don't add references or citations.
                Start with the following words: {herb_name_scientific} is .
                Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
            '''
            print(prompt)
            reply = llm_reply(prompt, model)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)

        with open('database/herbs-category-actions.txt') as f: categories = f.read().strip().split('\n')
        categories_prompt = ', '.join(categories)
        key = 'category_action'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            print(f'{herb_i} - {herb}')
            prompt = f'''
                Tell me in which category would you classify of the following herb bases on its medicianl action: {herb_name_scientific}.
                Also, give a confidence score from 1 to 10 for the category, indicating how sure you are about that.
                Choose only one of the following categories: {categories_prompt}.
                Reply in as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                {{
                    "name": <write name of category here>, 
                    "confidence_score": 8
                }} 
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if 'name' in json_data:
                data[key] = json_data['name'].lower().strip()
                json_write(json_filepath, data)
        
        # ailments (uses)
        gen_ai_data(
            json_filepath,
            data=data, 
            key='ailments', 
            prompt = f'''
                Write a list of the 10 most common ailments the plant {herb_name_scientific} can help.
                Also, give a confidence score from 1 to 10 for each ailment, indicating how sure you are about thet ailment.
                Write only 1 ailment for each list item.
                Never write the word "and".
                Write only the names of the ailment, don't add descriptions.
                Write the as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the structure in the following example:
                [
                    {{"name": "<insert name of ailment 1 here>", "confidence_score": 10}},
                    {{"name": "<insert name of ailment 2 here>", "confidence_score": 5}},
                    {{"name": "<insert name of ailment 3 here>", "confidence_score": 7}}
                ]
                Reply only with the JSON, don't add additional content.
                Don't include notes, reply ONLY with the JSON.
            ''',
            herb_i=herb_i
        )

        key = 'ailments_description'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            names = [ailment['name'].lower().strip() for ailment in data['ailments']]
            names_prompt = ', '.join(names)
            prompt = f'''
                Write 1 detailed paragraph about what are the most common ailments you can heal withthe plant {herb_name_scientific}.
                In specific, discuss the following ailments in this exact order: {names_prompt}.
                Only mention an ailment once throughout the paragraph, don't name the same ailment multiple times.
                Pack as much information in as few words as possible.
                Don't write fluff, only proven data.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Don't allucinate.
                Write the paragraph in 5 sentences.
                Write only the paragraph, don't add additional info.
                Don't add references or citations.
                Start with the following words: The most common ailments you can heal with {herb_name_scientific} are .
                Don't include all the ailments in the first sentence, but distribute them homogeneously throughout the paragraph.
                Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
            '''
            print(prompt)
            reply = llm_reply(prompt, model)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)

        # ;properties
        gen_ai_data(
            json_filepath,
            data=data, 
            key='properties', 
            prompt = f'''
                Write a list of the 10 most important medicinal properties of the plant: {herb_name_scientific}.
                Examples of properties are: antimicrobial, antioxidant, anti-inflammatory, analgesic, etc.
                Also, give a confidence score from 1 to 10 for each property, indicating how sure you are about that property.
                Write as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"name": <write the name of property 1 here>, "confidence_score": 8}},
                    {{"name": <write the name of property 2 here>, "confidence_score": 6}},
                    {{"name": <write the name of property 3 here>, "confidence_score": 9}}
                ]
                Only reply with the JSON, don't add additional info.
                Don't include notes, reply ONLY with the JSON.
            ''',
            herb_i=herb_i
        )

        key = 'properties_description'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            names = [obj['name'].lower().strip() for obj in data['properties']]
            names_prompt = ', '.join(names[:5])
            prompt = f'''
                Write 1 detailed paragraph about what are the therapeutic properties of the plant {herb_name_scientific}, and explain what are the bioactive compounds of this plant that are responsible for the medicinal properties.
                Discuss the following medicinal properties in this exact order: {names_prompt}.
                Examples of bioactive compounds are like: flavonoids, saponins, volatile oils, etc.
                The main subjects of the sentences are the medicinal properties, not the bioactive compounds.
                Only mention a medicinal property once throughout the paragraph, don't name the same medicinal property multiple times.
                Pack as much information in as few words as possible.
                Don't write fluff, only proven data.
                Don't allucinate.
                Write the paragraph in 5 sentences.
                Write only the paragraph, don't add additional info.
                Don't add references or citations.
                Start with the following words: The main therapeutic properties of {herb_name_scientific} are .
                Don't include all the properties in the first sentence, but distribute them homogeneously throughout the paragraph.
                Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
            '''
            print(prompt)
            reply = llm_reply(prompt, model)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)

        # constituents
        gen_ai_data(
            json_filepath,
            data=data, 
            key='constituents', 
            prompt = f'''
                Write a list of the 10 most important medicinal constituents of the following herb: {herb_name_scientific}.
                Also, give a confidence score from 1 to 10 for each constituent, indicating how sure you are about that constituent.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"name": <write the name of constituent 1 here>, "confidence_score": 8}},
                    {{"name": <write the name of consitutent 2 here>, "confidence_score": 6}},
                    {{"name": <write the name of consitutent 3 here>, "confidence_score": 9}}
                ]
                Only reply with the JSON, don't add additional info.
                Don't include notes, reply ONLY with the JSON.
            ''',
            herb_i=herb_i
        )

        key = 'constituents_description'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            names = [obj['name'].lower().strip() for obj in data['constituents']]
            names_prompt = ', '.join(names[:5])
            prompt = f'''
                Write 1 detailed paragraph about what are the healing constituents of {herb_name_scientific} and explain why.
                Include the following constituents: {names_prompt}.
                Pack as much information in as few words as possible.
                Don't write fluff, only proven data.
                Don't allucinate.
                Don't write the character ";".
                Write the paragraph in 5 sentences.
                Start the reply with the following words: The most important healing constituents of {herb_name_scientific} are .
            '''
            print(prompt)
            reply = llm_reply(prompt, model)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)

        # common names
        gen_ai_data(
            json_filepath,
            data=data, 
            key='herb_names_common', 
            prompt = f'''
                Write a list of the most common names of the plant with scientific (botanical) name: {herb_name_scientific}.
                Also, give a confidence score from 1 to 10 for each common name, indicating how sure you are about that common name.
                Write only 1 common name for each list item.
                Never write the word "and".
                Write only the common names, don't add descriptions.
                Write the as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the structure in the following example:
                [
                    {{"name": "<insert common name 1 here>", "confidence_score": 10}},
                    {{"name": "<insert common name 2 here>", "confidence_score": 5}},
                    {{"name": "<insert common name 3 here>", "confidence_score": 7}}
                ]
                Reply only with the JSON, don't add additional content.
                Don't include notes, reply ONLY with the JSON.
            ''',
            herb_i=herb_i
        )

        # ;preparations
        gen_ai_data(
            json_filepath,
            data=data, 
            key='preparations', 
            prompt = f'''
                Write a list of the most common herbal preparations you make with {herb_name_scientific}.
                Also, give a confidence score from 1 to 10 for each preparation, indicating how sure you are about that preparation.
                Write only 1 preparation for each list item.
                Never use the word "and".
                Write only the names of the preparation, don't add descriptions.
                Write the as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in JSON format using the structure in the following example:
                [
                    {{"name": "<insert name of preparation 1 here>", "confidence_score": "10"}},
                    {{"name": "<insert name of preparation 2 here>", "confidence_score": "5"}},
                    {{"name": "<insert name of preparation 3 here>", "confidence_score": "7"}}
                ]
                Reply only with the JSON, don't add additional content.
            ''',
            herb_i=herb_i
        )

        key = 'preparations_description'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            names = [obj['name'].lower().strip() for obj in data['preparations']]
            names_prompt = ', '.join(names[:5])
            prompt = f'''
                Write 1 detailed paragraph about what are the herbal preparations of {herb_name_scientific} and explain why.
                Include the following preparations: {names_prompt}.
                Pack as much information in as few words as possible.
                Don't write fluff, only proven data.
                Don't allucinate.
                Don't write the character ";".
                Write the paragraph in 5 sentences.
                Start the reply with the following words: The main herbal preparations of {herb_name_scientific} are .
            '''
            print(prompt)
            reply = llm_reply(prompt, model)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)

        # ;side_effects
        gen_ai_data(
            json_filepath,
            data=data, 
            key='side_effects', 
            prompt = f'''
                Write a list of 10 possible side effects of impropertly using the plant {herb_name_scientific} medicinally.
                Also, give a confidence score from 1 to 10 for each side effect, indicating how sure you are about that side effect.
                Write only the names of the side effects, don't add descriptions.
                Start each list item with a third-person singular actionable verb.
                Write only 1 side effect for each list item.
                Never use the word "and".
                Write only the names of the side effect, don't add descriptions.
                Write the as few words as possible.
                Don't write fluff, only proven data.
                Don't allucinate.
                Reply in JSON format using the following structure:
                [
                    {{"name": "<insert name of side effect 1 here>", "confidence_score": "10"}},
                    {{"name": "<insert name of side effect 2 here>", "confidence_score": "5"}},
                    {{"name": "<insert name of side effect 3 here>", "confidence_score": "7"}}
                ]
                Reply only with the JSON, don't add additional content.
            ''',
            herb_i=herb_i
        )

        key = 'side_effects_description'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            names = [obj['name'].lower().strip() for obj in data['side_effects']]
            names_prompt = ', '.join(names[:5])
            prompt = f'''
                Write 1 detailed paragraph about what are the possible side effects of using {herb_name_scientific} improperly and explain why.
                Include the following side effects: {names_prompt}.
                Pack as much information in as few words as possible.
                Don't write fluff, only proven data.
                Don't allucinate.
                Don't write the character ";".
                Write the paragraph in 5 sentences.
                Start the reply with the following words: The possible side effect of using {herb_name_scientific} are .
            '''
            print(prompt)
            reply = llm_reply(prompt, model)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)

        ##############################################################
        # ;html
        ##############################################################
        article_html = ''
        article_html += f'<h1 class="">{data["title"]}</h1>\n'

        article_html += f'<h2>What is {data["herb_name_scientific"]}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["what_description"])}\n'

        article_html += f'<h2>What ailments can you heal with this herb?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["ailments_description"])}\n'

        article_html += f'<h2>What are the therapeutic properties this herb?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["properties_description"])}\n'

        article_html += f'<h2>What are the medicinal constituents this herb?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["constituents_description"])}\n'

        article_html += f'<h2>What are the main herbal preparations this herb?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["preparations_description"])}\n'

        article_html += f'<h2>What are the possible side effects of using this herb improperly?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["side_effects_description"])}\n'

        breadcrumbs_html_filepath = f'{url}.html'
        breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
        meta_html = gen_meta(article_html, data["lastmod"])
        article_html = components.table_of_contents(article_html)
        head_html = head_html_generate(data['title'], '/style.css')

        social_html = html_article_social()
        sidebar_html = html_article_sidebar('', social_html)

        main_html = html_article_main(meta_html, article_html, '')
        layout_html = html_article_layout(main_html, sidebar_html)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                {breadcrumbs_html}
                {layout_html}
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)
        print(f'\n')
        print(html_filepath)
        # quit()


def a_herbs_wcvp():
    global plants_wcvp
    if plants_wcvp == []:
        plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    plants_wcvp_tmp = plants_wcvp[:HERBS_TO_GEN_NUM]
    # plants_wcvp_tmp = plants_wcvp[:]
    for herb_i, herb in enumerate(plants_wcvp_tmp):
        print(f'{herb_i} - {herb}')
        herb_name_scientific = herb['scientfiicname']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        family_name = herb['family']
        family_slug = family_name.strip().lower().replace(' ', '-').replace('.', '')
        url = f'herbs/{herb_slug}'
        title = herb_name_scientific
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/herbs'): os.mkdir(f'{website_folderpath}/herbs')

        # if os.path.exists(json_filepath): os.remove(json_filepath)
        # continue

        data = json_read(json_filepath, create=True)
        data['title'] = title
        data['herb_slug'] = herb_slug
        data['herb_name_scientific'] = herb_name_scientific
        data['family_slug'] = family_slug
        data['family_name'] = family_name
        data['url'] = url
        if 'lastmod' not in data: data['lastmod'] = today()
        json_write(json_filepath, data)


        if 0:
            key = 'medicine_or_poison'
            if key not in data: data[key] = ''
            # data[key] = ''
            if data[key] == '':
                outputs = []
                for i in range(20):
                    print(f'{herb_i} - {herb}')
                    prompt = f'''
                        Tell me if the following herb is considered medicinal or poisonous: {herb_name_scientific}.
                        Also, tell give a confidence score from 1 to 10, indicating how sure you are about your answer.
                        Don't write fluff, only proven facts.
                        Don't allucinate.
                        Reply in the following JSON format: 
                        [
                            {{"medicine_or_poison": <write "medicine" or "poison" here>, "confidence_score": 8}} 
                        ]
                        Only reply with the JSON, don't add additional info.
                        Don't include notes, reply ONLY with the JSON.
                    '''
                    reply = llm_reply(prompt, model).strip()
                    json_data = {}
                    try: json_data = json.loads(reply)
                    except: pass 
                    if json_data != {}:
                        _objs = []
                        for item in json_data:
                            try: name = item['medicine_or_poison']
                            except: 
                                print('FAILEDE: name ********************')
                                continue
                            try: score = item['confidence_score']
                            except: 
                                print('FAILEDE: score ********************')
                                continue
                            _objs.append({
                                "name": name, 
                                "score": score,
                            })
                        for _obj in _objs:
                            name = _obj['name']
                            score = _obj['score']
                            found = False
                            for output in outputs:
                                # print(output)
                                # print(name, '->', output['constituent_name'])
                                if name in output['medicine_or_poison']: 
                                    output['mentions'] += 1
                                    output['confidence_score'] += int(score)
                                    found = True
                                    break
                            if not found:
                                outputs.append({
                                    'medicine_or_poison': name, 
                                    'mentions': 1, 
                                    'confidence_score': int(score), 
                                })
                outputs_final = []
                for output in outputs:
                    outputs_final.append({
                        'medicine_or_poison': output['medicine_or_poison'],
                        'mentions': int(output['mentions']),
                        'confidence_score': int(output['confidence_score']),
                        'total_score': int(output['mentions']) * int(output['confidence_score']),
                    })
                outputs_final = sorted(outputs_final, key=lambda x: x['confidence_score'], reverse=True)
                print('***********************')
                print('***********************')
                print('***********************')
                for output in outputs_final:
                    print(output)
                print('***********************')
                print('***********************')
                print('***********************')
                data[key] = outputs_final
                json_write(json_filepath, data)

            medicine_or_poison = data['medicine_or_poison']
            medicine = {'medicine_or_poison': 'medicine', 'total_score': 0}
            for _obj in medicine_or_poison:
                if 'medicine' in _obj['medicine_or_poison']: 
                    medicine = _obj
                    break
            poison = {'medicine_or_poison': 'poison', 'total_score': 0}
            for _obj in medicine_or_poison:
                if 'poison' in _obj['medicine_or_poison']: 
                    poison = _obj
                    break

            if medicine['total_score'] <= poison['total_score']: continue

            # what is it
            key = 'what_description'
            if key not in data: data[key] = ''
            # data[key] = ''
            if data[key] == '':
                print(f'{herb_i} - {herb}')
                family_name = data['family_name'].strip()
                if family_name != '': family_prompt = f'Include the fact that it belongs to the family: {family_name}'
                else: family_prompt = ''
                prompt = f'''
                    Write 1 detailed paragraph about what is the plant {herb_name_scientific}.
                    Include botanical characteristics.
                    Include the fact that it belongs to the family: {family_name}.
                    Pack as much information in as few words as possible.
                    Don't write fluff, only proven data.
                    Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                    Don't allucinate.
                    Write the paragraph in 5 sentences.
                    Write only the paragraph, don't add additional info.
                    Don't add references or citations.
                    Start with the following words: {herb_name_scientific} is .
                    Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
                '''
                print(prompt)
                reply = llm_reply(prompt, model)
                lines = []
                for line in reply.split('\n'):
                    line = line.strip()
                    if line == '': continue
                    if ':' in line: continue
                    lines.append(line)
                if len(lines) == 1:
                    data[key] = lines[0]
                    json_write(json_filepath, data)

            with open('database/herbs-category-actions.txt') as f: categories = f.read().strip().split('\n')
            categories_prompt = ', '.join(categories)
            key = 'category_action'
            if key not in data: data[key] = ''
            # data[key] = ''
            if data[key] == '':
                print(f'{herb_i} - {herb}')
                prompt = f'''
                    Tell me in which category would you classify of the following herb bases on its medicianl action: {herb_name_scientific}.
                    Also, give a confidence score from 1 to 10 for the category, indicating how sure you are about that.
                    Choose only one of the following categories: {categories_prompt}.
                    Reply in as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    {{
                        "name": <write name of category here>, 
                        "confidence_score": 8
                    }} 
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if 'name' in json_data:
                    data[key] = json_data['name'].lower().strip()
                    json_write(json_filepath, data)
            
            # ailments (uses)
            gen_ai_data(
                json_filepath,
                data=data, 
                key='ailments', 
                prompt = f'''
                    Write a list of the 10 most common ailments the plant {herb_name_scientific} can help.
                    Also, give a confidence score from 1 to 10 for each ailment, indicating how sure you are about thet ailment.
                    Write only 1 ailment for each list item.
                    Never write the word "and".
                    Write only the names of the ailment, don't add descriptions.
                    Write the as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in JSON format using the structure in the following example:
                    [
                        {{"name": "<insert name of ailment 1 here>", "confidence_score": 10}},
                        {{"name": "<insert name of ailment 2 here>", "confidence_score": 5}},
                        {{"name": "<insert name of ailment 3 here>", "confidence_score": 7}}
                    ]
                    Reply only with the JSON, don't add additional content.
                    Don't include notes, reply ONLY with the JSON.
                ''',
                herb_i=herb_i
            )

            key = 'ailments_description'
            if key not in data: data[key] = ''
            # data[key] = ''
            if data[key] == '':
                names = [ailment['name'].lower().strip() for ailment in data['ailments']]
                names_prompt = ', '.join(names)
                prompt = f'''
                    Write 1 detailed paragraph about what are the most common ailments you can heal withthe plant {herb_name_scientific}.
                    In specific, discuss the following ailments in this exact order: {names_prompt}.
                    Only mention an ailment once throughout the paragraph, don't name the same ailment multiple times.
                    Pack as much information in as few words as possible.
                    Don't write fluff, only proven data.
                    Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                    Don't allucinate.
                    Write the paragraph in 5 sentences.
                    Write only the paragraph, don't add additional info.
                    Don't add references or citations.
                    Start with the following words: The most common ailments you can heal with {herb_name_scientific} are .
                    Don't include all the ailments in the first sentence, but distribute them homogeneously throughout the paragraph.
                    Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
                '''
                print(prompt)
                reply = llm_reply(prompt, model)
                lines = []
                for line in reply.split('\n'):
                    line = line.strip()
                    if line == '': continue
                    if ':' in line: continue
                    lines.append(line)
                if len(lines) == 1:
                    data[key] = lines[0]
                    json_write(json_filepath, data)

            # ;properties
            gen_ai_data(
                json_filepath,
                data=data, 
                key='properties', 
                prompt = f'''
                    Write a list of the 10 most important medicinal properties of the plant: {herb_name_scientific}.
                    Examples of properties are: antimicrobial, antioxidant, anti-inflammatory, analgesic, etc.
                    Also, give a confidence score from 1 to 10 for each property, indicating how sure you are about that property.
                    Write as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"name": <write the name of property 1 here>, "confidence_score": 8}},
                        {{"name": <write the name of property 2 here>, "confidence_score": 6}},
                        {{"name": <write the name of property 3 here>, "confidence_score": 9}}
                    ]
                    Only reply with the JSON, don't add additional info.
                    Don't include notes, reply ONLY with the JSON.
                ''',
                herb_i=herb_i
            )

            key = 'properties_description'
            if key not in data: data[key] = ''
            # data[key] = ''
            if data[key] == '':
                names = [obj['name'].lower().strip() for obj in data['properties']]
                names_prompt = ', '.join(names[:5])
                prompt = f'''
                    Write 1 detailed paragraph about what are the therapeutic properties of the plant {herb_name_scientific}, and explain what are the bioactive compounds of this plant that are responsible for the medicinal properties.
                    Discuss the following medicinal properties in this exact order: {names_prompt}.
                    Examples of bioactive compounds are like: flavonoids, saponins, volatile oils, etc.
                    The main subjects of the sentences are the medicinal properties, not the bioactive compounds.
                    Only mention a medicinal property once throughout the paragraph, don't name the same medicinal property multiple times.
                    Pack as much information in as few words as possible.
                    Don't write fluff, only proven data.
                    Don't allucinate.
                    Write the paragraph in 5 sentences.
                    Write only the paragraph, don't add additional info.
                    Don't add references or citations.
                    Start with the following words: The main therapeutic properties of {herb_name_scientific} are .
                    Don't include all the properties in the first sentence, but distribute them homogeneously throughout the paragraph.
                    Don't include a conclusory statement with words like overall, in summary, or in conclusion. 
                '''
                print(prompt)
                reply = llm_reply(prompt, model)
                lines = []
                for line in reply.split('\n'):
                    line = line.strip()
                    if line == '': continue
                    if ':' in line: continue
                    lines.append(line)
                if len(lines) == 1:
                    data[key] = lines[0]
                    json_write(json_filepath, data)

            # constituents
            gen_ai_data(
                json_filepath,
                data=data, 
                key='constituents', 
                prompt = f'''
                    Write a list of the 10 most important medicinal constituents of the following herb: {herb_name_scientific}.
                    Also, give a confidence score from 1 to 10 for each constituent, indicating how sure you are about that constituent.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"name": <write the name of constituent 1 here>, "confidence_score": 8}},
                        {{"name": <write the name of consitutent 2 here>, "confidence_score": 6}},
                        {{"name": <write the name of consitutent 3 here>, "confidence_score": 9}}
                    ]
                    Only reply with the JSON, don't add additional info.
                    Don't include notes, reply ONLY with the JSON.
                ''',
                herb_i=herb_i
            )

            key = 'constituents_description'
            if key not in data: data[key] = ''
            # data[key] = ''
            if data[key] == '':
                names = [obj['name'].lower().strip() for obj in data['constituents']]
                names_prompt = ', '.join(names[:5])
                prompt = f'''
                    Write 1 detailed paragraph about what are the healing constituents of {herb_name_scientific} and explain why.
                    Include the following constituents: {names_prompt}.
                    Pack as much information in as few words as possible.
                    Don't write fluff, only proven data.
                    Don't allucinate.
                    Don't write the character ";".
                    Write the paragraph in 5 sentences.
                    Start the reply with the following words: The most important healing constituents of {herb_name_scientific} are .
                '''
                print(prompt)
                reply = llm_reply(prompt, model)
                lines = []
                for line in reply.split('\n'):
                    line = line.strip()
                    if line == '': continue
                    if ':' in line: continue
                    lines.append(line)
                if len(lines) == 1:
                    data[key] = lines[0]
                    json_write(json_filepath, data)

            # ;preparations
            gen_ai_data(
                json_filepath,
                data=data, 
                key='preparations', 
                prompt = f'''
                    Write a list of the most common herbal preparations you make with {herb_name_scientific}.
                    Also, give a confidence score from 1 to 10 for each preparation, indicating how sure you are about that preparation.
                    Write only 1 preparation for each list item.
                    Never use the word "and".
                    Write only the names of the preparation, don't add descriptions.
                    Write the as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in JSON format using the structure in the following example:
                    [
                        {{"name": "<insert name of preparation 1 here>", "confidence_score": "10"}},
                        {{"name": "<insert name of preparation 2 here>", "confidence_score": "5"}},
                        {{"name": "<insert name of preparation 3 here>", "confidence_score": "7"}}
                    ]
                    Reply only with the JSON, don't add additional content.
                ''',
                herb_i=herb_i
            )

            key = 'preparations_description'
            if key not in data: data[key] = ''
            # data[key] = ''
            if data[key] == '':
                names = [obj['name'].lower().strip() for obj in data['preparations']]
                names_prompt = ', '.join(names[:5])
                prompt = f'''
                    Write 1 detailed paragraph about what are the herbal preparations of {herb_name_scientific} and explain why.
                    Include the following preparations: {names_prompt}.
                    Pack as much information in as few words as possible.
                    Don't write fluff, only proven data.
                    Don't allucinate.
                    Don't write the character ";".
                    Write the paragraph in 5 sentences.
                    Start the reply with the following words: The main herbal preparations of {herb_name_scientific} are .
                '''
                print(prompt)
                reply = llm_reply(prompt, model)
                lines = []
                for line in reply.split('\n'):
                    line = line.strip()
                    if line == '': continue
                    if ':' in line: continue
                    lines.append(line)
                if len(lines) == 1:
                    data[key] = lines[0]
                    json_write(json_filepath, data)

            # ;side_effects
            gen_ai_data(
                json_filepath,
                data=data, 
                key='side_effects', 
                prompt = f'''
                    Write a list of 10 possible side effects of impropertly using the plant {herb_name_scientific} medicinally.
                    Also, give a confidence score from 1 to 10 for each side effect, indicating how sure you are about that side effect.
                    Write only the names of the side effects, don't add descriptions.
                    Start each list item with a third-person singular actionable verb.
                    Write only 1 side effect for each list item.
                    Never use the word "and".
                    Write only the names of the side effect, don't add descriptions.
                    Write the as few words as possible.
                    Don't write fluff, only proven data.
                    Don't allucinate.
                    Reply in JSON format using the following structure:
                    [
                        {{"name": "<insert name of side effect 1 here>", "confidence_score": "10"}},
                        {{"name": "<insert name of side effect 2 here>", "confidence_score": "5"}},
                        {{"name": "<insert name of side effect 3 here>", "confidence_score": "7"}}
                    ]
                    Reply only with the JSON, don't add additional content.
                ''',
                herb_i=herb_i
            )

            key = 'side_effects_description'
            if key not in data: data[key] = ''
            # data[key] = ''
            if data[key] == '':
                names = [obj['name'].lower().strip() for obj in data['side_effects']]
                names_prompt = ', '.join(names[:5])
                prompt = f'''
                    Write 1 detailed paragraph about what are the possible side effects of using {herb_name_scientific} improperly and explain why.
                    Include the following side effects: {names_prompt}.
                    Pack as much information in as few words as possible.
                    Don't write fluff, only proven data.
                    Don't allucinate.
                    Don't write the character ";".
                    Write the paragraph in 5 sentences.
                    Start the reply with the following words: The possible side effect of using {herb_name_scientific} are .
                '''
                print(prompt)
                reply = llm_reply(prompt, model)
                lines = []
                for line in reply.split('\n'):
                    line = line.strip()
                    if line == '': continue
                    if ':' in line: continue
                    lines.append(line)
                if len(lines) == 1:
                    data[key] = lines[0]
                    json_write(json_filepath, data)

        # intro
        key = 'intro'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write a short 4-sentence paragraph about the plant {herb_name_scientific}.
                Include the following:
                - What is this plant (give definition)
                - What are the health benefits of this plant
                - What are the bioactive constituents of this plant
                - What are the most common herbal preparations made with of this plant
            '''
            print(prompt)
            reply = llm_reply(prompt, model).strip()
            if reply != '':
                data[key] = reply
                json_write(json_filepath, data)

        # tmp sections
        sections = [
            {'key': 'taxonomy', 'style': 'p', 'level': 2, 'item': 'classification', 'same': []},
            {'key': 'uses', 'style': 'p', 'level': 2, 'item': 'medicinal uses', 'same': []},
            {'key': 'benefits', 'style': 'p', 'level': 2, 'item': 'health benefits', 'same': []},
            {'key': 'properties', 'style': 'p', 'level': 2, 'item': 'therapeutic properties', 'same': []},
            {'key': 'constituents', 'style': 'p', 'level': 2, 'item': 'active constituents', 'same': []},
            {'key': 'parts', 'style': 'p', 'level': 2, 'item': 'medicinal parts', 'same': []},
            {'key': 'preparations', 'style': 'p', 'level': 2, 'item': 'herbal preparations', 'same': []},
            {'key': 'side_effects', 'style': 'p', 'level': 2, 'item': 'side effects', 'same': []},
        ]

        for section in sections:
            key = section['key']
            style = section['style']
            level = section['level']
            item = section['item']
            if key not in data: data[key] = ''
            # data[key] = ''
            if data[key] == '' or data == []:
                ai_paragraph_gen(
                    key = key, 
                    filepath = json_filepath, 
                    data = data, 
                    obj = data, 
                    prompt = f'''
                        Write a short 5-sentence paragraph regarding the following aspect of the plant {herb_name_scientific}: {item}.
                        If you know the answer, start the answer with the following words: {herb_name_scientific} .
                        If you don't know the answer or can't answer, reply only with the words: I can't answer.
                    ''',
                    print_prompt = True,
                    regen = True,
        )
        ##############################################################
        # ;html
        ##############################################################
        article_html = ''
        article_html += f'<h1 class="">{data["title"]}</h1>\n'
        article_html += f'{util.text_format_1N1_html(data["intro"])}\n'

        '''

        article_html += f'<h2>What is {data["herb_name_scientific"]}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["what_description"])}\n'

        article_html += f'<h2>What ailments can you heal with this herb?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["ailments_description"])}\n'

        article_html += f'<h2>What are the therapeutic properties this herb?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["properties_description"])}\n'

        article_html += f'<h2>What are the medicinal constituents this herb?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["constituents_description"])}\n'

        article_html += f'<h2>What are the main herbal preparations this herb?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["preparations_description"])}\n'

        article_html += f'<h2>What are the possible side effects of using this herb improperly?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["side_effects_description"])}\n'
        '''

        for section in sections:
            key = section['key']
            style = section['style']
            level = section['level']
            item = section['item']
            content = data[key]
            if level == 2:
                article_html += f'<h2>{item}</h2>\n'
                article_html += f'{content}\n'
            elif level == 3: 
                article_html += f'<h3>{item}</h3>\n'
                article_html += f'{content}\n'
            else:
                article_html += f'<p>{item}</p>\n'
                article_html += f'{content}\n'

        breadcrumbs_html_filepath = f'{url}.html'
        breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
        meta_html = gen_meta(article_html, data["lastmod"])
        article_html = components.table_of_contents(article_html)
        head_html = head_html_generate(data['title'], '/style.css')

        social_html = html_article_social()
        sidebar_html = html_article_sidebar('', social_html)

        main_html = html_article_main(meta_html, article_html, '')
        layout_html = html_article_layout(main_html, sidebar_html)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                {breadcrumbs_html}
                {layout_html}
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)
        print(f'\n')
        print(html_filepath)
        # quit()


def get_category_action():
    popular_herbs = get_popular_herbs_from_teas_articles()
    categories = []
    # for herb_i, herb in enumerate(plants_wcvp[:HERBS_TO_GEN_NUM]):
    for herb_i, herb in enumerate(popular_herbs[:]):
        print(f'{herb_i} - {herb}')
        # herb_name_scientific = herb['scientfiicname']
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        url = f'herbs/{herb_slug}'
        title = herb_name_scientific
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/herbs'): os.mkdir(f'{website_folderpath}/herbs')
        # if os.path.exists(json_filepath): os.remove(json_filepath)
        # continue
        data = json_read(json_filepath, create=True)
        try: category_name_todo = data['category_action']
        except: continue
        found = False
        for category in categories:
            category_name_done = category['name']
            if category_name_todo == category_name_done:
                category['herbs'].append(herb_name_scientific)
                found = True
                break
        if not found:
            categories.append({
                'name': category_name_todo,
                'herbs': [herb_name_scientific]
            })
    return categories

def categories_herbs():
    categories = []
    for herb_i, herb in enumerate(plants_wcvp[:]):
        print(f'{herb_i} - {herb}')
        herb_name_scientific = herb['scientfiicname']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        url = f'herbs/{herb_slug}'
        title = herb_name_scientific
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/herbs'): os.mkdir(f'{website_folderpath}/herbs')
        # if os.path.exists(json_filepath): os.remove(json_filepath)
        # continue
        data = json_read(json_filepath, create=True)
        try: category_name_todo = data['category_action']
        except: continue
        found = False
        for category in categories:
            category_name_done = category['name']
            if category_name_todo == category_name_done:
                category['herbs'].append(herb_name_scientific)
                found = True
                break
        if not found:
            categories.append({
                'name': category_name_todo,
                'herbs': [herb_name_scientific]
            })
    sections_html = ''
    for category in categories:
        herbs_blocks = ''
        for herb in category['herbs']:
            herbs_blocks += f'{herb}'
        section = f'''
            <section>
                <div class="container-xl">
                    <div class="grid-4">
                        <h2>{category['name']}</h2>
                        <a href="">{herbs_blocks}</a>
                    </div>
                </div>
            </section>
        '''
        sections_html += section
    html_filepath = f'{website_folderpath}/herbs.html'
    breadcrumbs_html_filepath = f'herbs.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate('herbs', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <main>
                {sections_html}
            </main>
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def p_herbs_popular():
    popular_herbs = get_popular_herbs_from_teas_articles()
    popular_herbs_formatted = []
    for herb_i, herb in enumerate(popular_herbs):
        print(f'{herb_i} - {herb}')
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        url = f'herbs/popular/{herb_slug}'
        title = herb_name_scientific
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/herbs'): os.mkdir(f'{website_folderpath}/herbs')
        if not os.path.exists(f'{website_folderpath}/herbs/popular'): os.mkdir(f'{website_folderpath}/herbs/popular')
        data = json_read(json_filepath, create=True)
        popular_herbs_formatted.append({
            'herb_name_scientific': herb_name_scientific,
            'herb_slug': herb_slug,
            'herb_url': f'/{url}.html',
        })
    # split data in pages
    page_i = 0
    herb_i = 0
    herb_num_x_page = 20
    pages = []
    curr_page = []
    for herb in popular_herbs_formatted:
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb['herb_slug']
        herb_url = herb['herb_url']
        print(herb_name_scientific, herb_slug, herb_url)
        curr_page.append([herb_slug, herb_name_scientific])
        herb_i += 1
        if herb_i > herb_num_x_page-1:
            page_i += 1
            herb_i = 0
            pages.append(curr_page)
            curr_page = []
    pages.append(curr_page)
    # gen pages html
    page_i = 1
    for page in pages:
        # intro html
        html_title = f'What Are The Most Popular Medicinal Herbs?'
        html_intro = f'The following list shows the best medicinal herbs to improve health and to heal ailments. Click on any of the following herbs to discover its medicinal aspects and much more.'
        # cards html
        cards_html = ''
        for herb in page:
            herb_slug = herb[0]
            herb_name_scientific = herb[1]
            src = f'/images/ailments/herbs/{herb_slug}.jpg'
            alt = f'{herb_name_scientific}'.lower()
            filepath_in = f'{vault}/terrawhisper/images/realistic/herbs/1x1/{herb_slug}.jpg'
            filepath_out = f'{website_folderpath}/images/herbs/{herb_slug}.jpg'
            # if not os.path.exists(filepath_out):
            if True:
                if os.path.exists(filepath_in):
                    image = Image.open(filepath_in)
                    image = img_resize(image)
                    image.save(filepath_out)
            card_html = f'''
                <div>
                    <a class="inline-block mb-48 no-underline" href="/herbs/{herb_slug}.html">
                        <img src="{src}">
                        <h2 class="mt-16 text-20 text-black">{herb_name_scientific.capitalize()}</h2>
                    </a>
                </div>
            '''
            cards_html += card_html
        # pagination html
        pagination_html = ''
        if page_i == 1:
            pagination_html += f'<a class="inline-block no-underline text-black" href="#">&lt;</a>'
        elif page_i == 2:
            pagination_html += f'<a class="inline-block no-underline text-black" href="/herbs.html">&lt;</a>'
        else:
            pagination_html += f'<a class="inline-block no-underline text-black" href="/herbs/page-{page_i-1}.html">&lt;</a>'
        for j in range(len(pages)):
            if j + 1 == page_i:
                pagination_html += f'''
                    <a class="inline-block no-underline bg-black text-white px-8 py-4" href="#">{j+1}</a>
                '''
            elif j + 1 == 1:
                pagination_html += f'''
                    <a class="inline-block no-underline text-black" href="/herbs.html">{j+1}</a>
                '''
            else:
                pagination_html += f'''
                    <a class="inline-block no-underline text-black" href="/herbs/page-{j+1}.html">{j+1}</a>
                '''
        if page_i == len(pages):
            pagination_html += f'<a class="inline-block no-underline text-black" href="#">&gt;</a>'
        else:
            pagination_html += f'<a class="inline-block no-underline text-black" href="/herbs/page-{page_i+1}.html">&gt;</a>'
        # html
        if page_i == 1:
            html_filepath = f'{website_folderpath}/herbs/popular.html'
            breadcrumbs_html_filepath = f'herbs/popular.html'
            breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
            html = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta name="author" content="{g.AUTHOR_NAME}">
                    <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                    <link rel="stylesheet" href="/style.css">
                    <title>{html_title}</title>
                    {g.GOOGLE_TAG}
                </head>
                <body>
                    {header_html}
                    {breadcrumbs_html}
                    <section class="pb-48">
                        <div class="container-md">
                            <h2 class="text-center">{html_title}</h2>
                            <p class="text-center">{html_intro}</p>
                        </div>
                    </section>
                    <section class="blog-grid pb-48">
                        <div class="container-xl">
                            <div class="grid grid-4 gap-24">
                                {cards_html}
                            </div>
                        </div>
                    </section>
                    <section class="pb-96">
                        <div class="container-xl text-center flex justify-center items-center gap-8">
                            {pagination_html}
                        </div>
                    </section>
                    {footer_html}
                </body>
                </html>
            '''
            util.file_write(html_filepath, html)
        else:
            html_filepath = f'{website_folderpath}/herbs/popular/page-{page_i}.html'
            breadcrumbs_html_filepath = f'herbs/popular/page-{page_i}.html'
            breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
            html = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta name="author" content="{g.AUTHOR_NAME}">
                    <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                    <link rel="stylesheet" href="/style.css">
                    <title>{html_title}</title>
                    {g.GOOGLE_TAG}
                </head>
                <body>
                    {header_html}
                    {breadcrumbs_html}
                    <section>
                        <div class="container-md">
                            <h2 class="text-center">{html_title}</h2>
                            <p class="text-center">{html_intro}</p>
                        </div>
                    </section>
                    <section class="blog-grid pb-48">
                        <div class="container-xl">
                            <div class="grid grid-4 gap-24">
                                {cards_html}
                            </div>
                        </div>
                    </section>
                    <section class="pb-96">
                        <div class="container-xl text-center flex justify-center items-center gap-8">
                            {pagination_html}
                        </div>
                    </section>
                    {footer_html}
                </body>
                </html>
            '''
            util.file_write(html_filepath, html)
        page_i += 1

def p_herbs_actions():
    category_action = get_category_action()
    cards_html = ''
    for obj_i, obj in enumerate(category_action[:]):
        print(f'{obj_i} - {obj}')
        name = obj['name']
        slug = name.strip().lower().replace(' ', '-')
        src = ''
        card_html = f'''
            <div>
                <a class="inline-block mb-48 no-underline" href="/herbs/actions/{slug}.html">
                    <img src="{src}">
                    <h2 class="mt-16 text-20 text-black">{name.capitalize()}</h2>
                </a>
            </div>
        '''
        cards_html += card_html
    print(cards_html)

    section_category_action = f'''
        <section class="mt-48">
            <div class="container-xl">
                <div class="mob-flex justify-between items-center">
                    <div>
                        <h2 class="mt-0">Actions</h2>
                    </div>
                </div>
                <div class="grid grid-4 gap-16">
                    {cards_html}
                </div>
            </div>
        </section>
    '''

    url_slug = 'herbs/actions'
    url_name = url_slug.strip().lower().replace('-', ' ')
    html_filepath = f'{website_folderpath}/{url_slug}.html'
    breadcrumbs_html_filepath = f'{url_slug}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate('{url_name}', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <main>
                {section_category_action}
            </main>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def p_herbs_action_var(category_action_name):
    popular_herbs = get_popular_herbs_from_teas_articles()
    popular_herbs_formatted = []
    for herb_i, herb in enumerate(popular_herbs):
        print(f'{herb_i} - {herb}')
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        herb_url = f'herbs/{herb_slug}'
        title = herb_name_scientific

        json_filepath = f'database/json/{herb_url}.json'
        html_filepath = f'{website_folderpath}/{herb_url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/herbs'): os.mkdir(f'{website_folderpath}/herbs')
        if not os.path.exists(f'{website_folderpath}/herbs/popular'): os.mkdir(f'{website_folderpath}/herbs/popular')
        json_data = json_read(json_filepath)

        category_action_slug = category_action_name.lower().strip().replace(' ', '-')
        if json_data['category_action'].lower().strip().replace(' ', '-') != category_action_slug: continue

        popular_herbs_formatted.append({
            'herb_name_scientific': herb_name_scientific,
            'herb_slug': herb_slug,
            'herb_url': f'/{herb_url}.html',
        })
    # split data in pages
    page_i = 0
    herb_i = 0
    herb_num_x_page = 20
    pages = []
    curr_page = []
    for herb in popular_herbs_formatted:
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb['herb_slug']
        herb_url = herb['herb_url']
        print(herb_name_scientific, herb_slug, herb_url)
        curr_page.append([herb_slug, herb_name_scientific])
        herb_i += 1
        if herb_i > herb_num_x_page-1:
            page_i += 1
            herb_i = 0
            pages.append(curr_page)
            curr_page = []
    pages.append(curr_page)
    # gen pages html
    page_i = 1
    for page in pages:
        # intro html
        html_title = f'What are the best {category_action_name} herbs?'
        html_intro = f''
        # cards html
        cards_html = ''
        for herb in page:
            herb_slug = herb[0]
            herb_name_scientific = herb[1]
            src = f'/images/ailments/herbs/{herb_slug}.jpg'
            alt = f'{herb_name_scientific}'.lower()
            filepath_in = f'{vault}/terrawhisper/images/realistic/herbs/1x1/{herb_slug}.jpg'
            filepath_out = f'{website_folderpath}/images/herbs/{herb_slug}.jpg'
            # if not os.path.exists(filepath_out):
            if True:
                if os.path.exists(filepath_in):
                    image = Image.open(filepath_in)
                    image = img_resize(image)
                    image.save(filepath_out)
            card_html = f'''
                <div>
                    <a class="inline-block mb-48 no-underline" href="/herbs/{herb_slug}.html">
                        <img src="{src}">
                        <h2 class="mt-16 text-20 text-black">{herb_name_scientific.capitalize()}</h2>
                    </a>
                </div>
            '''
            cards_html += card_html
        # pagination html
        pagination_html = ''
        if page_i == 1:
            pagination_html += f'<a class="inline-block no-underline text-black" href="#">&lt;</a>'
        elif page_i == 2:
            pagination_html += f'<a class="inline-block no-underline text-black" href="/herbs.html">&lt;</a>'
        else:
            pagination_html += f'<a class="inline-block no-underline text-black" href="/herbs/page-{page_i-1}.html">&lt;</a>'
        for j in range(len(pages)):
            if j + 1 == page_i:
                pagination_html += f'''
                    <a class="inline-block no-underline bg-black text-white px-8 py-4" href="#">{j+1}</a>
                '''
            elif j + 1 == 1:
                pagination_html += f'''
                    <a class="inline-block no-underline text-black" href="/herbs.html">{j+1}</a>
                '''
            else:
                pagination_html += f'''
                    <a class="inline-block no-underline text-black" href="/herbs/page-{j+1}.html">{j+1}</a>
                '''
        if page_i == len(pages):
            pagination_html += f'<a class="inline-block no-underline text-black" href="#">&gt;</a>'
        else:
            pagination_html += f'<a class="inline-block no-underline text-black" href="/herbs/page-{page_i+1}.html">&gt;</a>'
        # html
        if page_i == 1:
            html_filepath = f'{website_folderpath}/herbs/actions/{category_action_slug}.html'
            breadcrumbs_html_filepath = f'herbs/actions/{category_action_slug}.html'
            breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
            html = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta name="author" content="{g.AUTHOR_NAME}">
                    <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                    <link rel="stylesheet" href="/style.css">
                    <title>{html_title}</title>
                    {g.GOOGLE_TAG}
                </head>
                <body>
                    {header_html}
                    {breadcrumbs_html}
                    <section class="pb-48">
                        <div class="container-md">
                            <h2 class="text-center">{html_title}</h2>
                            <p class="text-center">{html_intro}</p>
                        </div>
                    </section>
                    <section class="blog-grid pb-48">
                        <div class="container-xl">
                            <div class="grid grid-4 gap-24">
                                {cards_html}
                            </div>
                        </div>
                    </section>
                    <section class="pb-96">
                        <div class="container-xl text-center flex justify-center items-center gap-8">
                            {pagination_html}
                        </div>
                    </section>
                    {footer_html}
                </body>
                </html>
            '''
            util.file_write(html_filepath, html)
        else:
            html_filepath = f'{website_folderpath}/herbs/actions/{category_action_slug}/page-{page_i}.html'
            breadcrumbs_html_filepath = f'herbs/actions/{category_action_slug}/page-{page_i}.html'
            breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
            html = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta name="author" content="{g.AUTHOR_NAME}">
                    <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                    <link rel="stylesheet" href="/style.css">
                    <title>{html_title}</title>
                    {g.GOOGLE_TAG}
                </head>
                <body>
                    {header_html}
                    {breadcrumbs_html}
                    <section>
                        <div class="container-md">
                            <h2 class="text-center">{html_title}</h2>
                            <p class="text-center">{html_intro}</p>
                        </div>
                    </section>
                    <section class="blog-grid pb-48">
                        <div class="container-xl">
                            <div class="grid grid-4 gap-24">
                                {cards_html}
                            </div>
                        </div>
                    </section>
                    <section class="pb-96">
                        <div class="container-xl text-center flex justify-center items-center gap-8">
                            {pagination_html}
                        </div>
                    </section>
                    {footer_html}
                </body>
                </html>
            '''
            util.file_write(html_filepath, html)
        page_i += 1


def herb_to_html_card(herb_data):
    herb_name_scientific = herb_data['herb_name_scientific']
    herb_slug = herb_data['herb_slug']
    herb_url = f'/herbs/{herb_slug}.html'

    src = f'/images/ailments/herbs/{herb_slug}.jpg'
    alt = f'{herb_name_scientific}'.lower()
    filepath_in = f'{vault}/terrawhisper/images/realistic/herbs/1x1/{herb_slug}.jpg'
    filepath_out = f'{website_folderpath}/images/herbs/{herb_slug}.jpg'

    # if not os.path.exists(filepath_out):
    if True:
        if os.path.exists(filepath_in):
            image = Image.open(filepath_in)
            image = img_resize(image)
            image.save(filepath_out)

    card_html = f'''
        <div>
            <a class="inline-block mb-48 no-underline" href="/herbs/{herb_slug}.html">
                <img src="{src}">
                <h2 class="mt-16 text-20 text-black">{herb_name_scientific.capitalize()}</h2>
            </a>
        </div>
    '''

    return card_html

def p_herbs():
    popular_herbs = get_popular_herbs_from_teas_articles()
    cards_html = ''
    for herb_i, herb in enumerate(popular_herbs[:4]):
        print()
        print(f'{herb_i} - {herb}')
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        title = herb_name_scientific
        url = f'herbs/{herb_slug}'
        json_filepath = f'database/json/{url}.json'
        print(f'    >> JSON: {json_filepath}')
        herb_data = json_read(json_filepath)
        card_html = herb_to_html_card(herb_data)
        cards_html += card_html
    print(cards_html)

    section_popular = f'''
        <section class="mt-48">
            <div class="container-xl">
                <div class="mob-flex justify-between items-center">
                    <div>
                        <h2 class="mt-0">Popular</h2>
                    </div>
                    <div>
                        <a href="/herbs/popular.html">See All Popular</a>
                    </div>
                </div>
                <div class="grid grid-4 gap-16">
                    {cards_html}
                </div>
            </div>
        </section>
    '''

    category_action = get_category_action()
    cards_html = ''
    for obj_i, obj in enumerate(category_action[:4]):
        print()
        print(f'{obj_i} - {obj}')
        action_name = obj['name'].split('/')[0]
        action_slug = action_name.lower().strip().replace(' ', '-')
        src = f'/images/herbs-actions/{action_slug}.jpg'
        alt = action_name
        card_html = f'''
            <div>
                <a class="inline-block mb-48 no-underline" href="/herbs/actions/{action_slug}.html">
                    <img src="{src}" alt="{alt}">
                    <h2 class="mt-16 text-20 text-black">{action_name.capitalize()}</h2>
                </a>
            </div>
        '''
        cards_html += card_html
    print(cards_html)

    section_category_action = f'''
        <section class="mt-48">
            <div class="container-xl">
                <div class="mob-flex justify-between items-center">
                    <div>
                        <h2 class="mt-0">Actions</h2>
                    </div>
                    <div>
                        <a href="/herbs/actions.html">See All Actions</a>
                    </div>
                </div>
                <div class="grid grid-4 gap-16">
                    {cards_html}
                </div>
            </div>
        </section>
    '''

    section_taxonomy = f'''
        <section class="mt-48">
            <div class="container-xl">
                <h2 class="mt-0">Taxonomy</h2>
                <p>If you want to find plants by Taxonomy (Linnaean Classification System),<a href="/herbs/taxonomy.html"> Browse The Taxonomy Page</a></p>
            </div>
        </section>
    '''

    url_slug = 'herbs'
    url_name = url_slug.strip().lower().replace('-', ' ')
    html_filepath = f'{website_folderpath}/{url_slug}.html'
    breadcrumbs_html_filepath = f'{url_slug}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate(f'{url_name}', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <main>
                {section_popular}
                {section_category_action}
                {section_taxonomy}
            </main>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def page_home():
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    random.shuffle(ailments)
    teas_blocks_data = []
    for ailment_i, ailment in enumerate(ailments[:]):
        preparation_slug = 'teas'
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        data = json_read(json_filepath)
        image_url = data['intro_image_src']
        title = data['title'].title()
        intro_desc = ' '.join(data['intro_desc'].split(' ')[:32])
        teas_blocks_data.append({
            'href': f'/{url}.html',
            'url': f'{image_url}',
            'title': f'{title}',
            'intro_desc': f'{intro_desc}',
        })
    tinctures_blocks_data = []
    for ailment_i, ailment in enumerate(ailments[:]):
        preparation_slug = 'tinctures'
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        data = json_read(json_filepath)
        image_url = data['intro_image_src']
        title = data['title'].title()
        intro_desc = ' '.join(data['intro_desc'].split(' ')[:32])
        tinctures_blocks_data.append({
            'href': f'/{url}.html',
            'url': f'{image_url}',
            'title': f'{title}',
            'intro_desc': f'{intro_desc}',
        })
    creams_blocks_data = []
    for ailment_i, ailment in enumerate(ailments[:]):
        preparation_slug = 'creams'
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        data = json_read(json_filepath)
        image_url = data['intro_image_src']
        title = data['title'].title()
        creams_blocks_data.append({
            'href': f'/{url}.html',
            'url': f'{image_url}',
            'title': f'{title}',
        })
    essential_oils_blocks_data = []
    for ailment_i, ailment in enumerate(ailments[:]):
        preparation_slug = 'essential-oils'
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        data = json_read(json_filepath)
        image_url = data['intro_image_src']
        title = data['title'].title()
        essential_oils_blocks_data.append({
            'href': f'/{url}.html',
            'url': f'{image_url}',
            'title': f'{title}',
        })

    herbs = get_popular_herbs_from_teas_articles()
    cards_html = ''
    for herb_i, herb in enumerate(herbs[:4]):
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        title = herb_name_scientific
        url = f'herbs/{herb_slug}'
        json_filepath = f'database/json/{url}.json'
        herb_data = json_read(json_filepath)
        card_html = herb_to_html_card(herb_data)
        cards_html += card_html
    section_herbs = f'''
        <section class="mt-96">
            <div class="container-xl">
                <div class="mob-flex justify-between items-center">
                    <div>
                        <h2 class="mt-0">Herbs</h2>
                    </div>
                    <div>
                        <a href="/herbs.html">See All Herbs</a>
                    </div>
                </div>
                <div class="grid grid-4 gap-16">
                    {cards_html}
                </div>
            </div>
        </section>
    '''


    section_1 = f'''
        <section class="container-xl grid-container mb-48">
            <a class="no-underline bg-center bg-cover card-wide card-tall flex items-end pl-16 pb-16 pr-48" href="{teas_blocks_data[0]['href']}" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url({teas_blocks_data[0]['url']})">
                <div>
                    <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">
                        PREPARATIONS
                    </span>
                    <h2 class="h2-plain text-white text-24 mb-16">
                        {teas_blocks_data[0]['title']}
                    </h2>
                    <p class="text-white">
                        Terrawhisper - 2024/10/14
                    </p>
                </div>
            </a>
            <a class="no-underline bg-center bg-cover card-wide flex items-end pl-16 pb-16 pr-48" href="{tinctures_blocks_data[1]['href']}" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url({tinctures_blocks_data[1]['url']})">
                <div>
                    <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">
                        PREPARATIONS
                    </span>
                    <h2 class="h2-plain text-white text-24 mb-16">
                        {tinctures_blocks_data[1]['title']}
                    </h2>
                </div>
            </a>
            <a class="no-underline bg-center bg-cover flex items-end pl-16 pb-16 pr-48" href="{creams_blocks_data[2]['href']}" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url({creams_blocks_data[2]['url']})">
                <div>
                    <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">
                        PREPARATIONS
                    </span>
                    <h2 class="h2-plain text-white text-16 mb-16">
                        {creams_blocks_data[2]['title']}
                    </h2>
                </div>
            </a>
            <a class="no-underline bg-center bg-cover flex items-end pl-16 pb-16 pr-48" href="{essential_oils_blocks_data[3]['href']}" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url({essential_oils_blocks_data[3]['url']})">
                <div>
                    <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">
                        PREPARATIONS
                    </span>
                    <h2 class="h2-plain text-white text-16 mb-16">
                        {essential_oils_blocks_data[4]['title']}
                    </h2>
                </div>
            </a>
        </section>
    '''

    cards_html = ''
    for i in range(4):
        cards_html += f'''
            <a class="article-card no-underline text-black" href="{teas_blocks_data[i+5]['href']}">
                <div class="flex gap-16">
                    <div class="flex-2">
                        <img class="object-cover" height="80" src="{teas_blocks_data[i+5]['url']}">
                    </div>
                    <div class="flex-5">
                        <h3 class="h3-plain text-14 mb-8">
                            {teas_blocks_data[i+5]['title']}
                        </h3>
                        <p class="text-12">
                            2024/10/14
                        </p>
                    </div>
                </div>
            </a>
        '''

    
    social_html = html_article_social()
    section_2 = f'''
        <section>
            <div class="container-xl flex mob-flex-col mb-48 gap-48">
                <div class="flex-2">
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="h2-plain text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Teas</h2>
                    </div>
                    <div class="flex mob-flex-col gap-48">
                        <div class="flex-1">
                            <a class="article-card no-underline text-black" href="{teas_blocks_data[4]['href']}">
                                <div class="relative mb-16">
                                    <img class="object-cover" height="240" src="{teas_blocks_data[4]['url']}">
                                </div>
                                <h3 class="h3-plain text-20 font-normal mb-8">
                                    {teas_blocks_data[4]['title']}
                                </h3>
                                <p class="text-12 mb-16">
                                    <span class="font-bold text-black">Terrawhisper</span> - 2024/10/12
                                </p>
                                <p class="text-14 mb-0">
                                    {teas_blocks_data[4]['intro_desc']}
                                </p>
                            </a>
                        </div>
                        <div class="flex-1 flex flex-col gap-24">
                            {cards_html}
                        </div>
                    </div>
                </div>
                <div class="flex-1">
                    {social_html}
                </div>
            </div>
        </section>
    '''

    section_3 = f'''
        <section>
            <div class="container-xl flex mob-flex-col mb-48 gap-48">
                <div class="flex-2">
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="h2-plain text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Tinctures</h2>
                    </div>
                    <div class="flex mob-flex-col gap-48">
                        <div class="flex-1 flex flex-col gap-24">
                            <div class="">
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[4]['href']}">
                                    <div class="relative mb-16">
                                        <img class="object-cover" height="240" src="{tinctures_blocks_data[4]['url']}">
                                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">tincture</p>
                                    </div>
                                    <h3 class="h3-plain text-20 font-normal mb-8">
                                        {tinctures_blocks_data[4]['title']}
                                    </h3>
                                    <p class="text-12 mb-16">
                                        <span class="font-bold text-black">Terrawhisper</span> - 2024/10/12
                                    </p>
                                    <p class="text-14 mb-0">
                                        {tinctures_blocks_data[4]['intro_desc']}
                                    </p>
                                </a>
                            </div>
                            <div class="flex-1 flex flex-col gap-24">
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[5]['href']}">
                                    <div class="flex gap-16">
                                        <div class="flex-2">
                                            <img class="object-cover" height="80" src="{tinctures_blocks_data[5]['url']}">
                                        </div>
                                        <div class="flex-5">
                                            <h3 class="h3-plain text-14 mb-8">
                                                {tinctures_blocks_data[5]['title']}
                                            </h3>
                                            <p class="text-12">2024/08/21</p>
                                        </div>
                                    </div>
                                </a>
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[6]['href']}">
                                    <div class="flex gap-16">
                                        <div class="flex-2">
                                            <img class="object-cover" height="80" src="{tinctures_blocks_data[6]['url']}">
                                        </div>
                                        <div class="flex-5">
                                            <h3 class="h3-plain text-14 mb-8">
                                                {tinctures_blocks_data[6]['title']}
                                            </h3>
                                            <p class="text-12">2024/08/21</p>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>
                        <div class="flex-1 flex flex-col gap-24">
                            <div class="">
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[7]['href']}">
                                    <div class="relative mb-16">
                                        <img class="object-cover" height="240" src="{tinctures_blocks_data[7]['url']}">
                                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">tincture</p>
                                    </div>
                                    <h3 class="h3-plain text-20 font-normal mb-8">
                                        {tinctures_blocks_data[7]['title']}
                                    </h3>
                                    <p class="text-12 mb-16">
                                        <span class="font-bold text-black">Terrawhisper</span> - 2024/10/12
                                    </p>
                                    <p class="text-14 mb-0">
                                        {tinctures_blocks_data[7]['intro_desc']}
                                    </p>
                                </a>
                            </div>
                            <div class="flex-1 flex flex-col gap-24">
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[8]['href']}">
                                    <div class="flex gap-16">
                                        <div class="flex-2">
                                            <img class="object-cover" height="80" src="{tinctures_blocks_data[8]['url']}">
                                        </div>
                                        <div class="flex-5">
                                            <h3 class="h3-plain text-14 mb-8">
                                                {tinctures_blocks_data[8]['title']}
                                            </h3>
                                            <p class="text-12">2024/08/21</p>
                                        </div>
                                    </div>
                                </a>
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[9]['href']}">
                                    <div class="flex gap-16">
                                        <div class="flex-2">
                                            <img class="object-cover" height="80" src="{tinctures_blocks_data[9]['url']}">
                                        </div>
                                        <div class="flex-5">
                                            <h3 class="h3-plain text-14 mb-8">
                                                {tinctures_blocks_data[9]['title']}
                                            </h3>
                                            <p class="text-12">2024/08/21</p>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex-1">
                    <div>
                        <div class="border-0 border-b-4 border-solid border-black mb-24">
                            <h2 class="h2-plain text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">creams</h2>
                        </div>
                        <div class="flex flex-col gap-24">
                            <div class="flex mob-flex-col gap-24">
                                <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{creams_blocks_data[4]['href']}">
                                    <div class="">
                                        <div class="relative mb-16">
                                            <img class="object-cover" height="180" src="{creams_blocks_data[4]['url']}">
                                            <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">creams</p>
                                        </div>
                                        <h3 class="h3-plain text-14 mb-8">
                                            {creams_blocks_data[4]['title']}
                                        </h3>
                                    </div>
                                </a>
                                <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{creams_blocks_data[5]['href']}">
                                    <div class="">
                                        <div class="relative mb-16">
                                            <img class="object-cover" height="180" src="{creams_blocks_data[5]['url']}">
                                            <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">creams</p>
                                        </div>
                                        <h3 class="h3-plain text-14 mb-8">
                                            {creams_blocks_data[5]['title']}
                                        </h3>
                                    </div>
                                </a>
                            </div>
                            <div class="flex mob-flex-col gap-24">
                                <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{creams_blocks_data[6]['href']}">
                                    <div class="">
                                        <div class="relative mb-16">
                                            <img class="object-cover" height="180" src="{creams_blocks_data[6]['url']}">
                                            <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">creams</p>
                                        </div>
                                        <h3 class="h3-plain text-14 mb-8">
                                            {creams_blocks_data[6]['title']}
                                        </h3>
                                    </div>
                                </a>
                                <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{creams_blocks_data[7]['href']}">
                                    <div class="">
                                        <div class="relative mb-16">
                                            <img class="object-cover" height="180" src="{creams_blocks_data[7]['url']}">
                                            <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">creams</p>
                                        </div>
                                        <h3 class="h3-plain text-14 mb-8">
                                            {creams_blocks_data[7]['title']}
                                        </h3>
                                    </div>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    '''

    section_4 = f'''
        <section>
            <div class="container-xl mob-flex mb-48 gap-48">
                <div class="flex-2">
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="h2-plain text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Essential Oils</h2>
                    </div>
                    <div class="flex mob-flex-col gap-24">
                        <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{essential_oils_blocks_data[4]['href']}">
                            <div class="">
                                <div class="relative mb-16">
                                    <img class="object-cover" height="180" src="{essential_oils_blocks_data[4]['url']}">
                                    <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">essential oils</p>
                                </div>
                                <h3 class="h3-plain text-14 mb-8">
                                    {essential_oils_blocks_data[4]['title']}
                                </h3>
                            </div>
                        </a>
                        <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{essential_oils_blocks_data[5]['href']}">
                            <div class="">
                                <div class="relative mb-16">
                                    <img class="object-cover" height="180" src="{essential_oils_blocks_data[5]['url']}">
                                    <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">essential oils</p>
                                </div>
                                <h3 class="h3-plain text-14 mb-8">
                                    {essential_oils_blocks_data[5]['title']}
                                </h3>
                            </div>
                        </a>
                        <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{essential_oils_blocks_data[6]['href']}">
                            <div class="">
                                <div class="relative mb-16">
                                    <img class="object-cover" height="180" src="{essential_oils_blocks_data[6]['url']}">
                                    <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">essential oils</p>
                                </div>
                                <h3 class="h3-plain text-14 mb-8">
                                    {essential_oils_blocks_data[6]['title']}
                                </h3>
                            </div>
                        </a>
                    </div>
                </div>
                <div class="flex-1">
                </div>
            </div>
        </section>
    '''

    html_hero = f'''
        <section class="container-xl grid-2 gap-64 items-center">
            <div>
                <h1>Use Medicinal Plants To Improve Your Health</h1>
                <p>Biggest archive of healing herbs from Terrawhisper to help herbalists cure ailments.</p>
                <a style="display: inline-block; text-decoration: none; background-color: #c2410c; color: #ffffff; padding: 12px 24px;" href="/herbs.html">Browse Herbs</a>
            </div>
            <img src="/images-static/medicinal-plants.jpg" alt="medicinal plants">
        </section>
    '''

    head_html = head_html_generate('improve your health with medicinal plants', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            <main>
                {html_hero}
                {section_herbs}
                {section_1}
                {section_2}
                {section_3}
                {section_4}
            </main>
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    html_filepath = f'{website_folderpath}/index.html'
    with open(html_filepath, 'w') as f: f.write(html)

def page_contacts():
    section_1 = f'''
        <section>
            <div class="container-xl mob-flex gap-64 mt-64">
                <div class="flex-2">
                    <h1>Contact Terrawhisper</h1>
                    <p>Need something? The best way to contact Terrawhisper is to send and email at <u>leen@terrawhisper.com</u></p>
                    <p>In alternative, follow our socials to stay in touch.</p>
                    <p>NOTE: Before contacting (especially if it's for business of non-profit partnerships) please visit Terrawhisper about page to understand if it makes sense asking what you want to ask (aka. if our visions are compatible).</p>
                    <h2 class="mt-48 mb-16">Valid reasons to contact</h2>
                    <p>Here's a list of valid reasons to get in touch:</p>
                    <ul>
                        <li>Business Partnerships: If you are a business who love nature, herbs, and holistic healing, and want to work together on a project, Terrawhisper is here for you. Send an email to the address above and share your ideas. If we are a good fit to each others, Terrawhisper will get back to you ASAP.</li>
                        <li>Request Content Review: Terrawhisper gather information from books, scientific papers, and articles. There's an ongoing effort to be as accurate as possible with the information shared, but no one is perfect. So, if you believe Terrawhisper published a piece of information that is not 100% accurate (or plain wrong), send an email telling us what you believe we should change. Please include the link to the article and a reference to the line to change.</li>
                        <li>Guest Posting: Terrawhisper lack manpower (when it comes to writing articles). If you are good at writing and at sharing information in an easy to understand way, and you believe you could be a positive contribute to Terrawhisper, let us know and we will welcome you with open arm.</li>
                    </ul>
                    <h2 class="mt-48 mb-16">NON Valid reasons to contact</h2>
                    <p>Here's a list of NON valid reasons to get in touch:</p>
                    <ul>
                        <li>Client Work and Personalized Prescriptions: Terrawhisper don't do client work at the time of the writing. If you don't find what you're looking for in the articles on the site, don't send an email describing your specific case/condition to ask for remedies. In the future, Terrawhisper will share more detailed and specialized remedies in the newsletter and in a book about medicinal plants that's in the making (coming soon), but that's as far as it goes. Don't ask to be a client or to get personalized advice.</li>
                    </ul>
                    <div class="mb-64"></div>
                </div>
                <div class="flex-1">
                    {author_block_html}
                    <div class="mb-64"></div>
                </div>
            </div>
        </section>
    '''
    html_filepath = f'{website_folderpath}/contacts.html'
    breadcrumbs_html_filepath = f'contacts.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate('contact terrawhisper', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <main>
                {section_1}
            </main>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def page_products():
    with open('assets/buy-buttons/stripe-test.txt') as f: stripe_button = f.read()
    section_1 = f'''
        <section>
            <div>
                {stripe_button}
            </div>
        </section>
    '''

    html_filepath = f'{website_folderpath}/products.html'
    breadcrumbs_html_filepath = f'products.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate('ebook', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <main>
                {section_1}
            </main>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def page_guides():
    cards = []
    card = f'''
        <a class="article-card no-underline text-black" href="/guides/checklist-dry-herbs.html">
            <div class="">
                <img class="mb-16" src="/images-static/checklist-dry-herbs.jpg" alt="herb drying checklist">
                <h2 class="h2-plain text-18 mb-12">The Ultimate Herb Drying Checklist</h2>
            </div>
        </a>
    '''
    cards.append(card)
    cards = ''.join(cards)

    section_1 = f'''
        <section class="mt-48 mb-48">
            <div class="container-md">
                <div class="grid grid-3 gap-16">
                    {cards}
                </div>
            </div>
        </section>
    '''

    html_filepath = f'{website_folderpath}/guides.html'
    breadcrumbs_html_filepath = f'guides.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate('guides on herbalism and herbal remedies', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <main>
                {section_1}
            </main>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def p_guides_infusion_checklist():
    html_filepath = f'{website_folderpath}/guides/infusion-checklist-download.html'
    breadcrumbs_html_filepath = f'guides/infusion-checklist-download.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate('medicinal infusion checklist - download', '/style.css')
    section_1 = f'''
        <section class="mt-48 mb-48">
            <div class="container-md">
                <h1 class="text-center">Download The Medicinal Infusion Checklist</h1>
                <div class="flex justify-center">
                    <a class="text-center" href="/assets/docs/medicinal-infusion-checklist.jpg" target="_blank">Click Here To Download</a>
                <div>
            </div>
        </section>
    '''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <main>
                {section_1}
            </main>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)


def page_lead_magnet_1():
    with open('assets/newsletter/sign-in-form.txt') as f: sign_in_form_html = f.read()
    section_top_html = f'''
        <section class="bg-black pl-16 pr-16 pt-16 pb-16 mb-24">
            <div class="container-xl">
                <h1 class="text-24 text-white text-center mb-0 pt-0">Here's what you NEED to know about drying herbs: before, during, and after!</h1>
            </div>
        </section>
    '''
    section_center_html = f'''
        <section>
            <div class="container-xl">
                <div class="mob-flex items-center gap-64">
                    <div class="flex-1 mb-24">
                        <img src="/images-static/checklist-dry-herbs.jpg">
                    </div>
                    <div class="flex-1 container-sm">
                        <p class="text-center text-20 helvetica-bold">
                            FREE: HERB DRYING CHECKLIST
                        </p>
                        <p class="text-center text-black text-32 helvetica-bold">
                            If you are thinking about drying herbs, get this checklist FIRST!
                        </p>
                        <p class="text-center">
                            Find out how to easily dry herbs, that don't grow mold, and that keep their medicinal power for a long time (more than 1 year).
                        {sign_in_form_html}
                    </div>
                </div>
            </div>
        </section>
    '''
    html_filepath = f'{website_folderpath}/guides/checklist-dry-herbs.html'
    breadcrumbs_html_filepath = f'guides/checklist-dry-herbs.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate('the ultimate herb drying checklist - opt in', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <div class="mb-48"></div>
            <main>
                {section_top_html}
                {section_center_html}
            </main>
            <div class="mb-48"></div>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)


def page_lead_magnet_1_congratulation():
    section_1 = f'''
        <section class="mt-48 mb-48">
            <div class="container-md">
                <h1>
                    Congratulation
                </h1>
                <p>
                    Check your email!
                </p>
                <p>
                    I just sent you an email to the email address you gave me. In this email, you find the download link for <strong class="text-black">The Ultimate Herb Drying Checklist</strong>. 
                </p>
                <p>
                    Expect to see the email in your inbox in the next 5 minutes (rarely it takes longer).
                </p>
                <p>
                    Enjoy the checklist. And let's start drying some herbs.
                </p>
                <p>
                    Stay grounded,
                </p>
                <p>
                    Leen
                </p>
                <img src="/images-static/dried-herbs.jpg" alt="dried herbs">
            </div>
        </section>
    '''

    html_filepath = f'{website_folderpath}/guides/checklist-dry-herbs-congratulation.html'
    breadcrumbs_html_filepath = f'guides/checklist-dry-herbs-congratulation.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate('the ultimate herb drying checklist - check email', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <main>
                {section_1}
            </main>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def page_lead_magnet_1_download():
    section_1 = f'''
        <section class="mt-48 mb-48">
            <div class="container-md">
                <p class="text-center">Here's Your Download</p>
                <h1 class="text-center">Download Your Herb Drying Checklist</h1>
                <p class="text-center">Click the link below and download your checklist. Dry your herbs effectively, prevent mold growth, and make them preserve their strong medicinal power for a very long time. Enjoy!</p>
                <div class="flex justify-center">
                    <a class="text-center" href="/assets/pdf/the-ultimate-herb-drying-checklist.pdf" target="_blank">Click Here To Download</a>
                <div>
            </div>
        </section>
    '''
    html_filepath = f'{website_folderpath}/guides/checklist-dry-herbs-download.html'
    breadcrumbs_html_filepath = f'guides/checklist-dry-herbs-download.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate('the ultimate herb drying checklist - download', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <main>
                {section_1}
            </main>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def page_systems():
    systems = [
        'cardiovascular',
        'digestive',
        'endocrine',
        'immune',
        'integumentary',
        'lymphatic',
        'musculoskeletal',
        'nervous',
        'reproductive',
        'respiratory',
        'urinary',
    ]
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    data = []
    for ailment in ailments:
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_name = ailment['ailment_name']
        ailment_slug = ailment['ailment_slug']

        found = False
        for obj in data:
            if obj['system_slug'] == system_slug:
                found = True
                obj['ailments_slugs'].append(ailment_slug)
                break
        if not found:
            data.append({
                'system_slug': system_slug,
                'ailments_slugs': [ailment_slug],
            })

    for obj in data:
        system_slug = obj['system_slug']
        system_name = system_slug.capitalize()
        section_1 = f'''
            <section class="mt-64 mb-64">
                <div class="container-xl text-center">
                    <h1>{system_name} System's Ailments</h1>
                    <p class="container-md">Here's a list of ailment related to the {system_slug} system and how to recover faster from them with healing herbs. Just click on any of the links below to read the full article about the corresponding ailment. If you don't find the ailment you are looking for here, maybe it's listed in another body system. If it's not listed in another body system either, visit our contacts page and send us a request to include it.</p>
                </div>
            </section>
        '''
        cards = []
        for ailment_slug in obj["ailments_slugs"]:
            url = f'remedies/{system_slug}-system/{ailment_slug}'
            json_filepath = f'database/json/{url}.json'
            data = json_read(json_filepath)
            src = data['intro_image_src']
            title = data['title']
            lastmod = data['lastmod']
            year, month, day = lastmod.split('-')
            month = int(month)
            if month == 1: month = "GEN"
            if month == 2: month = "FEB"
            if month == 3: month = "MAR"
            if month == 4: month = "APR"
            if month == 5: month = "MAY"
            if month == 6: month = "JUN"
            if month == 7: month = "JUL"
            if month == 8: month = "AUG"
            if month == 9: month = "SEP"
            if month == 10: month = "OCT"
            if month == 11: month = "NOV"
            if month == 12: month = "DEC"
            lastmod_format = f'{month.capitalize()} {day}, {year}'
            card = f'''
                <a class="article-card no-underline text-black" href="/remedies/{system_slug}-system/{ailment_slug}.html">
                    <div class="">
                        <img class="mb-16" src="{src}">
                        <h2 class="h2-plain text-18 mb-12">{title}</h2>
                        <p class="text-14">{lastmod_format}</p>
                    </div>
                </a>
            '''
            cards.append(card)
        cards = ''.join(cards)
        system_slug = obj['system_slug']
        system_name = system_slug.lower().strip().replace('-', ' ')

        html_filepath = f'{website_folderpath}/remedies/{system_slug}-system.html'
        breadcrumbs_html_filepath = f'remedies/{system_slug}-system.html'
        breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
        head_html = head_html_generate(f'{system_name} ailments', '/style.css')
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                {breadcrumbs_html}
                <main>
                    {section_1}
                    <section>
                        <div class="container-xl">
                            <div class="grid-container-2">
                                {cards}
                            </div>
                        </div>
                    </section>
                </main>
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)

def page_remedies():
    section_1 = f'''
        <section class="mt-64 mb-64">
            <div class="container-xl text-center">
                <h1>Herbal Remedies by Body System</h1>
                <p class="container-md">Different herbs improve different body systems. Select the body system you want to improve with herbal medicine by clicking one of the links below. When you click the link, the page about that particular body system opens. In that page, you find a list of common ailments you can relieve by using the natural power of herbalism.</p>
            </div>
        </section>
    '''
    systems = [
        'cardiovascular',
        'digestive',
        'endocrine',
        'immune',
        'integumentary',
        'lymphatic',
        'musculoskeletal',
        'nervous',
        'reproductive',
        'respiratory',
        'urinary',
    ]
    sections = []
    for i, system_name in enumerate(systems):
        system_slug = system_name.strip().lower().replace(' ', '-')
        url = f'remedies'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        data = json_read(json_filepath, create=True)

        key = f'{system_slug}_system_herbs'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            output_plants = []
            for i in range(20):
                prompt = f'''
                    List the best herbs that are good for the {system_name} system.
                    Also, for each herb name give a confidence score from 1 to 10, indicating how sure you are that is good for the {system_name} system.
                    Write only the scientific names (botanical names) of the plants used for the preparation, don't add descriptions or common names.
                    Write the names of the plants using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"herb_name_scientific": "scientific name of herb 1 used for preparation", "confidence_score": "10"}}, 
                        {{"herb_name_scientific": "scientific name of herb 2 used for preparation", "confidence_score": "5"}}, 
                        {{"herb_name_scientific": "scientific name of herb 3 used for preparation", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names_scientific = []
                    for item in json_data:
                        try: line = item['herb_name_scientific']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        print(line)
                        for plant in plants_wcvp:
                            name_scientific = plant['scientfiicname']
                            if name_scientific.lower().strip() in line.lower().strip():
                                if len(name_scientific.split(' ')) > 1:
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    print(name_scientific)
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    names_scientific.append({
                                        "name": name_scientific, 
                                        "score": score,
                                    })
                                    break
                        ## exceptions
                        if line.lower().strip() == 'mentha piperita':
                                names_scientific.append({"name": 'Mentha x piperita', "score": score})
                    for obj in names_scientific:
                        name = obj['name']
                        score = obj['score']
                        found = False
                        for output_plant in output_plants:
                            print(output_plant)
                            print(name, '->', output_plant['herb_name_scientific'])
                            if name in output_plant['herb_name_scientific']: 
                                output_plant['herb_mentions'] += 1
                                output_plant['herb_confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            output_plants.append({
                                'herb_name_scientific': name, 
                                'herb_mentions': 1, 
                                'herb_confidence_score': int(score), 
                            })
                output_plants_final = []
                for output_plant in output_plants:
                    output_plants_final.append({
                        'herb_name_scientific': output_plant['herb_name_scientific'],
                        'herb_mentions': int(output_plant['herb_mentions']),
                        'herb_confidence_score': int(output_plant['herb_confidence_score']),
                        'herb_total_score': int(output_plant['herb_mentions']) * int(output_plant['herb_confidence_score']),
                    })
                output_plants_final = sorted(output_plants_final, key=lambda x: x['herb_confidence_score'], reverse=True)
                print('***********************')
                print('***********************')
                print('***********************')
                for output_plant in output_plants_final:
                    print(output_plant)
                print('***********************')
                print('***********************')
                print('***********************')
                data[key] = output_plants_final[:10]
                json_write(json_filepath, data)

        key = f'{system_slug}_system_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data[f'{system_slug}_system_herbs']][:3]
            prompt = f'''
                Write a very short 5-sentence paragraph about herbal remedies for the {system_name} system. 
                Include the herbs, constituents, benefits, and preparations.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write lists.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                Start with the following words: Herbal remedies such as {herbs_names[0].title()}, {herbs_names[1].title()} and {herbs_names[0].title()} .
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        # ;image
        if 0:
            key = f'{system_slug}_system_image'
            herbs_names = [x['herb_name_scientific'] for x in data[f'{system_slug}_system_herbs'][:3]]
            herbs_names = ' and '.join(herbs_names)
            prompt = f'''
                top view of dry {herbs_names} herb on a wooden table,
                indoor, 
                natural light,
                earth tones,
                neutral colors,
                soft focus,
                warm tones,
                vintage,
                high resolution,
                cinematic
            '''
            negative_prompt = f'''
                text, watermark 
            '''
            prompt = f'''
                dry {herbs_names} herb on a wooden table,
                indoor, 
                natural window light,
                earth tones,
                neutral colors,
                soft focus,
                warm tones,
                vintage,
                high resolution,
                cinematic
            '''
            negative_prompt = f'''
                text, watermark 
            '''
            print(prompt)
            pipe_init()
            image = pipe(
                prompt=prompt, 
                negative_prompt=negative_prompt, 
                width=1024, height=1024, 
                num_inference_steps=30, 
                guidance_scale=7.0
            ).images[0]
            image = img_resize(image, w=768, h=768)
            output_filepath = f'{website_folderpath}/images-static/{system_slug}.jpg'
            html_filepath = f'/images-static/{system_slug}.jpg'
            image.save(output_filepath)
            data[key] = html_filepath
            json_write(json_filepath, data)

        key = f'{system_slug}_system_desc'
        system_desc = f'{data[key]}'
        system_desc = util.text_format_1N1_html(system_desc)
        if i % 2 == 0: reverse = ''
        else: reverse = 'row-reverse'
        section = f'''
            <section class="mb-64">
                <div class="container-xl">
                    <div class="flex mob-flex-col items-center {reverse} remedies_system_cols">
                        <div class="flex-1">
                             <img src="/images-static/{system_slug}.jpg">
                        </div>
                        <div class="flex-1">
                            <h2 class="h2-plain text-32 mb-16">{system_name.capitalize()} System</h2>
                            {system_desc}
                            <p>To learn more about herbal remedies for specific ailments of the {system_slug} system, clicke the button below.</p>
                            <a class="button" href="/remedies/{system_slug}-system.html" class="button">{system_name.capitalize()} System Remedies</a>
                        </div>
                    </div>
                </div>
            </section>
        '''
        sections.append(section)

    sections = ''.join(sections)

    html_filepath = f'{website_folderpath}/remedies.html'
    breadcrumbs_html_filepath = f'remedies.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate('herbal remedies by body systems', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <main>
                {section_1}
                {sections}
            </main>
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def page_about_2():

    with open('content/about.txt') as f: 
        content = f.read()
    
    lines = []
    for line in content.strip().split('\n'):
        line = line.strip()
        if line == '': continue
        tmp_line = line.split('.')
        if len(tmp_line) > 3:
            lines.append(f'{util.text_format_1N1_html(line)}')
        else:
            lines.append(f'<p>{line}</p>')

    content = ''.join(lines)

    section = f'''
        <section class="">
            <div class="container-xl">
                <div class="flex gap-96">
                    <div class="flex-2">
                        <h1>About Terrawhisper</h1>
                        <p>{content}</p>
                    </div>
                    <div class="flex-1">
                        {author_block_html}
                    </div>
                </div>
            </div>
        </section>
    '''
                        # <p>Herbalist & Healer, always hunting for new medicinal plants and scientific researches to expand my knowledge on natural remedies.</p>

    breadcrumbs_html_filepath = f'about.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    head_html = head_html_generate('About Terrawhisper', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            <div class="mt-64"></div>
            <main>
                {section}
            </main>
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''

    page_url = f'about'
    article_filepath_out = f'{website_folderpath}/{page_url}.html'
    util.file_write(article_filepath_out, html)

def page_privacy_policy():
    slug = 'privacy-policy'
    filepath_in = f'templates/{slug}.html'
    filepath_out = f'{website_folderpath}/{slug}.html'
    url = slug
    breadcrumbs_html_filepath = f'{url}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    template = util.file_read(filepath_in)
    template = template.replace('[title]', 'TerraWhisper Privacy Policy')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header_html)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    footer_formatted = f'''
        {footer_html}
    '''
    template = template.replace('[footer]', footer_formatted)
    util.file_write(filepath_out, template)

def page_cookie_policy():
    slug = 'cookie-policy'
    filepath_in = f'templates/{slug}.html'
    filepath_out = f'{website_folderpath}/{slug}.html'
    url = slug
    breadcrumbs_html_filepath = f'{url}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    template = util.file_read(filepath_in)
    template = template.replace('[title]', 'TerraWhisper Cookie Policy')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header_html)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    footer_formatted = f'''
        {footer_html}
    '''
    template = template.replace('[footer]', footer_formatted)
    util.file_write(filepath_out, template)

def p_preparations():
    pass

def p_preparations_teas():
    teas = get_popular_teas()

    lst = []
    for i, item in enumerate(teas):
        print(f'{i} - {item}')
        herb_name_scientific = item['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        url = f'preparations/teas/{herb_slug}'
        title = f'{herb_name_scientific} tea'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        data = json_read(json_filepath, create=True)
        lst.append({
            'herb_name_scientific': herb_name_scientific,
            'herb_slug': herb_slug,
            'url': f'/{url}.html',
        })
    page_i = 0
    herb_i = 0
    herb_num_x_page = 20
    pages = []
    curr_page = []
    for herb in lst:
        herb_slug = herb['herb_slug']
        herb_name_scientific = herb['herb_name_scientific']
        curr_page.append([herb_slug, herb_name_scientific])
        herb_i += 1
        if herb_i > herb_num_x_page-1:
            page_i += 1
            herb_i = 0
            pages.append(curr_page)
            curr_page = []
    pages.append(curr_page)
    page_i = 1
    for page in pages:
        print(page)
        cards_html = ''
        for herb in page:
            herb_slug = herb[0]
            herb_name_scientific = herb[1]
            src = f'/images/preparations/teas/{herb_slug}-herbal-teas.jpg'
            alt = f'{herb_name_scientific} tea'.lower()
            card_html = f'''
                <div>
                    <a class="inline-block mb-48" href="/preparations/teas/{herb_slug}.html">
                        {herb_name_scientific.capitalize()} tea
                    </a>
                </div>
            '''
            cards_html += card_html
        pagination_html = ''
        if page_i == 1:
            pagination_html += f'<a class="inline-block no-underline text-black" href="#">&lt;</a>'
        elif page_i == 2:
            pagination_html += f'<a class="inline-block no-underline text-black" href="/preparations/teas.html">&lt;</a>'
        else:
            pagination_html += f'<a class="inline-block no-underline text-black" href="/preparations/teas/page-{page_i-1}.html">&lt;</a>'
        for j in range(len(pages)):
            if j + 1 == page_i:
                pagination_html += f'''
                    <a class="inline-block no-underline bg-black text-white px-8 py-4" href="#">{j+1}</a>
                '''
            elif j + 1 == 1:
                pagination_html += f'''
                    <a class="inline-block no-underline text-black" href="/preparations/teas.html">{j+1}</a>
                '''
            else:
                pagination_html += f'''
                    <a class="inline-block no-underline text-black" href="/preparations/teas/page-{j+1}.html">{j+1}</a>
                '''
        if page_i == len(pages):
            pagination_html += f'<a class="inline-block no-underline text-black" href="#">&gt;</a>'
        else:
            pagination_html += f'<a class="inline-block no-underline text-black" href="/preparations/teas/page-{page_i+1}.html">&gt;</a>'
        html_title = f'Complete List Of Medicinal Herbs'
        html_intro = f'The following list shows the best medicinal herbs to improve health and to heal ailments. Click on any of the following herbs to discover its medicinal aspects and much more.'
        ## category page (page 1 - canonical)
        if page_i == 1:
            html_filepath = f'{website_folderpath}/preparations/teas.html'
            breadcrumbs_html_filepath = f'preparations/teas.html'
            breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
            html = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta name="author" content="{g.AUTHOR_NAME}">
                    <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                    <link rel="stylesheet" href="/style.css">
                    <title>{html_title}</title>
                    {g.GOOGLE_TAG}
                </head>
                <body>
                    {header_html}
                    {breadcrumbs_html}
                    <section class="pb-48">
                        <div class="container-md">
                            <h2 class="text-center">{html_title}</h2>
                            <p class="text-center">{html_intro}</p>
                        </div>
                    </section>
                    <section class="blog-grid pb-48">
                        <div class="container-xl">
                            <div class="grid grid-4 gap-24">
                                {cards_html}
                            </div>
                        </div>
                    </section>
                    <section class="pb-96">
                        <div class="container-xl text-center flex justify-center items-center gap-8">
                            {pagination_html}
                        </div>
                    </section>
                    {footer_html}
                </body>
                </html>
            '''
            util.file_write(html_filepath, html)
        else:
            html_filepath = f'{website_folderpath}/preparations/teas/page-{page_i}.html'
            breadcrumbs_html_filepath = f'preparations/teas/page-{page_i}.html'
            breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
            html = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta name="author" content="{g.AUTHOR_NAME}">
                    <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                    <link rel="stylesheet" href="/style.css">
                    <title>{html_title}</title>
                    {g.GOOGLE_TAG}
                </head>
                <body>
                    {header_html}
                    {breadcrumbs_html}
                    <section>
                        <div class="container-md">
                            <h2 class="text-center">{html_title}</h2>
                            <p class="text-center">{html_intro}</p>
                        </div>
                    </section>
                    <section class="blog-grid pb-48">
                        <div class="container-xl">
                            <div class="grid grid-4 gap-24">
                                {cards_html}
                            </div>
                        </div>
                    </section>
                    <section class="pb-96">
                        <div class="container-xl text-center flex justify-center items-center gap-8">
                            {pagination_html}
                        </div>
                    </section>
                    {footer_html}
                </body>
                </html>
            '''
            util.file_write(html_filepath, html)
        page_i += 1

def a_preparations_teas_var():
    teas = get_popular_teas()
    for tea_i, tea in enumerate(teas):
        herb_name_scientific = tea['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        url = f'herbs/{herb_slug}'
        json_filepath = f'database/json/{url}.json'
        data = json_read(json_filepath, create=True)
        herb_names_common = [x['name'] for x in data['herb_names_common']]
        herb_name_common = herb_names_common[0].lower().strip()
        herb_name_common_slug = herb_name_common.strip().lower().replace(' ', '-')

        print(f'\n>> {tea_i}/{len(teas)} - teas')
        print(f'\n>>     {tea}')
        url = f'preparations/teas/{herb_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/preparations'): os.mkdir(f'{website_folderpath}/preparations')
        if not os.path.exists(f'{website_folderpath}/preparations/teas'): os.mkdir(f'{website_folderpath}/preparations/teas')
        # if os.path.exists(json_filepath): os.remove(json_filepath)
        # continue

        data = json_read(json_filepath, create=True)
        data['herb_slug'] = herb_slug
        data['herb_name_scientific'] = herb_name_scientific
        data['url'] = url
        if 'lastmod' not in data: data['lastmod'] = today()

        data['title'] = f'{herb_name_scientific} tea'.title()

        json_write(json_filepath, data)

        # ====================================================
        # ;json
        # ====================================================
                # Use simple and short words, and a simple writing style.

        # intro desc
        key = 'intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write a 5-sentence paragraph about {herb_name_scientific} tea for medicinal use.
                Include uses, benefits, constituents, and possible side effects.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Use a conversational and fluid writing style.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                Start with the following words: {herb_name_scientific} .
            '''
            reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
            data[key] = reply
            json_write(json_filepath, data)

        # ;images
        img_url = f"images/preparations/teas/{herb_slug}-herbal-teas.jpg"
        src = f'/{img_url}'
        alt = f'{herb_name_scientific} tea'
        data['intro_image_src'] = src
        data['intro_image_alt'] = alt
        json_write(json_filepath, data)

        # uses img
        data['uses_image_src'] = f'/images/teas/{herb_slug}-uses.jpg'
        data['uses_image_alt'] = f'{herb_name_scientific} tea uses'
        json_write(json_filepath, data)

        # benefits img
        data['benefits_image_src'] = f'/images/teas/{herb_slug}-benefits.jpg'
        data['benefits_image_alt'] = f'{herb_name_scientific} tea benefits'
        json_write(json_filepath, data)

        # constituents img
        data['constituents_image_src'] = f'/images/teas/{herb_slug}-constituents.jpg'
        data['constituents_image_alt'] = f'{herb_name_scientific} tea constituents'
        json_write(json_filepath, data)

        # preparation img
        data['preparation_image_src'] = f'/images/teas/{herb_slug}-preparation.jpg'
        data['preparation_image_alt'] = f'{herb_name_scientific} tea preparation'
        json_write(json_filepath, data)

        # side effects img
        data['side_effects_image_src'] = f'/images/teas/{herb_slug}-side-effects.jpg'
        data['side_effects_image_alt'] = f'{herb_name_scientific} tea side effects'
        json_write(json_filepath, data)

        # uses desc
        key = 'uses_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write a 5-sentence paragraph explaining what are the most common uses of {herb_name_scientific} tea.
                By "uses" I mean what ailments and health problems they are used to heal.
                Don't explain why has those uses, only explain what are the uses and what they mean for people.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Use a conversational and fluid writing style.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                Start with the following words: {herb_name_scientific} are commonly used to .
            '''
            reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
            data[key] = reply
            json_write(json_filepath, data)

        # benefits desc
        key = 'benefits_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write a 5-sentence paragraph explaining what are the most well-known benefits of {herb_name_scientific} tea.
                Don't include the boiactive constituents, only explain the benefits and why these benefits are good for people.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Use a conversational and fluid writing style.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                Start with the following words: {herb_name_scientific} tea helps .
            '''
            reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
            data[key] = reply
            json_write(json_filepath, data)

        # constituents desc
        key = 'constituents_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write a 5-sentence paragraph explaining what are the most important bioactive constituents of {herb_name_scientific} tea for medicinal purposes.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Use a conversational and fluid writing style.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                Start with the following words: {herb_name_scientific} tea contains .
            '''
            reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
            data[key] = reply
            json_write(json_filepath, data)

        # preparation desc
        key = 'preparation_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write a 5-sentence paragraph explaining how to make {herb_name_scientific} tea for medicinal purposes.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Use a conversational and fluid writing style.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                Start with the following words: To make {herb_name_scientific} tea, .
            '''
            reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
            data[key] = reply
            json_write(json_filepath, data)

        # side effects desc
        key = 'side_effects_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write a 5-sentence paragraph explaining the possible side effects of {herb_name_scientific} tea if used improperly.
                Don't include words that communicate the feeling that the data you provide is not proven, like "can", "may", "might" and "is believed to". 
                Use a conversational and fluid writing style.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                Start with the following words: If used improperly, {herb_name_scientific} tea, .
            '''
            reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
            data[key] = reply
            json_write(json_filepath, data)

        #####################################################################3
        # ;html
        #####################################################################3
        article_html = ''
        _title = f'{herb_name_scientific} ({herb_name_common}) Tea for Medicinal Use'.title()
        article_html += f'<h1>{_title}</h1>\n'
        src = data['intro_image_src']
        alt = data['intro_image_alt']
        article_html += f'<img class="article-img" src="{src}" alt="{alt}">\n'
        article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'

        # ;aff_link 
        keyword_search = f'{herb_name_common_slug}-tea'
        aff_links_rows_related = [row for row in aff_links_rows if row.split('\\')[0] == keyword_search]
        if aff_links_rows_related != []: aff_link_row = aff_links_rows_related[0]
        else: aff_link_row = []
        if aff_link_row != []:
            aff_link_data = aff_link_row.split('\\')
            aff_link_url = aff_link_data[1]
            aff_link_title = aff_link_data[2]
            _html = gen_aff_html(aff_link_url, aff_link_title, herb_name_common)
            article_html += _html


        article_html += f'<h2>Uses of {herb_name_scientific} tea</h2>\n'
        article_html += f'''<img class="article-img" src="{data['uses_image_src']}" alt="{data['uses_image_alt']}">\n'''
        article_html += f'{util.text_format_1N1_html(data["uses_desc"])}\n'

        article_html += f'<h2>Benefits of {herb_name_scientific} tea</h2>\n'
        article_html += f'''<img class="article-img" src="{data['benefits_image_src']}" alt="{data['benefits_image_alt']}">\n'''
        article_html += f'{util.text_format_1N1_html(data["benefits_desc"])}\n'

        article_html += f'<h2>Constituents of {herb_name_scientific} tea</h2>\n'
        article_html += f'''<img class="article-img" src="{data['constituents_image_src']}" alt="{data['constituents_image_alt']}">\n'''
        article_html += f'{util.text_format_1N1_html(data["constituents_desc"])}\n'

        article_html += f'<h2>How to make {herb_name_scientific} tea</h2>\n'
        article_html += f'''<img class="article-img" src="{data['preparation_image_src']}" alt="{data['preparation_image_alt']}">\n'''
        article_html += f'{util.text_format_1N1_html(data["preparation_desc"])}\n'

        article_html += f'<h2>Possible side effects {herb_name_scientific} tea</h2>\n'
        article_html += f'''<img class="article-img" src="{data['side_effects_image_src']}" alt="{data['side_effects_image_alt']}">\n'''
        article_html += f'{util.text_format_1N1_html(data["side_effects_desc"])}\n'

        breadcrumbs_html_filepath = f'{url}.html'
        breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
        meta_html = gen_meta(article_html, data["lastmod"])

        head_html = head_html_generate(data['title'], '/style.css')

        main_html = html_article_main(meta_html, article_html, '')
        layout_html = html_article_layout(main_html, '')


        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                {breadcrumbs_html}
                {layout_html}
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)
        # quit()

def p_equipments(equipments_slugs):
    url = f'equipments'
    title = f'what equipments herbalists use?'
    json_filepath = f'equipments/jsons/equipments.json'
    html_filepath = f'{website_folderpath}/{url}.html'
    json_article = json_read(json_filepath, create=True)
    if 'lastmod' not in json_article: json_article['lastmod'] = today()
    json_article['title'] = title
    json_article['url'] = url
    json_write(json_filepath, json_article)
    # ;json
    key = 'intro'
    if key not in json_article: json_article[key] = ''
    # json_article[key] = ''
    if json_article[key] == '':
        prompt = f'''
            Write a 4-sentence short paragraph about the most common equipment used by herbalists to make herbal preparations.
        '''
        reply = llm_reply(prompt, model).strip()
        if reply.strip() != '':
            json_article[key] = reply
            json_write(json_filepath, json_article)
    # ;equipments
    for i, equipment_slug in enumerate(equipments_slugs):
        # init
        key = 'equipments'
        if key not in json_article: json_article[key] = []
        found = False
        for obj in json_article[key]:
            if obj['equipment_slug'] == equipment_slug:
                found = True
                break
        if not found:
            equipment = {'equipment_slug': equipment_slug}
            json_article[key].append(equipment)
        json_write(json_filepath, json_article)
        # update
        if 'equipments' not in json_article: json_article['equipments'] = []
        for obj in json_article['equipments']:
            if obj['equipment_slug'] == equipment_slug:
                equipment_name = equipment_slug.strip().lower().replace('-', ' ')
                obj['equipment_name'] = equipment_name
                obj['equipment_title'] = equipment_name
                json_write(json_filepath, json_article)
                # ;desc
                if 'equipment_desc' not in obj: obj['equipment_desc'] = ''
                # obj['equipment_desc'] = ''
                if obj['equipment_desc'] == '':
                    prompt = f'''
                        Write a 5-sentence 100-word paragraph about {equipment_name} for apothecary.
                        Include what this equipment is and why it's used.
                    '''
                    reply = llm_reply(prompt, model).strip()
                    # json_data = json.loads(reply)
                    if reply.strip() != '':
                        obj['equipment_desc'] = reply
                        json_write(json_filepath, json_article)
                break

    ##################################################################
    # ;HTML
    ##################################################################
    article_html = ''
    article_html += f'''<h1>{json_article["title"].title()}</h1>\n'''
    src = f'/images-static/herbalists-equipments.jpg'
    alt = f'equipments for herbalists'
    article_html += f'''<img style="margin-bottom: 16px;" src="{src}" alt="{alt}">\n'''
    article_html += f'{util.text_format_1N1_html(json_article["intro"])}\n'

    for i, obj in enumerate(json_article['equipments']):
        _equipment_head = obj['equipment_title']
        _equipment_desc = obj['equipment_desc']
        _equipment_slug = obj['equipment_slug']
        _equipment_name = obj['equipment_name']
        _html = f'''
            <h2>{_equipment_head.title()}</h2>
            <img style="margin-bottom: 16px;" src="/images/equipments/{_equipment_slug}.jpg" alt="{_equipment_name} for herbalism">
            {util.text_format_1N1_html(_equipment_desc)}
            <p>Here are the <a href="/equipments/{_equipment_slug}.html">best {_equipment_name} for herbalists</a>.
        '''
        article_html += _html

    breadcrumbs_html_filepath = f'{url}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    meta_html = gen_meta(article_html, json_article["lastmod"])
    head_html = head_html_generate(json_article['title'], '/style.css')
    main_html = html_article_main(meta_html, article_html, '')
    layout_html = html_article_layout(main_html, '')

    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            {layout_html}
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    print(html_filepath)
    with open(html_filepath, 'w') as f: f.write(html)
    


def a_equipment(equipment_slug):
    equipment_name = equipment_slug.lower().strip().replace('-', ' ')
    title = f'best {equipment_name} for herbalists'
    url = f'equipments/{equipment_slug}'
    json_filepath = f'equipments/jsons/{equipment_slug}.json'
    products_jsons_folderpath = f'{vault}/amazon/json/{equipment_slug}'
    html_filepath = f'{website_folderpath}/{url}.html'
    #####################################################
    # JSON
    #####################################################
    data = json_read(json_filepath, create=True)
    data['equipment_slug'] = equipment_slug
    data['equipment_name'] = equipment_name
    data['title'] = title
    data['url'] = url
    if 'products_num' not in data: data['products_num'] = random.choice([7, 9, 11, 13])
    products_num = data['products_num']
    if 'lastmod' not in data: data['lastmod'] = today()
    lastmod = data['lastmod']
    json_write(json_filepath, data)
    # ;intro
    if 'intro_desc' not in data: data['intro_desc'] = ''
    # data['intro_desc'] = ''
    if data['intro_desc'] == '':
        prompt = f'''
            Write a 5-sentence 100-word pargraph about {equipment_name} for apothecaries. 
            Include what this product is and why apothecaries use it.
        '''
        reply = llm_reply(prompt, model).strip()
        if reply.strip() != '':
            data['intro_desc'] = reply
            json_write(json_filepath, data)

    # ;jump
    # products
    products_jsons_filepaths = [f'{products_jsons_folderpath}/{x}' for x in os.listdir(products_jsons_folderpath)]
    # order filepaths by popularity
    products_jsons = []
    for i, product_json_filepath in enumerate(products_jsons_filepaths):
        product_data = json_read(product_json_filepath, create=True)
        product_asin = product_json_filepath.split('/')[-1].replace('.json', '')
        reviews_score_total = float(product_data['reviews_score_total'])
        products_jsons.append({'product_asin': product_asin, 'reviews_score_total': reviews_score_total})
    products_jsons_ordered = sorted(products_jsons, key=lambda x: x['reviews_score_total'], reverse=True)
    products_jsons_filepaths_ordered = []
    for product_json in products_jsons_ordered:
        product_asin = product_json['product_asin']
        product_filepath = f'{products_jsons_folderpath}/{product_asin}.json'
        products_jsons_filepaths_ordered.append(product_filepath)
    products_jsons_filepaths_ordered = products_jsons_filepaths_ordered[:products_num]
    # products
    for i, product_json_filepath in enumerate(products_jsons_filepaths_ordered):
        product_data = json_read(product_json_filepath, create=True)
        product_aff_link = product_data['affiliate_link']
        product_title = product_data['title']
        product_asin = product_json_filepath.split('/')[-1].replace('.json', '')
        # init
        key = 'products'
        if key not in data: data[key] = []
        found = False
        for obj in data[key]:
            if obj['product_id'] == product_asin:
                found = True
                break
        if not found:
            product = {'product_id': product_asin}
            data[key].append(product)
        json_write(json_filepath, data)
        # update
        if 'products' not in data: data['products'] = []
        for obj in data['products']:
            if obj['product_id'] == product_asin:
                obj['product_title'] = product_title
                obj['product_aff_link'] = product_aff_link
                json_write(json_filepath, data)
                # ;title
                if 'product_title_ai' not in obj: obj['product_title_ai'] = ''
                # obj['product_title_ai'] = ''
                if obj['product_title_ai'] == '':
                    prompt = f'''
                        Rewrite the following TITLE of a product using the following GUIDELINES: 
                        {product_title}
                        GUIDELINES:
                        Reply in less than 10 words.
                        Keep only the most important things for the TITLE.
                        Include the text "{equipment_name}".
                        Reply in the following JSON format: 
                        {{"title": "insert the rewritten title here"}} 
                        Only reply with the JSON.
                    '''
                    reply = llm_reply(prompt, model).strip()
                    # json_data = json.loads(reply)
                    try: json_data = json.loads(reply)
                    except: json_data = {}
                    if json_data != {}:
                        try: line = json_data['title']
                        except: continue
                        obj['product_title_ai'] = line
                        json_write(json_filepath, data)

                # ;pros
                if 'product_pros' not in obj: obj['product_pros'] = []
                # if 'product_pros' in obj: obj['product_pros'] = []
                if obj['product_pros'] == []:
                    positive_reviews_text = product_data['reviews_5s']
                    outputs = []
                    prompt = f'''
                        Extract a list of the most mentioned and recurring key features from the following CUSTOMERS REVIEWS.
                        Also, follow the GUIDELINES below.
                        CUSTOMERS REVIEWS:
                        {positive_reviews_text}
                        GUIDELINES:
                        Write the features in 7-10 words.
                        Reply in the following JSON format: 
                        [
                            {{"feature": "write feature 1 here"}}, 
                            {{"feature": "write feature 2 here"}}, 
                            {{"feature": "write feature 3 here"}}, 
                            {{"feature": "write feature 4 here"}}, 
                            {{"feature": "write feature 5 here"}} 
                        ]
                        Only reply with the JSON.
                    '''
                    reply = llm_reply(prompt, model).strip()
                    # json_data = json.loads(reply)
                    try: json_data = json.loads(reply)
                    except: json_data = {}
                    if json_data != {}:
                        for item in json_data:
                            try: line = item['feature']
                            except: continue
                            outputs.append(line)
                    obj['product_pros'] = outputs
                    json_write(json_filepath, data)

                # ;cons
                if 'product_cons' not in obj: obj['product_cons'] = []
                # if 'product_cons' in obj: obj['product_cons'] = []
                if obj['product_cons'] == []:
                    negative_reviews_text = product_data['reviews_1s']
                    outputs = []
                    if negative_reviews_text.strip() != '':
                        prompt = f'''
                            Extract a list of the most mentioned and recurring complaints from the following CUSTOMERS REVIEWS.
                            Also, follow the GUIDELINES below.
                            CUSTOMERS REVIEWS:
                            {negative_reviews_text}
                            GUIDELINES:
                            Write the features in 7-10 words.
                            Reply in the following JSON format: 
                            [
                                {{"complaint": "write complaint 1 here"}}, 
                                {{"complaint": "write complaint 2 here"}}, 
                                {{"complaint": "write complaint 3 here"}}, 
                                {{"complaint": "write complaint 4 here"}}, 
                                {{"complaint": "write complaint 5 here"}} 
                            ]
                            Only reply with the JSON.
                        '''
                        reply = llm_reply(prompt, model).strip()
                        try: json_data = json.loads(reply)
                        except: json_data = {}
                        if json_data != {}:
                            for item in json_data:
                                try: line = item['complaint']
                                except: continue
                                outputs.append(line)
                    obj['product_cons'] = outputs
                    json_write(json_filepath, data)

                # ;description
                if 'product_desc' not in obj: obj['product_desc'] = ''
                # if 'product_desc' in obj: obj['product_desc'] = ''
                if obj['product_desc'] == '':
                    pros = '\n'.join(obj['product_pros'])
                    cons = '\n'.join(obj['product_cons'])
                    prompt = f'''
                        Write a short 5-sentence paragraph about the following product: {equipment_name}.
                        The target audience for this product is: herbalists.
                        Use the following PROS and CONS to describe the features, and use the GUIDELINES below.
                        PROS:
                        {pros}
                        CONS:
                        {cons}
                        GUIDELIES:
                        Try to include 1-2 CONS.
                        Reply in paragraph format.
                        Don't write conclusory statements, like sentences that starts with "overall", "in conclusion", "to summarize", etc...
                        Start writing the features from the first sentence.
                        Start with the following words: These {equipment_name} .
                    '''
                    prompt = f'''
                        Write a short 5-sentence paragraph about the following product: {equipment_name}.
                        The target audience for this product is: apothecary.
                        Use the following INFO to describe the features, and use the GUIDELINES below.
                        INFO:
                        {pros}
                        GUIDELIES:
                        Reply in paragraph format.
                        Don't write conclusory statements, like sentences that starts with "overall", "in conclusion", "to summarize", etc...
                        Start writing the features from the first sentence.
                        Start with the following words: These {equipment_name} .
                    '''
                    reply = llm_reply(prompt)
                    obj['product_desc'] = reply
                    json_write(json_filepath, data)

                # ;cons_description
                if 'product_cons_desc' not in obj: obj['product_cons_desc'] = ''
                # if 'product_cons_desc' in obj: obj['product_cons_desc'] = ''
                if obj['product_cons_desc'] == '':
                    cons = '\n'.join(obj['product_cons'])
                    prompt = f'''
                        Write 1 short sentence about some of the complaints a few users had about the following product: {equipment_name}.
                        The COMPLAINTS are listed below.
                        <COMPLAINTS>
                        {cons}
                        </COMPLAINTS>
                        GUIDELIES:
                        Reply in paragraph format.
                        Don't write conclusory statements, like sentences that starts with "overall", "in conclusion", "to summarize", etc...
                        Try to include only the complaints that are specific to the characteristics of the products, not complaints about exernal factors (like bad shipping, etc.).
                        Start with the following words: Some users .
                    '''
                    reply = llm_reply(prompt)
                    obj['product_cons_desc'] = reply
                    json_write(json_filepath, data)

                break

    ##################################################################
    # ;IMG
    ##################################################################
    out_filepath = f'{website_folderpath}/images/equipments/{equipment_slug}.jpg'
    ast_filepath = f'assets/images/equipments/{equipment_slug}.jpg'
    # if os.path.exists(ost_filepath):
    if True:
        print(ast_filepath)
        print(out_filepath)
        image_w = 768
        image_h = 768
        pin_w = image_w
        pin_h = image_h
        img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
        _img = Image.open(ast_filepath)
        img.paste(_img, (0, 0))
        if 0:
            images_filepaths = [f'tmp-images/{x}' for x in os.listdir(f'tmp-images')]
            gap = 4
            if len(images_filepaths) == 4:
                img_0000 = Image.open(images_filepaths[0])
                img_0001 = Image.open(images_filepaths[1])
                img_0002 = Image.open(images_filepaths[2])
                img_0003 = Image.open(images_filepaths[3])
                img_0000 = util.img_resize(img_0000, int(pin_w*0.50), int(pin_h*0.5))
                img_0001 = util.img_resize(img_0001, int(pin_w*0.50), int(pin_h*0.5))
                img_0002 = util.img_resize(img_0002, int(pin_w*0.50), int(pin_h*0.5))
                img_0003 = util.img_resize(img_0003, int(pin_w*0.50), int(pin_h*0.5))
                img.paste(img_0000, (0, 0))
                img.paste(img_0001, (int(pin_w*0.50) + gap, 0))
                img.paste(img_0002, (0, int(pin_h*0.5) + gap))
                img.paste(img_0003, (int(pin_w*0.50) + gap, int(pin_h*0.5) + gap))
            if len(images_filepaths) == 9:
                img_0000 = Image.open(images_filepaths[0])
                img_0001 = Image.open(images_filepaths[1])
                img_0002 = Image.open(images_filepaths[2])
                img_0003 = Image.open(images_filepaths[3])
                img_0004 = Image.open(images_filepaths[4])
                img_0005 = Image.open(images_filepaths[5])
                img_0006 = Image.open(images_filepaths[6])
                img_0007 = Image.open(images_filepaths[7])
                img_0008 = Image.open(images_filepaths[8])
                img_0000 = util.img_resize(img_0000, int(pin_w*0.34), int(pin_h*0.34))
                img_0001 = util.img_resize(img_0001, int(pin_w*0.34), int(pin_h*0.34))
                img_0002 = util.img_resize(img_0002, int(pin_w*0.34), int(pin_h*0.34))
                img_0003 = util.img_resize(img_0003, int(pin_w*0.34), int(pin_h*0.34))
                img_0004 = util.img_resize(img_0004, int(pin_w*0.34), int(pin_h*0.34))
                img_0005 = util.img_resize(img_0005, int(pin_w*0.34), int(pin_h*0.34))
                img_0006 = util.img_resize(img_0006, int(pin_w*0.34), int(pin_h*0.34))
                img_0007 = util.img_resize(img_0007, int(pin_w*0.34), int(pin_h*0.34))
                img_0008 = util.img_resize(img_0008, int(pin_w*0.34), int(pin_h*0.34))
                img.paste(img_0000, (0, 0))
                img.paste(img_0001, (int(pin_w*0.34) + gap, 0))
                img.paste(img_0002, ((int(pin_w*0.34) + gap)*2, 0))
                img.paste(img_0003, (0, int(pin_h*0.34) + gap))
                img.paste(img_0004, (int(pin_w*0.34) + gap, int(pin_h*0.34) + gap))
                img.paste(img_0005, ((int(pin_w*0.34) + gap)*2, int(pin_h*0.34) + gap))
                img.paste(img_0006, (0, (int(pin_h*0.34) + gap)*2))
                img.paste(img_0007, (int(pin_w*0.34) + gap, (int(pin_h*0.34) + gap)*2))
                img.paste(img_0008, ((int(pin_w*0.34) + gap)*2, (int(pin_h*0.34) + gap)*2))
        '''
        draw = ImageDraw.Draw(img)
        rect_w = 480
        rect_h = 160
        x1 = image_w//2 - rect_w//2 
        y1 = image_h//2 - rect_h//2 
        x2 = image_w//2 + rect_w//2 
        y2 = image_h//2 + rect_h//2 
        draw.rectangle(
            (
                (x1, y1), 
                (x2, y2),
            ), 
            fill='#000000',
        )
        # title
        text = f'best {equipment_name}'.upper()
        title_font_size = 48
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, title_font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = image_w//2 - text_w//2
        y_cur = image_h//2 - text_h
        draw.text((x1, y_cur), text, '#ffffff', font=font)
        y_cur += title_font_size * 1.5
        # terrawhisper
        text = f'terrawhisper.com'
        font_size = 16
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = image_w//2 - text_w//2
        draw.text((x1, y_cur), text, '#ffffff', font=font)
        '''
        img.save(out_filepath, format='JPEG', subsampling=0, quality=70)

    ##################################################################
    # ;HTML
    ##################################################################
    article_html = ''
    article_html += f'''<h1>{data["products_num"]} {data["title"]}</h1>\n'''
    src = f'/images/equipments/{equipment_slug}.jpg'
    alt = f'{equipment_name} for herbalists'
    article_html += f'''<img class="mb-16" src="{src}" alt="{alt}">\n'''
    article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'
    if 'products' not in data: data['products'] = []
    for i, obj in enumerate(data['products'][:products_num]):
        asin = obj['product_id']
        product_title_ai = obj['product_title_ai']
        product_desc = obj['product_desc']
        product_aff_link = obj['product_aff_link']
        product_pros = obj['product_pros']
        product_cons = obj['product_cons']
        product_cons_desc = obj['product_cons_desc']

        article_html += f'<h2>{i+1}. {product_title_ai}</h2>\n'
        article_html += f'{util.text_format_1N1_html(product_desc)}\n'
        article_html += f'<p class="helvetica-bold text-black">Key Features:</p>\n'
        article_html += f'<ul>\n'
        for item in product_pros[:5]:
            article_html += f'<li>{item}</li>\n'
        article_html += f'</ul>\n'
        article_html += f'<p class="helvetica-bold text-black">Warnings:</p>\n'
        article_html += f'{util.text_format_1N1_html(product_cons_desc)}\n'
        product_img_filepath = f'{vault}/amazon/images/{equipment_slug}/{asin}.txt'
        print(product_img_filepath)
        amazon_button_html = amazon_buy_button(product_aff_link, product_img_filepath)
        article_html += amazon_button_html

    breadcrumbs_html_filepath = f'{url}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    meta_html = gen_meta(article_html, data["lastmod"])
    head_html = head_html_generate(data['title'], '/style.css')
    main_html = html_article_main(
        meta_html = meta_html, 
        article_html = article_html, 
        related_html = '', 
        affiliate_disclaimer_html = ''
    )
    layout_html = html_article_layout(main_html, '')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            {layout_html}
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def equipment_a(product_slug):
    equipment_slug = product_slug
    equipment_name = equipment_slug.lower().strip().replace(' ', '-')

    title = f'best {product_slug} for apothecary'
    url = f'equipments/{product_slug}'
    products_num = 9

    assets_folderpath = f'equipments/assets'
    jsons_folderpath = f'equipments/jsons'

    jars_assets_folderpath = f'{assets_folderpath}/{product_slug}'
    jars_json_filepath = f'{jsons_folderpath}/{product_slug}.json'

    html_filepath = f'{website_folderpath}/{url}.html'


    #####################################################
    # JSON
    #####################################################

    with open(f'{jars_assets_folderpath}/_urls.txt') as f: 
        affiliate_links_rows = [x.strip() for x in f.read().strip().split('\n') if x.strip() != '']

    data = json_read(jars_json_filepath, create=True)
    data['equipment_slug'] = equipment_slug
    data['equipment_name'] = equipment_name
    data['title'] = title
    data['url'] = url
    data['products_num'] = products_num
    if 'lastmod' not in data: data['lastmod'] = today()
    json_write(jars_json_filepath, data)

    # ;json products
    for i, affiliate_link_row in enumerate(affiliate_links_rows):
        affiliate_link_cols = affiliate_link_row.split('\\')
        product_page_link = affiliate_link_cols[0]
        product_aff_link = affiliate_link_cols[1]

        _id = product_page_link.split('/')[-1] # amazon asin
        product_title_short = product_page_link.split('/')[-3].replace('-', ' ') # amazon title short
        
        # init products list
        key = 'products'
        if key not in data: data[key] = []
        found = False
        for obj in data[key]:
            if obj['product_id'] == _id:
                found = True
                break
        if not found:
            product = {'product_id': _id}
            data[key].append(product)
        json_write(jars_json_filepath, data)
        
        # update products data
        if 'products' not in data: data['products'] = []
        for obj in data['products']:
            if obj['product_id'] == _id:
                obj['product_title_short'] = product_title_short
                obj['product_aff_link'] = product_aff_link
                json_write(jars_json_filepath, data)

                # ;pros
                if 'product_pros' not in obj: obj['product_pros'] = []
                # if 'product_pros' in obj: obj['product_pros'] = []
                if obj['product_pros'] == []:
                    with open(f'{jars_assets_folderpath}/{_id}-reviews-5star.txt') as f: positive_reviews_text = f.read()
                    outputs = []
                    prompt = f'''
                        Extract a list of the most mentioned and recurring key features from the following CUSTOMERS REVIEWS.
                        Also, follow the GUIDELINES below.
                        CUSTOMERS REVIEWS:
                        {positive_reviews_text}
                        GUIDELINES:
                        Write the features in 7-10 words.
                        Reply in the following JSON format: 
                        [
                            {{"feature": "write feature 1 here"}}, 
                            {{"feature": "write feature 2 here"}}, 
                            {{"feature": "write feature 3 here"}}, 
                            {{"feature": "write feature 4 here"}}, 
                            {{"feature": "write feature 5 here"}} 
                        ]
                        Only reply with the JSON.
                    '''
                    reply = llm_reply(prompt, model).strip()
                    # json_data = json.loads(reply)
                    try: json_data = json.loads(reply)
                    except: json_data = {}
                    if json_data != {}:
                        for item in json_data:
                            try: line = item['feature']
                            except: continue
                            outputs.append(line)
                    obj['product_pros'] = outputs
                    json_write(jars_json_filepath, data)

                # ;cons
                if 'product_cons' not in obj: obj['product_cons'] = []
                # if 'product_cons' in obj: obj['product_cons'] = []
                if obj['product_cons'] == []:
                    with open(f'{jars_assets_folderpath}/{_id}-reviews-1star.txt') as f: negative_reviews_text = f.read()
                    outputs = []
                    if negative_reviews_text.strip() != '':
                        prompt = f'''
                            Extract a list of the most mentioned and recurring complaints from the following CUSTOMERS REVIEWS.
                            Also, follow the GUIDELINES below.
                            CUSTOMERS REVIEWS:
                            {negative_reviews_text}
                            GUIDELINES:
                            Write the features in 7-10 words.
                            Reply in the following JSON format: 
                            [
                                {{"complaint": "write complaint 1 here"}}, 
                                {{"complaint": "write complaint 2 here"}}, 
                                {{"complaint": "write complaint 3 here"}}, 
                                {{"complaint": "write complaint 4 here"}}, 
                                {{"complaint": "write complaint 5 here"}} 
                            ]
                            Only reply with the JSON.
                        '''
                        reply = llm_reply(prompt, model).strip()
                        try: json_data = json.loads(reply)
                        except: json_data = {}
                        if json_data != {}:
                            for item in json_data:
                                try: line = item['complaint']
                                except: continue
                                outputs.append(line)
                    obj['product_cons'] = outputs
                    json_write(jars_json_filepath, data)

                # ;description
                if 'product_desc' not in obj: obj['product_desc'] = ''
                # if 'product_desc' in obj: obj['product_desc'] = ''
                if obj['product_desc'] == '':
                    pros = '\n'.join(obj['product_pros'])
                    cons = '\n'.join(obj['product_cons'])
                    prompt = f'''
                        Write a short 5-sentence paragraph about the following product: jars.
                        The target audience for this product is: herbalists.
                        Use the following PROS and CONS to describe the features, and use the GUIDELINES below.
                        PROS:
                        {pros}
                        CONS:
                        {cons}
                        GUIDELIES:
                        Try to include 1-2 CONS.
                        Reply in paragraph format.
                        Don't write conclusory statements, like sentences that starts with "overall", "in conclusion", "to summarize", etc...
                        Start writing the features from the first sentence.
                        Start with the following words: These jars .
                    '''
                    reply = llm_reply(prompt)
                    obj['product_desc'] = reply
                    json_write(jars_json_filepath, data)

                break

    ##################################################################
    # ;IMAGES
    ##################################################################
    products_img_url_0000 = f'images/equipments/{product_slug}.jpg'
    out_filepath = f'{website_folderpath}/{products_img_url_0000}'
    src = f'/{products_img_url_0000}'
    alt = f'examples of {product_slug} for herbalists'

    if not os.path.exists(out_filepath):
    # if True:
        if 0:
            for i in range(9):
                prompt = f'''
                    {product_slug},
                    on a wooden table,
                    dry herbs,
                    indoor, 
                    natural light,
                    earth tones,
                    neutral colors,
                    soft focus,
                    warm tones,
                    vintage,
                    high resolution,
                    cinematic
                '''
                negative_prompt = f'''
                    text, watermark 
                '''
                print(prompt)
                pipe_init()
                image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                image = img_resize(image, w=768, h=768)
                image.save(f'tmp-images/{i}.jpg')
            
        images_filepaths = [f'tmp-images/{x}' for x in os.listdir(f'tmp-images')]
        print(images_filepaths)

        image_w = 768
        image_h = 768
        pin_w = image_w
        pin_h = image_h
        img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
        gap = 4
        if len(images_filepaths) == 4:
            img_0000 = Image.open(images_filepaths[0])
            img_0001 = Image.open(images_filepaths[1])
            img_0002 = Image.open(images_filepaths[2])
            img_0003 = Image.open(images_filepaths[3])
            img_0000 = util.img_resize(img_0000, int(pin_w*0.50), int(pin_h*0.5))
            img_0001 = util.img_resize(img_0001, int(pin_w*0.50), int(pin_h*0.5))
            img_0002 = util.img_resize(img_0002, int(pin_w*0.50), int(pin_h*0.5))
            img_0003 = util.img_resize(img_0003, int(pin_w*0.50), int(pin_h*0.5))
            img.paste(img_0000, (0, 0))
            img.paste(img_0001, (int(pin_w*0.50) + gap, 0))
            img.paste(img_0002, (0, int(pin_h*0.5) + gap))
            img.paste(img_0003, (int(pin_w*0.50) + gap, int(pin_h*0.5) + gap))
        if len(images_filepaths) == 9:
            img_0000 = Image.open(images_filepaths[0])
            img_0001 = Image.open(images_filepaths[1])
            img_0002 = Image.open(images_filepaths[2])
            img_0003 = Image.open(images_filepaths[3])
            img_0004 = Image.open(images_filepaths[4])
            img_0005 = Image.open(images_filepaths[5])
            img_0006 = Image.open(images_filepaths[6])
            img_0007 = Image.open(images_filepaths[7])
            img_0008 = Image.open(images_filepaths[8])
            img_0000 = util.img_resize(img_0000, int(pin_w*0.34), int(pin_h*0.34))
            img_0001 = util.img_resize(img_0001, int(pin_w*0.34), int(pin_h*0.34))
            img_0002 = util.img_resize(img_0002, int(pin_w*0.34), int(pin_h*0.34))
            img_0003 = util.img_resize(img_0003, int(pin_w*0.34), int(pin_h*0.34))
            img_0004 = util.img_resize(img_0004, int(pin_w*0.34), int(pin_h*0.34))
            img_0005 = util.img_resize(img_0005, int(pin_w*0.34), int(pin_h*0.34))
            img_0006 = util.img_resize(img_0006, int(pin_w*0.34), int(pin_h*0.34))
            img_0007 = util.img_resize(img_0007, int(pin_w*0.34), int(pin_h*0.34))
            img_0008 = util.img_resize(img_0008, int(pin_w*0.34), int(pin_h*0.34))
            img.paste(img_0000, (0, 0))
            img.paste(img_0001, (int(pin_w*0.34) + gap, 0))
            img.paste(img_0002, ((int(pin_w*0.34) + gap)*2, 0))
            img.paste(img_0003, (0, int(pin_h*0.34) + gap))
            img.paste(img_0004, (int(pin_w*0.34) + gap, int(pin_h*0.34) + gap))
            img.paste(img_0005, ((int(pin_w*0.34) + gap)*2, int(pin_h*0.34) + gap))
            img.paste(img_0006, (0, (int(pin_h*0.34) + gap)*2))
            img.paste(img_0007, (int(pin_w*0.34) + gap, (int(pin_h*0.34) + gap)*2))
            img.paste(img_0008, ((int(pin_w*0.34) + gap)*2, (int(pin_h*0.34) + gap)*2))
        draw = ImageDraw.Draw(img)
        rect_w = 480
        rect_h = 160
        x1 = image_w//2 - rect_w//2 
        y1 = image_h//2 - rect_h//2 
        x2 = image_w//2 + rect_w//2 
        y2 = image_h//2 + rect_h//2 
        draw.rectangle(
            (
                (x1, y1), 
                (x2, y2),
            ), 
            fill='#000000',
        )
        # title
        text = f'best jars'.upper()
        title_font_size = 48
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, title_font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = image_w//2 - text_w//2
        y_cur = image_h//2 - text_h
        draw.text((x1, y_cur), text, '#ffffff', font=font)
        y_cur += title_font_size * 1.5

        # terrawhisper
        text = f'terrawhisper.com'
        font_size = 16
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = image_w//2 - text_w//2
        draw.text((x1, y_cur), text, '#ffffff', font=font)
        img.save(out_filepath, format='JPEG', subsampling=0, quality=70)

    data['products_img_src_0000'] = src
    data['products_img_alt_0000'] = alt
    json_write(jars_json_filepath, data)

    if 0:
        key = 'products_img_src_0000'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            images_filepaths = []
            for preparation in data['preparations'][:5]:
                preparation_name = preparation['preparation_name']
                preparation_check = ''
                if 'tea' in preparation_name.lower(): preparation_check = 'teas'
                if 'tincture' in preparation_name.lower(): preparation_check = 'tinctures'
                if 'cream' in preparation_name.lower(): preparation_check = 'creams'
                if 'essential' in preparation_name.lower(): preparation_check = 'essential-oils'
                if preparation_name[-1] != 's': preparation_name += 's'
                preparation_link_out = f'{website_folderpath}/{url}/{preparation_check}.html'
                found = False
                if preparation_check != '':
                    if os.path.exists(preparation_link_out): 
                        found = True
                if found:
                    _json_filepath = f'database/json/{url}/{preparation_check}.json'
                    _data = json_read(_json_filepath)
                    images_filepaths.append(f'{website_folderpath}' + _data['intro_image_src'])
            pin_w = 768
            pin_h = 768
            img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
            gap = 8
            if len(images_filepaths) >= 4:
                img_0000 = Image.open(images_filepaths[0])
                img_0001 = Image.open(images_filepaths[1])
                img_0002 = Image.open(images_filepaths[2])
                img_0003 = Image.open(images_filepaths[3])
                img_0000 = util.img_resize(img_0000, int(pin_w*0.50), int(pin_h*0.5))
                img_0001 = util.img_resize(img_0001, int(pin_w*0.50), int(pin_h*0.5))
                img_0002 = util.img_resize(img_0002, int(pin_w*0.50), int(pin_h*0.5))
                img_0003 = util.img_resize(img_0003, int(pin_w*0.50), int(pin_h*0.5))
                img.paste(img_0000, (0, 0))
                img.paste(img_0001, (int(pin_w*0.50) + gap, 0))
                img.paste(img_0002, (0, int(pin_h*0.5) + gap))
                img.paste(img_0003, (int(pin_w*0.50) + gap, int(pin_h*0.5) + gap))
            elif len(images_filepaths) >= 3:
                img_0000 = Image.open(images_filepaths[0])
                img_0001 = Image.open(images_filepaths[1])
                img_0002 = Image.open(images_filepaths[2])
                img_0000 = util.img_resize(img_0000, int(pin_w*0.50), int(pin_h*0.5))
                img_0001 = util.img_resize(img_0001, int(pin_w*0.50), int(pin_h*0.5))
                img_0002 = util.img_resize(img_0002, int(pin_w*1.00), int(pin_h*0.5))
                img.paste(img_0000, (0, 0))
                img.paste(img_0001, (int(pin_w*0.50) + gap, 0))
                img.paste(img_0002, (0, int(pin_h*0.5) + gap))
            elif len(images_filepaths) >= 2:
                img_0000 = Image.open(images_filepaths[0])
                img_0001 = Image.open(images_filepaths[1])
                img_0000 = util.img_resize(img_0000, int(pin_w*0.50), int(pin_h*1.0))
                img_0001 = util.img_resize(img_0001, int(pin_w*0.50), int(pin_h*1.0))
                img.paste(img_0000, (0, 0))
                img.paste(img_0001, (int(pin_w*0.50) + gap, 0))
            elif len(images_filepaths) >= 1:
                img_0000 = Image.open(images_filepaths[0])
                img_0000 = util.img_resize(img_0000, int(pin_w*1.0), int(pin_h*1.0))
                img.paste(img_0000, (0, 0))
            if len(images_filepaths) >= 1:
                image_out_filepath = f'{website_folderpath}/images/ailments/{ailment_slug}-herbal-preparations.jpg'
                image_src_filepath = f'/images/ailments/{ailment_slug}-herbal-preparations.jpg'
                img.save(
                    image_out_filepath,
                    format='JPEG',
                    subsampling=0,
                    quality=70,
                )
            data[key] = image_src_filepath
            json_write(json_filepath, data)

    ##################################################################
    # ;HTML
    ##################################################################
    article_html = ''
    article_html += f'''<h1>{data["products_num"]} {data["title"]}</h1>\n'''

    article_html += f'''<img src="{data['products_img_src_0000']}" alt="{data['products_img_alt_0000']}">\n'''

    if 'products' not in data: data['products'] = []
    for i, obj in enumerate(data['products']):
        product_title_short = obj['product_title_short']
        product_desc = obj['product_desc']
        product_aff_link = obj['product_aff_link']
        product_pros = obj['product_pros']

        article_html += f'<h2>{i+1}. {product_title_short}</h2>\n'
        article_html += f'{util.text_format_1N1_html(product_desc)}\n'
        article_html += f'<p class="helvetica-bold text-black">Key Features:</p>\n'
        article_html += f'<ul>\n'
        for item in product_pros[:5]:
            article_html += f'<li>{item}</li>\n'
        article_html += f'</ul>\n'
        amazon_button_html =  amazon_buy_button(product_aff_link)
        article_html += amazon_button_html

    breadcrumbs_html_filepath = f'{url}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    meta_html = gen_meta(article_html, data["lastmod"])
    head_html = head_html_generate(data['title'], '/style.css')
    main_html = html_article_main(meta_html, article_html, '')
    layout_html = html_article_layout(main_html, '')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            {layout_html}
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    print(html_filepath)
    with open(html_filepath, 'w') as f: f.write(html)


def p_taxonomy():
    kingdoms_slugs = [
        'animalia',
        'plantae',
        'fungi',
        'protista',
        'eubacteria',
        'archaebacteria',
    ]
    json_article_filepath = f'database/pages/herbs/taxonomy.json'
    html_article_filepath = f'{website_folderpath}/herbs/taxonomy.html'
    # ;json
    json_article = json_read(json_article_filepath, create=True)
    json_article['title'] = 'taxonomy of plants'
    if 'lastmod' not in json_article: json_article['lastmod'] = today()
    json_write(json_article_filepath, json_article)
    kingdoms_slugs_prompt = ', '.join(kingdoms_slugs)
    ai_paragraph_gen(
        key = 'intro', 
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a 4-sentence paragraph about the taxonomical classification of plants.
            Include:
            - What is a taxonomy (give definition).
            - Why it's important to have a taxonomical classification.
            - What is the taxonomical classification of plants. State that the main kindoms are: {kingdoms_slugs_prompt}.
            Start with the following words: The plant kingdom is .
        ''',
        print_prompt = True,
        regen = False,
    )
    if 'kingdoms' not in json_article: json_article['kingdoms'] = []
    # json_article['kingdoms'] = []
    for kingdom_slug in kingdoms_slugs:
        kingdoms = json_article['kingdoms']
        found = False
        for kingdom in kingdoms:
            if kingdom_slug == kingdom['kingdom_slug']:
                found = True
                break
        if not found:
            json_article['kingdoms'].append({
                'kingdom_slug': kingdom_slug,
                'kingdom_name': kingdom_slug.lower().strip().replace(' ', '-'),
                'kingdom_image': f'/images/taxonomy/{kingdom_slug}.jpg',
            })
            json_write(json_article_filepath, json_article)
    for kingdom_slug in kingdoms_slugs:
        for obj in json_article['kingdoms']:
            ai_paragraph_gen(
                key = 'kingdom_desc', 
                filepath = json_article_filepath, 
                data = json_article, 
                obj = obj, 
                prompt = f'''
                    Write 1 short sentence about the following of taxonomy classification: {obj['kingdom_name']}.
                    In specific, give a definition of this classification and include examples of organisms included in this classification.
                    Reply in as few words as possible.
                    Start with the following words: The kingdom {obj['kingdom_name']} is .
                ''',
                print_prompt = True,
                regen = False,
            )

    html_article = ''
    if 0:
        html_article += f'''
            <section class="container-xl mt-48">
                <h1>The Plant Kingdom: Taxonimical Classification</h1>
                {util.text_format_1N1_html(json_article["intro"])}
                <p>To learn about Plantae kingdom and all its plants, click the link below.</p>
                <div>
                    <a href="/herbs/taxonomy/plantae.html">Plantae Kingdom</a>
                </div>
            </section>
        '''
    html_cards = ''
    for kingdom in json_article['kingdoms']:
        html_cards += f'''
            <div>
                <h3 class="mt-16">{kingdom['kingdom_name'].title()}</h3>
                <img class="mb-16" src={kingdom['kingdom_image']}>
                <p>{kingdom['kingdom_desc']}</p>
            </div>
        '''
    html_article += f'''
        <section class="container-xl mt-48">
            <h1>Taxonimical Classification of Plants</h1>
            {util.text_format_1N1_html(json_article["intro"])}
            <p>To learn about Plantae kingdom and all its plants, click the link below.</p>
            <a style="display: inline-block; background-color: #c2410c; color: #ffffff; padding: 16px 32px; margin-bottom: 16px; text-decoration: none;" href="/herbs/taxonomy/plantae.html">Visit The Plantae Kingdom</a>
            <p>For completeness, an overview of all the primary kingdoms is found below.</p>
            <p>That said, here at TerraWhisper we cover only the Plantae kingdom.</p>
            <div class="grid-4" style="column-gap: 16px">
                {html_cards}
            </div>
        </section>
    '''
    breadcrumbs_html_filepath = f'herbs/taxonomy.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    meta_html = gen_meta(html_article, json_article["lastmod"])
    head_html = head_html_generate(json_article['title'], '/style.css')
    main_html = html_article_main(meta_html, html_article, '')
    layout_html = html_article_layout(main_html, '')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            {html_article}
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    with open(html_article_filepath, 'w') as f: f.write(html)

def p_taxonomy_kingdom(kingdom_slug):
    json_article_filepath = f'database/pages/herbs/taxonomy/{kingdom_slug}.json'
    html_article_filepath = f'{website_folderpath}/herbs/taxonomy/{kingdom_slug}.html'
    # ;json
    json_article = json_read(json_article_filepath, create=True)
    json_article['title'] = f'{kingdom_slug}'
    if 'lastmod' not in json_article: json_article['lastmod'] = today()
    json_write(json_article_filepath, json_article)
    # intro
    divisions_slugs = [vertex['division_slug'] for vertex in vertices_divisions]
    divisions_slugs_prompt = ', '.join(divisions_slugs)
    ai_paragraph_gen(
        key = 'intro', 
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the following taxonomical rank: plantae kingdom.
            For reference this is the full taxonomy classification of a plant: kingdom, division, class, subclass, order, family, genus, specie.
            I want you to ONLY describe the plantae kingdom, don't mention the other ranks.
            Include:
            - What is the plantae kingdom (write a definition).
            - Write the following examples of divisions in the plantae kingdom: {divisions_slugs_prompt}.
        ''',
        print_prompt = True,
        regen = False,
    )
    # list
    if 'divisions' not in json_article: json_article['divisions'] = []
    for vertex_division in vertices_divisions:
        division_slug = vertex_division['division_slug']
        found = False
        for division in json_article['divisions']:
            if division_slug == division['division_slug']:
                found = True
                break
        if not found:
            json_article['divisions'].append({
                'division_slug': division_slug,
            })
    for division in json_article['divisions']:
        division_slug = division['division_slug']
        ai_paragraph_gen(
            key = 'division_desc', 
            filepath = json_article_filepath, 
            data = json_article, 
            obj = division, 
            prompt = f'''
                Write short 1 sentence that describes the following division of the taxonomical classification of plants: {division_slug}.
                Start with the following words: {division_slug.title()} .
            ''',
            print_prompt = True,
            regen = False,
        )
    # ;html
    html_article = ''
    html_article += f'<h1>The Plantae Kingdom</h1>\n'
    html_article += f'{util.text_format_1N1_html(json_article["intro"])}\n'
    for division in json_article['divisions']:
        division_slug = division['division_slug']
        division_desc = division['division_desc']
        html_article += f'<h2>{division_slug.title()}</h2>\n'
        html_article += f'<p>{division_desc}</p>\n'
        html_article += f'<p>Check all <a href="/herbs/taxonomy/{kingdom_slug}/{division_slug}.html">{division_slug.title()}</a> plants.</p>\n'
    breadcrumbs_html_filepath = f'herbs/taxonomy/{kingdom_slug}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    meta_html = gen_meta(html_article, json_article["lastmod"])
    head_html = head_html_generate(json_article['title'], '/style.css')
    main_html = html_article_main(meta_html, html_article, '')
    layout_html = html_article_layout(main_html, '')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            {layout_html}
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    print(html_article_filepath)
    try: os.mkdir('/'.join(html_article_filepath.split('/')[:-1]))
    except: pass
    with open(html_article_filepath, 'w') as f: f.write(html)

def p_taxonomy_division(vertex_division):
    division_slug = vertex_division['division_slug']
    kingdom_slug = 'plantae'
    json_article_filepath = f'database/pages/herbs/taxonomy/{kingdom_slug}/{division_slug}.json'
    html_article_filepath = f'{website_folderpath}/herbs/taxonomy/{kingdom_slug}/{division_slug}.html'
    # ;json
    json_article = json_read(json_article_filepath, create=True)
    json_article['title'] = f'{division_slug}'
    if 'lastmod' not in json_article: json_article['lastmod'] = today()
    json_write(json_article_filepath, json_article)
    # intro
    classes_slugs = [vertex['class_slug'] for vertex in vertices_classes]
    classes_slugs_prompt = ', '.join(classes_slugs[:3])
    ai_paragraph_gen(
        key = 'intro', 
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the following taxonomical rank of plants: {division_slug}.
            For reference this is the full taxonomy classification of a plant: kingdom, division, class, subclass, order, family, genus, specie.
            I want you only to descrive the rank division {division_slug}, don't mention the others.
            Include:
            - What is the {division_slug} division rank (write a definition).
            - Write the following examples of divisions: {classes_slugs_prompt}.
        ''',
        print_prompt = True,
        regen = False,
    )
    if 'classes' not in json_article: json_article['classes'] = []
    # json_article['classes'] = [] # REGEN
    classes_slugs = [edge['vertex_1'] for edge in edges_classes_divisions if edge['vertex_2'] == division_slug]
    for class_slug in classes_slugs:
        found = False
        for _class in json_article['classes']:
            if class_slug == _class['class_slug']:
                found = True
                break
        if not found:
            json_article['classes'].append({
                'class_slug': class_slug,
            })
            json_write(json_article_filepath, json_article)
    for obj in json_article['classes']:
        class_slug = obj['class_slug']
        ai_paragraph_gen(
            key = 'class_desc', 
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write short 1 sentence that describes the following class of the taxonomical classification of plants: {class_slug}.
                Start with the following words: {class_slug.title()} .
            ''',
            print_prompt = True,
            regen = False,
        )
    # ;html
    html_article = ''
    html_article += f'<h1>The {division_slug.title()} Division</h1>\n'
    html_article += f'{util.text_format_1N1_html(json_article["intro"])}\n'
    for obj in json_article['classes']:
        class_slug = obj['class_slug']
        class_desc = obj['class_desc']
        html_article += f'<h2>{class_slug.title()}</h2>\n'
        html_article += f'<p>{class_desc}</p>\n'
        html_article += f'<p>Check all <a href="/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}.html">{class_slug.title()}</a> plants.</p>\n'
    breadcrumbs_html_filepath = f'herbs/taxonomy/{kingdom_slug}/{division_slug}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    meta_html = gen_meta(html_article, json_article["lastmod"])
    head_html = head_html_generate(json_article['title'], '/style.css')
    main_html = html_article_main(meta_html, html_article, '')
    layout_html = html_article_layout(main_html, '')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            {layout_html}
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    try: os.mkdir('/'.join(html_article_filepath.split('/')[:-1]))
    except: pass
    with open(html_article_filepath, 'w') as f: f.write(html)

def p_taxonomy_class(vertex_class):
    class_slug = vertex_class['class_slug']
    division_slug = [edge['vertex_2'] for edge in edges_classes_divisions if edge['vertex_1'] == class_slug][0]
    kingdom_slug = 'plantae'
    json_article_filepath = f'database/pages/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}.json'
    html_article_filepath = f'{website_folderpath}/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}.html'
    # ;json
    json_article = json_read(json_article_filepath, create=True)
    json_article['title'] = f'{class_slug}'
    if 'lastmod' not in json_article: json_article['lastmod'] = today()
    json_write(json_article_filepath, json_article)
    # intro
    subclasses_slugs = [vertex['subclass_slug'] for vertex in vertices_subclasses]
    subclasses_slugs_prompt = ', '.join(subclasses_slugs[:3])
    ai_paragraph_gen(
        key = 'intro', 
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the following taxonomical rank of plants: {class_slug}.
            For reference this is the full taxonomy classification of a plant: kingdom, division, class, subclass, order, family, genus, specie.
            I want you only to describe the rank {class_slug}, don't mention the others.
            Include:
            - What is the {class_slug} rank (write a definition).
            - Write the following examples of divisions: {subclasses_slugs_prompt}.
        ''',
        print_prompt = True,
        regen = False,
    )
    if 'subclasses' not in json_article: json_article['subclasses'] = []
    # json_article['subclasses'] = [] # REGEN
    subclasses_slugs = [edge['vertex_1'] for edge in edges_subclasses_classes if edge['vertex_2'] == class_slug]
    for subclass_slug in subclasses_slugs:
        found = False
        for subclass in json_article['subclasses']:
            if subclass_slug == subclass['subclass_slug']:
                found = True
                break
        if not found:
            json_article['subclasses'].append({
                'subclass_slug': subclass_slug,
            })
            json_write(json_article_filepath, json_article)
    for obj in json_article['subclasses']:
        subclass_slug = obj['subclass_slug']
        ai_paragraph_gen(
            key = 'subclass_desc', 
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write short 1 sentence that describes the following subclass of the taxonomical classification of plants: {subclass_slug}.
                Start with the following words: {subclass_slug.title()} .
            ''',
            print_prompt = True,
            regen = False,
        )
    # ;html
    html_article = ''
    html_article += f'<h1>The {class_slug.title()} Class</h1>\n'
    html_article += f'{util.text_format_1N1_html(json_article["intro"])}\n'
    for obj in json_article['subclasses']:
        subclass_slug = obj['subclass_slug']
        subclass_desc = obj['subclass_desc']
        html_article += f'<h2>{subclass_slug.title()}</h2>\n'
        html_article += f'<p>{subclass_desc}</p>\n'
        html_article += f'<p>Check all <a href="/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}.html">{subclass_slug.title()}</a> plants.</p>\n'
    breadcrumbs_html_filepath = f'herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    meta_html = gen_meta(html_article, json_article["lastmod"])
    head_html = head_html_generate(json_article['title'], '/style.css')
    main_html = html_article_main(meta_html, html_article, '')
    layout_html = html_article_layout(main_html, '')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            {layout_html}
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    try: os.mkdir('/'.join(html_article_filepath.split('/')[:-1]))
    except: pass
    with open(html_article_filepath, 'w') as f: f.write(html)

def p_taxonomy_subclass(vertex_subclass):
    subclass_slug = vertex_subclass['subclass_slug']
    class_slug = [edge['vertex_2'] for edge in edges_subclasses_classes if edge['vertex_1'] == subclass_slug][0]
    division_slug = [edge['vertex_2'] for edge in edges_classes_divisions if edge['vertex_1'] == class_slug][0]
    kingdom_slug = 'plantae'
    json_article_filepath = f'database/pages/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}.json'
    html_article_filepath = f'{website_folderpath}/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}.html'
    # ;json
    json_article = json_read(json_article_filepath, create=True)
    json_article['title'] = f'{subclass_slug}'
    if 'lastmod' not in json_article: json_article['lastmod'] = today()
    json_write(json_article_filepath, json_article)
    # intro
    orders_slugs = [vertex['order_slug'] for vertex in vertices_orders]
    orders_slugs_prompt = ', '.join(orders_slugs[:3])
    ai_paragraph_gen(
        key = 'intro', 
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the following taxonomical rank of plants: {subclass_slug}.
            For reference this is the full taxonomy classification of a plant: kingdom, division, class, subclass, order, family, genus, specie.
            I want you only to describe the rank {subclass_slug}, don't mention the others.
            Include:
            - What is the {subclass_slug} rank (write a definition).
            - Write the following examples of orders: {orders_slugs_prompt}.
        ''',
        print_prompt = True,
        regen = False,
    )
    if 'orders' not in json_article: json_article['orders'] = []
    # json_article['orders'] = [] # REGEN
    orders_slugs = [edge['vertex_1'] for edge in edges_orders_subclasses if edge['vertex_2'] == subclass_slug]
    for order_slug in orders_slugs:
        found = False
        for order in json_article['orders']:
            if order_slug == order['order_slug']:
                found = True
                break
        if not found:
            json_article['orders'].append({
                'order_slug': order_slug,
            })
            json_write(json_article_filepath, json_article)
    for obj in json_article['orders']:
        order_slug = obj['order_slug']
        ai_paragraph_gen(
            key = 'order_desc', 
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write short 1 sentence that describes the following order of the taxonomical classification of plants: {order_slug}.
                Start with the following words: {order_slug.title()} .
            ''',
            print_prompt = True,
            regen = False,
        )
    # ;html
    html_article = ''
    html_article += f'<h1>The {subclass_slug.title()} Subclass</h1>\n'
    html_article += f'{util.text_format_1N1_html(json_article["intro"])}\n'
    for obj in json_article['orders']:
        order_slug = obj['order_slug']
        order_desc = obj['order_desc']
        html_article += f'<h2>{order_slug.title()}</h2>\n'
        html_article += f'<p>{order_desc}</p>\n'
        html_article += f'<p>Check all <a href="/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}/{order_slug}.html">{order_slug.title()}</a> plants.</p>\n'
    breadcrumbs_html_filepath = f'herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    meta_html = gen_meta(html_article, json_article["lastmod"])
    head_html = head_html_generate(json_article['title'], '/style.css')
    main_html = html_article_main(meta_html, html_article, '')
    layout_html = html_article_layout(main_html, '')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            {layout_html}
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    try: os.mkdir('/'.join(html_article_filepath.split('/')[:-1]))
    except: pass
    with open(html_article_filepath, 'w') as f: f.write(html)

def p_taxonomy_order(vertex_order):
    order_slug = vertex_order['order_slug']
    subclass_slug = [edge['vertex_2'] for edge in edges_orders_subclasses if edge['vertex_1'] == order_slug][0]
    class_slug = [edge['vertex_2'] for edge in edges_subclasses_classes if edge['vertex_1'] == subclass_slug][0]
    division_slug = [edge['vertex_2'] for edge in edges_classes_divisions if edge['vertex_1'] == class_slug][0]
    kingdom_slug = 'plantae'
    json_article_filepath = f'database/pages/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}/{order_slug}.json'
    html_article_filepath = f'{website_folderpath}/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}/{order_slug}.html'
    # ;json
    json_article = json_read(json_article_filepath, create=True)
    json_article['title'] = f'{order_slug}'
    if 'lastmod' not in json_article: json_article['lastmod'] = today()
    json_write(json_article_filepath, json_article)
    # intro
    families_slugs = [vertex['family_slug'] for vertex in vertices_families]
    families_slugs_prompt = ', '.join(families_slugs[:3])
    ai_paragraph_gen(
        key = 'intro', 
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the following taxonomical rank of plants: {order_slug}.
            For reference this is the full taxonomy classification of a plant: kingdom, division, class, subclass, order, family, genus, specie.
            I want you only to describe the rank {order_slug}, don't mention the others.
            Include:
            - What is the {order_slug} rank (write a definition).
            - Write the following examples of families: {families_slugs_prompt}.
        ''',
        print_prompt = True,
        regen = False,
    )
    if 'families' not in json_article: json_article['families'] = []
    # json_article['families'] = [] # REGEN
    families_slugs = [edge['vertex_1'] for edge in edges_families_orders if edge['vertex_2'] == order_slug]
    for family_slug in families_slugs:
        found = False
        for family in json_article['families']:
            if family_slug == family['family_slug']:
                found = True
                break
        if not found:
            json_article['families'].append({
                'family_slug': family_slug,
            })
            json_write(json_article_filepath, json_article)
    for obj in json_article['families']:
        family_slug = obj['family_slug']
        ai_paragraph_gen(
            key = 'family_desc', 
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write short 1 sentence that describes the following family of the taxonomical classification of plants: {family_slug}.
                Start with the following words: {family_slug.title()} .
            ''',
            print_prompt = True,
            regen = False,
        )
    # ;html
    html_article = ''
    html_article += f'<h1>The {order_slug.title()} Orders</h1>\n'
    html_article += f'{util.text_format_1N1_html(json_article["intro"])}\n'
    for obj in json_article['families']:
        family_slug = obj['family_slug']
        family_desc = obj['family_desc']
        html_article += f'<h2>{family_slug.title()}</h2>\n'
        html_article += f'<p>{family_desc}</p>\n'
        html_article += f'<p>Check all <a href="/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}/{order_slug}/{family_slug}.html">{family_slug.title()}</a> plants.</p>\n'
    breadcrumbs_html_filepath = f'herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}/{order_slug}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    meta_html = gen_meta(html_article, json_article["lastmod"])
    head_html = head_html_generate(json_article['title'], '/style.css')
    main_html = html_article_main(meta_html, html_article, '')
    layout_html = html_article_layout(main_html, '')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            {layout_html}
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    try: os.mkdir('/'.join(html_article_filepath.split('/')[:-1]))
    except: pass
    with open(html_article_filepath, 'w') as f: f.write(html)

def p_taxonomy_family(vertex_family):
    family_slug = vertex_family['family_slug']
    order_slug = [edge['vertex_2'] for edge in edges_families_orders if edge['vertex_1'] == family_slug][0]
    subclass_slug = [edge['vertex_2'] for edge in edges_orders_subclasses if edge['vertex_1'] == order_slug][0]
    class_slug = [edge['vertex_2'] for edge in edges_subclasses_classes if edge['vertex_1'] == subclass_slug][0]
    division_slug = [edge['vertex_2'] for edge in edges_classes_divisions if edge['vertex_1'] == class_slug][0]
    kingdom_slug = 'plantae'
    json_article_filepath = f'database/pages/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}/{order_slug}/{family_slug}.json'
    html_article_filepath = f'{website_folderpath}/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}/{order_slug}/{family_slug}.html'
    json_article = json_read(json_article_filepath, create=True)
    json_article['title'] = f'{family_slug}'
    if 'lastmod' not in json_article: json_article['lastmod'] = today()
    json_write(json_article_filepath, json_article)
    if 'plants' not in json_article: json_article['plants'] = []
    json_article['plants'] = []
    vertices_plants_filtered = [vertex for vertex in vertices_plants if vertex['plant_family'] == family_slug]
    for i, vertex_plant in enumerate(vertices_plants_filtered):
        print(f'{i}/{len(vertices_plants_filtered)}')
        found = False
        for json_plant in json_article['plants']:
            if vertex_plant['plant_slug'] == json_plant['plant_slug']:
                found = True
                break
        if not found:
            json_article['plants'].append({
                'plant_slug': vertex_plant['plant_slug'],
                'plant_name_scientific': vertex_plant['plant_name_scientific'],
                'plant_family': vertex_plant['plant_family'],
                'plant_genus': vertex_plant['plant_genus'],
            })
    html_article = ''
    html_article += f'<h2>Plants</h2>\n'
    html_article += f'<ul>\n'
    for plant in json_article['plants']:
        plant_slug = plant['plant_slug']
        html_article += f'<li><a href="/herbs/{plant_slug}.html">{plant_name_scientific}</a></li>\n'
    html_article += f'</ul>\n'
    breadcrumbs_html_filepath = f'herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}/{order_slug}/{family_slug}.html'
    breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
    meta_html = gen_meta(html_article, json_article["lastmod"])
    head_html = head_html_generate(json_article['title'], '/style.css')
    main_html = html_article_main(meta_html, html_article, '')
    layout_html = html_article_layout(main_html, '')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            {breadcrumbs_html}
            {layout_html}
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    print(html_article_filepath)
    try: os.mkdir('/'.join(html_article_filepath.split('/')[:-1]))
    except: pass
    with open(html_article_filepath, 'w') as f: f.write(html)

# TODO: in the intro include the number of plants, calculated with len(families[i]['plants'])
def p_taxonomy_families():
    # this function is implemented different from others in taxonomy because there are a lot of plants to process
    # don't change it fundamentally, you'll regret it
    # make it paginated
    families = []
    for i, vertex_plant in enumerate(vertices_plants):
        print(f'{i}/{len(vertices_plants)}')
        found = False
        for family in families:
            if family['family_slug'] == vertex_plant['plant_family']:
                family['plants'].append(vertex_plant)
                found = True
                break
        if not found:
            families.append({
                'family_slug': vertex_plant['plant_family'],
                'plants': [vertex_plant],
            })
    for family in families:
        family_slug = family['family_slug']
        order_slug = [edge['vertex_2'] for edge in edges_families_orders if edge['vertex_1'] == family_slug][0]
        subclass_slug = [edge['vertex_2'] for edge in edges_orders_subclasses if edge['vertex_1'] == order_slug][0]
        class_slug = [edge['vertex_2'] for edge in edges_subclasses_classes if edge['vertex_1'] == subclass_slug][0]
        division_slug = [edge['vertex_2'] for edge in edges_classes_divisions if edge['vertex_1'] == class_slug][0]
        kingdom_slug = 'plantae'
        json_article_filepath = f'database/pages/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}/{order_slug}/{family_slug}.json'
        html_article_filepath = f'{website_folderpath}/herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}/{order_slug}/{family_slug}.html'
        json_article = json_read(json_article_filepath, create=True)
        json_article['title'] = f'{family_slug}'
        if 'lastmod' not in json_article: json_article['lastmod'] = today()
        json_write(json_article_filepath, json_article)
        # ;json
        # intro
        ai_paragraph_gen(
            key = 'intro', 
            filepath = json_article_filepath, 
            data = json_article, 
            obj = json_article, 
            prompt = f'''
                Write a short 4-sentence paragraph about the following taxonomical rank of plants: {family_slug}.
                For reference this is the full taxonomy classification of a plant: kingdom, division, class, subclass, order, family, genus, specie.
                I want you only to describe the rank {family_slug}, don't mention the others.
                Include:
                - What is the {family_slug} rank (write a definition).
            ''',
            print_prompt = True,
            regen = False,
        )
        if 'plants' not in json_article: json_article['plants'] = []
        # json_article['plants'] = [] # REGEN
        json_article['plants'] = family['plants']
        # ;html
        html_article = ''
        html_article += f'<h1>The {family_slug.title()} Family</h1>\n'
        html_article += f'{util.text_format_1N1_html(json_article["intro"])}\n'
        html_article += f'<h2>Plants</h2>\n'
        html_article += f'<ul>\n'
        for plant in json_article['plants']:
            plant_slug = plant['plant_slug']
            plant_name_scientific = plant['plant_name_scientific']
            if os.path.exists(f"{website_folderpath}/herbs/{plant_slug}.html"):
                html_article += f'<li><a href="/herbs/{plant_slug}.html">{plant_name_scientific}</a></li>\n'
            else:
                html_article += f'<li>{plant_name_scientific}</li>\n'
        html_article += f'</ul>\n'
        breadcrumbs_html_filepath = f'herbs/taxonomy/{kingdom_slug}/{division_slug}/{class_slug}/{subclass_slug}/{order_slug}/{family_slug}.html'
        breadcrumbs_html = breadcrumbs_gen(breadcrumbs_html_filepath)
        meta_html = gen_meta(html_article, json_article["lastmod"])
        head_html = head_html_generate(json_article['title'], '/style.css')
        main_html = html_article_main(meta_html, html_article, '')
        layout_html = html_article_layout(main_html, '')
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                {breadcrumbs_html}
                {layout_html}
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        try: os.mkdir('/'.join(html_article_filepath.split('/')[:-1]))
        except: pass
        with open(html_article_filepath, 'w') as f: f.write(html)

shutil.copy2('style.css', f'{website_folderpath}/style.css')
shutil.copy2('style-article.css', f'{website_folderpath}/style-article.css')


if 0:
    # ;guides
    page_guides()
    page_lead_magnet_1()
    page_lead_magnet_1_congratulation()
    page_lead_magnet_1_download()
    p_guides_infusion_checklist()

if 0:
    p_taxonomy()
    p_taxonomy_kingdom(kingdom_slug='plantae')
    for vertex_division in vertices_divisions:
        p_taxonomy_division(vertex_division)
    for vertex_class in vertices_classes:
        p_taxonomy_class(vertex_class)
    for vertex_subclass in vertices_subclasses:
        p_taxonomy_subclass(vertex_subclass)
    for vertex_order in vertices_orders:
        p_taxonomy_order(vertex_order)
    p_taxonomy_families()

if 1:
    # ;herbs
    a_herbs_popular()
    a_herbs_wcvp()
    quit()

if 0:
    p_herbs()
    p_herbs_popular()
    p_herbs_actions()
    actions = get_category_action()
    for action in actions:
        p_herbs_action_var(action['name'])

if 0:
    # NOTE: gen images first (image_generator.py) -> then article (or error)
    equipments_slugs = os.listdir(f'{vault}/amazon/json')
    for equipment_slug in equipments_slugs:
        a_equipment(equipment_slug)
    p_equipments(equipments_slugs)

if 0:
    # ;preparations
    a_preparations_teas_var()
    p_preparations_teas()
    p_preparations()

if 1:
    # remedies -> ailments -> preparations
    articles_preparations('teas')
    quit()
    articles_preparations('tinctures')
    articles_preparations('creams')
    articles_preparations('essential-oils')

if 0:
    page_products()

if 0:
    articles_ailments_2()

    page_remedies()
    page_systems()


    page_privacy_policy()
    page_cookie_policy()
    sitemap_2.sitemap_all()

    page_contacts()
    page_about_2()
    page_home()
