import os

from lib import g
from lib import components

def gen():
    html_folderpath = f'{g.WEBSITE_FOLDERPATH}/shop'
    html_filepath = f'{html_folderpath}/herb-drying-checklist-download.html'
    html_breadcrumbs = components.breadcrumbs(f'shop/herb-drying-checklist-download.html')
    page_title = f'the ultimate herb drying checklist download'
    product_download_href = f'/assets/shop/herb-drying-checklist.pdf'
    product_image_src = f'/images/shop/herb-drying-checklist.jpg'
    product_image_alt = f'herb drying checklist blurred'
    product_title ='the ultimate herb drying checklist download'.title()
    product_description = f'''
    '''
    html_product_description = ''.join([f'<p>{line}</p>' for line in product_description.strip().split('\n') if line.strip() != ''])
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 16px; margin-bottom: 16px;" class="container-xl">
                {html_breadcrumbs}
                <div style="margin-top: 24px;" class="mob-flex gap-48">
                    <img class="flex-1" style="object-fit: contain;" src="{product_image_src}" alt="{product_image_alt}">
                    <div class="flex-1">
                        <h1>{product_title}</h1>
                        {html_product_description}
                        <a class="button" href="{product_download_href}">DOWNLOAD CHECKLIST (HD)</a>
                    </div>
                </div>
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    try: os.mkdir(html_folderpath)
    except: pass
    with open(html_filepath, 'w') as f: f.write(html)

