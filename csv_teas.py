import time

import g
import util
import utils_ai


def teas_conditions():
    conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
    conditions_cols = util.csv_get_header_dict(conditions_rows)

    for condition_row in conditions_rows[1:]:
        condition_id = condition_row[conditions_cols['condition_id']].strip()
        condition_name = condition_row[conditions_cols['condition_names']].strip().lower().split(', ')[0]
        condition_slug = condition_row[conditions_cols['condition_slug']].strip().lower()
        condition_classification = condition_row[conditions_cols['condition_classification']].strip().lower()
        system_id = condition_row[conditions_cols['system_id']]
        to_process = condition_row[conditions_cols['to_process']]

        if to_process == '': continue

        teas_rows = util.csv_get_rows_by_entity(g.CSV_TEAS_FILEPATH, condition_id, col_num=0)
 
        if teas_rows != []: continue

        prompt_paragraphs_num = 19
        prompt = f'''
            Write a numbered list of the {prompt_paragraphs_num} best herbal teas for {condition_name}.
            Write only the names of the herbs, not the descriptions.
            Include only 1 herb for each list item.
            Don't include the parts of the herbs.
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

            util.csv_add_rows(g.CSV_TEAS_FILEPATH, reply_formatted)
            
        time.sleep(g.PROMPT_DELAY_TIME)


def related_conditions():
    conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
    conditions_cols = util.csv_get_cols(conditions_rows)
    conditions_names = [
        condition_row[conditions_cols['condition_names']].strip().lower().split(', ')[0]
        for condition_row in conditions_rows[1:]
        if condition_row[conditions_cols['condition_names']].strip().lower().split(', ')[0] != ''
    ]

    for condition_row in conditions_rows[1:]:
        condition_id = condition_row[conditions_cols['condition_id']].strip().lower()
        condition_name = condition_row[conditions_cols['condition_names']].strip().lower().split(', ')[0]
        condition_slug = condition_row[conditions_cols['condition_slug']].strip().lower()
        condition_classification = condition_row[conditions_cols['condition_classification']].strip().lower()
        to_process = condition_row[conditions_cols['to_process']].strip().lower()

        if condition_id == '': continue
        if condition_classification != 'symptom': continue
        
        related_problems_rows = util.csv_get_rows_by_entity(g.CSV_RELATED_PROBLEMS_FILEPATH, condition_id, col_num=0)

        if related_problems_rows != []: continue

        prompt = f'''
            Write a numbered list of symptoms people may experience when they have {condition_name}.
            Write only the names, not the descriptions.
            Use as few words as possible.
        '''
            # Write only 1 symptom per list item.
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

                related_condition_name = line.strip().lower()

                related_condition_row = []
                for condition_row_tmp in conditions_rows[1:]:
                    condition_names_tmp = condition_row_tmp[conditions_cols['condition_names']].strip().lower().split(', ')
                    if related_condition_name in condition_names_tmp:
                        related_condition_row = condition_row_tmp
                        break

                related_condition_id = ''
                related_condition_slug = ''
                
                if related_condition_row != []:
                    related_condition_id = related_condition_row[conditions_cols['condition_id']]
                    related_condition_slug = related_condition_row[conditions_cols['condition_slug']]
                reply_formatted.append([
                    condition_id, condition_name, condition_slug, 
                    related_condition_id, related_condition_name, related_condition_slug,
                ])
        
        if reply_formatted != '' and reply_formatted != []:
            print('***************************************')
            for line in reply_formatted: print(line)
            print('***************************************')

            util.csv_add_rows(g.CSV_RELATED_PROBLEMS_FILEPATH, reply_formatted)

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

        break




action = input('''
enter and action from the following:

1. teas_conditions()
2. related_conditions()

>> ''')

if action == '1':
    teas_conditions()
elif action == '2':
    related_conditions()


# related_conditions()