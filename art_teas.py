import time
import os

import g
import util
import utils_ai

csv_conditions_filepath = 'database/csv/ailments/conditions.csv'
conditions_rows = util.csv_get_rows(csv_conditions_filepath)
conditions_cols = util.csv_get_header_dict(conditions_rows)

for condition_row in conditions_rows[1:]:

    # CSV
    condition_id = condition_row[conditions_cols['condition_id']].strip()
    condition_name = condition_row[conditions_cols['condition_name']].strip().lower()
    condition_slug = condition_row[conditions_cols['condition_slug']]
    condition_classification = condition_row[conditions_cols['condition_classification']]

    if condition_id == '': continue
    if condition_classification != 'symptom': continue

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
    failed_regen = False
    if 'intro' not in data:
    # if 'intro' not in data or regen == True:
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
    teas_rows = util.csv_get_rows('database/csv/herbalism/teas_conditions.csv')
    teas_cols = util.csv_get_header_dict(teas_rows)

    for tea_row in teas_rows[1:]:
        tea_condition_name = tea_row[teas_cols['condition']].strip().lower()
        tea_name = tea_row[teas_cols['tea']].strip().lower()

        if tea_condition_name != condition_name: continue

        found = False
        for tea_obj in data['teas']:
            if tea_obj['tea_name'] == tea_name: 
                found = True 
                break

        if not found:
            data['teas'].append({'tea_name': tea_name})

    data_filtered = []
    for tea_obj in data['teas']: 
        found = False
        for tea_row in teas_rows[1:]:
            tea_condition_name = tea_row[teas_cols['condition']].strip().lower()
            tea_name = tea_row[teas_cols['tea']].strip().lower()

            if tea_condition_name != condition_name: continue

            if tea_obj['tea_name'] == tea_name: 
                found = True
                break
        
        if found:
            data_filtered.append(tea_obj)
    
    data['teas'] = data_filtered
    util.json_write(json_filepath, data)

    # AI (TO COMPLETE)
    for tea_obj in data['teas']:
        if 'tea_desc' not in tea_obj:
            tea_name = tea_obj['tea_name']
            prompt = f'''
                Explain in a 5-sentence paragraph why {tea_name} tea helps with {condition_name}.
            '''  
            reply = utils_ai.gen_reply(prompt)
            tea_obj['tea_desc'] = reply
            util.json_write(json_filepath, data)
            time.sleep(30)

    # HTML
    html_filepath = f'website/herbalism/tea/{condition_slug}.html'

    data = util.json_read(json_filepath)

    article_html = ''
    article_html += f'<h1>{title}</h1>\n'
    if 'intro' in data:
        article_html += f'<p>{data["intro"]}</p>\n'
    
    i = 0
    for tea_obj in data['teas'][:remedy_num]:
        i += 1
        tea_name = tea_obj['tea_name'].strip().lower()
        tea_slug = tea_name.replace(' ', '-').replace("'", '-').replace('.', '-')
        tea_desc = tea_obj['tea_desc']
        tea_image_url = f'/images/herbal-tea-for-{condition_slug}-{tea_slug}.jpg'
        article_html += f'<h2>{i}. {tea_name.title()}</h2>\n'
        if os.path.exists(f'website{tea_image_url}'):
            article_html += f'<img src="/images/herbal-tea-for-{condition_slug}-{tea_slug}.jpg">\n'
        else:
            print(f'IMG MISSING: {tea_image_url}')
        article_html += f'<p>{tea_desc}</p>\n'

    header_html = util.header_default()
    breadcrumbs_html = util.breadcrumbs(html_filepath)
    meta_html = util.article_meta(article_html)
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

    # print(data)

    break


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
        
        # TODO: gen ai desc for conditions here?

util.json_write(json_filepath, tea_data)


# HTML
html_filepath = f'website/herbalism/tea.html'

tea_data = util.json_read(json_filepath)
intro = tea_data['intro']

article_html = ''
article_html += f'<h1>{title}</h1>\n'
article_html += f'<p>{intro}</p>\n'

for system_obj in tea_data['systems']:
    system_name = system_obj['system_name']
    article_html += f'<h2>{system_name}</h2>\n'
    for condition_obj in system_obj['system_conditions']:
        condition_name = condition_obj['condition_name']
        article_html += f'<p>{condition_name}</p>\n'

header_html = util.header_default()
breadcrumbs_html = util.breadcrumbs(html_filepath)
meta_html = util.article_meta(article_html)
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
