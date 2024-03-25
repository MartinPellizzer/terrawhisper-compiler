import util
import os

def sitemap_teas():
    sitemap = ''
    sitemap += '''
<?xml version="1.0" encoding="UTF-8"?>
<urlset
      xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">


'''
    for filename in os.listdir('database/articles/herbalism/tea'):
        if filename.endswith('.json'):
            filename_html = filename.replace('.json', '.html')
            sitemap += f'''
<url>
  <loc>https://terrawhisper.com/herbalism/teas/{filename_html}</loc>
  <lastmod>2024-03-17T17:42:42+00:00</lastmod>
</url>
'''.strip() + '\n'
        

    sitemap += '''

</urlset>
'''
    util.file_write('sitemap_teas.xml', sitemap.strip())





def sitemap_plants():
    lastmod = '2024-03-17'
    sitemap = ''
    sitemap += '''
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    # ENTITIES
    for filename in os.listdir('database/articles/plants'):
        if filename.endswith('.json'):
            filename_html = filename.replace('.json', '.html')
            data = util.json_read(f'database/articles/plants/{filename}')
            try: lastmod_entity = data['lastmod']
            except: lastmod_entity = lastmod
            # print(filename)
            sitemap += f'''
<url>
  <loc>https://terrawhisper.com/{filename_html}</loc>
  <lastmod>{lastmod_entity}</lastmod>
</url>
'''.strip() + '\n'

        # MEDICINE, ETC...
        elif os.path.isdir(f'database/articles/plants/{filename}'):
            for filename_2 in os.listdir(f'database/articles/plants/{filename}'):
                if filename_2.endswith('.json'):
                    filename_2_html = filename_2.replace('.json', '.html')
                    sitemap += f'''
<url>
  <loc>https://terrawhisper.com/{filename}/{filename_2_html}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
'''.strip() + '\n'
                # BENEFITS, ETC...
                elif os.path.isdir(f'database/articles/plants/{filename}/{filename_2}'):
                    for filename_3 in os.listdir(f'database/articles/plants/{filename}/{filename_2}'):
                        if filename_3.endswith('.json'):
                            filename_3_html = filename_3.replace('.json', '.html')
                            sitemap += f'''
<url>
  <loc>https://terrawhisper.com/{filename}/{filename_2}/{filename_3_html}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
'''.strip() + '\n'

    sitemap += '''
</urlset>
'''
    util.file_write('sitemap_plants.xml', sitemap.strip())





def sitemap_main():
    sitemap = ''
    sitemap += '''
<?xml version="1.0" encoding="UTF-8"?>
<urlset
      xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">


'''

    sitemap += f'''
<url>
  <loc>https://terrawhisper.com/</loc>
  <lastmod>2024-03-17T17:42:42+00:00</lastmod>
</url>
'''.strip() + '\n'
    sitemap += f'''
<url>
  <loc>https://terrawhisper.com/herbalism.html</loc>
  <lastmod>2024-03-17T17:42:42+00:00</lastmod>
</url>
'''.strip() + '\n'
    sitemap += f'''
<url>
  <loc>https://terrawhisper.com/herbalism/tea.html</loc>
  <lastmod>2024-03-17T17:42:42+00:00</lastmod>
</url>
'''.strip() + '\n'
    sitemap += f'''
<url>
  <loc>https://terrawhisper.com/top-herbs.html</loc>
  <lastmod>2024-03-17T17:42:42+00:00</lastmod>
</url>
'''.strip() + '\n'
    sitemap += f'''
<url>
  <loc>https://terrawhisper.com/about.html</loc>
  <lastmod>2024-03-17T17:42:42+00:00</lastmod>
</url>
'''.strip() + '\n'

    sitemap += '''

</urlset>
'''
    util.file_write('sitemap_main.xml', sitemap.strip())


    
