import os
import util

from oliark_io import csv_read_rows_to_json

ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
redirects = []
for ailment in ailments:
    system_slug = f'{ailment["system_slug"]}-system'
    ailment_slug = f'{ailment["ailment_slug"]}'
    redirects.append({
        'url_old': f'https://terrawhisper.com/herbalism/tea/{system_slug}/{ailment_slug}.html',
        'url_new': f'https://terrawhisper.com/remedies/{system_slug}/{ailment_slug}/teas.html',
    })

for redirect in redirects:
    print(redirect)
    url_new = redirect['url_new']
    url_old = redirect['url_old']
    url_new_local = url_new.replace('https://terrawhisper.com/', 'website-2/')
    url_old_local = url_old.replace('https://terrawhisper.com/', 'website-2/')
    if os.path.exists(url_new_local):
        content = util.file_read(url_new_local)
        content = content.replace(
            '<head>',
            f'<head>\n    <meta http-equiv="refresh" content="0; url={url_new}">'
        )
        print(url_old_local)
        util.file_write(url_old_local, content)

redirects = [
    {
        'url_old': 'https://terrawhisper.com/herbalism/teas/hydration.html',
        'url_new': 'https://terrawhisper.com/herbalism/tea/hydration.html',
    },
    {
        'url_old': 'https://terrawhisper.com/cassia-senna/medicine/constituents.html',
        'url_new': 'https://terrawhisper.com/plants/cassia-senna/medicine/constituents.html',
    },
    {
        'url_old': 'https://terrawhisper.com/citrus-bergamia.html',
        'url_new': 'https://terrawhisper.com/plants/citrus-bergamia.html',
    },
    {
        'url_old': 'https://terrawhisper.com/eupatorium-purpureum.html',
        'url_new': 'https://terrawhisper.com/plants/eupatorium-purpureum.html',
    },
    {
        'url_old': 'https://terrawhisper.com/amaranthus-hypochondriacus/medicine.html',
        'url_new': 'https://terrawhisper.com/plants/amaranthus-hypochondriacus/medicine.html',
    },
    {
        'url_old': 'https://terrawhisper.com/coffea-arabica.html',
        'url_new': 'https://terrawhisper.com/plants/coffea-arabica.html',
    },
    {
        'url_old': 'https://terrawhisper.com/desmodium-adscendens.html',
        'url_new': 'https://terrawhisper.com/plants/desmodium-adscendens.html',
    },
    {
        'url_old': 'https://terrawhisper.com/eschscholzia-californica.html',
        'url_new': 'https://terrawhisper.com/plants/eschscholzia-californica.html',
    },
    {
        'url_old': 'https://terrawhisper.com/herbalism/tea/respiratory-system/coughing-fits.html',
        'url_new': 'https://terrawhisper.com/remedies/respiratory-system/coughing-fits/teas.html',
    },
    {
        'url_old': 'https://terrawhisper.com/herbalism/tea/cardiovascular-system/cholesterol.html',
        'url_new': 'https://terrawhisper.com/remedies/endocrine-system/high-cholesterol/teas.html',
    },
    {
        'url_old': 'https://terrawhisper.com/herbalism/tea/integumentary-system/fungal-infection.html',
        'url_new': 'https://terrawhisper.com/remedies/integumentary-system/fungal-skin-infection/teas.html',
    },
]

for redirect in redirects:
    print(redirect)
    url_new = redirect['url_new']
    url_old = redirect['url_old']
    url_new_local = url_new.replace('https://terrawhisper.com/', 'website-2/')
    url_old_local = url_old.replace('https://terrawhisper.com/', 'website-2/')
    if os.path.exists(url_new_local):
        content = util.file_read(url_new_local)
        content = content.replace(
            '<head>',
            f'<head>\n    <meta http-equiv="refresh" content="0; url={url_new}">'
        )
        print(url_old_local)
        util.file_write(url_old_local, content)

