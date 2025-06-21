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

def ai_what(entity, json_article_filepath, regen=False, clear=False):
    entity_slug = entity['entity_slug']
    entity_name_singular = entity['entity_name_singular']
    entity_name_plural = entity['entity_name_plural']
    ###
    json_article = io.json_read(json_article_filepath)
    reply_start = f'{entity_name_plural.capitalize()} are '
    llm.paragraph_ai(
        key = 'what',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 5-sentence paragraph about the following herbal preparation: {entity_name_plural}.
            Start by giving a simple and clear definition of what this herbal preparation is.
            Then compare with other herbal preparations, explaining how is it different.
            End by giving a quick overview of it's benefits compared to other preparations.
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

def ai_how_it_works(entity, json_article_filepath, regen=False, clear=False):
    entity_slug = entity['entity_slug']
    entity_name_singular = entity['entity_name_singular']
    entity_name_plural = entity['entity_name_plural']
    ###
    json_article = io.json_read(json_article_filepath)
    reply_start = f'{entity_name_plural.capitalize()} work by '
    llm.paragraph_ai(
        key = 'how_it_works',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 5-sentence paragraph about the following herbal preparation for medicinal purposes: {entity_name_plural}.
            Start by explaining how this preparation works, the science behind it (solubility, extraction, infusion, heat, alcohol, etc.)
            Then explain the active constituents typically extracted.
            End by explaining how it interacts with the body (asorption, delivery, potency).
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

def ai_best(entity, json_article_filepath, regen=False, clear=False):
    entity_slug = entity['entity_slug']
    entity_name_singular = entity['entity_name_singular']
    entity_name_plural = entity['entity_name_plural']
    ###
    json_article = io.json_read(json_article_filepath)
    reply_start = f'Some of the best herbal {entity_name_plural.lower()} for medicinal purposes are '
    herbs = data.preparations_popular_100_get(entity_slug)[:5]
    herbs_names_scientific = [item['herb_name_scientific'] for item in herbs]
    herbs_prompt = ', '.join(herbs_names_scientific)
    llm.paragraph_ai(
        key = 'best',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 5-sentence paragraph about the following herbal {entity_name_plural}.
            In specific, tell that the folloiwing herbs are the best and explain why: {herbs_prompt}.
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
    json_article['title'] = f'''What to know about {entity_name_plural.lower()} for medicinal use?'''
    io.json_write(json_article_filepath, json_article)
    ###
    ai_intro(entity, json_article_filepath, regen=False, clear=False)
    ai_what(entity, json_article_filepath, regen=False, clear=False)
    ai_how_it_works(entity, json_article_filepath, regen=False, clear=False)
    ai_best(entity, json_article_filepath, regen=False, clear=False)

def imgs_preparations_gen(entity, quality):
    entity_slug = entity['entity_slug']
    entity_name_singular = entity['entity_name_singular']
    img_w = 768
    img_h = 768
    color_background = '#000000'
    img = Image.new(mode="RGBA", size=(img_w, img_h), color=color_background)
    draw = ImageDraw.Draw(img)
    ###
    lines = [herb_name_scientific, 'health benefits']
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
    y_cur += 32
    px = 128
    draw.rectangle((0+px, y_cur, img_w-px, y_cur), '#ffffff')
    y_cur += 32
    ###
    font_size = 24
    font_path = f"assets/fonts/lora/static/Lora-Regular.ttf"
    font = ImageFont.truetype(font_path, font_size)
    lines_h = len(benefits_names)*font_size
    # off_y = (img_h - lines_h)//2
    line_height = 1.4
    for line in benefits_names:
        line = line.capitalize()
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
    img_filepath = f'{g.WEBSITE_FOLDERPATH}/images/herbs/{herb_slug}-benefits.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=quality)

def imgs_gen(entity, url_relative):
    entity_slug = entity['entity_slug']
    entity_name_singular = entity['entity_name_singular']
    img_filepath = f'{g.WEBSITE_FOLDERPATH}/images/preparations/{entity_slug}.jpg'
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
            {entity_name_singular} made with dry herbs,
            on a wooden table,
            rustic, vintage, boho,
            warm tones,
        '''
        negative_prompt = ''
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        image.save(img_filepath, format='JPEG', subsampling=0, quality=quality)

def html_gen(entity, url_relative):
    entity_slug = entity['entity_slug']
    entity_name_singular = entity['entity_name_singular']
    entity_name_plural = entity['entity_name_plural']
    ###
    json_article_filepath = f'database/json/{url_relative}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url_relative}.html'
    print(f'    >> JSON: {json_article_filepath}')
    print(f'    >> HTML: {html_article_filepath}')
    json_article = io.json_read(json_article_filepath)
    article_title = json_article['title']
    page_title = f'''Medicinal Herbal {entity_name_plural.title()}'''
    ###
    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    html_article += f'''
        <img style="margin-bottom: 16px;" 
        src="/images/preparations/{entity_slug}.jpg" 
        alt="{entity_name_singular}">
    '''
    key = 'intro'
    if key in json_article:
        if json_article[key][0] != '[':
            html_article += f'''{utils.text_format_1N1_html(json_article[key])}\n'''
    html_article += f'[html_intro_toc]\n'
    key = 'what'
    if key in json_article:
        if json_article[key][0] != '[':
            html_article += f'<h2>What is a {entity_name_singular}?</h2>\n'
            html_article += f'''{utils.text_format_1N1_html(json_article[key])}\n'''
    key = 'how_it_works'
    if key in json_article:
        if json_article[key][0] != '[':
            html_article += f'<h2>How {entity_name_singular} works?</h2>\n'
            html_article += f'''{utils.text_format_1N1_html(json_article[key])}\n'''
    key = 'best'
    if key in json_article:
        if json_article[key][0] != '[':
            html_article += f'''<h2>What are the best herbal {entity_name_plural}?</h2>\n'''
            html_article += f'''{utils.text_format_1N1_html(json_article[key])}\n'''
            html_article += f'''<p>Check this link for the full list of <a href="/{category_slug}/{entity_slug}/best.html">100 best {entity_name_plural} for medicinal use</a>.</p>\n'''
    ###
    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    html_breadcrumbs = components.breadcrumbs(f'{category_slug}/{entity_slug}.html')
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
        url_relative = f'{category_slug}/{entity_slug}'
        ###
        json_gen(entity, url_relative)
        # imgs_gen(entity, url_relative)
        html_gen(entity, url_relative)
        # quit()

