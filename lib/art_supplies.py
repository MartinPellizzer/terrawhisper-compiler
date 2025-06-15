import os

import llm 

from lib import g
from lib import io
from lib import utils
from lib import components

category = 'supplies'

def intro_ai(json_article_filepath, regen=False):
    json_article = io.json_read(json_article_filepath)
    supply_slug = json_article['supply_slug']
    supply_name_singular = json_article['supply_name_singular']
    supply_name_plural = json_article['supply_name_plural']
    llm.ai_paragraph_gen(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the following supply for herbalism: {supply_name_plural}.
            Include a definition of what {supply_name_plural} are.
            Include examples of usages of this supply in herbalism.
            Include examples of why this supply is important in herbalims.
            Include examples of how this supply can improve an herbalist life.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {supply_name_plural.capitalize()} are .
        ''',
        regen = regen,
        print_prompt = True,
    )

def json_gen(url, supply):
    json_article_filepath = f'database/json/{url}.json'
    supply_slug = supply['supply_slug']
    supply_name_singular = supply['supply_name_singular']
    supply_name_plural = supply['supply_name_plural']
    print(f'    >> JSON: {json_article_filepath}')
    ###
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url
    json_article['supply_slug'] = supply_slug
    json_article['supply_name_singular'] = supply_name_singular
    json_article['supply_name_plural'] = supply_name_plural
    json_article['title'] = f'{supply_name_plural} for herbalism'.title()
    if 'lastmod' not in json_article: json_article['lastmod'] = utils.today()
    io.json_write(json_article_filepath, json_article)
    ###
    intro_ai(json_article_filepath, regen=False)

def html_gen(url):
    json_article_filepath = f'database/json/{url}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url}.html'
    print(f'    >> HTML: {html_article_filepath}')
    print(f'    >> JSON: {json_article_filepath}')
    json_article = io.json_read(json_article_filepath)
    supply_slug = json_article['supply_slug']
    supply_name_singular = json_article['supply_name_singular']
    supply_name_plural = json_article['supply_name_plural']
    article_title = json_article['title']
    page_title = article_title
    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    html_article += f'{utils.text_format_sentences_html(json_article["intro"])}\n'
    '''
    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    '''
    html_breadcrumbs = components.breadcrumbs(f'{category}/{supply_slug}.html')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 24px;" class="container-md mob-flex gap-48">
                <article class="article">
                    {html_breadcrumbs}
                    {html_article}
                </article>
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    html_article_folderpath = '/'.join(html_article_filepath.split('/')[:-1])
    if not os.path.exists(html_article_folderpath): os.mkdir(html_article_folderpath)
    with open(html_article_filepath, 'w') as f: f.write(html)

def gen():
    if not os.path.exists(f'{g.WEBSITE_FOLDERPATH}/{category}'): 
        os.mkdir(f'{g.WEBSITE_FOLDERPATH}/{category}')
    supplies = [
        {
            'supply_name_singular': 'jar',
            'supply_name_plural': 'jars',
        },
    ]
    for supply_i, supply in enumerate(supplies):
        print(f'\n>> {supply_i}/{len(supplies)} - {supply}')
        supply_name_singular = supply['supply_name_singular']
        supply_name_plural = supply['supply_name_plural']
        supply_slug = utils.sluggify(supply_name_singular)
        url = f'{category}/{supply_slug}'
        obj = {
            'supply_slug': supply_slug,
            'supply_name_singular': supply_name_singular,
            'supply_name_plural': supply_name_plural,
        }
        json_gen(url, obj)
        html_gen(url)
