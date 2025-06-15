import os

from lib import g
from lib import io
from lib import utils
from lib import components

def medicine_poison_get(url):
    json_article_filepath = f'database/json/{url}.json'
    json_article = io.json_read(json_article_filepath)
    medicine_or_poison = json_article['medicine_or_poison']
    medicine = {'medicine_or_poison': 'medicine', 'total_score': 0}
    for _obj in medicine_or_poison:
        if 'medicine' in _obj['answer']: 
            medicine = _obj
            break
    poison = {'medicine_or_poison': 'poison', 'total_score': 0}
    for _obj in medicine_or_poison:
        if 'poison' in _obj['answer']: 
            poison = _obj
            break
    inert = {'medicine_or_poison': 'inert', 'total_score': 0}
    for _obj in medicine_or_poison:
        if 'inert' in _obj['answer']: 
            inert = _obj
            break
    if medicine['total_score'] > poison['total_score'] and medicine['total_score'] > inert['total_score']: return 'medicine'
    elif poison['total_score'] > medicine['total_score'] and poison['total_score'] > inert['total_score']: return 'poison'
    else: return 'inert'

def get_popular_herbs_from_teas_articles():
    output = []
    ailments = io.csv_to_dict('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}/teas'
        json_filepath = f'database/json/{url}.json'
        if os.path.exists(json_filepath):
            data = io.json_read(json_filepath, create=True)
            for obj in data['remedies']:
                found = False
                for item in output:
                    if obj['herb_name_scientific'] == item['herb_name_scientific']:
                        item['herb_total_score'] += obj['herb_total_score']
                        found = True
                        break
                if not found:
                    output.append({
                        'herb_name_scientific': obj['herb_name_scientific'],
                        'herb_total_score': obj['herb_total_score'],
                    })
    output = sorted(output, key=lambda x: x['herb_total_score'], reverse=True)
    return output


def gen():
    herbs_0000 = io.csv_to_dict(f'database/herbs-book-0000.csv')
    with open('database/herbs/books/medical-herbalism.txt') as f: herbs_0001 = f.read().split('\n')
    herbs = []
    for herb in herbs_0000: herbs.append(herb['latin_name'])
    for herb in herbs_0001: herbs.append(herb)
    herbs = list(set(herbs))
    herbs = sorted(herbs)

    html_cards = ''
    html_section_art = f'''
        <div style="margin-top: 1.6rem;" class="grid grid-4 gap-16">
    '''
    # herbs = get_popular_herbs_from_teas_articles()
    # herbs = sorted(herbs, key=lambda x: x['latin_name'].strip().lower(), reverse=False)
    i = 0
    for herb_i, herb in enumerate(herbs):
        print(f'\n>> {herb_i}/{len(herbs)} - {herb}')
        herb_name_scientific = herb.strip().capitalize()
        herb_slug = utils.sluggify(herb_name_scientific)
        url = f'herbs/{herb_slug}'
        ###
        medicine_or_poison = medicine_poison_get(f'herbs/{herb_slug}/benefits')
        if medicine_or_poison != 'medicine':
            continue
        ### 
        json_article_filepath = f'database/json/{url}.json'
        json_article = io.json_read(json_article_filepath)
        href = f'/{url}.html'
        src = f"/images/herbs/{herb_slug}.jpg" 
        title = json_article['title']
        html_section_art += components.card_art_html(
            href=href,
            src=src,
            title=title,
        )
        i += 1
    print(i)
    quit()

    html_section_art += f'''
        </div>
    '''
    print(html_section_art)

    html_filepath = f'{g.WEBSITE_FOLDERPATH}/herbs.html'
    page_title = f'medicinal herbs'
    html_breadcrumbs = components.breadcrumbs(f'herbs.html')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(page_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 24px;" class="container-xl">
                {html_breadcrumbs}
                {html_section_art}
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)
