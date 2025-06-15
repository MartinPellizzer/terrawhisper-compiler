import os

import torch
from diffusers import DiffusionPipeline
from diffusers import StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler 
from PIL import Image, ImageFont, ImageDraw 
from torchvision import transforms
import matplotlib.pyplot as plt
from transformers import AutoModelForImageSegmentation

from oliark import img_resize

from lib import g

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

def icons_gen(command):
    pipe_init()
    images_filepaths = []
    img_w = 1024
    img_h = 1024
    icons = [
        'drop of water',
        'flower',
        'clock',
        'thermometer',
        'lavender plant',
        'ginger plant',
        'echinacea plant',
        'rosemary plant',
        'teapot',
        'teacup',
        'teaspoon',
        'strainer',
        'mortar and pestle',
    ]
    i = 0
    if command == 'all':
        for icon in icons:
            i_srt = ''
            if i < 10: i_str = f'000{i}'
            elif i < 100: i_str = f'00{i}'
            elif i < 1000: i_str = f'0{i}'
            elif i < 10000: i_str = f'{i}'
            positive_prompt = f'''
                {icon},
                icon,
                hand drawn, dark lines, monocrome,
                vintage, victorian, rustic, elegant, minimalist, 
                light background,
            '''
            negative_prompt = f'''
                text, watermark 
            '''
            image = pipe(
                prompt=positive_prompt, 
                negative_prompt=negative_prompt, 
                width=img_w, 
                height=img_h, 
                num_inference_steps=20, 
                guidance_scale=7.0
            ).images[0]
            print(positive_prompt)
            folderpath = f'assets/digital-products/preparations-cheatsheets'
            try: os.mkdir(f'{folderpath}/tmp')
            except: pass
            image_filepath = f'{folderpath}/tmp/{i_str}.jpg'
            image.save(image_filepath)
            images_filepaths.append(image_filepath)
            # image.show()
            i += 1
    else: 
        i = int(command)
        if i >= 0 and i < len(icons):
            icon = icons[i]
            i_srt = ''
            if i < 10: i_str = f'000{i}'
            elif i < 100: i_str = f'00{i}'
            elif i < 1000: i_str = f'0{i}'
            elif i < 10000: i_str = f'{i}'
            positive_prompt = f'''
                {icon},
                icon,
                hand drawn, dark lines, monocrome,
                vintage, victorian, rustic, elegant, minimalist, 
                light background,
            '''
            negative_prompt = f'''
                text, watermark 
            '''
            image = pipe(
                prompt=positive_prompt, 
                negative_prompt=negative_prompt, 
                width=img_w, 
                height=img_h, 
                num_inference_steps=20, 
                guidance_scale=7.0
            ).images[0]
            print(positive_prompt)
            folderpath = f'assets/digital-products/preparations-cheatsheets'
            try: os.mkdir(f'{folderpath}/tmp')
            except: pass
            image_filepath = f'{folderpath}/tmp/{i_str}.jpg'
            image.save(image_filepath)
            images_filepaths.append(image_filepath)
            # image.show()
            i += 1

def icons_grid():
    folderpath = f'assets/digital-products/preparations-cheatsheets/tmp'
    images_filepaths = [f'{folderpath}/{filename}' for filename in os.listdir(folderpath)]
    images_filepaths.sort()
    pin_w = 1024
    pin_h = 1024
    grid_n = 4
    image_max_n = 13
    img_w = int(pin_w*(1/grid_n))
    img_h = int(pin_h*(1/grid_n))
    gap = 8
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#000000')
    images = []
    image_max_cur = 0
    for i in range(pow(grid_n, 2)):
        _img = Image.open(images_filepaths[i])
        _img = img_resize(_img, img_w, img_h)
        images.append(_img)
        image_max_cur += 1
        if image_max_cur >= image_max_n:
            break

    image_max_cur = 0
    to_break = False
    i = 0
    for row_i in range(grid_n):
        if to_break:
            break
        for col_i in range(grid_n):
            img.paste(images[i], (img_w*col_i + gap*col_i, img_h*row_i + gap*row_i))
            image_max_cur += 1
            if image_max_cur >= image_max_n:
                to_break = True
            i += 1
            if to_break:
                break

    folderpath = f'assets/digital-products/preparations-cheatsheets'
    image_filepath = f'{folderpath}/preview.jpg'
    img.save(image_filepath)
    # img.show()

def icons_grid_alpha():
    folderpath = f'assets/digital-products/preparations-cheatsheets/alpha'
    images_filepaths = [f'{folderpath}/{filename}' for filename in os.listdir(folderpath)]
    images_filepaths.sort()
    pin_w = 1024
    pin_h = 1024
    grid_n = 4
    image_max_n = 13
    img_w = int(pin_w*(1/grid_n))
    img_h = int(pin_h*(1/grid_n))
    gap = 8
    img = Image.new(mode="RGBA", size=(pin_w, pin_h), color='#ffffff')
    images = []
    image_max_cur = 0
    for i in range(pow(grid_n, 2)):
        _img = Image.open(images_filepaths[i])
        _img = img_resize(_img, img_w, img_h)
        images.append(_img)
        image_max_cur += 1
        if image_max_cur >= image_max_n:
            break
    image_max_cur = 0
    to_break = False
    i = 0
    for row_i in range(grid_n):
        if to_break:
            break
        for col_i in range(grid_n):
            img.paste(images[i], (img_w*col_i + gap*col_i, img_h*row_i + gap*row_i), images[i])
            image_max_cur += 1
            if image_max_cur >= image_max_n:
                to_break = True
            i += 1
            if to_break:
                break
    img = img.convert('RGB')
    folderpath = f'assets/digital-products/preparations-cheatsheets'
    image_filepath = f'{folderpath}/preview-alpha.jpg'
    img.save(image_filepath)

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

def plants_new_images_remove_bg():
    input_folderpath = f'assets/digital-products/preparations-cheatsheets/tmp'
    input_filepaths = [f'{input_folderpath}/{filepath}' for filepath in os.listdir(input_folderpath)]
    output_folderpath = f'assets/digital-products/preparations-cheatsheets/alpha'
    try: os.mkdir(output_folderpath)
    except: pass
    for input_filepath in input_filepaths:
        output_filename = input_filepath.split('/')[-1].split('.')[0] + '.png'
        output_filepath = f'{output_folderpath}/{output_filename}'
        image = Image.open(input_filepath)
        image = bg_remove_new(image)
        image.save(output_filepath)

plants_new_images_remove_bg()

if 0:
    while True:
        command = input('>> ')
        icons_gen(command)
        icons_grid()

# icons_grid_alpha()
