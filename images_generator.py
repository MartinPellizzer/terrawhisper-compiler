import os
import requests
import base64

from PIL import Image

import g
import util
import data_csv

import torch
from diffusers import DiffusionPipeline
from diffusers import StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image, ImageFont, ImageDraw

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read, json_write
from oliark import img_resize

ailments = csv_read_rows_to_json('systems-organs-ailments.csv')

vault = '/home/ubuntu/vault'
website_folderpath = 'website-2'

checkpoint_filepath = f'{vault}/stable-diffusion/checkpoints/xl/juggernautXL_juggXIByRundiffusion.safetensors'
pipe = None
def pipe_init():
    global pipe
    if pipe == None:
        pipe = StableDiffusionXLPipeline.from_single_file(
            checkpoint_filepath, 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

def gen_images_backup():
    vault = '/home/ubuntu/vault'
    category_name = 'tea'
    category_slug = category_name.replace(' ', '-')
    category_folderpath = f'{vault}/terrawhisper/images/{category_slug}s/2x3'
    try: os.makedirs(f'{category_folderpath}')
    except: pass
    herbs_rows, herbs_cols = data_csv.herbs()
    ## get starting herb index
    starting_herb_index = 0
    images_num_min = 999
    for herb_index, herb_row in enumerate(herbs_rows):
        herb_slug = herb_row[herbs_cols['herb_slug']]
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']]
        export_folder = f'{category_folderpath}/{herb_slug}'
        if not os.path.exists(export_folder):
            images_num_min = 0
            starting_herb_index = herb_index
            break
        images_filenames = os.listdir(export_folder)
        images_num = len(images_filenames)
        if images_num_min > images_num: 
            images_num_min = images_num
            starting_herb_index = herb_index
            
    print(starting_herb_index)
    print(images_num_min)
    ## gen images
    i = -1
    for herb_row in herbs_rows[starting_herb_index:]:
        i += 1
        herb_slug = herb_row[herbs_cols['herb_slug']]
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']]
        if category_name == 'salve': 
            prompt = f'''
                close-up of a small container with herbal salve, 
                on a wooden table, surrounded by {herb_name_scientific} and other herbs,
                natural lighting,
                depth of field, bokeh, 
                high resolution, cinematic
            '''
        print(prompt)
        for j in range(10):
            print(f'{herb_name_scientific} {i}/{len(herbs_rows)} - iter: {j}/100')
            tmp_filepath = f'{vault}/terrawhisper/images/tmp/tmp.png'
            image = pipe(
                prompt=prompt, 
                num_inference_steps=30
            ).images[0]
            image.save(tmp_filepath)
            ## compress image
            herb_folderpath = f'{category_folderpath}/{herb_slug}'
            try: os.makedirs(f'{herb_folderpath}')
            except: pass
            images_filenames = os.listdir(herb_folderpath)
            id_max = 0
            for image_filename in images_filenames:
                if id_max < int(image_filename.split('.')[0]):
                    id_max = int(image_filename.split('.')[0])
            id_next = id_max + 1
            export_filepath = f'{herb_folderpath}/{id_next}.jpg'
            img = Image.open(tmp_filepath)
            # img.thumbnail((768, 768), Image.Resampling.LANCZOS)
            img.save(export_filepath, optimize=True, quality=50)
        print(herb_row)


def gen_images():
    image_style = 'watercolor'
    image_ratio = '1x1'
    category_name = 'capsule'
    category_slug = category_name.replace(' ', '-')
    if image_style == 'watercolor':
        category_folderpath = f'{vault}/terrawhisper/images/{image_style}/{category_slug}s/{image_ratio}'
        try: os.makedirs(f'{category_folderpath}')
        except: pass
    else:
        category_folderpath = f'{vault}/terrawhisper/images/{category_slug}s/(image_ratio)'
        try: os.makedirs(f'{category_folderpath}')
        except: pass
    herbs_rows, herbs_cols = data_csv.herbs()
    ## gen images
    for herb_i, herb_row in enumerate(herbs_rows):
        herb_slug = herb_row[herbs_cols['herb_slug']]
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']]
        print(f'{herb_name_scientific} {herb_i}/{len(herbs_rows)}')
        filepath_out = f'{category_folderpath}/{herb_slug}.jpg'
        if os.path.exists(filepath_out): continue
        subject_name = category_name
        if 0: pass
        elif category_name == 'tea':
            subject_prompt = 'close-up of a cup of herbal tea'
        elif category_name == 'decoction':
            subject_prompt = 'close-up of a pot of herbal decoction'
        elif category_name == 'tincture':
            subject_prompt = 'close-up of a bottle of herbal tincture'
        elif category_name == 'essential oil':
            subject_prompt = 'close-up of a bottle of herbal essential oil'
        elif category_name == 'capsule':
            subject_prompt = 'close-up of a bottle of herbal capsules'
        elif category_name == 'cream':
            subject_prompt = 'close-up of a small container with herbal cream'
        elif category_name == 'salve': 
            subject_prompt = 'close-up of a small container with herbal salve'
        else: 
            print('category_name not valid')
            quit()
        if image_style == 'watercolor':
            prompt = f'''
                {subject_prompt}, 
                on a wooden table, surrounded by {herb_name_scientific},
                watercolor illustration,
                depth of field,
                detailed textures, high resolution, cinematic
            '''
        else:
            prompt = f'''
                {subject_prompt}, 
                on a wooden table, surrounded by {herb_name_scientific} and other herbs,
                natural lighting,
                depth of field, bokeh, 
                high resolution, cinematic
            '''
        print(prompt)
        if image_ratio == '1x1':
            image_size = [1024, 1024]
        else: 
            image_size = [832, 1216]
        image = pipe(
            prompt=prompt, 
            num_inference_steps=30,
            width=image_size[0], 
            height=image_size[1], 
        ).images[0]
        image.save(filepath_out, optimize=True, quality=50)

def gen_images_new():
    image_style = 'watercolor'
    image_ratio = '1x1'
    category_name = 'cream'
    category_slug = category_name.replace(' ', '-')
    if image_style == 'watercolor':
        category_folderpath = f'{vault}/terrawhisper/images/{image_style}/{category_slug}s/{image_ratio}'
        try: os.makedirs(f'{category_folderpath}')
        except: pass
    else:
        category_folderpath = f'{vault}/terrawhisper/images/{category_slug}s/(image_ratio)'
        try: os.makedirs(f'{category_folderpath}')
        except: pass
    herbs_rows, herbs_cols = data_csv.herbs()
    ## gen images
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        print(f'\n>> {ailment_i}/{len(ailments)} - preparation: {category_name}s')
        print(f'    >> {ailment}\n')
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}/{category_slug}s'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'website/{url}.html'
        data = json_read(json_filepath, create=True)
        for herb_i, obj in enumerate(data['remedies'][:]):
            herb_name_scientific = obj['plant_name_scientific']
            herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
            print(f'{herb_name_scientific} {herb_i}/{len(herbs_rows)}')
            filepath_out = f'{category_folderpath}/{herb_slug}.jpg'
            if os.path.exists(filepath_out): continue
            subject_name = category_name
            if 0: pass
            elif category_name == 'tea':
                subject_prompt = 'close-up of a cup of herbal tea'
            elif category_name == 'decoction':
                subject_prompt = 'close-up of a pot of herbal decoction'
            elif category_name == 'tincture':
                subject_prompt = 'close-up of a bottle of herbal tincture'
            elif category_name == 'essential oil':
                subject_prompt = 'close-up of a bottle of herbal essential oil'
            elif category_name == 'capsule':
                subject_prompt = 'close-up of a bottle of herbal capsules'
            elif category_name == 'cream':
                subject_prompt = 'close-up of a small container with herbal cream'
            elif category_name == 'salve': 
                subject_prompt = 'close-up of a small container with herbal salve'
            else: 
                print('category_name not valid')
                quit()
            if image_style == 'watercolor':
                prompt = f'''
                    {subject_prompt}, 
                    on a wooden table, surrounded by {herb_name_scientific},
                    watercolor illustration,
                    depth of field,
                    detailed textures, high resolution, cinematic
                '''
            else:
                prompt = f'''
                    {subject_prompt}, 
                    on a wooden table, surrounded by {herb_name_scientific} and other herbs,
                    natural lighting,
                    depth of field, bokeh, 
                    high resolution, cinematic
                '''
            print(prompt)
            if image_ratio == '1x1':
                image_size = [1024, 1024]
            else: 
                image_size = [832, 1216]
            image = pipe(
                prompt=prompt, 
                num_inference_steps=30,
                width=image_size[0], 
                height=image_size[1], 
            ).images[0]
            image.save(filepath_out, optimize=True, quality=50)


