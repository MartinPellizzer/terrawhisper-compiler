import os

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read

import g
import llm
from lib import io
from lib import utils
from lib import components

def intro_ai(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    llm.ai_paragraph_gen(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the herbal remedies used to treat the {ailment_name} ailment.
            Include a definition of what {ailment_name} is.
            Include the benefits of herbal remedies to treat this ailment.
            Include a lot of examples of herbs names to treat this ailment and explain why.
            Include a lot of examples of herbal preparations to treat this ailment and explain why.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {ailment_name.capitalize()} is .
        ''',
        regen = regen,
        print_prompt = True,
    )

def causes_ai(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    reply_start = f'The primary causes of {ailment_name.lower()} are '
    sentence_n = 4 
    llm.ai_paragraph_gen(
        key = 'causes',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        sentence_n = sentence_n, 
        reply_start = reply_start,
        prompt = f'''
            Write a short {sentence_n}-sentence paragraph about the causes of the following ailment: {ailment_name}.
            Include the primary causes of this ailment and explain why.
            Include examples of secondary causes of this ailment and explain why.
            Include examples of lifestyles that increases the chances you develop this ailment and explain why.
            Don't repeat yourself.
            Make sure you write only {sentence_n} sentences.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {reply_start}.
        ''',
        regen = regen,
        clear = clear,
        print_prompt = True,
    )

def herbs_ai(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    reply_start = f'The medicinal herbs used to treat {ailment_name.lower()} are '
    sentence_n = 4 
    llm.ai_paragraph_gen(
        key = 'herbs',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        sentence_n = sentence_n, 
        reply_start = reply_start,
        prompt = f'''
            Write a short {sentence_n}-sentence paragraph about the herbs that heal the following ailment: {ailment_name}.
            Include examples of herbs that heal this ailment.
            Include examples of therapeutic actions these herbs have that treat this ailment.
            Include examples of bioactive compounds these herbs have that treat this ailment.
            Don't repeat yourself.
            Make sure you write only {sentence_n} sentences.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {reply_start}.
        ''',
        regen = regen,
        clear = clear,
        print_prompt = True,
    )

def preparations_ai(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    reply_start = f'The herbal preparations used to treat {ailment_name.lower()} are '
    sentence_n = 4 
    llm.ai_paragraph_gen(
        key = 'preparations',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        sentence_n = sentence_n, 
        reply_start = reply_start,
        prompt = f'''
            Write a short {sentence_n}-sentence paragraph about the herbal preparations that are used to treat the following ailment: {ailment_name}.
            By herbal preparations I mean things like: teas, infusions, etc...
            Include a lot of examples of herbal preparations that heal this ailment and explain why.
            Don't include the names of herbs used to make the preaprations.
            Don't repeat yourself.
            Make sure you write only {sentence_n} sentences.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {reply_start}.
        ''',
        regen = regen,
        clear = clear,
        print_prompt = True,
    )


def json_gen(url, ailment):
    json_article_filepath = f'database/json/{url}.json'
    ailment_slug = ailment['ailment_slug']
    ailment_name = ailment['ailment_name']
    print(f'    >> JSON: {json_article_filepath}')

    json_article = json_read(json_article_filepath, create=True)
    json_article['url'] = url
    json_article['ailment_slug'] = ailment_slug
    json_article['ailment_name'] = ailment_name
    json_article['title'] = f'{ailment_name} causes, medicinal herbs and herbal preparations'.title()
    if 'lastmod' not in json_article: json_article['lastmod'] = utils.today()
    io.json_write(json_article_filepath, json_article)

    intro_ai(json_article_filepath, regen=False)
    causes_ai(json_article_filepath, regen=False, clear=False)
    herbs_ai(json_article_filepath, regen=False, clear=False)
    preparations_ai(json_article_filepath, regen=False, clear=False)

def html_gen(url):
    json_article_filepath = f'database/json/{url}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url}.html'
    print(f'    >> HTML: {html_article_filepath}')
    print(f'    >> JSON: {json_article_filepath}')

    json_article = json_read(json_article_filepath)
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    article_title = json_article['title']
    page_title = article_title

    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    html_article += f'''
        <img style="margin-bottom: 16px;" 
        src="/images/ailments/{ailment_slug}-herbal-remedies.jpg" 
        alt="herbal remedies for {ailment_name}">
    '''
    html_article += f'{utils.text_format_sentences_html(json_article["intro"])}\n'
    html_article += f'<h2>What causes {ailment_name}?</h2>\n'
    html_article += f'{utils.text_format_sentences_html(json_article["causes"])}\n'
    html_article += f'<h2>What herbs heal {ailment_name}?</h2>\n'
    html_article += f'{utils.text_format_sentences_html(json_article["herbs"])}\n'
    html_article += f'<h2>What preparations treat {ailment_name}?</h2>\n'
    html_article += f'{utils.text_format_sentences_html(json_article["preparations"])}\n'
    html_article += f'<p>The articles in the following links discuss in detail the best herbal preparation used to treat {ailment_name}.</p>\n'
    html_article += f'<ul>\n'
    preparations_slugs = [
        'teas',
        'tinctures',
        'essential-oils',
        'creams',
    ]
    for preparation_slug in preparations_slugs:
        json_article_preparation_filepath = f'database/json/{url}/{preparation_slug}.json'
        json_article_preparation = json_read(json_article_preparation_filepath)
        json_article_preparation_title = json_article_preparation['title']
        html_article_preparation_filepath = f'/{url}/{preparation_slug}.html'
        html_article += f'<li><a href="{html_article_preparation_filepath}">{json_article_preparation_title}</a></li>\n'
    html_article += f'</ul>\n'

    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    html_breadcrumbs = components.breadcrumbs(f'ailments/{ailment_slug}.html')
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
    category = 'ailments'
    if not os.path.exists(f'{g.WEBSITE_FOLDERPATH}/{category}'): 
        os.mkdir(f'{g.WEBSITE_FOLDERPATH}/{category}')

    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        print(f'\n>> {ailment_i}/{len(ailments)} - {ailment}')
        ailment_slug = ailment['ailment_slug']
        url = f'{category}/{ailment_slug}'
        json_gen(url, ailment)
        html_gen(url)
