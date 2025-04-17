import os
import random
import json

import torch
from diffusers import DiffusionPipeline
from diffusers import StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image, ImageFont, ImageDraw
from torchvision import transforms
import matplotlib.pyplot as plt
from transformers import AutoModelForImageSegmentation

import g
import util

from oliark_io import json_read, json_write
from oliark_llm import llm_reply
from oliark import img_resize

import lib_plants

PLANTS_NUM = 50

plants_popular = [
    {
        'plant_slug': plant['herb_name_scientific'].lower().strip().replace(' ', '-'),
        'plant_name_scientific': plant['herb_name_scientific'],
    }
    for plant in lib_plants.teas_popular_get()
]
regen = True
if regen:
    json_plants_folderpath = f'assets/digital-products/cards/plants-new/plants-jsons'
    for plant in plants_popular:
        plant_slug = plant['plant_slug']
        print(plant)
        plant_name_scientific = plant['plant_name_scientific']
        json_plant_filepath = f'{json_plants_folderpath}/{plant_slug}'
        json_plant = json_read(json_plant_filepath, create=True)

        json_plant['plant_slug'] = plant_slug
        json_plant['plant_name_scientific'] = plant_name_scientific
        j = json.dumps(json_plant, indent=4)
        with open(json_plant_filepath, 'w') as f:
            print(j, file=f)

        key = 'plant_family'
        if key not in json_plant: json_plant[key] = ''
        if json_plant[key] == '':
            species = plant_name_scientific
            for _ in range(1):
                prompt = f'''
                    Write the Linnaean system of classification for the plant: {plant_name_scientific}.
                    The Linnaean system is classified by: Kingdom, Division, Class, Subclass, Order, Family, Genus, Species.
                    I will give you the Species and the Genus of this plant and you have to fill the rest. 
                    Use as few words as possible.
                    Reply with the following JSON format:
                    [
                        {{"Kingdom": "write the kingdom name here"}},
                        {{"Division": "write the division name here"}},
                        {{"Class": "write the class name here"}},
                        {{"Subclass": "write the subclass name here"}},
                        {{"Order": "write the order name here"}},
                        {{"Family": "write the family name here"}},
                        {{"Genus": "write the genus name here"}},
                        {{"Species": "{species}"}}
                    ]
                    Reply only with the JSON.
                '''
                reply = llm_reply(prompt)
                try: json_reply = json.loads(reply)
                except: json_reply = {}
                if json_reply != {}:
                    try: plant_kingdom = json_reply[0]['Kingdom'].strip().lower()
                    except: continue
                    try: plant_division = json_reply[1]['Division'].strip().lower()
                    except: continue
                    try: plant_class = json_reply[2]['Class'].strip().lower()
                    except: continue
                    try: plant_subclass = json_reply[3]['Subclass'].strip().lower()
                    except: continue
                    try: plant_order = json_reply[4]['Order'].strip().lower()
                    except: continue
                    try: plant_family = json_reply[5]['Family'].strip().lower()
                    except: continue
                    try: plant_genus = json_reply[6]['Genus'].strip().lower()
                    except: continue
                    try: plant_species = json_reply[7]['Species'].strip().lower()
                    except: continue
                    print('***************************************')
                    json_plant[key] = plant_family
                    j = json.dumps(json_plant, indent=4)
                    with open(json_plant_filepath, 'w') as f:
                        print(j, file=f)
    
        key = 'plant_names_common'
        if key not in json_plant: json_plant[key] = ''
        if json_plant[key] == '':
            species = plant_name_scientific
            for _ in range(1):
                prompt = f'''
                    Write a list of the 10 most popular common names for the plant: {plant_name_scientific}.
                    Reply with the following JSON format:
                    [
                        {{"Common Name": "write the common name 1 here"}},
                        {{"Common Name": "write the common name 2 here"}},
                        {{"Common Name": "write the common name 3 here"}},
                    ]
                    Reply only with the JSON.
                '''
                reply = llm_reply(prompt)
                try: json_reply = json.loads(reply)
                except: json_reply = {}
                if json_reply != {}:
                    plant_names_common = []
                    for row in json_reply:
                        plant_name_common = row['Common Name'].strip().lower()
                        plant_names_common.append(plant_name_common)
                    print('***************************************')
                    json_plant[key] = plant_names_common
                    j = json.dumps(json_plant, indent=4)
                    with open(json_plant_filepath, 'w') as f:
                        print(j, file=f)
    


