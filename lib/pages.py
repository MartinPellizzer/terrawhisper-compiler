import g

import components

def page_guides():
    cards = []
    card = f'''
        <a class="article-card no-underline text-black" href="/guides/checklist-dry-herbs.html">
            <div class="">
                <img class="mb-16" src="/images-static/checklist-dry-herbs.jpg" alt="herb drying checklist">
                <h2 class="h2-plain text-18 mb-12">The Ultimate Herb Drying Checklist</h2>
            </div>
        </a>
    '''
    cards.append(card)
    cards = ''.join(cards)

    section_1 = f'''
        <section class="mt-48 mb-48">
            <div class="container-md">
                <div class="grid grid-3 gap-16">
                    {cards}
                </div>
            </div>
        </section>
    '''

    html_filepath = f'{g.WEBSITE_FOLDERPATH}/guides.html'
    breadcrumbs_html = components.breadcrumbs(f'guides.html')
    page_title = f'terrawhisper guides on herbalism an herbal medicine'
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            {breadcrumbs_html}
            <main>
                {section_1}
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)


