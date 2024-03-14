import sys
import shutil

print('params (ACTION, ENTITY, WORD)')

# if len(sys.argv) != 4:
#     print('ERR: params (ACTION, ENTITY, OUT_FILENAME, WORD)')
#     quit()


action = sys.argv[1]
entity = sys.argv[2]
word = sys.argv[3]



if action == 'filter':
    with open(f'keywords/{entity}/master.md', encoding='utf-8') as f:
        keywords = f.readlines()
        
    filtered_keywords_1 = []

    with open(f'keywords/plants.md', encoding='utf-8') as f:
        plants = f.readlines()

    for keyword in keywords:
        found = False
        for plant in plants:
            if plant.strip() not in keyword:
                found = True
                break
        if found:
            filtered_keywords_1.append(keyword)

    with open(f'keywords/blacklist.md', encoding='utf-8') as f:
        blacklisted_words = f.readlines()

    filtered_keywords_2 = []
    for keyword in filtered_keywords_1:
        found = False
        for blacklisted_word in blacklisted_words:
            if blacklisted_word.strip() in keyword:
                found = True
                break
        if not found:
            filtered_keywords_2.append(keyword)
        else:
            pass
    
    with open(f'keywords/{entity}/master_filtered.md', 'w', encoding='utf-8') as f:
        for item in filtered_keywords_2:
            f.write(item)










elif action == 'group':

    with open(f'keywords/{entity}/master_filtered.md', encoding='utf-8') as f:
        keywords = f.readlines()

    keep_lst = []
    move_lst = []
    for keyword in keywords:
        keyword = keyword.strip()
        if word in keyword:
            move_lst.append(keyword)
        else:
            keep_lst.append(keyword)

    with open(f'keywords/{entity}/master_filtered.md', 'w', encoding='utf-8') as f:
        for item in keep_lst:
            f.write(f'{item}\n')
            
    with open(f'keywords/{entity}/master_group.md', 'a', encoding='utf-8') as f:
        f.write(f'{word}\n')
        for item in move_lst:
            f.write(f'    {item}\n')
        f.write(f'\n')

    print(len(keep_lst))

    pass

elif action == 'groups-preparations':
    shutil.copy2(f'keywords/{entity}/master.md', f'keywords/{entity}/master_filtered.md')

    with open(f'keywords/{entity}/master_group.md', 'w', encoding='utf-8') as f:
        f.write('')

    with open(f'keywords/groups-preparations.md', encoding='utf-8') as f:
        groups = f.readlines()

    for group in groups:
        if group.strip() == '': break
        with open(f'keywords/{entity}/master_filtered.md', encoding='utf-8') as f:
            keywords = f.readlines()

        group = group.strip()
        keep_lst = []
        move_lst = []
        for keyword in keywords:
            keyword = keyword.strip()
            if group in keyword:
                move_lst.append(keyword)
            else:
                keep_lst.append(keyword)

        if move_lst:

            with open(f'keywords/{entity}/master_filtered.md', 'w', encoding='utf-8') as f:
                for item in keep_lst:
                    f.write(f'{item}\n')
                    
            with open(f'keywords/{entity}/master_group.md', 'a', encoding='utf-8') as f:
                f.write(f'{group}\n')
                for item in move_lst:
                    f.write(f'    {item}\n')
                f.write(f'\n')

            print(len(keep_lst))


elif action == 'group-auto':

    with open(f'keywords/groups.md', encoding='utf-8') as f:
        groups = f.readlines()

    for group in groups:
        with open(f'keywords/{entity}/master_filtered.md', encoding='utf-8') as f:
            keywords = f.readlines()

        group = group.strip()
        keep_lst = []
        move_lst = []
        for keyword in keywords:
            keyword = keyword.strip()
            if group in keyword:
                move_lst.append(keyword)
            else:
                keep_lst.append(keyword)

        if move_lst:

            with open(f'keywords/{entity}/master_filtered.md', 'w', encoding='utf-8') as f:
                for item in keep_lst:
                    f.write(f'{item}\n')
                    
            with open(f'keywords/{entity}/master_group.md', 'a', encoding='utf-8') as f:
                f.write(f'{group}\n')
                for item in move_lst:
                    f.write(f'    {item}\n')
                f.write(f'\n')

            print(len(keep_lst))


elif action == 'group-auto-test':

    with open(f'keywords/group.md', encoding='utf-8') as f:
        groups = f.readlines()

    for group in reversed(groups):
        if group.strip() == '': continue
        with open(f'keywords/{entity}/master_filtered.md', encoding='utf-8') as f:
            keywords = f.readlines()

        group = group.strip()
        keep_lst = []
        move_lst = []
        for keyword in keywords:
            keyword = keyword.strip()
            if group in keyword:
                move_lst.append(keyword)
            else:
                keep_lst.append(keyword)

        if move_lst:
            with open(f'keywords/{entity}/master_group.md', 'r', encoding='utf-8') as f:
                content = f.read()
            print(content)
                    
            with open(f'keywords/{entity}/master_group.md', 'w', encoding='utf-8') as f:
                f.write(f'{group}\n')
                for item in move_lst:
                    f.write(f'    {item}\n')
                f.write(f'\n')
                f.write(content)

            print(len(keep_lst))


elif action == 'group-auto-reverse':

    with open(f'keywords/groups.md', encoding='utf-8') as f:
        groups = f.readlines()

    for group in groups:
        with open(f'keywords/{entity}/master_filtered.md', encoding='utf-8') as f:
            keywords = f.readlines()

        group = group.strip()
        keep_lst = []
        move_lst = []
        for keyword in keywords:
            keyword = keyword.strip()
            if group in keyword:
                move_lst.append(keyword)
            else:
                keep_lst.append(keyword)

        if move_lst:

            with open(f'keywords/{entity}/master_filtered.md', 'w', encoding='utf-8') as f:
                for item in keep_lst:
                    f.write(f'{item}\n')
                    
            with open(f'keywords/{entity}/master_group.md', 'a', encoding='utf-8') as f:
                f.write(f'{group}\n')
                for item in move_lst:
                    f.write(f'    {item}\n')
                f.write(f'\n')

            print(len(keep_lst))
