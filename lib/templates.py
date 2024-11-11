import os
import json
import random

import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

import g
import util
from lib import components

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read, json_write
from oliark import img_resize, img_resize_save
from oliark_llm import llm_reply


vault = '/home/ubuntu/vault'
ailments = csv_read_rows_to_json('systems-organs-ailments.csv', debug=True)

checkpoint_filepath = f'{vault}/stable-diffusion/checkpoints/juggernautXL_juggXIByRundiffusion.safetensors'
pipe = None

def article(title, header, breadcrumbs, meta, article, footer):
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
            {g.GOOGLE_ADSENSE_TAG}
        </head>
        <body>
            {header}
            {breadcrumbs}
            <main>
                <section class="container-md my-96">
                    {meta}
                    {article}
                </section>
            <main>
            {footer}
            {g.COOKIE_CONSENT}
        </body>
        </html>
    '''
    return html


def homepage_articles(preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')

    status_list = csv_read_rows_to_json(g.CSV_STATUS_FILEPATH)
    system_list = csv_read_rows_to_json(g.CSV_SYSTEMS_FILEPATH)
    status_system_list = csv_read_rows_to_json(g.CSV_STATUS_SYSTEMS_FILEPATH)
    preparation_list = csv_read_rows_to_json(g.CSV_PREPARATIONS_FILEPATH)
    status_preparation_list = csv_read_rows_to_json(g.CSV_STATUS_PREPARATIONS_FILEPATH)

    articles_html = ''
    for status_index, status in enumerate(status_list[:5]):
        print(f'\n>> {status_index}/{len(status_list)} - preparation: {preparation_name}')
        print(f'    >> {status}\n')

        status_exe = status['status_exe']
        status_id = status['status_id']
        status_slug = status['status_slug']
        status_name = status['status_names'].split(',')[0].strip()
        status_system = [obj for obj in status_system_list if obj['status_id'] == status_id][0]
        system = [obj for obj in system_list if obj['system_id'] == status_system['system_id']][0]
        system_id = system['system_id']
        system_slug = system['system_slug']
        system_name = system['system_name']
        status_preparations = [obj for obj in status_preparation_list if obj['status_id'] == status_id]
        status_preparations_names = [obj['preparation_name'] for obj in status_preparations]
        if preparation_slug.replace('-', ' ') not in status_preparations_names: continue

        url = f'{g.CATEGORY_REMEDIES}/{system_slug}/{status_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'website/{url}.html'
        title = f'10 best herbal {preparation_name} for {status_name}'.title()
        data = json_read(json_filepath, create=True)

        src = f'/images/preparations/herbal-{preparation_slug}-for-{status_slug}-overview.jpg'
        alt = f'herbal {preparation_slug} for {status_slug} overview'

        articles_html += f'''
            <div class="homepage-article-card mb-32">
                <a href="/{url}.html">
                    <img class="mb-16" src="{src}" alt="{alt}">
                    <h3 class="homepage-article-title">{title}</h3>
                </a>
            </div>
        '''

    html = f'''
        <section class="mt-64">
            <div class="container-xl">
                <h2 class="homepage-articles-title text-center mb-16">Featured Remedies</h2>
                <p class="text-center mb-32">Explore the most used herbal remedies with us, served to you by mother nature</p>
                <div class="homepage-articles-grid">
                    {articles_html}
                </div>
            </div>
        </section>
    '''
    return html

def homepage_section_benefits():
    url = '/images-static/benefits.png'
    opacity = 0.0
    html = f'''
        <section class="h-80v">
            <div class="h-full" style="background-image: linear-gradient(rgba(0, 0, 0, {opacity}), rgba(0, 0, 0, {opacity})), url({url}); background-position: center; background-size: cover;">
            </div>
        </section>
    '''
    return html


def homepage_section_definition():
    html = f'''
        <section id="what" class="homepage-what">
            <h2 class="homepage-what-title">TerraWhisper is a online science-based herbal remedies encyclopedia</h2>
            <div class="homepage-what-cards">
                <div class="homepage-what-card">
                    <img class="mb-24" src="/images-static/herbal-remedies.png" alt="">
                    <a href="/remedies.html" class="button">Browse Remedies</a>
                </div>
                <div class="homepage-what-card">
                    <img class="mb-24" src="/images-static/healing-herbs.png" alt="">
                    <a href="/herbs.html" class="button">Browse Herbs</a>
                </div>
            </div>
        </section>
    '''
    return html
    bg_color_emerald_900 = '#064a3b'
    url = '/images-static/benefits.png'
    bg_color_fuchsia_700 = '#a21caf'
    bg_color_purple_100 = '#f3e8ff'
    bg_color_purple_200 = '#e9d5ff'
    bg_color_purple_700 = '#7e22ce'
    bg_color_stone_100 = '#f5f5f4'
    bg_color = bg_color_emerald_900
    text_color = 'white'
    opacity = 0.0
    html = f'''
        <section class="h-1000">
            <div class="flex h-full items-center" style="background-color: {bg_color};">
                <div class="flex-1 h-full" style="background-color: rgba(255, 255, 255, 1.0);">
                    <img style="height: 100%; object-fit: contain;" class="" src="/images-static/benefits.png" alt="">
                </div>
                <div class="flex-1">
                    <div class="container-xl-half ml-48 mr-auto py-96 text-{text_color}">
                        <h2 class="text-64 font-lato-regular">Benefits of using herbal remedies</h2>
                        <p class="mb-48">Herbs are a natural, effective, and eco-friendly solution to find relief from common ailments and improve you quality of life.</p>
                        <h3 class="text-20 font-lato-bold mb-8">1. Natural and non-toxic</h3>
                        <p class="mb-24">Unlike synthetic pharmaceuticals, herbal remedies are derived directly from plants, which have been used for centuries in traditional medicine and contain bioactive compounds in their natural form, making them less likely to cause adverse reactions or interract with medications.</p>
                        <h3 class="text-20 font-lato-bold mb-8">2. Effective for common ailments</h3>
                        <p class="mb-24">Herbal remedies are perfect to heal common ailments because they naturally address the root cause, promoting holistic and sustainable relief instantly always.</p>
                        <h3 class="text-20 font-lato-bold mb-8">3. Sustainable and environmentally friendly</h3>
                        <p class="mb-24">Herbal remedies are sustainable and environmentally friendly because they promote biodiversity, reduce chemical usage, and minimize waste in ecosystems naturally.</p>
                    </div>
                </div>
            </div>
        </section>
    '''
    return html

def homepage():
    homepage_section_hero_html = f'''
        <section class="homepage-hero-section">
            <div class="homepage-hero-layout">
                <div class="flex-1">
                    <div class="homepage-hero-content-container">
                        <h1 class="homepage-hero-title">Use Medicinal Herbs to Heal Naturally</h1>
                        <p class="text-white mb-24">Learn to leverage the power of healing plants to relieve more than 300 physical, mental and spiritual health problems.</p>
                        <a href="/remedies.html" class="button-white">Discover Remedies</a>
                    </div>
                </div>
                <div class="flex-1">
                    <img class="homepage-hero-image" src="/images-static/herbal-remedies-healing-plants.png" alt="herbal remedies and healing plants">
                </div>
            </div>
        </section>
    '''

    homepage_section_benefits_html = f'''
        <section class="">
            <div class="homepage-benefits-layout">
                <div class="flex-1">
                    <img class="homepage-benefits-image" src="/images-static/benefits.png" alt="">
                </div>
                <div class="flex-1">
                    <div class="homepage-benefits-content-container">
                        <h2 class="homepage-benefits-title">Benefits of using herbal remedies</h2>
                        <p class="mb-48">Herbs are a natural, effective, and eco-friendly solution to find relief from common ailments and improve you quality of life.</p>
                        <h3 class="text-20 font-lato-bold mb-8">1. Natural and non-toxic</h3>
                        <p class="mb-24">Unlike synthetic pharmaceuticals, herbal remedies are derived directly from plants, which have been used for centuries in traditional medicine and contain bioactive compounds in their natural form, making them less likely to cause adverse reactions or interract with medications.</p>
                        <h3 class="text-20 font-lato-bold mb-8">2. Effective for common ailments</h3>
                        <p class="mb-24">Herbal remedies are perfect to heal common ailments because they naturally address the root cause, promoting holistic and sustainable relief instantly always.</p>
                        <h3 class="text-20 font-lato-bold mb-8">3. Sustainable and environmentally friendly</h3>
                        <p class="mb-24">Herbal remedies are sustainable and environmentally friendly because they promote biodiversity, reduce chemical usage, and minimize waste in ecosystems naturally.</p>
                    </div>
                </div>
            </div>
        </section>
    '''

    homepage_section_encyclopedia_intro_html = f'''
        <section class="py-96">
            <div class="container-xl">
                <h2 class="mb-24 text-center">Buy a physical copy of terrawhisper encyclopedia to support our cause</h2>
                <div class="homepage-encyclopedia-intro-layout">
                    <div class="flex-1">
                        <img style="height: 600px; object-fit: contain;" src="/images-static/encyclopedia.png">
                    </div>
                    <div class="flex-1">
                        <p>TerraWhisper is a big project.</p>
                        <p>We provide free information about herbal remedies for more than 300 common ailments, and we do that by exracting data from more than 80.000 scientific articles and papers.</p>
                        <p>This requires our project a huge amount of resources in terms of time and money. But hey, it's ok. We are on a mission and we gladly do that.</p>
                        <p>That said, if you want to sustain our cause, get a physical copy of our herbal remedies encyclopedia as a way to say "thank you" for all we done so far.</p>
                        <a class="button mt-8">Coming Soon</a>
                    </div>
                </div>
            </div>
        </section>
    '''

    homepage_section_encyclopedia_features_html = f'''
        <section class="pb-96">
            <div class="homepage-encyclopedia-features-layout">
                <h2 class="mb-24 text-center">What sets our encyclopedia apart from other books</h2>
                <div class="homepage-encyclopedia-features-items">
                    <div class="flex-1">
                        <p class="text-96 text-center">1</p>
                        <h3 class="font-lato-bold text-center">Comprehensive Coverage</h3>
                        <p class="text-center mt-16">TerraWhisper Encyclopedia cover 300+ common ailments and includes causes, symptoms, healing herbs, medicnal preparations, and precautions for each ailment discussed.</p>
                    </div>
                    <div class="flex-1">
                        <p class="text-96 text-center">2</p>
                        <h3 class="font-lato-bold text-center">Scientifically-Backed Information</h3>
                        <p class="text-center mt-16">TerraWhisper Encyclopedia uses a corpus of 80.000+ scientific articles to validate its data and includes only information confirmed by at least 3 different studies.</p>
                    </div>
                    <div class="flex-1">
                        <p class="text-96 text-center">3</p>
                        <h3 class="font-lato-bold text-center">Easy-to-Use Format</h3>
                        <p class="text-center mt-16">TerraWhisper Encyclopedia it's designed and outlined in simple and fast to scan way, all you need are 30 seconds to find the ailment you want to heal.</p>
                    </div>
                </div>
            </div>
        </section>
    '''

    homepage_section_encyclopedia_benefits_html = f'''
        <section class="pb-96">
            <div class="homepage-encyclopedia-benefits-layout">
                <h2 class="mb-24 text-center">What are the benefits of using our encyclopedia</h2>
                <div class="homepage-encyclopedia-benefits-item">
                    <div class="flex-1">
                        <img src="/images-static/health.png">
                    </div>
                    <div class='flex-1'>
                        <h3 class="font-lato-bold">Improve your health and wellness</h3>
                        <p class="mt-16">Our comprehensive herbal remedies encyclopedia provides you the knowledge you need to get rid of common ailments and boost your overall health in a natural and safe way.</p>
                    </div>
                </div>
                <div class="homepage-encyclopedia-benefits-item reverse">
                    <div class='flex-1'>
                        <h3 class="font-lato-bold">Save time and money</h3>
                        <p class="mt-16">Our strictly structured encyclopedia allows you to find what you need without spending hours seaching around the web and saves you money you have to spend in costly medications.</p>
                    </div>
                    <div class="flex-1">
                        <img src="/images-static/time.png">
                    </div>
                </div>
                <div class="homepage-encyclopedia-benefits-item">
                    <div class="flex-1">
                        <img src="/images-static/confidence.png">
                    </div>
                    <div class='flex-1'>
                        <h3 class="font-lato-bold">Gain confidence in your health choices</h3>
                        <p class="mt-16">Our encyclopedia empowers you to make informed decisions about your health, boosting your confidence and educating you in when it's appropriate to choose natural alternatives to modern medicine.</p>
                    </div>
                </div>
            </div>
        </section>
    '''

    ailment_featured_list = csv_read_rows_to_json('systems-organs-ailments-featured.csv')

    articles_html = ''
    for ailment in ailment_featured_list[:]:
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        src = f'/images/ailments/{ailment_slug}-herbal-remedies.jpg'
        alt = f'herbal remedies for {ailment_slug}'
        articles_html += f'''
            <a class="no-underline" href="/remedies/{system_slug}-system/{ailment_slug}.html">
                <div>
                    <img src="{src}" alt="{alt}">
                    <h2 class="text-24 text-black no-underline mt-0 pt-16">{ailment_name.title()}: Causes, Medicinal Herbs and Herbal Preparations</h2>
                </div>
            </a>
        '''

    homepage_section_articles_html = f'''
        <section class="container-xl pb-96">
            <h2 class="text-center">Herbal Remedies Guide</h2>
            <p class="text-center mb-48">Discover the world of herbal remedies and medicinal plants to improve you health and wellness against the most common ailments.</p>
            <div class="container-xl grid grid-3 gap-64">
                {articles_html}
            </div>
        </section>
    '''

    # ----------------------------------------------------------------------------
    # ;new
    # ----------------------------------------------------------------------------

    section_hero = f'''
        <section class="py-192 flex items-center" style="background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(/images-static/medicinal-plants-botanical-garden.jpg); background-size: cover; background-position: center;">
            <div class="container-xl">
                <div class="flex">
                    <div class="flex-1">
                    </div>
                    <div class="flex-5 text-center">
                        <h2 class="text-white pt-0 text-80 weight-400">Use Healing Herbs to Enchance Your Health</h2>
                        <p class="text-white text-24">Exploit the therapeutic power of medicinal plants and herbal remedies to find physical, mental, and spiritual relief.</p>
                    </div>
                    <div class="flex-1">
                    </div>
                </div>
            </div>
        </section>
    '''

    section_proof = f'''
        <section class="pt-48 pb-32 bg-black">
            <div class="container-xl">
                <div class="flex justify-between">
                    <div class="flex-1 text-center">
                        <p class="text-white text-18 mb-0">PLANTS REVIEWED</p>
                        <p class="text-white text-48 mb-0">207</p>
                    </div>
                    <div class="flex-1 text-center">
                        <p class="text-white text-18 mb-0">STUDIES CITED</p>
                        <p class="text-white text-48 mb-0">147</p>
                    </div>
                    <div class="flex-1">
                    </div>
                </div>
            </div>
        </section>
    '''

    section_what = f'''
        <section class="py-96">
            <div class="container-xl">
                <div class="text-center">
                    <h2>Terrawhisper is a science-based encyclopedia of healing herbs</h2>
                </div>
                <div class="flex justify-between">
                    <div class="flex-1">
                        <p class="home-what-card">Uses</p>
                    </div>
                    <div class="flex-1">
                        <p class="home-what-card">Benefits</p>
                    </div>
                    <div class="flex-1">
                        <p class="home-what-card">Properties</p>
                    </div>
                </div>
                <div class="flex justify-between">
                    <div class="flex-1">
                        <p class="home-what-card">Constituents</p>
                    </div>
                    <div class="flex-1">
                        <p class="home-what-card">Parts</p>
                    </div>
                    <div class="flex-1">
                        <p class="home-what-card">Preparations</p>
                    </div>
                </div>
                <div class="flex justify-between">
                    <div class="flex-1">
                        <p class="home-what-card">Side Effects</p>
                    </div>
                    <div class="flex-1">
                        <p class="home-what-card">Precautions</p>
                    </div>
                </div>
            </div>
        </section>
    '''
    

    herbs_popular = []
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        data = json_read(json_filepath)
        for obj in data['herbs']:
            found = False
            for herb_popular in herbs_popular:
                if obj['plant_name_scientific'] == herb_popular['plant_name_scientific']:
                    herb_popular['confidence_score'] += obj['confidence_score']
                    found = True
                    break
            if not found:
                plant_slug = obj['plant_name_scientific'].lower().strip().replace(' ', '-')
                plant_json_filepath = f'database/json/herbs/{plant_slug}.json'
                if os.path.exists(plant_json_filepath):
                    _data = json_read(plant_json_filepath)
                    title = _data['title']
                    if 'intro_desc' in _data: description = ' '.join(_data['intro_desc'].split(' ')[:24])
                    else: description = ''
                    herbs_popular.append({
                        'plant_name_scientific': obj['plant_name_scientific'],
                        'plant_slug': plant_slug,
                        'confidence_score': obj['confidence_score'],
                        'title': title,
                        'description': description,
                    })
    herbs_popular = sorted(herbs_popular, key=lambda x: x['confidence_score'], reverse=True)
    print(herbs_popular)

    section_popular = f'''
        <section class="py-96">
            <div class="container-xl flex gap-32">
                <div class="flex-4">
                    <a class="inline-block no-underline text-black" href="/herbs/{herbs_popular[0]['plant_slug']}.html">
                        <img class="object-cover mb-24" height="540" src="/images/herbs/{herbs_popular[0]['plant_slug']}.jpg" alt="">
                        <p class="home-art-cat">Herbs</p>
                        <h2 class="pt-0">{herbs_popular[0]['title']}</h2>
                        <p>In the dynamic world of business and entrepreneurship, success is not just about having a great idea or a solid business plan. It requires a combination of factors, including setting goals,...</p>
                    </a>
                </div>
                <div class="flex-3 flex flex-col gap-16">
                    <p class="text-24 font-bold upper">Recommended</p>
                    <a class="inline-block no-underline text-black" href="/herbs/{herbs_popular[1]['plant_slug']}.html">
                        <div class="flex items-center gap-16">
                            <div class="flex-1">
                                <img height="100" class="object-cover" src="/images/herbs/{herbs_popular[1]['plant_slug']}.jpg" alt="">
                            </div>
                            <div class="flex-2">
                                <p class="home-art-cat">Herbs</p>
                                <h2 class="pt-0 text-18">{herbs_popular[1]['title']}</h2>
                            </div>
                        </div>
                    </a>
                    <a class="inline-block no-underline text-black" href="/herbs/{herbs_popular[2]['plant_slug']}.html">
                        <div class="flex items-center gap-16">
                            <div class="flex-1">
                                <img height="100" class="object-cover" src="/images/herbs/{herbs_popular[2]['plant_slug']}.jpg" alt="">
                            </div>
                            <div class="flex-2">
                                <p class="home-art-cat">Herbs</p>
                                <h2 class="pt-0 text-18">{herbs_popular[2]['title']}</h2>
                            </div>
                        </div>
                    </a>
                    <a class="inline-block no-underline text-black" href="/herbs/{herbs_popular[3]['plant_slug']}.html">
                        <div class="flex items-center gap-16">
                            <div class="flex-1">
                                <img height="100" class="object-cover" src="/images/herbs/{herbs_popular[3]['plant_slug']}.jpg" alt="">
                            </div>
                            <div class="flex-2">
                                <p class="home-art-cat">Herbs</p>
                                <h2 class="pt-0 text-18">{herbs_popular[3]['title']}</h2>
                            </div>
                        </div>
                    </a>
                    <a class="inline-block no-underline text-black" href="/herbs/{herbs_popular[4]['plant_slug']}.html">
                        <div class="flex items-center gap-16">
                            <div class="flex-1">
                                <img height="100" class="object-cover" src="/images/herbs/{herbs_popular[4]['plant_slug']}.jpg" alt="">
                            </div>
                            <div class="flex-2">
                                <p class="home-art-cat">Herbs</p>
                                <h2 class="pt-0 text-18">{herbs_popular[4]['title']}</h2>
                            </div>
                        </div>
                    </a>
                    <a class="inline-block no-underline text-black" href="/herbs/{herbs_popular[5]['plant_slug']}.html">
                        <div class="flex items-center gap-16">
                            <div class="flex-1">
                                <img height="100" class="object-cover" src="/images/herbs/{herbs_popular[5]['plant_slug']}.jpg" alt="">
                            </div>
                            <div class="flex-2">
                                <p class="home-art-cat">Herbs</p>
                                <h2 class="pt-0 text-18">{herbs_popular[5]['title']}</h2>
                            </div>
                        </div>
                    </a>
                    <a class="inline-block no-underline text-black" href="/herbs/{herbs_popular[6]['plant_slug']}.html">
                        <div class="flex items-center gap-16">
                            <div class="flex-1">
                                <img height="100" class="object-cover" src="/images/herbs/{herbs_popular[6]['plant_slug']}.jpg" alt="">
                            </div>
                            <div class="flex-2">
                                <p class="home-art-cat">Herbs</p>
                                <h2 class="pt-0 text-18">{herbs_popular[6]['title']}</h2>
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        </section>
    '''

    '''
    url = f'remedies/{system_slug}-system/sore-throat'
    json_filepath = f'database/json/{url}.json'
    data = json_read(json_filepath)
    '''
    popular_ailments_for_teas = [
            ['respiratory system', 'sore throat'],
            ['nervous system', 'headache'],
            ['reproductive system', 'menstrual cramps'],
            ['immune system', 'inflammation'],
            ['digestive system', 'constipation'],
            ['digestive system', 'acid reflux'],
            ['nervous system', 'anxiety'],
            ['nervous system', 'sleep deprivation'],
            ['cardiovascular system', 'high blood pressure'],
            ['respiratory system', 'colds'],
            ['respiratory system', 'cough'],
            ['immune system', 'fever'],
    ]
    popular_teas = []
    for ailment_row in popular_ailments_for_teas:
        system_name = ailment_row[0]
        system_slug = system_name.lower().strip().replace(' ', '-')
        ailment_name = ailment_row[1]
        ailment_slug = ailment_name.lower().strip().replace(' ', '-')

        data = json_read(f'database/json/remedies/{system_slug}/{ailment_slug}/teas.json')
        title = data['title']
        intro_desc = ' '.join(data['intro_desc'].split(' ')[:24]) + '...'

        popular_teas.append({
            'ailment_name': ailment_name,
            'ailment_slug': ailment_name.lower().strip().replace(' ', '-'),
            'system': system_name.title(),
            'title': title.title(),
            'link_url': f'/remedies/{system_slug}/{ailment_slug}/teas.html',
            'image_url': f'/images/preparations/herbal-teas-for-{ailment_slug}-overview.jpg',
            'intro_desc': intro_desc,
        })
    
    section_teas = f'''
        <section class="pb-96">
            <div class="container-xl">
                <h2 class="pt-0 pb-32 text-56">Teas</h2>
                <div class="flex gap-48">
                    <div class="flex-4 flex gap-16">
                        <div class="flex-1">
                            <a class="no-underline text-black" href="{popular_teas[0]['link_url']}">
                                <img class="object-cover mb-24" height="400" src="{popular_teas[0]['image_url']}" alt="">
                                <p class="home-art-cat">{popular_teas[0]['system']}</p>
                                <h2 class="pt-0 text-24">{popular_teas[0]['title']}</h2>
                                <p class="home-paragraph-secondary">{popular_teas[0]['intro_desc']}</p>
                            </a>
                        </div>
                        <div class="flex-1">
                            <a class="no-underline text-black" href="{popular_teas[1]['link_url']}">
                                <img class="object-cover mb-24" height="400" src="{popular_teas[1]['image_url']}" alt="">
                                <p class="home-art-cat">{popular_teas[1]['system']}</p>
                                <h2 class="pt-0 text-24">{popular_teas[1]['title']}</h2>
                                <p class="home-paragraph-secondary">{popular_teas[1]['intro_desc']}</p>
                            </a>
                        </div>
                    </div>
                    <div class="flex-3">
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_teas[2]['link_url']}">
                                    <p class="home-art-cat">{popular_teas[2]['system']}</p>
                                    <h2 class="pt-0 text-18">{popular_teas[2]['title']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_teas[3]['link_url']}">
                                    <p class="home-art-cat">{popular_teas[3]['system']}</p>
                                    <h2 class="pt-0 text-18">{popular_teas[3]['title']}</h2>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_teas[4]['link_url']}">
                                    <p class="home-art-cat">{popular_teas[4]['system']}</p>
                                    <h2 class="pt-0 text-18">{popular_teas[4]['title']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_teas[5]['link_url']}">
                                    <p class="home-art-cat">{popular_teas[5]['system']}</p>
                                    <h2 class="pt-0 text-18">{popular_teas[5]['title']}</h2>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_teas[6]['link_url']}">
                                    <p class="home-art-cat">{popular_teas[6]['system']}</p>
                                    <h2 class="pt-0 text-18">{popular_teas[6]['title']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_teas[7]['link_url']}">
                                    <p class="home-art-cat">{popular_teas[7]['system']}</p>
                                    <h2 class="pt-0 text-18">{popular_teas[7]['title']}</h2>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_teas[8]['link_url']}">
                                    <p class="home-art-cat">{popular_teas[8]['system']}</p>
                                    <h2 class="pt-0 text-18">{popular_teas[8]['title']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_teas[9]['link_url']}">
                                    <p class="home-art-cat">{popular_teas[9]['system']}</p>
                                    <h2 class="pt-0 text-18">{popular_teas[9]['title']}</h2>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_teas[10]['link_url']}">
                                    <p class="home-art-cat">{popular_teas[10]['system']}</p>
                                    <h2 class="pt-0 text-18">{popular_teas[10]['title']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_teas[11]['link_url']}">
                                    <p class="home-art-cat">{popular_teas[11]['system']}</p>
                                    <h2 class="pt-0 text-18">{popular_teas[11]['title']}</h2>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            <div>
        </section>
    '''

    popular_ailments_for_tinctures = [
            ['nervous system', 'sleep deprivation'],
            ['nervous system', 'anxiety'],
            ['immune system', 'allergies'],
            ['immune system', 'inflammation'],
            ['nervous system', 'headache'],
            ['cardiovascular system', 'high blood pressure'],
            ['musculoskeletal system', 'back pain'],
    ]
    popular_tinctures = []
    for ailment_row in popular_ailments_for_tinctures:
        system_name = ailment_row[0]
        system_slug = system_name.lower().strip().replace(' ', '-')
        ailment_name = ailment_row[1]
        ailment_slug = ailment_name.lower().strip().replace(' ', '-')

        data = json_read(f'database/json/remedies/{system_slug}/{ailment_slug}/tinctures.json')
        title = data['title']
        intro_desc = ' '.join(data['intro_desc'].split(' ')[:24]) + '...'

        popular_tinctures.append({
            'ailment_name': ailment_name,
            'ailment_slug': ailment_name.lower().strip().replace(' ', '-'),
            'system': system_name.title(),
            'title': title.title(),
            'link_url': f'/remedies/{system_slug}/{ailment_slug}/tinctures.html',
            'image_url': f'/images/preparations/herbal-tinctures-for-{ailment_slug}-overview.jpg',
            'intro_desc': intro_desc,
        })
    
    section_tinctures = f'''
        <section class="pb-96">
            <div class="container-xl">
                <h2 class="pt-0 pb-32 text-56">Tinctures</h2>
                <div class="flex gap-48">
                    <div class="flex-1">
                        <a class="no-underline text-black" href="{popular_tinctures[0]['link_url']}">
                            <img class="object-cover mb-24" height="400" src="{popular_tinctures[0]['image_url']}" alt="">
                            <p class="home-art-cat">{popular_tinctures[0]['system']}</p>
                            <h2 class="pt-0 pb-8">{popular_tinctures[0]['title']}</h2>
                            <p class="home-paragraph-secondary">{popular_tinctures[0]['intro_desc']}</p>
                        </a>
                    </div>
                    <div class="flex-1">
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_tinctures[1]['link_url']}">
                                    <img class="object-cover mb-24" height="200" src="{popular_tinctures[1]['image_url']}" alt="">
                                    <p class="home-art-cat">{popular_tinctures[1]['system']}</p>
                                    <h2 class="pt-0 text-18 pb-8">{popular_tinctures[1]['title']}</h2>
                                    <p class="home-paragraph-secondary">{popular_tinctures[1]['intro_desc']}</p>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_tinctures[2]['link_url']}">
                                    <img class="object-cover mb-24" height="200" src="{popular_tinctures[2]['image_url']}" alt="">
                                    <p class="home-art-cat">{popular_tinctures[2]['system']}</p>
                                    <h2 class="pt-0 text-18 pb-8">{popular_tinctures[2]['title']}</h2>
                                    <p class="home-paragraph-secondary">{popular_tinctures[2]['intro_desc']}</p>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_tinctures[3]['link_url']}">
                                    <p class="home-art-cat">{popular_tinctures[3]['system']}</p>
                                    <h2 class="pt-0 text-18 pb-8">{popular_tinctures[3]['title']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="{popular_tinctures[4]['link_url']}">
                                    <p class="home-art-cat">{popular_tinctures[4]['system']}</p>
                                    <h2 class="pt-0 text-18 pb-8">{popular_tinctures[4]['title']}</h2>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1">
                                <a class="no-underline text-black" href="{popular_tinctures[5]['link_url']}">
                                    <p class="home-art-cat">{popular_tinctures[5]['system']}</p>
                                    <h2 class="pt-0 text-18 pb-8">{popular_tinctures[5]['title']}</h2>
                                </a>
                            </div>
                            <div class="flex-1">
                                <a class="no-underline text-black" href="{popular_tinctures[6]['link_url']}">
                                    <p class="home-art-cat">{popular_tinctures[6]['system']}</p>
                                    <h2 class="pt-0 text-18 pb-8">{popular_tinctures[6]['title']}</h2>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    '''

    section_creams = f'''
        <section class="pb-96">
            <div class="container-xl">
                <h2 class="pt-0 pb-32 text-56">Creams</h2>
                <div class="flex gap-48">
                    <div class="flex-1">
                        <div class="flex gap-16">
                            <div class="flex-1">
                                <img class="object-cover mb-24" height="400" src="/images/herbs/{herbs_popular[0]['plant_slug']}.jpg" alt="">
                                <p class="home-art-cat">Creams</p>
                                <h2 class="pt-0 text-24">Advances in predicting and measuring atmospheric conditions</h2>
                                <p class="home-paragraph-secondary">In the dynamic world of business and entrepreneurship, success is not just about having a great idea or a solid business plan. It requires a combination of factors, including setting goals,...</p>
                            </div>
                            <div class="flex-1">
                                <img class="object-cover mb-24" height="400" src="/images/herbs/{herbs_popular[0]['plant_slug']}.jpg" alt="">
                                <p class="home-art-cat">Creams</p>
                                <h2 class="pt-0 text-24">Advances in predicting and measuring atmospheric conditions</h2>
                                <p class="home-paragraph-secondary">In the dynamic world of business and entrepreneurship, success is not just about having a great idea or a solid business plan. It requires a combination of factors, including setting goals,...</p>
                            </div>
                        </div>
                    </div>
                    <div class="flex-1">
                        <div class="flex gap-48">
                            <div class="flex-1">
                                <img class="object-cover mb-24" height="200" src="/images/herbs/{herbs_popular[0]['plant_slug']}.jpg" alt="">
                                <p class="home-art-cat">Creams</p>
                                <h2 class="pt-0 text-18">Advances in predicting and measuring atmospheric conditions</h2>
                                <img class="object-cover mb-24" height="200" src="/images/herbs/{herbs_popular[0]['plant_slug']}.jpg" alt="">
                                <p class="home-art-cat">Creams</p>
                                <h2 class="pt-0 text-18">Advances in predicting and measuring atmospheric conditions</h2>
                            </div>
                            <div class="flex-1">
                                <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                    <p class="home-art-cat">Creams</p>
                                    <h2 class="pt-0 text-18 pb-16">Advances in predicting and measuring atmospheric conditions</h2>
                                </div>
                                <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                    <p class="home-art-cat">Creams</p>
                                    <h2 class="pt-0 text-18 pb-16">Advances in predicting and measuring atmospheric conditions</h2>
                                </div>
                                <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                    <p class="home-art-cat">Creams</p>
                                    <h2 class="pt-0 text-18 pb-16">Advances in predicting and measuring atmospheric conditions</h2>
                                </div>
                                <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                    <p class="home-art-cat">Creams</p>
                                    <h2 class="pt-0 text-18 pb-16">Advances in predicting and measuring atmospheric conditions</h2>
                                </div>
                                <div class="flex-1">
                                    <p class="home-art-cat">Creams</p>
                                    <h2 class="pt-0 text-18 pb-16">Advances in predicting and measuring atmospheric conditions</h2>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    '''

    section_digestive_system = f'''
        <section class="pb-96">
            <div class="container-xl">
                <h2 class="pt-0 pb-32 text-48">Top Herbs for Digestive System</h2>
                <div class="flex gap-48">
                    <div class="flex-4 flex gap-16">
                        <div class="flex-1">
                            <a class="no-underline text-black" href="/herbs/{herbs_popular[7]['plant_slug']}.html">
                                <img class="object-cover mb-24" height="400" src="/images/herbs/{herbs_popular[7]['plant_slug']}.jpg" alt="">
                                <p class="home-art-cat">herbs</p>
                                <h2 class="pt-0 text-24">{herbs_popular[7]['plant_name_scientific']}</h2>
                                <p class="home-paragraph-secondary">{herbs_popular[7]['description']}</p>
                            </a>
                        </div>
                        <div class="flex-1">
                            <a class="no-underline text-black" href="/herbs/{herbs_popular[8]['plant_slug']}.html">
                                <img class="object-cover mb-24" height="400" src="/images/herbs/{herbs_popular[8]['plant_slug']}.jpg" alt="">
                                <p class="home-art-cat">herbs</p>
                                <h2 class="pt-0 text-24">{herbs_popular[8]['plant_name_scientific']}</h2>
                                <p class="home-paragraph-secondary">{herbs_popular[8]['description']}</p>
                            </a>
                        </div>
                    </div>
                    <div class="flex-3">
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[9]['plant_slug']}.html">
                                    <p class="home-art-cat">herbs</p>
                                    <h2 class="pt-0 text-18">{herbs_popular[9]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[10]['plant_slug']}.html">
                                    <p class="home-art-cat">herbs</p>
                                    <h2 class="pt-0 text-18">{herbs_popular[10]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[11]['plant_slug']}.html">
                                    <p class="home-art-cat">herbs</p>
                                    <h2 class="pt-0 text-18">{herbs_popular[11]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[12]['plant_slug']}.html">
                                    <p class="home-art-cat">herbs</p>
                                    <h2 class="pt-0 text-18">{herbs_popular[12]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[13]['plant_slug']}.html">
                                    <p class="home-art-cat">herbs</p>
                                    <h2 class="pt-0 text-18">{herbs_popular[13]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[14]['plant_slug']}.html">
                                    <p class="home-art-cat">herbs</p>
                                    <h2 class="pt-0 text-18">{herbs_popular[14]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[15]['plant_slug']}.html">
                                    <p class="home-art-cat">herbs</p>
                                    <h2 class="pt-0 text-18">{herbs_popular[15]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[16]['plant_slug']}.html">
                                    <p class="home-art-cat">herbs</p>
                                    <h2 class="pt-0 text-18">{herbs_popular[16]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[17]['plant_slug']}.html">
                                    <p class="home-art-cat">herbs</p>
                                    <h2 class="pt-0 text-18">{herbs_popular[17]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[18]['plant_slug']}.html">
                                    <p class="home-art-cat">herbs</p>
                                    <h2 class="pt-0 text-18">{herbs_popular[18]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            <div>
        </section>
    '''

    section_musculoskeletal_system = f'''
        <section class="pb-96">
            <div class="container-xl">
                <h2 class="pt-0 pb-32 text-48">Top Herbs for Musculoskeletal Sysstem</h2>
                <div class="flex gap-48">
                    <div class="flex-1">
                        <a class="no-underline text-black" href="/herbs/{herbs_popular[19]['plant_slug']}.html">
                            <img class="object-cover mb-24" height="400" src="/images/herbs/{herbs_popular[19]['plant_slug']}.jpg" alt="">
                            <h2 class="pt-0 text-24">{herbs_popular[19]['plant_name_scientific']}</h2>
                            <p class="home-paragraph-secondary">{herbs_popular[19]['description']}</p>
                        </a>
                    </div>
                    <div class="flex-1">
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[20]['plant_slug']}.html">
                                    <img class="object-cover mb-24" height="200" src="/images/herbs/{herbs_popular[20]['plant_slug']}.jpg" alt="">
                                    <h2 class="pt-0 text-24">{herbs_popular[20]['plant_name_scientific']}</h2>
                                    <p class="home-paragraph-secondary">{herbs_popular[20]['description']}</p>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[21]['plant_slug']}.html">
                                    <img class="object-cover mb-24" height="200" src="/images/herbs/{herbs_popular[21]['plant_slug']}.jpg" alt="">
                                    <h2 class="pt-0 text-24">{herbs_popular[21]['plant_name_scientific']}</h2>
                                    <p class="home-paragraph-secondary">{herbs_popular[21]['description']}</p>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[22]['plant_slug']}.html">
                                    <h2 class="pt-0 text-18">{herbs_popular[22]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                            <div class="flex-1 border-0 border-b border-solid border-black mb-16">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[23]['plant_slug']}.html">
                                    <h2 class="pt-0 text-18">{herbs_popular[23]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                        </div>
                        <div class="flex gap-16">
                            <div class="flex-1">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[24]['plant_slug']}.html">
                                    <h2 class="pt-0 text-18">{herbs_popular[24]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                            <div class="flex-1">
                                <a class="no-underline text-black" href="/herbs/{herbs_popular[25]['plant_slug']}.html">
                                    <h2 class="pt-0 text-18">{herbs_popular[25]['plant_name_scientific']}</h2>
                                </a>
                            </div>
                        </div>
                    </div>
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
            <meta name="author" content="{g.AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>Use Medicinal Herbs to Heal Naturally</title>
            {g.GOOGLE_TAG}
            {g.GOOGLE_ADSENSE_TAG}
        </head>
        <body>
            {components.header()}
            <main>
                {section_hero}
                {section_popular}
                {section_teas}
                {section_tinctures}
                {section_creams}
            </main>
            <div class="mt-64"></div>
            {components.footer()}
            {g.COOKIE_CONSENT} 
        </body>
        </html>
    '''

    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{g.AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>Use Medicinal Herbs to Heal Naturally</title>
            {g.GOOGLE_TAG}
            {g.GOOGLE_ADSENSE_TAG}
        </head>
        <body>
            {components.header()}
            <main>
                {section_hero}
                {section_proof}
                {section_what}
                {section_popular}
                {section_digestive_system}
                {section_musculoskeletal_system}
                {section_creams}
            </main>
            <div class="mt-64"></div>
            {components.footer()}
            {g.COOKIE_CONSENT} 
        </body>
        </html>
    '''
    return html
                #{section_articles}

def about_page():
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{g.AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>Use Medicinal Herbs to Heal Naturally</title>
            {g.GOOGLE_TAG}
            {g.GOOGLE_ADSENSE_TAG}
        </head>
        <body>
            {components.header()}
            <main>
                <section class="container-md mt-96">
                    <h1>Get To Know TerraWhisper</h1>
                    <img class="mb-16" src="/images-static/about-us.png" alt="terrawhisper botanical garden in italy">
                    <p>Welcome to TerrraWhisper, your science-based source of information regarding medicinal plants and herbal remedies. Our goal is to give you the most accurate, reliable, and easily accessible information on the world of healing herbs. We truly believe that natural health and wellness are the path to a happy and balanced life, and we do all we can to help you achieve your pick health.</p>
                    <h2 class="text-32">Our Mission</h2>
                    <p>TerraWhisper's mission is to empower you with knowledge and confidence to make informed decisions about your health. Our goal is to create a comprehensive and trusted resource for herbal remedies that's accessible to everyone. We believer medicinal herbs have the power to transform lives and we are committed to sharing this knowledge with the world.
                    </p>
                    <h2 class="text-32">Who's Behind TerraWhisper</h2>
                    <p>My name is Martin Pellizzer, nice to meet you. I'm a former computer scientist turning herbalist. Sounds strange? Here's why... I've spent most of my years post-graduation developing software for micro-biological analysis, to manily study animal tissues, bacteria, and (last but not least) plants. In all those years of observing and studing plants in particular, I learned how much bioactive constituents these plants contain that can be used for serious medical applications. I myself was experiencing serious health problems in those years, problems that were not lifethreatening but serious enough to completely ruin my days, wellness, and happiness. That's when I decided to give healing herbs a serious try and I confess that was the best decision of my life. Since then, I'm devoting myself in leveraging the power of herbalism to help those who may be in the same situation I once was. This is how TerraWhisper was born, where myself and a team of commited editors are building the best source of information for natural healing with herbal medicine, following a scientifically-base approach.
                    </p>
                    <h2 class="text-32">How We Make Sure Our Information Is "Science Approved"</h2>
                    <p>
                        If a piece of information is not presented in a scientific article, study, or paper, we don't include it in our encyclopedia. Actually, we go an extra mile and we accept only data that has is validated by more than one scientific study (usually 3 studies or more). For example, if we can't find different studies proving (with actual data and well-conducter tests) that the plant Achillea millefolium is good to stop bleeding, we don't promote this health benefit in our encyclopedia, no matter how many "mom-and-pop" websites or "influencer" blogs write about it out there in the wild web. We believe there are more than enough people who spread misinformation about healing herbs because of copying each other content without validating it, and we don't plan to be another one of them. We have a corpus of more than 80.000 scientific studies to take our information from, and this corpus is well curated from reputable scientific journals we found from directory such us PubMed, Google Scholar, and many other. Our motto is "If it ain't scientifically-proven, it ain't for us."
                    </p>
                </section>
            </main>
            <div class="mt-64"></div>
            {components.footer()}
            {g.COOKIE_CONSENT}
        </body>
        </html>
    '''
    return html

def contact_page():
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{g.AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>Use Medicinal Herbs to Heal Naturally</title>
            {g.GOOGLE_TAG}
            {g.GOOGLE_ADSENSE_TAG}
        </head>
        <body>
            {components.header()}
            <main>
                <section class="container-md mt-96">
                    <h1>How To Contact Us</h1>
                    <img class="mb-16" src="/images-static/contacts.png" alt="man writing a letter to contact terrawhisper">
                    <p>Contact us by writing an email to the following email address: <strong>leenrandell@gmail.com</strong></p>
                    <h2 class="text-32">Read this before contacting us</h2>
                    <p>We don't accept business proposals at this particular moment. If you contact us to offer business partnerships or products to sponsor, we will decline them. TerraWhisper has its own agenda, and it's a busy one. We invest every single drop of our time delivering the best solutions to our readers, and there's no time left for us for anything else. This may change in the future, but now we are closed to additional business. Thanks for the understanding.</p>
                    <p>Also, when you contact us at leenrandell@gmail.com, keep in mind that Leen (the lady behind our email inbox) is as busy as the rest of us. Please, respect her and her time. Don't take it personal if she doesn't reply fast or, depending on the nature of the question, doesn't reply at all. For example, if you send us an email asking for a specific remedy, we will not answer it, as there's our website for that. Please undersand that we have thousands of readers and that they all have their own specific situations. There's no way we can't keep up with all the requests.</p>
                </section>
            </main>
            <div class="mt-64"></div>
            {components.footer()}
            {g.COOKIE_CONSENT}
        </body>
        </html>
    '''
    return html


def homepage_2():
    herbs_popular = []
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        data = json_read(json_filepath)
        for obj in data['herbs']:
            found = False
            for herb_popular in herbs_popular:
                if obj['plant_name_scientific'] == herb_popular['plant_name_scientific']:
                    herb_popular['confidence_score'] += obj['confidence_score']
                    found = True
                    break
            if not found:
                plant_slug = obj['plant_name_scientific'].lower().strip().replace(' ', '-')
                plant_json_filepath = f'database/json/herbs/{plant_slug}.json'
                if os.path.exists(plant_json_filepath):
                    _data = json_read(plant_json_filepath)
                    title = _data['title']
                    if 'intro_description' in _data: description = ' '.join(_data['intro_description'].split(' ')[:16])
                    properties = _data['properties']
                    random.shuffle(properties)
                    properties_html = '<ul class="ml-16 mb-24">'
                    for item in properties[:random.randint(3, 3)]:
                        properties_html += f'<li>{item["property_name"].capitalize()}</li>'
                    properties_html += '</ul>'
                    herbs_popular.append({
                        'plant_name_scientific': obj['plant_name_scientific'],
                        'plant_slug': f'{plant_slug}-plant',
                        'confidence_score': obj['confidence_score'],
                        'title': title,
                        'description': description,
                        'properties_html': properties_html,
                        'url': f'/{_data["url"]}.html',
                    })
    herbs_popular = sorted(herbs_popular, key=lambda x: x['confidence_score'], reverse=True)
    print(herbs_popular)
    
    # <h1 class="home-h1">Use Healing Herbs to Enhance Your Health</h1>

    hero_section = f'''
        <section class="mt-64">
            <div class="container-xl">
                <div class="flex gap-64 items-center">
                    <div class="flex-1">
                        <p class="text-color-green">Lean and Heal</p>
                        <h1 class="home-h1">Your Online Library of Popular Healing Herbs</h1>
                        <p class="text-color-light">Exploit the therapeutic power of medicinal plants and herbal remedies to find physical, mental, and spiritual relief.</p>
                        <div>
                            <a class="button-green-fill inline-block" href="/herbs.html">Explore Popular Herbs</a>
                        </div>
                    </div>
                    <div class="flex-1">
                        <img class="rounded-24" src="/images/herbs/abies-balsamea.jpg" alt="">
                    </div>
                </div>
            </div>
        </section>
    '''

    proof_section = f'''
        <section class="mt-96">
            <div class="container-xl">
                <div class="container-md text-center">
                    <h2 class="helvetica-regular pt-0 pb-16">Terrawhisper is a Science-Based Encyclopedia of Therapeutic Plants</h2>
                    <p class="pb-32">Terrawhisper is an online encyclopedia of healing herbs, featuring a vast collection of popular plants that have been extensively researched, documented, and backed by scientific studies (mostly from PubMed). New additions are added every week to ensure the library remains comprehensive and in-depth.
                    </p>
                </div>
                <div class="flex items-center">
                    <div class="flex-1 text-center border-0 border-r border-solid border-black">
                        <p class="text-32 mb-0 helvetica-bold">207</p>
                        <p class="mb-0">Herbs Analyzed</p>
                    </div>
                    <div class="flex-1 text-center border-0 border-r border-solid border-black">
                        <p class="text-32 mb-0 helvetica-bold">143</p>
                        <p class="mb-0">Studies Cited</p>
                    </div>
                    <div class="flex-1 text-center">
                        <p class="text-32 mb-0 helvetica-bold">2-3</p>
                        <p class="mb-0">Weekly Updates</p>
                    </div>
                </div>
            </div>
        </section>
    '''

    news_section = f'''
        <section class="mt-96 py-96">
            <div class="container-xl">
                <h2 class="text-24 mt-0 pt-0">Recently Added Herbs</h2>
                <div class="flex gap-32">
                    <div class="flex-1">
                        <img class="object-cover rounded-16 mb-24" src="/images/herbs/{herbs_popular[0]['plant_slug']}.jpg" alt="">
                        <h3 class="text-18 pt-0">{herbs_popular[0]['plant_name_scientific']}</h3>
                        {herbs_popular[0]['properties_html']}
                        <a href="{herbs_popular[0]['url']}" class="inline-block">Discover Plant ></a>
                    </div>
                    <div class="flex-1">
                        <img class="object-cover rounded-16 mb-24" src="/images/herbs/{herbs_popular[1]['plant_slug']}.jpg" alt="">
                        <h3 class="text-18 pt-0">{herbs_popular[1]['plant_name_scientific']}</h3>
                        {herbs_popular[1]['properties_html']}
                        <a href="{herbs_popular[1]['url']}" class="inline-block">Discover Plant ></a>
                    </div>
                    <div class="flex-1">
                        <img class="object-cover rounded-16 mb-24" src="/images/herbs/{herbs_popular[2]['plant_slug']}.jpg" alt="">
                        <h3 class="text-18 pt-0">{herbs_popular[2]['plant_name_scientific']}</h3>
                        {herbs_popular[2]['properties_html']}
                        <a href="{herbs_popular[2]['url']}" class="inline-block">Discover Plant ></a>
                    </div>
                    <div class="flex-1">
                        <img class="object-cover rounded-16 mb-24" src="/images/herbs/{herbs_popular[3]['plant_slug']}.jpg" alt="">
                        <h3 class="text-18 pt-0">{herbs_popular[3]['plant_name_scientific']}</h3>
                        {herbs_popular[3]['properties_html']}
                        <a href="{herbs_popular[3]['url']}" class="inline-block">Discover Plant ></a>
                    </div>
                    <div class="flex-1">
                        <img class="object-cover rounded-16 mb-24" src="/images/herbs/{herbs_popular[4]['plant_slug']}.jpg" alt="">
                        <h3 class="text-18 pt-0">{herbs_popular[4]['plant_name_scientific']}</h3>
                        {herbs_popular[4]['properties_html']}
                        <a href="{herbs_popular[4]['url']}" class="inline-block">Discover Plant ></a>
                    </div>
                </div>
            </div>
        </section>
    '''

    _herbs_html = ''
    for _herb in herbs_popular[20:25]:
        _herbs_html += f'''
            <div>
                <a href="{_herb['url']}" class="no-underline text-black">
                    <img class="object-cover rounded-16 mb-24" src="/images/herbs/{_herb['plant_slug']}.jpg" alt="">
                    <h3 class="text-18 pt-0">{_herb['plant_name_scientific']}</h3>
                    <p>{_herb['description']}...</p>
                </a>
            </div>
        '''
    news_section = f'''
        <section class="mt-96">
            <div class="container-xl">
                <h2 class="text-24 mt-0 pt-0">Recently Added Herbs</h2>
                <div class="grid grid-5 gap-32">
                    {_herbs_html}
                </div>
            </div>
        </section>
    '''

    benefits_section = f'''
        <section class="mt-96">
            <div class="container-xl">
                <h2 class="text-24 mt-0 pt-0">Why Healing With Herbs</h2>
                <div class="flex gap-32">
                    <div class="flex-1">
                        <img class="object-cover rounded-16" height="720" src="/images-static/medicinal-herbs-benefits.png" alt="">
                    </div>
                    <div class="flex-2 flex flex-col gap-32">
                        <div class="flex gap-32">
                            <div class="flex-1">
                                <img class="img-ico-sm" src="/images/herbs/{herbs_popular[0]['plant_slug']}.jpg" alt="">
                                <h3 class="text-18 pt-16">Boost Energy and Vitality</h3>
                                <p>Herbal supplements like Ginseng, Ashwagandha, and Rhodiola Rosea increases energy levels and mental clarity.
                                </p>
                            </div>
                            <div class="flex-1">
                                <img class="img-ico-sm" src="/images/herbs/{herbs_popular[1]['plant_slug']}.jpg" alt="">
                                <h3 class="text-18 pt-16">Promote Healthy Skin and Hair</h3>
                                <p>Herbs like Aloe Vera, Green Tea, and Rosemary essential oils can hydrate and nourish the skin and promote healthy hair growth.
                            </div>
                        </div>
                        <div class="flex gap-32">
                            <div class="flex-1">
                                <img class="img-ico-sm" src="/images/herbs/{herbs_popular[2]['plant_slug']}.jpg" alt="">
                                <h3 class="text-18 pt-16">Aid in Digestive Health</h3>
                                <p>Herbal remedies like Peppermint, Chamomile, and Ginger can soothe digestive issues, reduce bloating, and alleviate symptoms of IBS.
                                </p>
                            </div>
                            <div class="flex-1">
                                <img class="img-ico-sm" src="/images/herbs/{herbs_popular[3]['plant_slug']}.jpg" alt="">
                                <h3 class="text-18 pt-16">Support Mental Clarity and Focus</h3>
                                <p>Herbs like Bacopa Monnieri, Ginkgo Biloba, and Acetyl-L-Carnitine can improve concentration, memory, and mood.
                            </div>
                        </div>
                        <div class="flex gap-32">
                            <div class="flex-1">
                                <img class="img-ico-sm" src="/images/herbs/{herbs_popular[4]['plant_slug']}.jpg" alt="">
                                <h3 class="text-18 pt-16">Reduce Stress and Anxiety</h3>
                                <p>Herbal supplements like Passionflower, Kava, and Valerian Root can calm the nervous system and promote relaxation.
                                </p>
                            </div>
                            <div class="flex-1">
                                <img class="img-ico-sm" src="/images/herbs/{herbs_popular[5]['plant_slug']}.jpg" alt="">
                                <h3 class="text-18 pt-16">Promote Immune System</h3>
                                <p>Herbs like Echinacea, Goldenseal, and St. John's Wort can boost the immune system and protect against infections.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    '''

    why_us_section = f'''
        <section class="mt-96">
            <div class="container-xl">
                <div class="container-md text-center">
                    <h2 class="helvetica-regular pt-0 pb-16">What to Expect From Our Library</h2>
                    <p class="pb-32">We say that our articles are in-depth, and we mean it. For each plant, we meticulously detail its major medicinal uses, benefits, properties, constituents, parts, and preparations, providing readers with a comprehensive understanding of the plant's traditional and modern applications.
                    </p>
                </div>
                <div class="flex gap-64 mb-48">
                    <div class="flex-1 text-center">
                        <p class="text-24 mb-0 helvetica-bold mb-16">Uses</p>
                        <p class="mb-0">Our library lists the uses of plants across different medicinal systems (like western modern medicine, traditional chinese medicine, and Ayurvedic medicine), to validate their effectiveness.</p>
                    </div>
                    <div class="flex-1 text-center">
                        <p class="text-24 mb-0 helvetica-bold mb-16">Benefits</p>
                        <p class="mb-0">We dive deeply into the benefits of each herb on distinct body systems (such as digestive, nervous, cardiovascular, and respiratory), to provide comprehensive insights for holistic wellness.
</p>
                    </div>
                    <div class="flex-1 text-center">
                        <p class="text-24 mb-0 helvetica-bold mb-16">Properties</p>
                        <p class="mb-0">Our encyclopedia cover a comprehensive range of properties for the herbs (like anti-inflammatory, antioxidant, and antimicrobial), which is beneficial to understand how these herbs interract with various health conditions.</p>
                    </div>
                </div>
                <div class="flex gap-64">
                    <div class="flex-1 text-center">
                        <p class="text-24 mb-0 helvetica-bold mb-16">Constituents</p>
                        <p class="mb-0">In our articles, we do our best to include the chemical constituents of the plants (for example flavonoids, alkaloids, and other bioactive compounds), which give proof on their medicinal properties.</p>
                    </div>
                    <div class="flex-1 text-center">
                        <p class="text-24 mb-0 helvetica-bold mb-16">Parts</p>
                        <p class="mb-0">We understand that some parts of a plant are more curative than others (including roots, stems, leaves, bark, seeds, and flowers), so we always include what parts are best to consume for each plant.</p>
                    </div>
                    <div class="flex-1 text-center">
                        <p class="text-24 mb-0 helvetica-bold mb-16">Preparations</p>
                        <p class="mb-0">There are a wide range of herbal preparations you can make with each plant (such as teas, tinctures, salves, and oils), that's why our library discusses only the most effective and commonly used.</p>
                    </div>
                </div>
            </div>
        </section>
    '''

    _herbs_html = ''
    for _herb in herbs_popular[:20]:
        _herbs_html += f'''
            <div>
                <a href="{_herb['url']}" class="no-underline text-black">
                    <img class="object-cover rounded-16 mb-24" src="/images/herbs/{_herb['plant_slug']}.jpg" alt="">
                    <h3 class="text-18 pt-0">{_herb['plant_name_scientific']}</h3>
                    <p>{_herb['description']}...</p>
                </a>
            </div>
        '''
    popular_section = f'''
        <section class="mt-96">
            <div class="container-xl">
                <h2 class="text-24 mt-0 pt-0">Most Popular Herbs in Our Library</h2>
                <div class="grid grid-4 gap-32">
                    {_herbs_html}
                </div>
            </div>
        </section>
    '''

    about_section = f'''
        <section class="mt-96">
            <div class="container-xl">
                <div class="flex gap-96 mb-16">
                    <div class="flex-2">
                        <h2 class="helvetica-regular pt-0 pb-16">About Terrawhisper</h2>
                        <p>Welcome to Terrawhisper, your premier online destination for healing herbs. As the owner and curator, I invite you to discover the world of Terrawhisper, where ancient herbalism meets modern wisdom.</p>
                        <p>Our vast collection offers a wealth of information and guidance for those seeking a deeper connection with nature. From soothing lavender to restorative chamomile, explore our library and discover the transformative power of herbs for your life.</p>
                        <p>If you want to know more about Terrawhisper, <a href="/about.html">visit our about page</a>.</p>
                    </div>
                    <div class="flex-1 flex flex-col items-center text-center">
                        <img class="home-about-image" src="/images-static/leen-randell.jpg" alt="">
                        <p class="helvetica-bold text-24">Leen Randell</p>
                        <p>Herbalist & Healer, always hunting for new medicinal plants and scientific researches to expand my knowledge on natural remedies.</p>
                    </div>
                </div>
            </div>
        </section>
    '''

    about_section = f'''
        <section class="mt-96">
            <div class="container-xl">
                <div class="flex gap-96 mb-16">
                    <div class="flex-2">
                        <h2 class="helvetica-regular pt-0 pb-16">About Terrawhisper</h2>
                        <p>Welcome to Terrawhisper, your online library featuring the most popular healing herbs all around the world. My name is Leen Randell, I'm a herbalist and love to talk with like-minded people who share my passion for herbs and natural healing.</p>
                        <p>Feel free to browse around the library, find a medicinal herbs you're are interested in, and discover how it can help you improve your life and the lives of those around you. Healing herbs can be a transformative experience, but only if you take action. And you are just a few clicks away from taking your wellness to a whole new level.</p>
                        <p>If you want to know more about me and Terrawhisper, <a href="/about.html">visit our about page</a>.</p>
                    </div>
                    <div class="flex-1 flex flex-col items-center text-center">
                        <img class="home-about-image" src="/images-static/leen-randell.jpg" alt="">
                        <p class="helvetica-bold text-24">Leen Randell</p>
                    </div>
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
            <meta name="author" content="{g.AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>Use Medicinal Herbs to Heal Naturally</title>
            {g.GOOGLE_TAG}
            {g.GOOGLE_ADSENSE_TAG}
        </head>
        <body>
            {components.header_2()}
            <main>
                {hero_section}
                {proof_section}
                {news_section}
                {benefits_section}
                {why_us_section}
                {popular_section}
                {about_section}
            </main>
            <div class="mt-64"></div>
            {components.footer_2()}
            {g.COOKIE_CONSENT} 
        </body>
        </html>
    '''
    return html
                #{section_articles}

def page_about_2():
    json_filepath = 'tmp/about-info-asked.json'
    if 0:
        prompt = f'''
            I have a brand called "terrawhisper", which is an online encyclopedia of medicinal herbs. 
            I have to write an "about us" page for our website.
            What info do you need so you can write me an 800-word about us page that's compelling to read?
            Don't ask for info about "mission statement" and what is the "vision for the future", as the "our mission" page is a separate page.
            Don't ask for info about "contact information", as it goes in a separate page.
            Reply in JSON format using the structure extracted from the following example:
            [
                {{"info_name": "insert name of info here", "info_description": "insert description of info here"}},
                {{"info_name": "insert name of info here", "info_description": "insert description of info here"}},
                {{"info_name": "insert name of info here", "info_description": "insert description of info here"}}
            ]
            Reply only with the JSON, don't add additional content.
        '''
        reply = llm_reply(prompt)
        try: json_data = json.loads(reply)
        except: json_data = '' 
        json_write(json_filepath, json_data)

    if 0:
        prompt = f'''
            Write me an outline for the "about me" page of my website.
            The website is an online encyclopedia of medicinal herbs.
            Don't include mission and vision, as they go to another page.
        '''
        reply = llm_reply(prompt)
        with open('tmp/outline.txt', 'w') as f:
            f.write(reply)
    
    if 0:
        with open('tmp/outline-final.txt') as f: content = f.read()    
        content = content.split('\n')[0].strip()
        prompt = f'''
            I have to write a section for an about me page for my website.
            The website is an online encyclopedia of medicinal herbs.
            The topic of the section is: {content}.
            What info do you need to write this section in a compelling way?
            The section should be about 100-word long.
        '''
        reply = llm_reply(prompt)

    if 0:
        with open('tmp/introduction.txt') as f: content = f.read()    
        content = content.split('\n')[0].strip()
        prompt = f'''
            Write me a 100-word section for an "about me" page for my website that's called "Terrawhisper", which is and online encyclopedia of medicinal herbs.
            Here's the outline and the info you need:
            {content}.
            Start with the following words: "Dear Friend, ".
        '''
        reply = llm_reply(prompt)

    # expertise
    if 0:
        with open('tmp/expertise.txt') as f: content = f.read()    
        content = content.split('\n')[0].strip()
        prompt = f'''
            I have to write a section for an about me page for my website.
            The website is an online encyclopedia of medicinal herbs.
            The topic of the section is: {content}.
            What info do you need to write this section in a compelling way?
            The section should be about 100-word long.
        '''
        reply = llm_reply(prompt)
        with open('tmp/expertise-final.txt', 'w') as f: f.write(reply)

    # terrawhisper story
    if 0:
        with open('tmp/terrawhisper-story.txt') as f: content = f.read()    
        content = content.split('\n')[0].strip()
        prompt = f'''
            I have to write a section for an about me page for my website.
            The website is an online encyclopedia of medicinal herbs.
            The topic of the section is: {content}.
            What info do you need to write this section in a compelling way?
            The section should be about 100-word long.
        '''
        reply = llm_reply(prompt)
        with open('tmp/expertise-final.txt', 'w') as f: f.write(reply)

    # about me
    if 0:
        with open('tmp/introduction-final.txt') as f: info = f.read()    
        with open('tmp/outline-final.txt') as f: outline = f.read()    
        prompt = f'''
            I have to write a 800-word about me page for my website using the following OUTLINE and INFORMATION.
            The website is an online encyclopedia of medicinal herbs.
            <OUTLINE>
            {outline}
            </OUTLINE>
            <INFORMATION>
            {info}
            </INFORMATION>
            Start with the following words: "Dear Friend, ".
        '''
        reply = llm_reply(prompt)
        with open('tmp/about.txt', 'w') as f: f.write(reply)

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
                    <div class="flex-3">
                        <h1>About Terrawhisper</h1>
                        <p>{content}</p>
                    </div>
                    <div class="flex-1 flex flex-col items-center text-center">
                        <img class="home-about-image" src="/images-static/leen-randell.jpg" alt="">
                        <p class="helvetica-bold text-24">Leen Randell</p>
                        <p>Herbalist & Healer, always hunting for new medicinal plants and scientific researches to expand my knowledge on natural remedies.</p>
                    </div>
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
            <meta name="author" content="{g.AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>Use Medicinal Herbs to Heal Naturally</title>
            {g.GOOGLE_TAG}
            {g.GOOGLE_ADSENSE_TAG}
        </head>
        <body>
            {components.header_2()}
            <main>
                {section}
            </main>
            <div class="mt-64"></div>
            {components.footer_2()}
            {g.COOKIE_CONSENT} 
        </body>
        </html>
    '''

    return html 

def page_mission():
    global pipe
    if pipe == None:
        pipe = StableDiffusionXLPipeline.from_single_file(
            checkpoint_filepath, 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

    image = Image.open(f'{vault}/terrawhisper/images-static/terrawhisper-botanical-garden.png')
    image = image.convert('RGB')
    width = 832
    height = 1216
    image = img_resize(image, w=width//2, h=height//2)
    image.save(f'website/images-static/terrawhisper-botanical-garden.jpg')

    image = Image.open(f'{vault}/terrawhisper/images-static/terrawhisper-apothecary.png')
    image = image.convert('RGB')
    width = 832
    height = 1216
    image = img_resize(image, w=width//2, h=height//2)
    image.save(f'website/images-static/terrawhisper-apothecary.jpg')

    if 0:
        prompt = f'''
            Write me an outline for the "our mission" page of my website.
            The website is an online encyclopedia of medicinal herbs.
        '''
        reply = llm_reply(prompt)
        with open('tmp/output.txt', 'w') as f:
            f.write(reply)
    
    if 0:
        with open('tmp/output.txt') as f: outline = f.read()
        with open('/home/ubuntu/vault/terrawhisper/marketing/identity.txt') as f: data = f.read()

        prompt = f'''
            Write the "our mission" page for a website that's an online encyclopedia of medicinal herbs.
            Reply in 800 words.
            Don't write lists.
            Use the folloing OUTLINE and fill it with the following DATA when applicable.
            <OUTLINE>
                {outline}
            </OUTLINE>
            <DATA>
                {data}
            </DATA>
        '''
        reply = llm_reply(prompt)

    with open('content/mission.txt') as f: 
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
                        <h1>Terrawhisper Mission</h1>
                        <p>{content}</p>
                    </div>
                    <div class="flex-1 flex flex-col items-center text-center gap-32">
                        <img class="" src="/images-static/terrawhisper-botanical-garden.jpg" alt="">
                        <img class="" src="/images-static/terrawhisper-apothecary.jpg" alt="">
                    </div>
                </div>
            </div>
        </section>
    '''

    if 0:
        prompt = f'''
            Write me an outline for the "our mission" page of my website.
            The website is an online encyclopedia of medicinal herbs.
        '''
        reply = llm_reply(prompt)
        with open('tmp/output.txt', 'w') as f:
            f.write(reply)
    


    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{g.AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>Use Medicinal Herbs to Heal Naturally</title>
            {g.GOOGLE_TAG}
            {g.GOOGLE_ADSENSE_TAG}
        </head>
        <body>
            {components.header_2()}
            <main>
                {section}
            </main>
            <div class="mt-64"></div>
            {components.footer_2()}
            {g.COOKIE_CONSENT} 
        </body>
        </html>
    '''

    return html 

def page_contacts_2():
    if 0:
        prompt = f'''
            Write me an outline for the "contacts" page of my website.
            The website is an online encyclopedia of medicinal herbs.
        '''
        reply = llm_reply(prompt)
        with open('tmp/output.txt', 'w') as f:
            f.write(reply)
    
    section = f'''
        <section class="">
            <div class="container-md">
                        <h1>Terrawhisper Contacts</h1>
                        <p>Send me an email at <u>leenrandell@gmail.com</u> if you want to contact me.</p>
                        <h2 class="text-32">Valid Reasons to Contact Me</h2>
                        <p>Please contact me only if you have one of the following reasons:</p>
                        <ul>
                            <li>Do you have a particular herb in mind that's missing at Terrawhisper and that you want me to cover? If so, send me an email with the scientific name (not common name) of that herb, along with a brief description on why you believe is an herb with great medicinal potential. Please note that there's a waiting line and that I'm already vetting dozens of requested herbs. It will take some time for me to serve your request.</li>
                            <li>Do you have a partnership proposal in mind and want to establish a collaboration with Terrawhisper? If so, send me an email with your request, I'm always happy to hear new ideas and ways to make the world grow greener thanks to the help of everyone.</li>
                            <li>Do you believe you have great feedback to offer to the site in terms of missing pieces of information about a herb or information that you think are wrong? If so, send me an email and I will double-check the library. Please, be ultra-specific on the page and the information to update. It's better if you send me a link to the page.</li>
                        </ul>
                        <p>IMPORTANT: If you contact me to ask to add a piece on info on one of our article, please understand that we only add info that has is validated by several different data point. I do not accept "anecdotal" or "word-of-mouth" information (i.e. information that has not being validated by at least a couple of scientific papers).</p>
                        <h2 class="text-32">NON Valid Reasons to Contact Me</h2>
                        <p>Simply put, I'm not open for some types of business requests. In particular:</p>
                        <ul>
                            <li>Do not contact me to ask me to sell your herbs (this happens too often). Terrawhisper is not an ecommerce.</li>
                            <li>Do not contact me to sell advertising space. I'm in the process of doing that with leading display-ad networks.</li>
                        </ul>
            </div>
        </section>
    '''


    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{g.AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>Use Medicinal Herbs to Heal Naturally</title>
            {g.GOOGLE_TAG}
            {g.GOOGLE_ADSENSE_TAG}
        </head>
        <body>
            {components.header_2()}
            <main>
                {section}
            </main>
            <div class="mt-64"></div>
            {components.footer_2()}
            {g.COOKIE_CONSENT} 
        </body>
        </html>
    '''

    return html 

# TODO: complete homepage
# fix images, links, num of plant, index of plants
