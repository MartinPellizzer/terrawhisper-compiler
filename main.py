import os
import time
import shutil
import markdown

import g
import util
import utils_ai

problems_rows = util.csv_get_rows(g.CSV_PROBLEMS_FILEPATH)
problems_cols = util.csv_get_cols(problems_rows)
problems_rows = problems_rows[1:]

conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
conditions_cols = util.csv_get_cols(conditions_rows)
conditions_rows = conditions_rows[1:]

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]

herbs_rows = util.csv_get_rows(g.CSV_HERBS_FILEPATH)
herbs_cols = util.csv_get_cols(herbs_rows)
herbs_rows = herbs_rows[1:]

problems_herbs_rows = util.csv_get_rows(g.CSV_PROBLEMS_HERBS_FILEPATH)
problems_herbs_cols = util.csv_get_cols(problems_herbs_rows)
problems_herbs_rows = problems_herbs_rows[1:]


# #########################################################
# CSVs
# #########################################################

def gen_csvs():
    for problem_row in problems_rows:
        problem_id = problem_row[problems_cols['problem_id']].strip().lower()
        problem_slug = problem_row[problems_cols['problem_slug']].strip().lower()
        problem_names = problem_row[problems_cols['problem_names']]
        problem_name = problem_names.split(',')[0].strip().lower()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        problems_herbs_rows = util.csv_get_rows_filtered(
            g.CSV_PROBLEMS_HERBS_FILEPATH, problems_herbs_cols['problem_id'], problem_id
        )

        if problems_herbs_rows != []: continue

        prompt = f'''
            Write a numbered list of 20 medicinal herbs for {problem_name}.
            Write only the names of the herbs, not the descriptions.
            Don't write the parts of the herbs.
        '''
        reply = utils_ai.gen_reply(prompt)

        lines = []
        for line in reply.split('\n'):
            line = line.strip().lower()
            if line == '': continue
            if not line[0].isdigit(): continue
            if '.' not in line: continue
            line = '.'.join(line.split('.')[1:])
            line = line.strip()
            if line == '': continue

            herbs_rows_filtered = util.csv_get_rows_filtered(
                g.CSV_HERBS_FILEPATH, herbs_cols['herb_name_common'], line
            )
            if herbs_rows_filtered != []:
                herb_row = herbs_rows_filtered[0]
                herb_id = herb_row[herbs_cols['herb_id']]
            else:
                herb_id = ''

            lines.append([problem_id, problem_slug, herb_id, line])

        if len(lines) >= 10:
            print('***************************************************')
            print(lines)
            print('***************************************************')
            util.csv_add_rows(g.CSV_PROBLEMS_HERBS_FILEPATH, lines)

        print(problem_id, problem_slug, problem_name)
        time.sleep(g.PROMPT_DELAY_TIME)



# #########################################################
# ARTICLES - PROBLEMS
# #########################################################

def art_problems_intro(json_filepath, data):
    key = 'intro'
    if key not in data:
        problem_name = data['problem_name']
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
            data[key] = reply[0]
            util.json_write(json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)


# TODO: regen all definition, changed prompt
def art_problems_definition(json_filepath, data):
    key = 'definition'
    if key not in data:
        problem_name = data['problem_name']
        prompt = f'''
            Write 1 short paragraph explaining what is {problem_name} and include many examples on how it affects your life.
            Don't mention the casuses of {problem_name}.
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)
        reply = utils_ai.reply_to_paragraphs(reply)
        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply[0]
            util.json_write(json_filepath, data)
        time.sleep(g.PROMPT_DELAY_TIME)


def art_problems_herbs(json_filepath, data):
    herbs_num = 10
    key = 'herbs_desc'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

        problems_herbs_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_PROBLEMS_HERBS_FILEPATH, problems_herbs_cols['problem_id'], problem_id,
        )

        problems_herbs_ids = [
            row[problems_herbs_cols['herb_id']] 
            for row in problems_herbs_rows_filtered
            if row[problems_herbs_cols['problem_id']] == problem_id
        ]

        herbs_rows_filtered = []
        for herb_row in herbs_rows:
            herb_id = herb_row[herbs_cols['herb_id']]
            if herb_id in problems_herbs_ids:
                herbs_rows_filtered.append(herb_row)
                
        herbs_common_names = [row[herbs_cols['herb_name_common']] for row in herbs_rows_filtered]
        herbs_common_names_prompt = ''
        for i, herb_common_name in enumerate(herbs_common_names[:herbs_num]):
            herbs_common_names_prompt += f'{i+1}. {herb_common_name.capitalize()}\n'

        prompt = f'''
            Here is a list of medicinal herbs for {problem_name}:
            {herbs_common_names_prompt}

            For each medicinal herb in the list above, explain in 1 sentence why that herb helps with {problem_name}.
            Reply with a numbered list using the following format: [herb name]: [herb description].
            Never use the following words: can, may, might.
        '''
        reply = utils_ai.gen_reply(prompt)
        # TODO: format and save reply
        time.sleep(g.PROMPT_DELAY_TIME)

        # print(herbs_common_names_prompt)


        # problem_name = data['problem_name']
        # prompt = f'''
        #     Write 1 short paragraph explaining what is {problem_name} and include many examples on how it affects your life.
        #     Don't mention the casuses of bad breath.
        #     Never use the following words: can, may, might.
        # '''
        # reply = utils_ai.gen_reply(prompt)
        # reply = utils_ai.reply_to_paragraphs(reply)
        # print(len(reply))
        # if len(reply) == 1:
        #     print('*******************************************')
        #     print(reply)
        #     print('*******************************************')
        #     data[key] = reply[0]
        #     util.json_write(json_filepath, data)
        # time.sleep(g.PROMPT_DELAY_TIME)


