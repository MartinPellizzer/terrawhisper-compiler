from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
import random

import g

C_LUNAR_GREEN = '#324030'
C_OFF_WHITE = '#F5F5F5'
C_OIL = '#271C13'
C_SWIRL = '#D8D1CB'
C_BLACK = '#000000'


###########################################################################
# UTILS
###########################################################################

def pin_save(img, filename):
    img_filepath = f'{g.PINTEREST_TMP_IMAGE_FOLDERPATH}/{filename}.jpg'
    img.save(
        img_filepath,
        format='JPEG',
        subsampling=0,
        quality=100,
    )
    return img_filepath



###########################################################################
# BLOCKS
###########################################################################

def gen_text_num(img, line_list, num):
    if num == 0: return img

    num = str(num)
    img_w, img_h = 1000, 1500
    
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, img_h//2 - 160), (img_w, img_h//2 + 160)), fill=C_OFF_WHITE)

    circle_size = 300
    x = img_w//2-circle_size//2
    draw.ellipse(
        (
            img_w//2-circle_size//2, img_h//2 - circle_size//2 - 160, 
            img_w//2+circle_size//2, img_h//2 + circle_size//2 - 160,
        ), 
        fill=C_OFF_WHITE)

    
    font_size = 160
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = num
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    if random.randint(0, 100) < 50: color_rand = C_BLACK
    else: color_rand = C_LUNAR_GREEN
    draw.text((img_w//2 - text_w//2, img_h//2 - 200 - font_size//2), text, color_rand, font=font)


    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, 64)
    text = line_list[0]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 - text_h*0.7), text, C_BLACK, font=font)

    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, 96)
    text = line_list[1]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + text_h*0.4), text, color_rand, font=font)

    return img


def gen_text(img, line_list):
    img_w, img_h = 1000, 1500
    
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, img_h//2 - 160), (img_w, img_h//2 + 160)), fill='C_OFF_WHITE')

    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, 64)
    text = line_list[0]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 - text_h*0.9), text, C_OIL, font=font)

    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, 96)
    text = line_list[1]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + text_h*0.4), text, C_LUNAR_GREEN, font=font)

    # font_family, font_weight = 'Lato', 'Regular'
    # font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    # font = ImageFont.truetype(font_path, 64)
    # text = line_list[2]
    # text_w = font.getbbox(text)[2]
    # text_h = font.getbbox(text)[3]
    # draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + text_h*1.4), text, C_OIL, font=font)

    return img



###########################################################################
# TEMPLATES
###########################################################################

def gen_img_template(line_list, img_list, out_filename, num=0,):
    img_w, img_h = 1000, 1500
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#e7e5e4')
    
    img1 = Image.open(img_list[0])
    img2 = Image.open(img_list[1])
    img3 = Image.open(img_list[2])
    img4 = Image.open(img_list[3])

    img1.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img1 = ImageOps.mirror(img1)
    img1_w, img1_h = img1.size
    img2.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img2 = ImageOps.mirror(img2)
    img2_w, img2_h = img2.size
    img3.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img3 = ImageOps.mirror(img3)
    img3_w, img3_h = img3.size
    img4.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img4 = ImageOps.mirror(img4)
    img4_w, img4_h = img4.size

    img_num = random.randint(2, 4)
    if img_num == 2:
        img.paste(img1, (0, 0 - int(img1_h*0.25)))
        img.paste(img2, (0, img_h - int(img2_h*0.75)))
    if img_num == 3:
        if random.randint(0, 100) < 50:
            img.paste(img1, (0, 0 - int(img1_h*0.25)))
            img.paste(img2, (0 - int(img2_h*0.50), img_h - int(img2_h*0.75)))
            img.paste(img3, (0 + int(img3_h*0.50), img_h - int(img3_h*0.75)))
            draw = ImageDraw.Draw(img)
            draw.rectangle(((img_w//2 - 4, img_h//2 + 160), (img_w//2 + 4, img_h)), fill="#e7e5e4")
        else:
            img.paste(img2, (0 - int(img2_h*0.50), 0))
            img.paste(img3, (0 + int(img3_h*0.50), 0))
            img.paste(img1, (0, img_h - int(img1_h*0.75)))
            draw = ImageDraw.Draw(img)
            draw.rectangle(((img_w//2 - 4, 0), (img_w//2 + 4, img_h//2 - 160)), fill="#e7e5e4")
    if img_num == 4:
        img.paste(img1, (0 - int(img1_h*0.50), 0))
        img.paste(img2, (0 + int(img2_h*0.50), 0))
        img.paste(img3, (0 - int(img3_h*0.50), img_h - int(img3_h*0.75)))
        img.paste(img4, (0 + int(img4_h*0.50), img_h - int(img4_h*0.75)))
        draw = ImageDraw.Draw(img)
        draw.rectangle(((img_w//2 - 4, 0), (img_w//2 + 4, img_h//2 - 160)), fill="#e7e5e4")
        draw.rectangle(((img_w//2 - 4, img_h//2 + 160), (img_w//2 + 4, img_h)), fill="#e7e5e4")

    if num != 0: gen_text_num(img, line_list, num)
    else: gen_text(img, line_list)

    img_filepath = pin_save(img, out_filename)
    return img_filepath
    

