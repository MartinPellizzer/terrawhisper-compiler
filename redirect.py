import os
import pathlib

import g
import util

util.file_write('_test.txt', '')

status_rows = util.csv_get_rows(g.CSV_STATUS_FILEPATH)
status_cols = util.csv_get_cols(status_rows)
status_rows = status_rows[1:]


path_teas_in = pathlib.Path('website/herbalism/teas')
filepaths_teas_in = path_teas_in.rglob("*.html")

path_tea_in = pathlib.Path('website/herbalism/tea')
filepaths_tea_in = path_tea_in.rglob("*.html")

path_tincture_in = pathlib.Path('website/herbalism/tincture')
filepaths_tincture_in = path_tincture_in.rglob("*.html")

path_out = pathlib.Path('website/remedies')
filepaths_out = path_out.rglob("*.html")

filepaths_teas_in = [str(item).replace('\\', '/').replace('.html', '') for item in filepaths_teas_in]
filepaths_tea_in = [str(item).replace('\\', '/').replace('.html', '') for item in filepaths_tea_in]
filepaths_tincture_in = [str(item).replace('\\', '/').replace('.html', '') for item in filepaths_tincture_in]
filepaths_out = [str(item).replace('\\', '/').replace('.html', '') for item in filepaths_out]
filepaths_teas_out = [item for item in filepaths_out if 'teas' in item]

redirects_list = []

for filepath_in in filepaths_teas_in: 
    status_slug_in = filepath_in.split('/')[-1]

    for filepath_out in filepaths_teas_out:
        status_slug_out = filepath_out.split('/')[-2]

        if status_slug_in == status_slug_out:
            print(filepath_in, '>>', filepath_out)
            util.file_append('_test.txt', f'{filepath_in} >> {filepath_out}' + '\n')
            redirects_list.append([filepath_in, filepath_out])

for filepath_in in filepaths_tea_in: 
    status_slug_in = filepath_in.split('/')[-1]

    for filepath_out in filepaths_teas_out:
        status_slug_out = filepath_out.split('/')[-2]

        if status_slug_in == status_slug_out:
            print(filepath_in, '>>', filepath_out)
            util.file_append('_test.txt', f'{filepath_in} >> {filepath_out}' + '\n')
            redirects_list.append([filepath_in, filepath_out])

for filepath_in in filepaths_tincture_in: 
    status_slug_in = filepath_in.split('/')[-1]

    for filepath_out in filepaths_teas_out:
        status_slug_out = filepath_out.split('/')[-2]

        if status_slug_in == status_slug_out:
            print(filepath_in, '>>', filepath_out)
            util.file_append('_test.txt', f'{filepath_in} >> {filepath_out}' + '\n')
            redirects_list.append([filepath_in, filepath_out])



for redirect in redirects_list:
    redirect_in = redirect[0] + '.html'
    redirect_out = redirect[1].replace('website', 'https://terrawhisper.com') + '.html'
    html = f'''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta http-equiv="refresh" content="0; url={redirect_out}">
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
    print()
    print(redirect_in)
    print(redirect_out)
    util.file_write(redirect_in, html)


    # print(filepath)
    # continue

    # for status_row in status_rows:
    #     status_slug_csv = status_row[status_cols['status_slug']]
    #     if status_slug_html == status_slug_csv:
    #         print(status_slug_html)
    #         util.file_append('_test.txt', f'{filepath_in} >> {status_row}' + '\n')
    #         break

    # if found:
    #     print(status_slug_html)
    #     continue
    #     relative_filepath = '/'.join(filepath.split('/')[-2:])
    #     new_filepath = f'website/remedies/{relative_filepath}/teas.html'
    #     if os.path.exists(new_filepath):
    #         print(relative_filepath, '>>', new_filepath)
    #     else:
    #         print(relative_filepath, '>>', 'not found')
