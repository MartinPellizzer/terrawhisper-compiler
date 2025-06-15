import os
import json

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read, json_write
from oliark_io import file_write

vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'
website_folderpath = 'website-2'

SITEMAP_CHUNK_SIZE = 40000
PLANTS_NUM_MAX = 600000

plants_wcvp = []
if plants_wcvp == []:
    plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    plants_wcvp = [plant for plant in plants_wcvp if ('var.' not in plant['scientfiicname'] and 'f.' not in plant['scientfiicname'] and 'subsp.' not in plant['scientfiicname'] and 'proles' not in plant['scientfiicname']  and 'stirps' not in plant['scientfiicname'] and 'monstr.' not in plant['scientfiicname'])]

def sitemap_main():
    sitemap = ''
    sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
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
    sitemap += '</urlset>\n'
    file_write('sitemap.xml', sitemap.strip())

def sitemap_herbs():
    urls = ''
    global plants_wcvp
    if plants_wcvp == []:
        plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    # plants_wcvp_tmp = plants_wcvp[:HERBS_TO_GEN_NUM]

    plants_wcvp_chunks = []
    row_cur = []
    for plant_i, plant in enumerate(plants_wcvp):
        if plant_i >= PLANTS_NUM_MAX: break
        if len(row_cur) >= SITEMAP_CHUNK_SIZE:
            plants_wcvp_chunks.append(row_cur)
            row_cur = []
            row_cur.append(plant)
        else:
            row_cur.append(plant)
    if len(row_cur) != 0: plants_wcvp_chunks.append(row_cur)
    '''
    for plants_wcvp_chunk in plants_wcvp_chunks:
        print(len(plants_wcvp_chunk))
        print(plants_wcvp_chunk[0])
        print(plants_wcvp_chunk[-1])
    '''

    for sitemap_i, plants_wcvp_chunk in enumerate(plants_wcvp_chunks):
        sitemap = ''
        sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        urls = ''
        for herb_i, herb in enumerate(plants_wcvp_chunk):
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
  <lastmod>2025-03-22</lastmod>
</url>
                '''.strip() + '\n'
        sitemap += f'{urls}\n'
        sitemap += '</urlset>\n'
        file_write(f'sitemaps/sitemap-herbs-{sitemap_i}.xml', sitemap.strip())

def sitemap_all():
    pass

sitemap_main()
sitemap_herbs()
