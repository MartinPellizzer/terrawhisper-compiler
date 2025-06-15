import os

from lib import g
from lib import components

def gen():
    html_folderpath = f'{g.WEBSITE_FOLDERPATH}/shop'
    html_filepath = f'{html_folderpath}/herb-drying-checklist.html'
    html_breadcrumbs = components.breadcrumbs(f'shop/herb-drying-checklist.html')
    page_title = f'the ultimate herb drying checklist'
    product_image_src = f'/images/shop/herb-drying-checklist-blurred.jpg'
    product_image_alt = f'herb drying checklist blurred'
    product_title ='the ultimate herb drying checklist'.title()
    product_subtitle ='(a.k.a. the "why didn\'t anyone tell me this sooner?" guide)'
    product_description = f'''
You grow your herbs. You love your herbs.
You harvest them with care... and then what?

You toss 'em in a paper bag and cross your fingers?
You hang 'em over your sink and hope they don't turn into green mush?

Yeah, I've done all that. And I've ruined more herbs than I care to admit.

So I made this thing.

<b style="color: #000000;">The Ultimate Herb Drying Checklist.</b>

No more guesswork. No more moldy bundles. No more "dang, that used to smell like something."

Here's what you get when you actually dry herbs the right way:

<ul><li>Herbs that don't mold for 1+ year. Like, for real. These babies can sit tight in a jar for a year or more and still be good.</li><li>Potent medicine for at least 6 months. Not sad, scentless leaves. We're talking strong, vibrant, ready-for-tea-and-tincture kinda herbs.</li><li>That satisfying feeling of "damn, I did that right." (Trust me, it hits.)</li></ul>

<b style="color: #000000;">And the best part? It's FREE.</b>

I'll send the checklist straight to your inbox. Just pop in your email below.
In return, you'll get signed up for The Apothecary Letter. My no-BS, plant-nerd newsletter where I talk herbal wisdom, witchy mishaps, and life lessons from the garden bed.

It's like a letter from a friend who smells like rosemary and says the quiet part out loud.

So if you're tired of moldy thyme and limp lemon balm...
If you want your herbs to work and not just look pretty in a jar...
If you're over winging it with herbs season after season (and ready to do it right)...

👇

Drop your email.
Grab the checklist.
Let's dry some damn herbs the right way.
    '''
    html_product_description = ''.join([f'<p>{line}</p>' for line in product_description.strip().split('\n') if line.strip() != ''])
    with open('assets/newsletter/herb-drying-checklist-js.txt') as f: sign_in_script = f.read()
    with open('assets/newsletter/herb-drying-checklist-component.txt') as f: sign_in_form = f.read()
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 16px; margin-bottom: 16px;" class="container-xl">
                {html_breadcrumbs}
                <div style="margin-top: 24px; align-items: start;" class="mob-flex gap-48">
                    <img class="flex-1" style="object-fit: contain;" src="{product_image_src}" alt="{product_image_alt}">
                    <div class="flex-1">
                        <h1>{product_title}</h1>
                        {html_product_description}
                        {sign_in_script}
                        <div style="max-width: 400px;">
                            {sign_in_form}
                        </div>
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


