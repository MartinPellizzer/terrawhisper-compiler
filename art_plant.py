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

def intro_ai(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    plant_name_scientific = json_article['plant_name_scientific']
    reply_start = f'{plant_name_scientific.capitalize()}, commonly known as '
    llm.ai_paragraph_gen(
        key = 'intro',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the {plant_name_scientific} plant.
            Include a definition of what this plant is.
            Include the health benefits.
            Include the therapeutic actions.
            Include the bioactive constituents.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {reply_start} .
        ''',
        reply_start = reply_start,
        regen = regen,
        print_prompt = True,
        clear = clear,
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
    reply_start = f'{plant_name_scientific.capitalize()} has many health benefits, such as '
    llm.ai_paragraph_gen(
        key = 'benefits',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the health benefits of the {plant_name_scientific} plant.
            Include a lot of examples.
            Include how these health benefits improve life.
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
            Include a lot of examples.
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

def gen_parts(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    plant_name_scientific = json_article['plant_name_scientific']
    reply_start = f'{plant_name_scientific.capitalize()} has many medicinal parts, such as '
    llm.ai_paragraph_gen(
        key = 'parts',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the medicinal parts of the {plant_name_scientific} plant.
            By medicinal parts I mean things like: leaves, flowers, roots, etc...
            Include examples of medicinal parts.
            Include examples of medicinal constituents that each of these medicinal parts contain.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {reply_start} .
        ''',
        reply_start = reply_start,
        regen = regen,
        print_prompt = True,
        clear = clear,
    )

def gen_preparations(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    plant_name_scientific = json_article['plant_name_scientific']
    reply_start = f'{plant_name_scientific.capitalize()} has many herbal preparations, such as '
    llm.ai_paragraph_gen(
        key = 'preparations',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the herbal preparations of the {plant_name_scientific} plant for medicinal purposes.
            By herbal preparations I mean things like: teas, tinctures, etc...
            Include examples of herbal preparations.
            Include examples of medicinal uses that each of these herbal preparations have.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {reply_start} .
        ''',
        reply_start = reply_start,
        regen = regen,
        print_prompt = True,
        clear = clear,
    )

def gen_side_effects(json_article_filepath, regen=False, clear=False):
    json_article = json_read(json_article_filepath)
    plant_name_scientific = json_article['plant_name_scientific']
    reply_start = f'{plant_name_scientific.capitalize()} can have side effects if used improperly, such as '
    llm.ai_paragraph_gen(
        key = 'side_effects',
        filepath = json_article_filepath, 
        data = json_article, 
        obj = json_article, 
        prompt = f'''
            Write a short 4-sentence paragraph about the side effects of the {plant_name_scientific} plant for health if used improperly.
            Include examples of side effects.
            If you can't answer, reply with only "I can't reply".
            Start with the following words: {reply_start} .
        ''',
        reply_start = reply_start,
        regen = regen,
        print_prompt = True,
        clear = clear,
    )

def art_plant_json(vertex_plant, json_article_filepath):
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

    # intro_ai(json_article_filepath, regen=False, clear=True)
    # gen_intro_study(json_article_filepath, regen=False)
    # gen_benefits(json_article_filepath, regen=False, clear=False)
    # gen_actions(json_article_filepath, regen=False, clear=False)
    '''
    gen_constituents(json_article_filepath, regen=False, clear=False)
    gen_parts(json_article_filepath, regen=False, clear=False)
    gen_preparations(json_article_filepath, regen=False, clear=False)
    gen_side_effects(json_article_filepath, regen=False, clear=False)
    '''

def art_plant_poison_html(html_article_filepath, json_article_filepath):
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

def has_section(json_article, section_name):
    if section_name not in json_article: return False 
    if json_article[section_name] == 'N/A': return False
    if json_article[section_name] == 'CANT': return False
    if json_article[section_name] == 'WRONG START': return False
    return True

def art_plant_medicine_html(html_article_filepath, json_article_filepath):
    json_article = json_read(json_article_filepath)
    plant_slug = json_article['plant_slug']
    plant_name_scientific = json_article['plant_name_scientific'].capitalize()
    page_title = plant_name_scientific
    html_article = ''
    html_article += f'<h1>{plant_name_scientific.capitalize()}</h1>\n'
    html_article += f'<img style="margin-bottom: 16px;" src="/images/herbs/{plant_slug}.jpg" alt="{plant_name_scientific}">\n'
    if has_section(json_article, 'intro'):
        html_article += f'{utils.text_format_sentences_html(json_article["intro"])}\n'
    print(json_article)
    print(json_article['intro'])
    if 'intro_study' in json_article and json_article['intro_study'] != 'N/A':
        html_article += components.study_snippet_html(json_article['intro_study'])
    html_article += f'<p style="margin-top: 16px; margin-bottom: 32px;">This page analize the most important medicinal aspects of {plant_name_scientific.capitalize()}.</p>\n'
    html_article += f'[html_intro_toc]\n'
    if 'benefits' in json_article and json_article['benefits'] != 'N/A':
        html_article += f'<h2>Health Benefits of {plant_name_scientific}</h2>\n'
        html_article += f'{utils.text_format_sentences_html(json_article["benefits"])}\n'
    if 'actions' in json_article and json_article['actions'] != 'N/A':
        html_article += f'<h2>Therapeutic Actions of {plant_name_scientific}</h2>\n'
        html_article += f'{utils.text_format_sentences_html(json_article["actions"])}\n'
    if 'constituents' in json_article and json_article['constituents'] != 'N/A':
        html_article += f'<h2>Bioactive Constituents of {plant_name_scientific}</h2>\n'
        html_article += f'{utils.text_format_sentences_html(json_article["constituents"])}\n'
    if 'parts' in json_article and json_article['parts'] != 'N/A':
        html_article += f'<h2>Medicinal Parts of {plant_name_scientific}</h2>\n'
        html_article += f'{utils.text_format_sentences_html(json_article["parts"])}\n'
    if 'preparations' in json_article and json_article['preparations'] != 'N/A':
        html_article += f'<h2>Herbal Preparations of {plant_name_scientific}</h2>\n'
        html_article += f'{utils.text_format_sentences_html(json_article["preparations"])}\n'
    if 'side_effects' in json_article and json_article['side_effects'] != 'N/A':
        html_article += f'<h2>Possible Side Effects of {plant_name_scientific}</h2>\n'
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

def art_plant_html(html_article_filepath, json_article_filepath):
    medicine_or_poison = medicine_poison_get(json_article_filepath)
    if medicine_or_poison:
        art_plant_medicine_html(html_article_filepath, json_article_filepath)
    else:
        art_plant_poison_html(html_article_filepath, json_article_filepath)

def art_plant_gen(vertex_plant):
    plant_slug = vertex_plant['plant_slug']
    html_article_folderpath = f'{g.WEBSITE_FOLDERPATH}/herbs'
    html_article_filepath = f'{html_article_folderpath}/{plant_slug}.html'
    json_article_filepath = f'database/pages/herbs/{plant_slug}.json'
    
    # if plant_slug != 'glycyrrhiza-glabra': return

    art_plant_json(vertex_plant, json_article_filepath)
    art_plant_html(html_article_filepath, json_article_filepath)

    # quit()
