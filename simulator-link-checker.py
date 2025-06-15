import util
import os
import pathlib
from bs4 import BeautifulSoup


path = pathlib.Path('website/herbalism')
filepaths = path.rglob("*.html")

links = set()
for filepath in filepaths: 
    filepath = str(filepath)
    html = util.file_read(filepath)
    soup = BeautifulSoup(html)
    for link in soup.findAll('a'):
        href = link.get('href')
        if '/herbalism' in href:
            # print(href)
            links.add((filepath, href))
    # print(filepath)

for item in links:
    if not os.path.exists(f'website{item[1]}'):
        print(item[0], item[1])