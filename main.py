import os
import time
import json
import shutil
import random
import datetime
from PIL import Image, ImageDraw, ImageFont

import g
import util
import utils_ai
import util_image
import util_data
import sitemap

import prompts

import data_csv

from lib import components
from lib import templates
from lib import tw_json

from oliark_io import file_write
from oliark_io import json_read, json_write
from oliark_io import csv_read_rows_to_json
from oliark import img_resize, img_resize_save, tw_img_gen_web_herb_rnd
from oliark_llm import llm_reply

import chromadb
from chromadb.utils import embedding_functions

import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

images_folder = 'C:/terrawhisper-assets/images/'
vault_folderpath = '/home/ubuntu/vault'
vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'

model = f'{vault_folderpath}/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
# model = f'{vault_folderpath}/llms/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf'

header_html = components.header()
footer_html = components.footer()

with open('assets/scripts/google-adsense.txt') as f: google_adsense_tag = f.read()

if not os.path.exists('website/images'): os.makedirs('website/images')

'''
checkpoint_filepath = f'{vault}/stable-diffusion/checkpoints/juggernautXL_juggXIByRundiffusion.safetensors'
pipe = StableDiffusionXLPipeline.from_single_file(
    checkpoint_filepath, 
    torch_dtype=torch.float16, 
    use_safetensors=True, 
    variant="fp16"
).to('cuda')
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
'''

plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')


# CSV MAIN
status_rows, status_cols = data_csv.status()
systems_rows, systems_cols = data_csv.systems()
preparations_rows, preparations_cols = data_csv.preparations()
herbs_rows, herbs_cols = data_csv.herbs()
herbs_names_common_rows, herbs_names_common_cols = data_csv.herbs_names_common()

# CSV JUNCTIONS
herbs_benefits_rows, herbs_benefits_cols = data_csv.herbs_benefits()
herbs_constituents_rows, herbs_constituents_cols = data_csv.herbs_constituents()
herbs_preparations_rows, herbs_preparations_cols = data_csv.herbs_preparations()
herbs_side_effects_rows, herbs_side_effects_cols = data_csv.herbs_side_effects()
herbs_precautions_rows, herbs_precautions_cols = data_csv.herbs_precautions()
status_systems_rows, status_systems_cols = data_csv.status_systems()
status_organs_rows, status_organs_cols = data_csv.status_organs()
status_herbs_rows, status_herbs_cols = data_csv.status_herbs()
status_preparations_rows, status_preparations_cols = data_csv.status_preparations()
status_preparations_teas_rows, status_preparations_teas_cols = data_csv.status_preparations_teas()
status_preparations_tinctures_rows, status_preparations_tinctures_cols = data_csv.status_preparations_tinctures()
status_preparations_decoctions_rows, status_preparations_decoctions_cols = data_csv.status_preparations_decoctions()
status_preparations_essential_oils_rows, status_preparations_essential_oils_cols = data_csv.status_preparations_essential_oils()
status_preparations_capsules_rows, status_preparations_capsules_cols = data_csv.status_preparations_capsules()
status_preparations_creams_rows, status_preparations_creams_cols = data_csv.status_preparations_creams()

# DEBUG
DEBUG_REMEDY_IMG_FOLDER_MISSING = 0
DEBUG_MISS_IMG_KEY_FEATURED = 0
DEBUG_MISS_IMG_KEY_LST = 0
DEBUG_MISS_REMEDY_DESC = 0
DEBUG_MISS_REMEDY_CONSTITUENTS = 0
DEBUG_MISS_REMEDY_PARTS = 0
DEBUG_MISS_REMEDY_RECIPE = 0
DEBUG_PROBLEMS = 0
DEBUG_PLANTS = 0
DEBUG_PLANTS_MEDICINE_BENEFITS = 0
DEBUG_PLANTS_MEDICINE_PREPARATIONS = 1
DEBUG_STATUS = 1
DEBUG_PREPARATION = 1
DEBUG_STATUS_JSON_FILEPATH = 0

# CONST
PREPARATIONS_NUM = 10

def today():
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    day = today.day
    today = f'{year}-{month}-{day}'
    print(today)
    return today


