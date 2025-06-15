import os
import json
import random

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read
from oliark_llm import llm_reply

import llm
import studies

from lib import g
from lib import io
from lib import data
from lib import utils
from lib import components

category_slug = 'herbs'
attribute_slug = 'preparations'
model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

def intro_ai(entity, json_article_filepath, regen=False, clear=False):
    herb_name_scientific = entity['herb_name_scientific']
    json_article = io.json_read(json_article_filepath)
    reply_start = f'The best medicinal preparations of {herb_name_scientific.capitalize()} are '
    preparations_names = [item['answer'] for item in entity['preparations']]
    preparations_names_prompt = ', '.join(preparations_names[:5])
    llm.paragraph_ai(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 5-sentence paragraph about the herbal preparations of the {herb_name_scientific} herb for medicinal purposes.
            Include the following preparations: {preparations_names_prompt}.
            Start the reply with the following words: {reply_start}.
            /no_think
        ''',
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def list_init_ai(entity, json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    if clear:
        json_article['preparation_list'] = []
        io.json_write(json_article_filepath, json_article)
        return
    if regen:
        json_article['preparation_list'] = []
        io.json_write(json_article_filepath, json_article)
    entity_benefits = entity['preparations']
    if 'preparation_list' not in json_article: json_article['preparation_list'] = []
    article_benefits = json_article['preparation_list']
    for entity_benefit in entity_benefits:
        found = False
        for article_benefit in article_benefits:
            if entity_benefit['answer'] == article_benefit['answer']:
                found = True
                break
        if not found:
            article_benefits.append(entity_benefit)
    json_article['preparation_list'] = article_benefits
    io.json_write(json_article_filepath, json_article)

def ai_list_preparation_overview(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    preparations_num = json_article['preparations_num']
    preparation_list = json_article['preparation_list']
    for obj_i, obj in enumerate(preparation_list):
        print(f'{obj_i}/{len(preparation_list)}')
        preparation_answer = obj['answer']
        reply_start = f'{herb_name_scientific.capitalize()} {preparation_answer.lower().strip()} is commonly used to '
        llm.paragraph_ai(
            key = 'overview',
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write a short 5-sentence paragraph about the following herbal preparation of the {herb_name_scientific} plant for medicinal purposes: {preparation_answer}.
                Explain what are the most common medicinal uses of this herbal preparations, including treated ailments.
                Explain what are the bioactive constituents of this herbal preparations that give its medicinal properties.
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

def ai_benefit_definition(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    benefits_num = json_article['benefits_num']
    benefits = json_article['benefits']
    sentence_n = 5
    reply_start = f''
    if reply_start != '':
        reply_start_prompt = f'Start with the following words: {reply_start}.'
    else:
        reply_start_prompt = ''
    for obj_i, obj in enumerate(benefits):
        print(f'{obj_i}/{len(benefits)}')
        benefit_answer = obj['answer']
        reply_start = f''
        llm.paragraph_ai(
            key = 'definition',
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write a short {sentence_n}-sentence paragraph about the following health benefit of the {herb_name_scientific} plant: {benefit_answer}.
                Start the reply by giving a definition of the specific health issue metioned in the benefit.
                The first thing you write is the name of the health issue mentioned in the benefit.
                Use synonyms and semantic variations of the health issue.
                Explain what causes it and who commonly experiences it.
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

def ai_benefit_constituents(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    benefits_num = json_article['benefits_num']
    benefits = json_article['benefits']
    sentence_n = 5
    for obj_i, obj in enumerate(benefits):
        print(f'{obj_i}/{len(benefits)}')
        benefit_answer = obj['answer']
        reply_start = f'{herb_name_scientific.capitalize()} {benefit_answer.lower()} because it contains '
        if reply_start != '':
            reply_start_prompt = f'Start with the following words: {reply_start}.'
        else:
            reply_start_prompt = ''
        llm.paragraph_ai(
            key = 'constituents',
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write a short {sentence_n}-sentence paragraph about the bioactive constituents (e.g. alkaloids, flavonoids) of the {herb_name_scientific} plant that give the following health benefit: {benefit_answer}.
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

def ai_benefit_study(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    benefits_num = json_article['benefits_num']
    benefits = json_article['benefits']
    for obj_i, obj in enumerate(benefits):
        print(f'{obj_i}/{len(benefits)}')
        benefit_answer = obj['answer']
        key = 'study'
        if key not in obj: obj[key] = ''
        if regen: obj[key] = ''
        if clear: 
            obj[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if obj[key] == '':
            reply = studies.ai_study_plant_benefit(herb_name_scientific, benefit_answer)
            if reply.strip() != '':
                obj[key] = reply
                io.json_write(json_article_filepath, json_article)

def json_gen(entity, article_url):
    herb_slug = entity['herb_slug']
    herb_name_scientific = entity['herb_name_scientific']
    ###
    json_article_filepath = f'{g.JSONS_ARTICLES_FOLDERPATH}/{article_url}.json'
    print(f'    >> JSON: {json_article_filepath}')
    json_article = io.json_read(json_article_filepath, create=True)
    if 'lastmod' not in json_article: json_article['lastmod'] = utils.today()
    json_article['url'] = article_url
    json_article['herb_slug'] = herb_slug
    json_article['herb_name_scientific'] = herb_name_scientific
    json_article['preparations_num'] = 10
    json_article['title'] = f'{json_article["preparations_num"]} best {herb_name_scientific.capitalize()} preparations'.title()
    io.json_write(json_article_filepath, json_article)
    ###
    intro_ai(entity, json_article_filepath, regen=False, clear=False)
    list_init_ai(entity, json_article_filepath, regen=False, clear=False)
    ai_list_preparation_overview(entity, json_article_filepath, regen=False, clear=False)
    '''
    ai_benefit_definition(entity, json_article_filepath, regen=False, clear=False)
    ai_benefit_constituents(entity, json_article_filepath, regen=False, clear=False)
    ai_benefit_study(entity, json_article_filepath, regen=False, clear=False)
    '''

def imgs_benefits_gen(entity, quality):
    benefits = entity['benefits']
    herb_slug = entity['herb_slug']
    herb_name_scientific = entity['herb_name_scientific'].capitalize()
    benefits = entity['benefits']
    benefits_num = entity['benefits_num']
    benefits_names = [benefit['answer'].lower().strip() for benefit in benefits][:benefits_num]
    for benefit_name in benefits_names:
        benefit_slug = utils.sluggify(benefit_name)
        img_w = 768
        img_h = 768
        color_background = '#000000'
        img = Image.new(mode="RGBA", size=(img_w, img_h), color=color_background)
        draw = ImageDraw.Draw(img)
        ###
        lines = [herb_name_scientific, f'health benefit']
        y_cur = 0
        y_cur += 32
        font_size = 48
        font_path = f"assets/fonts/lora/static/Lora-Regular.ttf"
        font = ImageFont.truetype(font_path, font_size)
        line_height = 1.2
        for line in lines:
            line = line.upper()
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((img_w//2 - line_w//2, y_cur), line, '#ffffff', font=font)
            y_cur += font_size*line_height
        ###
        font_size = 96
        font_path = f"assets/fonts/lora/static/Lora-Regular.ttf"
        font = ImageFont.truetype(font_path, font_size)
        line_height = 1.2
        text = benefit_name
        lines = []
        line = ''
        for word in text.split(' '):
            _, _, line_w, line_h = font.getbbox(line)
            _, _, word_w, word_h = font.getbbox(word)
            if line_w + word_w < img_w - int(img_w*0.3):
                line += word + ' '
            else:
                lines.append(line.strip())
                line = word + ' '
        if line != '': lines.append(line.strip())
            
        y_cur = img_h//2 - (font_size*len(lines))//2
        for line in lines:
            line = line.upper()
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((img_w//2 - line_w//2, y_cur), line, '#ffffff', font=font)
            y_cur += font_size*line_height
        ###
        line = 'terrawhisper.com'
        font_size = 16
        font_path = f"assets/fonts/lora/static/Lora-Regular.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((img_w//2 - line_w//2, img_h - font_size - 32), line, '#ffffff', font=font)
        ###
        img = img.convert('RGB')
        img_filepath = f'{g.WEBSITE_FOLDERPATH}/images/herbs/{herb_slug}-benefits-{benefit_slug}.jpg'
        img.save(img_filepath, format='JPEG', subsampling=0, quality=quality)

def imgs_gen(entity, url_relative):
    json_article_filepath = f'database/json/{url_relative}.json'
    json_article = io.json_read(json_article_filepath)
    ###
    quality = 10
    imgs_benefits_gen(entity, quality)

def html_gen(url):
    json_article_filepath = f'{g.JSONS_ARTICLES_FOLDERPATH}/{url}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url}.html'
    print(f'    >> HTML: {html_article_filepath}')
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    preparations_num = json_article['preparations_num']
    article_title = json_article['title']
    page_title = article_title
    ###
    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    if 0:
        html_article += f'''
            <img style="margin-bottom: 16px;" 
            src="/images/herbs/{herb_slug}.jpg" 
            alt="{herb_name_scientific}">
        '''
    intro = json_article['intro']
    if intro != '':
        html_article += f'{utils.text_format_sentences_html(json_article["intro"])}\n'
    html_article += f'<p>Below there\'s a list of the {preparations_num} best herbal preparations of {herb_name_scientific} for medicinal purposes.</p>\n'
    html_article += f'[html_intro_toc]\n'
    ###
    preparation_list = json_article['preparation_list']
    i = 0
    preparation_counter = 0
    for j in range(len(preparation_list)):
        preparation = preparation_list[j]
        preparation_answer = preparation['answer']
        preparation_slug = utils.sluggify(preparation_answer)
        preparation_overview = preparation['overview']
        if preparation_overview.strip() != '':
            if preparation_overview.strip()[0] != '[':
                html_article += f'<h2>{i+1}. {preparation_answer.capitalize()}</h2>\n'
                link_href = f'/preparations/{preparation_slug}/{herb_slug}.html'
                out_filepath = f'{g.WEBSITE_FOLDERPATH}/preparations/{preparation_slug}/{herb_slug}.html'
                if os.path.exists(out_filepath):
                    preparation_overview = preparation_overview.replace(
                        f'{herb_name_scientific.capitalize()} {preparation_answer.lower()}', 
                        f'<a href="{link_href}">{herb_name_scientific.capitalize()} {preparation_answer.lower()}</a>',
                        1,
                    )
                html_article += f'{utils.text_format_1N1_html(preparation_overview)}\n'
        i += 1
        preparation_counter += 1
        if 0:
            img_filepath = f'/images/herbs/{herb_slug}-benefits-{benefit_slug}.jpg'
            html_article += f'<img src="{img_filepath}" style="margin-bottom: 16px;">\n'
            benefit_constituents = benefit['constituents']
            if benefit_constituents.strip() != '':
                if benefit_constituents.strip()[0] != '[':
                    html_article += f'<h3>How this herb helps with {benefit_answer.lower()}?</h2>\n'
                    html_article += f'{utils.text_format_1N1_html(benefit_constituents)}\n'
            benefit_study = benefit['study']
            if benefit_study.strip() != '':
                if benefit_study.strip()[0] != '[':
                    if not benefit_study.strip().startswith('N/A'):
                        html_article += f'<h3>Scientific Research</h2>\n'
                        html_article += f'{utils.text_format_1N1_html(benefit_study)}\n'
        if preparation_counter >= json_article['preparations_num']:
            break
    ###
    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    html_breadcrumbs = components.breadcrumbs(f'{url}.html')
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
    herbs = data.herbs_books_get()
    for entity_i, herb in enumerate(herbs):
        print(f'{entity_i}/{len(herbs)} - {herb}')
        herb_name_scientific = herb.strip().lower()
        herb_slug = utils.sluggify(herb_name_scientific)
        url_relative = f'{category_slug}/{herb_slug}/{attribute_slug}'
        if not os.path.exists(f'{g.WEBSITE_FOLDERPATH}/{category_slug}'): 
            os.mkdir(f'{g.WEBSITE_FOLDERPATH}/{category_slug}')
        entity_filepath = f'{g.ENTITIES_FOLDERPATH}/herbs/{herb_slug}.json'
        entity = io.json_read(entity_filepath)
        ###
        if data.herb_medicine_poison_get(f'herbs/{herb_slug}') == 'medicine':
            json_gen(entity, url_relative)
            # imgs_gen(entity, url_relative)
            html_gen(url_relative)
    ###
    # debug_intro()

