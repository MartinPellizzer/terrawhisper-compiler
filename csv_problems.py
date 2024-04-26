import time

import g
import util
# import utils_ai

ailments_to_add = [
    'Abscess',
    'Acne',
    'Allergies',
    'Asthma',
    'Athlete\'s Foot',
    'Backache',
    'Bee Sting',
    'Bloating',
    'Bronchitis',
    'Bruise',
    'Burn',
    'Canker Sore',
    'Chapped Lips',
    'Chest Congestion',
    'Chicken Pox',
    'Cold',
    'Cold Sore',
    'Colic',
    'Conjunctivitis',
    'Constipation',
    'Cough',
    'Cuts and Scrapes',
    'Dandruff',
    'Diaper Rash',
    'Diarrhea',
    'Dry Skin',
    'Earache',
    'Eczema',
    'Fatigue',
    'Fever',
    'Flatulence',
    'Flu',
    'Gingivitis',
    'Hair Loss',
    'Halitosis',
    'Hangover',
    'Headache',
    'Heartburn',
    'Hemorrhoids',
    'High Blood Pressure',
    'Hives',
    'Indigestion',
    'Insect Bites',
    'Insomnia',
    'Jock Itch',
    'Keratosis Pilaris',
    'Laryngitis',
    'Menopause',
    'Mental Focus',
    'Mental Wellness',
    'Muscle Cramps',
    'Nausea',
    'Oily Skin',
    'Poison Ivy',
    'Premenstrual Syndrome',
    'Prostatitis',
    'Psoriasis',
    'Rheumatoid Arthritis',
    'Ringworm',
    'Rosacea',
    'Shingles',
    'Sinus Infection',
    'Skin Tag',
    'Sore Muscles',
    'Sore Throat',
    'Sprain',
    'Stiff Joints',
    'Sunburn',
    'Tendinitis',
    'Travel Sickness',
    'Urinary Tract Infection',
    'Warts',
    'Weight Loss',
    'Wrinkles',
    'Yeast Infection',
]

conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
conditions_cols = util.csv_get_cols(conditions_rows)
conditions_rows = conditions_rows[1:]

problems_rows = util.csv_get_rows(g.CSV_PROBLEMS_FILEPATH)
problems_cols = util.csv_get_cols(problems_rows)
problems_rows = problems_rows[1:]

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]

for condition_row in conditions_rows:
    condition_id = condition_row[conditions_cols['condition_id']]
    condition_slug = condition_row[conditions_cols['condition_slug']].split('/')[-1].strip()
    condition_names = condition_row[conditions_cols['condition_names']]
    system_id = condition_row[conditions_cols['system_id']]

    system_slug = ''
    if system_id != '':
        system_slug = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id
        )[0][systems_cols['system_slug']]

    if condition_id == '': continue
    if condition_slug == '': continue

    rows_found = util.csv_get_rows_filtered(g.CSV_PROBLEMS_FILEPATH, problems_cols['problem_id'], condition_id)
    if rows_found == []:
        util.csv_add_rows(g.CSV_PROBLEMS_FILEPATH, [[condition_id, condition_slug, condition_names, system_id, system_slug]])




# csv_filepath = 'database/csv/status/problems.csv'

# prompt = f'''
#     Write a numbered list of 20 medicinal herbs that helps with bad breath. 
#     Write only the names of the herbs, not the descriptions.
# '''

# reply = utils_ai.gen_reply(prompt)
# time.sleep(g.PROMPT_DELAY_TIME)





# herbs_list = [
#     'Parsley',
#     'Peppermint',
#     'Spearmint',
#     'Eucalyptus',
#     'Rosemary',
#     'Sage',
#     'Tea tree',
#     'Clove',
#     'Lemon',
#     'Ginger',
#     'Cinnamon',
# ]
# preparations_list = [
#     'Teas',
#     'Decoctions',
#     'Tinctures',
#     'Extracts',
#     'Salves',
#     'Ointments',
#     'Capsules',
#     'Tablets',
#     'Poultices',
#     'Compresses',
#     'Syrups',
#     'Elixirs',
#     'Powders',
# ]

# herbs_str = ''
# for i, herb_item in enumerate(herbs_list):
#     herbs_str += f'{i+1}. {herb_item}\n'

# preparations_str = ''
# for i, preparation_item in enumerate(preparations_list):
#     preparations_str += f'{i+1}. {preparation_item}\n'
    
# prompt = f'''
#     Write a list of the best medicinal preparations of Parsley for bad breath.
#     For each medicinal preparation, explain is 1 short sentence how to use it for bad breath.
#     Don't include other herbs.
#     Only pick these best medicinal preparations from the following list:
#     {preparations_str}
# '''
# reply = utils_ai.gen_reply(prompt)
# time.sleep(g.PROMPT_DELAY_TIME)


