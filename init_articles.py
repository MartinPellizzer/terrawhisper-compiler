import os 
import csv
import sys
import utils

entity_arg = None
if len(sys.argv) == 2:
    entity_arg = sys.argv[1]


rows = []
with open('database/tables/articles.csv', newline='') as f:
    reader = csv.reader(f, delimiter='\\')
    for row in reader:
        rows.append(row)
rows = rows[1:]

entities = [x[0].strip().lower().replace(' ', '-') for x in rows]

print(len(rows))
for entity in entities:
    if entity_arg:
        if entity_arg.strip() != entity.strip():
            continue
    # print(entity)
    # try: os.mkdir(f'database/articles/{entity}')
    # except: pass
    # try: os.mkdir(f'database/articles/{entity}/botany')
    # except: pass
    # try: os.mkdir(f'database/articles/{entity}/botany/morphology')
    # except: pass

    # folderpath = f'database/articles/{entity}/botany/morphology'
    # with open(f'{folderpath}/_intro.md', 'a', encoding='utf-8') as f: pass
    # with open(f'{folderpath}/roots.md', 'a', encoding='utf-8') as f: pass
    # with open(f'{folderpath}/stems.md', 'a', encoding='utf-8') as f: pass
    # with open(f'{folderpath}/rhizomes.md', 'a', encoding='utf-8') as f: pass
    # with open(f'{folderpath}/bulbs.md', 'a', encoding='utf-8') as f: pass
    # with open(f'{folderpath}/leaves.md', 'a', encoding='utf-8') as f: pass
    # with open(f'{folderpath}/flowers.md', 'a', encoding='utf-8') as f: pass
    # with open(f'{folderpath}/fruits.md', 'a', encoding='utf-8') as f: pass
    # with open(f'{folderpath}/seeds.md', 'a', encoding='utf-8') as f: pass

    
    # with open(f'database/articles/{entity}/_intro.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botanical.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/medicinal.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/culinary.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/horticultural.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/history-folklore.md', 'a', encoding='utf-8') as f: pass

    # health
    try: os.mkdir(f'database/articles/{entity}/medicine/')
    except: pass
    with open(f'database/articles/{entity}/medicine/_intro.md', 'a', encoding='utf-8') as f: pass
    with open(f'database/articles/{entity}/medicine/benefits.md', 'a', encoding='utf-8') as f: pass
    with open(f'database/articles/{entity}/medicine/constituents.md', 'a', encoding='utf-8') as f: pass
    with open(f'database/articles/{entity}/medicine/preparations.md', 'a', encoding='utf-8') as f: pass
    with open(f'database/articles/{entity}/medicine/precautions.md', 'a', encoding='utf-8') as f: pass


    # benefits
    try: os.mkdir(f'database/articles/{entity}/medicine/benefits/')
    except: pass
    with open(f'database/articles/{entity}/medicine/benefits/_intro.md', 'a', encoding='utf-8') as f: pass
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
    rows_filtered = [f'{x[1]}' for x in rows[:10]]
    for i, item in enumerate(rows_filtered):
        if i < 10: num = f'0{i}'
        else: num = f'{i}'
        item_formatted = item.lower().replace(' ', '-')
        with open(f'database/articles/{entity}/medicine/benefits/{num}-{item_formatted}.md', 'a', encoding='utf-8') as f: pass
        # with open(f'database/tables/{entity}/medicine/benefits/{num}-{item_formatted}.csv', 'a', encoding='utf-8') as f: pass
    


    # try: os.mkdir(f'database/articles/{entity}/botany/taxonomy')
    # except: pass
    # with open(f'database/articles/{entity}/botany/_intro.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/taxonomy.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/common-names.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/varieties.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/morphology.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/habitat.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/native.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/distribution.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/invasive.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/invasive-impact.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/invasive-control.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/life-cycle.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/perennial.md', 'a', encoding='utf-8') as f: pass

    
    # with open(f'database/articles/{entity}/botany/habitat.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/native.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/distribution.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/invasive.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/invasive-impact.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/invasive-control.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/life-cycle.md', 'a', encoding='utf-8') as f: pass
    # with open(f'database/articles/{entity}/botany/perennial.md', 'a', encoding='utf-8') as f: pass
    
    # try: os.mkdir(f'database/articles/{entity}/botany/symbology')
    # except: pass
    # with open(f'database/articles/{entity}/botany/symbology/symbology.md', 'a', encoding='utf-8') as f: pass
