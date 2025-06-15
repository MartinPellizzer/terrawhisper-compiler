import os
import util

from oliark_io import csv_read_rows_to_json

redirects = []
ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
for ailment in ailments:
    system_slug = f'{ailment["system_slug"]}-system'
    ailment_slug = f'{ailment["ailment_slug"]}'
    redirects.append({
        'url_old': f'https://terrawhisper.com/remedies/{system_slug}/{ailment_slug}/teas.html',
        'url_new': f'https://terrawhisper.com/ailments/{ailment_slug}/teas.html',
    })
    redirects.append({
        'url_old': f'https://terrawhisper.com/remedies/{system_slug}/{ailment_slug}/tinctures.html',
        'url_new': f'https://terrawhisper.com/ailments/{ailment_slug}/tinctures.html',
    })
    redirects.append({
        'url_old': f'https://terrawhisper.com/remedies/{system_slug}/{ailment_slug}/essential-oils.html',
        'url_new': f'https://terrawhisper.com/ailments/{ailment_slug}/essential-oils.html',
    })
    redirects.append({
        'url_old': f'https://terrawhisper.com/remedies/{system_slug}/{ailment_slug}/creams.html',
        'url_new': f'https://terrawhisper.com/ailments/{ailment_slug}/creams.html',
    })

for redirect in redirects:
    print(redirect)
    url_new = redirect['url_new']
    url_old = redirect['url_old']
    url_new_local = url_new.replace('https://terrawhisper.com/', '/home/ubuntu/vault/terrawhisper/website/terrawhisper/')
    url_old_local = url_old.replace('https://terrawhisper.com/', '/home/ubuntu/vault/terrawhisper/website/terrawhisper/')
    if os.path.exists(url_new_local):
        content = util.file_read(url_new_local)
        content = content.replace(
            '<head>',
            f'<head>\n    <meta http-equiv="refresh" content="0; url={url_new}">'
        )
        util.file_write(url_old_local, content)

