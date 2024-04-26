import time
import shutil

import g
import util
import utils_ai

problems_rows = util.csv_get_rows(g.CSV_PROBLEMS_FILEPATH)
problems_cols = util.csv_get_cols(problems_rows)
problems_rows = problems_rows[1:]

for problem_row in problems_rows:
    problem_id = problem_row[problems_cols['problem_id']]
    problem_slug = problem_row[problems_cols['problem_slug']]
    problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

    problem_system_id = problem_row[problems_cols['problem_system_id']]
    problem_system_slug = problem_row[problems_cols['problem_system_slug']]

    if problem_id == '': continue
    if problem_slug == '': continue
    if problem_name == '': continue
    if problem_system_id == '': continue
    if problem_system_slug == '': continue

    print(problem_id, problem_name)

    # json
    json_filepath = f'database/json/problems/{problem_slug}.json'

    util.create_folder_for_filepath(json_filepath)
    util.json_generate_if_not_exists(json_filepath)
    data = util.json_read(json_filepath)

    data['problem_id'] = problem_id
    data['problem_slug'] = problem_slug
    data['problem_name'] = problem_name

    lastmod = util.date_now()
    if 'lastmod' not in data: data['lastmod'] = lastmod
    else: lastmod = data['lastmod'] 

    title = f'What to know about {problem_name} before using medicinal herbs'
    data['title'] = title

    if 'herbs' not in data: data['herbs'] = []

    util.json_write(json_filepath, data)



    key = 'intro'
    if key not in data:
        prompt = f'''
            Write 1 short paragraph about the best herbal teas for {problem_name}.
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)
        reply = utils_ai.reply_to_paragraphs(reply)
        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply
            util.json_write(json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)
        
    key = 'definition'
    if key not in data:
        prompt = f'''
            Write 1 short paragraph explaining what is {problem_name} and why it is important for your life.
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)
        reply = utils_ai.reply_to_paragraphs(reply)
        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply
            util.json_write(json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)





    # html
    html_filepath = f'website/ailments/{problem_system_slug}/{problem_slug}.html'

    data = util.json_read(json_filepath)

    article_html = ''
    article_html += f'<h1>{title}</h1>\n'

    header_html = util.header_default_2()
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

    # break


shutil.copy2('style.css', 'website/style.css')