import sys

print('params (ACTION, ENTITY, OUT_FILENAME, WORD)')

# if len(sys.argv) != 4:
#     print('ERR: params (ACTION, ENTITY, OUT_FILENAME, WORD)')
#     quit()


action = sys.argv[1]
entity = sys.argv[2]
# out_filename = sys.argv[3]
# word = sys.argv[4]
# print(out_filename)
# print(word)
# quit()

if action == 'filter':
    with open(f'keywords/{entity}/master.md', encoding='utf-8') as f:
        keywords = f.readlines()
    with open(f'keywords/{entity}/blacklist.md', encoding='utf-8') as f:
        blacklisted_words = f.readlines()

    filtered_keywords = []
    for keyword in keywords:
        found = False
        for blacklisted_word in blacklisted_words:
            if blacklisted_word in keyword:
                found = True
                break
        if not found:
            filtered_keywords.append(keyword)
    
    with open(f'keywords/{entity}/master_filtered.md', 'w', encoding='utf-8') as f:
        for item in filtered_keywords:
            f.write(item)

else:

    # with open(f'keywords/{entity}/master.md', encoding='utf-8') as f:
    #     keywords = f.readlines()


    # keep_lst = []
    # move_lst = []
    # for keyword in keywords:
    #     keyword = keyword.strip()
    #     if word in keyword:
    #         move_lst.append(keyword)
    #     else:
    #         keep_lst.append(keyword)


    # with open(f'keywords/{entity}/master.md', 'w', encoding='utf-8') as f:
    #     for item in keep_lst:
    #         f.write(f'{item}\n')
            
    # with open(f'keywords/{entity}/{out_filename}.md', 'a', encoding='utf-8') as f:
    #     f.write(f'{word}\n')
    #     for item in move_lst:
    #         f.write(f'    {item}\n')
    #     f.write(f'\n')

    # print(len(keep_lst))

    pass
