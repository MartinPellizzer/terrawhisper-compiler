import os
import json
import random

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read, json_write
from oliark_llm import llm_reply

import g
import llm
import utils
import studies
import components

vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'

vertices_ailments_filepath = f'/home/ubuntu/vault/herbalism/vertices-ailments.json'
vertices_ailments = json_read(vertices_ailments_filepath)
plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')

def gen_intro(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    preparation_name = json_article['preparation_name']
    llm.ai_paragraph_gen(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the herbal {preparation_name} used to treat the {ailment_name} ailment.
            Include a definition of what herbal {preparation_name} for {ailment_name} is.
            Include why herbal {preparation_name} can treat this ailment.
            Include a lot of examples of herbal {preparation_name} to treat this ailment and explain why.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: Herbal {preparation_name} for {ailment_name.capitalize()} are .
        ''',
        regen = regen,
        print_prompt = True,
    )

def gen_intro_study(json_article_filepath, regen=False):
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
            json_write(json_article_filepath, json_article)

def gen_list_init(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    preparation_name = json_article['preparation_name']
    key = 'preparations'
    if key not in json_article: json_article[key] = []
    # json_article[key] = []
    if json_article[key] == []:
        output_plants = []
        for i in range(10):
            prompt = f'''
                List the 15 best herbs to make herbal {preparation_name} to relieve {ailment_name}.
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
        json_write(json_article_filepath, json_article)

def gen_list_desc_old(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    ailment_name = json_article['ailment_name']
    preparation_name = json_article['preparation_name']
    for obj in json_article['preparations'][:]:
        herb_name_scientific = obj['herb_name_scientific']
        llm.ai_paragraph_gen(
            key = 'herb_desc',
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write a short 4-sentence paragraph about {herb_name_scientific} {preparation_name} to treat the {ailment_name} ailment.
                Include bioactive constituents of this herbal preparation that help to treat this ailment.
                Include the properties of this herbal preparation that help to treat this ailment.
                Include how to make this herbal preparation to treat this ailment.
                Include how to consume this herbal preparation to treat this ailment.
                If you can't answer, reply with only "I can't reply".
                Start with the following words: {herb_name_scientific.capitalize()} {preparation_name} contains .
            ''',
            regen = regen,
            print_prompt = True,
        )

def gen_list_desc(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    ailment_name = json_article['ailment_name']
    preparation_name = json_article['preparation_name']
    for obj in json_article['preparations'][:]:
        herb_name_scientific = obj['herb_name_scientific']
        llm.ai_paragraph_gen(
            key = 'herb_desc',
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

def gen_list_how_to(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    preparation_name = json_article['preparation_name']
    ailment_name = json_article['ailment_name']
    for remedy_i, obj in enumerate(json_article['preparations']):
        key = 'preparation_procedure'
        if key not in obj: obj[key] = ''
        if regen: obj[key] = ''
        if obj[key] == '':
            herb_name = obj['herb_name_scientific']
            prompt = f'''
                Write a 5-step procedure on how to make {herb_name} {preparation_name} for {ailment_name}.
                Make the procedure easy to do and actionable.
                Use simple and short words, and a simple writing style.
                Write short and concise steps.
                Use tablespoon, cup of, etc. as unit of measure.
                Don't write fluff.
                Don't allucinate.
                Reply in the following JSON format: 
                {{
                    "step_1": "write step 1 here", 
                    "step_2": "write step 2 here", 
                    "step_3": "write step 3 here",
                    "step_4": "write step 4 here",
                    "step_5": "write step 5 here"
                }} 
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                try: step_1 = json_data['step_1']
                except: step_1 = ''
                try: step_2 = json_data['step_2']
                except: step_2 = ''
                try: step_3 = json_data['step_3']
                except: step_3 = ''
                try: step_4 = json_data['step_4']
                except: step_4 = ''
                try: step_5 = json_data['step_5']
                except: step_5 = ''
                if step_1 != '' and step_2 != '' and step_3 != '' and step_4 != '' and step_5 != '':
                    obj[key] = [
                        step_1,
                        step_2,
                        step_3,
                        step_4,
                        step_5,
                    ]
                    json_write(json_article_filepath, json_article)

def gen_list_usage(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    preparation_name = json_article['preparation_name']
    ailment_name = json_article['ailment_name']
    main_lst_num = json_article['main_lst_num']
    preparations = json_article['preparations'][:main_lst_num]
    for remedy_i, obj in enumerate(preparations):
        print(f'{remedy_i}/{len(preparations)}')
        key = 'preparation_usage'
        if key not in obj: obj[key] = ''
        if regen: obj[key] = ''
        if obj[key] == '':
            herb_name = obj['herb_name_scientific']
            prompt = f'''
                Write a 5-step procedure on how to use {herb_name} {preparation_name} for {ailment_name}.
                Write short and concise steps.
                Write each step in less than 15 words.
                Make the procedure easy to do and actionable.
                Use simple and short words, and a simple writing style.
                Include dosages and frequency of usage.
                Never include steps on how to prepare this preparation.
                Never include steps on side effects and precautions.
                Use tablespoon, cup of, etc. as unit of measure.
                Don't write fluff.
                Don't allucinate.
                Reply in the following JSON format: 
                {{
                    "step_1": "write step 1 here", 
                    "step_2": "write step 2 here", 
                    "step_3": "write step 3 here",
                    "step_4": "write step 4 here",
                    "step_5": "write step 5 here"
                }} 
                Only reply with the JSON, don't add additional info.
            '''
            reply = llm_reply(prompt).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                try: step_1 = json_data['step_1']
                except: step_1 = ''
                try: step_2 = json_data['step_2']
                except: step_2 = ''
                try: step_3 = json_data['step_3']
                except: step_3 = ''
                try: step_4 = json_data['step_4']
                except: step_4 = ''
                try: step_5 = json_data['step_5']
                except: step_5 = ''
                if step_1 != '' and step_2 != '' and step_3 != '' and step_4 != '' and step_5 != '':
                    obj[key] = [
                        step_1,
                        step_2,
                        step_3,
                        step_4,
                        step_5,
                    ]
                    json_write(json_article_filepath, json_article)

studies_tot_n = 0
def debug_list_study(json_article_filepath):
    global studies_tot_n
    json_article = json_read(json_article_filepath)
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

def gen_list_study(json_article_filepath, regen=False):
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
                json_write(json_article_filepath, json_article)

def gen_list_side_effects(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    ailment_name = json_article['ailment_name']
    preparation_name = json_article['preparation_name']
    for obj in json_article['preparations'][:]:
        herb_name_scientific = obj['herb_name_scientific']
        llm.ai_paragraph_gen(
            key = 'preparation_side_effect',
            filepath = json_article_filepath, 
            data = json_article, 
            obj = obj, 
            prompt = f'''
                Write a short 2-sentence paragraph about the possible side effects of using {herb_name_scientific} {preparation_name} to treat the {ailment_name} ailment.
                Include the side effects of this herbal preparation when used to treat this ailment.
                Include the precautions to take when using this herbal preparation to treat this ailment.
                Never include the fact that you should consult with a doctor or other experts in the precautions.
                If you can't answer, reply with only "I can't reply".
                Start with the following words: {herb_name_scientific.capitalize()} {preparation_name} can .
            ''',
            regen = regen,
            print_prompt = True,
        )

def gen_list_amazon(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    preparation_slug = json_article['preparation_slug']
    key = 'preparation_amazon'
    for obj in json_article['preparations'][:]:
        if key not in obj: obj[key] = ''
        if regen: obj[key] = ''
        if obj[key] == '':
            affiliate_product = components.amazon_json(obj, preparation_slug)
            obj[key] = affiliate_product
            json_write(json_article_filepath, json_article)

def art_ailments_preparation_json(preparation_slug, ailment, article_url, json_article_filepath):
    preparation_name = preparation_slug.replace('-', ' ')
    ailment_name = ailment['ailment_name']
    json_article = json_read(json_article_filepath, create=True)
    json_article['preparation_slug'] = preparation_slug
    json_article['preparation_name'] = preparation_name
    json_article['ailment_slug'] = ailment['ailment_slug']
    json_article['ailment_name'] = ailment_name
    json_article['system_slug'] = ailment['system_slug']
    json_article['organ_slug'] = ailment['organ_slug']
    json_article['url'] = article_url
    if 'main_lst_num' not in json_article: json_article['main_lst_num'] = random.choice([7, 9, 11, 13])
    json_article['title'] = f'{json_article["main_lst_num"]} Best Herbal {preparation_name.title()} For {ailment_name.title()}'
    json_write(json_article_filepath, json_article)

    gen_intro(json_article_filepath, regen=False)
    gen_intro_study(json_article_filepath, regen=False)
    gen_list_init(json_article_filepath, regen=False)
    gen_list_desc(json_article_filepath, regen=False)
    gen_list_how_to(json_article_filepath, regen=False)
    gen_list_usage(json_article_filepath, regen=False)
    gen_list_study(json_article_filepath, regen=False)
    gen_list_side_effects(json_article_filepath, regen=False)
    gen_list_amazon(json_article_filepath, regen=True)

def study_intro_html(json_article):
    html = ''
    study = json_article['intro_study']
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

def art_ailments_preparation_html(html_article_filepath, json_article_filepath):
    json_article = json_read(json_article_filepath)
    preparation_slug = json_article['preparation_slug']
    preparation_name = json_article['preparation_name']
    ailment_slug = json_article['ailment_slug']
    ailment_name = json_article['ailment_name']
    system_slug = json_article['system_slug']
    organ_slug = json_article['organ_slug']
    article_url = json_article['url'] 
    article_title = json_article['title']
    main_lst_num = json_article['main_lst_num']
    page_title = f'best herbal {preparation_name} for {ailment_name}'
    html_article = ''
    html_article += f'<h1>{article_title}</h1>\n'
    html_article += f'''
        <img style="margin-bottom: 16px;" 
        src="/images/preparations/{ailment_slug}-herbal-{preparation_slug}.jpg" 
        alt="herbal {preparation_name} for {ailment_name}">
    '''
    html_article += f'{utils.text_format_sentences_html(json_article["intro"])}\n'
    html_article += study_intro_html(json_article)
    html_article += f'<p>Below there\'s a list of the {main_lst_num} best herbal {preparation_name} for {ailment_name}.</p>\n'
    html_article += f'[html_intro_toc]\n'
    html_article += components.checklist_html()
    for i, preparation in enumerate(json_article['preparations'][:main_lst_num]):
        herb_name_scientific = preparation['herb_name_scientific']
        herb_slug = utils.sluggify(herb_name_scientific)
        herb_desc = preparation['herb_desc']
        preparation_side_effect = preparation['preparation_side_effect']
        html_article += f'<h2>{i+1}. {herb_name_scientific.capitalize()} {preparation_name}</h2>\n'
        html_article += f'''
            <img style="margin-bottom: 16px;" 
            src="/images/preparations/{preparation_slug}/{herb_slug}-herbal-{preparation_slug}.jpg" 
            alt="herbal {preparation_name} with {herb_name_scientific}">
        '''
        # desc
        html_article += f'{utils.text_format_sentences_html(herb_desc)}\n'
        # study
        preparation_study = preparation['preparation_study']
        if preparation_study != '' and preparation_study != 'N/A':
            html_article += f'''
                <div class="study">
                    <div class="study-header">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
                        </svg>
                        <p>Related Study</p>
                    </div>
                    <p>
                        {preparation_study}
                    </p>
                </div>
            '''
        # recipe
        # html_article += f'<p style="font-weight: bold; color: #101010;">{herb_name_scientific.title()} {preparation_name.title()} Recipe For {ailment_name.title()}:</p>\n'
        html_article += f'<p style="font-weight: bold; color: #101010;">Recipe:</p>\n'
        html_article += f'<ol>\n'
        for step in preparation['preparation_procedure']:
            html_article += f'<li>\n'
            html_article += f'{step}\n'
            html_article += f'</li>\n'
        html_article += f'</ol>\n'
        # usage
        if 0:
            html_article += f'<p style="font-weight: bold; color: #101010;">Usage:</p>\n'
            html_article += f'<ol>\n'
            for step in preparation['preparation_usage']:
                html_article += f'<li>\n'
                html_article += f'{step}\n'
                html_article += f'</li>\n'
            html_article += f'</ol>\n'
        # side effects
        html_article += f'{utils.text_format_sentences_html(preparation_side_effect)}\n'
        # amazon
        html_article += components.amazon_html(preparation)
    # checklist
    # html_article = html_article.replace('[checklist]', html_checklist)
    # toc
    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    html_breadcrumbs = components.breadcrumbs(f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}.html')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 24px;" class="container-xl mob-flex gap-48">
                <article style="flex: 2;" class="article">
                    {html_breadcrumbs}
                    {html_article}
                </article>
                <aside style="flex: 1; position: sticky; top: 100px; z-index: 999; align-self: flex-start; overflow-y: auto; height: 100vh;">
                    {html_toc_sidebar}
                </aside>
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
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

def art_ailments_preparations_gen(preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        article_url = f'remedies/{system_slug}-system/{ailment_slug}/{preparation_slug}'
        json_article_filepath = f'database/pages/{article_url}.json'
        html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{article_url}.html'

        '''
        print(f'\n>> {ailment_i}/{len(ailments)}')
        print(f'\n  >> ailment: {ailment_name}')
        print(f'\n  >> preparation: {preparation_name}')
        print(f'\n  >> article_url: {article_url}')
        '''

        art_ailments_preparation_json(preparation_slug, ailment, article_url, json_article_filepath)
        art_ailments_preparation_html(html_article_filepath, json_article_filepath)

        # debug
        debug_list_study(json_article_filepath)
        # break

    print(f'STUDIES TOT NUM: {studies_tot_n}')
