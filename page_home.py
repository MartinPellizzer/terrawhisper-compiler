import os
import random

from PIL import Image, ImageFont, ImageDraw

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read
from oliark import img_resize

import g
import lib_plants
import components

import shutil

def herb_to_html_card(herb_data):
    herb_name_scientific = herb_data['herb_name_scientific']
    herb_slug = herb_data['herb_slug']
    herb_url = f'/herbs/{herb_slug}.html'
    src = f'/images/ailments/herbs/{herb_slug}.jpg'
    alt = f'{herb_name_scientific}'.lower()
    filepath_in = f'{g.VAULT}/terrawhisper/images/realistic/herbs/1x1/{herb_slug}.jpg'
    filepath_out = f'{g.WEBSITE_FOLDERPATH}/images/herbs/{herb_slug}.jpg'
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

def page_home_gen():
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
        html_filepath = f'{g.WEBSITE_FOLDERPATH}/{url}.html'
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
        html_filepath = f'{g.WEBSITE_FOLDERPATH}/{url}.html'
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
        html_filepath = f'{g.WEBSITE_FOLDERPATH}/{url}.html'
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
        html_filepath = f'{g.WEBSITE_FOLDERPATH}/{url}.html'
        data = json_read(json_filepath)
        image_url = data['intro_image_src']
        title = data['title'].title()
        essential_oils_blocks_data.append({
            'href': f'/{url}.html',
            'url': f'{image_url}',
            'title': f'{title}',
        })

    herbs = lib_plants.teas_popular_get()
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

    
    html_social = components.social_html()
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
                    {html_social}
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

    html_hero = f'''
        <section style="background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(/images-static/medicinal-plants.jpg); background-size: cover; background-position: center;">
            <div style="padding-top: 192px; padding-bottom: 192px; text-align: center;" class="container-lg">
                <h1 style="font-size: 64px; color: #ffffff; text-align: center;">Use Medicinal Plants to Improve Your Health</h1>
                <a style="text-align: center;" class="button-white" href="/herbs.html">BROWSE HEALING HERBS</a>
            </div>
        </section>
    '''

    html_business_definition = f'''
        <section style="">
            <div style="padding-top: 64px; padding-bottom: 64px; text-align: center;" class="container-md">
                <h2 style="font-size: 48px; text-align: center;">Who Is TerraWhisper?</h1>
                <p>TerraWhisper is an online encyclopedia of medicinal (and poisonous) plants with more than 100,000 entries. We're talking plants for every ailment you can imagine, backed up by over 2,000 scientific studies. Whether you're an herbalist, an apothecary, or a DIY witch, we've got the tools and knowledge you need. We're not perfect (far from it), but we've got the grit to keep it real, keep it raw, and keep it useful. Stick around long enough, and you might just learn something that actually works.</p>
            </div>
        </section>
    '''

    page_title = f'improve your health with medicinal plants'
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main>
                {html_hero}
                {html_business_definition}
                {section_herbs}
                {section_1}
                {section_2}
                {section_3}
                {section_4}
            </main>
            <div class="mt-64"></div>
            {components.html_footer()}
        </body>
        </html>
    '''
    html_filepath = f'{g.WEBSITE_FOLDERPATH}/index.html'
    with open(html_filepath, 'w') as f: f.write(html)


shutil.copy2('style.css', f'{g.WEBSITE_FOLDERPATH}/style.css')
page_home_gen()
