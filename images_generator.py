import os
import requests
import base64

import g
import util
import data_csv

def preparations():
    vault_folderpath = '/home/ubuntu/vault'
    preparation_name = 'tea'
    # images_teas_folderpath = f'{vault_folderpath}/images/teas'
    images_folderpath_out = f'{vault_folderpath}/images/2x3/{preparation_name}s'
    images_folderpath_out = f'{vault_folderpath}/images/2x3/herbs'

    herbs_rows, herbs_cols = data_csv.herbs()

    starting_herb_index = 0
    images_num_min = 999
    for herb_index, herb_row in enumerate(herbs_rows):
        herb_slug = herb_row[herbs_cols['herb_slug']]
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']]
        export_folder = f'{images_folderpath_out}/{herb_slug}'
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
        export_folder = f'{images_folderpath_out}/{herb_slug}'
        # if os.path.exists(export_folder): continue
        # prompt = f'cup of {herb_name_scientific} herbal {preparation_name}, on a wooden table, surrounded by medicinal herbs'
        prompt = f'{herb_name_scientific} herb, on a wooden table, surrounded by medicinal herbs'
        prompt += f', cinematic, high resolution, macro photography'
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

            if not os.path.exists(f'{images_folderpath_out}'): os.makedirs(f'{images_folderpath_out}')
            if not os.path.exists(f'{export_folder}'): os.makedirs(f'/{export_folder}')

            images_filenames = os.listdir(export_folder)
            id_max = 0
            for image_filename in images_filenames:
                if id_max < int(image_filename.split('.')[0]):
                    id_max = int(image_filename.split('.')[0])
            id_next = id_max + 1

            export_filepath = f'{export_folder}/{id_next}.png'
            with open(export_filepath, 'wb') as f:
                f.write(base64.b64decode(r['images'][0]))

        print(herb_row)

preparations()
