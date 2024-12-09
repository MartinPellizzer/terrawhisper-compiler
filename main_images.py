# TMP
import os
import random
from tkinter import *

import torch
from diffusers import DiffusionPipeline
from diffusers import StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import ImageTk, Image, ImageFont, ImageDraw

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read, json_write
from oliark_llm import llm_reply
from oliark import img_resize

vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'
website_folderpath = 'website-2'

model_8b = f'/home/ubuntu/vault-tmp/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
model_validator_filepath = f'llms/Llama-3-Partonus-Lynx-8B-Instruct-Q4_K_M.gguf'
model = model_8b

checkpoint_filepath = f'{vault}/stable-diffusion/checkpoints/juggernautXL_juggXIByRundiffusion.safetensors'
pipe = None
def pipe_init():
    global pipe
    if not pipe:
        pipe = StableDiffusionXLPipeline.from_single_file(
            checkpoint_filepath, 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

def articles_preparations_2(preparation_slug):
    plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    preparation_name = preparation_slug.replace('-', ' ')
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        print(f'\n>> {ailment_i}/{len(ailments)} - preparation: {preparation_name}')
        print(f'    >> {ailment}')
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/remedies'): os.mkdir(f'{website_folderpath}/remedies')
        if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system'): os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system')
        if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system/{ailment_slug}'): os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system/{ailment_slug}')

        # if os.path.exists(json_filepath): os.remove(json_filepath)
        # continue

        data = json_read(json_filepath, create=True)
        data['ailment_slug'] = ailment_slug
        data['ailment_name'] = ailment_name
        data['system_slug'] = system_slug
        data['organ_slug'] = organ_slug
        data['preparation_slug'] = preparation_slug
        data['preparation_name'] = preparation_name
        data['url'] = url
        if 'lastmod' not in data: data['lastmod'] = today()

        if 'remedies_num' not in data: data['remedies_num'] = ''
        # data['remedies_num'] = ''
        if data['remedies_num'] == '': data['remedies_num'] = random.randint(7, 11)
        remedies_num = data['remedies_num']

        non_valid_preparations = [
            'decoctions',
        ]
        if preparation_slug not in non_valid_preparations:
            output_filepath = f'{website_folderpath}/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg'
            src = f'/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg'
            alt = f'herbal {preparation_name} for {ailment_name}'
            herbs_names_scientific = [x['herb_name_scientific'] for x in data["remedies"][:remedies_num]]
            herb_name_scientific = random.choice(herbs_names_scientific)
            print(output_filepath)
            if not os.path.exists(output_filepath):
            # if True:
                container = ''
                if preparation_slug == 'teas': container = 'a cup of'
                if preparation_slug == 'tinctures': container = 'a bottle of'
                if preparation_slug == 'essential-oils': container = 'a bottle of'
                prompt = f'''
                    {container} herbal {preparation_name} made with dry {herb_name_scientific} herb on a wooden table,
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
                running = True
                while running:
                    image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                    image = img_resize(image, w=768, h=768)
                    image.save(output_filepath)
                    img2 = ImageTk.PhotoImage(Image.open(output_filepath))
                    panel.configure(image=img2)
                    raw = input('next >>')
                    if raw.strip() != '': running = False

            for remedy_i, remedy in enumerate(data['remedies'][:remedies_num]):
                herb_name_scientific = remedy['herb_name_scientific']
                herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
                output_filepath = f'{website_folderpath}/images/preparations/{preparation_slug}/{herb_slug}-herbal-{preparation_slug}.jpg'
                src = f'/images/preparations/{preparation_slug}/{herb_slug}-herbal-{preparation_slug}.jpg'
                alt = f'{herb_name_scientific} herbal {preparation_name} for {ailment_name}'
                if not os.path.exists(output_filepath):
                    container = ''
                    if preparation_slug == 'teas': container = 'a cup of'
                    if preparation_slug == 'tinctures': container = 'a bottle of'
                    if preparation_slug == 'creams': container = 'a jar of'
                    if preparation_slug == 'essential-oils': container = 'a bottle of'
                    prompt = f'''
                        {container} herbal {preparation_name} made with dry {herb_name_scientific} herb on a wooden table,
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
                        text, watermark, label
                    '''
                    print(prompt)
                    pipe_init()
                    running = True
                    while running:
                        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                        image = img_resize(image, w=768, h=768)
                        image.save(output_filepath)
                        img2 = ImageTk.PhotoImage(Image.open(output_filepath))
                        panel.configure(image=img2)
                        raw = input('next >>')
                        if raw.strip() != '': running = False

root = Tk()
img = ImageTk.PhotoImage(Image.open("website-2/images-static/urinary.jpg"))
panel = Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")

# articles_preparations_2('teas')
# TODO: clean delete images in folder
# articles_preparations_2('tinctures')
articles_preparations_2('creams')
# articles_preparations_2('essential-oils')

root.mainloop()
