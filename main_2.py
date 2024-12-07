import os
import json
import random
import shutil
import datetime

import torch
from diffusers import DiffusionPipeline
from diffusers import StableDiffusionXLPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image, ImageFont, ImageDraw

import util

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

if 0:
    if 0:
        prompt = f'''
            write an outline for an article with the following title:
            10 herbal teas for dry hair
        '''
        reply = llm_reply(prompt)
        quit()
    if 0:
        prompt = f'''
            heres the title of my article title: 10 herbal teas for dry hair
            this article has an intro paragraph and 10 sub sections, one for each of the 10 herbal tea.
            give me a list of other supplementary things i can write about at the bottom of the article that a target reader would be very intereste in.
            reply only with the supplementary content.
        '''
        reply = llm_reply(prompt)
        quit()
    quit()

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

def today():
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    day = today.day
    today = f'{year}-{month}-{day}'
    print(today)
    return today

AUTHOR_NAME = 'Leen Randell'
GOOGLE_TAG = '''
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-9086LN3SRR"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-9086LN3SRR');
    </script>
'''
COOKIE_CONSENT = '''
    <div class="cookie-box">
        <p class="title">Cookies Consent</p>
        <p class="info">This website uses cookies to serve you the best content. To be compliant with GDPR and privacy laws, we require you to understand and accept that we are using cookies. 
        <div class="actions">
            <button class="item">Accept all</button>
            <a href="/cookie-policy.html">Read Our Cookie Policy</a></p>
        </div>
    </div>
    <script>
            const cookieBox = document.querySelector(".cookie-box"),
            acceptBtn = cookieBox.querySelector("button");
            acceptBtn.onclick = ()=>{
              //setting cookie for 1 month, after one month it'll be expired automatically
              document.cookie = "CookieBy=TerraWhisper; max-age="+60*60*24*30*12;
              if(document.cookie){ //if cookie is set
                cookieBox.classList.add("hide"); //hide cookie box
              }else{ //if cookie not set then alert an error
                alert("Cookie can't be set! Please unblock this site from the cookie setting of your browser.");
              }
            }
            let checkCookie = document.cookie.indexOf("CookieBy=TerraWhisper"); //checking our cookie
            //if cookie is set then hide the cookie box else show it
            checkCookie != -1 ? cookieBox.classList.add("hide") : cookieBox.classList.remove("hide");
    </script>
'''
with open('assets/scripts/google-adsense.txt') as f: GOOGLE_ADSENSE_TAG = f.read()

top_bar_html = f'''
    <section class="bg-black">
        <div class="container-xl">
            <div class="flex justify-between items-center top-bar">
                <span class="text-white text-14">Terrawhisper</span>
                <div class="flex gap-16">
                    <a href="https://www.pinterest.com/terrawhisper" target="_blank" class="inline-block">
                        <img class="social-icon-16" src="images-static/pinterest-small-white.png">
                    </a>
                    <a href="https://www.x.com/leenrandell" target="_blank" class="inline-block">
                        <img class="social-icon-16" src="images-static/twitter-small-white.png">
                    </a>
                </div>
            </div>
        </div>
    </section>
'''

header_html = ''
header_html += top_bar_html
header_html += f'''
    <header class="header">
        <a class="" href="/"><img height="64" src="/images-static/terrawhisper-logo-white.jpg" alt="logo of terrawhisper"></a>
        <nav class="header-nav">
            <a class="text-black no-underline text-16 menu-item" href="/remedies.html">REMEDIES</a>
            <a class="text-black no-underline text-16 menu-item" href="/about.html">ABOUT</a>
            <a class="text-black no-underline text-16 menu-item" href="/contacts.html">CONTACTS</a>
        </nav>
    </header>
'''
            # <a class="button-green-fill" href="/herbs.html">View Herbs</a>

footer_html = f'''
    <footer class="footer">
        <span>© TerraWhisper.com 2024 | All Rights Reserved</span>
        <div class="flex gap-24">
            <a href="/privacy-policy.html">Privacy Policy</a>
            <a href="/cookie-policy.html">Cookie Policy</a>
        </div>
    </footer>
'''

def head_html_generate(title, css_filepath):
    head_html = f'''
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="{css_filepath}">
            <title>{title}</title>
            {GOOGLE_TAG}
            {GOOGLE_ADSENSE_TAG}
        </head>
    '''
    return head_html

