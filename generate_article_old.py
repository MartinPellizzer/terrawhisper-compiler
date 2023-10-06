import json
import os
import random
import markdown

for file in os.listdir('tmp_articles'):
    os.remove(f'tmp_articles/{file}')


with open("database.json") as f:
    data = json.loads(f.read())
with open("database/constituents.json") as f:
    constituents_dict = json.loads(f.read())


with open("article_template.md") as f:
    loaded_template = f.read()


def lst_to_txt(lst):
    txt = ''
    if len(lst) == 0: txt = ''
    elif len(lst) == 1: txt = lst[0]
    elif len(lst) == 2: txt = f'{lst[0]} and {lst[1]}'
    else: txt = f'{", ".join(lst[:-1])}, and {lst[-1]}'
    return txt
    

def lst_to_aka(lst):
    txt = ''
    if len(lst) == 0: txt = ''
    elif len(lst) == 1: txt = lst[0]
    elif len(lst) == 2: txt = f'{lst[0]}, as known as {lst[1]},'
    else: txt = f'{lst[0]}, as known as {lst[1]} (or {lst[2]}),'
    return txt
    

def lst_to_blt(lst):
    txt = ''
    for item in lst:
        txt += f'- {item}\n'
    return txt.strip()
    




for plant in data:        
    template = loaded_template
    
    common_names = plant['common_names']
    original_habitats = plant['original_habitats']
    latin_names = plant['latin_names']
    family_name = plant['family_name']
    constituents = plant['constituents']
    actions = plant['actions']
    uses = plant['uses']
    parts_used = plant['parts_used']
    preparations = plant['preparations']
    cautions = plant['cautions']

    template = template.replace('[title]', plant['common_names'][0])
    
    # SECTION INTRO
    template = template.replace('[common_name_1]', plant['common_names'][0])

    txt = lst_to_aka(common_names)
    template = template.replace('[common_names]', txt)

    ltt = lst_to_txt(original_habitats)
    template = template.replace('[habitats]', ltt)

    template = template.replace('[latin_names]', ', '.join(latin_names))
    template = template.replace('[family_name]', family_name)

    # SECTION CONSTITUENTS
    ltt = lst_to_txt(constituents).lower()
    template = template.replace('[list_of_constituents]', ltt)

    benefits_num = 3
    constituents_formatted = []
    for constituent in constituents:
        for c in constituents_dict:
            c_name = c['name']
            if c_name.lower() in constituent.lower():
                benefits = c['benefits']
                benefits_rnd_txt = ''
                if benefits: 
                    random.shuffle(benefits)
                    benefits_rnd_lst = benefits[:benefits_num]
                    benefits_rnd_txt = lst_to_txt(benefits_rnd_lst)
                constituent = f'**{c_name}:** {benefits_rnd_txt}.'
                
        constituents_formatted.append(constituent)

    blt = lst_to_blt(constituents_formatted)
    template = template.replace('[bullet_list_of_constituents]', blt)

    # SECTION ACTIONS
    actions_names = [x['name'] for x in actions]
    ltt = lst_to_txt(actions_names).lower()
    template = template.replace('[list_of_actions]', ltt)
    actions = [f'**{x["name"]}**: {x["desc"]}.' for x in actions]
    blt = lst_to_blt(actions)
    template = template.replace('[bullet_list_of_actions]', blt)

    # SECTION USES
    uses_names = [x['name'] for x in uses]
    ltt = lst_to_txt(uses_names).lower()
    template = template.replace('[list_of_uses]', ltt)
    uses = [f'**{x["name"]}**: {x["desc"]}.' for x in uses]
    blt = lst_to_blt(uses)
    template = template.replace('[bullet_list_of_uses]', blt)

    # SECTION PARTS USED
    blt = lst_to_blt(parts_used)
    template = template.replace('[bullet_list_of_parts_used]', blt)

    # SECTION PREPARATIONS
    blt = lst_to_blt(preparations)
    template = template.replace('[bullet_list_of_preparations]', blt)

    # SECTION CAUTIONS
    blt = lst_to_blt(cautions)
    template = template.replace('[bullet_list_of_cautions]', blt)

    # print(template)

    with open(f'tmp_articles/{common_names[0].lower()}.md', 'a') as f:
        f.write(template)

    # break





with open('tmp_articles/yarrow.md') as f:
    article_md = f.read()

article_html = markdown.markdown(article_md)


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
        <section>
            <div class="container">
                {article_html}
            </div>
        </section>
    </body>

    </html>
'''

with open(f'article_viewer.html', 'w') as f:
    f.write(html)