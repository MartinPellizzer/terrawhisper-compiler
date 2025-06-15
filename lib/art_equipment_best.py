import os
import json
import random

import llm 

from lib import g
from lib import io
from lib import utils
from lib import components

from oliark_llm import llm_reply

model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

entities = io.csv_to_dict(f'database/entities/equipment.csv')
category = 'equipment'

def amazon_products_order(json_products_folderpath):
    products_jsons_filepaths = [f'{json_products_folderpath}/{x}' for x in os.listdir(json_products_folderpath)]
    products_jsons = []
    for i, product_json_filepath in enumerate(products_jsons_filepaths):
        print(f'{i}/{len(products_jsons_filepaths)} - {product_json_filepath}')
        product_data = io.json_read(product_json_filepath, create=True)
        product_asin = product_json_filepath.split('/')[-1].replace('.json', '')
        if 'reviews_num' in product_data:
            product_reviews_num = int(str(product_data['reviews_num']).replace('(', '').replace(')', ''))
        else:
            product_reviews_num = 0
        if 'reviews_score' in product_data:
            product_reviews_score = float(str(product_data['reviews_score']))
        else:
            product_reviews_score = 0
        product_reviews_score_total = product_reviews_num * product_reviews_score
        products_jsons.append({'product_asin': product_asin, 'reviews_score_total': product_reviews_score_total})
    products_jsons_ordered = sorted(products_jsons, key=lambda x: x['reviews_score_total'], reverse=True)
    products_jsons_filepaths_ordered = []
    for product_json in products_jsons_ordered:
        product_asin = product_json['product_asin']
        product_filepath = f'{json_products_folderpath}/{product_asin}.json'
        products_jsons_filepaths_ordered.append(product_filepath)
    return products_jsons_filepaths_ordered

def list_init_id_ai(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    main_lst_num = json_article['main_lst_num']
    equipment_slug = entity['entity_slug']
    ###
    json_products_folderpath = f'{g.AMAZON_FOLDERPATH}/json/{equipment_slug}'
    # order
    products_jsons_filepaths_ordered = amazon_products_order(json_products_folderpath)
    # ;product
    for i, product_json_filepath in enumerate(products_jsons_filepaths_ordered[:main_lst_num]):
        product_data = io.json_read(product_json_filepath)
        product_asin = product_json_filepath.split('/')[-1].replace('.json', '')
        # init product
        key = 'equipment_list'
        if key not in json_article: json_article[key] = []
        found = False
        for obj in json_article[key]:
            if obj['equipment_id'] == product_asin:
                found = True
                break
        if not found:
            if 'reviews_num' in product_data:
                product_reviews_num = int(str(product_data['reviews_num']).replace('(', '').replace(')', ''))
            else:
                product_reviews_num = 0
            if 'reviews_score' in product_data:
                product_reviews_score = float(str(product_data['reviews_score']))
            else:
                product_reviews_score = 0
            product_reviews_score_total = product_reviews_num * product_reviews_score
            product = {
                'equipment_id': product_asin,
                'equipment_url': product_data['url'],
                'equipment_affiliate_link': product_data['affiliate_link'],
                'equipment_title': product_data['title'],
                'equipment_description': product_data['description'],
                'equipment_price': product_data['price'],
                'equipment_reviews_num': product_reviews_num,
                'equipment_reviews_score': product_reviews_score,
                'equipment_reviews_score_total': product_reviews_score_total,
            }
            json_article[key].append(product)
        io.json_write(json_article_filepath, json_article)

def list_title_ai(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    if 'equipment_list' not in json_article: return
    for obj in json_article['equipment_list']:
        key = 'equipment_title_ai'
        if key not in obj: obj[key] = ''
        if regen: obj[key] = ''
        if obj[key] == '':
            equipment_title = obj['equipment_title']
            prompt = f'''
                Rewrite the following TITLE of a product using the following GUIDELINES: 
                {equipment_title}
                GUIDELINES:
                Reply in less than 10 words.
                Keep only the most important things for the TITLE.
                Keep the name of the brand if present at the beginning of the TITLE.
                Reply in the following JSON format: 
                {{"title": "insert the rewritten title here"}} 
                Only reply with the JSON.
                /no_think
            '''
            reply = llm_reply(prompt, model_path=model_filepath).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            try: json_data = json.loads(reply)
            except: json_data = {}
            if json_data != {}:
                try: line = json_data['title']
                except: continue
                obj[key] = line
                io.json_write(json_article_filepath, json_article)

def json_gen(entity, url):
    entity_name_singular = entity['entity_name_singular']
    entity_name_plural = entity['entity_name_plural']
    entity_slug = utils.sluggify(entity_name_singular)
    ###
    json_article_filepath = f'database/json/{url}.json'
    print(f'    >> JSON: {json_article_filepath}')
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url
    json_article['entity_slug'] = entity_slug
    json_article['entity_name_singular'] = entity_name_singular
    json_article['entity_name_plural'] = entity_name_plural
    json_article['title'] = f'{entity_name_plural} for herbalism'.title()
    if 'main_lst_num' not in json_article: json_article['main_lst_num'] = random.choice([7, 9, 11, 13])
    if 'lastmod' not in json_article: json_article['lastmod'] = utils.today()
    io.json_write(json_article_filepath, json_article)
    ###
    # intro_ai(entity, json_article_filepath, regen=False, clear=False)
    list_init_id_ai(entity, json_article_filepath, regen=False, clear=False)
    list_title_ai(entity, json_article_filepath, regen=False, clear=False)

def html_gen(url):
    json_article_filepath = f'database/json/{url}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url}.html'
    print(f'    >> HTML: {html_article_filepath}')
    json_article = io.json_read(json_article_filepath)
    entity_slug = json_article['entity_slug']
    entity_name_singular = json_article['entity_name_singular']
    entity_name_plural = json_article['entity_name_plural']
    main_lst_num = json_article['main_lst_num']
    title = json_article['title']
    page_title = f'best {entity_name_plural}'
    article_title = f'{main_lst_num} best {entity_name_plural} for herbalism'
    ###
    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    # html_article += f'{utils.text_format_sentences_html(json_article["intro"])}\n'
    ###
    html_breadcrumbs = components.breadcrumbs(f'{category}/{entity_slug}/best.html')
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
        os.mkdir(f'{g.WEBSITE_FOLDERPATH}/{category}/best')
    for entity_i, entity in enumerate(entities):
        print(f'\n>> {entity_i}/{len(entities)} - {entity}')
        entity_name_singular = entity['entity_name_singular']
        entity_name_plural = entity['entity_name_plural']
        entity_slug = utils.sluggify(entity_name_singular)
        url = f'{category}/{entity_slug}/best'
        obj = {
            'entity_slug': entity_slug,
            'entity_name_singular': entity_name_singular,
            'entity_name_plural': entity_name_plural,
        }
        json_gen(entity, url)
        html_gen(url)

