import shutil
import time
import os
import random

import g
import util
import utils_ai
import sitemap



########################################################################
# TEAS CONDITIONS
########################################################################

csv_conditions_filepath = 'database/csv/ailments/conditions.csv'
conditions_rows = util.csv_get_rows(csv_conditions_filepath)
conditions_cols = util.csv_get_header_dict(conditions_rows)

csv_teas_filepath = 'database/csv/herbalism/teas_conditions.csv'
teas_rows = util.csv_get_rows(csv_teas_filepath)
teas_cols = util.csv_get_header_dict(teas_rows)

for condition_row in conditions_rows[1:]:

    # CSV
    condition_id = condition_row[conditions_cols['condition_id']].strip()
    condition_name = condition_row[conditions_cols['condition_name']].strip().lower()
    condition_slug = condition_row[conditions_cols['condition_slug']]
    condition_classification = condition_row[conditions_cols['condition_classification']].strip().lower()
    condition_pinned = condition_row[conditions_cols['condition_pinned']].strip().lower()

    if condition_id == '': continue
    if condition_classification == '': continue
    if condition_pinned == '': continue 

    # JSON
    json_filepath = f'database/json/herbalism/tea/{condition_slug}.json'
    util.create_folder_for_filepath(json_filepath)
    util.json_generate_if_not_exists(json_filepath)
    data = util.json_read(json_filepath)
    data['condition_name'] = condition_name
    data['condition_slug'] = condition_slug
    data['url'] = f'herbalism/tea/{condition_slug}'
    lastmod = util.date_now()
    if 'lastmod' not in data: data['lastmod'] = lastmod
    else: lastmod = data['lastmod'] 
    remedy_num = 10
    data['remedy_num'] = remedy_num
    title = f'{remedy_num} best herbal teas for {condition_name}'
    data['title'] = title
    util.json_write(json_filepath, data)

    # AI
    # -----------------------------------------------------------------------------

    # GEN INTRO
    failed_regen = False
    if 'intro' not in data:
        prompt = f'''
            Write 1 short paragraph about the best herbal teas for {condition_name}.
        '''
        reply = utils_ai.gen_reply(prompt)
        if reply != '':
            data['intro'] = reply
            util.json_write(json_filepath, data)
        else:
            failed_regen = True
        time.sleep(30)

    # INIT/CLEAN LIST OF TEAS (TO REFACTOR)
    if 'teas' not in data: data['teas'] = []

    # ADD NEW TEAS
    for tea_row in teas_rows[1:]:
        tea_condition_id = tea_row[teas_cols['condition_id']].strip().lower()
        tea_name = tea_row[teas_cols['tea_name']].strip().lower()
        if tea_condition_id != condition_id: continue
        found = False
        for tea_obj in data['teas']:
            if tea_obj['tea_name'] == tea_name: 
                found = True
                break
        if not found:
            data['teas'].append({'tea_name': tea_name})

    # DELETE REMOVED TEAS
    data_filtered = []
    for tea_obj in data['teas']: 
        found = False
        for tea_row in teas_rows[1:]:
            tea_condition_name = tea_row[teas_cols['condition_name']].strip().lower()
            tea_name = tea_row[teas_cols['tea_name']].strip().lower()
            if tea_condition_name != condition_name: continue
            if tea_obj['tea_name'] == tea_name: 
                found = True
                break
        if found:
            data_filtered.append(tea_obj)

    data['teas'] = data_filtered
    util.json_write(json_filepath, data)

    # GEN TEAS (TO COMPLETE)
    for tea_obj in data['teas'][:remedy_num]:
        # del tea_obj['tea_desc'] # TODO: remove, temp reset
        if 'tea_desc' not in tea_obj:
            tea_name = tea_obj["tea_name"].strip().lower()
            tea_name = f'{tea_name} tea'.replace(' tea tea', ' tea')
            starting_text = f'{tea_name.capitalize()} helps with {condition_name} because '
            prompt = f'''
                Explain in a 5-sentence paragraph why {tea_name} helps with {condition_name}.
                Never use the following words: can, may, might.
            '''   
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_paragraphs(reply)
            if len(reply) == 1 and reply != '':
                tea_obj['tea_desc'] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(30)

        # del tea_obj['tea_parts'] # TODO: remove, temp reset
        if 'tea_parts' not in tea_obj:
            tea_name = tea_obj['tea_name']
            prompt = f'''
                Write a numbered list of the most used parts of the {tea_name} plant that are used to make medicinal tea for {condition_name}.
                Reply by only selecting parts from the following list:
                - Roots
                - Rhyzomes
                - Stems
                - Leaves
                - Flowers
                - Seeds
                - Buds
                - Bark
                Never include aerial parts.
                Never repeat the same part twice and never include similar parts.
                Include 1 short sentence description for each of these part, explaining why that part is good for making medicinal tea for {condition_name}.
                Never use the following words: can, may, might.
            '''     
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_list_column(reply)
            if reply != '':
                tea_obj['tea_parts'] = reply
                util.json_write(json_filepath, data)
            time.sleep(30)
        
        # gen study
        # gen constituents
        # gen recipe

    # GEN SECONDARY CONTENT 
    # related symptoms/causes

    # HTML
    html_filepath = f'website/herbalism/tea/{condition_slug}.html'

    data = util.json_read(json_filepath)

    article_html = ''
    article_html += f'<h1>{title}</h1>\n'

    tea_obj = data['teas'][0]
    tea_name = tea_obj['tea_name'].strip().lower()
    tea_slug = tea_name.replace(' ', '-').replace("'", '-').replace('.', '-')
    images_folderpath = f'C:/terrawhisper-assets/images/tea/{tea_slug}'
    if os.path.exists(images_folderpath):
        images_filepaths = [f'{images_folderpath}/{filename}' for filename in os.listdir(images_folderpath)] 
        image_filepath = random.choice(images_filepaths)
        if image_filepath != '':
            image_filepath_out = f'website/images/herbal-tea-for-{condition_slug}-overview.jpg'
            if not os.path.exists(image_filepath_out):
                util.image_variate(image_filepath, image_filepath_out)
    else:
        print(f'IMG FOLDER MISSING: {images_folderpath}')
    tea_image_url = f'/images/herbal-tea-for-{condition_slug}-{tea_slug}.jpg'
    if os.path.exists(f'website{tea_image_url}'):
        article_html += f'<p><img src="/images/herbal-tea-for-{condition_slug}-overview.jpg"><p>\n'
    else:
        print(f'IMG MISSING: {tea_slug}')

    if 'intro' in data:
        article_html += f'<p>{util.text_format_1N1_html(data["intro"])}</p>\n'
    
    i = 0
    for tea_obj in data['teas'][:remedy_num]:
        i += 1
        tea_name = tea_obj['tea_name'].strip().lower()
        tea_slug = tea_name.replace(' ', '-').replace("'", '-').replace('.', '-')

        article_html += f'<h2>{i}. {tea_name.title()}</h2>\n'
        try: article_html += f'<p>{util.text_format_1N1_html(tea_obj["tea_desc"])}</p>\n'
        except: print(f'MISSING DESC: {condition_name} >> {tea_name}')

        images_folderpath = f'C:/terrawhisper-assets/images/tea/{tea_slug}'
        if os.path.exists(images_folderpath):
            images_filepaths = [f'{images_folderpath}/{filename}' for filename in os.listdir(images_folderpath)] 
            image_filepath = random.choice(images_filepaths)
            if image_filepath != '':
                image_filepath_out = f'website/images/herbal-tea-for-{condition_slug}-{tea_slug}.jpg'
                if not os.path.exists(image_filepath_out):
                    util.image_variate(image_filepath, image_filepath_out)
        else:
            print(f'IMG FOLDER MISSING: {images_folderpath}')
        tea_image_url = f'/images/herbal-tea-for-{condition_slug}-{tea_slug}.jpg'
        if os.path.exists(f'website{tea_image_url}'):
            article_html += f'<p><img src="/images/herbal-tea-for-{condition_slug}-{tea_slug}.jpg"><p>\n'
        else:
            print(f'IMG MISSING: {tea_slug}')
            
        tea_parts = tea_obj['tea_parts']
        article_html += f'<p>Right below you will find a list of the most important active constituents in {tea_name} tea that help with {condition_name}.</p>\n'
        article_html += '<ul>\n'
        for tea_part in tea_parts:
            chunk_1 = tea_part.split(': ')[0]
            chunk_2 = ': '.join(tea_part.split(': ')[1:])
            article_html += f'<li><strong>{chunk_1}</strong>: {chunk_2}</li>\n'
        article_html += '</ul>\n'

    header_html = util.header_default()
    breadcrumbs_html = util.breadcrumbs(html_filepath)
    meta_html = util.article_meta(article_html, lastmod)
    article_html = util.article_toc(article_html)

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
            
        </head>

        <body>
            {header_html}
            {breadcrumbs_html}
            
            <section class="article-section">
                <div class="container">
                    {meta_html}
                    {article_html}
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




