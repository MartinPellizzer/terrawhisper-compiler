import os
import pathlib

import g
import util
import util_data
import data_csv

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read, json_write

def sitemap_ailments():
    urls = ''
    website_folderpath = 'website-2'
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}'
        filepath_web = f'https://terrawhisper.com/{url}.html'
        filepath_out = f'{website_folderpath}/{url}.html'
        json_filepath = f'database/json/{url}.json'
        data = json_read(json_filepath)
        if 'lastmod' not in data: data['lastmod'] = today()
        lastmod = data['lastmod']
        if os.path.exists(filepath_out):
            urls += f'''
<url>
  <loc>{filepath_web}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
            '''.strip() + '\n'
    return urls
        

    
def test_sitemap():
    sitemap_content = util.file_read('sitemap.xml')
    lines = sitemap_content.split('\n')
    for line in lines:
        if '<loc>' in line:
            line = line.replace('<loc>', '').replace('</loc>', '').strip()
            line = line.replace('https://terrawhisper.com', 'website')
            if not os.path.exists:
                print(f'missing: {line}')

def sitemap_all():
    sitemap = ''
    sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += sitemap_ailments()
    sitemap += '</urlset>\n'
    util.file_write('sitemap.xml', sitemap.strip())

sitemap_all()
