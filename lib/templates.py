import g
from lib import components

from oliark import csv_read_rows_to_json
from oliark import json_read

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
        </head>
        <body>
            {header}
            {breadcrumbs}
            <section class="container-md my-96">
                {meta}
                {article}
            </section>
            {footer}
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

def homepage_section_benefits_2():
    url = '/images-static/benefits.png'
    bg_color_fuchsia_700 = '#a21caf'
    bg_color_purple_100 = '#f3e8ff'
    bg_color_purple_200 = '#e9d5ff'
    bg_color_purple_700 = '#7e22ce'
    bg_color_stone_100 = '#f5f5f4'
    bg_color = bg_color_stone_100
    text_color = 'black'
    opacity = 0.0
    html = f'''
        <section class="h-80v">
            <div class="flex h-full items-center" style="background-color: {bg_color};">
                <div class="flex-1 h-full" style="background-image: linear-gradient(rgba(0, 0, 0, {opacity}), rgba(0, 0, 0, {opacity})), url({url}); background-position: center; background-size: cover;">
                </div>
                <div class="flex-1">
                    <div class="container-xl-half ml-0 ml-48 mr-auto">
                        <h2 class="text-64 font-lato-regular text-black">Benefits of using herbal remedies</h2>
                        <p class="mb-48 text-black">Herbs are a natural, effective, and eco-friendly solution to find relief from common ailments and improve you quality of life.</p>
                        <h3 class="text-black text-20 font-lato-bold mb-8">1. Natural and non-toxic</h3>
                        <p class="mb-24">Unlike synthetic pharmaceuticals, herbal remedies are derived directly from plants, which have been used for centuries in traditional medicine and contain bioactive compounds in their natural form, making them less likely to cause adverse reactions or interract with medications.</p>
                        <h3 class="text-black text-20 font-lato-bold mb-8">2. Effective for common ailments</h3>
                        <p class="mb-24">Unlike synthetic pharmaceuticals, herbal remedies are derived directly from plants, which have been used for centuries in traditional medicine and contain bioactive compounds in their natural form, making them less likely to cause adverse reactions or interract with medications.</p>
                        <h3 class="text-black text-20 font-lato-bold mb-8">3. Sustainable and environmentally friendly</h3>
                        <p class="mb-24">Unlike synthetic pharmaceuticals, herbal remedies are derived directly from plants, which have been used for centuries in traditional medicine and contain bioactive compounds in their natural form, making them less likely to cause adverse reactions or interract with medications.</p>
                    </div>
                </div>
            </div>
        </section>
    '''
    return html

def homepage():
    section_articles = homepage_articles('teas')
    opacity = 0.0
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
        </head>
        <body>
            {components.header()}
            <main>
                <section class="h-80v">
                    <div class="flex h-full items-center bg-emerald-900">
                        <div class="flex-1">
                            <div class="container-xl-half">
                                <h1 class="homepage-hero-card-title">Use Medicinal Herbs to Heal Naturally</h1>
                                <p class="text-white mb-24">Learn to leverage the power of healing plants to relieve more than 300 physical, mental and spiritual health problems.</p>
                                <a href="/remedies.html" class="button-white">Discover Remedies</a>
                            </div>
                        </div>
                        <div class="flex-1 h-full" style="background-image: linear-gradient(rgba(0, 0, 0, {opacity}), rgba(0, 0, 0, {opacity})), url(/images-static/hero.jpg); background-position: center; background-size: cover;">
                        </div>
                    </div>
                </section>
                <section id="what" class="homepage-what">
                    <h2 class="homepage-what-title">TerraWhisper is a science-based, daily updated, online herbal remedies encyclopedia</h2>
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
                {homepage_section_benefits_2()}
                {section_articles}
            </main>
            <div class="mt-64"></div>
            {components.footer()}
        </body>
        </html>
    '''
    return html
