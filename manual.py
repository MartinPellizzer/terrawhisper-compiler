import os
import random
import shutil

herbs = [
    'Feverfew',
    'Willow Bark',
    'Ginger',
    'Peppermint',
    'Lavender',
    'Chamomile',
    'Lemon Balm',
    'Clove',
    'Turmeric',
    'Valerian',
    'Lime Tree',
    'Sichuan Lovage',
    'Boldo',
    'Oregano',
    'Rosemary',
    'Ginkgo Biloba',
    'Passionflower',
    'Skullcap',
    'Catnip',
    'Butterbur',
    'Hibiscus',
]

images_folder = 'C:/terrawhisper-assets/images/tea'
for herb in herbs:
    herb = herb.replace(' ', '-').lower()
    images = os.listdir(f'{images_folder}/{herb}')
    random.shuffle(images)
    shutil.copy2(f'{images_folder}/{herb}/{images[0]}', f'tmp-images/{herb}-tea-for-headaches.jpg')