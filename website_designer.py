import os
import random
import shutil

import g
import util


problems_teas_rows = util.csv_get_rows(g.CSV_PROBLEMS_TEAS_FILEPATH)
problems_teas_cols = util.csv_get_cols(problems_teas_rows)
problems_teas_rows = problems_teas_rows[1:]

problems_systems_rows = util.csv_get_rows(g.CSV_PROBLEMS_SYSTEMS_FILEPATH)
problems_systems_cols = util.csv_get_cols(problems_systems_rows)
problems_systems_rows = problems_systems_rows[1:]

problems_preparations_rows = util.csv_get_rows(g.CSV_PROBLEMS_PREPARATIONS_FILEPATH)
problems_preparations_cols = util.csv_get_cols(problems_preparations_rows)
problems_preparations_rows = problems_preparations_rows[1:]



problems_rows = util.csv_get_rows(g.CSV_PROBLEMS_FILEPATH)
problems_cols = util.csv_get_cols(problems_rows)
problems_rows = problems_rows[1:]

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]

preparations_rows = util.csv_get_rows(g.CSV_PREPARATIONS_FILEPATH)
preparations_cols = util.csv_get_cols(preparations_rows)
preparations_rows = preparations_rows[1:]


def csv_get_system_by_problem(problem_id):
    system_row = []

    problems_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_SYSTEMS_FILEPATH, problems_systems_cols['problem_id'], problem_id,
    )

    if problems_systems_rows_filtered != []:
        problem_system_row = problems_systems_rows_filtered[0]
        system_id = problem_system_row[problems_systems_cols['system_id']]

        systems_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id,
        )

        if systems_rows_filtered != []:
            system_row = systems_rows_filtered[0]

    return system_row


def csv_get_preparations_by_problem(problem_id):
    problems_preparations_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_PREPARATIONS_FILEPATH, problems_preparations_cols['problem_id'], problem_id,
    )

    problems_preparations_ids = [
        row[problems_preparations_cols['preparation_id']] 
        for row in problems_preparations_rows_filtered
        if row[problems_preparations_cols['problem_id']] == problem_id
    ]

    preparations_rows_filtered = []
    for herb_row in preparations_rows:
        herb_id = herb_row[preparations_cols['preparation_id']]
        if herb_id in problems_preparations_ids:
            preparations_rows_filtered.append(herb_row)
            
    return preparations_rows_filtered



teas_articles_filepaths = []

for problem_row in problems_rows:
    problem_id = problem_row[problems_cols['problem_id']]
    problem_slug = problem_row[problems_cols['problem_slug']]
    problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

    if problem_id == '': continue
    if problem_slug == '': continue
    if problem_name == '': continue
    
    preparations_rows_filtered = csv_get_preparations_by_problem(problem_id)
    preparations_names = [row[preparations_cols['preparation_name']] for row in preparations_rows_filtered]
    if 'infusions' not in preparations_names: continue

    system_row = csv_get_system_by_problem(problem_id)

    system_id = system_row[systems_cols['system_id']]
    system_slug = system_row[systems_cols['system_slug']]
    system_name = system_row[systems_cols['system_name']]

    if system_id == '': continue
    if system_slug == '': continue
    if system_name == '': continue

    json_filepath = f'database/json/herbalism/tea/{system_slug}/{problem_slug}.json'
    teas_articles_filepaths.append(json_filepath)

teas_articles_filepaths = teas_articles_filepaths[:4]
print(teas_articles_filepaths[:4])

def article(image, title, desc):
    return f'''
        <div>
            <img class="mb-16" src="{image}" alt="">
            <h3 class="mb-16 text-24">{title}</h3>
            <p class="mb-16">{desc}</p>
            <div>
                <a class="button" href="">Learn More</a>
            </div>
        </div>
    '''

def articles():
    teas_articles_html = []
    for tea_article_filepath in teas_articles_filepaths:
        data = util.json_read(tea_article_filepath)
        problem_slug = data['problem_slug']
        tea_obj = data['remedies_list'][0]
        herb_name_common = tea_obj['herb_name_common']
        herb_name_common_slug = herb_name_common.replace(' ', '-').replace("'", '-')
        
        shutil.copy2(
            f'website/images/herbal-teas-for-{problem_slug}-overview.jpg',
            f'website-new/images/herbal-teas-for-{problem_slug}-overview.jpg',
        )

        image_filepath_out = f'/images/herbal-teas-for-{problem_slug}-overview.jpg'

        title = data['title']
        intro = data['intro'][:150] + '...'

        article_html = article(
            image=image_filepath_out, 
            title=title.title(), 
            desc=intro,
        )

        teas_articles_html.append(article_html)


    articles_html = ''.join(teas_articles_html)

    return f'''
    <section class="articles">
        <h2 class="mb-16 text-32">
            Herbal Teas Articles
        </h2>
        <div class="grid grid-2 gap-32">
            {articles_html}
        </div>
    </section>
    '''

articles = articles()
html = f'''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>Document</title>
</head>

<body>
    <header class="flex container justify-between py-24">
        <a class="decoration-none text-neutral-900" href="">TerraWhisper</a>
        <nav class="flex gap-24">
            <a class="decoration-none text-neutral-900" href="">Herbalism</a>
            <a class="decoration-none text-neutral-900" href="">Ailments</a>
            <a class="decoration-none text-neutral-900" href="">Herbs</a>
            <a class="decoration-none text-neutral-900" href="">About Us</a>
        </nav>
    </header>
    <main class="flex container gap-48">

        <div class="flex-3">
            <section class="mb-96 hero">
                <img class="mb-16" src="images/apothecary-01.jpg" alt="">
                <h1 class="mb-16 text-center text-48">Learn to Use Medicinal Herbs to Heal Physically,
                    Mentally, and
                    Spiritually</h1>
                <p class="mb-16 text-center">Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quibusdam
                    explicabo
                    impedit totam! Facere
                    earum minus provident possimus atque, nulla natus adipisci voluptatibus? Architecto, cupiditate
                    doloremque esse illum repudiandae quos quisquam!</p>
                <div class="text-center">
                    <a class="button" href="">Learn More</a>
                </div>
            </section>
            {articles}
            
            
        </div>

        <div class="flex-1">
            <div class="avatar-card">
                <h2 class="pb-48">Author</h2>
                <img class="mb-16 avatar-img" src="images/leen-drinking-tea-name-1.png" alt="" width="180" height="180">
                <p class="mb-16 text-24 font-bold">Leen Randell</p>
                <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Dolor laboriosam consequuntur?</p>

            </div>
        </div>

    </main>
    <footer></footer>
</body>

</html>
'''

util.file_write('website-new/index-auto.html', html)