def art_problems():
    for problem_row in problems_rows:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        # TODO: GET PROBLEM_SYSTEM FROM JUNCTION TABLE (to create)
        problem_system_id = problem_row[problems_cols['problem_system_id']]
        problem_system_slug = problem_row[problems_cols['problem_system_slug']]

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue
        if problem_system_id == '': continue
        if problem_system_slug == '': continue

        # if problem_slug != 'bad-breath': continue

        print(problem_id, problem_name)

        # json
        json_filepath = f'database/json/problems/{problem_system_slug}/{problem_slug}.json'

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



        # SECTIONS
        # art_problems_intro(json_filepath, data)
        # art_problems_definition(json_filepath, data)
        art_problems_herbs(json_filepath, data)


        # if data['herbs'] == []:
        #     problems_herbs_rows_filtered = util.csv_get_rows_filtered(
        #         g.CSV_PROBLEMS_HERBS_FILEPATH, problems_herbs_cols['problem_id'], problem_id,
        #     )

        #     problems_herbs_ids = [
        #         row[problems_herbs_cols['herb_id']] 
        #         for row in problems_herbs_rows_filtered
        #         if row[problems_herbs_cols['problem_id']] == problem_id
        #     ]

        #     herbs_rows_filtered = []
        #     for herb_row in herbs_rows:
        #         herb_id = herb_row[herbs_cols['herb_id']]
        #         if herb_id in problems_herbs_ids:
        #             herbs_rows_filtered.append(herb_row)

        #     for herb_row in herbs_rows_filtered:
        #         herb_id = herb_row[herbs_cols['herb_id']]
        #         herb_slug = herb_row[herbs_cols['herb_slug']]
        #         herb_name_common = herb_row[herbs_cols['herb_name_common']]
        #         data['herbs'].append({'herb_id': herb_id, 'herb_name_common': herb_name_common})

        #     util.json_write(json_filepath, data)

        # for herb_obj in data['herbs']:
        #     if 'herb_desc' not in herb_obj:
        #         herb_name_common = herb_obj['herb_name_common']
        #         prompt = f'''
        #             Write 1 short paragraph explaining why {herb_name_common} helps with {problem_name}.
        #             Never use the following words: can, may, might.
        #         '''
        #         reply = utils_ai.gen_reply(prompt)
        #         reply = utils_ai.reply_to_paragraphs(reply)
        #         print(len(reply))
        #         if len(reply) == 1:
        #             print('*******************************************')
        #             print(reply)
        #             print('*******************************************')
        #             herb_obj['herb_desc'] = reply[0]
        #             util.json_write(json_filepath, data)
        #         time.sleep(g.PROMPT_DELAY_TIME)
        #     print(herb_obj)


        # html
        html_filepath = f'website/ailments/{problem_system_slug}/{problem_slug}.html'

        data = util.json_read(json_filepath)

        article_html = ''
        article_html += f'<h1>{title}</h1>\n'
        # article_html += f'{util.text_format_1N1_html(data["intro"])}\n'
        # article_html += f'<h2>What is {data["problem_name"]} and and how it affects your life?</h2>\n'
        # article_html += f'{util.text_format_1N1_html(data["definition"][0])}\n'

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

        break

        # quit()



# #########################################################
# PAGES
# #########################################################

def page_home():
    header = util.header_default()
    
    teas_articles_html = ''
    for condition_row in conditions_rows[:6]:
        condition_name = condition_row[conditions_cols['condition_names']].split(',')[0].strip().lower()
        condition_slug = condition_row[conditions_cols['condition_slugs_prev']].split(',')[0].strip().lower()

        if condition_name == '': continue

        condition_system_id = condition_row[conditions_cols['system_id']].split(',')[0].strip().lower()
        condition_system_slug = util.csv_get_rows_filtered(g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], condition_system_id)[0][systems_cols['system_slug']]

        imagepath = f'/images/herbal-tea-for-{condition_slug}-overview.jpg'
        teas_articles_html += f'''
            <a href="/herbalism/tea/{condition_system_slug}/{condition_slug}.html">
                <div class="card">
                    <img class="card-image"
                        src="{imagepath}" alt=""
                        width="400" height="300">
                    <h3 class="px-16 mt-16">10 Best Herbal Teas For {condition_name.title()}</h3>
                    <p class="px-16 mt-16">Boosts the immune system and fights infections.</p>
                </div>
            </a>
        '''

    

    slug = 'index'

    template = util.file_read(f'templates/{slug}.html')

    template = template.replace('[meta_title]', 'Herbalism & Natural Healing')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[teas_articles]', teas_articles_html)

    util.file_write(f'website/{slug}.html', template)
    
    
