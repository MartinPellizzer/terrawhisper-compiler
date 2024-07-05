import os
import random
import requests
import base64

import g
import util

vault_folderpath = '/home/ubuntu/vault'
images_teas_folderpath = f'{vault_folderpath}/images/teas'

herbs_rows = util.csv_get_rows(g.CSV_HERBS_AUTO_FILEPATH)
herbs_cols = util.csv_get_cols(herbs_rows)
herbs_rows = herbs_rows[1:]

i = -1
for herb_row in herbs_rows[:10]:
    i += 1
    herb_slug = herb_row[herbs_cols['herb_slug']]
    herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']]
    prompt = f'cup of {herb_name_scientific} tea on a wooden table surrounded by medicinal herbs'
    prompt += f', style gothic, cinematic, high resolution, portrait, macro photography'

    for j in range(10):
        print(f'{herb_name_scientific} {i}/{len(herbs_rows)} - iter: {j}/100')
        payload = {
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "steps": 30,
            "cfg_scale": 7,
            "denoising_strength": 0.7,
            "sampler_name": "DPM++ 2M",
            "scheduler": "Karras",
            "seed": -1,
            "batch_size": 1
        }
        response = requests.post(url='http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload)
        r = response.json()

        export_folder = f'{images_teas_folderpath}/{herb_slug}'
        if not os.path.exists(f'{images_teas_folderpath}'): os.makedirs(f'{images_teas_folderpath}')
        if not os.path.exists(f'{export_folder}'): os.makedirs(f'/{export_folder}')

        export_filepath = f'{export_folder}/{j}.png'
        with open(export_filepath, 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))

    
    print(herb_row)

quit()



for i, herb in enumerate(herbs):
    prompt = f'cup of {herb} tea on a wooden table surrounded by medicinal herbs'
    prompt += f', style gothic, cinematic, high resolution, portrait, macro photography'
    for j in range(100):
        print(f'herb: (herb) {i}/{len(herbs)} - iter: {j}/100')
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

        export_folder = f'teas/{herb}'
        if not os.path.exists(f'export/teas'): os.makedirs(f'export/teas')
        if not os.path.exists(f'export/{export_folder}'): os.makedirs(f'export/{export_folder}')

        export_filepath = f'export/{export_folder}/{j}.png'
        with open(export_filepath, 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))

