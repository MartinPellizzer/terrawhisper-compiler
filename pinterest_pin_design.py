import os
import random

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

import util
from lib import utils

def product_card_gen():
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGBA", size=(pin_w, pin_h), color='#ece0c4')
    draw = ImageDraw.Draw(img)
    x_off = 50
    y_off = 50
    col_n = 5
    row_n = 10
    gap = 20
    pin_w_adj = 900 - gap*(col_n-1)
    pin_h_adj = 1500 - gap*(row_n-1)
    # cards
    card_folderpath = 'assets/digital-products/cards/plants-new/cards-images'
    card_filepaths = [f'{card_folderpath}/{filename}' for filename in os.listdir(card_folderpath)]
    random.shuffle(card_filepaths)
    card_n = 23
    card_w = 900
    card_h = 1500
    card_i = 0
    no_more_cards = False
    for row_i in range(row_n):
        if no_more_cards: break
        for col_i in range(col_n):
            if no_more_cards: break
            card_img = Image.open(card_filepaths[card_i])
            card_w_resized = pin_w_adj//col_n
            card_h_resized = pin_h_adj//col_n
            card_img = util.img_resize(card_img, card_w_resized, card_h_resized)
            img.paste(card_img, (x_off+card_w_resized*col_i + gap*col_i, y_off+card_h_resized*row_i + gap*row_i))
            card_i += 1
            if card_i >= card_n: no_more_cards = True
    # label center
    label_img_w = 900
    label_img_h = 900
    label_img = Image.open('pinterest/components/label-0000.png')
    label_img.thumbnail((label_img_w, label_img_h), Image.LANCZOS)
    img.paste(label_img, (pin_w//2-label_img_w//2, pin_h//2-label_img_h//2), label_img)
    # rects top/bottom
    rect_h = 30
    draw.rectangle(((0, 0), (pin_w, rect_h)), fill='#262524')
    draw.rectangle(((0, pin_h-rect_h), (pin_w, pin_h)), fill='#262524')
    x1 = x_off+card_w_resized*3+gap*3
    y1 = y_off+card_h_resized*4+gap*4
    draw.rectangle(((x1, y1), (x1+pin_w, y1+pin_h)), fill='#262524')
    # copyright
    text = 'Terra Whisper'
    font_size = 48
    font_path = f"assets/fonts/allura/Allura-Regular.ttf"
    font = ImageFont.truetype(font_path, font_size)
    draw.text((675, 1325), text, '#ece0c4', font=font)
    # save img
    img = img.convert('RGB')
    img_filepath = f'pinterest/products-digital/botanical-name-cards.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=100)
    # img.show()
    # save json
    json_filepath = 'pinterest/products-digital/0000.json'
    json_data = {
        'pin_title': 'Botanical Name Card Medicinal Herb Study Flashcard Plant Name Latin Identification Learning Tool',
        'pin_href': 'https://www.etsy.com/listing/1905803593/40-botanical-name-card-medicinal-herb',
        'pin_description': '''This is a digital download. Beautifully designed printable deck of 40 botanical flashcards. Each 3x5" card features one medicinal plant, including its scientific name, plant family, and common names. Perfect for students, herbalists, and nature lovers alike. Styled with Victorian elegance and rustic charm, this digital deck blends old-world aesthetics with modern learning. Whether you're building your herbal knowledge or just love vintage botanical art, these cards are a practical study tool.''',
        'pin_img_filepath': img_filepath,
        'pin_board_name': 'Herb Digital Products',
    }
    utils.json_write(json_filepath, json_data)

product_card_gen()