def page_start_here():
    slug = 'start-here'
    filepath_in = f'templates/{slug}.html'
    filepath_out = f'website/{slug}.html'

    header = util.header_default()
    breadcrumbs_html = util.breadcrumbs(filepath_out)

    template = util.file_read(filepath_in)
    template = template.replace('[title]', 'Start Your Herbalism Journey Here At TerraWhisper')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    util.file_write(filepath_out, template)


def page_about():
    page_url = 'about'
    article_filepath_out = f'website/{page_url}.html'

    header = util.header_default()
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)
    content = util.file_read(f'static/about.md')
    content = markdown.markdown(content, extensions=['markdown.extensions.tables'])
    
    template = util.file_read('templates/about.html')

    template = template.replace('[title]', 'TerraWhisper | About')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[content]', content)

    util.file_write(article_filepath_out, template)


def page_top_herbs():
    articles_folderpath = 'database/articles/plants'
    plants = util.csv_get_rows('database/tables/plants.csv')
    articles_html = ''

    plants_primary = []
    for plant in plants[1:]:
        latin_name = plant[0].strip().capitalize()
        entity = latin_name.lower().replace(' ', '-')
        filepath_in = f'{articles_folderpath}/{entity}.json'
        data = util.json_read(filepath_in)

        title = data['title']
        common_name = data['common_name']

        article_html = f'''
            <a href="/plants/{entity}.html">
                <div>
                    <img src="/images/{entity}-overview.jpg" alt="">
                    <h3 class="mt-0 mb-0">{latin_name} ({common_name})</h3>
                </div>
            </a>
        '''
        plants_primary.append(article_html)

    articles_html += '<div class="articles">' +'\n'.join(plants_primary) + '</div>'

    page_url = 'top-herbs'
    article_filepath_out = f'website/{page_url}.html'

    header = util.header_default()
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)

    template = util.file_read(f'templates/{page_url}.html')
    template = template.replace('[meta_title]', 'Herbs')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[articles]', articles_html)

    util.file_write(article_filepath_out, template)


def page_plants(regen_csv=False):
    json_filenames_plants_primary_secondary = [filename.lower().strip() for filename in os.listdir('database/articles/plants') if filename.endswith('.json')]
    # json_filenames_plants_treffle = [filename.lower().strip() for filename in os.listdir('database/articles/plants_trefle') if filename.endswith('.json')]
    
    json_filepaths_plants = [] 
    for filename in json_filenames_plants_primary_secondary: json_filepaths_plants.append(f'database/articles/plants/{filename}')
    # for filename in json_filenames_plants_treffle: json_filepaths_plants.append(f'database/articles/plants_trefle/{filename}')

    plants_list = []
    for filepath in json_filepaths_plants:
        filepath_in = f'{filepath}'
        data = util.json_read(filepath_in)
        plant_name = data['latin_name']
        plant_slug = data['entity']
        plants_list.append(f'<a href="/plants/{plant_slug}.html">{plant_name}</a>')

    plants_list = sorted(plants_list)
    plants_html = ''.join(plants_list)

    page_url = 'plants'
    article_filepath_out = f'website/{page_url}.html'
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)

    template = util.file_read(f'templates/{page_url}.html')
    template = template.replace('[title]', 'Plants')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', util.header_default())
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[plants_num]', str(len(json_filepaths_plants)))
    template = template.replace('[items]', plants_html)
    util.file_write(article_filepath_out, template)

    # GENERATE CSV TO DOWNLOAD
    if regen_csv:
        rows = []
        for filepath in json_filepaths_plants:
            slug = filepath.split('/')[-1].split('.')[0].strip().lower()
            rows.append([slug])

        csv_plants_primary = util.csv_get_rows('database/tables/plants.csv')
        csv_plants_secondary = util.csv_get_rows('database/tables/plants-secondary.csv')
        csv_plants_trefle = util.csv_get_rows('database/tables/plants/trefle.csv')

        csv_plants = [] 
        for row in csv_plants_primary: csv_plants.append(row)
        for row in csv_plants_secondary: csv_plants.append(row)
        for row in csv_plants_trefle: csv_plants.append(row)

        rows_final = [['slug', 'scientific_name', 'common_name', 'genus', 'family']]
        for row in rows:
            for csv_plant in csv_plants:
                if csv_plant[0].strip().lower() == row[0].strip().lower():
                    rows_final.append(csv_plant)
                    break

        util.csv_set_rows('website/plants.csv', rows_final, delimiter=',')




# #########################################################
# EXE
# #########################################################

# page_home()
# page_start_here()
# page_about()
# page_top_herbs()
# page_plants(regen_csv=False)

art_problems()

# gen_csvs()


# shutil.copy2('style.css', 'website/style.css')
# shutil.copy2('util.css', 'website/util.css')
# shutil.copy2('assets/images/healing-herbs.jpg', 'website/images/healing-herbs.jpg')