checkpoint_filepath = f'{g.VAULT}/stable-diffusion/checkpoints/xl/juggernautXL_juggXIByRundiffusion.safetensors'
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

plants = [
    'achillea millefolium',
]

with open('assets/digital-products/cards/prompts/styles.txt') as f: styles = f.read().split('\n')

backgrounds = [
    'white background',
]

plant = random.choice(plants)
# style = random.choice(styles)
background = random.choice(backgrounds)

def images_by_styles():
    for style in styles:
        positive_prompt = f''
        positive_prompt += f'{plant}, '
        positive_prompt += f'{style}, '
        # positive_prompt += f'{background}, '
        negative_prompt = f'''
            text, watermark 
        '''
        img_w = 832
        img_h = 1216
        grid_n = 4
        if 1:
            pipe_init()
            images_filepaths = []
            for i in range(pow(grid_n, 2)):
                image = pipe(
                    prompt=positive_prompt, 
                    negative_prompt=negative_prompt, 
                    width=img_w, 
                    height=img_h, 
                    num_inference_steps=20, 
                    guidance_scale=7.0
                ).images[0]
                print(positive_prompt)
                try: os.mkdir(f'assets/digital-products/cards/images-tmp/{style}')
                except: pass
                image_filepath = f'assets/digital-products/cards/images-tmp/{style}/{i}.jpg'
                image.save(image_filepath)
                images_filepaths.append(image_filepath)
                # image.show()
        else:
            images_filepaths = []
            folderpath = f'assets/digital-products/cards/images-tmp' 
            filenames = os.listdir(folderpath)
            images_filepaths = []
            for filename in filenames:
                if 'preview' in filename: continue
                images_filepaths.append(f'{folderpath}/{filename}')

        pin_w = img_w*grid_n
        pin_h = img_h*grid_n
        img_w = int(pin_w*(1/grid_n))
        img_h = int(pin_h*(1/grid_n))
        gap = 8
        img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#000000')
        images = []
        for i in range(pow(grid_n, 2)):
            images.append(Image.open(images_filepaths[i]))

        for row_i in range(grid_n):
            for col_i in range(grid_n):
                img.paste(images[row_i*col_i+col_i], (img_w*col_i + gap*col_i, img_h*row_i + gap*row_i))
        # img.show()


        img.save(f'assets/digital-products/cards/images-tmp/previews/{style}.jpg')