def herbs_gen():
    image_ratio = '1x1'
    category_folderpath = f'{vault}/terrawhisper/images/watercolor/herbs/{image_ratio}'
    herbs = []
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        data = json_read(json_filepath, create=True)
        for obj in data['herbs']:
            herb_name_scientific = obj['plant_name_scientific']
            if herb_name_scientific not in herbs:
                herbs.append(herb_name_scientific)
    ## gen images
    for herb_i, herb_name_scientific in enumerate(herbs[:]):
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
        print(f'{herb_name_scientific} {herb_i}/{len(herbs)}')
        filepath_out = f'{category_folderpath}/{herb_slug}.jpg'
        try: os.makedirs(f'{category_folderpath}')
        except: pass
        if os.path.exists(filepath_out): continue
        prompt = f'''
            {herb_name_scientific}, 
            watercolor,
            botanical medicinal illustration,
            beige background,
            high resolution
        '''
        print(prompt)
        if image_ratio == '1x1':
            image_size = [1024, 1024]
        image = pipe(
            prompt=prompt, 
            num_inference_steps=30,
            width=image_size[0], 
            height=image_size[1], 
        ).images[0]
        image.save(filepath_out, optimize=True, quality=50)

def herbs_old_gen():
    herbs_rows, herbs_cols = data_csv.herbs()
    print(herbs_rows)
    print(herbs_cols)
    herbs = []
    image_ratio = '1x1'
    category_folderpath = f'{vault}/terrawhisper/images/watercolor/herbs/{image_ratio}'
    herbs = [herb[herbs_cols['herb_name_scientific']] for herb in herbs_rows]
    ## gen images
    for herb_i, herb_name_scientific in enumerate(herbs[:]):
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
        print(f'{herb_name_scientific} {herb_i}/{len(herbs)}')
        filepath_out = f'{category_folderpath}/{herb_slug}.jpg'
        try: os.makedirs(f'{category_folderpath}')
        except: pass
        # if os.path.exists(filepath_out): continue
        prompt = f'''
            {herb_name_scientific}, 
            watercolor,
            botanical medicinal illustration,
            beige background,
            high resolution
        '''
        print(prompt)
        if image_ratio == '1x1':
            image_size = [1024, 1024]
        image = pipe(
            prompt=prompt, 
            num_inference_steps=30,
            width=image_size[0], 
            height=image_size[1], 
        ).images[0]
        image.save(filepath_out, optimize=True, quality=50)

