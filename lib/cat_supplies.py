import os

from lib import g
from lib import io
from lib import utils
from lib import components

category = 'supplies'
supplies = [
    {
        'supply_name_singular': 'jar',
        'supply_name_plural': 'jars',
    },
]

def gen():
    html_cards = ''

    html_section_art = f'''
        <div style="margin-top: 1.6rem;" class="grid grid-4 gap-16">
    '''

    for supply_i, supply in enumerate(supplies):
        print(f'\n>> {supply_i}/{len(supplies)} - {supply}')
        supply_name_singular = supply['supply_name_singular'].strip()
        supply_name_plural = supply['supply_name_plural'].strip()
        supply_slug = utils.sluggify(supply_name_singular)
        url = f'{category}/{supply_slug}'
        json_article_filepath = f'database/json/{url}.json'
        json_article = io.json_read(json_article_filepath)
        href = f'/{url}.html'
        src = f"/images/{category}/{supply_slug}.jpg" 
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
    page_title = f'herbalism supplies'
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