def articles_ailments_2():
    plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        print(f'\n>> {ailment_i}/{len(ailments)}')
        print(f'    >> {ailment}')
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/remedies'): 
            os.mkdir(f'{website_folderpath}/remedies')
        if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system'): 
            os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system')

        # if os.path.exists(json_filepath): os.remove(json_filepath)
        # continue

        data = json_read(json_filepath, create=True)
        data['ailment_slug'] = ailment_slug
        data['ailment_name'] = ailment_name
        data['system_slug'] = system_slug
        data['organ_slug'] = organ_slug
        data['url'] = url
        if 'lastmod' not in data: data['lastmod'] = today()

        if 'title' not in data: data['title'] = ''
        # data['title'] = ''
        if data['title'] == '':
            prompt = f'''
                Rewrite the following title in 10 different ways: {ailment_name}: Causes, Medicinal Herbs And Herbal Preparations.
                Write only the titles.
                Include the following words in each title: {ailment_name}.
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '. ' not in line: continue
                line = '. '.join(line.split('. ')[1:])
                line = line.replace('*', '')
                if line.endswith('.'): line = line[:-1]
                line = line.strip()
                if line == '': continue
                lines.append(line)
            line = random.choice(lines)
            data['title'] = line
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;causes
        ## ------------------------------------
        if 0:
            key = 'causes'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'causes'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            prompt = f'''
                List the names of the 20 most common causes of {ailment_name}.
                Also, for each cause name give a confidence score from 1 to 10, indicating how sure you are that is a cause of {ailment_name}.
                Write only the names of the causes, don't add descriptions.
                Write the names of the causes using as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"cause_name": "name of cause 1", "confidence_score": 10}}, 
                    {{"cause_name": "name of cause 2", "confidence_score": 5}}, 
                    {{"cause_name": "name of cause 3", "confidence_score": 7}} 
                ]
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                outputs = []
                for item in json_data:
                    try: item['cause_name']
                    except: continue
                    try: item['confidence_score']
                    except: continue
                    outputs.append({
                        'cause_name': item['cause_name'], 
                        'cause_confidence_score': int(item['confidence_score']),
                    })
            outputs = sorted(outputs, key=lambda x: x['cause_confidence_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output in outputs:
                print(output)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = outputs[:10]
            json_write(json_filepath, data)

        key = 'causes_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            causes_names = [x['cause_name'] for x in data['causes'][:5]]
            prompt = f'''
                Write a detailed paragraph explaining what are the main causes of {ailment_name}.
                Include the following causes and explain why: {causes_names}.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;benefits
        ## ------------------------------------
        key = 'benefits_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write a detailed paragraph explaining what are the main benefits of using herbs for {ailment_name}.
                Don't write the names of the herbs.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;herbs
        ## ------------------------------------
        if 0:
            key = 'herbs'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'herbs'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            items_num = 20
            output_plants = []
            for i in range(5):
                print(f'{ailment_i}/{len(ailments)} - {i}/20: {ailment}')
                prompt = f'''
                    List the best herbs to relieve {ailment_name}.
                    Also, for each herb name give a confidence score from 1 to 10, indicating how sure you are that herb is effective to relieve {ailment_name}.
                    Write only the scientific names (botanical names) of the herbs, don't add descriptions or common names.
                    Write the names of the herbs using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"herb_name_scientific": "scientific name of herb 1 used for preparation", "confidence_score": "10"}}, 
                        {{"herb_name_scientific": "scientific name of herb 2 used for preparation", "confidence_score": "5"}}, 
                        {{"herb_name_scientific": "scientific name of herb 3 used for preparation", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names_scientific = []
                    for item in json_data:
                        try: line = item['herb_name_scientific']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        print(line)
                        for plant in plants_wcvp:
                            name_scientific = plant['scientfiicname']
                            if name_scientific.lower().strip() in line.lower().strip():
                                if len(name_scientific.split(' ')) > 1:
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    print(name_scientific)
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    names_scientific.append({
                                        "name": name_scientific, 
                                        "score": score,
                                    })
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
                            print(name, '->', output_plant['herb_name_scientific'])
                            if name in output_plant['herb_name_scientific']: 
                                output_plant['herb_mentions'] += 1
                                output_plant['herb_confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            output_plants.append({
                                'herb_name_scientific': name, 
                                'herb_mentions': 1, 
                                'herb_confidence_score': int(score), 
                            })
            output_plants_final = []
            for output_plant in output_plants:
                output_plants_final.append({
                    'herb_name_scientific': output_plant['herb_name_scientific'],
                    'herb_mentions': int(output_plant['herb_mentions']),
                    'herb_confidence_score': int(output_plant['herb_confidence_score']),
                    'herb_total_score': int(output_plant['herb_mentions']) * int(output_plant['herb_confidence_score']),
                })
            output_plants_final = sorted(output_plants_final, key=lambda x: x['herb_total_score'], reverse=True)
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

        key = 'herbs_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['herbs'][:5]]
            prompt = f'''
                Write a detailed paragraph explaining why herbs are good for {ailment_name}.
                Include the following herbs and expalin why they are good: {herbs_names}.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;preparations
        ## ------------------------------------
        if 0:
            key = 'preparations'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'preparations'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            items_num = 20
            data_output = []
            for i in range(5):
                print(f'{ailment_i}/{len(ailments)}: {ailment}')
                prompt = f'''
                    Write a numbered list of the 10 most common herbal preparation used for {ailment_name}.
                    Also, give a confidence score in number format from 1 to 10 for each preparation representing how much you believe that herbal preparation is effective for the ailment.
                    For reference, examples of types of herbal preparations are: tea, decoction, tincture, creams, capsules, etc. 
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
                        try: 
                            score = item['confidence_score']
                            int(score)
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
                    'preparation_name': obj['name'],
                    'preparation_mentions': int(obj['mentions']),
                    'preparation_confidence_score': int(obj['score']),
                    'preparation_total_score': int(obj['mentions']) * int(obj['score']),
                })
            data_output_final = sorted(data_output_final, key=lambda x: x['preparation_total_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for obj in data_output_final:
                print(obj)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = data_output_final[:10]
            json_write(json_filepath, data)

        key = 'preparations_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            preparations_names = [x['preparation_name'] for x in data['preparations'][:5]]
            prompt = f'''
                Write a detailed paragraph explaining why herbal preparations are good for {ailment_name}.
                Include the following preparations and explain why they are good: {preparations_names}.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        #######################################################
        # ;image
        #######################################################
        if 1:
            herbs_names = [x['herb_name_scientific'] for x in data['herbs'][:5]]
            herb = random.choice(herbs_names)
            output_filepath = f'{website_folderpath}/images/ailments/{ailment_slug}-herbal-remedies.jpg'
            src = f'/images/ailments/{ailment_slug}-herbal-remedies.jpg'
            alt = f'herbal remedies for {ailment_name}'
            if not os.path.exists(output_filepath):
            # if system_slug == 'cardiovascular':
            # if True:
                prompt = f'''
                    dry {herb} herb on a wooden table,
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
                image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                image = img_resize(image, w=768, h=768)
                image.save(output_filepath)
            data['intro_image_src'] = src
            data['intro_image_alt'] = alt
            json_write(json_filepath, data)

        #######################################################
        # ;html
        #######################################################
        article_html = ''
        article_html += f'<h1>{data["title"]}</h1>'
        src = data['intro_image_src']
        alt = data['intro_image_alt']
        article_html += f'<img src="{src}" alt="{alt}">'
        article_html += f'<h2>What are the causes of {ailment_name}?</h2>'
        article_html += f'{util.text_format_1N1_html(data["causes_desc"])}\n'
        article_html += f'<h2>What are the main benefits of using herbs for {ailment_name}?</h2>'
        article_html += f'{util.text_format_1N1_html(data["benefits_desc"])}\n'
        article_html += f'<h2>What are the main medicinal herbs for {ailment_name}?</h2>'
        article_html += f'{util.text_format_1N1_html(data["herbs_desc"])}\n'
        article_html += f'<h2>What are the most used herbal preparations for {ailment_name}?</h2>'
        article_html += f'{util.text_format_1N1_html(data["preparations_desc"])}\n'

        head_html = head_html_generate(data['title'], '/style-article.css')
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                <main class="container-md">
                    {article_html}
                </main>
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)
        print(f'\n')
        print(html_filepath)
        # quit()



def articles_ailments():
    plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        print(f'\n>> {ailment_i}/{len(ailments)}')
        print(f'    >> {ailment}')
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        if not os.path.exists(f'{website_folderpath}/remedies'): 
            os.mkdir(f'{website_folderpath}/remedies')
        if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system'): 
            os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system')

        # if os.path.exists(json_filepath): os.remove(json_filepath)
        # continue

        data = json_read(json_filepath, create=True)
        data['ailment_slug'] = ailment_slug
        data['ailment_name'] = ailment_name
        data['system_slug'] = system_slug
        data['organ_slug'] = organ_slug
        data['url'] = url
        if 'lastmod' not in data: data['lastmod'] = today()

        if 'remedies_num' not in data: data['remedies_num'] = ''
        # data['remedies_num'] = ''
        if data['remedies_num'] == '': data['remedies_num'] = random.randint(7, 11)
        remedies_num = data['remedies_num']

        if 'preparations_num' not in data: data['preparations_num'] = ''
        # data['preparations_num'] = ''
        if data['preparations_num'] == '': data['preparations_num'] = random.randint(5, 9)
        preparations_num = data['preparations_num']

        if 'causes_num' not in data: data['causes_num'] = ''
        # data['causes_num'] = ''
        if data['causes_num'] == '': data['causes_num'] = random.randint(5, 7)
        causes_num = data['causes_num']

        if 'title' not in data: data['title'] = ''
        # data['title'] = ''
        if data['title'] == '':
            prompt = f'''
                Rewrite the following title in 10 different ways: {ailment_name}: Causes, Medicinal Herbs And Herbal Preparations.
                Write only the titles.
                Include the following words in each title: {ailment_name}.
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '. ' not in line: continue
                line = '. '.join(line.split('. ')[1:])
                line = line.replace('*', '')
                if line.endswith('.'): line = line[:-1]
                line = line.strip()
                if line == '': continue
                lines.append(line)
            line = random.choice(lines)
            data['title'] = line
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;causes
        ## ------------------------------------
        if 0:
            key = 'causes'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'causes'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            prompt = f'''
                List the names of the 20 most common causes of {ailment_name}.
                Also, for each cause name give a confidence score from 1 to 10, indicating how sure you are that is a cause of {ailment_name}.
                Write only the names of the causes, don't add descriptions.
                Write the names of the causes using as few words as possible.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"cause_name": "name of cause 1", "confidence_score": 10}}, 
                    {{"cause_name": "name of cause 2", "confidence_score": 5}}, 
                    {{"cause_name": "name of cause 3", "confidence_score": 7}} 
                ]
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                outputs = []
                for item in json_data:
                    try: item['cause_name']
                    except: continue
                    try: item['confidence_score']
                    except: continue
                    outputs.append({
                        'cause_name': item['cause_name'], 
                        'cause_confidence_score': int(item['confidence_score']),
                    })
            outputs = sorted(outputs, key=lambda x: x['cause_confidence_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output in outputs:
                print(output)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = outputs[:causes_num]
            json_write(json_filepath, data)

        ## ------------------------------------
        ## ;remedies
        ## ------------------------------------
        if 0:
            key = 'remedies'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        key = 'remedies'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            items_num = 20
            output_plants = []
            for i in range(20):
                print(f'{ailment_i}/{len(ailments)} - {i}/20: {ailment}')
                prompt = f'''
                    List the best herbs to relieve {ailment_name}.
                    Also, for each herb name give a confidence score from 1 to 10, indicating how sure you are that herb is effective to relieve {ailment_name}.
                    Write only the scientific names (botanical names) of the herbs, don't add descriptions or common names.
                    Write the names of the herbs using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"herb_name_scientific": "scientific name of herb 1 used for preparation", "confidence_score": "10"}}, 
                        {{"herb_name_scientific": "scientific name of herb 2 used for preparation", "confidence_score": "5"}}, 
                        {{"herb_name_scientific": "scientific name of herb 3 used for preparation", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names_scientific = []
                    for item in json_data:
                        try: line = item['herb_name_scientific']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        print(line)
                        for plant in plants_wcvp:
                            name_scientific = plant['scientfiicname']
                            if name_scientific.lower().strip() in line.lower().strip():
                                if len(name_scientific.split(' ')) > 1:
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    print(name_scientific)
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    names_scientific.append({
                                        "name": name_scientific, 
                                        "score": score,
                                    })
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
                            print(name, '->', output_plant['herb_name_scientific'])
                            if name in output_plant['herb_name_scientific']: 
                                output_plant['herb_mentions'] += 1
                                output_plant['herb_confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            output_plants.append({
                                'herb_name_scientific': name, 
                                'herb_mentions': 1, 
                                'herb_confidence_score': int(score), 
                            })
            output_plants_final = []
            for output_plant in output_plants:
                output_plants_final.append({
                    'herb_name_scientific': output_plant['herb_name_scientific'],
                    'herb_mentions': int(output_plant['herb_mentions']),
                    'herb_confidence_score': int(output_plant['herb_confidence_score']),
                    'herb_total_score': int(output_plant['herb_mentions']) * int(output_plant['herb_confidence_score']),
                })
            output_plants_final = sorted(output_plants_final, key=lambda x: x['herb_total_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output_plant in output_plants_final:
                print(output_plant)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = output_plants_final[:items_num]
            json_write(json_filepath, data)

        ## preparations
        key = 'preparations'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            items_num = 20
            data_output = []
            for i in range(20):
                print(f'{ailment_i}/{len(ailments)}: {ailment}')
                prompt = f'''
                    Write a numbered list of the 10 most common herbal preparation used for {ailment_name}.
                    Also, give a confidence score in number format from 1 to 10 for each preparation representing how much you believe that herbal preparation is effective for the ailment.
                    For reference, examples of types of herbal preparations are: tea, decoction, tincture, creams, capsules, etc. 
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
                        try: 
                            score = item['confidence_score']
                            int(score)
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
                    'preparation_name': obj['name'],
                    'preparation_mentions': int(obj['mentions']),
                    'preparation_confidence_score': int(obj['score']),
                    'preparation_total_score': int(obj['mentions']) * int(obj['score']),
                })
            data_output_final = sorted(data_output_final, key=lambda x: x['preparation_total_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for obj in data_output_final:
                print(obj)
            print('***********************')
            print('***********************')
            print('***********************')
            data[key] = data_output_final[:items_num]
            json_write(json_filepath, data)

        ########################################
        ########################################
        ########################################
        key = 'intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies'][:3]]
            preparations_names = [x['preparation_name'] for x in data['preparations'][:3]]
            prompt = f'''
                Write a detailed paragraph explaining why herbs and herbal preparations are good for {ailment_name}.
                Include the following herbs: {herbs_names}.
                Include the following herbal preparations: {preparations_names}.
                Include why it's important to deal with {ailment_name} and what are the consequences if you don't do it.
                Start with a definition of {ailment_name}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                Start with the following words: {ailment_name} is .
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        key = 'causes_intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            causes_names = [x['cause_name'] for x in data['causes'][:3]]
            prompt = f'''
                Write a detailed paragraph explaining what are the main causes of {ailment_name}.
                Include the following causes and explain why: {causes_names}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        for obj_i, obj in enumerate(data['causes'][:causes_num]):
            print(f'{ailment_i}/{len(ailments)} - {obj_i}/{causes_num} - {obj}')
            key = 'cause_desc'
            if key not in obj: obj[key] = ''
            # obj[key] = ''
            if obj[key] == '':
                cause_name = obj['cause_name']
                prompt = f'''
                    Write 1 detailed sentence explaining why {cause_name} is a cause of {ailment_name}.
                    Use simple and short words, and a simple writing style.
                '''
                reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
                obj[key] = reply
                json_write(json_filepath, data)

        key = 'remedies_intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies'][:3]]
            prompt = f'''
                Write a detailed paragraph explaining why herbs are good for {ailment_name}.
                Include the following herbs and expalin why they are good: {herbs_names}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        for remedy_i, obj in enumerate(data['remedies'][:remedies_num]):
            print(f'{ailment_i}/{len(ailments)} - {remedy_i}/{remedies_num} - {obj}')
            key = 'remedy_desc'
            if key not in obj: obj[key] = ''
            # obj[key] = ''
            if obj[key] == '':
                herb_name = obj['herb_name_scientific']
                prompt = f'''
                    Write a detailed paragraph explaining why {herb_name} is good for {ailment_name}.
                    Use simple and short words, and a simple writing style.
                    Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                '''
                reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
                obj[key] = reply
                json_write(json_filepath, data)

        key = 'preparations_intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            preparations_names = [x['preparation_name'] for x in data['preparations'][:3]]
            prompt = f'''
                Write a detailed paragraph explaining why herbal preparations are good for {ailment_name}.
                Include the following herbal preparations and explain why they are good: {preparations_names}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)
    
        for obj_i, obj in enumerate(data['preparations'][:preparations_num]):
            print(f'{ailment_i}/{len(ailments)} - {obj_i}/{remedies_num} - {obj}')
            key = 'preparation_desc'
            if key not in obj: obj[key] = ''
            # obj[key] = ''
            if obj[key] == '':
                preparation_name = obj['preparation_name']
                prompt = f'''
                    Write a detailed paragraph explaining why herbal {preparation_name} is good for {ailment_name}.
                    Use simple and short words, and a simple writing style.
                    Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                '''
                reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
                obj[key] = reply
                json_write(json_filepath, data)

        key = 'supplementary_avoid'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies'][:3]]
            prompt = f'''
                Write a detailed paragraph explaining what herbs to avoid if you have {ailment_name} and why.
                Never include the following herbs: {herbs_names}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        ########################################
        # ;html
        ########################################
        title = data['title']
        print(title)

        article_html = ''

        article_html += f'<h1>{title}</h1>\n'
        obj = data['remedies'][remedies_num-1]
        herb_name_scientific = obj['herb_name_scientific']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
        out = f'website-2/images/herbs/{herb_slug}-plant.jpg'
        src = f'/images/herbs/{herb_slug}-plant.jpg'
        if os.path.exists(out):
            article_html += f'<img src="{src}">\n'
        article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'
        article_html += f'<p>The following article lists the main herbal remedies used to treat {ailment_name}.</p>\n'

        # causes
        sub_title = f'What are the main causes of {ailment_name}?'.title()
        article_html += f'<h2>{sub_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["causes_intro_desc"])}\n'
        article_html += f'<p>Below are the main causes of {ailment_name}.</p>\n'
        article_html += f'<ul>\n'
        for obj_i, obj in enumerate(data['causes'][:causes_num]):
            cause_name = obj['cause_name']
            cause_desc = obj['cause_desc']
            article_html += f'<li><strong>{cause_name}</strong>: {cause_desc}</li>\n'
        article_html += f'</ul>\n'

        sub_title = f'{remedies_num} herbs for {ailment_name}'.title()
        article_html += f'<h2>{sub_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["remedies_intro_desc"])}\n'
        article_html += f'<p>Below are {remedies_num} healing hebs for {ailment_name}.</p>\n'
        for obj_i, obj in enumerate(data['remedies'][:remedies_num]):
            herb_name_scientific = obj['herb_name_scientific']
            herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
            remedy_desc = obj['remedy_desc']
            article_html += f'<h3>{obj_i+1}. {herb_name_scientific}</h3>\n'
            out = f'website-2/images/herbs/{herb_slug}-plant.jpg'
            src = f'/images/herbs/{herb_slug}-plant.jpg'
            if os.path.exists(out):
                article_html += f'<img src="{src}">\n'
            article_html += f'{util.text_format_1N1_html(remedy_desc)}\n'

        sub_title = f'{preparations_num} herbal preparations for {ailment_name}'.title()
        article_html += f'<h2>{sub_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["preparations_intro_desc"])}\n'
        article_html += f'<p>Below are {preparations_num} effective hebal preparations for {ailment_name}.</p>\n'
        for obj_i, obj in enumerate(data['preparations'][:preparations_num]):
            preparation_name = obj['preparation_name']
            preparation_desc = obj['preparation_desc']
            preparation_slug_2 = preparation_name.strip().lower().replace(' ', '-') + 's'
            article_html += f'<h3>{obj_i+1}. {preparation_name}</h3>\n'
            out = f'website-2/images/preparations/{ailment_slug}-herbal-{preparation_slug_2}.jpg'
            src = f'/images/preparations/{ailment_slug}-herbal-{preparation_slug_2}.jpg'
            if os.path.exists(out):
                article_html += f'<img src="{src}">\n'
            article_html += f'{util.text_format_1N1_html(preparation_desc)}\n'

        # supplementary avoid
        sub_title = f'What herbs to avoid if you have {ailment_name}?'.title()
        article_html += f'<h2>{sub_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["supplementary_avoid"])}\n'

        head_html = head_html_generate(title, '/style-article.css')
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                <main class="container-md">
                    {article_html}
                </main>
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)
        print(f'\n')
        print(html_filepath)
        # quit()

def articles_titles_check(preparation_slug):
    plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    preparation_name = preparation_slug.replace('-', ' ')
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    while 1:
        for ailment_i, ailment in enumerate(ailments):
            system_slug = ailment['system_slug']
            organ_slug = ailment['organ_slug']
            ailment_slug = ailment['ailment_slug']
            ailment_name = ailment['ailment_name']
            url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
            json_filepath = f'database/json/{url}.json'
            html_filepath = f'{website_folderpath}/{url}.html'
            if not os.path.exists(f'{website_folderpath}/remedies'): os.mkdir(f'{website_folderpath}/remedies')
            if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system'): os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system')
            if not os.path.exists(f'{website_folderpath}/remedies/{system_slug}-system/{ailment_slug}'): os.mkdir(f'{website_folderpath}/remedies/{system_slug}-system/{ailment_slug}')

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
            
            print(f'{ailment_i}. {data["title"]}')

        '''
        valid = input('>> (x/v)')
        if valid == 'x':
            if os.path.exists(json_filepath): os.remove(json_filepath)
        '''
        break

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

        json_write(json_filepath, data)

        key = 'audience'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            outputs = []
            for i in range(5):
                print(f'AUDIENCE: {ailment_i}/{len(ailments)} - {i}: {ailment}')
                rand_num = random.randint(7, 13)
                prompt = f'''
                    Write a list of (rand_num) names of types of people who are most likely affected by the following problem and most likely benefit from solving it: {ailment_name}.
                    Also, for each name give a confidence score from 1 to 10, indicating how sure you are about that name.
                    Write only the names, don't add descriptions.
                    Write the types using as few words as possible.
                    Neve include the word "people".
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"name": "name 1", "confidence_score": "10"}}, 
                        {{"name": "name 2", "confidence_score": "5"}}, 
                        {{"name": "name 3", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    _objs = []
                    for item in json_data:
                        try: name = item['name']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        _objs.append({
                            "name": name.lower().strip(), 
                            "score": score,
                        })
                    for _obj in _objs:
                        name = _obj['name']
                        score = _obj['score']
                        found = False
                        for output in outputs:
                            if name in output['audience_name']: 
                                output['audience_mentions'] += 1
                                output['audience_confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            outputs.append({
                                'audience_name': name, 
                                'audience_mentions': 1, 
                                'audience_confidence_score': int(score), 
                            })
            outputs_final = []
            for output in outputs:
                outputs_final.append({
                    'audience_name': output['audience_name'],
                    'audience_mentions': int(output['audience_mentions']),
                    'audience_confidence_score': int(output['audience_confidence_score']),
                    'audience_total_score': int(output['audience_mentions']) * int(output['audience_confidence_score']),
                })
            outputs_final = sorted(outputs_final, key=lambda x: x['audience_confidence_score'], reverse=True)
            print('***********************')
            print('***********************')
            print('***********************')
            for output in outputs_final:
                print(output)
            print('***********************')
            print('***********************')
            print('***********************')
            rand_output = random.choice(outputs_final[:5])
            data[key] = rand_output
            json_write(json_filepath, data)

        if 'title' not in data: data['title'] = ''
        # data['title'] = ''
        if data['title'] == '':
            prompt = f'''
                Write a numbered list of 10 titles for a listicle (list article) using the data below.
                problem: {data["ailment_name"]}.
                remedies: herbal {data["preparation_name"]}.
                remedies number: {data["remedies_num"]}.
                target audience: {data["audience"]["audience_name"]}.
                Write only the titles.
                Always write the remedies in plural form, for example write "teas" instead of "tea".
                Always include the problem, remedies, remedies number and target audience in each title.
                An example of title could be: {data['remedies_num']} {data['preparation_name']} for {data['audience']['audience_name']} with {data['ailment_name']}
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '. ' not in line: continue
                line = '. '.join(line.split('. ')[1:])
                line = line.replace('*', '')
                if line.endswith('.'): line = line[:-1]
                line = line.strip()
                if line == '': continue
                lines.append(line)
            line = random.choice(lines)
            data['title'] = line
            json_write(json_filepath, data)

        key = 'remedies'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            output_plants = []
            for i in range(5):
                print(f'{ailment_i}/{len(ailments)} - {i}: {ailment}')
                prompt = f'''
                    List the best herbs to make herbal {preparation_name} to relieve {ailment_name} for {data["audience"]}.
                    Also, for each herb name give a confidence score from 1 to 10, indicating how sure you are that herbal {preparation_name} made with that herb is effective to relieve {ailment_name}.
                    Write only the scientific names (botanical names) of the plants used for the preparation, don't add descriptions or common names.
                    Write the names of the plants using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"herb_name_scientific": "scientific name of herb 1 used for preparation", "confidence_score": "10"}}, 
                        {{"herb_name_scientific": "scientific name of herb 2 used for preparation", "confidence_score": "5"}}, 
                        {{"herb_name_scientific": "scientific name of herb 3 used for preparation", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names_scientific = []
                    for item in json_data:
                        try: line = item['herb_name_scientific']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        print(line)
                        for plant in plants_wcvp:
                            name_scientific = plant['scientfiicname']
                            if name_scientific.lower().strip() in line.lower().strip():
                                if len(name_scientific.split(' ')) > 1:
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    print(name_scientific)
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    names_scientific.append({
                                        "name": name_scientific, 
                                        "score": score,
                                    })
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
                            print(name, '->', output_plant['herb_name_scientific'])
                            if name in output_plant['herb_name_scientific']: 
                                output_plant['herb_mentions'] += 1
                                output_plant['herb_confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            output_plants.append({
                                'herb_name_scientific': name, 
                                'herb_mentions': 1, 
                                'herb_confidence_score': int(score), 
                            })
                output_plants_final = []
                for output_plant in output_plants:
                    output_plants_final.append({
                        'herb_name_scientific': output_plant['herb_name_scientific'],
                        'herb_mentions': int(output_plant['herb_mentions']),
                        'herb_confidence_score': int(output_plant['herb_confidence_score']),
                        'herb_total_score': int(output_plant['herb_mentions']) * int(output_plant['herb_confidence_score']),
                    })
                output_plants_final = sorted(output_plants_final, key=lambda x: x['herb_confidence_score'], reverse=True)
                print('***********************')
                print('***********************')
                print('***********************')
                for output_plant in output_plants_final:
                    print(output_plant)
                print('***********************')
                print('***********************')
                print('***********************')
                data[key] = output_plants_final[:remedies_num]
                json_write(json_filepath, data)

        # remedies desc
        for remedy_i, obj in enumerate(data['remedies']):
            print(f'{ailment_i}/{len(ailments)} - {remedy_i} - {preparation_name} - {obj}')
            key = 'remedy_desc'
            if key not in obj: obj[key] = ''
            # obj[key] = ''
            if obj[key] == '':
                herb_name = obj['herb_name_scientific']
                prompt = f'''
                    Write a detailed paragraph explaining why {herb_name} {preparation_name} is good for {ailment_name}.
                    Include the boiactive constituents and the properties.
                    Use simple and short words, and a simple writing style.
                    Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                '''
                prompt = f'''
                    Write a detailed paragraph about {herb_name} {preparation_name} for {ailment_name}.
                    In this paragraph, explain the following.
                    1. why {herb_name} {preparation_name} helps with {ailment_name}. Include properties and constituents.
                    2. specific advice on what actions to take.
                    3. what are the likely outcomes to occur from taking action.
                    Use simple and short words, and a simple writing style.
                    Use a conversational and fluid writing style.
                    Don't write fluff.
                    Don't allucinate.
                    Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                    Start with the following words: {herb_name} {preparation_name} .
                '''
                reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
                obj[key] = reply
                json_write(json_filepath, data)


        # intro desc
        key = 'intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies']]
            prompt = f'''
                Write a detailed paragraph about: herbal {data["preparation_name"]} for {data["ailment_name"]} in {data["audience"]["audience_name"].lower()}.
                Start by explaining why {data["audience"]["audience_name"].lower()} can suffer from {data["ailment_name"]} and how this affects their lives.
                End by giving a very brief overview on why herbal {data["preparation_name"]} helps {data["audience"]["audience_name"].lower()} treat {data["ailment_name"]}.
                Never mention names of herbs.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        # ;images
        if 1:
            non_valid_preparations = [
                'decoctions',
            ]
            if preparation_slug not in non_valid_preparations:
                output_filepath = f'{website_folderpath}/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg'
                src = f'/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg'
                alt = f'herbal {preparation_name} for {ailment_name}'
                herbs_names_scientific = [x['herb_name_scientific'] for x in data["remedies"][:remedies_num]]
                herb_name_scientific = random.choice(herbs_names_scientific)
                # if not os.path.exists(output_filepath):
                if True:
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
                        text, watermark 
                    '''
                    print(prompt)
                    pipe_init()
                    image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                    image = img_resize(image, w=768, h=768)
                    image.save(output_filepath)
                data['intro_image_src'] = src
                data['intro_image_alt'] = alt
                json_write(json_filepath, data)

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
                            text, watermark 
                        '''
                        print(prompt)
                        pipe_init()
                        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                        image = img_resize(image, w=768, h=768)
                        image.save(output_filepath)
                    remedy['image_src'] = src
                    remedy['image_alt'] = alt
                    json_write(json_filepath, data)


        ########################################
        # ;html
        ########################################
        title = data['title']
        print(title)

        article_html = ''

        article_html += f'<h1>{title}</h1>\n'
        article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'

        for remedy_i, remedy in enumerate(data['remedies']):
            article_html += f'<h2>{remedy_i+1}. {remedy["herb_name_scientific"]}</h2>\n'
            src = remedy['image_src']
            alt = remedy['image_alt']
            article_html += f'<img src="{src}" alt="{alt}">\n'
            article_html += f'{util.text_format_1N1_html(remedy["remedy_desc"])}\n'

        head_html = head_html_generate(title, '/style-article.css')
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                <main class="container-md">
                    {article_html}
                </main>
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)
        print(f'\n')
        print(html_filepath)

        # quit()



def articles_preparations(preparation_slug):
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
        data['status_slug'] = ailment_slug
        data['status_name'] = ailment_name
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

        if 'title' not in data: data['title'] = ''
        # data['title'] = ''
        if data['title'] == '':
            prompt = f'''
                Rewrite the following title in 10 different ways: {data["remedies_num"]} best herbal {preparation_name} for {ailment_name}.
                Write only the titles.
                Include the followin words in each title: {ailment_name}.
            '''
            reply = llm_reply(prompt)
            lines = []
            for line in reply.split('\n'):
                line = line.strip()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '. ' not in line: continue
                line = '. '.join(line.split('. ')[1:])
                line = line.replace('*', '')
                if line.endswith('.'): line = line[:-1]
                line = line.strip()
                if line == '': continue
                lines.append(line)
            line = random.choice(lines)
            data['title'] = line
            json_write(json_filepath, data)

        if 0:
            key = 'remedies'
            if key in data: del data[key]
            json_write(json_filepath, data)
            continue

        ## ------------------------------------
        key = 'remedies'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            output_plants = []
            for i in range(20):
                print(f'{ailment_i}/{len(ailments)} - {i}/20: {ailment}')
                prompt = f'''
                    List the best herbs to make herbal {preparation_name} to relieve {ailment_name}.
                    Also, for each herb name give a confidence score from 1 to 10, indicating how sure you are that herbal {preparation_name} made with that herb is effective to relieve {ailment_name}.
                    Write only the scientific names (botanical names) of the plants used for the preparation, don't add descriptions or common names.
                    Write the names of the plants using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"herb_name_scientific": "scientific name of herb 1 used for preparation", "confidence_score": "10"}}, 
                        {{"herb_name_scientific": "scientific name of herb 2 used for preparation", "confidence_score": "5"}}, 
                        {{"herb_name_scientific": "scientific name of herb 3 used for preparation", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names_scientific = []
                    for item in json_data:
                        try: line = item['herb_name_scientific']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        print(line)
                        for plant in plants_wcvp:
                            name_scientific = plant['scientfiicname']
                            if name_scientific.lower().strip() in line.lower().strip():
                                if len(name_scientific.split(' ')) > 1:
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    print(name_scientific)
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    names_scientific.append({
                                        "name": name_scientific, 
                                        "score": score,
                                    })
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
                            print(name, '->', output_plant['herb_name_scientific'])
                            if name in output_plant['herb_name_scientific']: 
                                output_plant['herb_mentions'] += 1
                                output_plant['herb_confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            output_plants.append({
                                'herb_name_scientific': name, 
                                'herb_mentions': 1, 
                                'herb_confidence_score': int(score), 
                            })
                output_plants_final = []
                for output_plant in output_plants:
                    output_plants_final.append({
                        'herb_name_scientific': output_plant['herb_name_scientific'],
                        'herb_mentions': int(output_plant['herb_mentions']),
                        'herb_confidence_score': int(output_plant['herb_confidence_score']),
                        'herb_total_score': int(output_plant['herb_mentions']) * int(output_plant['herb_confidence_score']),
                    })
                output_plants_final = sorted(output_plants_final, key=lambda x: x['herb_confidence_score'], reverse=True)
                print('***********************')
                print('***********************')
                print('***********************')
                for output_plant in output_plants_final:
                    print(output_plant)
                print('***********************')
                print('***********************')
                print('***********************')
                data[key] = output_plants_final[:remedies_num]
                json_write(json_filepath, data)

        for obj in data['remedies']:
            herb_name_scientific = obj['herb_name_scientific']
            key = 'remedy_constituents'
            if key not in obj: obj[key] = ''
            # obj[key] = ''
            if obj[key] == '':
                outputs = []
                for i in range(20):
                    print(f'{ailment_i}/{len(ailments)} - {i}/20: {ailment}')
                    prompt = f'''
                        List the best medicinal constituents of {herb_name_scientific} herbal {preparation_name} to relieve {ailment_name}.
                        Example of medicinal constituents are: flavonoinds, tannins, polyphenols, etc.
                        Also, for each constituent give a confidence score from 1 to 10, indicating how sure you are that constituent is effective to relieve {ailment_name}.
                        Write only the names of the constituents, don't add descriptions.
                        Write the names of the constituents using as few words as possible.
                        Don't write fluff, only proven facts.
                        Don't allucinate.
                        Reply in the following JSON format: 
                        [
                            {{"constituent_name": "name of constituent 1", "confidence_score": "10"}}, 
                            {{"constituent_name": "name of constituent 2", "confidence_score": "5"}}, 
                            {{"constituent_name": "name of constituent 3", "confidence_score": "7"}} 
                        ]
                        Only reply with the JSON, don't add additional info.
                    '''
                    reply = llm_reply(prompt, model).strip()
                    json_data = {}
                    try: json_data = json.loads(reply)
                    except: pass 
                    if json_data != {}:
                        _objs = []
                        for item in json_data:
                            try: name = item['constituent_name']
                            except: continue
                            try: score = item['confidence_score']
                            except: continue
                            _objs.append({
                                "name": name, 
                                "score": score,
                            })
                        for _obj in _objs:
                            name = _obj['name']
                            score = _obj['score']
                            found = False
                            for output in outputs:
                                # print(output)
                                # print(name, '->', output['constituent_name'])
                                if name in output['constituent_name']: 
                                    output['constituent_mentions'] += 1
                                    output['constituent_confidence_score'] += int(score)
                                    found = True
                                    break
                            if not found:
                                outputs.append({
                                    'constituent_name': name, 
                                    'constituent_mentions': 1, 
                                    'constituent_confidence_score': int(score), 
                                })
                outputs_final = []
                for output in outputs:
                    outputs_final.append({
                        'constituent_name': output['constituent_name'],
                        'constituent_mentions': int(output['constituent_mentions']),
                        'constituent_confidence_score': int(output['constituent_confidence_score']),
                        'constituent_total_score': int(output['constituent_mentions']) * int(output['constituent_confidence_score']),
                    })
                outputs_final = sorted(outputs_final, key=lambda x: x['constituent_confidence_score'], reverse=True)
                print('***********************')
                print('***********************')
                print('***********************')
                for output in outputs_final:
                    print(output)
                print('***********************')
                print('***********************')
                print('***********************')
                rand_outputs = random.randint(3, 5)
                obj[key] = outputs_final[:rand_outputs]
                json_write(json_filepath, data)
    
        ####################################################################
        # ;json content
        ####################################################################
        
        key = 'intro_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies'][:2]]
            prompt = f'''
                Write a detailed paragraph explaining why herbal {preparation_name} is good for {ailment_name}.
                Include the following herbs and expalin why they are good: {herbs_names}.
                Explain why it's important to fix the issue above mentioned and how can improve your life.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)
    

        if 0:
            for obj in data['remedies'][:remedies_num]:
                key = 'remedy_desc'
                if key in obj: del obj[key]
                json_write(json_filepath, data)
            continue

        for remedy_i, obj in enumerate(data['remedies'][:remedies_num]):
            print(f'{ailment_i}/{len(ailments)} - {remedy_i}/{remedies_num} - {preparation_name} - {obj}')
            key = 'remedy_desc'
            if key not in obj: obj[key] = ''
            # obj[key] = ''
            if obj[key] == '':
                herb_name = obj['herb_name_scientific']
                prompt = f'''
                    Write a detailed paragraph explaining why {herb_name} {preparation_name} is good for {ailment_name}.
                    Use simple and short words, and a simple writing style.
                    Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
                '''
                reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
                obj[key] = reply
                json_write(json_filepath, data)

        # remedy constituents desc
        for remedy_i, remedy in enumerate(data['remedies'][:remedies_num]):
            print(f'{ailment_i}/{len(ailments)} - {remedy_i}/{remedies_num} - {preparation_name} - {obj}')
            herb_name_scientific = obj['herb_name_scientific']
            constituents = remedy['remedy_constituents']
            for constituent_i, constituent in enumerate(constituents):
                print(f'{ailment_i}/{len(ailments)} - {remedy_i}/{remedies_num} - {constituent_i}/{len(constituents)} - {preparation_name}')
                key = 'constituent_desc'
                if key not in constituent: constituent[key] = ''
                # constituent[key] = ''
                if constituent[key] == '':
                    constituent_name = constituent['constituent_name']
                    prompt = f'''
                        Write 1 detailed sentence explaining why the bioactive compound {constituent_name} in {herb_name_scientific} is/are good for {ailment_name}.
                        Use simple and short words, and a simple writing style.
                        Start the reply with the following words: {constituent_name.capitalize()} in {herb_name_scientific.capitalize} .
                    '''
                    reply = llm_reply(prompt).strip().replace('\n', ' ').replace('  ', ' ')
                    reply = reply.replace(f' in {herb_name_scientific.capitalize()}', '')
                    constituent[key] = reply
                    json_write(json_filepath, data)

        # remedy preparation
        for remedy_i, remedy in enumerate(data['remedies'][:remedies_num]):
            print(f'{ailment_i}/{len(ailments)} - {remedy_i}/{remedies_num} - {preparation_name} - {obj}')
            herb_name_scientific = obj['herb_name_scientific']
            key = 'remedy_preparation'
            if key not in remedy: remedy[key] = ''
            # remedy[key] = ''
            if remedy[key] == '':
                prompt = f'''
                    Write 1 detailed paragraph explaining how to make {herb_name_scientific} herbal {preparation_name} that help with {ailment_name}.
                    Reply in paragraph format, don't use lists.
                    Use simple and short words, and a simple writing style.
                '''
                reply = llm_reply(prompt).strip()
                reply = [line.strip() for line in reply.split('\n')]
                reply = ' '.join(reply)
                remedy[key] = reply
                json_write(json_filepath, data)

        # what is the best combination of herbal teas for dry hair?
        key = 'supplementary_best'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies']]
            prompt = f'''
                Write a detailed paragraph explaining what is the best combination of herbal {preparation_name} to remedy {ailment_name} and explain why that combination is the best. 
                Only choose from the following herbs: {herbs_names}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        # what herbal teas to avoid for dry hair?
        key = 'supplementary_avoid'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies']]
            prompt = f'''
                Write a detailed paragraph explaining what herbal {preparation_name} you should avoid if you have {ailment_name} and explain why. 
                Don't mention the following herbs: {herbs_names}.
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        # complementary natural remedies for dry hair?
        key = 'supplementary_other_remedies'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies']]
            prompt = f'''
                Write a detailed paragraph explaining what other natural remedies except from herbal {preparation_name} that can help with {ailment_name} and explain why. 
                Use simple and short words, and a simple writing style.
                Don't write lists.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)
    
        # related ailments you can eliminate with herbal teas?
        key = 'supplementary_related_ailments'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            herbs_names = [x['herb_name_scientific'] for x in data['remedies']]
            prompt = f'''
                Write a detailed paragraph explaining what other ailments people who have {ailment_name} are likely to experience that can be healed with medicinal herbs and explain why. 
                Use simple and short words, and a simple writing style.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)
    
        '''
        '''

        ########################################
        # ;images
        ########################################
        if 1:
            non_valid_preparations = [
                'decoctions',
            ]
            if preparation_slug not in non_valid_preparations:
                output_filepath = f'{website_folderpath}/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg'
                src = f'/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg'
                alt = f'herbal {preparation_name} for {ailment_name}'
                herbs_names_scientific = [x['herb_name_scientific'] for x in data["remedies"][:remedies_num]]
                herb_name_scientific = random.choice(herbs_names_scientific)
                if not os.path.exists(output_filepath):
                    prompt = f'''
                        {herb_name_scientific} herbal {preparation_name},
                        close-up,
                        on a wooden table,
                        surrounded by herbs,
                        window,
                        soft light,
                        neutral color palette,
                        vintage, 
                        indoor,
                        depth of field, bokeh,
                        high resolution
                    ''' 
                    negative_prompt = f'''
                        text, watermark 
                    '''
                    print(prompt)
                    pipe_init()
                    image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                    image = img_resize(image, w=768, h=768)
                    image.save(output_filepath)
                data['intro_image_src'] = src
                data['intro_image_alt'] = alt
                json_write(json_filepath, data)

                for remedy_i, remedy in enumerate(data['remedies'][:remedies_num]):
                    herb_name_scientific = remedy['herb_name_scientific']
                    herb_slug = herb_name_scientific.strip().lower().replace(' ', '-')
                    output_filepath = f'{website_folderpath}/images/preparations/{preparation_slug}/{herb_slug}-herbal-{preparation_slug}.jpg'
                    src = f'/images/preparations/{preparation_slug}/{herb_slug}-herbal-{preparation_slug}.jpg'
                    alt = f'{herb_name_scientific} herbal {preparation_name} for {ailment_name}'
                    if not os.path.exists(output_filepath):
                        prompt = f'''
                            {herb_name_scientific} herbal {preparation_name},
                            on a wooden table surrounded by medicinal herbs,
                            window, 
                            daylight, natural light, soft light,
                            neutral color palette, neutral colors, earth tones,
                            indoor,
                            depth of field,
                            high resolution,
                            cinematic
                        '''
                        negative_prompt = f'''
                            text, watermark 
                        '''
                        print(prompt)
                        pipe_init()
                        image = pipe(prompt=prompt, negative_prompt=negative_prompt, width=1024, height=1024, num_inference_steps=30, guidance_scale=7.0).images[0]
                        image = img_resize(image, w=768, h=768)
                        image.save(output_filepath)
                    remedy['image_src'] = src
                    remedy['image_alt'] = alt
                    json_write(json_filepath, data)
                    

        ########################################
        # ;html
        ########################################
        title = data['title']
        print(title)

        article_html = ''

        article_html += f'<h1>{title}</h1>\n'
        # article_html += f'<img src="{src_intro}" alt="{alt_intro}">\n'
        article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'
        for remedy_i, remedy in enumerate(data['remedies'][:remedies_num]):
            article_html += f'<h2>{remedy_i+1}. {remedy["herb_name_scientific"].title()}</h2>\n'
            article_html += f'{util.text_format_1N1_html(remedy["remedy_desc"])}\n'
            # src = remedy['image_src']
            # alt = remedy['image_alt']
            # article_html += f'<img src="{src}" alt="{alt}">\n'
            article_html += f'<ul>\n'
            for constituent in remedy['remedy_constituents']:
                constituent_name = constituent['constituent_name']
                constituent_desc = constituent['constituent_desc']
                article_html += f'<li>\n'
                article_html += f'<strong>{constituent_name}</strong>: {constituent_desc}\n'
                article_html += f'</li>\n'
            article_html += f'</ul>\n'
            remedy_preparation = remedy["remedy_preparation"]
            if "can't" not in remedy_preparation and "cannot" not in remedy_preparation:
                article_html += f'{util.text_format_1N1_html(remedy_preparation)}\n'
        # what is the best combination of herbal teas for dry hair?
        _title = f'what is the best combination of herbal {preparation_name} for {ailment_name}?'.lower().capitalize()
        article_html += f'<h2>{_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["supplementary_best"])}\n'
        # what herbal teas to avoid if you have dry hair?
        _title = f'what herbal {preparation_name} you should avoid if you have {ailment_name}?'.lower().capitalize()
        article_html += f'<h2>{_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["supplementary_avoid"])}\n'
        # complementary natural remedies for dry hair?
        _title = f'what other natural remedies you can use with herbal {preparation_name} for {ailment_name}?'.lower().capitalize()
        article_html += f'<h2>{_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["supplementary_other_remedies"])}\n'

        # related ailments you can eliminate with herbal teas?
        _title = f'what other ailments people who have {ailment_name} are likely to experience?'.lower().capitalize()
        article_html += f'<h2>{_title}</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["supplementary_related_ailments"])}\n'

        key = 'supplementary_related_ailments'

        head_html = head_html_generate(title, '/style-article.css')
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                <main class="container-md">
                    {article_html}
                </main>
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)
        print(f'\n')
        print(html_filepath)
        # quit()

def page_home():
    banner_html = f'''
        <section class="container-xl">
            <div class="banner">
                <h1 class="text-white">Healing Herbs to Improve Your Wellness</h1>
            </div>
        </section>
    '''
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    random.shuffle(ailments)
    teas_blocks_data = []
    for ailment_i, ailment in enumerate(ailments[:]):
        preparation_slug = 'teas'
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        image_url = f'/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg'
        data = json_read(json_filepath)
        title = data['title'].capitalize()
        intro_desc = ' '.join(data['intro_desc'].split(' ')[:32])
        teas_blocks_data.append({
            'href': f'/{url}.html',
            'url': f'{image_url}',
            'title': f'{title}',
            'intro_desc': f'{intro_desc}',
        })
    tinctures_blocks_data = []
    for ailment_i, ailment in enumerate(ailments[:]):
        preparation_slug = 'tinctures'
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        image_url = f'/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg'
        data = json_read(json_filepath)
        title = data['title'].capitalize()
        intro_desc = ' '.join(data['intro_desc'].split(' ')[:32])
        tinctures_blocks_data.append({
            'href': f'/{url}.html',
            'url': f'{image_url}',
            'title': f'{title}',
            'intro_desc': f'{intro_desc}',
        })
    creams_blocks_data = []
    for ailment_i, ailment in enumerate(ailments[:]):
        preparation_slug = 'creams'
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        image_url = f'/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg'
        data = json_read(json_filepath)
        title = data['title'].capitalize()
        creams_blocks_data.append({
            'href': f'/{url}.html',
            'url': f'{image_url}',
            'title': f'{title}',
        })
    essential_oils_blocks_data = []
    for ailment_i, ailment in enumerate(ailments[:]):
        preparation_slug = 'essential-oils'
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        image_url = f'/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg'
        data = json_read(json_filepath)
        title = data['title'].capitalize()
        essential_oils_blocks_data.append({
            'href': f'/{url}.html',
            'url': f'{image_url}',
            'title': f'{title}',
        })
    '''
        <section>
            <div class="container-xl mob-flex gap-48">
                <div class="flex-2">
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Popular Now</h2>
                    </div>
                </div>
            </div>
        </section>
    '''

    head_html = head_html_generate('the future of wellness is natural remedies', '/style.css')
    section_1 = f'''
        <section class="container-xl grid-container mb-48">
            <a class="no-underline bg-center bg-cover card-wide card-tall flex items-end pl-16 pb-16 pr-48" href="{teas_blocks_data[0]['href']}" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url({teas_blocks_data[0]['url']})">
                <div>
                    <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">
                        PREPARATIONS
                    </span>
                    <h2 class="text-white text-24 mb-16">
                        {teas_blocks_data[0]['title']}
                    </h2>
                    <p class="text-white">
                        Terrawhisper - 2024/10/14
                    </p>
                </div>
            </a>
            <a class="no-underline bg-center bg-cover card-wide flex items-end pl-16 pb-16 pr-48" href="{tinctures_blocks_data[1]['href']}" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url({tinctures_blocks_data[1]['url']})">
                <div>
                    <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">
                        PREPARATIONS
                    </span>
                    <h2 class="text-white text-24 mb-16">
                        {tinctures_blocks_data[1]['title']}
                    </h2>
                </div>
            </a>
            <a class="no-underline bg-center bg-cover flex items-end pl-16 pb-16 pr-48" href="{creams_blocks_data[2]['href']}" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url({creams_blocks_data[2]['url']})">
                <div>
                    <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">
                        PREPARATIONS
                    </span>
                    <h2 class="text-white text-16 mb-16">
                        {creams_blocks_data[2]['title']}
                    </h2>
                </div>
            </a>
            <a class="no-underline bg-center bg-cover flex items-end pl-16 pb-16 pr-48" href="{essential_oils_blocks_data[3]['href']}" style="background-image: linear-gradient(rgba(0, 0, 0, 0.0), rgba(0, 0, 0, 0.5)), url({essential_oils_blocks_data[3]['url']})">
                <div>
                    <span class="inline-block text-12 text-white bg-black uppercase mb-16 pl-8 pr-8 pt-4 pb-4">
                        PREPARATIONS
                    </span>
                    <h2 class="text-white text-16 mb-16">
                        {essential_oils_blocks_data[4]['title']}
                    </h2>
                </div>
            </a>
        </section>
    '''

    cards_html = ''
    for i in range(4):
        cards_html += f'''
            <a class="article-card no-underline text-black" href="{teas_blocks_data[i+5]['href']}">
                <div class="flex gap-16">
                    <div class="flex-2">
                        <img class="object-cover" height="80" src="{teas_blocks_data[i+5]['url']}">
                    </div>
                    <div class="flex-5">
                        <h3 class="text-14 mb-8">
                            {teas_blocks_data[i+5]['title']}
                        </h3>
                        <p class="text-12">
                            2024/10/14
                        </p>
                    </div>
                </div>
            </a>
        '''

    section_2 = f'''
        <section>
            <div class="container-xl flex mob-flex-col mb-48 gap-48">
                <div class="flex-2">
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Teas</h2>
                    </div>
                    <div class="flex mob-flex-col gap-48">
                        <div class="flex-1">
                            <a class="article-card no-underline text-black" href="{teas_blocks_data[4]['href']}">
                                <div class="relative mb-16">
                                    <img class="object-cover" height="240" src="{teas_blocks_data[4]['url']}">
                                </div>
                                <h3 class="text-20 font-normal mb-8">
                                    {teas_blocks_data[4]['title']}
                                </h3>
                                <p class="text-12 mb-16">
                                    <span class="font-bold text-black">Terrawhisper</span> - 2024/10/12
                                </p>
                                <p class="text-14 mb-0">
                                    {teas_blocks_data[4]['intro_desc']}
                                </p>
                            </a>
                        </div>
                        <div class="flex-1 flex flex-col gap-24">
                            {cards_html}
                        </div>
                    </div>
                </div>
                <div class="flex-1">
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Stay Connected</h2>
                    </div>
                    <div class="flex flex-col items-center">
                        <img src="images-static/leen-randell.jpg" class="avatar">
                        <p class="helvetica-bold">Leen Randell</p>
                        <div class="flex flex-col gap-16">
                            <a href="https://www.pinterest.com/terrawhisper" target="_blank" class="inline-block flex items-center gap-16 no-underline">
                                <img class="social-icon" src="images-static/pinterest.png">
                            </a>
                            <a href="https://www.x.com/leenrandell" target="_blank" class="inline-block flex items-center gap-16 no-underline">
                                <img class="social-icon" src="images-static/twitter.png">
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    '''

    section_3 = f'''
        <section>
            <div class="container-xl flex mob-flex-col mb-48 gap-48">
                <div class="flex-2">
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Tinctures</h2>
                    </div>
                    <div class="flex mob-flex-col gap-48">
                        <div class="flex-1 flex flex-col gap-24">
                            <div class="">
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[4]['href']}">
                                    <div class="relative mb-16">
                                        <img class="object-cover" height="240" src="{tinctures_blocks_data[4]['url']}">
                                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">tincture</p>
                                    </div>
                                    <h3 class="text-20 font-normal mb-8">
                                        {tinctures_blocks_data[4]['title']}
                                    </h3>
                                    <p class="text-12 mb-16">
                                        <span class="font-bold text-black">Terrawhisper</span> - 2024/10/12
                                    </p>
                                    <p class="text-14 mb-0">
                                        {tinctures_blocks_data[4]['intro_desc']}
                                    </p>
                                </a>
                            </div>
                            <div class="flex-1 flex flex-col gap-24">
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[5]['href']}">
                                    <div class="flex gap-16">
                                        <div class="flex-2">
                                            <img class="object-cover" height="80" src="{tinctures_blocks_data[5]['url']}">
                                        </div>
                                        <div class="flex-5">
                                            <h3 class="text-14 mb-8">
                                                {tinctures_blocks_data[5]['title']}
                                            </h3>
                                            <p class="text-12">2024/08/21</p>
                                        </div>
                                    </div>
                                </a>
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[6]['href']}">
                                    <div class="flex gap-16">
                                        <div class="flex-2">
                                            <img class="object-cover" height="80" src="{tinctures_blocks_data[6]['url']}">
                                        </div>
                                        <div class="flex-5">
                                            <h3 class="text-14 mb-8">
                                                {tinctures_blocks_data[6]['title']}
                                            </h3>
                                            <p class="text-12">2024/08/21</p>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>
                        <div class="flex-1 flex flex-col gap-24">
                            <div class="">
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[7]['href']}">
                                    <div class="relative mb-16">
                                        <img class="object-cover" height="240" src="{tinctures_blocks_data[7]['url']}">
                                        <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">tincture</p>
                                    </div>
                                    <h3 class="text-20 font-normal mb-8">
                                        {tinctures_blocks_data[7]['title']}
                                    </h3>
                                    <p class="text-12 mb-16">
                                        <span class="font-bold text-black">Terrawhisper</span> - 2024/10/12
                                    </p>
                                    <p class="text-14 mb-0">
                                        {tinctures_blocks_data[7]['intro_desc']}
                                    </p>
                                </a>
                            </div>
                            <div class="flex-1 flex flex-col gap-24">
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[8]['href']}">
                                    <div class="flex gap-16">
                                        <div class="flex-2">
                                            <img class="object-cover" height="80" src="{tinctures_blocks_data[8]['url']}">
                                        </div>
                                        <div class="flex-5">
                                            <h3 class="text-14 mb-8">
                                                {tinctures_blocks_data[8]['title']}
                                            </h3>
                                            <p class="text-12">2024/08/21</p>
                                        </div>
                                    </div>
                                </a>
                                <a class="article-card no-underline text-black" href="{tinctures_blocks_data[9]['href']}">
                                    <div class="flex gap-16">
                                        <div class="flex-2">
                                            <img class="object-cover" height="80" src="{tinctures_blocks_data[9]['url']}">
                                        </div>
                                        <div class="flex-5">
                                            <h3 class="text-14 mb-8">
                                                {tinctures_blocks_data[9]['title']}
                                            </h3>
                                            <p class="text-12">2024/08/21</p>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="flex-1">
                    <div>
                        <div class="border-0 border-b-4 border-solid border-black mb-24">
                            <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">creams</h2>
                        </div>
                        <div class="flex flex-col gap-24">
                            <div class="flex mob-flex-col gap-24">
                                <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{creams_blocks_data[4]['href']}">
                                    <div class="">
                                        <div class="relative mb-16">
                                            <img class="object-cover" height="180" src="{creams_blocks_data[4]['url']}">
                                            <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">creams</p>
                                        </div>
                                        <h3 class="text-14 mb-8">
                                            {creams_blocks_data[4]['title']}
                                        </h3>
                                    </div>
                                </a>
                                <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{creams_blocks_data[5]['href']}">
                                    <div class="">
                                        <div class="relative mb-16">
                                            <img class="object-cover" height="180" src="{creams_blocks_data[5]['url']}">
                                            <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">creams</p>
                                        </div>
                                        <h3 class="text-14 mb-8">
                                            {creams_blocks_data[5]['title']}
                                        </h3>
                                    </div>
                                </a>
                            </div>
                            <div class="flex mob-flex-col gap-24">
                                <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{creams_blocks_data[6]['href']}">
                                    <div class="">
                                        <div class="relative mb-16">
                                            <img class="object-cover" height="180" src="{creams_blocks_data[6]['url']}">
                                            <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">creams</p>
                                        </div>
                                        <h3 class="text-14 mb-8">
                                            {creams_blocks_data[6]['title']}
                                        </h3>
                                    </div>
                                </a>
                                <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{creams_blocks_data[7]['href']}">
                                    <div class="">
                                        <div class="relative mb-16">
                                            <img class="object-cover" height="180" src="{creams_blocks_data[7]['url']}">
                                            <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">creams</p>
                                        </div>
                                        <h3 class="text-14 mb-8">
                                            {creams_blocks_data[7]['title']}
                                        </h3>
                                    </div>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    '''
    
    section_4 = f'''
        <section>
            <div class="container-xl mob-flex mb-48 gap-48">
                <div class="flex-2">
                    <div class="border-0 border-b-4 border-solid border-black mb-24">
                        <h2 class="text-16 font-normal uppercase bg-black text-white pl-16 pr-16 pt-8 pb-4 inline-block">Essential Oils</h2>
                    </div>
                    <div class="flex mob-flex-col gap-24">
                        <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{essential_oils_blocks_data[4]['href']}">
                            <div class="">
                                <div class="relative mb-16">
                                    <img class="object-cover" height="180" src="{essential_oils_blocks_data[4]['url']}">
                                    <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">essential oils</p>
                                </div>
                                <h3 class="text-14 mb-8">
                                    {essential_oils_blocks_data[4]['title']}
                                </h3>
                            </div>
                        </a>
                        <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{essential_oils_blocks_data[5]['href']}">
                            <div class="">
                                <div class="relative mb-16">
                                    <img class="object-cover" height="180" src="{essential_oils_blocks_data[5]['url']}">
                                    <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">essential oils</p>
                                </div>
                                <h3 class="text-14 mb-8">
                                    {essential_oils_blocks_data[5]['title']}
                                </h3>
                            </div>
                        </a>
                        <a class="article-card no-underline flex-1 flex flex-col gap-24 text-black" href="{essential_oils_blocks_data[6]['href']}">
                            <div class="">
                                <div class="relative mb-16">
                                    <img class="object-cover" height="180" src="{essential_oils_blocks_data[6]['url']}">
                                    <p class="absolute bottom-0 text-12 bg-black text-white pl-8 pr-8 pt-2 pb-2">essential oils</p>
                                </div>
                                <h3 class="text-14 mb-8">
                                    {essential_oils_blocks_data[6]['title']}
                                </h3>
                            </div>
                        </a>
                    </div>
                </div>
                <div class="flex-1">
                </div>
            </div>
        </section>
    '''

    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            <main>
                {section_1}
                {section_2}
                {section_3}
                {section_4}
            </main>
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    html_filepath = f'{website_folderpath}/index.html'
    with open(html_filepath, 'w') as f: f.write(html)

def page_systems():
    systems = [
        'cardiovascular',
        'digestive',
        'endocrine',
        'immune',
        'integumentary',
        'lymphatic',
        'musculoskeletal',
        'nervous',
        'reproductive',
        'respiratory',
        'urinary',
    ]
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    data = []
    for ailment in ailments:
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_name = ailment['ailment_name']
        ailment_slug = ailment['ailment_slug']

        found = False
        for obj in data:
            if obj['system_slug'] == system_slug:
                found = True
                obj['ailments_slugs'].append(ailment_slug)
                break
        if not found:
            data.append({
                'system_slug': system_slug,
                'ailments_slugs': [ailment_slug],
            })

    for obj in data:
        system_slug = obj['system_slug']
        system_name = system_slug.capitalize()
        section_1 = f'''
            <section class="mt-64 mb-64">
                <div class="container-xl text-center">
                    <h1>{system_name} System's Ailments</h1>
                    <p class="container-md">Different herbs improve different body systems. Select the body system you want to improve with natural remedies by clicking one of thm links below. When you'll click the selected link, you'll navigate to that particular body system page. In that page you'll find a list of common ailments you can relieve with herbalism.</p>
                </div>
            </section>
        '''
        cards = []
        for ailment_slug in obj["ailments_slugs"]:
            url = f'remedies/{system_slug}-system/{ailment_slug}'
            json_filepath = f'database/json/{url}.json'
            data = json_read(json_filepath)
            src = data['intro_image_src']
            title = data['title']
            lastmod = data['lastmod']
            year, month, day = lastmod.split('-')
            month = int(month)
            if month == 1: month = "GEN"
            if month == 2: month = "FEB"
            if month == 3: month = "MAR"
            if month == 4: month = "APR"
            if month == 5: month = "MAY"
            if month == 6: month = "JUN"
            if month == 7: month = "JUL"
            if month == 8: month = "AUG"
            if month == 9: month = "SEP"
            if month == 10: month = "OCT"
            if month == 11: month = "NOV"
            if month == 12: month = "DEC"
            lastmod_format = f'{month.capitalize()} {day}, {year}'
            card = f'''
                <a class="article-card no-underline text-black" href="/remedies/{system_slug}-system/{ailment_slug}.html">
                    <div class="">
                        <img class="mb-16" src="{src}">
                        <h2 class="text-18 mb-12">{title}</h2>
                        <p class="text-14">{lastmod_format}</p>
                    </div>
                </a>
            '''
            cards.append(card)
        cards = ''.join(cards)
        system_slug = obj['system_slug']
        system_name = system_slug.lower().strip().replace('-', ' ')
        head_html = head_html_generate(f'{system_name} ailments', '/style.css')
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {header_html}
                <main>
                    {section_1}
                    <section>
                        <div class="container-xl">
                            <div class="grid-container-2">
                                {cards}
                            </div>
                        </div>
                    </section>
                </main>
                <div class="mt-64"></div>
                {footer_html}
            </body>
            </html>
        '''
        html_filepath = f'{website_folderpath}/remedies/{system_slug}-system.html'
        with open(html_filepath, 'w') as f: f.write(html)

