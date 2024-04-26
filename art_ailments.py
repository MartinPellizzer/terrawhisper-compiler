import time

import g
import util
import utils_ai


def ailments():
    csv_ailments_filepath = 'database/csv/ailments.csv'
    ailments_rows = util.csv_get_rows(csv_ailments_filepath)
    ailments_cols = util.csv_get_cols(ailments_rows)

    csv_ailments_preparations_filepath = 'database/csv/ailments_preparations.csv'
    ailments_preparations_rows = util.csv_get_rows(csv_ailments_preparations_filepath)
    ailments_preparations_cols = util.csv_get_cols(ailments_preparations_rows)

    csv_ailments_herbs_filepath = 'database/csv/ailments_herbs.csv'
    ailments_herbs_rows = util.csv_get_rows(csv_ailments_herbs_filepath)
    ailments_herbs_cols = util.csv_get_cols(ailments_herbs_rows)




    for ailment_row in ailments_rows[1:]:
        ailment_id = ailment_row[ailments_cols['ailment_id']] 
        ailment_name = ailment_row[ailments_cols['ailment_names']].split(',')[0].strip().lower()
        ailment_slug = ailment_row[ailments_cols['ailment_slug']] 

        # csv
        found = False
        for ailment_herb_row in ailments_herbs_rows[1:]:
            ailment_id_tmp = ailment_herb_row[ailments_herbs_cols['ailment_id']]
            if ailment_id == ailment_id_tmp:
                found = True
        
        if not found:
            prompt = f'''
                Write a numbered list of 15 medicinal herbs that helps with {ailment_name}. 
                Write only the names of the herbs, not the descriptions.
                Don't include the parts of herbs, only write the names of the herbs
            '''
            
            reply = utils_ai.gen_reply(prompt)

            lst = []
            lines = reply.split('\n')
            for line in lines:
                line = line.strip().lower()
                if line == '': continue
                if not line[0].isdigit(): continue
                if '.' not in line: continue
                line = '.'.join(line.split('.')[1:])
                line = line.strip()
                if line == '': continue
                lst.append([ailment_id, '', '', line])

            if len(lst) >= 10:
                print('*****************************************************')
                print(lst)
                print('*****************************************************')
                util.csv_add_rows(csv_ailments_herbs_filepath, lst)
                
            time.sleep(g.PROMPT_DELAY_TIME)

        # json
        json_ailments_filepath = f'database/json/ailments/{ailment_slug}.json'

        util.create_folder_for_filepath(json_ailments_filepath)
        util.json_generate_if_not_exists(json_ailments_filepath)
        data = util.json_read(json_ailments_filepath)

        data['ailment_id'] = ailment_id
        data['ailment_slug'] = ailment_slug
        data['ailment_name'] = ailment_name
        data['url'] = f'ailment/{ailment_slug}'

        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 

        title = f'What to know about {ailment_name} before using medicinal herbs'
        data['title'] = title

        if 'herbs' not in data: data['herbs'] = []

        util.json_write(json_ailments_filepath, data)




        # find herbs for ailment
        ailments_herbs_rows_filtered = []
        for ailment_herb_row in ailments_herbs_rows[1:]:
            ailment_id_tmp = ailment_herb_row[ailments_herbs_cols['ailment_id']]
            if ailment_id_tmp == ailment_id:
                ailments_herbs_rows_filtered.append(ailment_herb_row)


        # add herbs in json if not already present
        for ailment_herb_row in ailments_herbs_rows_filtered:
            herb_name = ailment_herb_row[ailments_herbs_cols['herb_name']]
            found = False
            for herb_obj in data['herbs']:
                herb_name_tmp = herb_obj['herb_name']
                if herb_name_tmp == herb_name:
                    found = True
                    break

            if not found:
                data['herbs'].append({'herb_name': herb_name})

        util.json_write(json_ailments_filepath, data)



        # html
        html_ailments_filepath = f'website/ailments/{ailment_slug}.html'

        data = util.json_read(json_ailments_filepath)

        article_html = ''
        article_html += f'<h1>{title}</h1>\n'

        header_html = util.header_default()
        breadcrumbs_html = util.breadcrumbs(html_ailments_filepath)
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

        util.file_write(html_ailments_filepath, html)