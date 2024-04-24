import shutil
import time
import os
import random

import g
import util
import utils_ai
import sitemap


conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
conditions_cols = util.csv_get_cols(conditions_rows)

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)


def delete_old_json_conditions_files():
    conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
    conditions_cols = util.csv_get_header_dict(conditions_rows)

    for tea_condition_json_filename in os.listdir('database/json/herbalism/tea'):
        tea_condition_slug = tea_condition_json_filename.replace('.json', '').lower().strip()
        tea_condition_filepath = f'database/json/herbalism/tea/{tea_condition_json_filename}'
    
        file_to_delete = ''
        found = False
        for condition_row in conditions_rows[1:]:
            condition_slug = condition_row[conditions_cols['condition_slug']].strip().lower()
            to_process = condition_row[conditions_cols['to_process']]

            if to_process == '' and tea_condition_slug == condition_slug: 
                found = True
                file_to_delete = tea_condition_filepath
                break

        if found:
            print(file_to_delete)


def delete_json_teas_fields():
    for condition_row in conditions_rows[1:]:
        condition_slug = condition_row[conditions_cols['condition_slug']]
        json_filepath = f'database/json/herbalism/tea/{condition_slug}.json'
        try: data = util.json_read(json_filepath)
        except: continue
        for tea_obj in data['teas']:
            try: del tea_obj['tea_recipe']
            except: pass
        util.json_write(json_filepath, data)


def delete_json_field(key):
    csv_conditions_filepath = 'database/csv/status/conditions.csv'
    conditions_rows = util.csv_get_rows(csv_conditions_filepath)
    conditions_cols = util.csv_get_header_dict(conditions_rows)

    for condition_row in conditions_rows[1:]:
        condition_slug = condition_row[conditions_cols['condition_slug']]
        json_filepath = f'database/json/herbalism/tea/{condition_slug}.json'
        
        try: data = util.json_read(json_filepath)
        except: continue

        print(json_filepath)
        
        try: del data[key]
        except: pass
        
        util.json_write(json_filepath, data)


########################################################################
# TEAS CONDITIONS
########################################################################