def page_remedies():
    section_1 = f'''
        <section class="mt-64 mb-64">
            <div class="container-xl text-center">
                <h1>Herbal Remedies by Body System</h1>
                <p class="container-md">Different herbs improve different body systems. Select the body system you want to improve with natural remedies by clicking one of thm links below. When you'll click the selected link, you'll navigate to that particular body system page. In that page you'll find a list of common ailments you can relieve with herbalism.</p>
            </div>
        </section>
    '''
    plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    systems = [
        'cardiovascular',
        'digestive',
        'endocrine',
        'immune',
        'integumentary',
        'lymphatic',
        'musculoskeletal',
        'nervous',
        'reproductive',
        'respiratory',
        'urinary',
    ]
    sections = []
    for i, system_name in enumerate(systems):
        system_slug = system_name.strip().lower().replace(' ', '-')
        url = f'remedies'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        data = json_read(json_filepath, create=True)

        key = f'{system_slug}_system_herbs'
        if key not in data: data[key] = []
        # data[key] = []
        if data[key] == []:
            output_plants = []
            for i in range(20):
                prompt = f'''
                    List the best herbs that are good for the {system_name} system.
                    Also, for each herb name give a confidence score from 1 to 10, indicating how sure you are that is good for the {system_name} system.
                    Write only the scientific names (botanical names) of the plants used for the preparation, don't add descriptions or common names.
                    Write the names of the plants using as few words as possible.
                    Don't write fluff, only proven facts.
                    Don't allucinate.
                    Reply in the following JSON format: 
                    [
                        {{"herb_name_scientific": "scientific name of herb 1 used for preparation", "confidence_score": "10"}}, 
                        {{"herb_name_scientific": "scientific name of herb 2 used for preparation", "confidence_score": "5"}}, 
                        {{"herb_name_scientific": "scientific name of herb 3 used for preparation", "confidence_score": "7"}} 
                    ]
                    Only reply with the JSON, don't add additional info.
                '''
                reply = llm_reply(prompt, model).strip()
                json_data = {}
                try: json_data = json.loads(reply)
                except: pass 
                if json_data != {}:
                    names_scientific = []
                    for item in json_data:
                        try: line = item['herb_name_scientific']
                        except: continue
                        try: score = item['confidence_score']
                        except: continue
                        print(line)
                        for plant in plants_wcvp:
                            name_scientific = plant['scientfiicname']
                            if name_scientific.lower().strip() in line.lower().strip():
                                if len(name_scientific.split(' ')) > 1:
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    print(name_scientific)
                                    print('++++++++++++++++++++++++++++++++++++++++')
                                    names_scientific.append({
                                        "name": name_scientific, 
                                        "score": score,
                                    })
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
                            print(name, '->', output_plant['herb_name_scientific'])
                            if name in output_plant['herb_name_scientific']: 
                                output_plant['herb_mentions'] += 1
                                output_plant['herb_confidence_score'] += int(score)
                                found = True
                                break
                        if not found:
                            output_plants.append({
                                'herb_name_scientific': name, 
                                'herb_mentions': 1, 
                                'herb_confidence_score': int(score), 
                            })
                output_plants_final = []
                for output_plant in output_plants:
                    output_plants_final.append({
                        'herb_name_scientific': output_plant['herb_name_scientific'],
                        'herb_mentions': int(output_plant['herb_mentions']),
                        'herb_confidence_score': int(output_plant['herb_confidence_score']),
                        'herb_total_score': int(output_plant['herb_mentions']) * int(output_plant['herb_confidence_score']),
                    })
                output_plants_final = sorted(output_plants_final, key=lambda x: x['herb_confidence_score'], reverse=True)
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

        key = f'{system_slug}_system_desc'
        if key not in data: data[key] = ''
        # data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write a very short 5-sentence paragraph about herbal remedies for the {system_name} system. 
                Include the benefits, the constituents, the herbs, and the preparations.
                Use simple and short words, and a simple writing style.
                Use a conversational and fluid writing style.
                Don't write lists.
                Don't write fluff.
                Don't allucinate.
                Don't include an conclusory statement, like a sentence that start with the words "overall", "in conclusion", "in summary", etc.
            '''
            reply = llm_reply(prompt).strip()
            reply = [line.strip() for line in reply.split('\n')]
            reply = ' '.join(reply)
            data[key] = reply
            json_write(json_filepath, data)

        # ;image
        if 0:
            key = f'{system_slug}_system_image'
            herbs_names = [x['herb_name_scientific'] for x in data[f'{system_slug}_system_herbs'][:3]]
            herbs_names = ' and '.join(herbs_names)
            prompt = f'''
                top view of dry {herbs_names} herb on a wooden table,
                indoor, 
                natural light,
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
            image = pipe(
                prompt=prompt, 
                negative_prompt=negative_prompt, 
                width=1024, height=1024, 
                num_inference_steps=30, 
                guidance_scale=7.0
            ).images[0]
            image = img_resize(image, w=768, h=768)
            output_filepath = f'{website_folderpath}/images-static/{system_slug}.jpg'
            html_filepath = f'/images-static/{system_slug}.jpg'
            image.save(output_filepath)
            data[key] = html_filepath
            json_write(json_filepath, data)

        key = f'{system_slug}_system_desc'
        system_desc = f'{data[key]}'
        system_desc = util.text_format_1N1_html(system_desc)
        if i % 2 == 0: reverse = ''
        else: reverse = 'row-reverse'
        section = f'''
            <section class="mb-64">
                <div class="container-xl">
                    <div class="flex mob-flex-col items-center {reverse} remedies_system_cols">
                        <div class="flex-1">
                             <img src="/images-static/{system_slug}.jpg">
                        </div>
                        <div class="flex-1">
                            <h2 class="text-32 mb-16">{system_name.capitalize()} System</h2>
                            {system_desc}
                            <a class="button" href="/remedies/{system_slug}-system.html" class="button">{system_name.capitalize()} System Remedies</a>
                        </div>
                    </div>
                </div>
            </section>
        '''
        sections.append(section)

    sections = ''.join(sections)

    head_html = head_html_generate('remedies for body systems', '/style.css')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {header_html}
            <main>
                {section_1}
                {sections}
            </main>
            <div class="mt-64"></div>
            {footer_html}
        </body>
        </html>
    '''
    html_filepath = f'{website_folderpath}/remedies.html'
    with open(html_filepath, 'w') as f: f.write(html)


shutil.copy2('style.css', f'{website_folderpath}/style.css')
shutil.copy2('style-article.css', f'{website_folderpath}/style-article.css')

# articles_preparations('teas')
# articles_preparations('tinctures')
# articles_preparations('decoctions')
# articles_preparations('creams')
# articles_preparations('essential-oils')
# articles_preparations_2('teas')
# articles_preparations_2('tinctures')
# articles_preparations_2('creams')
# articles_preparations_2('essential-oils')
# articles_ailments()
# articles_ailments_2()
page_home()
page_remedies()
page_systems()

# articles_titles_check('teas')

quit()

# TODO: mobile version
# TODO: breadcrumbs
# TODO: footer
# TODO: sitemap
# TODO: bad image regen
# TODO: contact
# TODO: system page -> titles of ailments articles and description, and header description
# TODO: articles -> author/meta section
# TODO: articles -> table of content
# TODO: articles ailments -> intro, links to preparations, supplementary content, regen headers (variations), images, related
# TODO: articles preparations -> ...

