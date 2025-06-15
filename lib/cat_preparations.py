import os

import llm

from lib import g
from lib import io
from lib import utils
from lib import components

category = 'preparations'
model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

def ai_intro(json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    llm.paragraph_ai(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a 5-sentence paragraph about the herbal preparations used in herbalism as natural remedies.
            Include preparations such as teas, infusions, decoctions, creams, etc.
            /no_think
        ''',
        reply_start = '',
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def ai_list_init(json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    if clear:
        json_article['preparation_list'] = []
        io.json_write(json_article_filepath, json_article)
        return
    if regen:
        json_article['preparation_list'] = []
        io.json_write(json_article_filepath, json_article)
    if 'preparation_list' not in json_article: json_article['preparation_list'] = []
    entity_list = io.csv_to_dict(f'database/entities/preparations.csv')
    json_preparation_list = json_article['preparation_list']
    for entity in entity_list:
        found = False
        for json_preparation in json_preparation_list:
            if json_preparation['entity_slug'] == entity['entity_slug']:
                found = True
                break
        if not found:
            json_preparation_list.append(entity)
    json_article['preparation_list'] = json_preparation_list
    io.json_write(json_article_filepath, json_article)

def ai_list_desc(json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    entity_list = json_article['preparation_list']
    for obj_i, obj in enumerate(entity_list):
        print(f'{obj_i}/{len(entity_list)}')
        entity_slug = obj['entity_slug']
        entity_name_singular = obj['entity_name_singular']
        entity_name_plural = obj['entity_name_plural']
        reply_start = f'{entity_name_plural.capitalize()} ar '
        llm.paragraph_ai(
            key = 'desc',
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write a short 5-sentence paragraph about the following herbal preparation: {entity_name_plural}.
                Explain what this preparation is and how is used in herbalism for medicinal purposes.
                If you can't answer, reply with only "I can't reply".
                Start with the following words: {reply_start} .
                /no_think
            ''',
            reply_start = reply_start,
            regen = regen,
            clear = clear,
            print_prompt = True,
            model_filepath = model_filepath,
        )

def json_gen(url_relative):
    json_article_filepath = f'database/json/{url_relative}.json'
    print(f'    >> JSON: {json_article_filepath}')
    json_article = io.json_read(json_article_filepath, create=True)
    if 'lastmod' not in json_article: json_article['lastmod'] = utils.today()
    json_article['url'] = url_relative
    json_article['title'] = f'herbal preaprations'.title()
    io.json_write(json_article_filepath, json_article)
    ###
    ai_intro(json_article_filepath, regen=False, clear=False)
    ai_list_init(json_article_filepath, regen=False, clear=False)
    ai_list_desc(json_article_filepath, regen=False, clear=False)

def html_gen(url_relative):
    json_article_filepath = f'database/json/{url_relative}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url_relative}.html'
    print(f'    >> HTML: {html_article_filepath}')
    json_article = io.json_read(json_article_filepath)
    article_title = json_article['title']
    page_title = article_title
    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    if json_article['intro'] != '':
        html_article += f'{utils.text_format_1N1_html(json_article["intro"])}\n'
    if json_article['preparation_list'] != '':
        for entity in json_article['preparation_list']:
            html_article += f'<h2>{entity["entity_name_plural"].title()}</h2>\n'
            html_article += f'''
                <img style="margin-bottom: 16px;" 
                src="/images/preparations/{entity["entity_slug"]}.jpg" 
                alt="{entity["entity_name_singular"]}">
            '''
            html_article += f'{utils.text_format_1N1_html(entity["desc"])}\n'
            html_article += f'''<p>Learn more about <a href="/{category}/{entity['entity_slug']}.html">{entity['entity_name_plural']}</a>.</p>\n'''
    html_breadcrumbs = components.breadcrumbs(f'{url_relative}.html')
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

def entity_gen(row):
    entity_slug = row['entity_slug']
    entity_name_singular = row['entity_name_singular']
    entity_name_plural = row['entity_name_plural']
    url_relative = f'{category}/{entity_slug}'
    json_entity_filepath = f'{g.ENTITIES_FOLDERPATH}/{url_relative}.json'
    json_entity = io.json_read(json_entity_filepath, create=True)
    if 'lastmod' not in json_entity: json_entity['lastmod'] = utils.today()
    json_entity['url'] = url_relative
    json_entity['entity_slug'] = entity_slug
    json_entity['entity_name_singular'] = entity_name_singular
    json_entity['entity_name_plural'] = entity_name_plural
    io.json_write(json_entity_filepath, json_entity)

def gen():
    rows = io.csv_to_dict(f'database/entities/preparations.csv')
    for row_i, row in enumerate(rows):
        print(f'\n>> ROW: {row_i}/{len(rows)} - {row}')
        entity_gen(row)

    url_relative = f'{category}'
    json_gen(url_relative)
    html_gen(url_relative)