def herbs_realistic():
    herbs_rows, herbs_cols = data_csv.herbs()
    print(herbs_rows)
    print(herbs_cols)
    herbs = []
    image_ratio = '1x1'
    category_folderpath = f'{vault}/terrawhisper/images/realistic/herbs/{image_ratio}'
    herbs = [herb[herbs_cols['herb_name_scientific']] for herb in herbs_rows]
    ## gen images
    for herb_i, herb_name_scientific in enumerate(herbs[:]):
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
        print(f'{herb_name_scientific} {herb_i}/{len(herbs)}')
        filepath_out = f'{category_folderpath}/{herb_slug}.jpg'
        try: os.makedirs(f'{category_folderpath}')
        except: pass
        # if os.path.exists(filepath_out): continue
        prompt = f'''
            {herb_name_scientific} plant, 
            nature,
            depth of field, 
            detailed texture, high resolution, cinematic
        '''
        print(prompt)
        if image_ratio == '1x1':
            image_size = [1024, 1024]
        image = pipe(
            prompt=prompt, 
            num_inference_steps=30,
            width=image_size[0], 
            height=image_size[1], 
        ).images[0]
        image.save(filepath_out, optimize=True, quality=50)

def popular_herbs_realistic():
    image_ratio = '1x1'
    category_folderpath = f'{vault}/terrawhisper/images/realistic/herbs/{image_ratio}'
    herbs = []
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        data = json_read(json_filepath, create=True)
        for obj in data['herbs']:
            herb_name_scientific = obj['plant_name_scientific']
            if herb_name_scientific not in herbs:
                herbs.append(herb_name_scientific)
    ## gen images
    for herb_i, herb_name_scientific in enumerate(herbs[:]):
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
        print(f'{herb_name_scientific} {herb_i}/{len(herbs)}')
        filepath_out = f'{category_folderpath}/{herb_slug}.jpg'
        try: os.makedirs(f'{category_folderpath}')
        except: pass
        if os.path.exists(filepath_out): continue
        prompt = f'''
            {herb_name_scientific} plant, 
            nature,
            depth of field, 
            detailed texture, high resolution, cinematic
        '''
        print(prompt)
        if image_ratio == '1x1':
            image_size = [1024, 1024]
        image = pipe(
            prompt=prompt, 
            num_inference_steps=30,
            width=image_size[0], 
            height=image_size[1], 
        ).images[0]
        image.save(filepath_out, optimize=True, quality=50)

