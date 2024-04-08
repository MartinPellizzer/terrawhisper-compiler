import time

import g
import util
import utils_ai

csv_filepath = 'database/tables/conditions/conditions.csv'
conditions_rows = util.csv_get_rows(csv_filepath)
conditions_cols = util.csv_get_header_dict(conditions_rows)

for condition_row in conditions_rows[1:]:

    # GET CONDITION DATA
    condition_id = condition_row[conditions_cols['condition_id']].strip()
    condition_name = condition_row[conditions_cols['condition_name']].strip().lower()
    condition_slug = condition_row[conditions_cols['condition_slug']]
    condition_classification = condition_row[conditions_cols['condition_classification']]
    remedy_num = 10
    title = f'{remedy_num} best herbal teas for {condition_name}'

    # SKIP IF ROW IS EITHER INVALID OR NOT YET MANAGED
    if condition_id == '': continue
    if condition_classification != 'symptom': continue

    # print(condition_id)
    # print(condition_name)
    # print(condition_slug)
    
    json_filepath = f'database/articles/herbalism/tea/{condition_slug}.json'
    util.json_generate_if_not_exists(json_filepath)
    data = util.json_read(json_filepath)
    data['condition_name'] = condition_name
    data['condition_slug'] = condition_slug
    data['url'] = f'herbalism/tea/{condition_slug}'
    data['remedy_num'] = remedy_num
    data['title'] = title
    if 'teas' not in data: data['teas'] = []
    util.json_write(json_filepath, data)


    # AI
    # ------------------------------------------------------------------------------------
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
            

    # INIT/CLEAN LIST OF TEAS (TO REFACTOR FOR GOD SAKE!!!)
    teas_rows = util.csv_get_rows('database/tables/herbalism/teas_conditions.csv')
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
            print(tea_obj)
    
    data['teas'] = data_filtered
    util.json_write(json_filepath, data)


    # AI GEN FOR EACH TEA (TO COMPLETE)
    for tea_obj in data['teas']:
        if 'tea_desc' not in tea_obj:
            tea_name = tea_obj['tea_name']
            prompt = f'''
                Explain in a 5-sentence paragraph why {tea_name} tea helps with {condition_name}.
            '''  
            reply = utils_ai.gen_reply(prompt)

            if reply != '':
                tea_obj['tea_desc'] = reply
                util.json_write(json_filepath, data)
            else:
                failed_regen = True
            
            time.sleep(30)




    # HTML
    # ------------------------------------------------------------------------------------
    html_filepath = f'website/herbalism/tea/{condition_slug}.html'

    data = util.json_read(json_filepath)

    article_html = ''
    article_html += f'<h1>{title}</h1>\n'
    if 'intro' in data:
        article_html += f'<p>{data["intro"]}</p>\n'

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