def redirect(html_filepath, source, target):
    old_plant_filepath = html_filepath.replace(target, source)
    web_plant_filepath = html_filepath.replace('website/', '')
    if not os.path.exists(old_plant_filepath):
        util.create_folder_for_filepath(old_plant_filepath)
        html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta http-equiv="refresh" content="0; url=https://terrawhisper.com/{web_plant_filepath}">
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="Leen Randell">
            <link rel="stylesheet" href="/style.css">
            <title>Content Permanently Moved (Redirected)</title>
        </head>
        <body>
        </body>
        </html>
        '''
        util.file_write(old_plant_filepath, html)

# #########################################################
# ;ai
# #########################################################
def ai_paragraph_aka(json_filepath, data, key, aka, prompt):
    herb_name_common = data['herb_name_common']
    if key not in data:
        reply = llm_reply(prompt)
        reply = reply.replace(aka, '')
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 1:
            reply_formatted = lines[0]
            print('*******************************************')
            print(reply_formatted)
            print('*******************************************')
            data[key] = reply_formatted
            util.json_write(json_filepath, data)

def ai_paragraph(json_filepath, data, key, prompt, regen=False):
    if key not in data: data[key] = []
    if regen: data[key] = []
    if data[key] == []:
        reply = llm_reply(prompt)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if line.endswith(':'): continue
            lines.append(line)
        if len(lines) == 1:
            reply_formatted = lines[0]
            print('*******************************************')
            print(reply_formatted)
            print('*******************************************')
            data[key] = reply_formatted
            json_write(json_filepath, data)

def reply_to_paragraph(reply):
    reply_formatted = ''
    lines = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if line.endswith(':'): continue
        lines.append(line)
    if len(lines) == 1:
        reply_formatted = lines[0]
    else:
        reply_formatted = ''
    return reply_formatted

def ai_paragraphs(json_filepath, data, key, prompt, regen=False):
    if key not in data: data[key] = []
    if regen: data[key] = []
    if data[key] == []:
        reply = llm_reply(prompt)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if ':' in line: continue
            lines.append(line)
        if len(lines) == 5:
            reply_formatted = lines
            print('*******************************************')
            print(reply_formatted)
            print('*******************************************')
            data[key] = reply_formatted
            util.json_write(json_filepath, data)

def ai_paragraphs_aka(json_filepath, data, key, aka, num, prompt, regen=False):
    if key not in data: data[key] = []
    if regen: data[key] = []
    if data[key] == []:
        reply = llm_reply(prompt)
        reply = reply.replace(aka, '')
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            if line.endswith(':'): continue
            lines.append(line)
        if len(lines) == num:
            reply_formatted = lines
            print('*******************************************')
            print(reply_formatted)
            print('*******************************************')
            data[key] = reply_formatted
            util.json_write(json_filepath, data)

def ai_list(json_filepath, data, key, prompt, regen=False):
    if key not in data: data[key] = []
    if regen: data[key] = []
    if data[key] == []:
        reply = llm_reply(prompt)
        lines = reply.split('\n')
        lines_filtered = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            if not line[0].isdigit(): continue
            if '.' not in line: continue
            if ':' not in line: continue
            line = '. '.join(line.split('. ')[1:])
            line = line.replace('*', '')
            line = line.strip()
            lines_filtered.append(line)
        if lines_filtered != []:
            print('\n\n********************************')
            print(lines_filtered)
            print('********************************\n\n')
            data[key] = lines_filtered
            json_write(json_filepath, data)

def reply_to_list(reply):
    reply_formatted = ''
    lines = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '.' not in line: continue
        if ':' not in line: continue
        line = '. '.join(line.split('. ')[1:])
        line = line.replace('*', '')
        line = line.strip()
        lines.append(line)
    return lines

def ai_list_column_eval(json_filepath, data, key, prompt, target_vals, items_num, regen=False):
    if key not in data: data[key] = []
    if regen: data[key] = []
    if data[key] == []:
        reply = llm_reply(prompt)
        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            line = line.replace('*', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            if not line[0].isdigit(): continue
            if '.' not in line: continue
            if ':' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            name = line.split(':')[0].strip()
            desc = line.split(':')[1].strip()
            if name.lower() not in target_vals.lower(): continue
            lines_formatted.append(line)
        lines_num = len(lines_formatted)
        if lines_num <= items_num and lines_num > items_num//2:
            print('***************************************')
            print(lines_formatted)
            print('***************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

# #########################################################
# ;images
# #########################################################
def image_preparation_intro(regen=False):
    if os.path.exists(images_folderpath_in):
        if not os.path.exists(image_filepath_out):
            random_image_filename = random.choice(os.listdir(images_folderpath_in))
            random_image_filepath = f'{images_folderpath_in}/{random_image_filename}'
            image_resize_save(random_image_filepath, image_filepath_out)
    html = f'<p><img src="{src}" alt="{alt}"></p>\n'

def gen_image_preparation(data, obj, img_src):
    img_src = img_src.replace('/', '-')
    img_alt = img_src.replace('-', ' ')
    preparation_slug = data['preparation_slug']
    herb_slug = obj['herb_slug']
    herb_name_scientific = obj['herb_name_scientific']
    images_folderpath_in = f'{vault_folderpath}/images/2x3/{preparation_slug}/{herb_slug}'
    images_folderpath_out = f'website/images/preparations'
    image_filepath_out = f'{images_folderpath_out}/{img_src}.jpg'
    image_filepath_web = f'/images/preparations/{img_src}.jpg'
    if os.path.exists(images_folderpath_in):
        if not os.path.exists(image_filepath_out):
        # if True:
            random_image_filename = random.choice(os.listdir(images_folderpath_in))
            img_w, img_h = 768, 768
            img = Image.open(f'{images_folderpath_in}/{random_image_filename}')
            img = util.img_resize(img, w=img_w, h=img_h)
            img.save(image_filepath_out, optimize=True, qulity=70)
    html = f'<p><img src="{image_filepath_web}" alt="{img_alt}"></p>\n'
    return html

def gen_image_preparation_old(data, img_src=''):
    images_folderpath_in = f'{vault_folderpath}/images/{preparation_slug}/{herb_slug}'
    if os.path.exists(images_folderpath_in):
        images_folderpath_out = f'website/images'
        image_slug = f'herbal-{preparation_slug}-for-{status_slug}-{herb_slug}'
        image_alt = f'herbal {preparation_name} for {status_name} {herb_name_scientific}'.lower()
        image_filepath_out = f'{images_folderpath_out}/{image_slug}.jpg'
        image_filepath_web = f'/images/{image_slug}.jpg'
        if not os.path.exists(image_filepath_out):
        # if True:
            random_image_filename = random.choice(os.listdir(images_folderpath_in))
            img_w, img_h = 768, 768
            text_color = '#ffffff'
            bg_color = '#000000'
            img = Image.open(f'{images_folderpath_in}/{random_image_filename}')
            img = util.img_resize(img, w=img_w, h=img_h)
            draw = ImageDraw.Draw(img)
            rect_h = 128
            draw.rectangle(((0, img_h - rect_h), (img_w, img_h)), fill=bg_color)
            text_size = 32
            text_off_y = text_size//8
            line_spacing = text_size * 0.3
            text = f'{herb_name_scientific} {preparation_name.title()} for'
            font = ImageFont.truetype('assets/fonts/Lato/Lato-Regular.ttf', text_size)
            _, _, text_w, text_h = font.getbbox(text)
            draw.text((img_w//2 - text_w//2, img_h - rect_h//2 - text_size - line_spacing//2 - text_off_y), text, text_color, font=font)
            text = f'{status_name.title()}'
            font = ImageFont.truetype('assets/fonts/Lato/Lato-Regular.ttf', text_size)
            _, _, text_w, text_h = font.getbbox(text)
            draw.text((img_w//2 - text_w//2, img_h - rect_h//2 + line_spacing//2 - text_off_y), text, text_color, font=font)
            img.save(image_filepath_out, optimize=True, qulity=70)
            # img.show()
            # quit()
        article_html += f'<p><img src="{image_filepath_web}" alt="{image_alt} herbs"></p>'

def gen_image_text(data):
    herb_slug = data['herb_slug']
    herb_name_scientific = ['herb_name_scientific']
    images_folderpath_in = f'{vault_folderpath}/images/2x3/herbs/{herb_slug}'
    images_folderpath_out = f'website/images'
    image_slug = f'{herb_slug}-medicine-benefits-overview'
    image_alt = f'{herb_name_scientific} medicine benefits overview'.lower()
    image_filepath_out = f'{images_folderpath_out}/{image_slug}.jpg'
    image_filepath_web = f'/images/{image_slug}.jpg'
    if os.path.exists(images_folderpath_in):
        if not os.path.exists(image_filepath_out):
        # if True:
            random_image_filename = random.choice(os.listdir(images_folderpath_in))
            img_w, img_h = 768, 768
            img = Image.open(f'{images_folderpath_in}/{random_image_filename}')
            img = util.img_resize(img, w=img_w, h=img_h)
            img.save(image_filepath_out, optimize=True, qulity=70)
    html = f'<p><img src="{image_filepath_web}" alt="{image_alt} herbs"></p>\n'
    return html

# #########################################################
# ;preparations
# #########################################################
def get_system_by_status(status_id):
    system_row = []
    status_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_STATUS_SYSTEMS_FILEPATH, status_systems_cols['status_id'], status_id,
    )
    if status_systems_rows_filtered != []:
        status_system_row = status_systems_rows_filtered[0]
        system_id = status_system_row[status_systems_cols['system_id']]
        systems_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id,
        )
        if systems_rows_filtered != []:
            system_row = systems_rows_filtered[0]
    return system_row

def main_preparations():
    art_preparations_new('teas')
    art_preparations_new('decoctions')
    art_preparations_new('tinctures')
    art_preparations_new('essential-oils')
    art_preparations_new('capsules')
    art_preparations_new('creams')

def art_preparations_new(preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')

    status_list = csv_read_rows_to_json(g.CSV_STATUS_FILEPATH)
    system_list = csv_read_rows_to_json(g.CSV_SYSTEMS_FILEPATH)
    status_system_list = csv_read_rows_to_json(g.CSV_STATUS_SYSTEMS_FILEPATH)
    preparation_list = csv_read_rows_to_json(g.CSV_PREPARATIONS_FILEPATH)
    status_preparation_list = csv_read_rows_to_json(g.CSV_STATUS_PREPARATIONS_FILEPATH)

    'uncoment to delete - recomment to regen'
    # tw_json.delete_preparations__remedy_recipe(preparation_slug)
    # tw_json.delete_preparations__supplementary_best_treatment(preparation_slug)
    # tw_json.delete_preparations__intro_study(preparation_slug)
    # return

    for status_index, status in enumerate(status_list[:]):
        print(f'\n>> {status_index}/{len(status_list)} - preparation: {preparation_name}')
        print(f'    >> {status}\n')

        status_exe = status['status_exe']
        status_id = status['status_id']
        status_slug = status['status_slug']
        status_name = status['status_names'].split(',')[0].strip()
        status_system = [obj for obj in status_system_list if obj['status_id'] == status_id][0]
        system = [obj for obj in system_list if obj['system_id'] == status_system['system_id']][0]
        system_id = system['system_id']
        system_slug = system['system_slug']
        system_name = system['system_name']
        status_preparations = [obj for obj in status_preparation_list if obj['status_id'] == status_id]
        status_preparations_names = [obj['preparation_name'] for obj in status_preparations]
        if preparation_slug.replace('-', ' ') not in status_preparations_names: continue

        ## init
        url = f'{g.CATEGORY_REMEDIES}/{system_slug}/{status_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'website/{url}.html'
        title = f'{PREPARATIONS_NUM} best herbal {preparation_name} for {status_name}'
        data = json_read(json_filepath, create=True)
        data['status_id'] = status_id
        data['status_slug'] = status_slug
        data['status_name'] = status_name
        data['system_id'] = system_id
        data['system_slug'] = system_slug
        data['system_name'] = system_name
        data['preparation_slug'] = preparation_slug
        data['preparation_name'] = preparation_name
        data['url'] = url
        if 'lastmod' not in data: data['lastmod'] = today()
        data['title'] = title
        data['remedies_num'] = PREPARATIONS_NUM

        ## init list TODO: clean, remove util_data
        key = 'remedies_list'
        if key not in data: data[key] = []
        herbs_rows_filtered = util_data.get_remedies_by_status(status_id, preparation_slug)
        for herb_row in herbs_rows_filtered:
            herb_id = herb_row[herbs_cols['herb_id']].strip()
            herb_slug = herb_row[herbs_cols['herb_slug']].strip()
            herb_name_common = herb_row[2].strip()
            herb_name_scientific = herb_slug.replace('-', ' ').capitalize()
            if herb_id == '': continue
            if herb_slug == '': continue
            if herb_name_scientific == '': continue
            found = False
            for obj in data[key]:
                if obj['herb_id'] == herb_id: 
                    found = True
                    break
            if not found:
                data[key].append({
                    'herb_id': herb_id,
                    'herb_slug': herb_slug,
                    'herb_name_common': herb_name_common,
                    'herb_name_scientific': herb_name_scientific,
                })
        json_write(json_filepath, data)
        
        ## article
        article_html = ''
        article_html += f'<h1 class="article-h1">{title.title()}</h1>\n'

        ## featured image
        remedy_slug = data['remedies_list'][0]['herb_slug']
        src = f'/images/preparations/herbal-{preparation_slug}-for-{status_slug}-overview.jpg'
        alt = f'herbal {preparation_slug} for {status_slug} overview'
        filepath_out = f'website/images/preparations/herbal-{preparation_slug}-for-{status_slug}-overview.jpg'
        filepath_in = f'{vault_folderpath}/terrawhisper/images/watercolor/{preparation_slug}/1x1/{remedy_slug}.jpg'
        # if not os.path.exists(filepath_out):
        if True:
            if os.path.exists(filepath_in):
                image = Image.open(filepath_in)
                image = img_resize(image)
                draw = ImageDraw.Draw(image)
                font_size = 36
                font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
                font = ImageFont.truetype(font_path, font_size)
                rect_h = 120

                text = f'Herbal {preparation_name.title()} For'.upper()
                _, _, text_w, text_h = font.getbbox(text)
                draw.rectangle(((0, 768 - rect_h), (768, 768)), '#000000')
                draw.text((768//2 - text_w//2, 768-font_size*2*1.2-10), text, '#ffffff', font=font)

                text = status_name.title().upper()
                _, _, text_w, text_h = font.getbbox(text)
                draw.text((768//2 - text_w//2, 768-font_size*1.2-10), text, '#ffffff', font=font)
                image.save(filepath_out)
        if os.path.exists(filepath_out):
            article_html += f'<p><img src="{src}" alt="{alt}"></p>\n'
        
        ## intro
        key = 'intro_desc'
        prompt = prompts.preparation__intro(preparation_name, status_name)
        ai_paragraph(json_filepath, data, key, prompt)
        if key in data:
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        ## intro_study
        if 0:
            key = 'intro_study'
            if key not in data or data[key] == []:
                sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name='all-mpnet-base-v2', 
                    device='cuda',
                )
                chroma_client = chromadb.PersistentClient(path=f'{vault_folderpath}/terrawhisper/chroma-db')
                collection = chroma_client.get_or_create_collection(name='medicinal-plants', embedding_function=sentence_transformer_ef)
                query = f'herbal {preparation_name} for {status_name}'
                prompt = f'''
                    Write an example abstract for a scientific study about {query}.
                    Include an introduction, the methods, the results, the discussions, and the conclusion.
                    Pack as many info, data points, numbers, and statistics in as few words as possible.
                    Reply in a paragraph.
                    Don't include lists.
                '''
                reply = llm_reply(prompt)
                n_results = 5
                results = collection.query(query_texts=[query], n_results=n_results)
                documents = results['documents'][0]
                metadatas = results['metadatas'][0]
                if len(documents) == n_results and len(metadatas) == n_results:
                    abstracts = []
                    for i, document in enumerate(documents):
                        document_formatted = f'PARAGRAPH {i+1}: {document}'
                        abstracts.append(document_formatted)
                    prompt = f'''
                        From the {n_results} paragraphs below, pick the one that best proves that herbal {preparation_name} are good for {status_name}, and that includes the most amount of data, information, details, results and numbers to prove it.
                        Only select a study that explicitly mention {preparation_name} and {status_name}.
                        Reply with only the number of the paragraph you select, don't explain why you selected it.
                        If you don't find a good candidate, reply with "0".
                        Below are the {n_results} paragraphs.
                        {abstracts}
                    '''
                    reply = llm_reply(prompt)
                    paragraph_num = 0
                    for line in reply.split('\n'):
                        line = line.strip()
                        if line == '': continue
                        if line[0].isdigit():
                            if line[0] == 0:
                                break
                            else:
                                try: paragraph_num = int(line.split(' ')[0])
                                except: pass
                                break
                    if paragraph_num != 0:
                        document = documents[paragraph_num-1]
                        metadata = metadatas[paragraph_num-1]
                        prompt = prompts.preparation__intro_study__generate(preparation_name, status_name, document, metadata['journal_title'])
                        reply = llm_reply(prompt)
                        reply = reply_to_paragraph(reply)
                        if reply != '':
                            if 'can\'t do that' not in reply: 
                                data[key] = reply
                                json_write(json_filepath, data)
            if key in data:
                article_html += f'<p>{data[key]}</p>\n'

        article_html += f'<p>The following article describes in detail the most important {preparation_name} for {status_name}, including medicinal properties, parts of herbs to use, and recipes for preparations.</p>\n'

        ## remedies
        for i, obj in enumerate(data['remedies_list'][:PREPARATIONS_NUM]):
            print(f'\n>> {status_index}/{len(status_list)} - preparation: {preparation_name}')
            print(f'    >> {status}\n')
            herb_name_common = obj['herb_name_common']
            herb_name_scientific = obj['herb_name_scientific']
            herb_slug = obj['herb_slug']
            aka = f', also known as {herb_name_common},'

            ## desc
            key = 'remedy_desc'
            # if key in obj: del obj[key]
            if key not in obj or obj[key] == []:
                prompt = prompts.preparation__remedy_desc(preparation_name, status_name, herb_name_scientific, aka)
                reply = llm_reply(prompt)
                reply = reply_to_paragraph(reply)
                if reply != '':
                    obj[key] = reply
                    json_write(json_filepath, data)
            if key in obj:
                article_html += f'<h2>{i+1}. {herb_name_scientific.capitalize()}</h2>\n'
                article_html += f'{util.text_format_1N1_html(obj[key])}\n'

            ## image
            preparation_name_singular = preparation_name
            if preparation_name_singular[-1] == 's': preparation_name_singular = preparation_name_singular[:-1]
            remedy_slug = herb_slug
            src = f'/images/preparations/{herb_slug}-herbal-{preparation_slug}.jpg'
            alt = f'{herb_name_scientific} herbal {preparation_slug} for {status_slug}'.lower()
            filepath_out = f'website/images/preparations/{herb_slug}-herbal-{preparation_slug}.jpg'
            filepath_in = f'{vault_folderpath}/terrawhisper/images/watercolor/{preparation_slug}/1x1/{remedy_slug}.jpg'
            # if not os.path.exists(filepath_out):
            if True:
                if os.path.exists(filepath_in):
                    image = Image.open(filepath_in)
                    image = img_resize(image)
                    draw = ImageDraw.Draw(image)
                    font_size = 36
                    font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                    rect_h = 120

                    text = f'{herb_name_scientific}'.upper()
                    _, _, text_w, text_h = font.getbbox(text)
                    draw.rectangle(((0, 768 - rect_h), (768, 768)), '#000000')
                    draw.text((768//2 - text_w//2, 768-font_size*2*1.2-10), text, '#ffffff', font=font)

                    text = f'Herbal {preparation_name_singular}'.upper()
                    _, _, text_w, text_h = font.getbbox(text)
                    draw.text((768//2 - text_w//2, 768-font_size*1.2-10), text, '#ffffff', font=font)
                    image.save(filepath_out)
            if os.path.exists(filepath_out):
                article_html += f'<p><img src="{src}" alt="{alt}"></p>\n'

            ## properties
            key = 'remedy_constituents'
            if key not in obj or obj[key] == []:
                prompt = prompts.preparation__remedy_constituents(preparation_name, status_name, herb_name_scientific)
                reply = llm_reply(prompt)
                reply = reply_to_list(reply)
                if reply != []:
                    obj[key] = reply
                    json_write(json_filepath, data)
            if key in obj:
                items = obj[key]
                article_html += f'<p class="text-24 text-black font-bold">Medicinal Constituents</p>\n'
                article_html += f'<p>The list below shows the primary medicinal constituents in {herb_name_scientific} {preparation_name} that help with {status_name}.</p>\n'
                article_html += '<ul>\n'
                for item in items:
                    chunk_1 = item.split(': ')[0].split('(')[0].strip()
                    chunk_2 = ': '.join(item.split(': ')[1:])
                    article_html += f'<li><strong>{chunk_1.capitalize()}</strong>: {chunk_2}</li>\n'
                article_html += '</ul>\n'

            ## parts
            key = 'remedy_parts'
            if key not in obj or obj[key] == []:
                prompt = prompts.preparation__remedy_parts(preparation_name, status_name, herb_name_scientific)
                reply = llm_reply(prompt)
                lines = []
                for line in reply.split('\n'):
                    line = line.strip()
                    if line == '': continue
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    if ':' not in line: continue
                    line = '. '.join(line.split('. ')[1:])
                    line = line.replace('*', '')
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    line_name = line.split(':')[0].strip().lower()
                    parts = ['roots', 'rhyzomes', 'stems', 'leaves', 'flowers', 'seeds', 'buds', 'barks', 'fruits']
                    found = False
                    for part in parts:
                        if part in line_name:
                            found = True
                            break
                    if not found: continue
                    line = line.strip()
                    lines.append(line)
                if lines != []:
                    obj[key] = lines
                    json_write(json_filepath, data)
            if key in obj:
                items = obj[key]
                article_html += f'<p class="text-24 text-black font-bold">Parts Used</p>\n'
                article_html += f'<p>The list below shows the primary parts of {herb_name_common} used to make {preparation_name} for {status_name}.</p>\n'
                article_html += '<ul>\n'
                for item in items:
                    chunk_1 = item.split(': ')[0]
                    chunk_2 = ': '.join(item.split(': ')[1:])
                    article_html += f'<li><strong>{chunk_1.capitalize()}</strong>: {chunk_2}</li>\n'
                article_html += '</ul>\n'

            ## recipe
            key = 'remedy_recipe'
            if key not in obj or obj[key] == []:
                prompt = prompts.preparation__remedy_recipe(preparation_name, herb_name_scientific)
                reply = llm_reply(prompt)
                lines = reply.split('\n')
                lines_filtered = []
                valid_output = True
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    if 'cannot' in line: 
                        valid_output = False
                        break
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    line = '. '.join(line.split('. ')[1:])
                    line = line.replace('*', '')
                    line = line.strip()
                    if line == '': continue
                    if len(line.split(' ')) < 7: continue
                    if not line.endswith('.'): line += '.'
                    line = line.capitalize()
                    lines_filtered.append(line)
                if len(lines_filtered) == 5 and valid_output:
                    print('********************************')
                    print(lines_filtered)
                    print('********************************')
                    obj[key] = lines_filtered
                    json_write(json_filepath, data)
            if key in obj:
                recipe = obj[key]
                article_html += f'<p class="text-24 text-black font-bold">Quick Recipe</p>\n'
                article_html += f'<p>The following recipe gives a procedure to make a basic {herb_name_common} for {status_name}.</p>\n'
                article_html += '<ol>\n'
                for step in recipe:
                    article_html += f'<li>{step}</li>\n'
                article_html += '</ol>\n'

        key = 'supplementary_best_treatment'
        if key not in data or data[key] == '':
            prompt = prompts.preparation__supplementary_best_treatment(status_name, preparation_name)
            reply = llm_reply(prompt)
            reply = reply_to_paragraph(reply)
            if reply != '':
                data[key] = reply
                json_write(json_filepath, data)
        if key in data:
            article_html += f'<h2>What is the best combination of herbal {preparation_name} to use for {status_name}?</h2>\n'
            text = data[key].replace(status_name, f'<a href="/{g.CATEGORY_REMEDIES}/{system_slug}/{status_slug}.html">{status_name}</a>', 1)
            article_html += f'{util.text_format_1N1_html(text)}\n'

        key = 'supplementary_causes'
        if key not in data or data[key] == '':
            prompt = f'''
                What ailments similar to {status_name} are treated with herbal {preparation_name}?
                Reply in a short paragraph of about 60 to 80 words.
                Start the reply with the following words: Ailments similar to {status_name} that are treated with herbal {preparation_name} are .
            '''
            reply = llm_reply(prompt)
            reply = reply_to_paragraph(reply)
            if reply != '':
                data[key] = reply
                json_write(json_filepath, data)
        if key in data and data[key] != '':
            text = data[key]
            article_html += f'<h2>What ailments similar to {status_name} are treated with herbal {preparation_name}?</h2>\n'
            i = 0
            for tmp_status in status_list:
                tmp_status_exe = status['status_exe']
                tmp_status_id = status['status_id']
                tmp_status_slug = status['status_slug']
                tmp_status_name = status['status_names'].split(',')[0].strip()
                tmp_status_system = [obj for obj in status_system_list if obj['status_id'] == tmp_status_id][0]
                tmp_system = [obj for obj in system_list if obj['system_id'] == tmp_status_system['system_id']][0]

                tmp_system_id = tmp_system['system_id']
                tmp_system_slug = tmp_system['system_slug']
                tmp_system_name = tmp_system['system_name']
                html_filepath = f'website/{g.CATEGORY_REMEDIES}/{tmp_system_slug}/{tmp_status_slug}/{preparation_slug}.html'
                if os.path.exists(html_filepath):
                    if i >= 3: break
                    if tmp_status_name in text:
                        text = text.replace(tmp_status_name, f'<a href="/{g.CATEGORY_REMEDIES}/{tmp_system_slug}/{tmp_status_slug}/{preparation_slug}.html">{tmp_status_name}</a>', 1)
                        i += 1
            article_html += f'{util.text_format_1N1_html(text)}\n'

        ## html
        breadcrumbs = util.breadcrumbs(html_filepath)
        meta = components.meta(article_html, data["lastmod"])
        article = components.table_of_contents(article_html)
        html = templates.article(title, header_html, breadcrumbs, meta, article, footer_html)
        file_write(html_filepath, html)

def gen_preparation__supplementary(json_filepath, data, article_html):
    return article_html

def del_preparations__remedy_parts(preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ').strip()
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        if DEBUG_STATUS: print(f'> {status_name}')
        system_row = util_data.get_system_by_status(status_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue
        if DEBUG_STATUS: print(f'  > {system_name}')
        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{status_slug}/{preparation_slug}.json'
        if DEBUG_STATUS_JSON_FILEPATH: print(json_filepath)
        if not os.path.exists(json_filepath):
            continue
        data = json_read(json_filepath)
        for remedy_obj in data['remedies_list']:
            if 'remedy_parts' in remedy_obj:
                del remedy_obj['remedy_parts']
        util.json_write(json_filepath, data)

def del_preparations__remedies_recipes(preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ').strip()
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        if DEBUG_STATUS: print(f'> {status_name}')
        system_row = util_data.get_system_by_status(status_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue
        if DEBUG_STATUS: print(f'  > {system_name}')
        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{status_slug}/{preparation_slug}.json'
        if DEBUG_STATUS_JSON_FILEPATH: print(json_filepath)
        if not os.path.exists(json_filepath):
            continue
        data = json_read(json_filepath)
        for remedy_obj in data['remedies_list']:
            if 'remedy_recipe' in remedy_obj:
                del remedy_obj['remedy_recipe']
        util.json_write(json_filepath, data)



# #########################################################
# ;herbs
# #########################################################

def main_herbs():
    herbs = csv_read_rows_to_json(g.CSV_HERBS_FILEPATH)
    for i, herb in enumerate(herbs):
        print()
        print('***********************')
        print('***********************')
        print(f'{i}/{len(herbs)} - {herb}')
        print('***********************')
        print('***********************')
        print()
        art_herb(herb)
        art_herb_medicine(herb)
        art_herb_medicine_benefits(herb)
        art_herb_medicine_constituents(herb)
        art_herb_medicine_preparations(herb)
        art_herb_medicine_side_effects(herb)
        art_herb_medicine_precautions(herb)
    art_herb_category()
    
def art_herb(herb):
    herb_id = herb['herb_id']
    herb_slug = herb['herb_slug']
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_common = util_data.get_herb_common_name_by_id(herb_id)
    url = f'herbs/{herb_slug}'
    json_filepath = f'database/json/{url}.json'
    html_filepath = f'website/{url}.html'
    title = f'What to know about {herb_name_scientific} ({herb_name_common}) before using it medicinally'
    aka = f', also known as {herb_name_common},'
    data = json_read(json_filepath, create=True)
    data['herb_id'] = herb_id
    data['herb_slug'] = herb_slug
    data['herb_name_scientific'] = herb_name_scientific
    data['herb_name_common'] = herb_name_common
    data['url'] = url
    if 'lastmod' not in data: data['lastmod'] = today()
    data['title'] = title
    json_write(json_filepath, data)
    article_html = ''
    article_html += f'<h1>{title}</h1>\n'
    article_html += tw_img_gen_web_herb_rnd(herb)
    key = 'intro_desc'
    prompt = prompts.herb__intro(herb_name_scientific, herb_name_common)
    ai_paragraph(json_filepath, data, key, prompt)
    if data[key] != '':
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
        article_html += f'<p>This article explains the medicinal, horticultural, botanical, and historical aspects of {herb_name_scientific}.</p>\n'
    key = 'medicine_desc'
    prompt = prompts.herb__medicine(herb_name_scientific, herb_name_common, aka)
    ai_paragraphs_aka(json_filepath, data, key, aka, 5, prompt)
    if data[key] != []:
        article_html += f'<h2>What are the medicinal properties of {herb_name_scientific}?</h2>\n'
        for item in data[key]:
            article_html += f'<p>{item}</p>\n'
    key = 'horticulture_desc'
    prompt = prompts.herb__horticulture(herb_name_scientific, herb_name_common, aka)
    ai_paragraphs_aka(json_filepath, data, key, aka, 4, prompt)
    if data[key] != []:
        article_html += f'<h2>What are the horticulural aspects of {herb_name_scientific}?</h2>\n'
        for item in data[key]:
            article_html += f'<p>{item}</p>\n'
    key = 'botany_desc'
    prompt = prompts.herb__botany(herb_name_scientific, herb_name_common, aka)
    ai_paragraphs_aka(json_filepath, data, key, aka, 5, prompt)
    if data[key] != []:
        article_html += f'<h2>What are the botanical aspects of {herb_name_scientific}?</h2>\n'
        for item in data[key]:
            article_html += f'<p>{item}</p>\n'
    key = 'history_desc'
    prompt = prompts.herb__history(herb_name_scientific, herb_name_common, aka)
    ai_paragraphs_aka(json_filepath, data, key, aka, 5, prompt)
    if data[key] != []:
        article_html += f'<h2>What are the historical aspects of {herb_name_scientific}?</h2>\n'
        for item in data[key]:
            article_html += f'<p>{item}</p>\n'
    breadcrumbs = util.breadcrumbs(html_filepath)
    meta = components.meta(article_html, data["lastmod"])
    article = components.table_of_contents(article_html)
    html = templates.article(title, header_html, breadcrumbs, meta, article, footer_html)
    file_write(html_filepath, html)
    redirect(html_filepath, source='/plants/', target='/herbs/')

def art_herb_medicine(herb):
    herb_id = herb['herb_id']
    herb_slug = herb['herb_slug']
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_common = util_data.get_herb_common_name_by_id(herb_id)
    url = f'herbs/{herb_slug}/medicine'
    json_filepath = f'database/json/{url}.json'
    html_filepath = f'website/{url}.html'
    title = f'What Are The Medicinal Properties of {herb_name_scientific} ({herb_name_common})?'
    aka = f', also known as {herb_name_common},'
    data = json_read(json_filepath, create=True)
    data['herb_id'] = herb_id
    data['herb_slug'] = herb_slug
    data['herb_name_common'] = herb_name_common
    data['herb_name_scientific'] = herb_name_scientific
    data['url'] = url
    if 'lastmod' not in data: data['lastmod'] = today()
    data['title'] = title
    util.json_write(json_filepath, data)
    article_html = ''
    article_html += f'<h1>{title.title()}</h1>\n'
    article_html += tw_img_gen_web_herb_rnd(herb)
    # intro
    key = 'intro_desc'
    prompt = prompts.herb_medicine__intro(herb_name_scientific, herb_name_common, aka)
    ai_paragraph(json_filepath, data, key, prompt)
    if key in data:
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
        article_html += f'<p>This article explains the health benefits, active constituents, medicinal preparations, possible side effects, and precautions related to {herb_name_scientific}.</p>\n'
    # benefits
    key = 'benefits'
    prompt = prompts.herb_medicine__benefits(herb_name_scientific, herb_name_common, aka)
    ai_paragraph(json_filepath, data, key, prompt)
    if key in data:
        article_html += f'<h2>What are the health benefits of {herb_name_scientific}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
        if os.path.exists(f'website/herbs/{herb_slug}/medicine/benefits.html'):
            article_html += f'<p>Here\'s a detailed article about the <a href="/herbs/{herb_slug}/medicine/benefits.html">10 health benefits of {herb_name_scientific}</a>.</p>\n'
    # constituents
    key = 'constituents'
    prompt = prompts.herb_medicine__constituents(herb_name_scientific, herb_name_common, aka)
    ai_paragraph(json_filepath, data, key, prompt)
    if key in data:
        article_html += f'<h2>What are the active constituents of {herb_name_scientific}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
        if os.path.exists(f'website/herbs/{herb_slug}/medicine/constituents.html'):
            article_html += f'<p>Here\'s a detailed article about the <a href="/herbs/{herb_slug}/medicine/constituents.html">10 active constituents of {herb_name_scientific}</a>.</p>\n'
    # preparations
    key = 'preparations'
    prompt = prompts.herb_medicine__preparations(herb_name_scientific, herb_name_common, aka)
    ai_paragraph(json_filepath, data, key, prompt)
    if key in data:
        article_html += f'<h2>What are the medicinal preparations of {herb_name_scientific}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
        if os.path.exists(f'website/herbs/{herb_slug}/medicine/preparations.html'):
            article_html += f'<p>Here\'s a detailed article about the <a href="/herbs/{herb_slug}/medicine/preparations.html">10 medicinal preparations of {herb_name_scientific}</a>.</p>\n'
    # side effects
    key = 'side_effects'
    prompt = prompts.herb_medicine__side_effects(herb_name_scientific, herb_name_common, aka)
    ai_paragraph(json_filepath, data, key, prompt)
    if key in data:
        article_html += f'<h2>What are the possible side effect of using {herb_name_scientific} improperly?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
        if os.path.exists(f'website/herbs/{herb_slug}/medicine/side-effects.html'):
            article_html += f'<p>Here\'s a detailed article about the <a href="/herbs/{herb_slug}/medicine/side-effects.html">10 most common side effects of {herb_name_scientific}</a>.</p>\n'
    # precautions
    key = 'precautions'
    prompt = prompts.herb_medicine__precautions(herb_name_scientific, herb_name_common, aka)
    ai_paragraph(json_filepath, data, key, prompt)
    if key in data:
        article_html += f'<h2>What precautions to take when using {herb_name_scientific} medicinally?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
        if os.path.exists(f'website/herbs/{herb_slug}/medicine/precautions.html'):
            article_html += f'<p>Here\'s a detailed article about <a href="/herbs/{herb_slug}/medicine/precautions.html">10 precautions to take when using {herb_name_scientific}</a>.</p>\n'
    breadcrumbs = util.breadcrumbs(html_filepath)
    meta = components.meta(article_html, data['lastmod'])
    article = components.table_of_contents(article_html)
    html = templates.article(title, header_html, breadcrumbs, meta, article, footer_html)
    file_write(html_filepath, html)
    redirect(html_filepath, source='/plants/', target='/herbs/')

def art_herb_medicine_benefits(herb):
    herb_id = herb['herb_id']
    herb_slug = herb['herb_slug']
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_common = util_data.get_herb_common_name_by_id(herb_id)
    url = f'herbs/{herb_slug}/medicine/benefits'
    json_filepath = f'database/json/{url}.json'
    html_filepath = f'website/{url}.html'
    title = f'10 health benefits of {herb_name_scientific} ({herb_name_common})'
    aka = f', also known as {herb_name_common},'
    data = json_read(json_filepath, create=True)
    data['herb_id'] = herb_id
    data['herb_slug'] = herb_slug
    data['herb_name_common'] = herb_name_common
    data['herb_name_scientific'] = herb_name_scientific
    data['url'] = url
    if 'lastmod' not in data: data['lastmod'] = today()
    data['title'] = title
    util.json_write(json_filepath, data)
    article_html = ''
    article_html += f'<h1>{title.title()}</h1>\n'
    article_html += tw_img_gen_web_herb_rnd(herb)
    key = 'intro_desc'
    ai_paragraph(json_filepath, data, key, 
        prompts.herb_medicine_benefits__intro(herb_name_scientific, herb_name_common, aka), 
    )
    if key in data:
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
    article_html += f'<p>This article explains in details the 10 best health benefits of {herb_name_scientific}.</p>\n'
    key = 'benefits_list'
    if key not in data: data[key] = []
    herbs_benefits_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_HERBS_BENEFITS_FILEPATH, herbs_benefits_cols['herb_id'], herb_id
    )
    for herb_benefit_row in herbs_benefits_rows_filtered:
        print(herb_benefit_row)
        benefit_name = herb_benefit_row[herbs_benefits_cols['benefit_name']]
        found = False
        for obj in data[key]:
            if obj['benefit_name'] == benefit_name: 
                found = True
                break
        if not found:
            data[key].append({
                'herb_id': herb_id,
                'herb_slug': herb_slug,
                'herb_name_common': herb_name_common,
                'herb_name_scientific': herb_name_scientific,
                'benefit_name': benefit_name,
            })
    util.json_write(json_filepath, data)
    for i, obj in enumerate(data['benefits_list'][:10]):
        benefit_name = obj['benefit_name']
        benefit_slug = benefit_name.strip().lower().replace(' ', '-')
        key = 'benefit_desc'
        prompt = prompts.herb_medicine_benefits__benefit_desc(
            herb_name_scientific, herb_name_common, benefit_name, aka
        )
        ai_paragraph_aka(json_filepath, obj, key, aka, prompt)
        if key in obj:
            article_html += f'<h2>{i+1}. {benefit_name.capitalize()}</h2>\n'
            article_html += f'<p>{util.text_format_1N1_html(obj[key])}</p>\n'
    breadcrumbs = util.breadcrumbs(html_filepath)
    meta = components.meta(article_html, data['lastmod'])
    article = components.table_of_contents(article_html)
    html = templates.article(title, header_html, breadcrumbs, meta, article, footer_html)
    file_write(html_filepath, html)
    redirect(html_filepath, source='/plants/', target='/herbs/')

def art_herb_medicine_constituents(herb):
    herb_id = herb['herb_id']
    herb_slug = herb['herb_slug']
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_common = util_data.get_herb_common_name_by_id(herb_id)
    url = f'herbs/{herb_slug}/medicine/constituents'
    json_filepath = f'database/json/{url}.json'
    html_filepath = f'website/{url}.html'
    title = f'10 medicinal constituents of {herb_name_scientific} ({herb_name_common})'
    aka = f', also known as {herb_name_common},'
    data = json_read(json_filepath, create=True)
    data['herb_id'] = herb_id
    data['herb_slug'] = herb_slug
    data['herb_name_common'] = herb_name_common
    data['herb_name_scientific'] = herb_name_scientific
    data['url'] = url
    if 'lastmod' not in data: data['lastmod'] = today()
    data['title'] = title
    util.json_write(json_filepath, data)
    article_html = ''
    article_html += f'<h1>{title.title()}</h1>\n'
    article_html += tw_img_gen_web_herb_rnd(herb)
    key = 'intro_desc'
    ai_paragraph(json_filepath, data, key, 
        prompts.herb_medicine_constituents__intro(herb_name_scientific, herb_name_common, aka), 
    )
    if key in data:
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
    article_html += f'<p>This article explains in details the 10 best active constituents of {herb_name_scientific}.</p>\n'
    key = 'constituents_list'
    if key not in data: data[key] = []
    herbs_constituents_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_HERBS_CONSTITUENTS_FILEPATH, herbs_constituents_cols['herb_id'], herb_id
    )
    for herb_constituent_row in herbs_constituents_rows_filtered:
        print(herb_constituent_row)
        constituent_name = herb_constituent_row[herbs_constituents_cols['constituent_name']]
        found = False
        for obj in data[key]:
            if obj['constituent_name'] == constituent_name: 
                found = True
                break
        if not found:
            data[key].append({
                'herb_id': herb_id,
                'herb_slug': herb_slug,
                'herb_name_common': herb_name_common,
                'herb_name_scientific': herb_name_scientific,
                'constituent_name': constituent_name,
            })
    util.json_write(json_filepath, data)
    for i, obj in enumerate(data[key][:10]):
        constituent_name = obj["constituent_name"].strip()
        constituent_slug = constituent_name.strip().lower().replace(' ', '-')
        key = 'constituent_desc'
        if key not in obj:
            aka = f', also known as {herb_name_common},'
            prompt = f'''
                Write 1 paragraph of 60 to 80 words on what is {herb_name_scientific} {constituent_name}.
                Start the reply with the following words: {herb_name_scientific}{aka} {constituent_name} is .
            '''
            reply = llm_reply(prompt)
            reply = reply.replace(aka, '')
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                reply = lines[0]
                print('********************************')
                print(reply)
                print('********************************')
                obj[key] = reply
                util.json_write(json_filepath, data)
        if key in obj:
            article_html += f'<h2>{i+1}. {constituent_name.capitalize()}</h2>\n'
            article_html += f'<p>{util.text_format_1N1_html(obj[key])}</p>\n'
    breadcrumbs = util.breadcrumbs(html_filepath)
    meta = components.meta(article_html, data['lastmod'])
    article = components.table_of_contents(article_html)
    html = templates.article(title, header_html, breadcrumbs, meta, article, footer_html)
    file_write(html_filepath, html)
    redirect(html_filepath, source='/plants/', target='/herbs/')

def art_herb_medicine_preparations(herb):
    herb_id = herb['herb_id']
    herb_slug = herb['herb_slug']
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_common = util_data.get_herb_common_name_by_id(herb_id)
    url = f'herbs/{herb_slug}/medicine/preparations'
    json_filepath = f'database/json/{url}.json'
    html_filepath = f'website/{url}.html'
    title = f'10 medicinal preparations of {herb_name_scientific} ({herb_name_common})'
    aka = f', also known as {herb_name_common},'
    data = json_read(json_filepath, create=True)
    data['herb_id'] = herb_id
    data['herb_slug'] = herb_slug
    data['herb_name_common'] = herb_name_common
    data['herb_name_scientific'] = herb_name_scientific
    data['url'] = url
    if 'lastmod' not in data: data['lastmod'] = today()
    data['title'] = title
    util.json_write(json_filepath, data)
    article_html = ''
    article_html += f'<h1>{title.title()}</h1>\n'
    article_html += tw_img_gen_web_herb_rnd(herb)
    key = 'intro_desc'
    ai_paragraph_aka(json_filepath, data, key, aka, 
        prompts.herb_medicine_preparations__intro(herb_name_scientific, herb_name_common, aka)
    )
    if key in data:
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
    article_html += f'<p>This article explains in details the 10 best medicinal preparations of {herb_name_scientific}.</p>\n'
    key = 'preparations_list'
    # if key in data: data[key] = []
    if key not in data: data[key] = []
    herbs_preparations_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_HERBS_PREPARATIONS_FILEPATH, herbs_preparations_cols['herb_id'], herb_id
    )
    for herb_preparation_row in herbs_preparations_rows_filtered:
        preparation_name = herb_preparation_row[herbs_preparations_cols['preparation_name']]
        found = False
        for obj in data[key]:
            if obj['preparation_name'] == preparation_name: 
                found = True
                break
        if not found:
            data[key].append({
                'herb_id': herb_id,
                'herb_slug': herb_slug,
                'herb_name_common': herb_name_common,
                'herb_name_scientific': herb_name_scientific,
                'preparation_name': preparation_name,
            })
    util.json_write(json_filepath, data)
    for i, obj in enumerate(data[key][:10]):
        preparation_name = obj["preparation_name"].strip()
        preparation_slug = preparation_name.lower().strip().replace(' ', '-')
        key = 'preparation_desc'
        if key not in obj:
            aka = f', also known as {herb_name_common},'
            prompt = f'''
                Write 1 paragraph of 60 to 80 words on what are the uses of {herb_name_scientific} {preparation_name} for health purposes.
                Start the reply with the following words: {herb_name_scientific}{aka} {preparation_name} is used to .
            '''
            reply = llm_reply(prompt)
            reply = reply.replace(aka, '')
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                reply = lines[0]
                print('********************************')
                print(reply)
                print('********************************')
                obj[key] = reply
                util.json_write(json_filepath, data)
        if key in obj:
            article_html += f'<h2>{i+1}. {preparation_name.capitalize()}</h2>\n'
            article_html += f'<p>{util.text_format_1N1_html(obj[key])}</p>\n'
    breadcrumbs = util.breadcrumbs(html_filepath)
    meta = components.meta(article_html, data['lastmod'])
    article = components.table_of_contents(article_html)
    html = templates.article(title, header_html, breadcrumbs, meta, article, footer_html)
    file_write(html_filepath, html)
    redirect(html_filepath, source='/plants/', target='/herbs/')

def art_herb_medicine_side_effects(herb):
    herb_id = herb['herb_id']
    herb_slug = herb['herb_slug']
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_common = util_data.get_herb_common_name_by_id(herb_id)
    url = f'herbs/{herb_slug}/medicine/side-effects'
    json_filepath = f'database/json/{url}.json'
    html_filepath = f'website/{url}.html'
    title = f'10 possible side effects of {herb_name_scientific} ({herb_name_common})'
    aka = f', also known as {herb_name_common},'
    data = json_read(json_filepath, create=True)
    data['herb_id'] = herb_id
    data['herb_slug'] = herb_slug
    data['herb_name_common'] = herb_name_common
    data['herb_name_scientific'] = herb_name_scientific
    data['url'] = url
    if 'lastmod' not in data: data['lastmod'] = today()
    data['title'] = title
    util.json_write(json_filepath, data)
    article_html = ''
    article_html += f'<h1>{title.title()}</h1>\n'
    article_html += tw_img_gen_web_herb_rnd(herb)
    key = 'intro_desc'
    ai_paragraph_aka(json_filepath, data, key, aka, 
        prompts.herb_medicine_side_effects__intro(herb_name_scientific, herb_name_common, aka)
    )
    if key in data:
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
    article_html += f'<p>This article explains in details the 10 most common side effects of {herb_name_scientific} if used imporperly.</p>\n'
    key = 'side_effects_list'
    if key not in data: data[key] = []
    herbs_side_effects_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_HERBS_SIDE_EFFECTS_FILEPATH, herbs_side_effects_cols['herb_id'], herb_id
    )
    for herb_side_effect_row in herbs_side_effects_rows_filtered:
        print(herb_side_effect_row)
        side_effect_name = herb_side_effect_row[herbs_side_effects_cols['side_effect_name']]
        found = False
        for obj in data[key]:
            if obj['side_effect_name'] == side_effect_name: 
                found = True
                break
        if not found:
            data[key].append({
                'herb_id': herb_id,
                'herb_slug': herb_slug,
                'herb_name_common': herb_name_common,
                'herb_name_scientific': herb_name_scientific,
                'side_effect_name': side_effect_name,
            })
    util.json_write(json_filepath, data)
    for i, obj in enumerate(data[key][:10]):
        obj_herb_name_common = obj["herb_name_common"].strip()
        obj_herb_name_scientific = obj["herb_name_scientific"].strip()
        obj_side_effect_name = obj["side_effect_name"].strip()
        side_effect_slug = side_effect_name.lower().strip().replace(' ', '-')
        key = 'side_effect_desc'
        if key not in obj:
            prompt = f'''
                write 1 paragraph of 60 to 80 words about the following SIDE EFFECT people may experience when using {herb_name_scientific}.
                also, follow the GUIDELINES below.
                SIDE EFFECT
                {side_effect_name}
                GUIDELINES
                include the reasons why {herb_name_scientific} gives this side effect.        
                don't mention consulting and healthcare provider or similar.
                don't include solutions or precautions.
                start the reply with the following words: {herb_name_scientific}{aka} {side_effect_name} .
            '''
            reply = llm_reply(prompt)
            reply = reply.replace(aka, '')
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                reply = lines[0]
                print('********************************')
                print(reply)
                print('********************************')
                obj[key] = reply
                util.json_write(json_filepath, data)
        if key in obj:
            article_html += f'<h2>{i+1}. {side_effect_name.capitalize()}</h2>\n'
            article_html += f'<p>{util.text_format_1N1_html(obj[key])}</p>\n'
    breadcrumbs = util.breadcrumbs(html_filepath)
    meta = components.meta(article_html, data['lastmod'])
    article = components.table_of_contents(article_html)
    html = templates.article(title, header_html, breadcrumbs, meta, article, footer_html)
    file_write(html_filepath, html)
    redirect(html_filepath, source='/plants/', target='/herbs/')

def art_herb_medicine_precautions(herb):
    herb_id = herb['herb_id']
    herb_slug = herb['herb_slug']
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_common = util_data.get_herb_common_name_by_id(herb_id)
    url = f'herbs/{herb_slug}/medicine/precautions'
    json_filepath = f'database/json/{url}.json'
    html_filepath = f'website/{url}.html'
    title = f'10 precautions to take when using {herb_name_scientific} ({herb_name_common})'
    aka = f', also known as {herb_name_common},'
    data = json_read(json_filepath, create=True)
    data['herb_id'] = herb_id
    data['herb_slug'] = herb_slug
    data['herb_name_common'] = herb_name_common
    data['herb_name_scientific'] = herb_name_scientific
    data['url'] = url
    if 'lastmod' not in data: data['lastmod'] = today()
    data['title'] = title
    util.json_write(json_filepath, data)
    article_html = ''
    article_html += f'<h1>{title.title()}</h1>\n'
    article_html += tw_img_gen_web_herb_rnd(herb)
    key = 'intro_desc'
    ai_paragraph_aka(json_filepath, data, key, aka, 
        prompts.herb_medicine_precautions__intro(herb_name_scientific, herb_name_common, aka)
    )
    if key in data:
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
    article_html += f'<p>This article explains in details the 10 most important precautions to take when using {herb_name_scientific} medicinally.</p>\n'

    key = 'precautions_list'
    if key not in data: data[key] = []
    herbs_precautions_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_HERBS_PRECAUTIONS_FILEPATH, herbs_precautions_cols['herb_id'], herb_id
    )
    for herb_precaution_row in herbs_precautions_rows_filtered:
        precaution_name = herb_precaution_row[herbs_precautions_cols['precaution_name']]
        found = False
        for obj in data[key]:
            if obj['precaution_name'] == precaution_name: 
                found = True
                break
        if not found:
            data[key].append({
                'herb_id': herb_id,
                'herb_slug': herb_slug,
                'herb_name_common': herb_name_common,
                'herb_name_scientific': herb_name_scientific,
                'precaution_name': precaution_name,
            })
    util.json_write(json_filepath, data)
    for i, obj in enumerate(data[key][:10]):
        obj_herb_name_common = obj["herb_name_common"].strip()
        obj_herb_name_scientific = obj["herb_name_scientific"].strip()
        obj_precaution_name = obj["precaution_name"].strip()
        precaution_slug = precaution_name.lower().strip().replace(' ', '-')
        key = 'precaution_desc'
        if key not in obj:
            aka = f', also known as {herb_name_common},'
            prompt = f'''
                write 1 paragraph of 60 to 80 words about the following precaution people should take when using {herb_name_scientific} medicinally.
                also, follow the guidelines below.
                ## precaution
                {precaution_name}
                ## guidelines
                include the reasons why it's important to take this precaution when using {herb_name_scientific}.
                start the reply with the following words: When using {herb_name_scientific}{aka} medicinally, it's important to {precaution_name} .
            '''
            reply = llm_reply(prompt)
            reply = reply.replace(aka, '')
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                reply = lines[0]
                print('********************************')
                print(reply)
                print('********************************')
                obj[key] = reply
                util.json_write(json_filepath, data)
        if key in obj:
            article_html += f'<h2>{i+1}. {precaution_name.capitalize()}</h2>\n'
            article_html += f'<p>{util.text_format_1N1_html(obj[key])}</p>\n'
    breadcrumbs = util.breadcrumbs(html_filepath)
    meta = components.meta(article_html, data['lastmod'])
    article = components.table_of_contents(article_html)
    html = templates.article(title, header_html, breadcrumbs, meta, article, footer_html)
    file_write(html_filepath, html)
    redirect(html_filepath, source='/plants/', target='/herbs/')

def gen_herb_medicine_precautions__precaution_desc(json_filepath, data, obj, article_html, i):
    herb_slug = data['herb_slug']
    herb_name_common = data['herb_name_common']
    herb_name_scientific = data['herb_name_scientific']
    precaution_name = obj['precaution_name']
    return article_html

def art_herb_category():
    html_list = ''
    for herb_row in herbs_rows:
        herb_id = herb_row[herbs_cols['herb_id']].strip()
        herb_slug = herb_row[herbs_cols['herb_slug']]
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']]
   
        url = f'herbs/{herb_slug}'
        json_filepath = f'database/json/{url}.json'
        if not os.path.exists(json_filepath): continue
        html_list += f'''
            <div>
                <a href="/herbs/{herb_slug}.html">{herb_name_scientific}</a>
            </div>
        '''
    html_filepath = f'website/herbs.html'
    breadcrumbs_html = util.breadcrumbs(html_filepath)
    html_title = f'List Of The Most Used Medicinal Herbs For Better Health'
    html_intro = f'The following list shows the best medicinal herbs to improve health and to heal ailments. Click on any of the following herbs to discover its medicinal aspects and much more. We decided to list the scientific names instead of the common ones to eliminiate ambiguity.'
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{g.AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>{html_title}</title>
            {g.GOOGLE_TAG}
            
        </head>
        <body>
            {header_html}
            {breadcrumbs_html}
            <section>
                <div class="container-md">
                    <h2 class="text-center">{html_title}</h2>
                    <p class="text-center">{html_intro}</p>
                </div>
            </section>
            <section class="blog-grid">
                <div class="container-lg">
                    <div class="grid grid-4 gap-24">
                        {html_list}
                    </div>
                </div>
            </section>
            <footer>
                <div class="container-lg">
                    <span>© TerraWhisper.com 2024 | All Rights Reserved
                </div>
            </footer>
        </body>
        </html>
    '''
    util.file_write(html_filepath, html)

