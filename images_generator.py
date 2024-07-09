import os
import random
import requests
import base64

import g
import util

vault_folderpath = '/home/ubuntu/vault'
preparation_name = 'essential oil'
# images_teas_folderpath = f'{vault_folderpath}/images/teas'
images_folderpath_out = f'{vault_folderpath}/images/{preparation_name}s'

herbs_rows = util.csv_get_rows(g.CSV_HERBS_AUTO_FILEPATH)
herbs_cols = util.csv_get_cols(herbs_rows)
herbs_rows = herbs_rows[1:]

i = -1
for herb_row in herbs_rows[:100]:
    i += 1
    herb_slug = herb_row[herbs_cols['herb_slug']]
    herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']]
    prompt = f'bottle of of {herb_name_scientific} {preparation_name} on a wooden table surrounded by medicinal herbs'
    # prompt = f'bottle of {herb_name_scientific} {preparation_name} on a wooden table surrounded by medicinal herbs'
    prompt += f', style gothic, cinematic, high resolution, portrait, macro photography'

    for j in range(100):
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

        export_folder = f'{images_folderpath_out}/{herb_slug}'
        if not os.path.exists(f'{images_folderpath_out}'): os.makedirs(f'{images_folderpath_out}')
        if not os.path.exists(f'{export_folder}'): os.makedirs(f'/{export_folder}')

        export_filepath = f'{export_folder}/{j}.png'
        with open(export_filepath, 'wb') as f:
            f.write(base64.b64decode(r['images'][0]))

    
    print(herb_row)

