import os
import pathlib

import g
import util


problems_rows = util.csv_get_rows(g.CSV_PROBLEMS_FILEPATH)
problems_cols = util.csv_get_cols(problems_rows)
problems_rows = problems_rows[1:]

conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
conditions_cols = util.csv_get_cols(conditions_rows)
conditions_rows = conditions_rows[1:]
# print(conditions_rows)


systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]


problems_systems_rows = util.csv_get_rows(g.CSV_PROBLEMS_SYSTEMS_FILEPATH)
problems_systems_cols = util.csv_get_cols(problems_systems_rows)
problems_systems_rows = problems_systems_rows[1:]


def csv_get_system_by_problem(problem_id):
    system_row = []

    problems_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_SYSTEMS_FILEPATH, problems_systems_cols['problem_id'], problem_id,
    )

    if problems_systems_rows_filtered != []:
        problem_system_row = problems_systems_rows_filtered[0]
        system_id = problem_system_row[problems_systems_cols['system_id']]

        systems_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id,
        )

        if systems_rows_filtered != []:
            system_row = systems_rows_filtered[0]

    return system_row





def sitemap_all():
    sitemap = ''
    sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += sitemap_main()
    sitemap += sitemap_remedies_systems()
    sitemap += sitemap_remedies_systems_problems()
    # sitemap += sitemap_plants()
    sitemap += '</urlset>\n'
    util.file_write('sitemap.xml', sitemap.strip())


def sitemap_remedies_systems():
    urls = ''
    for system_row in systems_rows:
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}.json'
        
        if os.path.exists(json_filepath):
            data = util.json_read(json_filepath)
            lastmod = data['lastmod']
            
            html_filepath = f'https://terrawhisper.com/remedies/{system_slug}.html'
            urls += f'''
<url>
  <loc>{html_filepath}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
'''.strip() + '\n'

    return urls



def sitemap_remedies_systems_problems():
    urls = ''
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        print(f'> {problem_name}')

        system_row = csv_get_system_by_problem(problem_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        print(f'  > {system_name}')
        
        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}.json'
        if os.path.exists(json_filepath):
            data = util.json_read(json_filepath)
            lastmod = data['lastmod']
            
            html_filepath = f'https://terrawhisper.com/remedies/{system_slug}/{problem_slug}.html'
            urls += f'''
<url>
  <loc>{html_filepath}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
'''.strip() + '\n'

        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}/teas.json'
        if os.path.exists(json_filepath):
            data = util.json_read(json_filepath)
            lastmod = data['lastmod']
            
            html_filepath = f'https://terrawhisper.com/remedies/{system_slug}/{problem_slug}/teas.html'
            urls += f'''
<url>
  <loc>{html_filepath}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
'''.strip() + '\n'

        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}/tinctures.json'
        if os.path.exists(json_filepath):
            data = util.json_read(json_filepath)
            lastmod = data['lastmod']
            
            html_filepath = f'https://terrawhisper.com/remedies/{system_slug}/{problem_slug}/tinctures.html'
            urls += f'''
<url>
  <loc>{html_filepath}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
'''.strip() + '\n'

    return urls


# def sitemap_teas():
#   urls = ''
#   for condition_row in conditions_rows:
#     # print(condition_row)
#     condition_slug = condition_row[conditions_cols['condition_slug']].strip().lower()
#     to_process = condition_row[conditions_cols['to_process']].lower().strip()

#     if to_process == '': continue
#     if condition_slug == '': continue

#     # print(condition_slug)

#     html_filepath = f'https://terrawhisper.com/herbalism/tea/{condition_slug}.html'
#     urls += f'''
# <url>
#   <loc>{html_filepath}</loc>
#   <lastmod>2024-03-17</lastmod>
# </url>
# '''.strip() + '\n'

# #     urls = ''
# #     for filename in os.listdir('database/json/herbalism/tea'):
# #         if filename.endswith('.json'):
# #             filename_html = filename.replace('.json', '.html')
# #             urls += f'''
# # <url>
# #   <loc>https://terrawhisper.com/herbalism/tea/{filename_html}</loc>
# #   <lastmod>2024-03-17</lastmod>
# # </url>
# # '''.strip() + '\n'

#   return urls



# EXCLUDE ARTICLES IN "MEDICINE/" UTIL GENERATED THE HTMLS
# TODO: REDO
# def sitemap_plants():
#     lastmod_dummy = '2024-03-17'
#     urls = ''

#     path = pathlib.Path('database/articles/plants')
#     filepaths = path.rglob("*.json")

#     for filepath in filepaths: 
#         filepath = str(filepath)
#         filepath_in = filepath.replace('\\', '/')
#         filepath_out = filepath_in.replace('database/articles/', '').replace('.json', '.html')
#         # print(filepath_out)

#         data = util.json_read(filepath_in)
#         try: lastmod = data['lastmod']
#         except: lastmod = lastmod_dummy
#         urls += f'<url>\n'
#         urls += f'  <loc>https://terrawhisper.com/{filepath_out}</loc>\n'
#         urls += f'  <lastmod>{lastmod}</lastmod>\n'
#         urls += f'</url>\n'

#     return urls





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
  <loc>https://terrawhisper.com/remedies.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'

#     urls += f'''
# <url>
#   <loc>https://terrawhisper.com/herbalism/tea.html</loc>
#   <lastmod>2024-03-17</lastmod>
# </url>
# '''.strip() + '\n'

#     urls += f'''
# <url>
#   <loc>https://terrawhisper.com/plants.html</loc>
#   <lastmod>2024-03-17</lastmod>
# </url>
# '''.strip() + '\n'
#     urls += f'''
# <url>
#   <loc>https://terrawhisper.com/top-herbs.html</loc>
#   <lastmod>2024-03-17</lastmod>
# </url>
# '''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://terrawhisper.com/about.html</loc>
  <lastmod>2024-03-17</lastmod>
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

test_sitemap()