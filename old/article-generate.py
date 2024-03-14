import os
import util

remedies = [
'Chamomile',
'Dandelion',
'Fennel',
'Ginger',
'Lemon balm',
'Mint',
'Peppermint',
'Anise',
'Basil',
'Caraway',
'Cardamom',
'Cinnamon',
'Coriander',
'Dill',
'Echinacea',
'Fenugreek',
'Gentian',
'Green tea',
'Hibiscus',
'Lemon verbena',
'Licorice',
'Linden',
'Marshmallow root',
'Oregano',
'Parsley',
'Rosemary',
'Sage',
'Thyme',
'Turmeric',
'Valerian',
]

problem = 'bloating'


remedy_study_folder = f'database-new/articles/herbalism/tea/{problem}/remedy-study'

# INIT (create folders and files)
util.folder_create(f'database-new/articles/herbalism/tea/{problem}')
util.folder_create(remedy_study_folder)
for i, remedy in enumerate(remedies):
    remedy_study_filepath = f'{remedy_study_folder}/{i}-{remedy.strip().lower().replace(" ", "-")}.md'
    util.file_append(remedy_study_filepath, '')
    


herb = 'ginger'

print(f'''
Write a 60-word paragraph explaining why {herb} tea helps with {problem}.

-------------------------------------------------
''')

print(f'''
Write a 5 strep recipe to make {herb} tea for {problem}.
Include ingredients and dosages.

-------------------------------------------------
''')

# write a 60-word paragraph explaining that chamomile is good for bloating using the info provided by the following study:

# [study]

# Start the paragraph with these words: According to a study published by the *[journal]*, 