def teas_conditions_pages():
    for condition_row in conditions_rows[1:]:
        condition_id = condition_row[conditions_cols['condition_id']].strip()
        condition_name = condition_row[conditions_cols['condition_names']].strip().lower().split(', ')[0]
        condition_slug = condition_row[conditions_cols['condition_slug']].strip().lower()
        condition_slugs_prev = condition_row[conditions_cols['condition_slugs_prev']].strip().lower()
        condition_classification = condition_row[conditions_cols['condition_classification']].strip().lower()
        condition_pinned = condition_row[conditions_cols['condition_pinned']].strip().lower()
        related_conditions = condition_row[conditions_cols['related_conditions']].strip().lower()
        to_process = condition_row[conditions_cols['to_process']]

        if to_process == '': continue
        if condition_id == '': continue
        if condition_slug == '': continue
        # if condition_classification == 'benefit': continue
        # if condition_name == 'digestive system': continue
        # if condition_name != 'bad breath': continue

        print(f'>> {condition_name}')

        # COPY FILES TO NEW LOCATIONS IF MOVED
        condition_new_filepath = f'database/json/herbalism/tea/{condition_slug}.json'
        if not os.path.exists(condition_new_filepath):
            condition_slug_prev_latest = condition_slugs_prev.split(',')[-1].strip()
            condition_old_filepath = f'database/json/herbalism/tea/{condition_slug_prev_latest}.json'
            if os.path.exists(condition_old_filepath):
                util.create_folder_for_filepath(condition_new_filepath)
                shutil.copy2(condition_old_filepath, condition_new_filepath)

        # if condition_name == 'bladder infection':
        #     print('here')
        #     quit()

        # INIT
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

        # AI INTRO
        key = 'intro'
        if key not in data:
            prompt = f'''
                Write 1 short paragraph about the best herbal teas for {condition_name}.
                Never use the following words: can, may, might.
            '''
            reply = utils_ai.gen_reply(prompt)
            if reply != '':
                data[key] = reply
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)

        # JSON TEAS
        teas_rows = util.csv_get_rows(g.CSV_TEAS_FILEPATH)
        teas_cols = util.csv_get_header_dict(teas_rows)

        # add new
        if 'teas' not in data: data['teas'] = []
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

        # del old
        data_filtered = []
        for tea_obj in data['teas']: 
            found = False
            for tea_row in teas_rows[1:]:
                tea_condition_id = tea_row[teas_cols['condition_id']].strip().lower()
                tea_name = tea_row[teas_cols['tea_name']].strip().lower()
                if tea_condition_id != condition_id: continue
                if tea_obj['tea_name'] == tea_name: 
                    found = True
                    break
            if found:
                data_filtered.append(tea_obj)

        data['teas'] = data_filtered
        util.json_write(json_filepath, data)

        # AI TEAS
        for tea_obj in data['teas'][:remedy_num]:
            tea_name = tea_obj["tea_name"].strip().lower()
            tea_name = f'{tea_name} tea'.replace(' tea tea', ' tea')

            if 'tea_desc' not in tea_obj:
                starting_text = f'{tea_name.capitalize()} helps with {condition_name} because '
                prompt = f'''
                    Explain in a 5-sentence paragraph why {tea_name} helps with {condition_name}.
                    Never use the following words: can, may, might.
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_paragraphs(reply)
                if len(reply) == 1 and reply != '':
                    print('********************************')
                    print(reply)
                    print('********************************')
                    tea_obj['tea_desc'] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)

            if 'tea_parts' not in tea_obj or tea_obj['tea_parts'] == []:
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
                    Write each list element using the following format: [part name]: [part description].
                    Never use the following words: can, may, might.
                '''     
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_list_column(reply)
                if reply != '' and reply != []:
                    print('********************************')
                    print(reply)
                    print('********************************')
                    tea_obj['tea_parts'] = reply
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
                
            key = 'tea_constituents'
            if key not in tea_obj or tea_obj[key] == []:
                prompt = f'''
                    Write a numbered list of the most important medicinal constituents of {tea_name} that help with {condition_name}.
                    Include 1 short sentence description for each of these medicinal constituents, explaining why that medicinal contituent is good for {condition_name}.
                    Include only medicinal constituents that have short names.
                    Don't include the name of the plant in the constituents names.
                    Write each list element using the following format: [constituent name]: [constituent description].
                    Never use the following words: can, may, might.
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_list_column(reply)
                reply = [line.replace('[', '').replace(']', '') for line in reply]
                if reply != '' and reply != []:
                    print('********************************')
                    print(reply)
                    print('********************************')
                    tea_obj[key] = reply
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)

            if 'tea_recipe' not in tea_obj or tea_obj['tea_recipe'] == []:
                prompt = f'''
                    Write a 5-step recipe in list format to make {tea_name} for {condition_name}.
                    Include ingredients dosages and preparations times.
                    Write only 1 sentence for each step.
                    Start each step in the list with an action verb.
                    Don't include optional steps.
                    Never use the following words: can, may, might.
                '''  
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_list(reply)
                if reply != '' and reply != [] and len(reply) == 5:
                    print('********************************')
                    print(reply)
                    print('********************************')
                    tea_obj['tea_recipe'] = reply
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)

            # TODO: gen study
        
        
        if condition_classification != 'demography' and condition_classification != 'animal' and condition_classification == 'benefit':      
            # AI DEFINITION
            key = 'definition'
            if key not in data:
                prompt = f'''
                    Write 1 short paragraph explaining what is {condition_name} and how it impacts people lives.
                    Never use the following words: can, may, might.
                '''
                reply = utils_ai.gen_reply(prompt)
                if reply != '':
                    data[key] = reply
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)

            # AI RELATED PROBLEMS
            related_problems_rows = util.csv_get_rows(g.CSV_RELATED_PROBLEMS_FILEPATH)
            related_problems_cols = util.csv_get_header_dict(related_problems_rows)

            related_problmes_rows_filtered = []
            for related_problem_row in related_problems_rows:
                problem_condition_id = related_problem_row[related_problems_cols['condition_id']]
                if problem_condition_id == condition_id:
                    related_problmes_rows_filtered.append(related_problem_row)
            
            if related_problmes_rows_filtered != []:
                related_problems_names = [row[related_problems_cols['related_problem_name']] for row in related_problmes_rows_filtered]
                related_problems_names_formatted = '\n- '.join(related_problems_names)

                key = 'related_problems'
                if key not in data:
                    prompt = f'''
                        Write a numbered list explaining why people with {condition_name} also experience the following problems:
                        {related_problems_names_formatted}.
                        Write the list items using the following structure: [related problem]: [explanation].
                        Never use the following words: can, may, might.
                    '''
                    reply = utils_ai.gen_reply(prompt)
                    reply = utils_ai.reply_to_list_column(reply)
                    if reply != []:
                        print('********************************')
                        print(reply)
                        print('********************************')
                        data[key] = reply
                        util.json_write(json_filepath, data)
                    time.sleep(g.PROMPT_DELAY_TIME)
            
            # AI OTHER REMEDIES
            key = 'other_remedies'
            if key not in data:
                prompt = f'''
                    Write 1 detailed paragraph about what are the most common and effective natural remedies for {condition_name}.
                    Don't include herbal teas.
                    Never use the following words: can, may, might.
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_paragraphs(reply)
                if reply != [] and len(reply) == 1:
                    print('********************************')
                    print(reply)
                    print('********************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)


        # HTML
        html_filepath = f'website/herbalism/tea/{condition_slug}.html'

        data = util.json_read(json_filepath)
        condition_slugs_prev = condition_row[conditions_cols['condition_slugs_prev']].strip().lower()

        article_html = ''
        article_html += f'<h1>{title}</h1>\n'

        # pil image
        tea_obj = data['teas'][0]
        tea_name = tea_obj['tea_name'].strip().lower()
        tea_slug = tea_name.replace(' ', '-').replace("'", '-').replace('.', '-')

        images_folderpath = f'C:/terrawhisper-assets/images/tea/{tea_slug}'
        if os.path.exists(images_folderpath):
            images_filepaths = [f'{images_folderpath}/{filename}' for filename in os.listdir(images_folderpath)] 
            image_filepath = random.choice(images_filepaths)
            if image_filepath != '':
                image_condition_slug = condition_slug.split('/')[-1]
                image_filepath_out = f'website/images/herbal-tea-for-{image_condition_slug}-overview.jpg'
                if not os.path.exists(image_filepath_out):
                    util.image_variate(image_filepath, image_filepath_out)
        else:
            print(f'IMG FOLDER MISSING: {images_folderpath}')
        
        # html image
        tea_image_url = f'/images/herbal-tea-for-{image_condition_slug}-overview.jpg'
        if os.path.exists(f'website{tea_image_url}'):
            article_html += f'<p><img src="{tea_image_url}"><p>\n'
        else:
            print(f'IMG MISSING: {tea_slug}')

        try: article_html += f'<p>{util.text_format_1N1_html(data["intro"])}</p>\n'
        except: print(f'MISSING INTRO: {condition_name}')

        
        i = 0
        for tea_obj in data['teas'][:remedy_num]:
            i += 1
            tea_name = tea_obj['tea_name'].strip().lower()
            tea_slug = tea_name.replace(' ', '-').replace("'", '-').replace('.', '-')

            article_html += f'<h2>{i}. {tea_name.title()}</h2>\n'
            
            key = 'tea_desc'
            try: article_html += f'<p>{util.text_format_1N1_html(tea_obj[key])}</p>\n'
            except: print(f'MISSING TEA DESC: {condition_name} >> {tea_name}')

            # img
            images_folderpath = f'C:/terrawhisper-assets/images/tea/{tea_slug}'
            if os.path.exists(images_folderpath):
                images_filepaths = [f'{images_folderpath}/{filename}' for filename in os.listdir(images_folderpath)] 
                image_filepath = random.choice(images_filepaths)
                if image_filepath != '':
                    image_condition_slug = condition_slug.split('/')[-1]
                    image_filepath_out = f'website/images/herbal-tea-for-{image_condition_slug}-{tea_slug}.jpg'
                    if not os.path.exists(image_filepath_out):
                        util.image_variate(image_filepath, image_filepath_out)
            else:
                print(f'IMG FOLDER MISSING: {images_folderpath}')
            tea_image_url = f'/images/herbal-tea-for-{image_condition_slug}-{tea_slug}.jpg'
            if os.path.exists(f'website{tea_image_url}'):
                article_html += f'<p><img src="{tea_image_url}"><p>\n'
            else:
                print(f'MISSING TEA IMAGE: {condition_name} >> {tea_name}')
                
            try:
                tea_parts = tea_obj['tea_parts']
                article_html += f'<p>Right below you will find a list of the most important active constituents in {tea_name} tea that help with {condition_name}.</p>\n'
                article_html += '<ul>\n'
                for tea_part in tea_parts:
                    chunk_1 = tea_part.split(': ')[0]
                    chunk_2 = ': '.join(tea_part.split(': ')[1:])
                    article_html += f'<li><strong>{chunk_1}</strong>: {chunk_2}</li>\n'
                article_html += '</ul>\n'
            except: print(f'MISSING TEA PARTS: {condition_name} >> {tea_name}')

            try:
                tea_constituents = tea_obj['tea_constituents']
                article_html += f'<p>The list below shows the primary active constituents in {tea_name} tea that help with {condition_name}.</p>\n'
                article_html += '<ul>\n'
                for tea_constituent in tea_constituents:
                    chunk_1 = tea_constituent.split(': ')[0]
                    chunk_2 = ': '.join(tea_constituent.split(': ')[1:])
                    article_html += f'<li><strong>{chunk_1}</strong>: {chunk_2}</li>\n'
                article_html += '</ul>\n'
            except: print(f'MISSING TEA CONSTITUENTS: {condition_name} >> {tea_name}')

            try:
                tea_recipe = tea_obj['tea_recipe']
                article_html += f'<p>The following recipe gives a procedure to make a basic {tea_name} tea for {condition_name}.</p>\n'
                article_html += '<ol>\n'
                for step in tea_recipe:
                    article_html += f'<li>{step}</li>\n'
                article_html += '</ol>\n'
            except: print(f'MISSING TEA RECIPE: {condition_name} >> {tea_name}')
 
        if condition_classification != 'demography' and condition_classification != 'animal':
            key = 'definition'
            if key in data:
                article_html += f'<h2>What is {condition_name} and how can it affect your life?</h2>\n'
                article_html += f'<p>{util.text_format_1N1_html(data[key])}</p>\n'
            else:
                print(f'MISSING DEFINITION: {condition_name}')

            key = 'other_remedies'
            if key in data:
                article_html += f'<h2>What other natural remedies help with {condition_name}?</h2>\n'
                article_html += f'<p>{util.text_format_1N1_html(data[key])}</p>\n'
            else:
                print(f'MISSING OTHER REMEDIES: {condition_name}')
                
            key = 'related_problems'
            if key in data:
                article_html += f'<h2>What other health issues people with {condition_name} are likely to experience?</h2>\n'
                article_html += f'<p>The issues people with {condition_name} are likely to experiece are listed below.</p>\n'
                article_html += '<ul>\n'
                for item in data[key]:
                    chunk_1 = item.split(': ')[0]

                    # get related condition link
                    condition_slug_link = ''
                    for condition_row_tmp in conditions_rows[1:]:
                        condition_names_tmp = condition_row_tmp[conditions_cols['condition_names']].strip().lower().split(', ')
                        condition_slug_tmp = condition_row_tmp[conditions_cols['condition_slug']].strip().lower()
                        if chunk_1.strip().lower() in condition_names_tmp:
                            condition_slug_link = condition_slug_tmp
                            break

                    chunk_2 = ': '.join(item.split(': ')[1:])
                    if condition_slug_link != '': article_html += f'<li><a href="/herbalism/tea/{condition_slug_link}.html"><strong>{chunk_1}</strong></a>: {chunk_2}</li>\n'
                    else: article_html += f'<li><strong>{chunk_1}</strong>: {chunk_2}</li>\n'
                article_html += '</ul>\n'
            else:
                print(f'MISSING RELATED PROBLEMS: {condition_name}')

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

        # REDIRECTS
        condition_slugs_prev_list = condition_slugs_prev.split(',')
        for condition_slug_prev in condition_slugs_prev_list:
            print(condition_slug_prev)
            if condition_slug_prev == condition_slug: continue
            html_filepath_out = f'website/herbalism/tea/{condition_slug_prev}.html'
            html_filepath_web = f'https://terrawhisper.com/herbalism/tea/{condition_slug}.html'
            html = util.file_read(html_filepath_out)
            if os.path.exists(html_filepath_out):
                if f'<meta http-equiv="refresh" content="0; url={html_filepath_web}">' not in html:
                    html = html.replace(
                        '<head>',
                        f'<head>\n<meta http-equiv="refresh" content="0; url={html_filepath_web}">'
                    )
            util.file_write(html_filepath_out, html)



########################################################################
# TEA SYSTEMS PAGE
########################################################################

def teas_systems_page():
    for system_row in systems_rows[1:]:
        system_id = system_row[systems_cols['system_id']].strip().lower()
        system_slug = system_row[systems_cols['system_slug']].strip().lower()
        system_name = system_row[systems_cols['system_name']].strip().lower()

        print(f'>> {system_slug}')

        json_filepath = f'database/json/herbalism/tea/{system_slug}.json'

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)

        data['system_id'] = system_id
        data['system_name'] = system_name
        data['system_slug'] = system_slug
        data['url'] = f'herbalism/tea/{system_slug}'

        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod']

        title = f'Herbal tea for the {system_name}'
        # title = f'Herbal tea for the {system_name}: x health problems solved by medicinal infusions'
        data['title'] = title

        util.json_write(json_filepath, data)

        # AI INTRO
        key = 'intro'
        if key not in data:
            prompt = f'''
                Write 1 short paragraph about the best herbal teas for the {system_name}.
                Never use the following words: can, may, might.
            '''
            reply = utils_ai.gen_reply(prompt)
            if reply != '':
                data[key] = reply
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)

        key = 'conditions'
        if key not in data: data[key] = []
        for condition_row in conditions_rows[1:]:
            condition_id = condition_row[conditions_cols['condition_id']].strip().lower()
            condition_slug = condition_row[conditions_cols['condition_slug']].strip().lower()
            condition_name = condition_row[conditions_cols['condition_names']].split(',')[0].strip().lower()
            condition_system_id = condition_row[conditions_cols['system_id']].strip().lower()
            if condition_slug == '': continue
            if condition_system_id != system_id: continue
            found = False
            for condition_obj in data[key]:
                if condition_obj['condition_name'] == condition_name:
                    found = True
                    break
            if not found:
                data[key].append({
                    'condition_id': condition_id,
                    'condition_slug': condition_slug,
                    'condition_name': condition_name,
                })
        util.json_write(json_filepath, data)

        # TODO: code to delete from json conditions that are removed from csv

        for condition_obj in data['conditions']:
            key = 'tea_desc'
            if key not in condition_obj:
                condition_name = condition_obj["condition_name"].strip().lower()
                prompt = f'''
                    Explain in a 5-sentence paragraph why herbal tea helps with {condition_name}.
                    Include examples of herbal teas that help with {condition_name}.
                    Include properties and active constituents of herbal teas that help with {condition_name}.
                    Never use the following words: can, may, might.
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_paragraphs(reply)
                if len(reply) == 1 and reply != '':
                    print('********************************')
                    print(reply)
                    print('********************************')
                    condition_obj[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)

        # HTML
        html_filepath = f'website/herbalism/tea/{system_slug}.html'

        data = util.json_read(json_filepath)

        article_html = ''
        article_html += f'<h1>{title}</h1>\n'

        try: article_html += f'<p>{util.text_format_1N1_html(data["intro"])}</p>\n'
        except: print(f'MISSING INTRO: {condition_name}')

        conditions_objs = data['conditions']
        for i, condition_obj in enumerate(conditions_objs):
            condition_name = condition_obj["condition_name"].strip().lower()
            condition_slug = condition_obj["condition_slug"].strip().lower()
            
            article_html += f'<h2>{i+1}. {condition_name.title()}</h2>\n'
            
            image_condition_slug = condition_slug.split('/')[-1]
            image_url = f'/images/herbal-tea-for-{image_condition_slug}-overview.jpg'
            if os.path.exists(f'website{image_url}'):
                article_html += f'<p><img src="{image_url}"><p>\n'
            else:
                print(f'IMG MISSING: {condition_slug}')

            article_html += f'<p>{util.text_format_1N1_html(condition_obj["tea_desc"])}</p>\n'
            article_html += f'<p>Visit the following link to lean more about the <a href="/herbalism/tea/{condition_slug}.html">herbal teas for {condition_name}</a>.</p>\n'

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

        print(html_filepath)
        util.file_write(html_filepath, html)
        




########################################################################
# TEA PAGE
########################################################################
def tea_page():
    json_filepath = f'database/json/herbalism/tea.json'

    util.create_folder_for_filepath(json_filepath)
    util.json_generate_if_not_exists(json_filepath)
    tea_data = util.json_read(json_filepath)
    tea_data['url'] = f'herbalism/tea'
    title = f'What to know before using herbal tea for medicinal purposes'
    tea_data['title'] = title

    lastmod = util.date_now()
    if 'lastmod' not in tea_data: tea_data['lastmod'] = lastmod
    else: lastmod = tea_data['lastmod'] 

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
        time.sleep(g.PROMPT_DELAY_TIME)

    # SYSTEMS
    if 'systems' not in tea_data: tea_data['systems'] = []

    for system_row in systems_rows[1:]:
        system_id = system_row[systems_cols['system_id']].strip()
        system_name = system_row[systems_cols['system_name']].strip().lower()
        system_slug = system_row[systems_cols['system_slug']].strip().lower()

        found = False
        for system_obj in tea_data['systems']:
            if system_obj['system_id'] == system_id:
                found = True
                break

        if not found: 
            if system_name not in tea_data['systems']: 
                tea_data['systems'].append({
                    'system_id': system_id, 
                    'system_name': system_name,
                    'system_slug': system_slug,
                })
            util.json_write(json_filepath, tea_data)

    # AI SYSTEMS CONDITIONS
    # for system_obj in tea_data['systems']:
    #     if 'system_conditions' not in system_obj: system_obj['system_conditions'] = []
    #     system_id = system_obj['system_id']

    #     for condition_row in conditions_rows[1:]:
    #         condition_id = condition_row[conditions_cols['condition_id']]
    #         condition_name = condition_row[conditions_cols['condition_names']].strip().lower().split(', ')[0]
    #         condition_slug = condition_row[conditions_cols['condition_slug']].strip().lower()
    #         condition_classification = condition_row[conditions_cols['condition_classification']]
    #         condition_system_id = condition_row[conditions_cols['system_id']]

    #         to_process = condition_row[conditions_cols['to_process']]
    #         if to_process == '': continue

    #         if system_id != condition_system_id: continue

    #         found = False
    #         for condition_obj in system_obj['system_conditions']:
    #             if condition_obj['condition_id'] == condition_id:
    #                 found = True
    #                 break
            
    #         if not found:
    #             system_obj['system_conditions'].append({
    #                 'condition_id': condition_id, 
    #                 'condition_name': condition_name, 
    #                 'condition_slug': condition_slug,
    #                 'condition_classification': condition_classification,
    #             })
    # util.json_write(json_filepath, tea_data)

    # 
    # for system_obj in tea_data['systems']:
    #     for condition_obj in system_obj['system_conditions']:
    #         if 'condition_desc' not in condition_obj: condition_obj['condition_desc'] = ''
    #         condition_name = condition_obj['condition_name'].strip().lower()
    #         condition_desc = condition_obj['condition_desc'].strip()
    #         if condition_desc == '':
    #             prompt = f'''
    #                 Write 1 sentence explaining what herbal teas can help with {condition_name}.
    #             '''
    #             reply = utils_ai.gen_reply(prompt)
    #             condition_obj['condition_desc'] = reply
    #             util.json_write(json_filepath, tea_data)
    #             time.sleep(g.PROMPT_DELAY_TIME)

    # AI SYSTEMS CONDITIONS DESC    
    for system_obj in tea_data['systems']:
        if 'system_desc' not in system_obj: 
            system_name = system_obj['system_name'].strip().lower()
            prompt = f'''
                Write 1 paragraph explaining what herbal teas help with {system_name}.
                Never use the following words: can, may, might.
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('****************************************************')
                print(reply)
                print('****************************************************')
                system_obj['system_desc'] = reply[0]
                util.json_write(json_filepath, tea_data)
            time.sleep(g.PROMPT_DELAY_TIME)

    # HTML
    html_filepath = f'website/herbalism/tea.html'

    tea_data = util.json_read(json_filepath)
    intro = tea_data['intro']

    article_html = ''
    article_html += f'<h1>{title}</h1>\n'
    article_html += f'<p>{util.text_format_1N1_html(intro)}</p>\n'

    article_html += f'<h2>Which herbal are best for each body system?</h2>\n'
    for i, system_obj in enumerate(tea_data['systems']):
        system_name = system_obj['system_name']
        system_slug = system_obj['system_slug']
        system_desc = system_obj['system_desc']

        if system_name == 'other systems':
            article_html += f'<h3>{i+1}. Herbal teas for {system_name}</h3>\n'
        else:
            article_html += f'<h3>{i+1}. Herbal teas for the {system_name}</h3>\n'

        article_html += f'<p>{util.text_format_1N1_html(system_desc)}</p>\n'

        if system_name == 'other systems':
            article_html += f'<p>Visit the following link to learn more about the <a href="/herbalism/tea/{system_slug}.html">herbal teas for {system_name}</a> and the health conditions related to this system.</p>\n'
        else:
            article_html += f'<p>Visit the following link to learn more about the <a href="/herbalism/tea/{system_slug}.html">herbal teas for the {system_name}</a> and the health conditions related to this system.</p>\n'

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




# def tea_page():
#     conditions_num = 0
#     for condition_row in conditions_rows[1:]:
#         to_process = condition_row[conditions_cols['to_process']].strip().lower()
#         if to_process == '': continue
#         conditions_num += 1

#     # JSON
#     json_filepath = f'database/json/herbalism/tea.json'
#     util.create_folder_for_filepath(json_filepath)
#     util.json_generate_if_not_exists(json_filepath)
#     tea_data = util.json_read(json_filepath)
#     tea_data['url'] = f'herbalism/tea'
#     title = f'herbal tea ({conditions_num})'
#     tea_data['title'] = title

#     lastmod = util.date_now()
#     if 'lastmod' not in tea_data: tea_data['lastmod'] = lastmod
#     else: lastmod = tea_data['lastmod'] 

#     util.json_write(json_filepath, tea_data)

#     # AI
#     if 'intro' not in tea_data:
#         prompt = f'''
#             Write a 5-sentence paragraph about herbal teas for medicinal purposes.
#             Include the definition of herbal teas.
#             Include the medicinal properties of herbal teas.
#             Include examples of what are some of the most used herbal teas.
#             Include examples of the most common health conditions you can heal with herbal teas.
#             Include a simple general procedure to make effective herbal teas.
#             Reply in as few words as possible.
#             Start with the following words: Herbal teas are .
#         '''
#         reply = utils_ai.gen_reply(prompt)
#         tea_data['intro'] = reply
#         util.json_write(json_filepath, tea_data)
#         time.sleep(g.PROMPT_DELAY_TIME)

