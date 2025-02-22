import os
import json

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read, json_write
from oliark_io import file_write

vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'
website_folderpath = 'website-2'

HERBS_TO_GEN_NUM = 40000

plants_wcvp = []
if plants_wcvp == []:
    plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    plants_wcvp = [plant for plant in plants_wcvp if ('var.' not in plant['scientfiicname'] and 'f.' not in plant['scientfiicname'] and 'subsp.' not in plant['scientfiicname'] and 'proles' not in plant['scientfiicname']  and 'stirps' not in plant['scientfiicname'] and 'monstr.' not in plant['scientfiicname'])]

def sitemap_main():
    urls = ''
    urls += f'''
<url>
  <loc>https://terrawhisper.com/</loc>
  <lastmod>2025-02-19</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://terrawhisper.com/herbs.html</loc>
  <lastmod>2025-02-19</lastmod>
</url>
'''.strip() + '\n'

    return urls

def sitemap_herbs():
    urls = ''
    global plants_wcvp
    if plants_wcvp == []:
        plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    plants_wcvp_tmp = plants_wcvp[:HERBS_TO_GEN_NUM]
    for herb_i, herb in enumerate(plants_wcvp_tmp):
        print(f'{herb_i} - {herb}')
        herb_name_scientific = herb['scientfiicname']
        herb_slug = herb_name_scientific.strip().lower().replace(' ', '-').replace('.', '')
        url = f'herbs/{herb_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'{website_folderpath}/{url}.html'
        web_filepath = f'https://terrawhisper.com/herbs/{herb_slug}.html'
        print(f'    >> JSON: {json_filepath}')
        print(f'    >> HTML: {html_filepath}')
        print(f'    >> WEB: {web_filepath}')
        if not os.path.exists(f'{html_filepath}'): continue
        data = json_read(f'database/json/herbs/{herb_slug}.json')
        lastmod = data['lastmod']
        if os.path.exists(html_filepath):
            urls += f'''
<url>
  <loc>{web_filepath}</loc>
  <lastmod>2025-02-19</lastmod>
</url>
            '''.strip() + '\n'
    return urls

def sitemap_all():
    sitemap = ''
    sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += sitemap_main()
    sitemap += sitemap_herbs()
    # sitemap += sitemap_status()
    # sitemap += sitemap_remedies_systems_problems()
    # sitemap += sitemap_plants()
    sitemap += '</urlset>\n'
    file_write('sitemap.xml', sitemap.strip())

sitemap_all()
