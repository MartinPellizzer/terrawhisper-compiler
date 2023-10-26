import os 
import csv

rows = []
with open('database/tables/articles.csv', newline='') as f:
    reader = csv.reader(f, delimiter='\\')
    for row in reader:
        rows.append(row)
rows = rows[1:]

entities = [x[0].strip().lower().replace(' ', '-') for x in rows]

print(len(rows))
for entity in entities:
    print(entity)
    try: os.mkdir(f'database/articles/{entity}')
    except: pass
    try: os.mkdir(f'database/articles/{entity}/botany')
    except: pass
    try: os.mkdir(f'database/articles/{entity}/botany/morphology')
    except: pass

    folderpath = f'database/articles/{entity}/botany/morphology'
    with open(f'{folderpath}/_intro.md', 'a', encoding='utf-8') as f: pass
    with open(f'{folderpath}/roots.md', 'a', encoding='utf-8') as f: pass
    with open(f'{folderpath}/stems.md', 'a', encoding='utf-8') as f: pass
    with open(f'{folderpath}/rhizomes.md', 'a', encoding='utf-8') as f: pass
    with open(f'{folderpath}/bulbs.md', 'a', encoding='utf-8') as f: pass
    with open(f'{folderpath}/leaves.md', 'a', encoding='utf-8') as f: pass
    with open(f'{folderpath}/flowers.md', 'a', encoding='utf-8') as f: pass
    with open(f'{folderpath}/fruits.md', 'a', encoding='utf-8') as f: pass
    with open(f'{folderpath}/seeds.md', 'a', encoding='utf-8') as f: pass
    
    try: os.mkdir(f'database/articles/{entity}/botany/taxonomy')
    except: pass
    with open(f'database/articles/{entity}/botany/taxonomy/taxonomy.md', 'a', encoding='utf-8') as f: pass
    with open(f'database/articles/{entity}/botany/taxonomy/common-names.md', 'a', encoding='utf-8') as f: pass
    with open(f'database/articles/{entity}/botany/taxonomy/varieties.md', 'a', encoding='utf-8') as f: pass
    with open(f'database/articles/{entity}/botany/taxonomy/morphology.md', 'a', encoding='utf-8') as f: pass
    
    # try: os.mkdir(f'database/articles/{entity}/botany/symbology')
    # except: pass
    # with open(f'database/articles/{entity}/botany/symbology/symbology.md', 'a', encoding='utf-8') as f: pass