def page_privacy_policy():
    slug = 'privacy-policy'
    filepath_in = f'templates/{slug}.html'
    filepath_out = f'website/{slug}.html'
    breadcrumbs_html = util.breadcrumbs(filepath_out)
    footer = components.footer()
    template = util.file_read(filepath_in)
    template = template.replace('[title]', 'TerraWhisper Privacy Policy')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header_html)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[footer]', footer)
    util.file_write(filepath_out, template)

def page_cookie_policy():
    slug = 'cookie-policy'
    filepath_in = f'templates/{slug}.html'
    filepath_out = f'website/{slug}.html'
    breadcrumbs_html = util.breadcrumbs(filepath_out)
    footer = components.footer()
    template = util.file_read(filepath_in)
    template = template.replace('[title]', 'TerraWhisper Cookie Policy')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header_html)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[footer]', footer)
    util.file_write(filepath_out, template)

def page_about():
    page_url = 'about'
    article_filepath_out = f'website/{page_url}.html'
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)
    content = util.file_read(f'static/about.md')
    template = util.file_read('templates/about.html')
    template = template.replace('[title]', 'TerraWhisper | About')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header_html)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[content]', content)
    util.file_write(article_filepath_out, template)

def page_top_herbs():
    articles_folderpath = 'database/articles/plants'
    plants = util.csv_get_rows('database/tables/plants.csv')
    articles_html = ''
    plants_primary = []
    for plant in plants[1:]:
        latin_name = plant[0].strip().capitalize()
        entity = latin_name.lower().replace(' ', '-')
        filepath_in = f'{articles_folderpath}/{entity}.json'
        data = json_read(filepath_in)
        title = data['title']
        common_name = data['common_name']
        article_html = f'''
            <a href="/plants/{entity}.html">
                <div>
                    <img src="/images/{entity}-overview.jpg" alt="">
                    <h3 class="mt-0 mb-0">{latin_name} ({common_name})</h3>
                </div>
            </a>
        '''
        plants_primary.append(article_html)
    articles_html += '<div class="articles">' +'\n'.join(plants_primary) + '</div>'
    page_url = 'top-herbs'
    article_filepath_out = f'website/{page_url}.html'
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)
    template = util.file_read(f'templates/{page_url}.html')
    template = template.replace('[meta_title]', 'Herbs')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header_html)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[articles]', articles_html)
    util.file_write(article_filepath_out, template)


