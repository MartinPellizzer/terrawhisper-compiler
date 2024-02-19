import os

folderpath = 'keywords/_sorted_auto'

try: os.makedirs(folderpath)
except: pass

# remaining_keywords = []

# keywords_found = []
# for keyword in keywords:
#     if 'with' in keyword: continue  
#     words = keyword.split(' ')
#     found = False
#     for word in words:
#         if 'tea' == word.lower().strip():
#             found = True
#             break
#     if found:
#         keywords_found.append(keyword)
#     else:
#         remaining_keywords.append(keyword)

preparations = [
    'tea',
    'tincture',
    'extract',
    'serum',
    'drop',
    'capsule',
    'essential oil', 
    'infused oil', 
    'oil', 
    'ointment',
    'salve',
    'infusion',
    'infuse',

    'benefit',

    'dye',
]

for f in os.listdir('keywords'):
    if f.endswith('.txt'):
        entity = f.split('.')[0].replace(' ', '-').lower()

        with open(f'keywords/{f}', 'r', encoding='utf-8') as reader:
            keywords = reader.readlines()

        try: os.makedirs(f'{folderpath}/{entity}')
        except: pass
        # try: os.makedirs(f'{folderpath}/{entity}/preparations')
        # except: pass


            


        remaining_keywords = keywords

        with open(f'{folderpath}/{entity}/preparations.txt', 'w', encoding='utf-8') as writer: pass

        for preparation in preparations:

            tmp_remaining_keywords = [x for x in remaining_keywords]
            remaining_keywords = []

            keywords_found = []
            for keyword in tmp_remaining_keywords:
                if preparation.lower() in keyword.lower(): keywords_found.append(keyword)
                else: remaining_keywords.append(keyword)

            with open(f'{folderpath}/{entity}/preparations.txt', 'a', encoding='utf-8') as writer:
                for keyword in keywords_found:
                    writer.write(keyword)
                writer.write('\n')



        # remaining
        with open(f'{folderpath}/{entity}/remaining.txt', 'w', encoding='utf-8') as writer:
            for keyword in remaining_keywords:
                writer.write(keyword)
            writer.write('\n')



        