def preparations_realistic():
    preparation_name = 'tincture'
    preparation_slug = preparation_name.replace(' ', '-') + 's'
    preparation_name_plural = preparation_name + 's'
    image_ratio = '1x1'
    category_folderpath = f'{vault}/terrawhisper/images/realistic/{preparation_slug}/{image_ratio}'
    herbs = []
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        data = json_read(json_filepath, create=True)
        for obj in data['herbs']:
            herb_name_scientific = obj['plant_name_scientific']
            if herb_name_scientific not in herbs:
                herbs.append(herb_name_scientific)
    ## gen images
    for herb_i, herb_name_scientific in enumerate(herbs[:]):
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
        print(f'{herb_name_scientific} {herb_i}/{len(herbs)}')
        filepath_out = f'{category_folderpath}/{herb_slug}.jpg'
        try: os.makedirs(f'{category_folderpath}')
        except: pass
        if os.path.exists(filepath_out): continue
        prompt = f'''
            close up of a bottle of {herb_name_scientific} herbal tincture, 
            on a wooden table, surrounded by medicinal herbs, 
            depth of field, bokeh, 
            detailed texture, high resolution, cinematic
        '''
        negative_prompt = f'''
            text, label, drawing, watermark
        '''
        print(prompt)
        if image_ratio == '1x1':
            image_size = [1024, 1024]
        image = pipe(
            prompt=prompt, 
            negative_prompt=negative_prompt, 
            num_inference_steps=30,
            width=image_size[0], 
            height=image_size[1], 
        ).images[0]
        image.save(filepath_out, optimize=True, quality=50)

def get_popular_teas():
    output = []
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}/teas'
        json_filepath = f'database/json/{url}.json'
        if os.path.exists(json_filepath):
            data = json_read(json_filepath, create=True)
            for obj in data['remedies']:
                found = False
                for item in output:
                    if obj['herb_name_scientific'] == item['herb_name_scientific']:
                        item['herb_total_score'] += obj['herb_total_score']
                        found = True
                        break
                if not found:
                    output.append({
                        'herb_name_scientific': obj['herb_name_scientific'],
                        'herb_total_score': obj['herb_total_score'],
                    })
    output = sorted(output, key=lambda x: x['herb_total_score'], reverse=True)
    return output

def gen_images_teas():
    teas = get_popular_teas()
    for tea in teas:
        herb_name_scientific = tea['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-').replace('.', '')
        images_vars = [
            'uses',
            'benefits',
            'constituents',
            'preparation',
            'side-effects',
        ]
        for image_var in images_vars:
            output_filepath_1 = f"{website_folderpath}/images-tmp/preparations/teas/{herb_slug}-{image_var}.jpg"
            output_filepath_2 = f"{website_folderpath}/images/teas/{herb_slug}-{image_var}.jpg"
            if os.path.exists(output_filepath_1): continue
            if os.path.exists(output_filepath_2): continue
            prompt = f'''
                a cup of herbal teas made with dry {herb_name_scientific} herb on a wooden table,
                indoor, 
                natural window light,
                earth tones,
                neutral colors,
                soft focus,
                warm tones,
                vintage,
                high resolution,
                cinematic
            '''
            negative_prompt = f'''
                text, watermark 
            '''
            print(prompt)
            pipe_init()
            image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
            image = img_resize(image, w=768, h=768)
            image.save(output_filepath_1)