def images_by_style(style):
    with open(f'assets/digital-products/cards/prompts/{style}.txt') as f: style_prompt = f.read()
    positive_prompt = f''
    positive_prompt += f'{plant}, '
    positive_prompt += f'{style_prompt}, '
    # positive_prompt += f'{background}, '
    negative_prompt = f'''
        text, watermark 
    '''
    img_w = 832
    img_h = 1216
    grid_n = 4
    if 1:
        pipe_init()
        images_filepaths = []
        for i in range(pow(grid_n, 2)):
            image = pipe(
                prompt=positive_prompt, 
                negative_prompt=negative_prompt, 
                width=img_w, 
                height=img_h, 
                num_inference_steps=20, 
                guidance_scale=7.0
            ).images[0]
            print(positive_prompt)
            try: os.mkdir(f'assets/digital-products/cards/images-tmp/{style}')
            except: pass
            image_filepath = f'assets/digital-products/cards/images-tmp/{style}/{i}.jpg'
            image.save(image_filepath)
            images_filepaths.append(image_filepath)
            # image.show()
    else:
        images_filepaths = []
        folderpath = f'assets/digital-products/cards/images-tmp' 
        filenames = os.listdir(folderpath)
        images_filepaths = []
        for filename in filenames:
            if 'preview' in filename: continue
            images_filepaths.append(f'{folderpath}/{filename}')

    pin_w = img_w*grid_n
    pin_h = img_h*grid_n
    img_w = int(pin_w*(1/grid_n))
    img_h = int(pin_h*(1/grid_n))
    gap = 8
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#000000')
    images = []
    for i in range(pow(grid_n, 2)):
        images.append(Image.open(images_filepaths[i]))

    for row_i in range(grid_n):
        for col_i in range(grid_n):
            img.paste(images[row_i*col_i+col_i], (img_w*col_i + gap*col_i, img_h*row_i + gap*row_i))
    # img.show()

    img.save(f'assets/digital-products/cards/images-tmp/previews/{style}.jpg')


def plants_images_by_style(style, ratio='2x3'):
    with open(f'assets/digital-products/cards/prompts/plants.txt') as f: lines = [line.strip().lower() for line in f.read().split('\n') if line.strip() != '']
    plants = [line.split('\\')[1] for line in lines]
    with open(f'assets/digital-products/cards/prompts/{style}.txt') as f: style_prompt = f.read()

    for plant in plants:
        plant_slug = plant.strip().lower().replace(' ', '-')
        positive_prompt = f''
        positive_prompt += f'{plant}, '
        positive_prompt += f'{style_prompt}, '
        negative_prompt = f'''
            text, watermark 
        '''
        if ratio == '1x1':
            img_w = 1024
            img_h = 1024
        else:
            img_w = 832
            img_h = 1216
        grid_n = 2
        images_filepaths = []
        if 1:
            pipe_init()
            for i in range(pow(grid_n, 2)):
                image = pipe(
                    prompt=positive_prompt, 
                    negative_prompt=negative_prompt, 
                    width=img_w, 
                    height=img_h, 
                    num_inference_steps=20, 
                    guidance_scale=7.0
                ).images[0]
                print(positive_prompt)
                try: os.mkdir(f'assets/digital-products/cards/plants')
                except: pass
                try: os.mkdir(f'assets/digital-products/cards/plants/{ratio}')
                except: pass
                try: os.mkdir(f'assets/digital-products/cards/plants/{ratio}/{plant_slug}')
                except: pass
                try: os.mkdir(f'assets/digital-products/cards/plants/{ratio}/{plant_slug}/{style}')
                except: pass
                image_filepath = f'assets/digital-products/cards/plants/{ratio}/{plant_slug}/{style}/{i}.jpg'
                image.save(image_filepath)
                images_filepaths.append(image_filepath)
        else:
            folderpath = f'assets/digital-products/cards/{ratio}/plants/{plant_slug}/{style}' 
            filenames = os.listdir(folderpath)
            images_filepaths = []
            for filename in filenames:
                image_filepath = f'{folderpath}/{filename}'
                images_filepaths.append(image_filepath)

        pin_w = img_w*grid_n
        pin_h = img_h*grid_n
        img_w = int(pin_w*(1/grid_n))
        img_h = int(pin_h*(1/grid_n))
        gap = 8
        img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#000000')
        images = []
        for i in range(pow(grid_n, 2)):
            images.append(Image.open(images_filepaths[i]))

        img_i = 0
        for row_i in range(grid_n):
            for col_i in range(grid_n):
                img.paste(images[img_i], (img_w*col_i + gap*col_i, img_h*row_i + gap*row_i))
                img_i += 1
        # img.show()

        previews_folderpath = f'assets/digital-products/cards/plants/{ratio}/0_previews'
        try: os.mkdir(f'{previews_folderpath}')
        except: pass
        try: os.mkdir(f'{previews_folderpath}/{style}')
        except: pass
        img.save(f'{previews_folderpath}/{style}/{plant}.jpg')
    
    # master preview
    images_filepaths = []
    for plant in plants:
        plant_slug = plant.strip().lower().replace(' ', '-')
        images_filepaths.append(f'assets/digital-products/cards/plants/{ratio}/{plant_slug}/{style}/0.jpg')

    for x in images_filepaths:
        print(x)
    print(len(images_filepaths))

    grid_n = 4
    pin_w = img_w*grid_n
    pin_h = img_h*grid_n
    img_w = int(pin_w*(1/grid_n))
    img_h = int(pin_h*(1/grid_n))
    gap = 8
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#000000')
    images = []
    for i in range(pow(grid_n, 2)):
        images.append(Image.open(images_filepaths[i]))

    img_i = 0
    for row_i in range(grid_n):
        for col_i in range(grid_n):
            img.paste(images[img_i], (img_w*col_i + gap*col_i, img_h*row_i + gap*row_i))
            img_i += 1
    # img.show()

    try: os.mkdir(f'assets/digital-products/cards/plants/{ratio}/previews')
    except: pass
    try: os.mkdir(f'assets/digital-products/cards/plants/{ratio}/previews/{style}')
    except: pass
    img.save(f'assets/digital-products/cards/plants/{ratio}/previews/{style}/0_master.jpg')
    
