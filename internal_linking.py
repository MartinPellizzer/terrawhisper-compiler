import g
import util
import utils_ai
import time

conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
conditions_cols = util.csv_get_cols(conditions_rows)
conditions_names = [
    condition_row[conditions_cols['condition_name']].strip().lower() 
    for condition_row in conditions_rows[1:]
    if condition_row[conditions_cols['condition_name']].strip().lower() != ''
]

csv_related_problems_filepath = 'database/csv/status/related_problems.csv'

for condition_row in conditions_rows[1:]:
    condition_id = condition_row[conditions_cols['condition_id']].strip().lower()
    condition_name = condition_row[conditions_cols['condition_name']].strip().lower()
    condition_slug = condition_row[conditions_cols['condition_slug']].strip().lower()
    to_process = condition_row[conditions_cols['to_process']].strip().lower()

    if condition_id == '': continue
    if condition_slug != 'cough': continue
    
    related_problems_rows = util.csv_get_rows_by_entity(csv_related_problems_filepath, condition_id, col_num=0)

    if related_problems_rows != []: continue

    prompt = f'''
        Write a numbered list about what symptoms people may also experience when they have {condition_name}.
        Write only the names, not the descriptions.
        Write only 1 symptom per list item.
    '''
    reply = utils_ai.gen_reply(prompt)
    # reply = utils_ai.reply_to_list_column(reply)

    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip().lower()
        if line == '': continue
        if ':' in line: continue 
        if line[0].isdigit():
            if '. ' in line: line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            if line.endswith('.'): line = line[0:-1]
            related_condition_name = line
            related_conditions_rows = util.csv_get_rows_by_entity(g.CSV_CONDITIONS_FILEPATH, related_condition_name, col_num=conditions_cols['condition_name'])
            related_condition_id = ''
            related_condition_slug = ''
            if related_conditions_rows != []:
                related_condition_row = related_conditions_rows[0]
                related_condition_id = related_condition_row[conditions_cols['condition_id']]
                related_condition_slug = related_condition_row[conditions_cols['condition_slug']]
            reply_formatted.append([
                condition_id, condition_name, condition_slug, related_condition_id, related_condition_name, related_condition_slug,
            ])
    
    if reply_formatted != '' and reply_formatted != []:
        print('***************************************')
        for line in reply_formatted: print(line)
        print('***************************************')

        util.csv_add_rows(csv_related_problems_filepath, reply_formatted)

    time.sleep(g.PROMPT_DELAY_TIME)

    # conditions_names_text = '\n- '.join(conditions_names)
    # prompt = f'''
    #     Pair each element in the List 1 with the most similar item from the List 2 using this structure: [item list 1]: [item list 2].
        
    #     List 1:
    #     {reply}

    #     List 2:
    #     {conditions_names_text}
    # '''
    # reply = utils_ai.gen_reply(prompt)
    # time.sleep(g.PROMPT_DELAY_TIME)




    # print(condition_name)