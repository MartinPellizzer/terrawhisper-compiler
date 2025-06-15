import os
import shutil

from oliark_io import csv_read_rows_to_json

import g


def ailments_gen():
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')

    for ailment_i, ailment in enumerate(ailments):
        print(f'\n>> {ailment_i}/{len(ailments)}')
        print(f'    >> {ailment}')
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        html_filepath_in = f'{g.WEBSITE_FOLDERPATH}/remedies/{system_slug}-system/{ailment_slug}.html'
        html_filepath_out = f'{g.WEBSITE_FOLDERPATH}/ailments/{ailment_slug}.html'
        try: shutil.copy2(html_filepath_in, html_filepath_out)
        except: pass

ailments_gen()