def home_images_static():
    # hero
    slug = 'medicinal-plants'
    output_filepath = f'{website_folderpath}/images-static/{slug}.jpg'
    src = f'/images-static/{slug}.jpg'
    alt = f'medicinal plants'
    if not os.path.exists(output_filepath):
    # if True:
        prompt = f'''
            dry herbs and spices in jars,
            on a wooden table,
            indoor, 
            natural light,
            earth tones,
            neutral colors,
            soft focus,
            warm tones,
            vintage,
            depth of field, bokeh, 
        '''
        prompt = f'''
            a close-up of an apothecary cabinet full of herbs,
            indoor, 
            vintage,
            natural light,
            earth tones,
            neutral colors,
            soft focus,
            warm tones,
            cinematic,
        '''
        negative_prompt = f'''
            text, watermark 
        '''
        print(prompt)
        pipe_init()
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        image.save(output_filepath)

# home_images_static()

##################################################################################
# ;equipments
##################################################################################
prompt_style = f'''
    vintage,
    natural light,
    neutral colors,
    earth tones, warm tones,
    soft focus,
'''

def p_equipments_intro():
    output_filepath = f'{website_folderpath}/images-static/herbalists-equipments.jpg'
    if not os.path.exists(output_filepath):
    # if True:
        prompt = f'''
            close-up of pestle and mortar,
            wooden table,
            indoor, 
        '''
        prompt += prompt_style
        negative_prompt = f'''
            text, watermark 
        '''
        print(prompt)
        pipe_init()
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        image.save(output_filepath)

def a_equipments_intro():
    for equipment_slug in os.listdir(f'{vault}/amazon/json'):
        equipment_name = equipment_slug.lower().strip().replace('-', ' ')
        if equipment_name[-1] == 's': equipment_name = equipment_name[:-1]
        out_filepath = f'{website_folderpath}/images/equipments/{equipment_slug}.jpg'
        ast_filepath = f'assets/images/equipments/{equipment_slug}.jpg'
        tmp_filepath = f'assets/images/equipments-tmp/{equipment_slug}.jpg'
        if not os.path.exists(ast_filepath):
        # if True:
            prompt = f'''
                close-up of {equipment_name},
                on a wooden table,
                with herbs,
                indoor, 
            '''
            prompt += prompt_style
            negative_prompt = f'''
                text, watermark 
            '''
            print(prompt)
            pipe_init()
            image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
            image = img_resize(image, w=768, h=768)
            image.save(tmp_filepath)

# p_equipments_intro()
# a_equipments_intro()

def get_popular_herbs_from_teas_articles():
    output = []
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}/teas'
        json_filepath = f'database/json/{url}.json'
        if os.path.exists(json_filepath):
            data = json_read(json_filepath, create=True)
            for obj in data['remedies']:
                found = False
                for item in output:
                    if obj['herb_name_scientific'] == item['herb_name_scientific']:
                        item['herb_total_score'] += obj['herb_total_score']
                        found = True
                        break
                if not found:
                    output.append({
                        'herb_name_scientific': obj['herb_name_scientific'],
                        'herb_total_score': obj['herb_total_score'],
                    })
    output = sorted(output, key=lambda x: x['herb_total_score'], reverse=True)
    return output

def get_actions():
    popular_herbs = get_popular_herbs_from_teas_articles()
    categories = []
    for herb_i, herb in enumerate(popular_herbs[:]):
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        url = f'herbs/{herb_slug}'
        title = herb_name_scientific
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        if not os.path.exists(f'{website_folderpath}/herbs'): os.mkdir(f'{website_folderpath}/herbs')
        data = json_read(json_filepath, create=True)
        try: category_name_todo = data['category_action']
        except: continue
        found = False
        for category in categories:
            category_name_done = category['name']
            if category_name_todo == category_name_done:
                category['herbs'].append(herb_name_scientific)
                found = True
                break
        if not found:
            categories.append({
                'name': category_name_todo,
                'herbs': [herb_name_scientific]
            })
    return categories

def herbs_actions():
    actions_names = [action['name'] for action in get_actions()]
    image_w = 768
    image_h = 768
    for action_name in actions_names:
        action_name = action_name.split('/')[0]
        action_slug = action_name.lower().strip().replace(' ', '-')
        img = Image.new(mode="RGB", size=(image_w, image_h), color='#000000')
        draw = ImageDraw.Draw(img)
        text = f'{action_name}'.upper()
        title_font_size = 48
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, title_font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x = image_w//2 - text_w//2
        y = image_h//2 - text_h//2
        draw.text((x, y), text, '#ffffff', font=font)
        img.save(f'{website_folderpath}/images/herbs-actions/{action_slug}.jpg', format='JPEG', subsampling=0, quality=70)

