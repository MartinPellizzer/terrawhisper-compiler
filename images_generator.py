import os
import requests
import base64

from PIL import Image

import g
import util
import data_csv

def gen_images():
    vault = '/home/ubuntu/vault'
    category_name = 'capsule'
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

    i = -1
    for herb_row in herbs_rows[starting_herb_index:]:
        i += 1
        herb_slug = herb_row[herbs_cols['herb_slug']]
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']]
        prompt = f'{herb_name_scientific} herbal {category_name}, on a wooden table, surrounded by medicinal herbs'
        prompt += f', high resolution, cinematic, macro photography'
        print(prompt)

        for j in range(10):
            print(f'{herb_name_scientific} {i}/{len(herbs_rows)} - iter: {j}/100')
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
            tmp_filepath = f'{vault}/terrawhisper/images/tmp/tmp.png'
            with open(tmp_filepath, 'wb') as f:
                f.write(base64.b64decode(r['images'][0]))

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

gen_images()
