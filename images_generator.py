import os
import requests
import base64

from PIL import Image

import g
import util
import data_csv

import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read, json_write

ailments = csv_read_rows_to_json('systems-organs-ailments.csv')

vault = '/home/ubuntu/vault'

checkpoint_filepath = '/home/ubuntu/vault/stable-diffusion/checkpoints/juggernautXL_juggXIByRundiffusion.safetensors'
pipe = StableDiffusionXLPipeline.from_single_file(
    checkpoint_filepath, 
    torch_dtype=torch.float16, 
    use_safetensors=True, 
    variant="fp16"
).to('cuda')
pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config, 
    use_karras_sigmas=True, 
)

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
    preparation_name = 'tea'
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
            close up of a cup of {herb_name_scientific} herbal tea, 
            on a wooden table, surrounded by medicinal herbs, 
            depth of field, bokeh, 
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

# gen_images_new()
# herbs_gen()
# herbs_old_gen()

# herbs_realistic()
# popular_herbs_realistic()

preparations_realistic()

'''
payload = {
    "prompt": prompt,
    "width": 832,
    "height": 1216,
    "steps": 30,
    "cfg_scale": 6,
    "denoising_strength": 0.7,
    "sampler_name": "DPM++ 2M",
    "scheduler": "Karras",
    "seed": -1,
    "batch_size": 1
}
response = requests.post(url='http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload)
r = response.json()

## save raw image (tmp)
with open(tmp_filepath, 'wb') as f:
    f.write(base64.b64decode(r['images'][0]))
'''

