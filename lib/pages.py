import shutil

import g
import components

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

shutil.copy2('style.css', f'{g.WEBSITE_FOLDERPATH}/style.css')
# page_guides()

