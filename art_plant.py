import os
import json

from oliark_io import json_read, json_write
from oliark_llm import llm_reply

import g
import llm
import utils

import components
import studies

def medicine_poison_gen(json_article_filepath, regen, clear):
    json_article = json_read(json_article_filepath)
    herb_name_scientific = json_article['plant_name_scientific']
    key = 'medicine_or_poison'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if clear: 
        json_article[key] = ''
        json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            prompt = f'''
                Tell me if the following herb is considered medicinal or poisonous: {herb_name_scientific}.
                Also, tell give a confidence score from 1 to 10, indicating how sure you are about your answer.
                Don't write fluff, only proven facts.
                Don't allucinate.
                Reply in the following JSON format: 
                [
                    {{"medicine_or_poison": <write "medicine" or "poison" here>, "confidence_score": 8}} 
                ]
                Only reply with the JSON, don't add additional info.
                Don't include notes, reply ONLY with the JSON.
            '''
            reply = llm_reply(prompt).strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = []
                for item in json_data:
                    try: name = item['medicine_or_poison']
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
                        if name in output['medicine_or_poison']: 
                            output['mentions'] += 1
                            output['confidence_score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'medicine_or_poison': name, 
                            'mentions': 1, 
                            'confidence_score': int(score), 
                        })
        outputs_final = []
        for output in outputs:
            outputs_final.append({
                'medicine_or_poison': output['medicine_or_poison'],
                'mentions': int(output['mentions']),
                'confidence_score': int(output['confidence_score']),
                'total_score': int(output['mentions']) * int(output['confidence_score']),
            })
        outputs_final = sorted(outputs_final, key=lambda x: x['total_score'], reverse=True)
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs_final:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        json_article[key] = outputs_final
        json_write(json_article_filepath, json_article)

def medicine_poison_get(json_article_filepath):
    json_article = json_read(json_article_filepath)
    medicine_or_poison = json_article['medicine_or_poison']
    medicine = {'medicine_or_poison': 'medicine', 'total_score': 0}
    for _obj in medicine_or_poison:
        if 'medicine' in _obj['medicine_or_poison']: 
            medicine = _obj
            break
    poison = {'medicine_or_poison': 'poison', 'total_score': 0}
    for _obj in medicine_or_poison:
        if 'poison' in _obj['medicine_or_poison']: 
            poison = _obj
            break
    if medicine['total_score'] > poison['total_score']: return 'medicine'
    else: return 'poison'

def gen_intro(vertex_plant, json_article_filepath):
    plant_name_scientific = vertex_plant['plant_name_scientific']
    json_article = json_read(json_article_filepath)
    llm.ai_paragraph_gen(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the {plant_name_scientific} plant.
            Include a definition of what this plant is.
            Include the medicinal properties.
            Include the health benefits.
            Include the herbal preparations.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {plant_name_scientific.capitalize()} .
        ''',
        regen = False,
        print_prompt = True,
    )

def gen_intro_study(json_article_filepath, regen=False):
    json_article = json_read(json_article_filepath)
    plant_name_scientific = json_article['plant_name_scientific']
    key = 'intro_study'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if json_article[key] == '':
        reply = studies.gen_study_plant_intro(plant_name_scientific)
        if reply.strip() != '':
            json_article[key] = reply
            json_write(json_article_filepath, json_article)

def gen_benefits(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    plant_name_scientific = json_article['plant_name_scientific']
    reply_start = f'{plant_name_scientific.capitalize()} has many benefits, such as '
    llm.ai_paragraph_gen(
        key = 'benefits',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the benefits of the {plant_name_scientific} plant.
            Include the benefits of this plant on healh.
            Include a lot of examples of benefits.
            Include how these benefits improve life.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {reply_start} .
        ''',
        reply_start = reply_start,
        regen = regen,
        print_prompt = True,
        clear = clear,
    )

