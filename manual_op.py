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

    
filenames = os.listdir('database/articles/plants_trefle')

for filename in filenames:
    filepath = f'database/articles/plants_trefle/{filename}'
    content = util.file_read(filepath)
    if content == '{}':
        os.remove(filepath)