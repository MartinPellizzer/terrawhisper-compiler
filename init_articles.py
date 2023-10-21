import os 
import sys
import csv

rows = []
with open('database/tables/articles.csv', newline='') as f:
    reader = csv.reader(f, delimiter='\\')
    for row in reader:
        rows.append(row)
rows = rows[1:]

print(len(rows))
for row in rows:
    entity = row[0].strip().lower().replace(' ', '-')
    category = row[1].strip().lower().replace(' ', '-')
    attribute = row[2].strip().lower().replace(' ', '-')
    date = row[3]
    state = row[4]
    latin_name = entity.replace('-', ' ').capitalize()
    print(latin_name)

    try: os.mkdir(f'database/articles/{entity}')
    except: pass
    try: os.mkdir(f'database/articles/{entity}/{category}')
    except: pass
    try: os.mkdir(f'database/articles/{entity}/{category}/{attribute}')
    except: pass

    folderpath = f'database/articles/{entity}/{category}/{attribute}'
    if attribute == 'morphology':
        with open(f'{folderpath}/roots.md', 'a', encoding='utf-8') as f: pass
        with open(f'{folderpath}/stems.md', 'a', encoding='utf-8') as f: pass
        with open(f'{folderpath}/rhizomes.md', 'a', encoding='utf-8') as f: pass
        with open(f'{folderpath}/leaves.md', 'a', encoding='utf-8') as f: pass
        with open(f'{folderpath}/flowers.md', 'a', encoding='utf-8') as f: pass
        with open(f'{folderpath}/fruits.md', 'a', encoding='utf-8') as f: pass
        with open(f'{folderpath}/seeds.md', 'a', encoding='utf-8') as f: pass
    elif attribute == 'taxonomy':
        with open(f'{folderpath}/taxonomy.md', 'a', encoding='utf-8') as f: pass
    elif attribute == 'symbology':
        with open(f'{folderpath}/symbology.md', 'a', encoding='utf-8') as f: pass


    # filepath = f'database/articles/{entity}.json'

    # if os.path.exists(filepath): continue

    # text = (f'''
    # [
    #     {{
    #         "state": "{state}",
    #         "date": "",
    #         "post_type": "list",
    #         "entity": "{entity}",
    #         "attribute": "{category}/{attribute}",
    #         "latin_name": "{latin_name}",
    #         "common_name": "",
    #         "main_content": [
    #             {{
    #                 "title": "Roots",
    #                 "content": []
    #             }},
    #             {{
    #                 "title": "Stems",
    #                 "content": []
    #             }},
    #             {{
    #                 "title": "Leaves",
    #                 "content": []
    #             }},
    #             {{
    #                 "title": "Flowers",
    #                 "content": []
    #             }},
    #             {{
    #                 "title": "Fruits",
    #                 "content": []
    #             }},
    #             {{
    #                 "title": "Seeds",
    #                 "content": []
    #             }}
    #         ]
    #     }}
    # ]
    # ''')


    # with open(filepath, 'w', encoding='utf-8') as f:
    #     f.write(text)
