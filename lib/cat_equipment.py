import os

from lib import g
from lib import io
from lib import utils
from lib import components

entities = io.csv_to_dict(f'database/entities/equipment.csv')
category = 'equipment'

def gen():
    html_cards = ''

    html_section_art = f'''
        <div style="margin-top: 1.6rem;" class="grid grid-4 gap-16">
    '''

    for entity_i, entity in enumerate(entities):
        print(f'\n>> {entity_i}/{len(entities)} - {entity}')
        entity_name_singular = entity['entity_name_singular'].strip()
        entity_name_plural = entity['entity_name_plural'].strip()
        entity_slug = utils.sluggify(entity_name_singular)
        url = f'{category}/{entity_slug}'
        if not os.path.exists(f'database/json/{category}'):
            os.mkdir(f'database/json/{category}')
        json_article_filepath = f'database/json/{url}.json'
        json_article = io.json_read(json_article_filepath)
        href = f'/{url}.html'
        src = f"/images/{category}/{entity_slug}.jpg" 
        title = json_article['title']
        html_section_art += components.card_art_html(
            href=href,
            src=src,
            title=title,
        )

    html_section_art += f'''
        </div>
    '''
    print(html_section_art)

    html_filepath = f'{g.WEBSITE_FOLDERPATH}/{category}.html'
    page_title = f'Equipments'
    html_breadcrumbs = components.breadcrumbs(f'{category}.html')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 24px;" class="container-xl">
                {html_breadcrumbs}
                {html_section_art}
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)


