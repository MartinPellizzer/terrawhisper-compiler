import os
import json

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from oliark_io import json_read
from oliark_llm import llm_reply
from oliark import img_resize

import llm
import studies

from lib import g
from lib import io
from lib import data
from lib import utils
from lib import components

category_slug = 'preparations'
articles_folderpath = 'database/json'
model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

def ai_intro(preparation, herb, json_article_filepath, regen=False, clear=False):
    preparation_slug = preparation['entity_slug']
    preparation_name_singular = preparation['entity_name_singular']
    preparation_name_plural = preparation['entity_name_plural']
    ###
    herb_slug = herb['herb_slug']
    herb_name_scientific = herb['herb_name_scientific']
    ###
    json_article = io.json_read(json_article_filepath)
    reply_start = f'{herb_name_scientific.capitalize()} {preparation_name_singular.lower()} is '
    llm.paragraph_ai(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 5-sentence paragraph about the following herbal preparation: {herb_name_scientific.capitalize()} {preparation_name_singular.lower()}.
            Explain what this preparation is and how it's used in herbalism for medicinal purposes.
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

def json_gen(preparation, herb, url_relative):
    preparation_slug = preparation['entity_slug']
    preparation_name_singular = preparation['entity_name_singular']
    preparation_name_plural = preparation['entity_name_plural']
    ###
    herb_slug = herb['herb_slug']
    herb_name_scientific = herb['herb_name_scientific']
    ###
    json_article_filepath = f'{articles_folderpath}/{url_relative}.json'
    print(f'    >> JSON: {json_article_filepath}')
    json_article = io.json_read(json_article_filepath, create=True)
    if 'lastmod' not in json_article: json_article['lastmod'] = utils.today()
    json_article['url'] = url_relative
    json_article['entity_slug'] = f'{herb_slug}/{preparation_slug}'
    json_article['entity_name_singular'] = f'{herb_name_scientific}/{preparation_name_singular}'
    json_article['entity_name_plural'] = f'{herb_name_scientific}/{preparation_name_plural}'
    json_article['title'] = f'''{herb_name_scientific.capitalize()} {preparation_name_singular.lower()} for medicinal use'''
    io.json_write(json_article_filepath, json_article)
    ###
    ai_intro(preparation, herb, json_article_filepath, regen=False, clear=False)

def html_gen(preparation, herb, url_relative):
    preparation_slug = preparation['entity_slug']
    preparation_name_singular = preparation['entity_name_singular']
    preparation_name_plural = preparation['entity_name_plural']
    ###
    herb_slug = herb['herb_slug']
    herb_name_scientific = herb['herb_name_scientific']
    ###
    json_article_filepath = f'database/json/{url_relative}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url_relative}.html'
    print(f'    >> JSON: {json_article_filepath}')
    print(f'    >> HTML: {html_article_filepath}')
    json_article = io.json_read(json_article_filepath)
    article_title = json_article['title']
    page_title = article_title
    ###
    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    html_article += f'''
        <img style="margin-bottom: 16px;" 
        src="/images/preparations/{herb_slug}-{preparation_slug}.jpg" 
        alt="{herb_name_scientific} {preparation_name_singular}">
    '''
    key = 'intro'
    if key in json_article:
        if json_article[key][0] != '[':
            html_article += f'''{utils.text_format_1N1_html(json_article[key])}\n'''
    html_article += f'[html_intro_toc]\n'
    ###
    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    html_breadcrumbs = components.breadcrumbs(f'{category_slug}/{preparation_slug}/{herb_slug}.html')
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
    if not os.path.exists(f'{g.WEBSITE_FOLDERPATH}/{category_slug}'): 
        os.mkdir(f'{g.WEBSITE_FOLDERPATH}/{category_slug}')
    ###
    preparation_list = io.csv_to_dict(f'database/entities/preparations.csv')
    for preparation_i, preparation in enumerate(preparation_list):
        print(f'{preparation_i}/{len(preparation_list)} - {preparation}')
        preparation_slug = preparation['entity_slug']
        preparation_name_singular = preparation['entity_name_singular']
        preparation_name_plural = preparation['entity_name_plural']
        ###
        if not os.path.exists(f'{g.WEBSITE_FOLDERPATH}/{category_slug}/{preparation_slug}'): 
            os.mkdir(f'{g.WEBSITE_FOLDERPATH}/{category_slug}/{preparation_slug}')
        ###
        herb_list = data.preparations_popular_100_get(preparation_slug)
        for herb in herb_list:
            herb_slug = herb['herb_slug']
            herb_name_scientific = herb['herb_name_scientific']
            url_relative = f'{category_slug}/{preparation_slug}/{herb_slug}'
            json_gen(preparation, herb, url_relative)
            # imgs_gen(preparation, url_relative)
            html_gen(preparation, herb, url_relative)
            # quit()
            print(url_relative)