#     # AI SYSTEMS
#     if 'systems' not in tea_data: tea_data['systems'] = []
#     systems_rows = util.csv_get_rows('database/csv/status/systems.csv')
#     systems_cols = util.csv_get_header_dict(systems_rows)
#     for system_row in systems_rows[1:]:
#         system_id = system_row[systems_cols['system_id']].strip()
#         system_name = system_row[systems_cols['system_name']].strip().lower()
#         found = False
#         for system_obj in tea_data['systems']:
#             if system_obj['system_id'] == system_id:
#                 found = True
#                 break
#         if not found: 
#             if system_name not in tea_data['systems']: tea_data['systems'].append({'system_id': system_id, 'system_name': system_name})
#             util.json_write(json_filepath, tea_data)

#     # AI SYSTEMS CONDITIONS
#     for system_obj in tea_data['systems']:
#         if 'system_conditions' not in system_obj: system_obj['system_conditions'] = []
#         system_id = system_obj['system_id']

#         for condition_row in conditions_rows[1:]:
#             condition_id = condition_row[conditions_cols['condition_id']]
#             condition_name = condition_row[conditions_cols['condition_names']].strip().lower().split(', ')[0]
#             condition_slug = condition_row[conditions_cols['condition_slug']].strip().lower()
#             condition_classification = condition_row[conditions_cols['condition_classification']]
#             condition_system_id = condition_row[conditions_cols['system_id']]

