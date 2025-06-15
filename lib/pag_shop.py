
from lib import g
from lib import io
from lib import utils
from lib import components

def gen():
    html_cards = ''
    html_section_art = f'''
        <div style="margin-top: 1.6rem;" class="grid grid-4 gap-16">
    '''
    href = f'/shop/infusion-cheatsheet-download.html'
    src = f'/images/shop/medicinal-herbal-infusion-cheatsheet-cover.jpg'
    title = f'medicinal herbal infusion cheatsheet'.title()
    html_section_art += components.card_art_html(
        href=href,
        src=src,
        title=title,
    )
    html_section_art += f'''
        </div>
    '''
    print(html_section_art)
    html_filepath = f'{g.WEBSITE_FOLDERPATH}/shop.html'
    page_title = f'shop'
    html_breadcrumbs = components.breadcrumbs(f'shop.html')
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


