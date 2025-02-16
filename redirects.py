import os
import util

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
]

for redirect in redirects:
    print(redirect)
    url_new = redirect['url_new']
    url_old = redirect['url_old']
    url_new_local = url_new.replace('https://terrawhisper.com/', 'website/')
    url_old_local = url_old.replace('https://terrawhisper.com/', 'website/')
    if os.path.exists(url_new_local):
        content = util.file_read(url_new_local)
        content = content.replace(
            '<head>',
            f'<head>\n    <meta http-equiv="refresh" content="0; url={url_new}">'
        )
        util.file_write(url_old_local, content)
