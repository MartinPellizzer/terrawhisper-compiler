import os

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

def ailments_herbs_list_get(ailments_target):
    output_yes = []
    output_no = []
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')

    for ailment_target_i, ailment_target in enumerate(ailments_target):
        found = 0
        for ailment in ailments:
            ailment_name = ailment['ailment_name']
            if ailment_target.strip().lower() == ailment_name.strip().lower():
                output_yes.append(ailment)
                found = 1
                break
        if not found:
            output_no.append(ailment_target)
        
    ailments_herbs_list = []
    for ailment in output_yes:
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        json_article_filepath = f'database/pages/remedies/{system_slug}-system/{ailment_slug}/teas.json'
        json_article = json_read(json_article_filepath)
        preparations = json_article['preparations']
        preparations_names = [preparation['herb_name_scientific'] for preparation in preparations]
        ailments_herbs_list.append({
            'ailment_name': ailment_name,
            'preparations_names': preparations_names,
        })
        for ailment_herb in ailments_herbs_list:
            print(ailment_herb)

    return ailments_herbs_list

with open('assets/digital-products/checklists/ailments-herbs-shopping-list.txt') as f: 
    ailments = [line for line in f.read().split('\n') if line.strip() != '']

print(ailments)
print(len(ailments))

ailments_herbs_list = ailments_herbs_list_get(ailments)

PAGE_WIDTH, PAGE_HEIGHT = 2480, 3508

img = Image.new(mode="RGB", size=(PAGE_WIDTH, PAGE_HEIGHT), color='#ffffff')
draw = ImageDraw.Draw(img)

page_px = 128
y_start = 80
y_cur = y_start

# title
lines = ['THE ULTIMATE HERBAL TEA', 'SHOPPING LIST']
font_size = 160
font_family, font_weight = 'Lato', 'Black'
font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
font = ImageFont.truetype(font_path, font_size)
_, _, line_w, line_h = font.getbbox(lines[0])
draw.text((PAGE_WIDTH//2 - line_w//2, y_cur), lines[0], '#000000', font=font)
y_cur += font_size
_, _, line_w, line_h = font.getbbox(lines[1])
draw.text((PAGE_WIDTH//2 - line_w//2, y_cur), lines[1], '#000000', font=font)
y_cur += font_size
y_cur += 50

# subtitle
text = 'Effective herbal teas for the most common ailments'
font_size = 64
font_family, font_weight = 'Lato', 'Regular'
font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
font = ImageFont.truetype(font_path, font_size)
# lines = multiline(text, width=1600)
lines = [text]
for line in lines:
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((PAGE_WIDTH//2 - line_w//2, y_cur), line, '#000000', font=font)
    y_cur += font_size*1.3
y_cur += 130

# copyright
line = 'terrawhisper.com'
font_size = 36
font_family, font_weight = 'Lato', 'Regular'
font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
font = ImageFont.truetype(font_path, font_size)
_, _, line_w, line_h = font.getbbox(line)
x1 = PAGE_WIDTH - line_w - page_px
y1 = PAGE_HEIGHT - 80 - font_size
draw.text((x1, y1), line, '#000000', font=font)

# list
item_i = 0
col_1_w = 600
px = 128
cell_px = 32
cell_py = 8
y_cur = 600
for item in ailments_herbs_list:
    item_i += 1
    x_cur = 128

    ailment_name = f'{item_i}. {item["ailment_name"].title()}'
    font_size = 48
    line_h = 1.5
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    draw.rectangle([(x_cur, y_cur), (x_cur + col_1_w, y_cur + font_size*line_h + cell_py*2)], fill='#ffffff', outline='#000000', width=1)
    draw.text((x_cur+cell_px, y_cur + cell_py*1.5), ailment_name, '#000000', font=font)
    _, _, ailment_name_w, ailment_name_h = font.getbbox(ailment_name)
    x_cur += col_1_w

    herbs_names_scientific = ', '.join(item['preparations_names'][:3])
    font_size = 48
    line_h = 1.5
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    draw.rectangle([(x_cur, y_cur), (PAGE_WIDTH - px, y_cur + font_size*line_h + cell_py*2)], fill='#ffffff', outline='#000000', width=1)
    draw.text((x_cur+cell_px, y_cur + cell_py*1.5), herbs_names_scientific, '#000000', font=font)
    y_cur += font_size*line_h + cell_py*2

with open('assets/digital-products/checklists/ailments-herbs-shopping-list.txt') as f: 
    ailments = [line for line in f.read().split('\n') if line.strip() != '']

img.save(f'assets/digital-products/checklists/the-ultimate-herbal-tea-shopping-list.jpg')
img.show()
