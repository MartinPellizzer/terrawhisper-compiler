import os
import random
import shutil

from PIL import Image, ImageFont, ImageDraw

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read
from oliark import img_resize

from lib import g
from lib import io
# import lib_plants
from lib import data
from lib import utils
from lib import components

articles_folderpath = 'database/json'

meta_title = f'''Terrawhisper | Learn Medicinal Herbs & Craft Healing Remedies'''
meta_description = f'''Terrawhisper is your guide to natural wellness through herbalism. Whether you're just starting or growing a home apothecary, we give you the tools, confidence, and support to make effective, natural remedies with clarity and care.'''
meta_favicon = f'''<link rel="icon" href="/images-static/terrawhisper-favicon.ico">'''
meta_image = f'''<meta property="og:image" content="/images-static/medicinal-herbs.png">'''

def herb_to_html_card(herb_data):
    herb_name_scientific = herb_data['herb_name_scientific']
    herb_slug = herb_data['herb_slug']
    herb_url = f'/herbs/{herb_slug}.html'
    src = f'/images/ailments/herbs/{herb_slug}.jpg'
    alt = f'{herb_name_scientific}'.lower()
    filepath_in = f'{g.VAULT}/terrawhisper/images/realistic/herbs/1x1/{herb_slug}.jpg'
    filepath_out = f'{g.WEBSITE_FOLDERPATH}/images/herbs/{herb_slug}.jpg'
    # if not os.path.exists(filepath_out):
    if True:
        if os.path.exists(filepath_in):
            image = Image.open(filepath_in)
            image = img_resize(image)
            image.save(filepath_out)
    card_html = f'''
        <div>
            <a class="inline-block mb-48 no-underline" href="/herbs/{herb_slug}.html">
                <img src="{src}">
                <h2 class="mt-16 text-20 text-black">{herb_name_scientific.capitalize()}</h2>
            </a>
        </div>
    '''
    return card_html

