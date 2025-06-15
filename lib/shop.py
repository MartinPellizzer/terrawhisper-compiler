from lib import g
from lib import io
from lib import utils
from lib import components

def gen():
    html_cards = ''
    html_section_art = f'''
        <div style="margin-top: 1.6rem;" class="grid grid-4 gap-16">
    '''
    ailments = io.csv_to_dict('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        print(f'\n>> {ailment_i}/{len(ailments)} - {ailment}')
        ailment_slug = ailment['ailment_slug']
        url = f'ailments/{ailment_slug}'
        json_article_filepath = f'database/json/{url}.json'
        json_article = io.json_read(json_article_filepath)
        href = f'/{url}.html'
        src = f"/images/ailments/{ailment_slug}-herbal-remedies.jpg" 
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
    html_filepath = f'{g.WEBSITE_FOLDERPATH}/ailments.html'
    page_title = f'shop'
    html_breadcrumbs = components.breadcrumbs(f'ailments.html')
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



