import sys

if len(sys.argv) != 4:
    print('ERR: params (ENTITY, OUT_FILENAME, WORD)')
    quit()


entity = sys.argv[1]
out_filename = sys.argv[2]
word = sys.argv[3]
print(out_filename)
print(word)
# quit()

with open(f'keywords/{entity}/keywords.md', encoding='utf-8') as f:
    keywords = f.readlines()


keep_lst = []
move_lst = []
for keyword in keywords:
    keyword = keyword.strip()
    if word in keyword:
        move_lst.append(keyword)
    else:
        keep_lst.append(keyword)


with open(f'keywords/{entity}/keywords.md', 'w', encoding='utf-8') as f:
    for item in keep_lst:
        f.write(f'{item}\n')
        
with open(f'keywords/{entity}/{out_filename}.md', 'a', encoding='utf-8') as f:
    f.write(f'{word}\n')
    for item in move_lst:
        f.write(f'    {item}\n')
    f.write(f'\n')

print(len(keep_lst))

# print(len(keep_lst))
# print(len(move_lst))

# for item in keep_lst:
#     print(item)

# for item in move_lst:
#     print(item)