########################################################################
# TEA PAGE
########################################################################
title = 'herbal tea'

# JSON
json_filepath = f'database/json/herbalism/tea.json'
util.create_folder_for_filepath(json_filepath)
util.json_generate_if_not_exists(json_filepath)
tea_data = util.json_read(json_filepath)
tea_data['url'] = f'herbalism/tea'
lastmod = util.date_now()
if 'lastmod' not in tea_data: tea_data['lastmod'] = lastmod
else: lastmod = tea_data['lastmod'] 
tea_data['title'] = title
util.json_write(json_filepath, tea_data)

# AI
if 'intro' not in tea_data:
    prompt = f'''
        Write a 5-sentence paragraph about herbal teas for medicinal purposes.
        Include the definition of herbal teas.
        Include the medicinal properties of herbal teas.
        Include examples of what are some of the most used herbal teas.
        Include examples of the most common health conditions you can heal with herbal teas.
        Include a simple general procedure to make effective herbal teas.
        Reply in as few words as possible.
        Start with the following words: Herbal teas are .
    '''
    reply = utils_ai.gen_reply(prompt)
    tea_data['intro'] = reply
    util.json_write(json_filepath, tea_data)
    time.sleep(30)

# AI SYSTEMS
if 'systems' not in tea_data: tea_data['systems'] = []
systems_rows = util.csv_get_rows('database/csv/ailments/systems.csv')
systems_cols = util.csv_get_header_dict(systems_rows)
for system_row in systems_rows[1:]:
    system_id = system_row[systems_cols['system_id']].strip()
    system_name = system_row[systems_cols['system_name']].strip().lower()
    found = False
    for system_obj in tea_data['systems']:
        if system_obj['system_id'] == system_id:
            found = True
            break
    if not found: 
        if system_name not in tea_data['systems']: tea_data['systems'].append({'system_id': system_id, 'system_name': system_name})
        util.json_write(json_filepath, tea_data)

