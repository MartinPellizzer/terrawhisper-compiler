import time

import g
import util
import utils_ai

csv_filepath = 'database/csv/status/problems.csv'

prompt = f'''
    Write a numbered list of 20 medicinal herbs that helps with bad breath. 
    Write only the names of the herbs, not the descriptions.
'''

reply = utils_ai.gen_reply(prompt)
time.sleep(g.PROMPT_DELAY_TIME)





herbs_list = [
    'Parsley',
    'Peppermint',
    'Spearmint',
    'Eucalyptus',
    'Rosemary',
    'Sage',
    'Tea tree',
    'Clove',
    'Lemon',
    'Ginger',
    'Cinnamon',
]
preparations_list = [
    'Teas',
    'Decoctions',
    'Tinctures',
    'Extracts',
    'Salves',
    'Ointments',
    'Capsules',
    'Tablets',
    'Poultices',
    'Compresses',
    'Syrups',
    'Elixirs',
    'Powders',
]

herbs_str = ''
for i, herb_item in enumerate(herbs_list):
    herbs_str += f'{i+1}. {herb_item}\n'

preparations_str = ''
for i, preparation_item in enumerate(preparations_list):
    preparations_str += f'{i+1}. {preparation_item}\n'
    
prompt = f'''
    Write a list of the best medicinal preparations of Parsley for bad breath.
    For each medicinal preparation, explain is 1 short sentence how to use it for bad breath.
    Don't include other herbs.
    Only pick these best medicinal preparations from the following list:
    {preparations_str}
'''
reply = utils_ai.gen_reply(prompt)
time.sleep(g.PROMPT_DELAY_TIME)


