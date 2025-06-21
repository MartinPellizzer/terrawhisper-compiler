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
checkpoint_filepath = f'{g.VAULT}/stable-diffusion/checkpoints/xl/juggernautXL_ragnarokBy.safetensors'
pipe = None

def ai_intro(entity, json_article_filepath, regen=False, clear=False):
    entity_slug = entity['entity_slug']
    entity_name_singular = entity['entity_name_singular']
    entity_name_plural = entity['entity_name_plural']
    ###
    json_article = io.json_read(json_article_filepath)
    reply_start = f'{entity_name_plural.capitalize()} are '
    llm.paragraph_ai(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
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

def ai_list_init(entity, json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    key = 'preparation_list'
    if clear:
        json_article[key] = []
        io.json_write(json_article_filepath, json_article)
        return
    if regen:
        json_article[key] = []
        io.json_write(json_article_filepath, json_article)
    ###
    if key not in json_article: json_article[key] = []
    preparation_list = json_article[key]
    preparation_popular_list = data.preparations_popular_100_get(entity['entity_slug'])
    for preparation_popular in preparation_popular_list:
        found = False
        for preparation in preparation_list:
            if preparation['herb_slug'] == preparation_popular['herb_slug']:
                found = True
                break
        if not found:
            preparation_list.append({
                'herb_slug': preparation_popular['herb_slug'],
                'herb_name_scientific': preparation_popular['herb_name_scientific'],
                'herb_total_score': preparation_popular['herb_total_score'],
            })
    json_article[key] = preparation_list
    io.json_write(json_article_filepath, json_article)
    
        
def list_desc_ai(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    benefits_num = json_article['benefits_num']
    benefits = json_article['benefits']
    for obj_i, obj in enumerate(benefits):
        print(f'{obj_i}/{len(benefits)}')
        benefit_answer = obj['answer']
        reply_start = f'{herb_name_scientific.capitalize()} {benefit_answer.lower().strip()} because '
        llm.paragraph_ai(
            key = 'desc',
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write a short 4-sentence paragraph about the following health benefit of the {herb_name_scientific} plant: {benefit_answer}.
                Include examples of bioactive constituents this plant contains to have this health benefit.
                Include examples of ailments that are related to this benefit that are relieved with this benefit.
                If you can't answer, reply with only "I can't reply".
                Start with the following words: {reply_start} .
                /no_think
            ''',
            reply_start = reply_start,
            regen = regen,
            print_prompt = True,
            clear = clear,
            model_filepath = model_filepath,
        )

def ai_list_desc(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    preparation_name_plural = entity['entity_name_plural'].lower().strip()
    preparation_list = json_article['preparation_list']
    for obj_i, obj in enumerate(preparation_list):
        print(f'{obj_i}/{len(preparation_list)}')
        herb_slug = obj['herb_slug']
        herb_name_scientific = obj['herb_name_scientific']
        reply_start = f'{herb_name_scientific.capitalize()} {preparation_name_plural} are used to '
        llm.paragraph_ai(
            key = 'desc',
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write a short 5-sentence paragraph about the following the following herbal preparation: {herb_name_scientific} {preparation_name_plural}.
                Include the most common uses of this herbal preparation. By uses I mean the ailments it treats.
                Include the most important bioactive constituents this herbal preparation has that are medicinal.
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

def json_gen(entity, url_relative):
    entity_slug = entity['entity_slug']
    entity_name_singular = entity['entity_name_singular']
    entity_name_plural = entity['entity_name_plural']
    ###
    json_article_filepath = f'{articles_folderpath}/{url_relative}.json'
    print(f'    >> JSON: {json_article_filepath}')
    json_article = io.json_read(json_article_filepath, create=True)
    if 'lastmod' not in json_article: json_article['lastmod'] = utils.today()
    json_article['url'] = url_relative
    json_article['entity_slug'] = entity_slug
    json_article['entity_name_singular'] = entity_name_singular
    json_article['entity_name_plural'] = entity_name_plural
    json_article['title'] = f'''100 best {entity_name_plural.lower()} for medicinal use'''
    io.json_write(json_article_filepath, json_article)
    ###
    ai_intro(entity, json_article_filepath, regen=False, clear=False)
    ai_list_init(entity, json_article_filepath, regen=False, clear=False)
    ai_list_desc(entity, json_article_filepath, regen=False, clear=False)

def imgs_gen(entity, url_relative):
    json_article_filepath = f'{articles_folderpath}/{url_relative}.json'
    json_article = io.json_read(json_article_filepath)
    print(f'    >> JSON: {json_article_filepath}')
    ###
    preparation_slug = entity['entity_slug']
    preparation_name_singular = entity['entity_name_singular']
    key = 'preparation_list'
    if key in json_article:
        for obj_i, obj in enumerate(json_article[key]):
            herb_slug = obj['herb_slug']
            herb_name_scientific = obj['herb_name_scientific']
            img_filepath = f'{g.WEBSITE_FOLDERPATH}/images/preparations/{herb_slug}-{preparation_slug}.jpg'
            if not os.path.exists(img_filepath):
                import torch
                from diffusers import DiffusionPipeline
                from diffusers import StableDiffusionXLPipeline
                from diffusers import DPMSolverMultistepScheduler
                quality = 30
                global pipe
                if pipe == None:
                    pipe = StableDiffusionXLPipeline.from_single_file(
                        checkpoint_filepath, 
                        torch_dtype=torch.float16, 
                        use_safetensors=True, 
                        variant="fp16"
                    ).to('cuda')
                    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
                prompt = f'''
                    herbal {preparation_name_singular} made with dry {herb_name_scientific},
                    on a wooden table,
                    rustic, vintage, boho,
                    warm tones,
                '''
                negative_prompt = ''
                image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                image = img_resize(image, w=768, h=768)
                image.save(img_filepath, format='JPEG', subsampling=0, quality=quality)

def html_gen(entity, url_relative):
    preparation_slug = entity['entity_slug']
    preparation_name_singular = entity['entity_name_singular']
    preparation_name_plural = entity['entity_name_plural']
    ###
    json_article_filepath = f'database/json/{url_relative}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url_relative}.html'
    print(f'    >> JSON: {json_article_filepath}')
    print(f'    >> HTML: {html_article_filepath}')
    json_article = io.json_read(json_article_filepath)
    article_title = json_article['title']
    page_title = f'''Medicinal Herbal {preparation_name_plural.title()}'''
    ###
    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    if 0:
        html_article += f'''
            <img style="margin-bottom: 16px;" 
            src="/images/preparations/{preparation_slug}.jpg" 
            alt="{preparation_name_singular}">
        '''
    key = 'intro'
    if key in json_article:
        if json_article[key][0] != '[':
            html_article += f'''{utils.text_format_1N1_html(json_article[key])}\n'''
    html_article += f'[html_intro_toc]\n'
    key = 'preparation_list'
    if key in json_article:
        for obj_i, obj in enumerate(json_article[key]):
            herb_slug = obj['herb_slug']
            herb_name_scientific = obj['herb_name_scientific']
            html_article += f'''<h2>{obj_i+1}. {obj['herb_name_scientific'].capitalize()}</h2>\n'''
            html_article += f'''
                <img style="margin-bottom: 16px;" 
                src="/images/preparations/{herb_slug}-{preparation_slug}.jpg" 
                alt="{herb_name_scientific} {preparation_name_singular}">
            '''
            desc = obj['desc']
            desc = desc.replace(
                f'{herb_name_scientific.capitalize()} {preparation_name_plural.lower()}', 
                f'<a href="/{category_slug}/{preparation_slug}/{herb_slug}.html">{herb_name_scientific.capitalize()} {preparation_name_plural.lower()}</a>',
                1
            )
            html_article += f'''{utils.text_format_1N1_html(desc)}\n'''
    ###
    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    html_breadcrumbs = components.breadcrumbs(f'{category_slug}/{preparation_slug}/best.html')
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
    entity_list = io.csv_to_dict(f'database/entities/preparations.csv')
    for entity_i, entity in enumerate(entity_list):
        print(f'{entity_i}/{len(entity_list)} - {entity}')
        entity_slug = entity['entity_slug']
        entity_name_singular = entity['entity_name_singular']
        entity_name_plural = entity['entity_name_plural']
        url_relative = f'{category_slug}/{entity_slug}/best'
        ###
        json_gen(entity, url_relative)
        # imgs_gen(entity, url_relative)
        html_gen(entity, url_relative)
        # quit()
