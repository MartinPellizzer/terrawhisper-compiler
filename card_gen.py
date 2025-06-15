import os
import shutil

import torch
from diffusers import DiffusionPipeline
from diffusers import StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler 
from PIL import Image, ImageFont, ImageDraw 
from torchvision import transforms
import matplotlib.pyplot as plt
from transformers import AutoModelForImageSegmentation

from lib import g
from lib import io
from lib import utils

from oliark import img_resize

CARD_N = 9999

plants = io.csv_to_dict(f'database/herbs-book-0000.csv')

checkpoint_filepath = f'{g.VAULT}/stable-diffusion/checkpoints/xl/juggernautXL_juggXIByRundiffusion.safetensors'
pipe = None
bg_model = None

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

def plants_images_gen():
    for plant_i, plant in enumerate(plants[:CARD_N]):
        print(f'{plant_i}/{len(plants)} - {plant}')
        plant_slug = utils.sluggify(plant['latin_name'])
        plant_name_scientific = plant['latin_name']
        plant_name_common = plant['common_name']

        image_filepath_tmp = f'assets/shop/cards/plants/tmp/{plant_slug}.jpg'
        image_filepath_valid = f'assets/shop/cards/plants/valid/{plant_slug}.jpg'
        if os.path.exists(image_filepath_valid): continue
        positive_prompt = f'''
            {plant_name_scientific},
            botanical illustration,
            vintage style,
            color tea-stained, muted greens,
            rustic elegance,
            aged paper texture,
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
            guidance_scale=6.0
        ).images[0]
        print(positive_prompt)
        image.save(image_filepath_tmp)

def plants_images_alpha_gen():
    input_folderpath = f'assets/shop/cards/plants/valid'
    output_folderpath = f'assets/shop/cards/plants/alpha'
    try: os.mkdir(output_folderpath)
    except: pass
    for plant_i, plant in enumerate(plants[:CARD_N]):
        print(f'{plant_i}/{len(plants)} - {plant}')
        plant_slug = utils.sluggify(plant['latin_name'])
        plant_name_scientific = plant['latin_name']
        plant_name_common = plant['common_name']

        image_filepath = f'{input_folderpath}/{plant_slug}.jpg'
        image = Image.open(image_filepath)
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
        image_filepath = f'{output_folderpath}/{plant_slug}.png'
        image.save(image_filepath)

def plants_cards_images():
    input_folderpath = f'assets/shop/cards/plants/valid'
    output_folderpath = f'assets/shop/cards/plants/final'
    try: os.mkdir(output_folderpath)
    except: pass
    for filename in os.listdir(output_folderpath):
        os.remove(f'{output_folderpath}/{filename}')
    for plant_i, plant in enumerate(plants[:CARD_N]):
        print(f'{plant_i}/{len(plants)} - {plant}')
        plant_slug = utils.sluggify(plant['latin_name'])
        plant_name_scientific = plant['latin_name']
        plant_name_common = plant['common_name']
        card_w, card_h = 900, 1500
        plant_w, plant_h = 832, 1216
        plant_w = int(plant_w*0.95)
        plant_h = int(plant_h*0.95)
        plant_h_off = -50
        img = Image.new(mode="RGBA", size=(card_w, card_h), color='#ffffff')
        bg_filepath = f'assets/shop/cards/plants/assets/bg.jpg'
        bg_paper = Image.open(bg_filepath)
        bg_paper = img_resize(bg_paper, card_w+10, card_h+10)
        img.paste(bg_paper, (-5, -5))
        image_filepath = f'assets/shop/cards/plants/alpha/{plant_slug}.png'
        plant_alpha = Image.open(image_filepath)
        plant_alpha = img_resize(plant_alpha, plant_w, plant_h)
        img.paste(plant_alpha, (card_w//2 - plant_w//2, card_h//2 - plant_h//2 + plant_h_off), plant_alpha)
        label_filepath = f'assets/shop/cards/plants/assets/label.png'
        label_image = Image.open(label_filepath)
        label_w, label_h = label_image.size
        img.paste(label_image, (0, card_h - label_h), label_image)
        draw = ImageDraw.Draw(img)
        words = plant_name_scientific.title().strip().split(' ')
        font_size = 64
        font_family, font_weight = 'Rye', 'Regular'
        font_path = f"assets/shop/cards/plants/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        for i, word in enumerate(words):
            _, _, text_w, text_h = font.getbbox(word)
            draw.text((card_w//2 - text_w//2, 1160 + font_size*i), word, '#372D24', font=font)
        image_filepath = f'{output_folderpath}/{plant_slug}.jpg'
        img = img.convert('RGB')
        img.save(image_filepath, format='JPEG', quality=30)
        # img.show()
        # quit()

def plants_cards_final_split():
    part_n = 150
    input_folderpath = f'assets/shop/cards/plants/final'
    output_folderpath = f'assets/shop/cards/plants/final-split'
    try: shutil.rmtree(output_folderpath)
    except: pass
    try: os.mkdir(output_folderpath)
    except: pass
    plants_llst = []
    plants_lst = []
    plants = os.listdir(input_folderpath)
    for plant_i, plant_filename in enumerate(plants):
        print(f'{plant_i}/{len(plants)} - {plant_filename}')

        _output_folderpath = f'{output_folderpath}/healing-herb-botanical-name-card-part-{len(plants_llst)+1}'
        try: os.mkdir(_output_folderpath)
        except: pass
        plants_lst.append({
            'input_filepath': f'{input_folderpath}/{plant_filename}',
            'output_filepath': f'{_output_folderpath}/{plant_filename}',
        })

        if len(plants_lst) >= part_n:
            plants_llst.append(plants_lst)
            plants_lst = []

    if plants_lst != []:
        plants_llst.append(plants_lst)

    for plants_lst in plants_llst:
        for plant in plants_lst:
            shutil.copy2(plant['input_filepath'], plant['output_filepath'])

# plants_images_gen()
# plants_images_alpha_gen()
# plants_cards_images()
plants_cards_final_split()