def page_home_gen():
    title = 'Learn Herbalism, Live Healthier'.title()
    max_width = '992px'
    html_hero = f'''
        <section style="height: 70vh;">
            <div class="mob-flex" style="height: 100%; align-items: center;">
                <div style="flex: 1; height: 100%;">
                    <img style="object-fit: cover; height: 100%;" src="/images/medicinal-herbs.webp" alt="medicinal herbs">
                </div>
                <div style="flex: 1;">
                    <div style="max-width: {max_width}; padding-left: 32px; padding-right: 32px;">
                        <h1 class="playfair-display-regular" style="font-size: 96px; line-height: 1;">{title}</h1>
                        <p> Your beginner-friendly herbal encyclopedia for healing herbs, natural remedies, and home apothecary tools. Learn to harness nature's wisdom, one herb at a time.
                        </p>
                        <a class="ds-c-button-primary" href="#">Explore the Herb Encyclopedia</a>
                    </div>
                </div>
            </div>
        </section>
    '''

    ### about
    title = 'Welcome to TerraWhisper'
    html_business_definition = f'''
        <section style="">
            <div style="padding-top: 64px; padding-bottom: 64px; text-align: center;" class="container-md">
                <h2 style="font-size: 32px; text-align: center;" class="playfair-display-regular">{title}</h2>
                <p>Your beginner-friendly guide to herbal medicine and home apothecary wisdom.</p>
                <p>At TerraWhisper, we help curious herbalists and natural wellness seekers explore medicinal herbs, craft DIY remedies, and build their own home apothecaries. All with clear, gentle guidance.</p>
                <p>Whether you're easing a cold, calming anxiety, or starting your herbal toolkit, let the whispers of the Earth lead the way. </p>
            </div>
        </section>
    '''

    ### categories
    if 0:
        html_categories = f'''
            <section style="">
                <div style="padding-top: 64px; padding-bottom: 64px;" class="container-xl">
                    <h2 style="font-size: 32px; text-align: center;" class="playfair-display-regular">Core Sections Preview</h2>
                    <div style="display: flex; flex-wrap: wrap; gap: 16px;">
                        <div style="flex: 1;">
                            <img style="height: 480px; object-fit: cover;" src="/images/herbs/achillea-millefolium.jpg" alt="">
                            <h3 style="margin-top: 16px;">Medicinal Herbs</h3>
                            <p>Learn how to identify, grow, and use safe medicinal herbs for beginners. Your go-to guide for calendula, echinacea, chamomile and more.</p>
                            <div>
                                <a class="button-outline" href="/herbs.html">View Herbs</a>
                            </div>
                        </div>
                        <div style="flex: 1;">
                            <img style="height: 480px; object-fit: cover;" src="/images/ailments/anxiety-herbal-remedies.jpg" alt="">
                            <h3 style="margin-top: 16px;">Common Ailments</h3>
                            <p>Find natural herbal remedies for headaches, anxiety, colds, and more. Step-by-step DIY guides for common ailments.</p>
                            <div>
                                <a class="button-outline" href="/ailments.html">View Ailments</a>
                            </div>
                        </div>
                        <div style="flex: 1;">
                            <img style="height: 480px; object-fit: cover;" src="/images/equipment/cup.jpg" alt="">
                            <h3 style="margin-top: 16px;">Apothecary Equipment</h3>
                            <p>Equip your home apothecary with mortars and pestles, glassware, and infusion kits. Beginner-friendly tools for DIY herbal remedis.</p>
                            <div>
                                <a class="button-outline" href="/equipment.html">View Equipment</a>
                            </div>
                        </div>
                        <div style="flex: 1;">
                            <img style="height: 480px; object-fit: cover;" src="/images/preparations/tinctures/achillea-millefolium-herbal-tinctures.jpg" alt="">
                            <h3 style="margin-top: 16px;">Herbal Preparations</h3>
                            <p>Step-by-step DIY herbal remedy recipes for teas, salves, tinctures, syrups and more. Perect for beginner home apothecaries.</p>
                        </div>
                    </div>
                </div>
            </section>
        '''

    html_herbs = f'''
        <div style="display: flex; flex-wrap: wrap; gap: 64px; align-items: center;">
            <div style="flex: 4;">
                <h2 style="font-size: 32px;" class="playfair-display-regular">Medicinal Herbs</h2>
                <p>Learn how to identify, grow, and use safe medicinal herbs for beginners. Your go-to guide for calendula, echinacea, chamomile and more.</p>
                <div>
                    <a style="display: inline-block; background-color: #dddad5; text-decoration-line: none; color: #111111; padding: 12px 24px; text-transform: uppercase; letter-spacing: 2px;" class="playfair-display-regular" href="/herbs.html">View Herbs</a>
                </div>
            </div>
            <div style="flex: 3;">
                <img style="height: 480px; object-fit: cover;" src="/images/herbs/achillea-millefolium.jpg" alt="">
            </div>
        </div>
    '''

    html_ailments = f'''
        <div style="display: flex; flex-wrap: wrap; gap: 64px; align-items: center;">
            <div style="flex: 3;">
                <img style="height: 480px; object-fit: cover;" src="/images/ailments/anxiety-herbal-remedies.jpg" alt="">
            </div>
            <div style="flex: 4;">
                <h2 style="font-size: 32px;" class="playfair-display-regular">Common Ailments</h2>
                <p>Find natural herbal remedies for headaches, anxiety, colds, and more. Step-by-step DIY guides for common ailments.</p>
                <div>
                    <a style="display: inline-block; background-color: #dddad5; text-decoration-line: none; color: #111111; padding: 12px 24px; text-transform: uppercase; letter-spacing: 2px;" class="playfair-display-regular" href="/ailments.html">View Ailments</a>
                </div>
            </div>
        </div>
    '''

    html_categories = f'''
        <section style="">
            <div style="padding-top: 64px; padding-bottom: 64px; display: flex; flex-direction: column; gap: 64px;" class="container-xl">
                {html_herbs}
                {html_ailments}
            </div>
        </section>
    '''

    if 0:
        ### articles
        ### herbs
        cards = []
        herbs_books = data.herbs_books_get()
        herbs = []
        for herb in herbs_books: herbs.append(herb)
        herbs = list(set(herbs))
        herbs = sorted(herbs)
        random.shuffle(herbs)
        for herb_i, herb in enumerate(herbs[:4]):
            print(f'{herb_i}/{len(herbs)} - {herb}')
            herb_name_scientific = herb.strip().lower()
            herb_slug = utils.sluggify(herb_name_scientific)
            url = f'herbs/{herb_slug}/benefits'
            json_article_filepath = f'{articles_folderpath}/{url}.json'
            json_article = io.json_read(json_article_filepath)
            article_title = json_article['title']
            herb_card = f'''
                <div>
                    <img src="/images/herbs/{herb_slug}.jpg">
                    <h3 style="margin-top: 16px;">{article_title}</h3>
                </div>
            '''
            cards.append(herb_card)
        ### ailments
        ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
        for ailment_i, ailment in enumerate(ailments[:4]):
            print(f'\n>> {ailment_i}/{len(ailments)} - {ailment}')
            ailment_slug = ailment['ailment_slug']
            url = f'ailments/{ailment_slug}/teas'
            json_article_filepath = f'database/json/{url}.json'
            json_article = io.json_read(json_article_filepath)
            article_title = json_article['title']
            herb_card = f'''
                <div>
                    <img src="/images/preparations/{ailment_slug}-herbal-teas.jpg">
                    <h3 style="margin-top: 16px;">{article_title}</h3>
                </div>
            '''
            cards.append(herb_card)

        cards = '\n'.join(cards)

        html_articles = f'''
            <section style="">
                <div style="padding-top: 64px; padding-bottom: 64px;" class="container-xl">
                    <h2 style="font-size: 32px; text-align: center;" class="playfair-display-regular">Core Sections Preview</h2>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px">
                        {cards}
                    </div>
                </div>
            </section>
        '''

    html_articles = ''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        {meta_favicon}
        {meta_image}
        <body>
            {components.html_header()}
            <main>
                {html_hero}
                {html_business_definition}
                {html_categories}
                {html_articles}
            </main>
            <div class="mt-64"></div>
            {components.html_footer()}
        </body>
        </html>
    '''
    html_filepath = f'{g.WEBSITE_FOLDERPATH}/index.html'
    with open(html_filepath, 'w') as f: f.write(html)

shutil.copy2('style.css', f'{g.WEBSITE_FOLDERPATH}/style.css')
page_home_gen()
