import os
import pathlib

import g
import util

util.file_write('_test.txt', '')

# status_rows = util.csv_get_rows(g.CSV_STATUS_FILEPATH)
# status_cols = util.csv_get_cols(status_rows)
# status_rows = status_rows[1:]


# path_teas_in = pathlib.Path('website/herbalism/teas')
# filepaths_teas_in = path_teas_in.rglob("*.html")

# path_tea_in = pathlib.Path('website/herbalism/tea')
# filepaths_tea_in = path_tea_in.rglob("*.html")

# path_tincture_in = pathlib.Path('website/herbalism/tincture')
# filepaths_tincture_in = path_tincture_in.rglob("*.html")

# path_out = pathlib.Path('website/remedies')
# filepaths_out = path_out.rglob("*.html")

# filepaths_teas_in = [str(item).replace('\\', '/').replace('.html', '') for item in filepaths_teas_in]
# filepaths_tea_in = [str(item).replace('\\', '/').replace('.html', '') for item in filepaths_tea_in]
# filepaths_tincture_in = [str(item).replace('\\', '/').replace('.html', '') for item in filepaths_tincture_in]
# filepaths_out = [str(item).replace('\\', '/').replace('.html', '') for item in filepaths_out]
# filepaths_teas_out = [item for item in filepaths_out if 'teas' in item]

# redirects_list = []

# for filepath_in in filepaths_teas_in: 
#     status_slug_in = filepath_in.split('/')[-1]

#     for filepath_out in filepaths_teas_out:
#         status_slug_out = filepath_out.split('/')[-2]

#         if status_slug_in == status_slug_out:
#             print(filepath_in, '>>', filepath_out)
#             util.file_append('_test.txt', f'{filepath_in} >> {filepath_out}' + '\n')
#             redirects_list.append([filepath_in, filepath_out])

# for filepath_in in filepaths_tea_in: 
#     status_slug_in = filepath_in.split('/')[-1]

#     for filepath_out in filepaths_teas_out:
#         status_slug_out = filepath_out.split('/')[-2]

#         if status_slug_in == status_slug_out:
#             print(filepath_in, '>>', filepath_out)
#             util.file_append('_test.txt', f'{filepath_in} >> {filepath_out}' + '\n')
#             redirects_list.append([filepath_in, filepath_out])

# for filepath_in in filepaths_tincture_in: 
#     status_slug_in = filepath_in.split('/')[-1]

#     for filepath_out in filepaths_teas_out:
#         status_slug_out = filepath_out.split('/')[-2]

#         if status_slug_in == status_slug_out:
#             print(filepath_in, '>>', filepath_out)
#             util.file_append('_test.txt', f'{filepath_in} >> {filepath_out}' + '\n')
#             redirects_list.append([filepath_in, filepath_out])



# for redirect in redirects_list:
#     redirect_in = redirect[0] + '.html'
#     redirect_out = redirect[1].replace('website', 'https://terrawhisper.com') + '.html'
#     html = f'''
#     <!DOCTYPE html>
#     <html lang="en">

#     <head>
#         <meta http-equiv="refresh" content="0; url={redirect_out}">
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <meta name="author" content="Leen Randell">
#         <link rel="stylesheet" href="/style.css">
#         <title>Content Permanently Moved (Redirected)</title>
#     </head>

#     <body>
#     </body>

#     </html>
#     '''
#     print()
#     print(redirect_in)
#     print(redirect_out)
#     util.file_write(redirect_in, html)



#########################################################################
# PLANTS
#########################################################################

new_plants_filepaths = pathlib.Path('website/herbs')
new_plants_filepaths = new_plants_filepaths.rglob("*.html")
new_plants_filepaths = [str(item).replace('\\', '/').replace('.html', '') for item in new_plants_filepaths]

for new_plant_filepath in new_plants_filepaths:
    old_plant_filepath = new_plant_filepath.replace('/herbs/', '/plants/') + '.html'
    web_plant_filepath = new_plant_filepath.replace('website/', '') + '.html'
    print(old_plant_filepath)
    print(web_plant_filepath)
    print()
    
    util.create_folder_for_filepath(old_plant_filepath)
    html = f'''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta http-equiv="refresh" content="0; url=https://terrawhisper.com/{web_plant_filepath}">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="author" content="Leen Randell">
        <link rel="stylesheet" href="/style.css">
        <title>Content Permanently Moved (Redirected)</title>
    </head>

    <body>
    </body>

    </html>
    '''
    util.file_write(old_plant_filepath, html)

# path_plants_in = pathlib.Path('website/plants')
# filepaths_plants_in = path_plants_in.rglob("*.html")
# path_out = pathlib.Path('website/herbs')
# filepaths_out = path_out.rglob("*.html")

# filepaths_plants_in = [str(item).replace('\\', '/').replace('.html', '') for item in filepaths_plants_in]
# filepaths_plants_out = [item for item in filepaths_out]

# print(filepaths_plants_in)

# redirects_list = []

# for filepath_in in filepaths_plants_in: 
#     status_slug_in = filepath_in.split('/')[-1]

#     for filepath_out in filepaths_teas_out:
#         status_slug_out = filepath_out.split('/')[-2]

#         if status_slug_in == filepaths_plants_out:
#             print(filepath_in, '>>', filepath_out)
#             util.file_append('_test.txt', f'{filepath_in} >> {filepath_out}' + '\n')
#             redirects_list.append([filepath_in, filepath_out])

