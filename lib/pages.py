import shutil

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read

import g
from lib import utils
from lib import components

def card_guide_html(href, src, title, image_border=False):
    if image_border: image_border_style = 'border: 1px solid #000000;'
    else: image_border_style = ''
    html = f'''
        <a class="article-card no-underline text-black" href="{href}">
            <img style="{image_border_style}" class="mb-16" src="{src}" alt="herb drying checklist">
            <h2 class="h2-plain text-18 mb-12">{title}</h2>
        </a>
    '''
    return html

def page_guides():
    cards_html = ''
    cards_html += card_guide_html(
        href="/guides/checklist-dry-herbs.html",
        src="/images-static/checklist-dry-herbs.jpg",
        title="The Ultimate Herb Drying Checklist",
    )
    cards_html += card_guide_html(
        href="/guides/tinctures.html",
        src="/images/guides/medicinal-herbal-tinctures-1-cover.jpg",
        title="Medicinal Herbal Tinctures Mini-Manual",
    )
    cards_html += card_guide_html(
        href="/guides/herbal-tea-shopping-list-download.html",
        src="/images/guides/herbal-tea-shopping-list-cover.jpg",
        title="Herbal Tea Shopping List",
        image_border=True,
    )

    section_1 = f'''
        <section class="mt-48 mb-48">
            <div class="container-md">
                <div class="grid grid-3 gap-16">
                    {cards_html}
                </div>
            </div>
        </section>
    '''

    html_filepath = f'{g.WEBSITE_FOLDERPATH}/guides.html'
    page_title = f'terrawhisper guides on herbalism and herbal medicine'
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <div style="padding-top: 16px;" class="container-xl">
                {components.breadcrumbs('guides.html')}
            </div>
            <main>
                {section_1}
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def page_guides_tinctures_gen():
    html_filepath = f'{g.WEBSITE_FOLDERPATH}/guides/tinctures.html'
    html_breadcrumbs = components.breadcrumbs(f'guides/tinctures.html')
    page_title ='medicinal herbal tinctures'
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 16px; margin-bottom: 16px;" class="container-xl">
                {html_breadcrumbs}
                <div style="margin-top: 24px;" class="mob-flex gap-48">
                    <img class="flex-1" src="/images/guides/medicinal-herbal-tinctures-1-cover.jpg" alt="medicinal herbal tinctures edition 1 cover">
                    <div class="flex-1">
                        <span style="font-size: 14px; margin-bottom: 16px; display: inline-block; background-color: #c2410c; color: #ffffff; padding: 8px 16px;">FREE DOWNLOAD CLOSED</span>
                        <h1>Medicinal Herbal Tinctures Mini-Manual</h1>
                        <p>So you wanna learn how to make herbal tinctures?</p>
                        <p>Great. Because I'm giving away my mini-manual on how to make medicinal herbal tincture - for FREE until April 10th.</p>
                        <p>Here's why you NEED this:</p>
                        <ul>
                            <li>Forget overpriced store-bought tinctures that are 80% water and 20% hope. You lean to make the real deal. No frills. No fake promises.</li>
                            <li>I'm not handing you some complicated, lab-science mumbo jumbo. If you can boil water (and you don't need), you can do this.</li>
                            <li>You're not going to get smacked with some 10-hour online class. This guide is short, sweet, and straight to the point. It's only 10 pages, perfect for a fast win and understand if it's something you enjoy or not.</li>
                        </ul>
                        <p>But here's the catch...</p>
                        <p>This isn't gonna be free forever. After April 10th, no more free. Poof. Like that.</p>
                        <p>My advice? Download it NOW. Yes, even if you're not interested. One day you may be, and you'll have to pay for it. Grab it now just in case.</p>
                        <p>Stay Grounded,</p>
                        <p>Leen</p>
                        <a class="button" href="">FREE DOWNLOAD CLOSED</a>
                    </div>
                </div>
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def page_guides_teas_shopping_list_download_gen():
    html_filepath = f'{g.WEBSITE_FOLDERPATH}/guides/herbal-tea-shopping-list-download.html'
    html_breadcrumbs = components.breadcrumbs(f'guides/herbal-tea-shopping-list-download.html')
    page_title ='herbal tea shopping list'
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 16px; margin-bottom: 16px;" class="container-xl">
                {html_breadcrumbs}
                <div style="margin-top: 24px;" class="mob-flex gap-48">
                    <img class="flex-1" style="object-fit: contain;" src="/images/guides/herbal-tea-shopping-list-cover.jpg" alt="medicinal herbal tinctures edition 1 cover">
                    <div class="flex-1">
                        <h1>The Ultimate Herbal Tea Shopping List</h1>
                        <p>Dear Apothecary,</p>
                        <p>I made "The Ultimate Herbal Tea Shopping List".</p>
                        <p>Why? Cuz if you're anything like me, you don't have time to scroll TikTok for 3 hours to figure out which tea helps with bloating or anxiety or PMS from hell.</p>
                        <p>This list has 30 common ailments (the ones that mess with our sleep, energy, mood, digestion, and hormones).</p>
                        <p>And for each one? 3 badass herbal teas that actually help.</p>
                        <p>Here's what you'll feel when you use it:</p>
                        <ul>
                            <li>Wake up without that brain-fog zombie feeling</li>
                            <li>Calm your nervous system without numbing out</li>
                            <li>Poop better (yup, I said it, regular AF)</li>
                            <li>Feel like your body actually has your back again</li>
                            <li>Sip tea... and actually feel better, not just warm</li>
                        </ul>
                        <p>No fluff. Just ancient remedies for modern chaos.</p>
                        <p>And yeah, it's free, because this info should be in everyone's damn kitchen.</p>
                        <p>Grab it. Print it. Stick it on your fridge. Use it.</p>
                        <p>You'll thank me when your gut, skin, and soul all start chillin'.</p>
                        <p>Stay Grounded,</p>
                        <p>Leen</p>
                        <a class="button" href="/assets/pdf/herbal-tea-shopping-list.jpg">FREE DOWNLOAD</a>
                    </div>
                </div>
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def page_guides_cards_pk1():
    html_filepath_relative = 'products/cards.html'
    html_filepath = f'{g.WEBSITE_FOLDERPATH}/{html_filepath_relative}'
    html_breadcrumbs = components.breadcrumbs(f'{html_filepath_relative}')
    page_title ='40 Flashcard Designs To Learn Medicinal Names Of Herbs (Printables)'
                # {html_breadcrumbs}
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 16px; margin-bottom: 16px;" class="container-xl">
                <div style="margin-top: 24px;" class="mob-flex gap-48">
                    <img class="flex-1" style="object-fit: contain;" src="/images/guides/botanical-deck.png" alt="botanical deck">
                    <div class="flex-1">
                        <h1>40 Flashcard Printable Designs To Learn Medicinal Names Of Herbs</h1>
                        <p>Beautifully designed printable deck of 40 botanical flashcards. Each 3x5" card features one medicinal plant, including its scientific name, plant family, and common names—perfect for students, herbalists, and nature lovers alike.</p>
                        <p>Styled with Victorian elegance and rustic charm, this digital deck blends old-world aesthetics with modern learning. Whether you're building your herbal knowledge or just love vintage botanical art, these cards are both a practical study tool and a gorgeous collector’s piece.</p>
                        <p><i>(Digital download only, no physical product will be shipped)</i></p>
                        <p><b>Product Features:</b></p>
                        <ul>
                            <li>40 Botanical Flashcards: Each card highlights one healing herb with its scientific name, plant family, and common names</li>
                            <li>Vintage-Inspired Design: Elegant Victorian and rustic aesthetics create a timeless, apothecary-style vibe</li>
                            <li>Perfect for Study & Memorization: Ideal for herbalists, students, gardeners, and nature lovers looking to deepen their knowledge of medicinal plants</li>
                            <li>Flashcard Size: 3x5 inches, easy to print, cut, and store, great for hands-on learning or display</li>
                            <li>Digital Download Only: Instant access to print-at-home card, no physical item will be shipped</li>
                            <li>Makes a Unique Gift: A thoughtful present for herbalism students, plant enthusiasts, or fans of vintage botanical art</li>
                        </ul>
                        <div class="flex gap-8 items-center mb-16">
                            <p class="price">€0.00</p> 
                            <p class="price-stroke"><s>€9.95</s></p> 
                            <div>
                                <p class="sales-tag">100% off</p>
                            </div>
                        </div>
                        <a class="buy-button" href="/assets/products/cards.zip">DOWNLOAD PRODUCT (.ZIP)</a>
                        <p><span style="font-weight: bold;">WARNING:</span> The download is compressed in a .ZIP archive, so you need a .ZIP extraction software to access the content of this download.</p>
                    </div>
                </div>
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def html_card_art(href, src, title):
    html = f'''
        <a class="article-card no-underline text-black" href="{href}">
            <img class="mb-16" src="{src}" alt="herb drying checklist">
            <h2 class="h2-plain text-18 mb-12">{title}</h2>
        </a>
    '''
    return html

