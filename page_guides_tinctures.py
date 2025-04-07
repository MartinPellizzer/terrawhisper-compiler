import shutil

import g
import components

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
            <main style="margin-top: 24px; margin-bottom: 24px;" class="container-xl">
                {html_breadcrumbs}
                <div style="margin-top: 24px;" class="mob-flex gap-48">
                    <img class="flex-1" src="/images/guides/medicinal-herbal-tinctures-1-cover.jpg" alt="medicinal herbal tinctures edition 1 cover">
                    <div class="flex-1">
                        <span style="font-size: 14px; margin-bottom: 16px; display: inline-block; background-color: #c2410c; color: #ffffff; padding: 8px 16px;">FREE UNTIL APRIL 10</span>
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
                        <a class="button" href="/assets/pdf/medicinal-herbal-tinctures-1.pdf">FREE DOWNLOAD</a>
                    </div>
                </div>
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

shutil.copy2(
    f'assets/digital-products/medicinal-herbal-tinctures-1-cover.jpg', 
    f'{g.WEBSITE_FOLDERPATH}/images/guides/medicinal-herbal-tinctures-1-cover.jpg',
)