# AI SYSTEMS CONDITIONS
for system_obj in tea_data['systems']:
    if 'system_conditions' not in system_obj: system_obj['system_conditions'] = []
    system_id = system_obj['system_id']

    conditions_rows = util.csv_get_rows(csv_conditions_filepath)
    conditions_cols = util.csv_get_header_dict(conditions_rows)

    for condition_row in conditions_rows[1:]:
        condition_system_id = condition_row[conditions_cols['system_id']]
        condition_classification = condition_row[conditions_cols['condition_classification']]

        if condition_system_id != system_id: continue
        if condition_classification != 'symptom': continue

        condition_id = condition_row[conditions_cols['condition_id']]
        condition_name = condition_row[conditions_cols['condition_name']]
        condition_slug = condition_row[conditions_cols['condition_slug']]

        found = False
        for condition_obj in system_obj['system_conditions']:
            if condition_obj['condition_id'] == condition_id:
                found = True
                break
        
        if not found:
            system_obj['system_conditions'].append({
                'condition_id': condition_id, 
                'condition_name': condition_name, 
                'condition_slug': condition_slug,
                'condition_classification': condition_classification,
            })
util.json_write(json_filepath, tea_data)

# AI SYSTEMS CONDITIONS DESC
for system_obj in tea_data['systems']:   
    for condition_obj in system_obj['system_conditions']:
        if 'condition_desc' not in condition_obj: condition_obj['condition_desc'] = ''
        condition_name = condition_obj['condition_name']
        condition_desc = condition_obj['condition_desc']
        if condition_desc == '':
            prompt = f'''
                Write 1 sentence explaining what is {condition_name} and what herbal teas can help with this problem.
            '''
            reply = utils_ai.gen_reply(prompt)
            condition_obj['condition_desc'] = reply
            util.json_write(json_filepath, tea_data)
            time.sleep(30)




# HTML
html_filepath = f'website/herbalism/tea.html'

tea_data = util.json_read(json_filepath)
intro = tea_data['intro']

article_html = ''
article_html += f'<h1>{title}</h1>\n'
article_html += f'<p>{intro}</p>\n'

for system_obj in tea_data['systems']:
    system_name = system_obj['system_name']
    article_html += f'<h2>Herbal Teas For The {system_name.title()} System</h2>\n'
    article_html += f'<ul>\n'
    for condition_obj in system_obj['system_conditions']:
        condition_name = condition_obj['condition_name'].strip().title()
        condition_slug = condition_obj['condition_slug'].strip().lower()
        condition_desc = condition_obj['condition_desc'].strip()
        article_html += f'<li><strong><a href="/herbalism/tea/{condition_slug}.html">Herbal Teas For {condition_name}</a></strong>: {condition_desc}</li>\n'
    article_html += f'</ul>\n'

header_html = util.header_default()
breadcrumbs_html = util.breadcrumbs(html_filepath)
meta_html = util.article_meta(article_html, lastmod)
article_html = util.article_toc(article_html)

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
        
    </head>

    <body>
        {header_html}
        {breadcrumbs_html}
        
        <section class="article-section">
            <div class="container">
                {meta_html}
                {article_html}
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







sitemap.sitemap_all()
shutil.copy2('sitemap.xml', 'website/sitemap.xml')