def gen_actions(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    plant_name_scientific = json_article['plant_name_scientific']
    reply_start = f'{plant_name_scientific.capitalize()} has many therapeutic actions, such as '
    llm.ai_paragraph_gen(
        key = 'actions',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the therapeutic actions of the {plant_name_scientific} plant.
            Include a lot of examples of therapeutic actions.
            Include examples of how these therapeutic actions improve people daily lives.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {reply_start} .
        ''',
        reply_start = reply_start,
        regen = regen,
        print_prompt = True,
        clear = clear,
    )

def gen_constituents(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    plant_name_scientific = json_article['plant_name_scientific']
    reply_start = f'{plant_name_scientific.capitalize()} has many active constituents, such as '
    llm.ai_paragraph_gen(
        key = 'constituents',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the medicinal constituents of the {plant_name_scientific} plant.
            Include a lot of examples of medicinal constituents.
            Include examples of how these medicinal constituents improve people daily lives.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {reply_start} .
        ''',
        reply_start = reply_start,
        regen = regen,
        print_prompt = True,
        clear = clear,
    )

def gen_art_plant_json(vertex_plant, json_article_filepath):
    plant_slug = vertex_plant['plant_slug']
    plant_name_scientific = vertex_plant['plant_name_scientific']
    # plant_names_common = vertex_plant['plant_names_common']
    json_article = json_read(json_article_filepath, create=True)
    json_article['plant_slug'] = plant_slug
    json_article['plant_name_scientific'] = plant_name_scientific
    # json_article['plant_names_common'] = plant_names_common
    json_article['plant_url'] = f'herbs/{plant_slug}.html'
    json_article['title'] = f'{plant_name_scientific}'
    json_write(json_article_filepath, json_article)

    medicine_poison_gen(json_article_filepath, regen=False, clear=False)
    gen_intro(vertex_plant, json_article_filepath)
    # gen_intro_study(json_article_filepath, regen=False)
    gen_benefits(json_article_filepath, regen=False, clear=False)
    gen_actions(json_article_filepath, regen=False, clear=False)
    gen_constituents(json_article_filepath, regen=False, clear=False)

    '''
    gen_parts(vertex_plant, json_article_filepath)
    gen_preparations(vertex_plant, json_article_filepath)
    gen_side_effects(vertex_plant, json_article_filepath)
    '''

def gen_art_plant_poison_html(html_article_filepath, json_article_filepath):
    json_article = json_read(json_article_filepath)
    plant_slug = json_article['plant_slug']
    plant_name_scientific = json_article['plant_name_scientific'].capitalize()
    page_title = plant_name_scientific
    html_article = ''
    html_article += f'<h1>{plant_name_scientific.capitalize()}</h1>\n'
    # html_article += f'<img src="/images/herbs/{plant_slug}.jpg" alt="{plant_name_scientific}">\n'
    html_article += f'<p>{plant_name_scientific.capitalize()} is mostly categorized as a poisonous plant, so it will not be coverd.</p>\n'
    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    html_breadcrumbs = components.breadcrumbs(f'herbs/{plant_slug}.html')
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
    html_article_folderpath = '/'.join(html_article_filepath.split('/')[:-1])
    if not os.path.exists(html_article_folderpath): 
        os.mkdir(html_article_folderpath)
    with open(html_article_filepath, 'w') as f: 
        f.write(html)

def gen_art_plant_medicine_html(html_article_filepath, json_article_filepath):
    json_article = json_read(json_article_filepath)
    plant_slug = json_article['plant_slug']
    plant_name_scientific = json_article['plant_name_scientific'].capitalize()
    page_title = plant_name_scientific
    html_article = ''
    html_article += f'<h1>{plant_name_scientific.capitalize()}</h1>\n'
    # html_article += f'<img src="/images/herbs/{plant_slug}.jpg" alt="{plant_name_scientific}">\n'
    if 'intro' in json_article and json_article['intro'] != 'N/A':
        html_article += f'{utils.text_format_sentences_html(json_article["intro"])}\n'
    # study
    try: intro_study = json_article['intro_study']
    except: intro_study = ''
    if intro_study != '' and intro_study != 'N/A':
        html_article += f'''
            <div class="study" style="margin-bottom: 16px;">
                <div class="study-header">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
                    </svg>
                    <p>Related Study</p>
                </div>
                <p>
                    {intro_study}
                </p>
            </div>
        '''
    html_article += f'<p style="margin-top: 16px; margin-bottom: 32px;">This page analize the most important medicinal aspects of {plant_name_scientific.capitalize()}.</p>\n'
    html_article += f'[html_intro_toc]\n'
    html_article += f'<h2>Benefits</h2>\n'
    try: html_article += f'{utils.text_format_sentences_html(json_article["benefits"])}\n'
    except: pass
    # html_article += f'<p>Here are the <a href="/herbs/{plant_slug}/benefit.html">best health benefits of {plant_name_scientific}</a>.</p>\n'
    html_article += f'<h2>Therapeutic Actions</h2>\n'
    html_article += f'{utils.text_format_sentences_html(json_article["actions"])}\n'
    if 0:
        html_article += f'<h2>Constituents</h2>\n'
        html_article += f'{utils.text_format_sentences_html(json_article["constituents"])}\n'
        html_article += f'<h2>Parts</h2>\n'
        html_article += f'{utils.text_format_sentences_html(json_article["parts"])}\n'
        html_article += f'<h2>Preparations</h2>\n'
        html_article += f'{utils.text_format_sentences_html(json_article["preparations"])}\n'
        html_article += f'<h2>Side Effects</h2>\n'
        html_article += f'{utils.text_format_sentences_html(json_article["side_effects"])}\n'
    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    html_breadcrumbs = components.breadcrumbs(f'herbs/{plant_slug}.html')
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
    html_article_folderpath = '/'.join(html_article_filepath.split('/')[:-1])
    if not os.path.exists(html_article_folderpath): 
        os.mkdir(html_article_folderpath)
    with open(html_article_filepath, 'w') as f: 
        f.write(html)

def gen_art_plant_html(html_article_filepath, json_article_filepath):
    medicine_or_poison = medicine_poison_get(json_article_filepath)
    if medicine_or_poison:
        gen_art_plant_medicine_html(html_article_filepath, json_article_filepath)
    else:
        gen_art_plant_poison_html(html_article_filepath, json_article_filepath)

def gen_art_plant(vertex_plant):
    plant_slug = vertex_plant['plant_slug']
    html_article_folderpath = f'{g.WEBSITE_FOLDERPATH}/herbs'
    html_article_filepath = f'{html_article_folderpath}/{plant_slug}.html'
    json_article_filepath = f'database/pages/herbs/{plant_slug}.json'

    gen_art_plant_json(vertex_plant, json_article_filepath)
    gen_art_plant_html(html_article_filepath, json_article_filepath)

    # quit()
