import os

from lib import g
from lib import components

def gen():
    html_folderpath = f'{g.WEBSITE_FOLDERPATH}/shop'
    html_filepath = f'{html_folderpath}/infusion-cheatsheet-download.html'
    html_breadcrumbs = components.breadcrumbs(f'shop/infusion-cheatsheet-download.html')
    page_title = f'medicinal herbal infusion cheatsheet'
    product_download_href = f'/assets/shop/medicinal-herbal-infusion-cheatsheet.jpg'
    product_image_src = f'/images/shop/medicinal-herbal-infusion-cheatsheet-cover.jpg'
    product_image_alt = f'medicinal herbal infusion cheatsheet cover'
    product_title ='medicinal herbal infusion cheatsheet'.title()
    product_description = f'''
I used to just throw herbs in hot water and hope for the best.

No clue what I was doing. Half the time it tasted like boiled weeds... the other half, like sad leaf soup.

But I was DONE googling 27 tabs just to make one damn cup of tea.

So I made this.

A one-stop, no-fluff cheatsheet for herbal infusions. Digital. A4. Printable. Simple AF.

It’s got the formula (finally), prep steps that actually make sense, the tools, examples of popular herbs, and tips to not kill the potency.

Plus, herbal pairings that slap.

I legit use it every day now. Like... it's taped to my damn kitchen wall.

If you're tired of guessing... or just wanna feel like you kinda know what you're doing with your mug of magic... get this thing.

Grab it. Print it. Brew better.
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
                        <a class="button" href="{product_download_href}">DOWNLOAD CHEATSHEET (HD)</a>
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