#             to_process = condition_row[conditions_cols['to_process']]
#             if to_process == '': continue

#             if system_id != condition_system_id: continue

#             found = False
#             for condition_obj in system_obj['system_conditions']:
#                 if condition_obj['condition_id'] == condition_id:
#                     found = True
#                     break
            
#             if not found:
#                 system_obj['system_conditions'].append({
#                     'condition_id': condition_id, 
#                     'condition_name': condition_name, 
#                     'condition_slug': condition_slug,
#                     'condition_classification': condition_classification,
#                 })
#     util.json_write(json_filepath, tea_data)

#     # AI SYSTEMS CONDITIONS DESC
#     for system_obj in tea_data['systems']:
#         for condition_obj in system_obj['system_conditions']:
#             if 'condition_desc' not in condition_obj: condition_obj['condition_desc'] = ''
#             condition_name = condition_obj['condition_name'].strip().lower()
#             condition_desc = condition_obj['condition_desc'].strip()
#             if condition_desc == '':
#                 prompt = f'''
#                     Write 1 sentence explaining what herbal teas can help with {condition_name}.
#                 '''
#                 reply = utils_ai.gen_reply(prompt)
#                 condition_obj['condition_desc'] = reply
#                 util.json_write(json_filepath, tea_data)
#                 time.sleep(g.PROMPT_DELAY_TIME)

