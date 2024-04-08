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
    condition_name = condition_row[conditions_cols['condition_name']]
    condition_slug = condition_row[conditions_cols['condition_slug']]
    system_id = condition_row[conditions_cols['system_id']]
    condition_classification = condition_row[conditions_cols['condition_classification']]
    title = f'What to know about {condition_name} before using medicinal herbs'
    regen = condition_row[conditions_cols['regen']].strip()
    if regen == '': regen = False
    else: regen = True


    # SKIP IF ROW IS EITHER INVALID OR NOT YET MANAGED
    if condition_id == '': continue
    if condition_classification != 'symptom': continue


    # CSV DATA TO JSON
    json_filepath = f'database/articles/conditions/{condition_slug}.json'
    util.json_generate_if_not_exists(json_filepath)
    data = util.json_read(json_filepath)
    
    if 'condition_id' not in data: data['condition_id'] = condition_id
    if 'condition_name' not in data: data['condition_name'] = condition_name
    if 'condition_slug' not in data: data['condition_slug'] = condition_slug
    if 'title' not in data: data['title'] = title

    if (
        data['condition_id'] != condition_id or 
        data['condition_name'] != condition_name or
        data['condition_slug'] != condition_slug
        ): regen = True 

    data['condition_id'] = condition_id
    data['condition_name'] = condition_name
    data['condition_slug'] = condition_slug
    data['title'] = title
    # data = {item: data[item] for item in ['condition_id', 'condition_name', 'condition_slug', 'title', 'intro']}
    util.json_write(json_filepath, data)



    # AI
    # ------------------------------------------------------------------------------------
    failed_regen = False

    if 'intro' not in data or regen == True:
        prompt = f'''
            Write 1 short paragraph about {condition_name}.
        '''
        reply = utils_ai.gen_reply(prompt)

        if reply != '':
            data['intro'] = reply
            util.json_write(json_filepath, data)
        else:
            failed_regen = True
        
        time.sleep(30)
            
    if 'definition' not in data or regen == True:
        prompt = f'''
            Write a 5-sentence paragraph about {condition_name}.
            Include a detailed definition of what {condition_name} is.
            Include a description about the impact that {condition_name} has on human health.
        '''
        reply = utils_ai.gen_reply(prompt)

        if reply != '':
            data['definition'] = reply
            util.json_write(json_filepath, data)
        else:
            failed_regen = True
            
        time.sleep(30)
            
    if 'causes' not in data or regen == True:
        prompt = f'''
            Write a 5-sentence paragraph explaing what are the causes of {condition_name}.
        '''
        reply = utils_ai.gen_reply(prompt)

        if reply != '':
            data['causes'] = reply
            util.json_write(json_filepath, data)
        else:
            failed_regen = True
            
        time.sleep(30)
            
    if 'herbal_remedies' not in data or regen == True:
        prompt = f'''
            Write a 5-sentence paragraph explaing what are the herbal remedies for {condition_name}.
        '''
        reply = utils_ai.gen_reply(prompt)

        if reply != '':
            data['herbal_remedies'] = reply
            util.json_write(json_filepath, data)
        else:
            failed_regen = True
            
        time.sleep(30)
            
    if 'other_remedies' not in data or regen == True:
        prompt = f'''
            Write a 5-sentence paragraph explaing what are the natural remedies and lifestyle changes to help reduce {condition_name}.
            Don't include herbs and herbal remedies.
        '''
        reply = utils_ai.gen_reply(prompt)

        if reply != '':
            data['other_remedies'] = reply
            util.json_write(json_filepath, data)
        else:
            failed_regen = True
            
        time.sleep(30)
            
    if 'associated_symptoms' not in data or regen == True:
        prompt = f'''
            Write a 5-sentence paragraph explaing what are other symptoms associated with {condition_name}.
        '''
        reply = utils_ai.gen_reply(prompt)

        if reply != '':
            data['associated_symptoms'] = reply
            util.json_write(json_filepath, data)
        else:
            failed_regen = True
            
        time.sleep(30)


    if failed_regen:
        condition_row[conditions_cols['regen']] = 'x'
        util.csv_set_rows(csv_filepath, conditions_rows)
    else:
        condition_row[conditions_cols['regen']] = ''
        util.csv_set_rows(csv_filepath, conditions_rows)



    # HTML
    # ------------------------------------------------------------------------------------
    html_filepath = f'website/conditions/{condition_slug}.html'

    data = util.json_read(json_filepath)

    article_html = ''
    article_html += f'<h1>{title}</h1>\n'
    if 'intro' in data:
        article_html += f'<p>{data["intro"]}</p>\n'
    if 'definition' in data:
        article_html += f'<h2>What is {condition_name} and how it affects your life?</h2>\n'
        article_html += f'<p>{data["definition"]}</p>\n'
    if 'causes' in data:
        article_html += f'<h2>What are the primary causes of {condition_name}?</h2>\n'
        article_html += f'<p>{data["causes"]}</p>\n'
    if 'herbal_remedies' in data:
        article_html += f'<h2>What are the most common herbal remedies for {condition_name}?</h2>\n'
        article_html += f'<p>{data["herbal_remedies"]}</p>\n'
    if 'other_remedies' in data:
        article_html += f'<h2>What other natural remedies and lifestyle changes reduce {condition_name}?</h2>\n'
        article_html += f'<p>{data["other_remedies"]}</p>\n'
    if 'associated_symptoms' in data:
        article_html += f'<h2>What symptoms associated with {condition_name} negatively impact your health?</h2>\n'
        article_html += f'<p>{data["associated_symptoms"]}</p>\n'

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

    print(data)
    # break