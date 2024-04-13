import os
import util


# rows = util.csv_get_rows('database/tables/_plants_all_new.csv')[1:15]
# plants = [row[0] for row in rows]
# filenames = os.listdir('database/articles/plants_trefle')
# for filename in filenames:
#     if filename.replace('.json', '') not in plants:
#         print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
#         filepath = f'database/articles/plants_trefle/{filename}'
#         os.remove(filepath)
#     else:
#         print('ok')
#     # print(filepath)


# def rename():
#     filenames = os.listdir('database/articles/plants_trefle')

#     for filename in filenames:
#         filepath = f'database/articles/plants_trefle/{filename}'
#         content = util.file_read(filepath)
#         if content == '{}':
#             os.remove(filepath)


# def delete():
#     filenames = os.listdir('database/articles/plants_trefle')

#     for filename in filenames:
#         filepath = f'database/articles/plants_trefle/{filename}'
#         content = util.file_read(filepath)
#         if content == '{}':
#             os.remove(filepath)

def add_id_to_teas_conditions():
    csv_conditions_filepath = 'database/csv/ailments/conditions.csv'
    conditions_rows = util.csv_get_rows(csv_conditions_filepath)
    conditions_cols = util.csv_get_header_dict(conditions_rows)
    
    csv_teas_filepath = 'database/csv/herbalism/teas_conditions.csv'
    teas_rows = util.csv_get_rows(csv_teas_filepath)
    teas_cols = util.csv_get_header_dict(teas_rows)

    new_teas_rows = [['condition_id', 'condition_name', 'condition_slug', 'tea_name']]
    for tea_row in teas_rows[1:]:
        tea_name = tea_row[teas_cols['tea_name']].lower().strip()
        tea_condition_name = tea_row[teas_cols['condition_name']].lower().strip()

        condition_id = ''
        condition_name = ''
        condition_slug = ''
        found = False
        for condition_row in conditions_rows[1:]:
            condition_id = condition_row[conditions_cols['condition_id']].strip()
            condition_name = condition_row[conditions_cols['condition_name']].lower().strip()
            condition_slug = condition_row[conditions_cols['condition_slug']].lower().strip()
            if tea_condition_name == condition_name:
                # new_teas_rows.append([condition_id, condition_name, tea_name])
                found = True
                break

        if found:
            new_teas_rows.append([condition_id, condition_name, condition_slug, tea_name])
        else:
            new_teas_rows.append(['????', tea_condition_name, '', tea_name])


    for new_tea_row in new_teas_rows:
        print(new_tea_row)

    util.csv_set_rows(csv_teas_filepath, new_teas_rows)


            
add_id_to_teas_conditions()