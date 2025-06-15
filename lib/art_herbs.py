import os
import json

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

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
articles_folderpath = 'database/json'

model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

reply_debug = False

paragraphs_failed = []

def intro_ai(entity, json_article_filepath, regen=False, clear=False):
    herb_name_scientific = entity['herb_name_scientific']
    json_article = io.json_read(json_article_filepath)
    reply_start = f'{herb_name_scientific.capitalize()}, commonly known as '
    llm.paragraph_ai(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the {herb_name_scientific} herb.
            Include a definition of what this herb is.
            Include the health benefits.
            Include the bioactive constituents this herb has that give its therapeutic actions.
            Include the herbal preparations you can do with this herb (ex. infusions, etc...).
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

def intro_study_ai(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    herb_name_scientific = json_article['herb_name_scientific']
    key = 'intro_study'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if clear: 
        json_article[key] = ''
        return
    if json_article[key] == '':
        reply = studies.study_plant_intro_ai(herb_name_scientific)
        if reply.strip() != '':
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)

def benefits_desc_ai(entity, json_article_filepath, regen=False, clear=False):
    benefits_n = 4
    benefits = entity['benefits']
    benefits_names = [benefit['answer'].lower().strip() for benefit in benefits][:benefits_n]
    benefits_names_prompt = ', '.join(benefits_names)
    if len(benefits_names) != benefits_n: return
    ##
    json_article = io.json_read(json_article_filepath)
    herb_name_scientific = json_article['herb_name_scientific']
    reply_start = f'{herb_name_scientific.capitalize()} {benefits_names[0]} '
    sentence_n = 4
    prompt = f'''
        Write a detailed {sentence_n}-sentence paragraph about the health benefits of the {herb_name_scientific} herb.
        In sentence 1, state that {herb_name_scientific} {benefits_names[0]} and explain why in detail.
        In sentence 2, state that {herb_name_scientific} {benefits_names[1]} and explain why in detail.
        In sentence 3, state that {herb_name_scientific} {benefits_names[2]} and explain why in detail.
        In sentence 4, state that {herb_name_scientific} {benefits_names[3]} and explain why in detail.
        If you can't answer, reply with only "I can't reply".
        Start with the following words: {reply_start} .
        /no_think
    '''
    sentence_n = 5
    prompt = f'''
        Write a detailed {sentence_n}-sentence paragraph in about 200 words about some of the following health benefits of the {herb_name_scientific} herb: {benefits_names_prompt}.
        If you can't answer, reply with only "I can't reply".
        Start with the following words: {reply_start} .
        /no_think
    '''
    llm.paragraph_ai(
        key = 'benefits',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = prompt, 
        sentence_n = sentence_n,
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def benefits_list_ai(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    key = 'benefits_list'
    obj = json_article
    data = json_article
    filepath = json_article_filepath
    if key not in obj: obj[key] = ''
    if regen: obj[key] = ''
    if clear: 
        obj[key] = ''
        io.json_write(filepath, data)
        return
    if obj[key] == '':
        herb_name_scientific = json_article['herb_name_scientific']
        benefits = entity['benefits']
        benefits_num = entity['benefits_num']
        benefits_names = [benefit['answer'].lower().strip() for benefit in benefits][:benefits_num]
        benefits_rows_prompt = []
        for benefit_name in benefits_names:
            benefits_rows_prompt.append(f'{{"benefit": "{benefit_name}", "description": "write the description here"}}')
        benefits_prompt = ',\n'.join(benefits_rows_prompt)
        
        prompt = f'''
            Write a short description for each of the {benefits_num} health benefits of the {herb_name_scientific.capitalize()} herb listed in the JSON below.
            Reply in the following JSON format:
            [
                {benefits_prompt}
            ]
            Only reply with the JSON, don't add additional info.
            /no_think
        '''
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        outputs = []
        if json_data != {}:
            for item in json_data:
                try: name = item['benefit']
                except: continue
                try: description = item['description']
                except: continue
                outputs.append({
                    "name": name, 
                    "description": description,
                })
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        if outputs != []:
            json_article[key] = outputs[:20]
            io.json_write(json_article_filepath, json_article)
        else:
            json_article[key] = 'EMPTY'
            io.json_write(json_article_filepath, json_article)

def constituents_desc_ai(entity, json_article_filepath, regen=False, clear=False):
    constituents_n = 4
    constituents = entity['constituents']
    constituents_names = [item['answer'].lower().strip() for item in constituents][:constituents_n]
    if len(constituents_names) != constituents_n: return
    constituents_names_prompt = ', '.join(constituents_names)
    ##
    json_article = io.json_read(json_article_filepath)
    herb_name_scientific = json_article['herb_name_scientific']
    reply_start = f'{herb_name_scientific.capitalize()} {constituents_names[0]} '
    sentence_n = 4
    length = 'detailed'
    prompt = f'''
        Write a {length} {sentence_n}-sentence paragraph about the medicinal constituents of the {herb_name_scientific} herb.
        In sentence 1, write about {herb_name_scientific} {constituents_names[0]} in {length}.
        In sentence 2, write about {herb_name_scientific} {constituents_names[1]} in {length}.
        In sentence 3, write about {herb_name_scientific} {constituents_names[2]} in {length}.
        In sentence 4, write about {herb_name_scientific} {constituents_names[3]} in {length}.
        If you can't answer, reply with only "I can't reply".
        Start with the following words: {reply_start} .
        /no_think
    '''
    sentence_n = 5
    prompt = f'''
        Write a detailed {sentence_n}-sentence paragraph in about 200 words about some of the following medicinal constitunets of the {herb_name_scientific} herb: {constituents_names_prompt}.
        If you can't answer, reply with only "I can't reply".
        Start with the following words: {reply_start} .
        /no_think
    '''
    llm.paragraph_ai(
        key = 'constituents',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = prompt,
        sentence_n = '',
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def constituents_list_ai(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    key = 'constituents_list'
    obj = json_article
    data = json_article
    filepath = json_article_filepath
    if key not in obj: obj[key] = ''
    if regen: obj[key] = ''
    if clear: 
        obj[key] = ''
        io.json_write(filepath, data)
        return
    if obj[key] == '':
        constituents_num = entity['constituents_num']
        constituents_names = [item['answer'].lower().strip() for item in constituents][:constituents_num]
        constituents_rows_prompt = []
        for name in constituents_names:
            constituents_rows_prompt.append(f'{{"name": "{name}", "description": "write the description here"}}')
        constituents_prompt = ',\n'.join(constituents_rows_prompt)
        prompt = f'''
            Write a short description for each of the {constituents_num} medicinal constituents of the {herb_name_scientific.capitalize()} herb listed in the JSON below.
            Reply in the following JSON format:
            [
                {constituents_prompt}
            ]
            Only reply with the JSON, don't add additional info.
            /no_think
        '''
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        outputs = []
        if json_data != {}:
            for item in json_data:
                try: name = item['name']
                except: continue
                try: description = item['description']
                except: continue
                outputs.append({
                    "name": name, 
                    "description": description,
                })
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        if outputs != []:
            json_article[key] = outputs[:20]
            io.json_write(json_article_filepath, json_article)
        else:
            json_article[key] = 'EMPTY'
            io.json_write(json_article_filepath, json_article)

def parts_desc_ai(entity, json_article_filepath, regen=False, clear=False):
    parts = entity['parts']
    ###
    json_article = io.json_read(json_article_filepath)
    try: parts_names = [item['answer'].lower().strip() for item in parts][:json_article['parts_num']]
    except: return
    parts_n = len(parts_names)
    parts_names_prompt = ', '.join(parts_names)
    if parts_names == []: return
    ###
    herb_name_scientific = json_article['herb_name_scientific']
    reply_start = f'{herb_name_scientific.capitalize()} {parts_names[0]}'
    sentence_n = 4
    length = 'detailed'
    prompt = f'''
        Write a {length} {sentence_n}-sentence paragraph about the following medicinal parts of the {herb_name_scientific} herb: {parts_names_prompt}.
        Explain what are the main herbal preparations you can make with these parts.
        Only examine the parts listed above.
        If you can't answer, reply with only "I can't reply".
        Start with the following words: {reply_start} .
        /no_think
    '''
    sentence_n = 5
    prompt = f'''
        Write a detailed {sentence_n}-sentence paragraph in about 200 words about some of the following medicinal parts of the {herb_name_scientific} herb: {parts_names_prompt}.
        If you can't answer, reply with only "I can't reply".
        Start with the following words: {reply_start} .
        /no_think
    '''
    llm.paragraph_ai(
        key = 'parts',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = prompt,
        sentence_n = '',
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def parts_list_ai(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    key = 'parts_list'
    obj = json_article
    data = json_article
    filepath = json_article_filepath
    if key not in obj: obj[key] = ''
    if regen: obj[key] = ''
    if clear: 
        obj[key] = ''
        io.json_write(filepath, data)
        return
    if obj[key] == '':
        try: parts_names = [item['answer'].lower().strip() for item in parts][:json_article['parts_num']]
        except: return
        parts_rows_prompt = []
        for name in parts_names:
            parts_rows_prompt.append(f'{{"name": "{name}", "description": "write the description here"}}')
        parts_prompt = ',\n'.join(parts_rows_prompt)
        prompt = f'''
            Write a short description for each of the {json_article['parts_num']} parts of the {herb_name_scientific.capitalize()} herb listed in the JSON below, explaining their medicinal properties.
            Reply in the following JSON format:
            [
                {parts_prompt}
            ]
            Only reply with the JSON, don't add additional info.
            /no_think
        '''
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        outputs = []
        if json_data != {}:
            for item in json_data:
                try: name = item['name']
                except: continue
                try: description = item['description']
                except: continue
                outputs.append({
                    "name": name, 
                    "description": description,
                })
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        if outputs != []:
            json_article[key] = outputs[:20]
            io.json_write(json_article_filepath, json_article)
        else:
            json_article[key] = 'EMPTY'
            io.json_write(json_article_filepath, json_article)

def preparations_desc_ai(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    preparations_names = [item['answer'].lower().strip() for item in entity['preparations']][:json_article['preparations_num']]
    preparations_n = len(preparations_names)
    preparations_names_prompt = ', '.join(preparations_names)
    if preparations_names == []: return
    ###
    herb_name_scientific = json_article['herb_name_scientific']
    reply_start = f'{herb_name_scientific.capitalize()} {preparations_names[0].lower()} '
    sentence_n = 4
    length = 'detailed'
    prompt = f'''
        Write a {length} {sentence_n}-sentence paragraph about the following herbal preparations of the {herb_name_scientific} herb: {preparations_names_prompt}.
        Explain what are the most common uses of these preparations.
        If you can't answer, reply with only "I can't reply".
        Start with the following words: {reply_start} .
        /no_think
    '''
    sentence_n = 5
    prompt = f'''
        Write a detailed {sentence_n}-sentence paragraph in about 200 words about some of the following herbal preparations of the {herb_name_scientific} herb: {preparations_names_prompt}.
        If you can't answer, reply with only "I can't reply".
        Start with the following words: {reply_start} .
        /no_think
    '''
    llm.paragraph_ai(
        key = 'preparations',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = prompt,
        sentence_n = '',
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def preparations_list_ai(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    key = 'preparations_list'
    obj = json_article
    data = json_article
    filepath = json_article_filepath
    if key not in obj: obj[key] = ''
    if regen: obj[key] = ''
    if clear: 
        obj[key] = ''
        io.json_write(filepath, data)
        return
    if obj[key] == '':
        preparations_names = [item['answer'].lower().strip() for item in entity['preparations']][:json_article['preparations_num']]
        preparations_rows_prompt = []
        for name in preparations_names:
            preparations_rows_prompt.append(f'{{"name": "{name}", "description": "write the description here"}}')
        preparations_prompt = ',\n'.join(preparations_rows_prompt)
        prompt = f'''
            Write a short description for each of the {json_article['preparations_num']} herbal preparations of the {herb_name_scientific.capitalize()} herb listed in the JSON below, explaining their medicinal uses.
            Reply in the following JSON format:
            [
                {preparations_prompt}
            ]
            Only reply with the JSON, don't add additional info.
            /no_think
        '''
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        outputs = []
        if json_data != {}:
            for item in json_data:
                try: name = item['name']
                except: continue
                try: description = item['description']
                except: continue
                outputs.append({
                    "name": name, 
                    "description": description,
                })
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        if outputs != []:
            json_article[key] = outputs[:20]
            io.json_write(json_article_filepath, json_article)
        else:
            json_article[key] = 'EMPTY'
            io.json_write(json_article_filepath, json_article)


def side_effects_desc_ai(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    side_effects = entity['side_effects']
    if len(side_effects) < 4: return
    ###
    try: side_effects_names = [item['answer'].lower().strip() for item in side_effects][:json_article['side_effects_num']]
    except: return
    side_effects_n = len(side_effects_names)
    side_effects_names_prompt = ', '.join(side_effects_names)
    if side_effects_names == []: return
    ###
    herb_name_scientific = json_article['herb_name_scientific']
    reply_start = f'{herb_name_scientific.capitalize()} {side_effects_names[0].lower()} '
    sentence_n = 4
    length = 'detailed'
    prompt = f'''
        Write a {length} {sentence_n}-sentence paragraph about the most common health side effects of the {herb_name_scientific} herb.
        In sentence 1, write that {herb_name_scientific} {side_effects_names[0]} and explain why.
        In sentence 2, write that {herb_name_scientific} {side_effects_names[1]} and explain why.
        In sentence 3, write that {herb_name_scientific} {side_effects_names[2]} and explain why.
        In sentence 4, write that {herb_name_scientific} {side_effects_names[3]} and explain why.
        If you can't answer, reply with only "I can't reply".
        Start with the following words: {reply_start} .
        /no_think
    ''',
    sentence_n = 5
    prompt = f'''
        Write a detailed {sentence_n}-sentence paragraph in about 200 words about some of the following health side effects of the {herb_name_scientific} herb: {side_effects_names_prompt}.
        If you can't answer, reply with only "I can't reply".
        Start with the following words: {reply_start} .
        /no_think
    '''
    llm.paragraph_ai(
        key = 'side_effects',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = prompt,
        sentence_n = '',
        reply_start = reply_start,
        regen = regen,
        clear = clear,
        print_prompt = True,
        model_filepath = model_filepath,
    )

def side_effects_list_ai(entity, json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    key = 'side_effects_list'
    obj = json_article
    data = json_article
    filepath = json_article_filepath
    if key not in obj: obj[key] = ''
    if regen: obj[key] = ''
    if clear: 
        obj[key] = ''
        io.json_write(filepath, data)
        return
    if obj[key] == '':
        side_effects_num = entity['side_effects_num']
        try: side_effects_names = [item['answer'].lower().strip() for item in side_effects][:json_article['side_effects_num']]
        except: return
        side_effects_rows_prompt = []
        for name in side_effects_names:
            side_effects_rows_prompt.append(f'{{"name": "{name}", "description": "write the description here"}}')
        side_effects_prompt = ',\n'.join(side_effects_rows_prompt)
        
        prompt = f'''
            Write a short description for each of the {side_effects_num} health side effects of the {herb_name_scientific.capitalize()} herb listed in the JSON below.
            Reply in the following JSON format:
            [
                {side_effects_prompt}
            ]
            Only reply with the JSON, don't add additional info.
            /no_think
        '''
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        outputs = []
        if json_data != {}:
            for item in json_data:
                try: name = item['name']
                except: continue
                try: description = item['description']
                except: continue
                outputs.append({
                    "name": name, 
                    "description": description,
                })
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        if outputs != []:
            json_article[key] = outputs[:20]
            io.json_write(json_article_filepath, json_article)
        else:
            json_article[key] = 'EMPTY'
            io.json_write(json_article_filepath, json_article)

def json_gen(entity, url_relative):
    herb_slug = entity['herb_slug']
    herb_name_scientific = entity['herb_name_scientific']
    benefits_num = entity['benefits_num']
    ###
    json_article_filepath = f'{articles_folderpath}/{url_relative}.json'
    print(f'    >> JSON: {json_article_filepath}')
    json_article = io.json_read(json_article_filepath, create=True)
    if 'lastmod' not in json_article: json_article['lastmod'] = utils.today()
    json_article['url'] = url_relative
    json_article['herb_slug'] = herb_slug
    json_article['herb_name_scientific'] = herb_name_scientific
    json_article['benefits_num'] = benefits_num
    json_article['constituents_num'] = entity['constituents_num']
    json_article['parts_num'] = len([item['answer'].lower().strip() for item in entity['parts'] if item['grade'] >= 6])
    json_article['preparations_num'] = len([item['answer'].lower().strip() for item in entity['preparations'] if item['grade'] >= 6])
    json_article['side_effects_num'] = entity['side_effects_num']
    json_article['title'] = f'{herb_name_scientific.capitalize()} uses, benefits, and remedies'.title()
    io.json_write(json_article_filepath, json_article)
    ###
    intro_ai(entity, json_article_filepath, regen=False, clear=False)
    # intro_study_ai(json_article_filepath, regen=False, clear=False)
    benefits_desc_ai(entity, json_article_filepath, regen=False, clear=False)
    benefits_list_ai(entity, json_article_filepath, regen=False, clear=False)
    constituents_desc_ai(entity, json_article_filepath, regen=False, clear=False)
    constituents_list_ai(entity, json_article_filepath, regen=False, clear=False)
    parts_desc_ai(entity, json_article_filepath, regen=False, clear=False)
    parts_list_ai(entity, json_article_filepath, regen=False, clear=False)
    preparations_desc_ai(entity, json_article_filepath, regen=False, clear=False)
    preparations_list_ai(entity, json_article_filepath, regen=False, clear=False)
    side_effects_desc_ai(entity, json_article_filepath, regen=False, clear=False)
    side_effects_list_ai(entity, json_article_filepath, regen=False, clear=False)

def imgs_benefits_gen(entity, quality):
    herb_slug = entity['herb_slug']
    herb_name_scientific = entity['herb_name_scientific'].capitalize()
    benefits = entity['benefits']
    benefits_num = entity['benefits_num']
    benefits_names = [benefit['answer'].lower().strip() for benefit in benefits][:benefits_num]
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

def imgs_constituents_gen(entity, quality):
    herb_slug = entity['herb_slug']
    herb_name_scientific = entity['herb_name_scientific'].capitalize()
    constituents = entity['constituents']
    constituents_num = entity['constituents_num']
    constituents_names = [item['answer'].lower().strip() for item in constituents][:constituents_num]
    img_w = 768
    img_h = 768
    color_background = '#000000'
    img = Image.new(mode="RGBA", size=(img_w, img_h), color=color_background)
    draw = ImageDraw.Draw(img)
    ###
    lines = [herb_name_scientific, 'bioactive constituents']
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
    lines_h = len(constituents_names)*font_size
    # off_y = (img_h - lines_h)//2
    line_height = 1.4
    for line in constituents_names:
        line = line.replace('α', 'alpha')
        line = line.replace('β', 'beta')
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
    img_filepath = f'{g.WEBSITE_FOLDERPATH}/images/herbs/{herb_slug}-constituents.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=quality)

def imgs_parts_gen(entity, names, quality):
    herb_slug = entity['herb_slug']
    herb_name_scientific = entity['herb_name_scientific'].capitalize()
    img_w = 768
    img_h = 768
    color_background = '#000000'
    img = Image.new(mode="RGBA", size=(img_w, img_h), color=color_background)
    draw = ImageDraw.Draw(img)
    ###
    lines = [herb_name_scientific, 'medicinal parts']
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
    lines_h = len(names)*font_size
    # off_y = (img_h - lines_h)//2
    line_height = 1.4
    for line in names:
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
    img_filepath = f'{g.WEBSITE_FOLDERPATH}/images/herbs/{herb_slug}-parts.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=quality)

def imgs_preparations_gen(entity, names, quality):
    herb_slug = entity['herb_slug']
    herb_name_scientific = entity['herb_name_scientific'].capitalize()
    img_w = 768
    img_h = 768
    color_background = '#000000'
    img = Image.new(mode="RGBA", size=(img_w, img_h), color=color_background)
    draw = ImageDraw.Draw(img)
    ###
    lines = [herb_name_scientific, 'herbal preparations']
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
    lines_h = len(names)*font_size
    # off_y = (img_h - lines_h)//2
    line_height = 1.4
    for line in names:
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
    img_filepath = f'{g.WEBSITE_FOLDERPATH}/images/herbs/{herb_slug}-preparations.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=quality)

def imgs_side_effects_gen(entity, names, quality):
    herb_slug = entity['herb_slug']
    herb_name_scientific = entity['herb_name_scientific'].capitalize()
    img_w = 768
    img_h = 768
    color_background = '#000000'
    img = Image.new(mode="RGBA", size=(img_w, img_h), color=color_background)
    draw = ImageDraw.Draw(img)
    ###
    lines = [herb_name_scientific, 'health side effects']
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
    lines_h = len(names)*font_size
    # off_y = (img_h - lines_h)//2
    line_height = 1.4
    for line in names:
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
    img_filepath = f'{g.WEBSITE_FOLDERPATH}/images/herbs/{herb_slug}-side-effects.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=quality)


def imgs_gen(entity, url_relative):
    json_article_filepath = f'database/json/{url_relative}.json'
    json_article = io.json_read(json_article_filepath)
    try: parts_names = [item['name'] for item in json_article['parts_list']]
    except: parts_names = []
    try: preparations_names = [item['name'] for item in json_article['preparations_list']][:10]
    except: preparations_names = []
    try: side_effects_names = [item['name'] for item in json_article['side_effects_list']]
    except: side_effects_names = []
    ###
    quality = 30
    imgs_benefits_gen(entity, quality)
    imgs_constituents_gen(entity, quality)
    if parts_names != []:
        imgs_parts_gen(entity, parts_names, quality)
    if preparations_names != []:
        imgs_preparations_gen(entity, preparations_names, quality)
    if side_effects_names != []:
        imgs_side_effects_gen(entity, side_effects_names, quality)

def html_gen(url):
    json_article_filepath = f'database/json/{url}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url}.html'
    print(f'    >> JSON: {json_article_filepath}')
    print(f'    >> HTML: {html_article_filepath}')
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    # herb_name_common = json_article['herb_name_common']
    article_title = json_article['title']
    page_title = article_title
    ###
    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    html_article += f'''
        <img style="margin-bottom: 16px;" 
        src="/images/herbs/{herb_slug}.jpg" 
        alt="{herb_name_scientific}">
    '''
    if 'intro' in json_article:
        intro = json_article['intro']
        if intro != 'N/A' and intro != 'WRONG START':
            html_article += f'{utils.text_format_sentences_html(intro)}\n'
    if 'intro_study' in json_article:
        intro_study = json_article['intro_study']
        if intro_study != 'N/A' and intro_study != 'WRONG START':
            html_article += components.study_snippet_html(json_article['intro_study'])
    html_article += f'<p style="margin-top: 16px; margin-bottom: 32px;">This page analize the most important medicinal aspects of {herb_name_scientific.capitalize()}.</p>\n'
    html_article += f'[html_intro_toc]\n'
    ###
    if 'benefits' in json_article:
        err = False
        for reply_error in llm.reply_errors:
            if json_article['benefits'].startswith(reply_error):
                paragraphs_failed.append('benefits')
                err = True
                break
        if not reply_debug:
            if not err and json_article['benefits'] != '':
                html_article += f'<h2>Health Benefits</h2>\n'
                html_article += f'{utils.text_format_1N1_html(json_article["benefits"])}\n'
    html_article += f'<p>The {json_article["benefits_num"]} best health benefits of {herb_name_scientific.capitalize()} are shown in the image below.</p>\n'
    img_filepath = f'/images/herbs/{herb_slug}-benefits.jpg'
    html_article += f'<img src="{img_filepath}" style="margin-bottom: 16px;">\n'
    if 'benefits_list' in json_article:
        html_article += f'<p>The list below give a brief description of the <a href="/{url}/benefits.html">{json_article["benefits_num"]} best health benefits of {herb_name_scientific.capitalize()}</a>.</p>\n'
        html_article += f'<ol>\n'
        for benefit in json_article['benefits_list']:
            html_article += f'<li><strong>{benefit["name"].title()}</strong>: {benefit["description"]}</li>\n'
        html_article += f'</ol>\n'
    '''
    if 'actions' in json_article:
        html_article += f'<h2>Therapeutic Actions of {herb_name_scientific}</h2>\n'
        html_article += f'{utils.text_format_sentences_html(json_article["actions"])}\n'
    '''
    ###
    if 'constituents' in json_article:
        err = False
        for reply_error in llm.reply_errors:
            if json_article['constituents'].startswith(reply_error):
                paragraphs_failed.append('constituents')
                err = True
                break
        if not reply_debug:
            if not err and json_article['constituents'] != '':
                html_article += f'<h2>Bioactive Constituents</h2>\n'
                html_article += f'{utils.text_format_1N1_html(json_article["constituents"])}\n'
    html_article += f'<p>The {json_article["constituents_num"]} best bioactive constituents of {herb_name_scientific.capitalize()} are shown in the image below.</p>\n'
    img_filepath = f'/images/herbs/{herb_slug}-constituents.jpg'
    html_article += f'<img src="{img_filepath}" style="margin-bottom: 16px;">\n'
    if 'constituents_list' in json_article:
        html_article += f'<p>The list below give a brief description of the {json_article["benefits_num"]} best bioactive constituents of {herb_name_scientific.capitalize()}.</p>\n'
        html_article += f'<ol>\n'
        for item in json_article['constituents_list']:
            html_article += f'<li><strong>{item["name"].title()}</strong>: {item["description"]}</li>\n'
        html_article += f'</ol>\n'
    ###
    if 'parts' in json_article:
        err = False
        for reply_error in llm.reply_errors:
            if json_article['parts'].startswith(reply_error):
                paragraphs_failed.append('parts')
                err = True
                break
        if not reply_debug:
            if not err and json_article['parts'] != '':
                html_article += f'<h2>Medicinal Parts</h2>\n'
                html_article += f'{utils.text_format_1N1_html(json_article["parts"])}\n'
    html_article += f'<p>The {json_article["parts_num"]} best medicinal parts of {herb_name_scientific.capitalize()} are shown in the image below.</p>\n'
    img_filepath = f'/images/herbs/{herb_slug}-parts.jpg'
    html_article += f'<img src="{img_filepath}" style="margin-bottom: 16px;">\n'
    if 'parts_list' in json_article:
        html_article += f'<p>The list below give a brief description of the {json_article["parts_num"]} best medicinal parts of {herb_name_scientific.capitalize()}.</p>\n'
        html_article += f'<ol>\n'
        for item in json_article['parts_list']:
            html_article += f'<li><strong>{item["name"].title()}</strong>: {item["description"]}</li>\n'
        html_article += f'</ol>\n'
    ###
    if 'preparations' in json_article:
        err = False
        for reply_error in llm.reply_errors:
            if json_article['preparations'].startswith(reply_error):
                paragraphs_failed.append('preparations')
                err = True
                break
        if not reply_debug:
            if not err and json_article['preparations'] != '':
                html_article += f'<h2>Herbal Preparations</h2>\n'
                html_article += f'{utils.text_format_1N1_html(json_article["preparations"])}\n'
    html_article += f'<p>The 10 best herbal preparations of {herb_name_scientific.capitalize()} are shown in the image below.</p>\n'
    img_filepath = f'/images/herbs/{herb_slug}-preparations.jpg'
    html_article += f'<img src="{img_filepath}" style="margin-bottom: 16px;">\n'
    if 'preparations_list' in json_article:
        html_article += f'<p>The list below give a brief description of the <a href="/{url}/preparations.html">10 best herbal preparations of {herb_name_scientific.capitalize()}</a>.</p>\n'
        html_article += f'<ol>\n'
        for item in json_article['preparations_list'][:10]:
            html_article += f'<li><strong>{item["name"].title()}</strong>: {item["description"]}</li>\n'
        html_article += f'</ol>\n'
    ###
    if 'side_effects' in json_article:
        err = False
        for reply_error in llm.reply_errors:
            if json_article['side_effects'].startswith(reply_error):
                paragraphs_failed.append('side_effects')
                err = True
                break
        if not reply_debug:
            if not err and json_article['side_effects'] != '':
                html_article += f'<h2>Side Effects of {herb_name_scientific}</h2>\n'
                html_article += f'{utils.text_format_1N1_html(json_article["side_effects"])}\n'
    html_article += f'<p>The {json_article["side_effects_num"]} most common side effects of {herb_name_scientific.capitalize()} are shown in the image below.</p>\n'
    img_filepath = f'/images/herbs/{herb_slug}-side-effects.jpg'
    html_article += f'<img src="{img_filepath}" style="margin-bottom: 16px;">\n'
    if 'side_effects_list' in json_article:
        html_article += f'<p>The list below give a brief description of the {json_article["side_effects_num"]} most common side effects of {herb_name_scientific.capitalize()}.</p>\n'
        html_article += f'<ol>\n'
        for item in json_article['side_effects_list']:
            html_article += f'<li><strong>{item["name"].title()}</strong>: {item["description"]}</li>\n'
        html_article += f'</ol>\n'
    ###
    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    html_breadcrumbs = components.breadcrumbs(f'{category_slug}/{herb_slug}.html')
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
    herbs_books = data.herbs_books_get()
    herbs = []
    for herb in herbs_books: herbs.append(herb)
    ###
    herbs = herbs[:]
    for herb_i, herb in enumerate(herbs):
        print(f'{herb_i}/{len(herbs)} - {herb}')
        herb_name_scientific = herb.strip().lower()
        herb_slug = utils.sluggify(herb_name_scientific)
        ###
        url_relative = f'{category_slug}/{herb_slug}'
        ###
        entity_filepath = f'{g.ENTITIES_FOLDERPATH}/herbs/{herb_slug}.json'
        entity = io.json_read(entity_filepath)
        ###
        if data.herb_medicine_poison_get(url_relative) == 'medicine':
            json_gen(entity, url_relative)
            # imgs_gen(entity, url_relative)
            html_gen(url_relative)