# #########################################################
# ;remedies
# #########################################################
def page_remedies():
    lst = [
        {'system': 'digestive-system', 'organ': 'liver',},
        {'system': 'respiratory-system', 'organ': 'lungs',},
        {'system': 'cardiovascular-system', 'organ': 'heart',},
        {'system': 'musculoskeletal-system', 'organ': 'skull',},
        {'system': 'integumentary-system', 'organ': 'face',},
        {'system': 'nervous-system', 'organ': 'brain',},
        {'system': 'immune-system', 'organ': 'bone marrow',},
        {'system': 'urinary-system', 'organ': 'kidney',},
        {'system': 'reproductive-system', 'organ': 'uterus',},
        {'system': 'endocrine-system', 'organ': 'thyroid',},
        {'system': 'lymphatic-system', 'organ': 'spleen',},
    ]
    for item in lst:
        found = False
        for i in range(10):
            if os.path.exists(f'website/images-static/{item["system"]}-{i}.jpg'):
                found = True
                break
        if os.path.exists(f'website/images-static/{item["system"]}.jpg'):
            found = True
        if not found:
            for i in range(10):
                if not os.path.exists(f'website/images-static/{item["system"]}-{i}.jpg'):
                    prompt = f'''
                        {item['organ']}, botanical illustration, 
                        high resolution
                    '''
                    print(prompt)
                    image = pipe(prompt=prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                    image = img_resize(image, w=512, h=512)
                    image.save(f'website/images-static/{item["system"]}-{i}.jpg')

    title = f'Herbal Remedies To Heal Your Body Systems'
    content_html = ''
    for system_row in systems_rows:
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue
        src = f'/images-static/{system_slug}.jpg'
        alt = f'{system_name}'
        content_html += f'''
            <a href="/remedies/{system_slug}.html">
                <div>
                    <img src="{src}" alt="{alt}">
                    <h2 class="text-24 text-black no-underline mt-0 pt-16">{system_name.title()}</h2>
                </div>
            </a>
        '''
        page_url = f'remedies'
        article_filepath_out = f'website/{page_url}.html'
        breadcrumbs_html = util.breadcrumbs(article_filepath_out)
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                {g.GOOGLE_ADSENSE_TAG}
            </head>
            <body>
                {header_html}
                {breadcrumbs_html}
                <section class="container-xl">
                    <h1 class="mt-64 text-center">{title}</h1>
                    <div class="container-md text-center">
                        <p>This page lists the main systems of the body. <u>Select the body system in which your ailment is categorized</u>, to find out the best herbal remedies for it.
                        For example, if you want to find relief for your cough, click the respiratory system. Or, if you want to stop your headache, choose the nervous system.
                        Once you click a body system, you get redirected to a page that lists all the ailments associated to that body system.
                        If you don't know in which body system is classified your ailment, just browse around until you find it. It's your best option.
                        </p>
                    </div>
                    <div class="grid grid-3 gap-64 my-96">
                        {content_html}
                    </div>
                </section>
                {footer_html}
                {g.COOKIE_CONSENT}
            </body>
            </html>
        '''
    util.file_write(article_filepath_out, html)

def page_systems_old():
    status_list = csv_read_rows_to_json(g.CSV_STATUS_FILEPATH)
    system_list = csv_read_rows_to_json(g.CSV_SYSTEMS_FILEPATH)
    body_part_list = csv_read_rows_to_json(g.CSV_BODY_PARTS_FILEPATH)
    status_system_list = csv_read_rows_to_json(g.CSV_STATUS_SYSTEMS_FILEPATH)
    status_body_part_list = csv_read_rows_to_json(g.CSV_STATUS_PARTS_FILEPATH)

    data_merged = []
    for status in status_list:
        status_id = status["status_id"]
        status_slug = status["status_slug"]
        status_name = status["status_names"].split(',')[0].strip()
        status_system = [obj for obj in status_system_list if obj['status_id'] == status_id][0]
        system = [obj for obj in system_list if obj['system_id'] == status_system['system_id']][0]
        system_id = system['system_id']
        system_slug = system['system_slug']
        system_name = system['system_name']
        status_body_part = [obj for obj in status_body_part_list if obj['status_id'] == status_id][0]
        body_part = [obj for obj in body_part_list if obj['body_part_id'] == status_body_part['body_part_id']][0]
        body_part_id = body_part['body_part_id']
        body_part_slug = body_part['body_part_slug']
        body_part_name = body_part['body_part_name']
        data_merged.append({
            'status_id': status_id,
            'status_slug': status_slug, 
            'status_name': status_name, 
            'system_id': system_id, 
            'system_slug': system_slug, 
            'system_name': system_name, 
            'body_part_id': body_part_id,
            'body_part_slug': body_part_slug,
            'body_part_name': body_part_name,
        })

    for system in system_list:
        system_id = system['system_id']
        system_slug = system['system_slug']
        system_name = system['system_name']
        body_parts = []
        for obj in data_merged:
            if system_id == obj['system_id']:
                if obj['body_part_name'] not in body_parts:
                    body_parts.append(obj['body_part_name'])
        
        json_filepath = f'database/json/remedies/{system_slug}.json'
        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = json_read(json_filepath)
        data['url'] = system_slug
        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 
        title = f'{system_name.title()} Ailments To Heal With Herbal Remedies'
        data['title'] = title
        util.json_write(json_filepath, data)

        category_title = f'<h1>{title}</h1>'
        category_intro = f'<p></p>'
        content_html = ''
        content_html += f'''
            <section class="container-lg my-96">
                {category_title}
                {category_intro}
        '''
        for body_part in body_parts:
            content_html += f'''
                <div class="border-0 border-b-4 border-black border-solid mb-32 mt-64">
                    <h2 class="text-24 bg-black text-white pt-8 pb-4 px-16 inline-block">{body_part.title()}</h2>
                </div>
            '''
            content_html += f'<div class="grid grid-4 gap-32">'
            status_rows = []
            for obj in data_merged:
                if system_id == obj['system_id']:
                    if body_part == obj['body_part_name']:
                        status_rows.append([obj['status_id'], obj['status_slug'], obj['status_name']])
            for status_row in status_rows:
                status_id = status_row[0]
                status_slug = status_row[1]
                status_name = status_row[2]
                herbs_slugs_filtered = []
                for status_herb_row in status_herbs_rows:
                    j_status_id = status_herb_row[status_herbs_cols['status_id']]
                    j_herb_slug = status_herb_row[status_herbs_cols['herb_slug']]
                    if j_status_id == status_id:
                        herbs_slugs_filtered.append(j_herb_slug)
                herb_slug_filtered = herbs_slugs_filtered[0]
                src = f'/images/ailments/{status_slug}-herbal-remedies.jpg'
                alt = f'herbal remedies for {status_name}'
                content_html += f'''
                    <a href="/remedies/{system_slug}/{status_slug}.html" class="no-underline flex flex-col gap-16 mb-32">
                        <img src="{src}" alt="{alt}">
                        <h3 class="text-24 text-black">{status_name.title()}</h3>
                    </a>
                '''
            content_html += f'</div>'
        content_html += '</section>'

        title = f'{system_name.title()} Ailments to Heal With Herbal Remedies'
        page_url = f'remedies/{system_slug}'
        article_filepath_out = f'website/{page_url}.html'
        breadcrumbs_html = util.breadcrumbs(article_filepath_out)
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                {g.GOOGLE_ADSENSE_TAG}
            </head>
            <body>
                {header_html}
                {breadcrumbs_html}
                <section class="container-lg">
                    {content_html}
                </section>
                {footer_html}
                {g.COOKIE_CONSENT}
            </body>
            </html>
        '''
        '''
        template = util.file_read('templates/category.html')
        template = template.replace('[title]', )
        template = template.replace('[google_tag]', g.GOOGLE_TAG)
        template = template.replace('[author_name]', g.AUTHOR_NAME)
        template = template.replace('[header]', header_html)
        template = template.replace('[breadcrumbs]', breadcrumbs_html)
        template = template.replace('[content]', content_html)
        '''
        file_write(article_filepath_out, html)


def page_systems():
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')

    system_list = [
        'integumentary',
        'nervous',
        'digestive',
        'cardiovascular',
        'respiratory',
        'immune',
        'musculoskeletal',
        'urinary',
        'endocrine',
        'lymphatic',
        'reproductive',
    ]

    for system in system_list:
        system_slug = system
        system_name = system
        body_parts = []
        for obj in ailments:
            if system == obj['system_slug']:
                if obj['organ_slug'] not in body_parts:
                    body_parts.append(obj['organ_slug'])
        
        json_filepath = f'database/json/remedies/{system_slug}-system.json'
        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = json_read(json_filepath)
        data['url'] = f'{system_slug}-system'
        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 
        title = f'{system_name.title()} Ailments To Heal With Herbal Remedies'
        data['title'] = title
        util.json_write(json_filepath, data)

        category_title = f'<h1>{title}</h1>'
        category_intro = f'<p></p>'
        content_html = ''
        content_html += f'''
            <section class="container-lg my-96">
                {category_title}
                {category_intro}
        '''
        for body_part in body_parts:
            content_html += f'''
                <div class="border-0 border-b-4 border-black border-solid mb-32 mt-64">
                    <h2 class="text-24 bg-black text-white pt-8 pb-4 px-16 inline-block">{body_part.title()}</h2>
                </div>
            '''
            content_html += f'<div class="grid grid-4 gap-32">'
            ailments_filtered = []
            for obj in ailments:
                if system_slug == obj['system_slug']:
                    if body_part == obj['organ_slug']:
                        ailments_filtered.append(obj)

            for ailment in ailments_filtered:
                ailment_slug = ailment['ailment_slug']
                ailment_name = ailment['ailment_name']
                src = f'/images/ailments/{ailment_slug}-herbal-remedies.jpg'
                alt = f'herbal remedies for {ailment_name}'
                content_html += f'''
                    <a href="/remedies/{system_slug}-system/{ailment_slug}.html" class="no-underline flex flex-col gap-16 mb-32">
                        <img src="{src}" alt="{alt}">
                        <h3 class="text-24 text-black">{ailment_name.title()}</h3>
                    </a>
                '''
            content_html += f'</div>'
        content_html += '</section>'

        title = f'{system_name.title()} Ailments to Heal With Herbal Remedies'
        page_url = f'remedies/{system_slug}-system'
        article_filepath_out = f'website/{page_url}.html'
        breadcrumbs_html = util.breadcrumbs(article_filepath_out)
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                {g.GOOGLE_ADSENSE_TAG}
            </head>
            <body>
                {header_html}
                {breadcrumbs_html}
                <section class="container-lg">
                    {content_html}
                </section>
                {footer_html}
                {g.COOKIE_CONSENT}
            </body>
            </html>
        '''
        '''
        template = util.file_read('templates/category.html')
        template = template.replace('[title]', )
        template = template.replace('[google_tag]', g.GOOGLE_TAG)
        template = template.replace('[author_name]', g.AUTHOR_NAME)
        template = template.replace('[header]', header_html)
        template = template.replace('[breadcrumbs]', breadcrumbs_html)
        template = template.replace('[content]', content_html)
        '''
        file_write(article_filepath_out, html)


def articles_ailments():
    ailment_list = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailment_list):
        print(ailment)

        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']

        url = f'{g.CATEGORY_REMEDIES}/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'website/{url}.html'
        title = f'{ailment_name.title()}: Causes, Medicinal Herbs and Herbal Preparations'
        try: data = json_read(json_filepath, create=True)
        except: data = {}
        data['system_slug'] = system_slug
        data['ailment_slug'] = ailment_slug
        data['ailment_name'] = ailment_name
        data['url'] = url
        data['lastmod'] = today()
        data['title'] = title
        json_write(json_filepath, data)

        ## title
        article_html = ''
        article_html += f'<h1>{title}</h1>\n'

        ## image featured
        ## TODO: move this code at the end of the function with all the "article_html" lines??
        ## or it wont work when createing new ailments?
        featured_preparation_name = [obj['name'] for obj in data['preparations']][0]
        image_filepath = f'website/images/ailments/{ailment_slug}-herbal-remedies.jpg'
        preparation_type = 'a cup of'
        preparation_type = ''
        if not os.path.exists(image_filepath):
        # if True:
            prompt = f'''
                close-up of {preparation_type} herbal {featured_preparation_name}, 
                on a wooden table, surrounded by medicinal herbs,
                watercolor illustration,
                depth of field,
                detailed textures, high resolution, cinematic
            '''.replace('  ', ' ')
            image = pipe(prompt=prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=6.0).images[0]
            image = img_resize(image, w=768, h=768)
            image.save(image_filepath)
        src = f'/images/ailments/{ailment_slug}-herbal-remedies.jpg'
        alt = f'herbal remedies for {ailment_slug}'
        article_html += f'<p><img src="{src}" alt="{alt}"></p>\n'

        ## intro
        key = 'intro_desc'
        if key not in data or data[key] == '':
            prompt = f'''
                Write 1 short 60-80 words paragraph about: herbal remedies for {ailment_name}.
                Include a detailed definition of {ailment_name}.
                Include the causes of {ailment_name}.
                Include the negative impacts of {ailment_name} on health.
                Include the healing herbs and medicinal preparations to relief {ailment_name}.
                Include the precautions to take when using medicinal herbs for {ailment_name}.
                Reply in paragraph format.
                Don't include lists.
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)
        if key in data:
            article_html += f'{util.text_format_1N1_html(data[key])}\n'
        article_html += f'<p>This article explains in detail what are the causes of {ailment_name}, what medicinal herbs to use to relieve this problem and how to prepare these herbs to get the best results.</p>\n'

        ## causes
        key = 'causes_desc'
        if key not in data or data[key] == '':
            prompt = f'''
                Write 1 detailed paragraph about: causes of {ailment_name}.
                Pack as much information in as few words as possible.
                Don't write fluff, only proven data.
                Write the paragraph in 5 sentences.
                Start the reply with the following words: The main causes of {ailment_name} are .
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)
        if key in data and data[key] != '':
            article_html += f'<h2>What are the main causes of {ailment_name}?</h2>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'
        key = 'causes_list'
        if key not in data or data[key] == '':
            prompt = f'''
                Write a numbered list of most common causes of {ailment_name} and explain why.
                Order the list items by the most common to the least common.
                Write the names of the causes using as few words as possible.
                Write the descriptions of the causes in a full, complete and detailed sentence.
                Don't write fluff, only proven facts.
                Reply in the following JSON format: 
                [
                    {{"cause_name": "name of cause 1", "cause_description": "describe why this is a cause of {ailment_name}."}}, 
                    {{"cause_name": "name of cause 2", "cause_description": "describe why this is a cause of {ailment_name}."}}, 
                    {{"cause_name": "name of cause 3", "cause_description": "describe why this is a cause of {ailment_name}."}} 
                ]
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt).strip()
            try: 
                json_data = json.loads(reply)
                error = False
                for obj in json_data:
                    if 'cause_name' not in obj:
                        error = True
                        break
                    if 'cause_description' not in obj:
                        error = True
                        break
                if not error:
                    data[key] = json_data
                    json_write(json_filepath, data)
            except: pass
        if key in data and data[key] != '':
            article_html += f'<ul>\n'
            for obj in data[key]:
                article_html += f'<li><strong>{obj["cause_name"]}:</strong> {obj["cause_description"]}</li>\n'
            article_html += f'</ul>\n'

        ## herbs
        key = 'herbs'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            output_plants = []
            for i in range(20):
                print(f'{ailment_i}/{len(ailment_list)}: {ailment}')
                prompt = f'''
                    Write a numbered list of most common medicinal plants used for {ailment_name}.
                    Also, give a confidence score in number format from 1 to 10 for each plant representing how much you believe that medicinal plant is effective for the ailment.
                    
                    Write only the scientific names (botanical names) of the plants, don't add descriptions or common names.
                    Write the names of the plants using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"herb_name_scientific": "scientific name of herb 1", "confidence_score": "10"}}, 
                        {{"herb_name_scientific": "scientific name of herb 2", "confidence_score": "5"}}, 
                        {{"herb_name_scientific": "scientific name of herb 3", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names_scientific = []
                    for item in json_data:
                        line = item['herb_name_scientific']
                        score = item['confidence_score']
                        print(line)
                        for plant in plants_wcvp:
                            name_scientific = plant['scientfiicname']
                            if name_scientific.lower().strip() in line.lower().strip():
                                if len(name_scientific.split(' ')) > 1:
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    print(name_scientific)
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    names_scientific.append({"name": name_scientific, "score": score})
                                    break
                        ## exceptions
                        if line.lower().strip() == 'mentha piperita':
                                names_scientific.append({"name": 'Mentha x piperita', "score": score})
                    for obj in names_scientific:
                        name = obj['name']
                        score = obj['score']
                        found = False
                        for output_plant in output_plants:
                            print(output_plant)
                            print(name, '->', output_plant['plant_name_scientific'])
                            if name in output_plant['plant_name_scientific']: 
                                output_plant['plant_mentions'] += 1
                                output_plant['plant_score'] += int(score)
                                found = True
                                break
                        if not found:
                            output_plants.append({
                                'plant_name_scientific': name, 
                                'plant_mentions': 1, 
                                'plant_score': int(score), 
                            })
                output_plants_final = []
                for output_plant in output_plants:
                    output_plants_final.append({
                        'plant_name_scientific': output_plant['plant_name_scientific'],
                        'confidence_score': int(output_plant['plant_mentions']) * int(output_plant['plant_score']),
                    })
                    
                output_plants_final = sorted(output_plants_final, key=lambda x: x['confidence_score'], reverse=True)
                print('***********************')
                print('***********************')
                print('***********************')
                for output_plant in output_plants_final:
                    print(output_plant)
                print('***********************')
                print('***********************')
                print('***********************')
                
                data[key] = output_plants_final[:10]
                json_write(json_filepath, data)
        '''
        if data[key] != []:
            article_html += f'<h2>What are the primary medicinal plants used for {ailment_name}?</h2>\n'
            article_html += f'<ul>\n'
            for obj in data[key]:
                article_html += f'<li><strong>{obj["plant_name_scientific"]}:</strong> {obj["confidence_score"]}</li>\n'
            article_html += f'</ul>\n'
        '''

        key = 'herbs_desc'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            herbs_names = [obj['plant_name_scientific'] for obj in data['herbs']]
            herbs_names_prompt = ', '.join(herbs_names)
            prompt = f'''
                Write 1 detailed paragraph about what are the medicinal herbs for {ailment_name} and explain why.
                Include the following herbs: {herbs_names_prompt}.
                Pack as much information in as few words as possible.
                Don't write fluff, only proven data.
                Don't allucinate.
                Don't write the character ";".
                Write the paragraph in 5 sentences.
                Start the reply with the following words: The main medicinal herbs used for {ailment_name} are {herbs_names_prompt}. {herbs_names[0].capitalize()} .
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)
        if data[key] != []:
            article_html += f'<h2>What are the primary medicinal plants used for {ailment_name}?</h2>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        key = 'herbs_image'
        image_filepath = f'website/images/ailments/{ailment_slug}-medicinal-plants.jpg'
        herbs_names = [obj['plant_name_scientific'] for obj in data['herbs']]
        if not os.path.exists(image_filepath):
        # if True:
            images = []
            for i in range(10):
                prompt = f'''
                    {herbs_names[i]}, 
                    botanical illustration, medicinal illustration, 
                    blueprint, watercolor,
                    beige paper
                '''
                image = pipe(prompt=prompt, width=1216, height=832, num_inference_steps=30, guidance_scale=6.0).images[0]
                image = img_resize(image, w=500, h=300)
                images.append(image)
            image = Image.new(mode="RGB", size=(1000, 1500), color='#000000')
            image.paste(images[0], (0, 0))
            image.paste(images[1], (500, 0))
            image.paste(images[2], (0, 300))
            image.paste(images[3], (500, 300))
            image.paste(images[4], (0, 600))
            image.paste(images[5], (500, 600))
            image.paste(images[6], (0, 900))
            image.paste(images[7], (500, 900))
            image.paste(images[8], (0, 1200))
            image.paste(images[9], (500, 1200))
            image.save(image_filepath)
        image_filepath_new = f'website/images/ailments/{ailment_slug}-medicinal-plants-new.jpg'
        if os.path.exists(image_filepath):
        # if True:
            image = Image.open(image_filepath)
            draw = ImageDraw.Draw(image)
            px = 32
            py = 8
            font_size = 24
            font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
            font = ImageFont.truetype(font_path, font_size)
            # ---
            text = herbs_names[0].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((250 - text_w//2 - px, 300 - text_h - py*2), (250 + text_w//2 + px, 300)), '#000000')
            draw.text((250 - text_w//2, 300 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = herbs_names[1].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((750 - text_w//2 - px, 300 - text_h - py*2), (750 + text_w//2 + px, 300)), '#000000')
            draw.text((750 - text_w//2, 300 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = herbs_names[2].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((250 - text_w//2 - px, 600 - text_h - py*2), (250 + text_w//2 + px, 600)), '#000000')
            draw.text((250 - text_w//2, 600 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = herbs_names[3].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((750 - text_w//2 - px, 600 - text_h - py*2), (750 + text_w//2 + px, 600)), '#000000')
            draw.text((750 - text_w//2, 600 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = herbs_names[4].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((250 - text_w//2 - px, 900 - text_h - py*2), (250 + text_w//2 + px, 900)), '#000000')
            draw.text((250 - text_w//2, 900 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = herbs_names[5].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((750 - text_w//2 - px, 900 - text_h - py*2), (750 + text_w//2 + px, 900)), '#000000')
            draw.text((750 - text_w//2, 900 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = herbs_names[6].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((250 - text_w//2 - px, 1200 - text_h - py*2), (250 + text_w//2 + px, 1200)), '#000000')
            draw.text((250 - text_w//2, 1200 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = herbs_names[7].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((750 - text_w//2 - px, 1200 - text_h - py*2), (750 + text_w//2 + px, 1200)), '#000000')
            draw.text((750 - text_w//2, 1200 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = herbs_names[8].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((250 - text_w//2 - px, 1500 - text_h - py*2), (250 + text_w//2 + px, 1500)), '#000000')
            draw.text((250 - text_w//2, 1500 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = herbs_names[9].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((750 - text_w//2 - px, 1500 - text_h - py*2), (750 + text_w//2 + px, 1500)), '#000000')
            draw.text((750 - text_w//2, 1500 - text_h - py), text, '#ffffff', font=font)
            # ---
            image.save(image_filepath_new)
        if os.path.exists(image_filepath):
            src = f'/images/ailments/{ailment_slug}-medicinal-plants-new.jpg'
            alt = f'medicinal plants for {ailment_slug}'
            article_html += f'<p><img src="{src}" alt="{alt}"></p>\n'

        key = 'herbs_list'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            names = [obj['plant_name_scientific'] for obj in data['herbs']]
            names_prompt = ', '.join(names)
            prompt = f'''
                Write a description for each of the following medicinal plants explaining why that plant helps with {ailment_name}: {names_prompt}.
                Write the descriptions in a full, complete and detailed sentence.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"plant_name": "{{names[0]}}", "description": "describe why this plant helps with {ailment_name}."}}, 
                    {{"plant_name": "{{names[1]}}", "description": "describe why this plant helps with {ailment_name}."}}, 
                    {{"plant_name": "{{names[2]}}", "description": "describe why this plant helps with {ailment_name}."}}, 
                    {{"plant_name": "{{names[3]}}", "description": "describe why this plant helps with {ailment_name}."}}, 
                    {{"plant_name": "{{names[4]}}", "description": "describe why this plant helps with {ailment_name}."}}, 
                    {{"plant_name": "{{names[5]}}", "description": "describe why this plant helps with {ailment_name}."}}, 
                    {{"plant_name": "{{names[6]}}", "description": "describe why this plant helps with {ailment_name}."}}, 
                    {{"plant_name": "{{names[7]}}", "description": "describe why this plant helps with {ailment_name}."}}, 
                    {{"plant_name": "{{names[8]}}", "description": "describe why this plant helps with {ailment_name}."}}, 
                    {{"plant_name": "{{names[9]}}", "description": "describe why this plant helps with {ailment_name}."}} 
                ]
                Use the plants scientific names in the descriptions.
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass
            if json_data != {}:
                error = False
                for obj in json_data:
                    if 'plant_name' not in obj or 'description' not in obj:
                        error = True
                        break
                if not error:
                    data[key] = json_data
                    json_write(json_filepath, data)
        if data[key] != []:
            article_html += f'<ul>\n'
            for obj in data[key]:
                name = obj["plant_name"]
                description = obj["description"]
                article_html += f'<li><strong>{name}:</strong> {obj["description"]}</li>\n'
            article_html += f'</ul>\n'

        ## preparations
        key = 'preparations'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            data_output = []
            for i in range(20):
                print(f'{ailment_i}/{len(ailment_list)}: {ailment}')
                prompt = f'''
                    Write a numbered list of the 10 most common herbal preparation used for {ailment_name}.
                    Also, give a confidence score in number format from 1 to 10 for each preparation representing how much you believe that herbal preparation is effective for the ailment.
                    For reference, examples of types of herbal preparations are: tea, decoction, tincture, creams, capsules, etc. 
                    Don't include infusion, as it's the same of tea for me.
                    Don't include herbs names in the praparations, just write the type of the preparation.
                    Write the names of the preparations using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"preparation_name": "name of preparation 1", "confidence_score": "10"}}, 
                        {{"preparation_name": "name of preparation 2", "confidence_score": "5"}}, 
                        {{"preparation_name": "name of preparation 3", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    preparations = []
                    for item in json_data:
                        try: name = item['preparation_name']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        preparations.append({"name": name, "score": score})
                    for obj in preparations:
                        name = obj['name']
                        score = obj['score']
                        found = False
                        for obj in data_output:
                            if name in obj['name']: 
                                obj['mentions'] += 1
                                obj['score'] += int(score)
                                found = True
                                break
                        if not found:
                            data_output.append({
                                'name': name, 
                                'mentions': 1, 
                                'score': int(score), 
                            })
                data_output_final = []
                for obj in data_output:
                    data_output_final.append({
                        'name': obj['name'],
                        'score': int(obj['mentions']) * int(obj['score']),
                    })
                data_output_final = sorted(data_output_final, key=lambda x: x['score'], reverse=True)
                print('***********************')
                print('***********************')
                print('***********************')
                for obj in data_output_final:
                    print(obj)
                print('***********************')
                print('***********************')
                print('***********************')
                data[key] = data_output_final[:20]
                json_write(json_filepath, data)

        key = 'preparations_desc'
        if key not in data: data[key] = '' 
        # data[key] = ''
        if data[key] == '':
            preparations_names = [obj['name'] for obj in data['preparations']][:10]
            preparations_names_prompt = ', '.join(preparations_names)
            prompt = f'''
                Write 1 detailed paragraph about what are the medicinal herbal preparations for {ailment_name} and explain why.
                Include the following proparations: {preparations_names_prompt}.
                Pack as much information in as few words as possible.
                Don't write fluff, only proven data.
                Don't allucinate.
                Don't write the character ";".
                Write the paragraph in 5 sentences.
                Start the reply with the following words: The main herbal preparations used for {ailment_name} are {preparations_names_prompt}. {preparations_names[0].capitalize()} .
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if ':' in line: continue
                lines.append(line)
            if len(lines) == 1:
                data[key] = lines[0]
                json_write(json_filepath, data)
        if data[key] != '':
            article_html += f'<h2>What are the main herbal preparations used for {ailment_name}?</h2>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        key = 'preparations_image'
        image_filepath = f'website/images/ailments/{ailment_slug}-herbal-preparations.jpg'
        names = [obj['name'] for obj in data['preparations']]
        if not os.path.exists(image_filepath):
        # if True:
            images = []
            for i in range(10):
                prompt = f'''
                    herbal {names[i]}, 
                    medicinal illustration, 
                    blueprint, watercolor,
                    beige paper
                '''
                image = pipe(prompt=prompt, width=1216, height=832, num_inference_steps=30, guidance_scale=6.0).images[0]
                image = img_resize(image, w=500, h=300)
                images.append(image)
            image = Image.new(mode="RGB", size=(1000, 1500), color='#000000')
            image.paste(images[0], (0, 0))
            image.paste(images[1], (500, 0))
            image.paste(images[2], (0, 300))
            image.paste(images[3], (500, 300))
            image.paste(images[4], (0, 600))
            image.paste(images[5], (500, 600))
            image.paste(images[6], (0, 900))
            image.paste(images[7], (500, 900))
            image.paste(images[8], (0, 1200))
            image.paste(images[9], (500, 1200))
            image.save(image_filepath)
        image_filepath_new = f'website/images/ailments/{ailment_slug}-herbal-preparations-new.jpg'
        if os.path.exists(image_filepath):
        # if True:
            image = Image.open(image_filepath)
            draw = ImageDraw.Draw(image)
            px = 32
            py = 8
            font_size = 24
            font_path = f"website/assets/fonts/helvetica/Helvetica.ttf"
            font = ImageFont.truetype(font_path, font_size)
            # ---
            text = names[0].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((250 - text_w//2 - px, 300 - text_h - py*2), (250 + text_w//2 + px, 300)), '#000000')
            draw.text((250 - text_w//2, 300 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = names[1].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((750 - text_w//2 - px, 300 - text_h - py*2), (750 + text_w//2 + px, 300)), '#000000')
            draw.text((750 - text_w//2, 300 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = names[2].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((250 - text_w//2 - px, 600 - text_h - py*2), (250 + text_w//2 + px, 600)), '#000000')
            draw.text((250 - text_w//2, 600 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = names[3].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((750 - text_w//2 - px, 600 - text_h - py*2), (750 + text_w//2 + px, 600)), '#000000')
            draw.text((750 - text_w//2, 600 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = names[4].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((250 - text_w//2 - px, 900 - text_h - py*2), (250 + text_w//2 + px, 900)), '#000000')
            draw.text((250 - text_w//2, 900 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = names[5].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((750 - text_w//2 - px, 900 - text_h - py*2), (750 + text_w//2 + px, 900)), '#000000')
            draw.text((750 - text_w//2, 900 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = names[6].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((250 - text_w//2 - px, 1200 - text_h - py*2), (250 + text_w//2 + px, 1200)), '#000000')
            draw.text((250 - text_w//2, 1200 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = names[7].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((750 - text_w//2 - px, 1200 - text_h - py*2), (750 + text_w//2 + px, 1200)), '#000000')
            draw.text((750 - text_w//2, 1200 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = names[8].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((250 - text_w//2 - px, 1500 - text_h - py*2), (250 + text_w//2 + px, 1500)), '#000000')
            draw.text((250 - text_w//2, 1500 - text_h - py), text, '#ffffff', font=font)
            # ---
            text = names[9].capitalize()
            _, _, text_w, text_h = font.getbbox(text)
            draw.rectangle(((750 - text_w//2 - px, 1500 - text_h - py*2), (750 + text_w//2 + px, 1500)), '#000000')
            draw.text((750 - text_w//2, 1500 - text_h - py), text, '#ffffff', font=font)
            # ---
            image.save(image_filepath_new)
        if os.path.exists(image_filepath):
            src = f'/images/ailments/{ailment_slug}-herbal-preparations-new.jpg'
            alt = f'herbal preparations for {ailment_slug}'
            article_html += f'<p><img src="{src}" alt="{alt}"></p>\n'

        key = 'preparation_list'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            names = [obj['name'] for obj in data['preparations']][:10]
            names_prompt = ', '.join(names)
            prompt = f'''
                Write a description for each of the following medicinal herbal preparation explaining why that preparation helps with {ailment_name}: {names_prompt}.
                Write the descriptions in a full, complete and detailed sentence.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"preparation_name": "{{names[0]}}", "description": "describe why this preparation helps with {ailment_name}."}}, 
                    {{"preparation_name": "{{names[1]}}", "description": "describe why this preparation helps with {ailment_name}."}}, 
                    {{"preparation_name": "{{names[2]}}", "description": "describe why this preparation helps with {ailment_name}."}}, 
                    {{"preparation_name": "{{names[3]}}", "description": "describe why this preparation helps with {ailment_name}."}}, 
                    {{"preparation_name": "{{names[4]}}", "description": "describe why this preparation helps with {ailment_name}."}}, 
                    {{"preparation_name": "{{names[5]}}", "description": "describe why this preparation helps with {ailment_name}."}}, 
                    {{"preparation_name": "{{names[6]}}", "description": "describe why this preparation helps with {ailment_name}."}}, 
                    {{"preparation_name": "{{names[7]}}", "description": "describe why this preparation helps with {ailment_name}."}}, 
                    {{"preparation_name": "{{names[8]}}", "description": "describe why this preparation helps with {ailment_name}."}}, 
                    {{"preparation_name": "{{names[9]}}", "description": "describe why this preparation helps with {ailment_name}."}} 
                ]
                Use the plants scientific names in the descriptions.
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass
            if json_data != {}:
                error = False
                for obj in json_data:
                    if 'preparation_name' not in obj or 'description' not in obj:
                        error = True
                        break
                if not error:
                    data[key] = json_data
                    json_write(json_filepath, data)
        if data[key] != []:
            article_html += f'<ul>\n'
            for obj in data[key]:
                name = obj["preparation_name"]
                preparation_slug = obj["preparation_name"].lower().strip().replace(' ', '-') + 's'
                description = obj["description"]
                href = f'/{g.CATEGORY_REMEDIES}/{system_slug}-system/{ailment_slug}/{preparation_slug}.html'
                filepath = f'website/{g.CATEGORY_REMEDIES}/{system_slug}-system/{ailment_slug}/{preparation_slug}.html'
                if os.path.exists(filepath):
                    article_html += f'<li><strong><a href="{href}">{name}</a>:</strong> {obj["description"]}</li>\n'
                else:
                    article_html += f'<li><strong>{name}:</strong> {obj["description"]}</li>\n'
            article_html += f'</ul>\n'

        breadcrumbs = util.breadcrumbs(html_filepath)
        meta = components.meta(article_html, data['lastmod'])
        article = components.table_of_contents(article_html)
        html = templates.article(title, header_html, breadcrumbs, meta, article, footer_html)
        file_write(html_filepath, html)

def gen_status__precautions(json_filepath, data, article_html):
    key = 'precautions_desc'
    status_name = data['status_name']
    if key not in data:
        prompt = f'''
            Write 1 paragraph about the precautions to take when using herbal remedies for {status_name}.
        '''
        reply = llm_reply(prompt)
        reply = utils_ai.reply_to_paragraphs(reply)
        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply[0]
            util.json_write(json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)
    if key in data:
        article_html += f'<h2>What precautions to take when using herbal remedies for {status_name}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data[key])}\n'
    key = 'precautions_list'
    if key not in data:
        prompt = f'''
            Write a numbered list of precautions to take when using herbal remedies for {status_name}.
            Start each precaution with an action verb.
            Don't use the character ":".
        '''
        reply = llm_reply(prompt)
        lines = reply.split('\n')
        lines_formatted = []
        for line in lines:
            line = line.strip()
            if line == '': continue
            line = line.replace('*', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            if not line[0].isdigit(): continue
            if '.' not in line: continue
            if ':' in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue
            lines_formatted.append(line)
        print(len(lines_formatted))
        if len(lines_formatted) >= 4:
            print('***************************************')
            print(lines_formatted)
            print('***************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)
    if key in data:
        article_html += f'<p>The most important precautions to take when using herbal remedies for {status_name} are listed below.</p>\n'
        article_html += f'<ul>\n'
        for item in data['precautions_list']:
            article_html += f'<li>{item}</li>\n'
        article_html += f'</ul>\n'
    return article_html

# #########################################################
# EXE
# #########################################################

def page_home():
    html = templates.homepage()
    page_url = f'index'
    article_filepath_out = f'website/{page_url}.html'
    util.file_write(article_filepath_out, html)

def page_about():
    html = templates.about_page()
    page_url = f'about-us'
    article_filepath_out = f'website/{page_url}.html'
    util.file_write(article_filepath_out, html)

def page_contact():
    html = templates.contact_page()
    page_url = f'contacts'
    article_filepath_out = f'website/{page_url}.html'
    util.file_write(article_filepath_out, html)


def main():
    sitemap.sitemap_all()
    shutil.copy2('sitemap.xml', 'website/sitemap.xml')
    shutil.copy2('style.css', 'website/style.css')

    main_preparations()
    quit()
    articles_ailments()
    page_systems()

    page_home()
    page_about()
    page_contact()

    page_remedies()

    main_herbs()

    page_privacy_policy()
    page_cookie_policy()



    # filepath_in = 'assets/images/hero-salvia-2.jpg'
    # filepath_out = 'website/images/hero-salvia-2.jpg'
    # if not os.path.exists(filepath_out):
        # img = Image.open(filepath_in)
        # img = util_image.img_resize(img, 768, 768)
        # img.save(filepath_out, format='JPEG', optimize=True, quality=50)


    # shutil.copy2('util.css', 'website/util.css')
    # shutil.copy2('assets/images/healing-herbs.jpg', 'website/images/healing-herbs.jpg')
    # shutil.copy2('assets/images/hero-salvia.jpg', 'website/images/hero-salvia.jpg')
    # shutil.copy2('assets/images/hero-salvia-2.jpg', 'website/images/hero-salvia-2.jpg')
    # shutil.copy2('pinterest-3e4f1.html', 'website/pinterest-3e4f1.html')

main()