def cat_ailments():
    html_cards = ''
    html_section_art = f'''
        <div style="margin-top: 1.6rem;" class="grid grid-4 gap-16">
    '''
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        print(f'\n>> {ailment_i}/{len(ailments)} - {ailment}')
        ailment_slug = ailment['ailment_slug']
        url = f'ailments/{ailment_slug}'
        json_article_filepath = f'database/json/{url}.json'
        json_article = json_read(json_article_filepath)
        href = f'/{url}.html'
        src = f"/images/ailments/{ailment_slug}-herbal-remedies.jpg" 
        title = json_article['title']
        html_section_art += html_card_art(
            href=href,
            src=src,
            title=title,
        )
    html_section_art += f'''
        </div>
    '''
    print(html_section_art)
    html_filepath = f'{g.WEBSITE_FOLDERPATH}/ailments.html'
    page_title = f'ailments herbal remedies'
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


def product_bundle_download_gen():
    html_filepath_relative = 'products/bundle-download.html'
    html_filepath = f'{g.WEBSITE_FOLDERPATH}/{html_filepath_relative}'
    html_breadcrumbs = components.breadcrumbs(f'{html_filepath_relative}')
    page_title ='The Herbalist Boundle: Herbs Drying Checklist, Herbal Tea Shopping List, Medicinal Herbs Flashcards'
    # {html_breadcrumbs}
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 16px; margin-bottom: 16px;" class="container-xl">
                <h1 style="margin-top: 4.8rem;">Congratulation! Here's Your Boundle.</h1>
                <p>Below you'll find your bundle. The bundle consists of 3 digital products to download. You'll find a brief description for each product too. Download and enjoy them.</p>
                <h2>Digital Product 1: The Herb Drying Checklist</h2>
                <p>This product (digital download) includes 30 quick-and-easy steps to "check" every time you have to dry herbs to make sure they don't mold and last for 1+ year (in a 6 page .PDF file format). It's better suited to be consulted digitally (PC/smartphone), as it wasn't desinged and optimize to be perfect for printing.</p>
                <p>Click the button below to download The Herb Drying Checklist in full resolution (HD).</p>
                <div style="margin-bottom: 1.6rem;">
                    <a class="button-fill" href="/assets/products/herb-drying-checklist.pdf">DOWNLOAD PRODUCT</a>
                </div>
                <p>The following image show a preview of this product.</p>
                <div class="grid-2 gap-24">
                    <img src="/images/products/herb-drying-checklist.jpg">
                </div>
                <h2>Digital Product 2: The Herbal Tea Shopping List</h2>
                <p>This product (digital download) includes 30 common ailments and 3 medicinal herbal teas to treat each ailment (1 printable page in A4 format). Its design is barebone, so you can easily print it and take it with you while shopping.</p>
                <p>Click the button below to download The Herbal Tea Shopping List in full resolution (HD).</p>
                <div style="margin-bottom: 1.6rem;">
                    <a class="button-fill" href="/assets/products/herbal-tea-shopping-list.jpg">DOWNLOAD PRODUCT</a>
                </div>
                <p>The following image show a preview of this product.</p>
                <div class="grid-2 gap-24">
                    <img src="/images/products/herbal-tea-shopping-list-cover.jpg">
                </div>
                <h2>Digital Product 3: The Medicinal Herb Flashcards</h2>
                <p>This product (digital download) includes 40 beautifully designed botanical printable flashcards (3x5" size). Their are Victorian, vintage, and rustic elegance in style. Each card has an illustration of a medicinal herb, the scientific name of the card, the family name of the card, and the most common names used for this herbs. Great as index cards and as memory card to learn the scientific names of the herbs.</p>
                <p>This is deck #1. More packages with other herbs will be designed and added in the future.</p>
                <p>Click the button below to download The Medicinal Herbs Flashcards.</p>
                <div style="margin-bottom: 1.6rem;">
                    <a class="button-fill" href="/assets/products/cards.zip">DOWNLOAD PRODUCT (.ZIP)</a>
                </div>
                <p><u>Download Notes:</u> As this digital download consists of 40+ files, it was compressed in a .ZIP file. This mean you need to download a free unzipping software (which you can find online) if you don't have one already installed in your PC/smartphone (by default you should have one already installed).</p>
                <p>The following images show a preview of this product.</p>
                <div class="grid-2 gap-24">
                    <img src="/images/products/botanical-card-1.jpg">
                    <img src="/images/products/botanical-flashcard-pack-table.jpg">
                </div>
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