def herbs_taxonomy_kingdoms_animalia():
    ast_filepath = f'assets/images/taxonomy/animalia.jpg'
    tmp_filepath = f'assets/images/tmp/animalia.jpg'
    if not os.path.exists(ast_filepath):
    # if True:
        prompt = f'''
            close-up of fox,
        '''
        prompt += prompt_style
        negative_prompt = f'''
            text, watermark 
        '''
        print(prompt)
        pipe_init()
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        image.save(tmp_filepath)

def herbs_taxonomy_kingdoms_plantae():
    out_filepath = f'{website_folderpath}/images/taxonomy/plantae.jpg'
    ast_filepath = f'assets/images/taxonomy/plantae.jpg'
    tmp_filepath = f'assets/images/tmp/plantae.jpg'
    tmp_filepath = ast_filepath
    # if not os.path.exists(ast_filepath):
    if True:
        prompt = f'''
            close-up of plant,
        '''
        prompt += prompt_style
        negative_prompt = f'''
            text, watermark 
        '''
        print(prompt)
        pipe_init()
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        image.save(tmp_filepath)
        image.save(out_filepath)

def herbs_taxonomy_kingdoms_fungi():
    out_filepath = f'{website_folderpath}/images/taxonomy/fungi.jpg'
    ast_filepath = f'assets/images/taxonomy/fungi.jpg'
    tmp_filepath = f'assets/images/tmp/fungi.jpg'
    tmp_filepath = ast_filepath
    # if not os.path.exists(ast_filepath):
    if True:
        prompt = f'''
            close-up of fungi,
        '''
        prompt += prompt_style
        negative_prompt = f'''
            text, watermark 
        '''
        print(prompt)
        pipe_init()
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        image.save(tmp_filepath)
        image.save(out_filepath)

def herbs_taxonomy_kingdoms_protista():
    out_filepath = f'{website_folderpath}/images/taxonomy/protista.jpg'
    ast_filepath = f'assets/images/taxonomy/protista.jpg'
    tmp_filepath = f'assets/images/tmp/protista.jpg'
    tmp_filepath = ast_filepath
    # if not os.path.exists(ast_filepath):
    if True:
        prompt = f'''
            close-up of protista,
        '''
        prompt += prompt_style
        negative_prompt = f'''
            text, watermark 
        '''
        print(prompt)
        pipe_init()
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        image.save(tmp_filepath)
        image.save(out_filepath)

def herbs_taxonomy_kingdoms_eubacteria():
    out_filepath = f'{website_folderpath}/images/taxonomy/eubacteria.jpg'
    ast_filepath = f'assets/images/taxonomy/eubacteria.jpg'
    tmp_filepath = f'assets/images/tmp/eubacteria.jpg'
    tmp_filepath = ast_filepath
    # if not os.path.exists(ast_filepath):
    if True:
        prompt = f'''
            close-up of eubacteria,
            high resolution,
        '''
        prompt += prompt_style
        negative_prompt = f'''
            text, watermark 
        '''
        print(prompt)
        pipe_init()
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        image.save(tmp_filepath)
        image.save(out_filepath)

def herbs_taxonomy_kingdoms_archaebacteria():
    out_filepath = f'{website_folderpath}/images/taxonomy/archaebacteria.jpg'
    ast_filepath = f'assets/images/taxonomy/archaebacteria.jpg'
    tmp_filepath = f'assets/images/tmp/archaebacteria.jpg'
    tmp_filepath = ast_filepath
    # if not os.path.exists(ast_filepath):
    if True:
        prompt = f'''
            close-up of archaebacteria,
            high resolution,
        '''
        prompt += prompt_style
        negative_prompt = f'''
            text, watermark 
        '''
        print(prompt)
        pipe_init()
        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = img_resize(image, w=768, h=768)
        image.save(tmp_filepath)
        image.save(out_filepath)

# herbs_actions()
# herbs_taxonomy_kingdoms_animalia()
# herbs_taxonomy_kingdoms_plantae()
# herbs_taxonomy_kingdoms_fungi()
# herbs_taxonomy_kingdoms_protista()
# herbs_taxonomy_kingdoms_eubacteria()
# herbs_taxonomy_kingdoms_archaebacteria()