def plants_text_images_by_style(style, ratio='2x3'):
    with open(f'assets/digital-products/cards/prompts/plants.txt') as f: lines = [line.strip().lower() for line in f.read().split('\n') if line.strip() != '']
    plants = [line.split('\\')[1] for line in lines]
    with open(f'assets/digital-products/cards/prompts/{style}.txt') as f: style_prompt = f.read()
    for plant in plants:
        plant_slug = plant.strip().lower().replace(' ', '-')
        positive_prompt = f''
        positive_prompt += f'{plant}, '
        positive_prompt += f'{style_prompt}, '
        negative_prompt = f'''
            text, watermark 
        '''

        images_filepaths = []
        folderpath = f'assets/digital-products/cards/plants/{plant_slug}/{style}' 
        filenames = os.listdir(folderpath)
        images_filepaths = []
        for filename in filenames:
            image_filepath = f'{folderpath}/{filename}'
            images_filepaths.append(image_filepath)

        grid_n = 2
        if ratio == '1x1':
            img_w = 1024
            img_h = 1024
        elif ratio == '2x3':
            img_w = 832
            img_h = 1216

        font_size = 240
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        for i, image_filepath in enumerate(images_filepaths):
            text = 'test'
            img = Image.open(image_filepath)
            _, _, text_w, text_h = font.getbbox(text)
            draw = ImageDraw.Draw(img)
            draw.text((img_w//2 - text_w//2, img_h//2 - 320), text, '#ffffff', font=font)
            try: os.mkdir(f'assets/digital-products/cards/plants-text')
            except: pass
            try: os.mkdir(f'assets/digital-products/cards/plants-text/{plant_slug}')
            except: pass
            try: os.mkdir(f'assets/digital-products/cards/plants-text/{plant_slug}/{style}')
            except: pass
            image_filepath = f'assets/digital-products/cards/plants-text/{plant_slug}/{style}/{i}.jpg'
            img.save(image_filepath)

        pin_w = img_w*grid_n
        pin_h = img_h*grid_n
        img_w = int(pin_w*(1/grid_n))
        img_h = int(pin_h*(1/grid_n))
        gap = 8
        img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#000000')
        images = []
        for i in range(pow(grid_n, 2)):
            images.append(Image.open(images_filepaths[i]))
        img_i = 0
        for row_i in range(grid_n):
            for col_i in range(grid_n):
                img.paste(images[img_i], (img_w*col_i + gap*col_i, img_h*row_i + gap*row_i))
                img_i += 1
        try: os.mkdir(f'assets/digital-products/cards/previews')
        except: pass
        try: os.mkdir(f'assets/digital-products/cards/previews/{style}')
        except: pass
        img.save(f'assets/digital-products/cards/previews/{style}/{plant}.jpg')
    
    # master preview
    images_filepaths = []
    for plant in plants:
        plant_slug = plant.strip().lower().replace(' ', '-')
        images_filepaths.append(f'assets/digital-products/cards/plants/{plant_slug}/{style}/0.jpg')

    for x in images_filepaths:
        print(x)
    print(len(images_filepaths))

    grid_n = 4
    pin_w = img_w*grid_n
    pin_h = img_h*grid_n
    img_w = int(pin_w*(1/grid_n))
    img_h = int(pin_h*(1/grid_n))
    gap = 8
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#000000')
    images = []
    for i in range(pow(grid_n, 2)):
        images.append(Image.open(images_filepaths[i]))

    img_i = 0
    for row_i in range(grid_n):
        for col_i in range(grid_n):
            img.paste(images[img_i], (img_w*col_i + gap*col_i, img_h*row_i + gap*row_i))
            img_i += 1
    # img.show()

    try: os.mkdir(f'assets/digital-products/cards/previews')
    except: pass
    try: os.mkdir(f'assets/digital-products/cards/previews/{style}')
    except: pass
    img.save(f'assets/digital-products/cards/previews/{style}/_master.jpg')
    
'''
'''

# images_by_style('style-apothecary')
# plants_images_by_style('style-watercolor')
# plants_images_by_style('style-apothecary', ratio='1x1')
# plants_text_images_by_style('style-apothecary', ratio='1x1')

###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################

bg_model = None
def bg_remove_new(image):
    global bg_model
    if not bg_model:
        bg_model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
    torch.set_float32_matmul_precision(['high', 'highest'][0])
    bg_model.to('cuda')
    bg_model.eval()
    # Data settings
    image_size = (1024, 1024)
    transform_image = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    input_images = transform_image(image).unsqueeze(0).to('cuda')
    # Prediction
    with torch.no_grad():
        preds = bg_model(input_images)[-1].sigmoid().cpu()
    pred = preds[0].squeeze()
    pred_pil = transforms.ToPILImage()(pred)
    mask = pred_pil.resize(image.size)
    image.putalpha(mask)
    return image

def plants_new_images_by_style():
    style = 'style-apothecary'
    with open(f'assets/digital-products/cards/prompts/{style}.txt') as f: style_prompt = f.read()
    json_plants_folderpath = f'assets/digital-products/cards/plants-new/plants-jsons'
    for plant_i, plant in enumerate(plants_popular[:50]):
        print(f'{plant_i}/{len(plants_popular)} - {plant_popular}')
        plant_slug = plant['plant_slug']
        json_plant_filepath = f'{json_plants_folderpath}/{plant_slug}'
        json_plant = json_read(json_plant_filepath)
        plant_name_scientific = json_plant['plant_name_scientific']
        positive_prompt = f'''
            {plant_name_scientific},
            {style_prompt}
        '''
        negative_prompt = f'''
            text, watermark 
        '''
        img_w = 832
        img_h = 1216
        images_filepaths = []
        pipe_init()
        image = pipe(
            prompt=positive_prompt, 
            negative_prompt=negative_prompt, 
            width=img_w, 
            height=img_h, 
            num_inference_steps=20, 
            guidance_scale=7.0
        ).images[0]
        print(positive_prompt)
        image_filepath = f'assets/digital-products/cards/plants-new/tmp/{plant_slug}.jpg'
        image.save(image_filepath)

def plants_new_images_remove_bg():
    json_plants_folderpath = f'assets/digital-products/cards/plants-new/plants-jsons'
    for plant_i, plant in enumerate(plants_popular[:50]):
        print(f'{plant_i}/{len(plants)} - {plant}')
        plant_slug = plant['plant_slug']
        json_plant_filepath = f'{json_plants_folderpath}/{plant_slug}'
        json_plant = json_read(json_plant_filepath)
        plant_name_scientific = json_plant['plant_name_scientific']
        image_filepath = f'assets/digital-products/cards/plants-new/valid/{plant_slug}.jpg'
        image = Image.open(image_filepath)
        image = bg_remove_new(image)
        image_filepath = f'assets/digital-products/cards/plants-new/valid-alpha/{plant_slug}.png'
        image.save(image_filepath)

def plants_new_cards_images():
    json_plants_folderpath = f'assets/digital-products/cards/plants-new/plants-jsons'
    for plant_i, plant in enumerate(plants_popular[:PLANTS_NUM]):
        print(f'{plant_i}/{len(plants)} - {plant}')
        plant_slug = plant['plant_slug']
        json_plant_filepath = f'{json_plants_folderpath}/{plant_slug}'
        json_plant = json_read(json_plant_filepath)
        plant_name_scientific = json_plant['plant_name_scientific']
        plant_family = json_plant['plant_family']
        plant_names_common = json_plant['plant_names_common']

        card_w, card_h = 900, 1500
        plant_w, plant_h = 832, 1216
        plant_w = int(plant_w*0.70)
        plant_h = int(plant_h*0.70)
        plant_h_off = 30
        img = Image.new(mode="RGBA", size=(card_w, card_h), color='#ffffff')

        image_filepath = f'assets/digital-products/cards/plants-new/bg-papers/0002.jpg'
        bg_paper = Image.open(image_filepath)
        bg_paper = img_resize(bg_paper, card_w+10, card_h+10)
        img.paste(bg_paper, (-5, -5))

        image_filepath = f'assets/digital-products/cards/plants-new/valid-alpha/{plant_slug}.png'
        plant_alpha = Image.open(image_filepath)
        plant_alpha = img_resize(plant_alpha, plant_w, plant_h)
        img.paste(plant_alpha, (card_w//2 - plant_w//2, card_h//2 - plant_h//2 + plant_h_off), plant_alpha)

        text = plant_name_scientific.capitalize()
        font_size = 36
        font_family, font_weight = 'Rye', 'Regular'
        font_path = f"assets/digital-products/cards/plants-new/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw = ImageDraw.Draw(img)
        draw.text((card_w//2 - text_w//2, 205), text, '#372D24', font=font)

        text = plant_family.capitalize()
        font_size = 36
        font_family, font_weight = 'Allura', 'Regular'
        font_path = f"assets/digital-products/cards/plants-new/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw = ImageDraw.Draw(img)
        draw.text((card_w//2 - text_w//2, 245), text, '#372D24', font=font)

        plant_names_common_x3 = ', '.join(plant_names_common[:3]) + ','
        text = plant_names_common_x3
        font_size = 24
        font_family, font_weight = 'IM_Fell_English', 'Regular'
        font_path = f"assets/digital-products/cards/plants-new/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw = ImageDraw.Draw(img)
        draw.text((card_w//2 - text_w//2, 1255), text, '#372D24', font=font)

        plant_names_common_x3 = ', '.join(plant_names_common[3:6])
        text = plant_names_common_x3
        font_size = 24
        font_family, font_weight = 'IM_Fell_English', 'Regular'
        font_path = f"assets/digital-products/cards/plants-new/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw = ImageDraw.Draw(img)
        draw.text((card_w//2 - text_w//2, 1285), text, '#372D24', font=font)

        # bg_paper.show()
        # plant_alpha.show()
        # img.show()
        image_filepath = f'assets/digital-products/cards/plants-new/cards-images/{plant_slug}.png'
        img.save(image_filepath)
        # quit()

# plants_new_images_by_style()
# plants_new_images_remove_bg()
plants_new_cards_images()
