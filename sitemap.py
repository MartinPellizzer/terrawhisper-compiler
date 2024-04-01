import util
import os
import pathlib


def sitemap_all():
    sitemap = ''
    sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += sitemap_main()
    sitemap += sitemap_teas()
    sitemap += sitemap_plants()
    sitemap += '</urlset>\n'
    util.file_write('sitemap.xml', sitemap.strip())




def sitemap_teas():
    urls = ''
    for filename in os.listdir('database/articles/herbalism/tea'):
        if filename.endswith('.json'):
            filename_html = filename.replace('.json', '.html')
            urls += f'''
<url>
  <loc>https://terrawhisper.com/herbalism/teas/{filename_html}</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'

    return urls



# EXCLUDE ARTICLES IN "MEDICINE/" UTIL GENERATED THE HTMLS
def sitemap_plants():
    lastmod_dummy = '2024-03-17'
    urls = ''

    path = pathlib.Path('database/articles/plants')
    filepaths = path.rglob("*.json")

    for filepath in filepaths: 
        filepath = str(filepath)
        filepath_in = filepath.replace('\\', '/')
        filepath_out = filepath_in.replace('database/articles/', '').replace('.json', '.html')
        # if 'medicine/constituents' in filepath_in: continue
        if 'medicine/preparations' in filepath_in: continue
        if 'medicine/side-effects' in filepath_in: continue
        if 'medicine/precautions' in filepath_in: continue
        print(filepath_out)

        data = util.json_read(filepath_in)
        try: lastmod = data['lastmod']
        except: lastmod = lastmod_dummy
        urls += f'<url>\n'
        urls += f'  <loc>https://terrawhisper.com/{filepath_out}</loc>\n'
        urls += f'  <lastmod>{lastmod}</lastmod>\n'
        urls += f'</url>\n'

    return urls





def sitemap_main():
    urls = ''
    urls += f'''
<url>
  <loc>https://terrawhisper.com/</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://terrawhisper.com/herbalism.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://terrawhisper.com/herbalism/tea.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://terrawhisper.com/plants.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://terrawhisper.com/top-herbs.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://terrawhisper.com/about.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'

    return urls



    
