from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
import os
import random
import utils
import csv
import shutil

def img_generate(line_1, line_2, img1_filepath, img2_filepath, out_filename):
    img_w, img_h = 1000, 1500
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#e7e5e4')
    
    img1 = Image.open(img1_filepath)
    img2 = Image.open(img2_filepath)

    img1.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img1 = ImageOps.mirror(img1)
    img2.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img2 = ImageOps.mirror(img2)
    img2_w, img2_h = img2.size

    img.paste(img1, (0, 0))
    img.paste(img2, (0, img_h - img2_h))

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(
        "assets/fonts/playfairdisplay/PlayfairDisplay-Italic.ttf", 
        72,
    )
    text = 'how to make effective'
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 - text_h*0.75), text, '#1c1917', font=font)

    font = ImageFont.truetype(
        "assets/fonts/playfairdisplay/PlayfairDisplay-Black.ttf", 
        96,
    )
    text = 'medicinal herbal tea'
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + text_h*0.25), text, '#1c1917', font=font)

    # img.show()

    img.save(
        f'pinterest/tmp/{i}.jpg',
        format='JPEG',
        subsampling=0,
        quality=100,
    )



def gen_img_template_1(line_1, line_2, img1_filepath, img2_filepath, out_filename):
    img_w, img_h = 1000, 1500
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#e7e5e4')
    
    img1 = Image.open(img1_filepath)
    img2 = Image.open(img2_filepath)

    img1.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img1 = ImageOps.mirror(img1)
    img1_w, img1_h = img1.size

    img2.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img2 = ImageOps.mirror(img2)
    img2_w, img2_h = img2.size

    img.paste(img1, (0, 0 - int(img1_h*0.25)))
    img.paste(img2, (0, img_h - int(img2_h*0.75)))

    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, img_h//2 - 160), (img_w, img_h//2 + 160)), fill="#e7e5e4")

    font = ImageFont.truetype(
        "assets/fonts/playfairdisplay/PlayfairDisplay-Italic.ttf", 
        72,
    )
    text = '5 simple steps to make'
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 - text_h*0.75), text, '#1c1917', font=font)

    font = ImageFont.truetype(
        "assets/fonts/playfairdisplay/PlayfairDisplay-Black.ttf", 
        96,
    )
    text = 'effective herbal tea'
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + text_h*0.25), text, '#1c1917', font=font)

    # img.show()

    img.save(
        f'pinterest/tmp/{i}.jpg',
        format='JPEG',
        subsampling=0,
        quality=100,
    )



def gen_img_template_2(line_1, line_2, img1_filepath, img2_filepath, img3_filepath, out_filename):
    img_w, img_h = 1000, 1500
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#e7e5e4')
    
    img1 = Image.open(img1_filepath)
    img2 = Image.open(img2_filepath)
    img3 = Image.open(img3_filepath)

    img1.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img1 = ImageOps.mirror(img1)
    img1_w, img1_h = img1.size

    img2.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img2 = ImageOps.mirror(img2)
    img2_w, img2_h = img2.size

    img3.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img3 = ImageOps.mirror(img3)
    img3_w, img3_h = img3.size

    img.paste(img1, (0, 0 - int(img1_h*0.25)))
    img.paste(img2, (0 - int(img2_h*0.50), img_h - int(img2_h*0.75)))
    img.paste(img3, (0 + int(img3_h*0.50), img_h - int(img3_h*0.75)))

    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, img_h//2 - 160), (img_w, img_h//2 + 160)), fill="#e7e5e4")
    draw.rectangle(((img_w//2 - 4, img_h//2 + 160), (img_w//2 + 4, img_h)), fill="#e7e5e4")

    font = ImageFont.truetype(
        "assets/fonts/playfairdisplay/PlayfairDisplay-Italic.ttf", 
        72,
    )
    text = '5 simple steps to make'
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 - text_h*0.75), text, '#1c1917', font=font)

    font = ImageFont.truetype(
        "assets/fonts/playfairdisplay/PlayfairDisplay-Black.ttf", 
        96,
    )
    text = 'effective herbal tea'
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + text_h*0.25), text, '#1c1917', font=font)

    # img.show()

    img.save(
        f'pinterest/tmp/{i}.jpg',
        format='JPEG',
        subsampling=0,
        quality=100,
    )


try: shutil.rmtree('pinterest/tmp')
except: pass
try: os.mkdir('pinterest/tmp')
except: pass

img_folderpath = 'C:/tw-images/database/preparations/tea/general'
for i in range(3):
    img_lst = os.listdir(img_folderpath)
    random.shuffle(img_lst)
    img1_filename = img_lst.pop()
    img2_filename = img_lst.pop()
    img3_filename = img_lst.pop()

    img1_filepath = f'{img_folderpath}/{img1_filename}'
    img2_filepath = f'{img_folderpath}/{img2_filename}'
    img3_filepath = f'{img_folderpath}/{img3_filename}'

    # img1_filepath = f'C:/tw-images/tea/5x3/0000.png'
    # img2_filepath = f'C:/tw-images/tea/5x3/0001.png'
    gen_img_template_2(
        'line 1', 
        'line 2', 
        img1_filepath, 
        img2_filepath,
        img3_filepath,
        i,
    )
