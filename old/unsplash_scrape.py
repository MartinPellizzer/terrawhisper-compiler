import requests
import os

import util


ACCESS_KEY = util.file_read('C:/api-keys/unsplash-api-key.txt')

query = 'cheese'
url = f'https://api.unsplash.com/search/photos?page=1&query={query}&client_id={ACCESS_KEY}'
response = requests.get(url)
data = response.json()
results = data['results']
for i, result in enumerate(results):
    url = result['urls']['regular']
    filename = f'{i}.jpg'
    image_response = requests.get(url, stream=True)
    print(image_response)
    if image_response.status_code == 200:
        with open(f'scraped/images/{filename}', 'wb') as image_file:
            for chunck in image_response:
                image_file.write(chunck)
    print(url)