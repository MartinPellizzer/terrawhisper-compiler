import os

import llm 

from lib import g
from lib import io
from lib import utils
from lib import components

model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

entities = io.csv_to_dict(f'database/entities/equipment.csv')
category = 'equipment'
sentence_n_master = 4
reply_debug = False

paragraphs_failed = []

def intro_ai(entity, json_article_filepath, regen=False, clear=False):
    entity_name_plural = entity['entity_name_plural']
    json_article = io.json_read(json_article_filepath)
    reply_start = f'{entity_name_plural.capitalize()} '
    if reply_start != '': reply_start_prompt = f'Start with the following words: {reply_start}.'
    else: reply_start_prompt = ''
    sentence_n = sentence_n_master
    llm.paragraph_ai(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a {sentence_n}-sentence paragraph about the following equipment for herbalism: {entity_name_plural}.
            Include brief introduction of the equipment.
            Include an explanation of its relevance in herbalism or home apothecaries.
            Reply in english and use only english characters.
            If you can't answer, reply with only "I can't reply".
            {reply_start_prompt}
            /no_think
        ''',
        sentence_n = sentence_n,
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def definition_ai(entity, json_article_filepath, regen=False, clear=False):
    entity_name_plural = entity['entity_name_plural']
    json_article = io.json_read(json_article_filepath)
    reply_start = f'{entity_name_plural.capitalize()} are '
    if reply_start != '': reply_start_prompt = f'Start with the following words: {reply_start}.'
    else: reply_start_prompt = ''
    sentence_n = sentence_n_master
    llm.paragraph_ai(
        key = 'definition',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a 4-sentence paragraph about the following equipment for herbalism: {entity_name_plural}.
            Include a definition of the equipment.
            Include a description of its basic design and components.
            Include a description of its primary purpose.
            Reply in english and use only english characters.
            If you can't answer, reply with only "I can't reply".
            {reply_start_prompt}
            /no_think
        ''',
        sentence_n = sentence_n,
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def uses_ai(entity, json_article_filepath, regen=False, clear=False):
    entity_name_plural = entity['entity_name_plural']
    json_article = io.json_read(json_article_filepath)
    reply_start = f'{entity_name_plural} are used to '.capitalize()
    if reply_start != '': reply_start_prompt = f'Start with the following words: {reply_start}.'
    else: reply_start_prompt = ''
    sentence_n = sentence_n_master
    sentence_n = 5
    llm.paragraph_ai(
        key = 'uses',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a {sentence_n}-sentence paragraph about what are the main uses of the following equipment in herbalism: {entity_name_plural}.
            Include a lot of examples of uses.
            Reply in english and use only english characters.
            If you can't answer, reply with only "I can't reply".
            {reply_start_prompt}
            /no_think
        ''',
        sentence_n = sentence_n,
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def variations_ai(entity, json_article_filepath, regen=False, clear=False):
    entity_name_plural = entity['entity_name_plural']
    json_article = io.json_read(json_article_filepath)
    reply_start = f''
    if reply_start != '': reply_start_prompt = f'Start with the following words: {reply_start}.'
    else: reply_start_prompt = ''
    sentence_n = sentence_n_master
    llm.paragraph_ai(
        key = 'variations',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a detailed paragraph about the variations of the following equipment for herbalism: {entity_name_plural}.
            Include an overview of different types/models/sizes.
            Include pros and cons of each.
            Reply in english and use only english characters.
            If you can't answer, reply with only "I can't reply".
            {reply_start_prompt}
            /no_think
        ''',
        sentence_n = '',
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def how_to_ai(entity, json_article_filepath, regen=False, clear=False):
    entity_name_plural = entity['entity_name_plural']
    json_article = io.json_read(json_article_filepath)
    reply_start = f''
    if reply_start != '': reply_start_prompt = f'Start with the following words: {reply_start}.'
    else: reply_start_prompt = ''
    sentence_n = sentence_n_master
    llm.paragraph_ai(
        key = 'how_to',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a detailed paragraph about how do you use the following equipment in herbalism: {entity_name_plural}.
            Reply in english and use only english characters.
            If you can't answer, reply with only "I can't reply".
            {reply_start_prompt}
            /no_think
        ''',
        sentence_n = '',
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def best_practices_ai(entity, json_article_filepath, regen=False, clear=False):
    entity_name_plural = entity['entity_name_plural']
    json_article = io.json_read(json_article_filepath)
    reply_start = f''
    if reply_start != '': reply_start_prompt = f'Start with the following words: {reply_start}.'
    else: reply_start_prompt = ''
    sentence_n = sentence_n_master
    llm.paragraph_ai(
        key = 'best_practices',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a 4-sentence paragraph about the following equipment for herbalism: {entity_name_plural}.
            In sentence 1, write about safety tips.
            In sentence 2, write about storage tips.
            In sentence 3, write about cleaning tips.
            In sentence 4, write about maintenance tips.
            Reply in english and use only english characters.
            If you can't answer, reply with only "I can't reply".
            {reply_start_prompt}
            /no_think
        ''',
        sentence_n = sentence_n,
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def best_preparations_ai(entity, json_article_filepath, regen=False, clear=False):
    entity_name_plural = entity['entity_name_plural']
    json_article = io.json_read(json_article_filepath)
    reply_start = f''
    if reply_start != '': reply_start_prompt = f'Start with the following words: {reply_start}.'
    else: reply_start_prompt = ''
    sentence_n = sentence_n_master
    llm.paragraph_ai(
        key = 'best_preparations',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a 4-sentence paragraph about the top herbs and preparations you can make with the following equipment for herbalism: {entity_name_plural}.
            Include list of herbs or remedies best suited to use with this equipment.
            Include quick recipe ideas of diy suggestions.
            Reply in english and use only english characters.
            If you can't answer, reply with only "I can't reply".
            {reply_start_prompt}
            /no_think
        ''',
        sentence_n = sentence_n,
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def json_gen(entity):
    entity_name_singular = entity['entity_name_singular']
    entity_name_plural = entity['entity_name_plural']
    entity_slug = utils.sluggify(entity_name_singular)
    ###
    url_partial = f'{category}/{entity_slug}'
    json_article_filepath = f'{g.JSONS_ARTICLES_FOLDERPATH}/{url_partial}.json'
    print(f'    >> JSON: {json_article_filepath}')
    ###
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_partial
    json_article['entity_slug'] = entity_slug
    json_article['entity_name_singular'] = entity_name_singular
    json_article['entity_name_plural'] = entity_name_plural
    json_article['title'] = f'{entity_name_plural} for herbalism'.title()
    if 'lastmod' not in json_article: json_article['lastmod'] = utils.today()
    io.json_write(json_article_filepath, json_article)
    ###
    intro_ai(entity, json_article_filepath, regen=False, clear=False)
    definition_ai(entity, json_article_filepath, regen=True, clear=True)
    uses_ai(entity, json_article_filepath, regen=True, clear=True)
    variations_ai(entity, json_article_filepath, regen=True, clear=True)
    how_to_ai(entity, json_article_filepath, regen=True, clear=True)
    best_practices_ai(entity, json_article_filepath, regen=True, clear=True)
    best_preparations_ai(entity, json_article_filepath, regen=True, clear=True)

def html_gen(entity):
    global paragraphs_failed_n
    entity_name_singular = entity['entity_name_singular']
    entity_name_plural = entity['entity_name_plural']
    entity_slug = utils.sluggify(entity_name_singular)
    ###
    url_partial = f'{category}/{entity_slug}'
    json_article_filepath = f'{g.JSONS_ARTICLES_FOLDERPATH}/{url_partial}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url_partial}.html'
    print(f'    >> HTML: {html_article_filepath}')
    ###
    json_article = io.json_read(json_article_filepath)
    entity_slug = json_article['entity_slug']
    entity_name_singular = json_article['entity_name_singular']
    entity_name_plural = json_article['entity_name_plural']
    article_title = json_article['title']
    page_title = article_title
    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    html_article += f'{utils.text_format_sentences_html(json_article["intro"])}\n'
    if os.path.exists(f'{g.WEBSITE_FOLDERPATH}/{url_partial}/best.html'):
        html_article += f'<a href="/{url_partial}/best.html">Best {entity_name_plural} for herbalism</a>\n'
    if 'definition' in json_article:
        err = False
        for reply_error in llm.reply_errors:
            if json_article['definition'].startswith(reply_error):
                paragraphs_failed.append('definition')
                err = True
                break
        if not reply_debug:
            if not err and json_article['definition'] != '':
                html_article += f'<h2>What are {entity_name_plural}?</h2>\n'
                html_article += f'{utils.text_format_sentences_html(json_article["definition"])}\n'
        else:
            html_article += f'<h2>What are {entity_name_plural}?</h2>\n'
            html_article += f'{utils.text_format_sentences_html(json_article["definition"])}\n'
    if 'uses' in json_article:
        err = False
        for reply_error in llm.reply_errors:
            if json_article['uses'].startswith(reply_error):
                paragraphs_failed.append('uses')
                err = True
                break
        if not reply_debug:
            if not err and json_article['uses'] != '':
                html_article += f'<h2>Why herbalists use {entity_name_plural}?</h2>\n'
                html_article += f'{utils.text_format_1N1_html(json_article["uses"])}\n'
        else:
            html_article += f'<h2>Why herbalists use {entity_name_plural}?</h2>\n'
            html_article += f'{utils.text_format_1N1_html(json_article["uses"])}\n'
    if 'variations' in json_article:
        err = False
        for reply_error in llm.reply_errors:
            if json_article['variations'].startswith(reply_error):
                paragraphs_failed.append('variations')
                err = True
                break
        if not reply_debug:
            if not err and json_article['variations'] != '':
                html_article += f'<h2>Types of {entity_name_plural}</h2>\n'
                html_article += f'{utils.text_format_sentences_html(json_article["variations"])}\n'
        else:
            html_article += f'<h2>Types of {entity_name_plural}</h2>\n'
            html_article += f'{utils.text_format_sentences_html(json_article["variations"])}\n'
    if 'how_to' in json_article:
        err = False
        for reply_error in llm.reply_errors:
            if json_article['how_to'].startswith(reply_error):
                paragraphs_failed.append('how_to')
                err = True
                break
        if not reply_debug:
            if not err and json_article['how_to'] != '':
                html_article += f'<h2>How to use {entity_name_plural}</h2>\n'
                html_article += f'{utils.text_format_sentences_html(json_article["how_to"])}\n'
        else:
            html_article += f'<h2>How to use {entity_name_plural}</h2>\n'
            html_article += f'{utils.text_format_sentences_html(json_article["how_to"])}\n'
    if 'best_practices' in json_article:
        err = False
        for reply_error in llm.reply_errors:
            if json_article['best_practices'].startswith(reply_error):
                paragraphs_failed.append('best_practices')
                err = True
                break
        if not reply_debug:
            if not err and json_article['best_practices'] != '':
                html_article += f'<h2>Best practices and tips for herbalists</h2>\n'
                html_article += f'{utils.text_format_sentences_html(json_article["best_practices"])}\n'
        else:
            html_article += f'<h2>Best practices and tips for herbalists</h2>\n'
            html_article += f'{utils.text_format_sentences_html(json_article["best_practices"])}\n'
    if 'best_preparations' in json_article:
        err = False
        for reply_error in llm.reply_errors:
            if json_article['best_preparations'].startswith(reply_error):
                paragraphs_failed.append('best_preparations')
                err = True
                break
        if not reply_debug:
            if not err and json_article['best_preparations'] != '':
                html_article += f'<h2>Top preparations to make with {entity_name_plural}</h2>\n'
                html_article += f'{utils.text_format_sentences_html(json_article["best_preparations"])}\n'
        else:
            html_article += f'<h2>Top preparations to make with {entity_name_plural}</h2>\n'
            html_article += f'{utils.text_format_sentences_html(json_article["best_preparations"])}\n'
    html_breadcrumbs = components.breadcrumbs(f'{category}/{entity_slug}.html')
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
    for entity_i, entity in enumerate(entities):
        print(f'\n>> {entity_i}/{len(entities)} - {entity}')
        json_gen(entity)
        html_gen(entity)
        # break
    print(paragraphs_failed)
    print(len(paragraphs_failed))

