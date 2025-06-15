import os
import json
import random

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read
from oliark_llm import llm_reply

import llm
import studies
from lib import g
from lib import io
from lib import utils
from lib import components

plants_wcvp = csv_read_rows_to_json(f'{g.VAULT_TMP}/terrawhisper/wcvp_taxon.csv', delimiter = '|')

studies_tot_n = 0
def debug_list_study(url):
    global studies_tot_n
    json_article_filepath = f'database/json/{url}.json'
    json_article = io.json_read(json_article_filepath)
    ailment_name = json_article['ailment_name']
    preparation_name = json_article['preparation_name']
    studies_art_n = 0
    for obj in json_article['preparations'][:]:
        herb_name_scientific = obj['herb_name_scientific']
        print(f'STUDY: {herb_name_scientific}')
        key = 'preparation_study'
        if key not in obj: obj[key] = ''
        if obj[key] != '' and obj[key] != 'N/A':
            print(obj[key])
            studies_art_n += 1
            studies_tot_n += 1
    print(f'STUDIES ART NUM: {studies_art_n}')

def intro_ai(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    preparation_slug = json_article['preparation_slug']
    preparation_name = json_article['preparation_name']
    llm.ai_paragraph_gen(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the herbal {preparation_name} used to treat the {ailment_name} ailment.
            Include a definition of what herbal {preparation_name} for {ailment_name} are.
            Include the benefits of herbal {preparation_name} to treat this ailment.
            Include a lot of examples of herbal {preparation_name} to treat this ailment and explain why.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: Herbal {preparation_name} for {ailment_name.capitalize()} are .
        ''',
        regen = regen,
        print_prompt = True,
    )

def intro_study_ai(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    preparation_name = json_article['preparation_name']
    key = 'intro_study'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if json_article[key] == '':
        reply = studies.gen_study_ailment_tea_intro(preparation_name, ailment_name)
        if reply.strip() != '':
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)

def list_init_ai(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    preparation_name = json_article['preparation_name']
    key = 'preparations'
    if key not in json_article: json_article[key] = []
    if regen: json_article[key] = []
    if clear: 
        json_article[key] = []
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == []:
        output_plants = []
        for i in range(20):
            prompt = f'''
                List the 20 best herbs to make herbal {preparation_name} to relieve {ailment_name}.
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
            reply = llm_reply(prompt).strip()
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
        json_article[key] = output_plants_final[:20]
        io.json_write(json_article_filepath, json_article)

def list_desc_ai(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    ailment_name = json_article['ailment_name']
    preparation_name = json_article['preparation_name']
    for obj in json_article['preparations'][:]:
        herb_name_scientific = obj['herb_name_scientific']
        llm.ai_paragraph_gen(
            key = 'preparation_desc',
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write a short 4-sentence paragraph about {herb_name_scientific} {preparation_name} to treat the {ailment_name} ailment.
                Include the properties of this herbal preparation that help to treat this ailment.
                Include how this herbal preparation helps to treat this ailment.
                Include bioactive constituents of this herbal preparation that help to treat this ailment.
                Include the benefits of this herbal preparation to treat this ailment.
                If you can't answer, reply with only "I can't reply".
                Start with the following words: {herb_name_scientific.capitalize()} {preparation_name} .
            ''',
            regen = regen,
            print_prompt = True,
        )

def list_study_ai(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    ailment_name = json_article['ailment_name']
    preparation_name = json_article['preparation_name']
    main_lst_num = json_article['main_lst_num']
    for obj in json_article['preparations'][:main_lst_num]:
        herb_name_scientific = obj['herb_name_scientific']
        key = 'preparation_study'
        if key not in obj: obj[key] = ''
        if regen: obj[key] = ''
        if obj[key] == '':
            reply = studies.gen_study_ailment_tea_list(herb_name_scientific.capitalize(), preparation_name, ailment_name)
            if reply.strip() != '':
                obj[key] = reply
                io.json_write(json_article_filepath, json_article)

def list_amazon_gen(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    preparation_slug = json_article['preparation_slug']
    key = 'preparation_amazon'
    for obj in json_article['preparations'][:]:
        if key not in obj: obj[key] = ''
        if regen: obj[key] = ''
        if obj[key] == '':
            try: 
                affiliate_product = components.amazon_json(obj, preparation_slug)
                obj[key] = affiliate_product
                io.json_write(json_article_filepath, json_article)
            except: pass

def json_gen(url, ailment, preparation):
    json_article_filepath = f'database/json/{url}.json'
    ailment_slug = ailment['ailment_slug']
    ailment_name = ailment['ailment_name']
    preparation_slug = preparation['preparation_slug']
    preparation_name = preparation['preparation_name']
    print(f'    >> JSON: {json_article_filepath}')
    ###
    json_article = json_read(json_article_filepath, create=True)
    json_article['url'] = url
    json_article['ailment_slug'] = ailment_slug
    json_article['ailment_name'] = ailment_name
    json_article['preparation_slug'] = preparation_slug
    json_article['preparation_name'] = preparation_name
    if 'lastmod' not in json_article: json_article['lastmod'] = utils.today()
    if 'main_lst_num' not in json_article: json_article['main_lst_num'] = random.choice([7, 9, 11, 13])
    json_article['title'] = f'{json_article["main_lst_num"]} best herbal {preparation_name} for {ailment_name}'.title()
    io.json_write(json_article_filepath, json_article)
    ###
    intro_ai(json_article_filepath, regen=False)
    intro_study_ai(json_article_filepath, regen=False)
    list_init_ai(json_article_filepath, regen=False, clear=False)
    list_desc_ai(json_article_filepath, regen=False)
    list_study_ai(json_article_filepath, regen=False)
    list_amazon_gen(json_article_filepath, regen=True)

def html_study_gen(json_article, key):
    html = ''
    study = json_article[key]
    if study != '' and study != 'N/A':
        html += f'''
            <div class="study" style="margin-bottom: 16px;">
                <div class="study-header">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
                    </svg>
                    <p>Related Study</p>
                </div>
                <p>
                    {study}
                </p>
            </div>
        '''
    return html

def html_gen(url):
    json_article_filepath = f'database/json/{url}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url}.html'
    print(f'    >> JSON: {json_article_filepath}')
    print(f'    >> HTML: {html_article_filepath}')
    json_article = json_read(json_article_filepath)
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    preparation_slug = json_article['preparation_slug']
    preparation_name = json_article['preparation_name']
    main_lst_num = json_article['main_lst_num']
    article_title = json_article['title']
    page_title = article_title
    ###
    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    html_article += f'''
        <img style="margin-bottom: 16px;" 
        src="/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg" 
        alt="herbal {preparation_name} for {ailment_name}">
    '''
    html_article += f'{utils.text_format_sentences_html(json_article["intro"])}\n'
    html_article += components.study_snippet_html(json_article['intro_study'])
    html_article += f'<p>Below there\'s a list of the {main_lst_num} best herbal {preparation_name} for {ailment_name}.</p>\n'
    html_article += f'[html_intro_toc]\n'
    html_article += components.lead_magnet_html()
    ###
    preparations = json_article['preparations']
    for i, preparation in enumerate(preparations[:main_lst_num]):
        herb_name_scientific = preparation['herb_name_scientific']
        herb_slug = utils.sluggify(herb_name_scientific)
        preparation_desc = preparation['preparation_desc']
        html_article += f'<h2>{i+1}. {herb_name_scientific.capitalize()} {preparation_name}</h2>\n'
        html_article += f'''
            <img style="margin-bottom: 16px;" 
            src="/images/preparations/{preparation_slug}/{herb_slug}-herbal-{preparation_slug}.jpg" 
            alt="herbal {preparation_name} with {herb_name_scientific}">
        '''
        html_article += f'{utils.text_format_sentences_html(preparation_desc)}\n'
        html_article += html_study_gen(preparation, 'preparation_study')
        html_article += components.amazon_html(preparation)
    ###
    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    html_breadcrumbs = components.breadcrumbs(f'ailments/{ailment_slug}/{preparation_slug}.html')
    ###
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 24px;" class="container-md mob-flex gap-48">
                <article class="article">
                    {html_breadcrumbs}
                    {html_article}
                </article>
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    html_article_folderpath = '/'.join(html_article_filepath.split('/')[:-1])
    if not os.path.exists(html_article_folderpath): os.mkdir(html_article_folderpath)
    with open(html_article_filepath, 'w') as f: f.write(html)

def gen():
    category_slug = 'ailments'
    preparations = []
    if 1:
        preparations.append({
            'preparation_slug': 'teas',
            'preparation_name': 'teas',
        })
    if 1:
        preparations.append({
            'preparation_slug': 'tinctures',
            'preparation_name': 'tinctures',
        })
    if 1:
        preparations.append({
            'preparation_slug': 'creams',
            'preparation_name': 'creams',
        })
    if 1:
        preparations.append({
            'preparation_slug': 'essential-oils',
            'preparation_name': 'essential oils',
        })
    for preparation in preparations:
        preparation_slug = preparation['preparation_slug']
        preparation_name = preparation['preparation_name']
        ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
        for ailment_i, ailment in enumerate(ailments):
            print(f'\n>> {ailment_i}/{len(ailments)} - {ailment}')
            ailment_slug = ailment['ailment_slug']
            if not os.path.exists(f'{g.WEBSITE_FOLDERPATH}/{category_slug}'): 
                os.mkdir(f'{g.WEBSITE_FOLDERPATH}/{category_slug}')

            if not os.path.exists(f'{g.WEBSITE_FOLDERPATH}/{category_slug}/{ailment_slug}'): 
                os.mkdir(f'{g.WEBSITE_FOLDERPATH}/{category_slug}/{ailment_slug}')
            url = f'{category_slug}/{ailment_slug}/{preparation_slug}'
            json_gen(url, ailment, preparation)
            html_gen(url)

            # debug_list_study(url)
