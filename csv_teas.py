import time

import util
import utils_ai


csv_conditions_filepath = 'database/csv/status/conditions.csv'
csv_teas_filepath = 'database/csv/herbalism/teas_conditions.csv'

conditions_rows = util.csv_get_rows(csv_conditions_filepath)
conditions_cols = util.csv_get_header_dict(conditions_rows)

for condition_row in conditions_rows[1:]:
    condition_id = condition_row[conditions_cols['condition_id']].strip()
    condition_name = condition_row[conditions_cols['condition_name']].strip().lower()
    condition_slug = condition_row[conditions_cols['condition_slug']].strip().lower()
    condition_classification = condition_row[conditions_cols['condition_classification']].strip().lower()
    system_id = condition_row[conditions_cols['system_id']]
    to_process = condition_row[conditions_cols['to_process']]

    if to_process == '': continue

    teas_rows = util.csv_get_rows_by_entity(csv_teas_filepath, condition_id, col_num=0)

    if teas_rows != []: continue

    prompt_paragraphs_num = 19
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} best herbal teas for {condition_name}.
        Write only the names of the herbs, not the descriptions.
        Include only 1 herb for each list item.
        Don't specify the part of the herb.
    '''

    reply = utils_ai.gen_reply(prompt)

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip().lower()
        if line == '': continue
        if ':' in line: continue 
        if line[0].isdigit():
            if '. ' in line: line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            if line.endswith('.'): line = line[0:-1]
            reply_formatted.append([condition_id, condition_name, condition_slug, line])

    if prompt_paragraphs_num == len(reply_formatted):
        print('***************************************')
        for line in reply_formatted:
            print(line)
        print('***************************************')

        util.csv_add_rows(csv_teas_filepath, reply_formatted)
        
    time.sleep(30)

