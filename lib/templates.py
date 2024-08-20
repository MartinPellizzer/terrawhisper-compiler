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

def homepage():
    section_articles = homepage_articles('teas')

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
                <section class="h-80v" style="background-image: url(/images-static/medicinal-plants.jpg); background-position: center; background-size: cover;">
                    <div class="container-xl h-full">
                        <div class="flex items-center h-full">
                            <div class="homepage-hero-card">
                                <h1 class="homepage-hero-card-title">Use Medicinal Herbs to Heal Naturally</h1>
                                <p>Learn to leverage the power of healing plants to cure more than 300 physical, mental and spiritual health problems.</p>
                                <a href="/remedies.html" class="button">Discover Remedies</a>
                            </div>
                        </div>
                    </div>
                </section>
                <section id="what" class="homepage-what">
                    <h2 class="homepage-what-title">TerraWhisper is a science-based, daily updated, online herbal remedies encyclopedia</h2>
                    <div class="homepage-what-cards">
                        <div class="homepage-what-card">
                            <img class="mb-24" src="/images-static/herbal-remedies.jpg" alt="">
                            <a href="/remedies.html" class="button">Browse Remedies</a>
                        </div>
                        <div class="homepage-what-card">
                            <img class="mb-24" src="/images-static/healing-herbs.jpg" alt="">
                            <a href="/herbs.html" class="button">Browse Herbs</a>
                        </div>
                    </div>
                </section>
                {section_articles}
            </main>
            <div class="mt-64"></div>
            {components.footer()}
        </body>
        </html>
    '''
    return html
