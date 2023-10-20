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
    entity = row[0]
    category = row[1]
    attribute = row[2]
    date = row[3]
    state = row[4]
    latin_name = entity.replace('-', ' ').capitalize()
    print(latin_name)


    filepath = f'database/articles/{entity}.json'

    if os.path.exists(filepath): continue

    text = (f'''
    [
        {{
            "state": "{state}",
            "date": "",
            "post_type": "list",
            "entity": "{entity}",
            "attribute": "{category}/{attribute}",
            "latin_name": "{latin_name}",
            "common_name": "",
            "main_content": [
                {{
                    "title": "Roots",
                    "content": []
                }},
                {{
                    "title": "Stems",
                    "content": []
                }},
                {{
                    "title": "Leaves",
                    "content": []
                }},
                {{
                    "title": "Flowers",
                    "content": []
                }},
                {{
                    "title": "Fruits",
                    "content": []
                }},
                {{
                    "title": "Seeds",
                    "content": []
                }}
            ]
        }}
    ]
    ''')


    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