#     # HTML
#     html_filepath = f'website/herbalism/tea.html'

#     tea_data = util.json_read(json_filepath)
#     intro = tea_data['intro']

#     article_html = ''
#     article_html += f'<h1>{title}</h1>\n'
#     article_html += f'<p>{intro}</p>\n'

#     for system_obj in tea_data['systems']:
#         system_name = system_obj['system_name']
#         article_html += f'<h2>Herbal Teas For The {system_name.title()} System</h2>\n'
#         article_html += f'<ul>\n'
#         for condition_obj in system_obj['system_conditions']:
#             condition_name = condition_obj['condition_name'].strip().title()
#             condition_slug = condition_obj['condition_slug'].strip().lower()
#             condition_desc = condition_obj['condition_desc'].strip()
#             article_html += f'<li><strong><a href="/herbalism/tea/{condition_slug}.html">Herbal Teas For {condition_name}</a></strong>: {condition_desc}</li>\n'
#         article_html += f'</ul>\n'

#     header_html = util.header_default()
#     breadcrumbs_html = util.breadcrumbs(html_filepath)
#     meta_html = util.article_meta(article_html, lastmod)
#     article_html = util.article_toc(article_html)

#     html = f'''
#         <!DOCTYPE html>
#         <html lang="en">

#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <meta name="author" content="{g.AUTHOR_NAME}">
#             <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
#             <link rel="stylesheet" href="/style.css">
#             <title>{title}</title>
#             {g.GOOGLE_TAG}
            
#         </head>

#         <body>
#             {header_html}
#             {breadcrumbs_html}
            
#             <section class="article-section">
#                 <div class="container">
#                     {meta_html}
#                     {article_html}
#                 </div>
#             </section>

#             <footer>
#                 <div class="container-lg">
#                     <span>© TerraWhisper.com 2024 | All Rights Reserved
#                 </div>
#             </footer>
#         </body>

#         </html>
#     '''

#     util.file_write(html_filepath, html)


# action = input('''
# enter and action from the following:

# 1. clean old json files
# 2. delete json field

# >> ''')

# if action == '1':
#     delete_old_json_conditions_files()
# elif action == '2':
#     field_name = input('enter field name >> ')
#     delete_json_field(field_name)

# quit()


teas_conditions_pages()
# teas_systems_page()
# tea_page()


# sitemap.sitemap_all()
# shutil.copy2('sitemap.xml', 'website/sitemap.xml')
# shutil.copy2('style.css', 'website/style.css')