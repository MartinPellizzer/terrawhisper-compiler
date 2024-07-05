
from PIL import Image, ImageDraw, ImageFont
import random
import os
import data_csv
import util
import g


c_dark = '#030712'
c_holy = '#f5f5f5'
c_bg = '#f5f5f5'



def img_resize(img, w, h):
    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    return img


def text_to_lines(text, font, line_width_max):
    lines = []

    words = text.split()
    line_curr = ''
    for word in words:
        _, _, line_w, _ = font.getbbox(line_curr)
        _, _, word_w, _ = font.getbbox(word)
        if line_w + word_w < line_width_max:
            line_curr += f'{word} '
        else:
            if line_curr != '':
                lines.append(line_curr.strip())
            line_curr = f'{word} '
    lines.append(line_curr.strip())

    return lines


def image_template_causes(image_filepath_out, data):
    img_w, img_h = 768, 512
    p_x = 48
    stroke_w = 1
    font_size = img_w//12
    img = Image.new(mode="RGB", size=(img_w, img_h), color=c_dark)
    draw = ImageDraw.Draw(img)
    
    status_name = data['status_name']
    text = f'{status_name.upper()} CAUSES'
    font_size = 20
    font = ImageFont.truetype("assets/fonts/arial/ARIALBD.TTF", font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x = img_w//2 - text_w//2
    y = 30
    draw.text((x, y), text, c_holy, font=font)
    
    
    starting_y = 30

    x1 = img_w//2
    y1 = y + text_h + starting_y
    x2 = img_w//2
    y2 = img_h - 30
    draw.line((x1, y1, x2, y2), fill=c_holy, width=1)

    lines = data['causes_list']
    for i, item in enumerate(lines):
        line_length = 100
        line_length = line_length - random.randint(0, int(line_length*0.5))
        if i % 2 == 0: offset = 0
        else: offset = line_length

        x1 = img_w//2 - line_length + offset
        y1 = y + text_h + starting_y + (i*40) + 20
        x2 = img_w//2 + offset
        y2 = y + text_h + starting_y + (i*40) + 20

        draw.line((x1, y1, x2, y2), fill=c_holy, width=1)

        r = 4
        if i % 2 == 0: 
            c_x = x1
            c_y = y1
        else: 
            c_x = x2
            c_y = y2
        draw.ellipse((c_x - r, c_y - r, c_x + r, c_y + r), fill=c_holy)

        chunks = item.split(':')
        text = chunks[0].strip()
        font_size = 14
        font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)
        _, _, text_w, text_h = font.getbbox(text)
        
        if i % 2 == 0: 
            t_x = c_x - text_w - 20
        else: 
            t_x = c_x + 20
        t_y = c_y - font_size//2
        draw.text((t_x, t_y), text, c_holy, font=font)






    # r = 192
    # draw.ellipse((img_w//2 - r, img_h//2 - r, img_w//2 + r, img_h//2 + r), fill=(255, 255, 255))
    # draw.ellipse(
    #     (img_w//2 - r + stroke_w, img_h//2 - r + stroke_w, img_w//2 + r - stroke_w, img_h//2 + r - stroke_w), 
    #     fill=c_dark)
    
    # r = 128
    # draw.ellipse((img_w//2 - r, img_h//2 - r, img_w//2 + r, img_h//2 + r), fill=(255, 255, 255))
    # draw.ellipse(
    #     (img_w//2 - r + stroke_w, img_h//2 - r + stroke_w, img_w//2 + r - stroke_w, img_h//2 + r - stroke_w), 
    #     fill=c_dark)
        
    # r = 64
    # draw.ellipse((img_w//2 - r, img_h//2 - r, img_w//2 + r, img_h//2 + r), fill=(255, 255, 255))
    
    # text = 'CAUSES'
    # font_size = 20
    # font = ImageFont.truetype("assets/fonts/arial/ARIALBD.TTF", font_size)
    # _, _, text_w, text_h = font.getbbox(text)
    # draw.text(
    #     (img_w//2 - text_w//2, img_h//2 - text_h//2), 
    #     text, c_dark, font=font)

    # font_size = 14
    # font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)
    # pos_list = [
    #     [0, -128],
    #     [0, 128],
    #     [0, -192],
    #     [0, 192],
    #     [-192, 0],
    #     [192, 0],
    #     [-160, -128],
    #     [160, -128],
    #     [-160, 128],
    #     [160, 128],
    # ]
    
    # lines = data['causes_list']
    # text_height_max = 0
    # for i, item in enumerate(lines):
    #     chunks = item.split(':')
    #     text = chunks[0].strip()
    #     _, _, text_w, text_h = font.getbbox(item)
    #     if text_height_max < text_h: text_height_max = text_h

    # for i, item in enumerate(lines):
    #     chunks = item.split(':')
    #     text = chunks[0].strip()
    #     _, _, text_w, _ = font.getbbox(text)
    #     text_h = text_height_max
    #     px = 8
    #     py = px
    #     x1 = img_w//2 - text_w//2 + pos_list[i][0]
    #     y1 = img_h//2 - text_h//2 + pos_list[i][1]
    #     x2 = img_w//2 + text_w//2 + pos_list[i][0]
    #     y2 = img_h//2 + text_h//2 + pos_list[i][1]
    #     draw.rectangle(((x1 - px, y1 - py), (x2 + px, y2 + py)), fill=c_dark)
    #     draw.text((x1, y1), text, '#ffffff', font=font)

    img.save(image_filepath_out, quality=50) 


def image_template_herbs(image_filepath_out, data):
    img_w, img_h = 768, 512
    p_x = 48
    stroke_w = 1
    font_size = img_w//12
    img = Image.new(mode="RGB", size=(img_w, img_h), color=c_dark)
    draw = ImageDraw.Draw(img)
    
    r = 192
    draw.ellipse((img_w//2 - r, img_h//2 - r, img_w//2 + r, img_h//2 + r), fill=(255, 255, 255))
    draw.ellipse(
        (img_w//2 - r + stroke_w, img_h//2 - r + stroke_w, img_w//2 + r - stroke_w, img_h//2 + r - stroke_w), 
        fill=c_dark)
    
    r = 128
    draw.ellipse((img_w//2 - r, img_h//2 - r, img_w//2 + r, img_h//2 + r), fill=(255, 255, 255))
    draw.ellipse(
        (img_w//2 - r + stroke_w, img_h//2 - r + stroke_w, img_w//2 + r - stroke_w, img_h//2 + r - stroke_w), 
        fill=c_dark)
        
    r = 64
    draw.ellipse((img_w//2 - r, img_h//2 - r, img_w//2 + r, img_h//2 + r), fill=(255, 255, 255))
    
    text = 'HERBS'
    font_size = 20
    font = ImageFont.truetype("assets/fonts/arial/ARIALBD.TTF", font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text(
        (img_w//2 - text_w//2, img_h//2 - text_h//2), 
        text, c_dark, font=font)

    font_size = 14
    font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)
    pos_list = [
        [0, -128],
        [0, 128],
        [0, -192],
        [0, 192],
        [-192, 0],
        [192, 0],
        [-160, -128],
        [160, -128],
        [-160, 128],
        [160, 128],
    ]
    
    lines = data['herbs_list']
    text_height_max = 0
    for i, item in enumerate(lines):
        chunks = item.split(':')
        text = chunks[0].strip()
        _, _, text_w, text_h = font.getbbox(item)
        if text_height_max < text_h: text_height_max = text_h

    for i, item in enumerate(lines):
        chunks = item.split(':')
        text = chunks[0].strip()
        _, _, text_w, _ = font.getbbox(text)
        text_h = text_height_max
        px = 8
        py = px
        x1 = img_w//2 - text_w//2 + pos_list[i][0]
        y1 = img_h//2 - text_h//2 + pos_list[i][1]
        x2 = img_w//2 + text_w//2 + pos_list[i][0]
        y2 = img_h//2 + text_h//2 + pos_list[i][1]
        draw.rectangle(((x1 - px, y1 - py), (x2 + px, y2 + py)), fill=c_dark)
        draw.text((x1, y1), text, '#ffffff', font=font)

    img.save(image_filepath_out, quality=50) 


def image_template_preparations(image_filepath_out, data):
    img_w, img_h = 768, 512
    px = 48
    stroke_w = 1
    font_size = img_w//12
    img = Image.new(mode="RGB", size=(img_w, img_h), color=c_dark)
    draw = ImageDraw.Draw(img)
  
    status_name = data['status_name']
    text = f'HERBAL PREPARATIONS FOR {status_name.upper()}'
    font_size = 20
    font = ImageFont.truetype("assets/fonts/arial/ARIALBD.TTF", font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x = img_w//2 - text_w//2
    y = 30
    draw.text((x, y), text, c_holy, font=font)


    font_size = 14
    font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)
    
    lines = data['preparations_list']
    text_height_max = 0
    for i, item in enumerate(lines):
        chunks = item.split(':')
        text = chunks[0].strip()
        _, _, text_w, text_h = font.getbbox(item)
        if text_height_max < text_h: text_height_max = text_h

    gx = 16
    px = 64
    bx = 1
    by = 1
    rect_width = img_w // 4 - 32
    rect_height = 48

    gap_x = 16
    gap_y = 32
    
    x1 = img_w//2 - rect_width//2
    y1 = 96
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    draw.rectangle(((x1, y1), (x2, y2)), fill=c_holy)
    draw.rectangle(((x1 + bx, y1 + by), (x2 - bx, y2 - by)), fill=c_dark)
    
    draw.line((x1 + rect_width//4, y2, x1 + rect_width//4, y2 + gap_y), fill=c_holy, width=1)
    draw.line((x1 + (rect_width//4)*3, y2, x1 + (rect_width//4)*3, y2 + gap_y), fill=c_holy, width=1)

    line = lines[0].split(':')[0]
    _, _, text_w, _ = font.getbbox(line)
    draw.text((x1 + (x2-x1)//2 - text_w//2, y1 + (y2-y1)//2 - text_height_max//2), line, '#ffffff', font=font)



    x1 = img_w//2 - rect_width - gap_x//2
    y1 = 100 + rect_height + gap_y
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    draw.rectangle(((x1, y1), (x2, y2)), fill=c_holy)
    draw.rectangle(((x1 + bx, y1 + by), (x2 - bx, y2 - by)), fill=c_dark)
    
    draw.line((x1 + rect_width//4, y2, x1 + rect_width//4, y2 + gap_y), fill=c_holy, width=1)
    draw.line((x1 + (rect_width//4)*3, y2, x1 + (rect_width//4)*3, y2 + gap_y), fill=c_holy, width=1)

    line = lines[1].split(':')[0]
    _, _, text_w, _ = font.getbbox(line)
    draw.text((x1 + (x2-x1)//2 - text_w//2, y1 + (y2-y1)//2 - text_height_max//2), line, '#ffffff', font=font)

    x1 = img_w//2 + gap_x//2
    y1 = 100 + rect_height + gap_y
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    draw.rectangle(((x1, y1), (x2, y2)), fill=c_holy)
    draw.rectangle(((x1 + bx, y1 + by), (x2 - bx, y2 - by)), fill=c_dark)
    
    draw.line((x1 + rect_width//4, y2, x1 + rect_width//4, y2 + gap_y), fill=c_holy, width=1)
    draw.line((x1 + (rect_width//4)*3, y2, x1 + (rect_width//4)*3, y2 + gap_y), fill=c_holy, width=1)

    line = lines[2].split(':')[0]
    _, _, text_w, _ = font.getbbox(line)
    draw.text((x1 + (x2-x1)//2 - text_w//2, y1 + (y2-y1)//2 - text_height_max//2), line, '#ffffff', font=font)



    x1 = img_w//2 - rect_width//2 - rect_width - gap_x
    y1 = 100 + rect_height*2 + gap_y*2
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    draw.rectangle(((x1, y1), (x2, y2)), fill=c_holy)
    draw.rectangle(((x1 + bx, y1 + by), (x2 - bx, y2 - by)), fill=c_dark)
    
    draw.line((x1 + rect_width//4, y2, x1 + rect_width//4, y2 + gap_y), fill=c_holy, width=1)
    draw.line((x1 + (rect_width//4)*3, y2, x1 + (rect_width//4)*3, y2 + gap_y), fill=c_holy, width=1)

    line = lines[3].split(':')[0]
    _, _, text_w, _ = font.getbbox(line)
    draw.text((x1 + (x2-x1)//2 - text_w//2, y1 + (y2-y1)//2 - text_height_max//2), line, '#ffffff', font=font)

    x1 = img_w//2 - rect_width//2
    y1 = 100 + rect_height*2 + gap_y*2
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    draw.rectangle(((x1, y1), (x2, y2)), fill=c_holy)
    draw.rectangle(((x1 + bx, y1 + by), (x2 - bx, y2 - by)), fill=c_dark)
    
    draw.line((x1 + rect_width//4, y2, x1 + rect_width//4, y2 + gap_y), fill=c_holy, width=1)
    draw.line((x1 + (rect_width//4)*3, y2, x1 + (rect_width//4)*3, y2 + gap_y), fill=c_holy, width=1)

    line = lines[4].split(':')[0]
    _, _, text_w, _ = font.getbbox(line)
    draw.text((x1 + (x2-x1)//2 - text_w//2, y1 + (y2-y1)//2 - text_height_max//2), line, '#ffffff', font=font)

    x1 = img_w//2 + rect_width//2 + gap_x
    y1 = 100 + rect_height*2 + gap_y*2
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    draw.rectangle(((x1, y1), (x2, y2)), fill=c_holy)
    draw.rectangle(((x1 + bx, y1 + by), (x2 - bx, y2 - by)), fill=c_dark)
    
    draw.line((x1 + rect_width//4, y2, x1 + rect_width//4, y2 + gap_y), fill=c_holy, width=1)
    draw.line((x1 + (rect_width//4)*3, y2, x1 + (rect_width//4)*3, y2 + gap_y), fill=c_holy, width=1)

    line = lines[5].split(':')[0]
    _, _, text_w, _ = font.getbbox(line)
    draw.text((x1 + (x2-x1)//2 - text_w//2, y1 + (y2-y1)//2 - text_height_max//2), line, '#ffffff', font=font)



    x1 = img_w//2 - rect_width*2 - gap_x - gap_x//2 
    y1 = 100 + rect_height*3 + gap_y*3
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    draw.rectangle(((x1, y1), (x2, y2)), fill=c_holy)
    draw.rectangle(((x1 + bx, y1 + by), (x2 - bx, y2 - by)), fill=c_dark)

    line = lines[6].split(':')[0]
    _, _, text_w, _ = font.getbbox(line)
    draw.text((x1 + (x2-x1)//2 - text_w//2, y1 + (y2-y1)//2 - text_height_max//2), line, '#ffffff', font=font)

    x1 = img_w//2 - rect_width - gap_x//2
    y1 = 100 + rect_height*3 + gap_y*3
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    draw.rectangle(((x1, y1), (x2, y2)), fill=c_holy)
    draw.rectangle(((x1 + bx, y1 + by), (x2 - bx, y2 - by)), fill=c_dark)

    line = lines[7].split(':')[0]
    _, _, text_w, _ = font.getbbox(line)
    draw.text((x1 + (x2-x1)//2 - text_w//2, y1 + (y2-y1)//2 - text_height_max//2), line, '#ffffff', font=font)

    x1 = img_w//2 + gap_x//2
    y1 = 100 + rect_height*3 + gap_y*3
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    draw.rectangle(((x1, y1), (x2, y2)), fill=c_holy)
    draw.rectangle(((x1 + bx, y1 + by), (x2 - bx, y2 - by)), fill=c_dark)

    line = lines[8].split(':')[0]
    _, _, text_w, _ = font.getbbox(line)
    draw.text((x1 + (x2-x1)//2 - text_w//2, y1 + (y2-y1)//2 - text_height_max//2), line, '#ffffff', font=font)

    x1 = img_w//2 + rect_width + gap_x + gap_x//2 
    y1 = 100 + rect_height*3 + gap_y*3
    x2 = x1 + rect_width
    y2 = y1 + rect_height
    draw.rectangle(((x1, y1), (x2, y2)), fill=c_holy)
    draw.rectangle(((x1 + bx, y1 + by), (x2 - bx, y2 - by)), fill=c_dark)

    line = lines[9].split(':')[0]
    _, _, text_w, _ = font.getbbox(line)
    draw.text((x1 + (x2-x1)//2 - text_w//2, y1 + (y2-y1)//2 - text_height_max//2), line, '#ffffff', font=font)


    # line = 'Leen Randell'
    # font_size = 30
    # font = ImageFont.truetype("assets/fonts/Tangerine/Tangerine-Regular.TTF", font_size)
    # _, _, text_w, _ = font.getbbox(line)
    # draw.text((img_w//2 - text_w//2, img_h - 80), line, '#ffffff', font=font)
    
    line = 'TerraWhisper.com'.upper()
    font_size = 12
    font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)
    _, _, text_w, _ = font.getbbox(line)
    draw.text((img_w - text_w - 48, img_h - 50), line, '#ffffff', font=font)



    img.save(image_filepath_out, quality=50) 


def cheatsheet(image_filepath_out, data):
    title = data['title']
    
    
    img_width = 2480
    img_height = 3508
    gap_width = img_width//10
    x = gap_width
    y = 80
    w = img_width//3 + gap_width//3 - 32
    h = 64
    col_curr = 0
    c_dark = '#030712'
    c_bg = '#f5f5f5'

    img = Image.new(mode="RGB", size=(img_width, img_height), color=c_bg)
    draw = ImageDraw.Draw(img)

    # TITLE
    px = 64
    py = 64
    text = title.title()
    font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 72)
    _, _, text_w, text_h = font.getbbox(text)
    draw.rectangle(((x, y), (x + text_w + px*2, y + text_h + py*2)), fill=c_dark)
    draw.text(
        (x + px, y + py), 
        text,
        (255, 255, 255), font=font
    )
    by_line_x = x + text_w + px*2 + 64
    rect_h = text_h + py*2
    y_start = y + text_h + py*2 + 80
    
    # FOOTER
    text = 'by Leen Randell -- TerraWhisper.com'
    font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 48)
    draw.text(
        (x, img_height - 128), 
        text, c_dark, font=font
    )
    y = y_start

    # remedies
    remedies_list = data['remedies_list']
    for i, remedy_obj in enumerate(remedies_list[:10]):
        herb_name_common = remedy_obj['herb_name_common']
        if 'remedy_properties' not in remedy_obj: continue
        if 'remedy_parts' not in remedy_obj: continue
        remedy_properties = [item.split(':')[0] for item in remedy_obj['remedy_properties']]
        remedy_parts = [item.split(':')[0] for item in remedy_obj['remedy_parts']]
        random.shuffle(remedy_properties)
        random.shuffle(remedy_parts)
        remedy_properties = remedy_properties[:3]
        remedy_parts = remedy_parts[:3]

        # Calc Needed Height
        y_tmp = y
        y_tmp += h
        y_tmp += h
        for item in remedy_properties: y_tmp += h
        y_tmp += h
        for item in remedy_parts: y_tmp += h
        
        if y_tmp >= img_height:
            col_curr += 1
            if col_curr == 1:
                x = img_width//3 + gap_width//3 + 16
                y = y_start
                w = img_width - img_width//3 - gap_width//3 - 16
                h = 64
            if col_curr == 2:
                x = img_width - img_width//3 - gap_width//3 + 32
                y = y_start
                w = img_width - gap_width
                h = 64
            if col_curr == 3:
                print('ERROR: Not enough space to draw all remedies')
                break

        # Herb
        cell_herb_h = 96
        text_margin_l = 32
        text_margin_t = 20
        draw.rectangle(((x, y), (w, y + cell_herb_h)), fill=c_dark)
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)
        draw.text(
            (x + text_margin_l, y + text_margin_t), 
            f'{i+1}. {herb_name_common.upper()}', 
            c_bg, font=font
        )
        y += cell_herb_h

        # Properties Head
        cell_category_h = 96
        text_margin_t = 16
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)
        text_x, text_y, text_w, text_h = font.getbbox("Properties")
        draw.rectangle(
            (
                (x + text_margin_l + text_w + 32, y + cell_category_h//2), 
                (w, y + cell_category_h//2 + 4)
            ), 
            fill="#737373"
        )
        draw.text(
            (x + text_margin_l, y + text_margin_t), 
            'Properties', 
            c_dark, font=font
        )
        y += cell_category_h

        # Properties Vals
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 36)
        for item in remedy_properties:
            item = item.replace('properties', '')
            draw.rectangle(((x, y), (w, y + h)), fill=c_bg)
            draw.rectangle((
                (x + text_margin_l + 16, y + h//2 - 16), 
                (x + text_margin_l + 32, y + h//2)), fill=c_dark)
            draw.text(
            (x + text_margin_l + 48, y), 
                item, c_dark, font=font
            )
            y += h

        # Parts Head
        cell_category_h = 96
        text_margin_t = 16
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)
        text_x, text_y, text_w, text_h = font.getbbox("Plant Parts")
        draw.rectangle(
            (
                (x + text_margin_l + text_w + 32, y + cell_category_h//2), 
                (w, y + cell_category_h//2 + 4)
            ), 
            fill="#737373"
        )
        draw.text(
            (x + text_margin_l, y + text_margin_t), 
            'Plant Parts', c_dark, font=font
        )
        y += cell_category_h

        # Parts Vals
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 36)
        for item in remedy_parts:
            draw.rectangle(((x, y), (w, y + h)), fill=c_bg)
            draw.rectangle((
                (x + text_margin_l + 16, y + h//2 - 16), 
                (x + text_margin_l + 32, y + h//2)), fill=c_dark)
            draw.text(
            (x + text_margin_l + 48, y), 
                item, c_dark, font=font
            )
            y += h
        y += h

    img.thumbnail((img_width//3, img_height//3), Image.LANCZOS)
    img.save(image_filepath_out, quality=50) 
    print('SAVED CHEATSHEET:', image_filepath_out)



def template_remedy(image_filepath_out, obj, preparation_name):

    img_w, img_h = 768, 512
    img_padding_x = 80
    y = 0

    img = Image.new(mode="RGB", size=(img_w, img_h), color=c_dark)
    draw = ImageDraw.Draw(img)

    herb_name_common = obj['herb_name_common']
    text = f'{herb_name_common} {preparation_name}'.upper()
    # text = f'Eastern purple coneflower tea'.upper()
    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial/ARIALBD.TTF", font_size)

    words = text.split(' ')
    lines = []
    line_curr = ''
    for word in words:
        _, _, line_w, _ = font.getbbox(line_curr)
        _, _, word_w, _ = font.getbbox(word)
        if line_w + word_w < img_w - img_padding_x:
            line_curr += f'{word} '
        else:
            lines.append(line_curr)
            line_curr = f'{word} '
    if line_curr != '':
        lines.append(line_curr)

    y += 50
    for i, line in enumerate(lines):
        _, _, line_w, _ = font.getbbox(line)
        x = img_w//2 - line_w//2
        y += font_size*i*1.0
        draw.text((x, y), line, c_holy, font=font)

    herb_name_scientific = obj['herb_name_scientific']
    text = f'({herb_name_scientific})'
    font_size = 20
    font = ImageFont.truetype("assets/fonts/arial/ARIALI.TTF", font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x = img_w//2 - text_w//2
    y += 60
    draw.text((x, y), text, c_holy, font=font)


    y += 100
    if 'table':

        # v line
        x_1 = img_w//2
        y_1 = y
        x_2 = img_w//2
        y_2 = img_h - 130
        draw.line((x_1, y_1, x_2, y_2), fill=c_holy, width=1)

        if 'table_headers':
            header_font_size = 20
            header_gap_x = 20

            # header "properties"
            text = f'Properties'.upper()
            font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", header_font_size)
            _, _, text_w, text_h = font.getbbox(text)
            x = img_w//2 - text_w - header_gap_x
            draw.text((x, y), text, c_holy, font=font)

            # header "parts"
            text = f'Plant Parts'.upper()
            font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", header_font_size)
            _, _, text_w, text_h = font.getbbox(text)
            x = img_w//2 + header_gap_x
            draw.text((x, y), text, c_holy, font=font)
        
        # h line
        y += 30
        h_line_lenght = 400
        x_1 = img_w//2 - h_line_lenght//2
        y_1 = y
        x_2 = img_w//2 + h_line_lenght//2
        y_2 = y
        draw.line((x_1, y_1, x_2, y_2), fill=c_holy, width=1)

        if 'table_data':
            y += 10
            font_size = 14
            line_h = 1.4

            font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)

            # properties
            lines = [item.split(':')[0] for item in obj['remedy_properties']]
            for i, line in enumerate(lines):
                _, _, text_w, _ = font.getbbox(line)
                x_1 = img_w//2 - text_w - header_gap_x
                y_1 = y + font_size*line_h*i
                draw.text((x_1, y_1), line, c_holy, font=font)

            # parts
            lines = [item.split(':')[0] for item in obj['remedy_parts']]
            for i, line in enumerate(lines):
                _, _, text_w, _ = font.getbbox(line)
                x_1 = img_w//2 + header_gap_x
                y_1 = y + font_size*line_h*i
                draw.text((x_1, y_1), line, c_holy, font=font)

    
        text = f'TerraWhisper'.upper()
        font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", 12)
        _, _, text_w, text_h = font.getbbox(text)
        x_1 = img_w//2 +  - text_w//2
        y_1 = img_h - 50
        draw.text((x_1, y_1), text, c_holy, font=font)



    img.save(image_filepath_out, quality=50)
    # img.show()
    # quit()












def template_herb(filepath_out, data):
    img_w, img_h = 768, 512
    p_x = 48
    stroke_w = 1
    font_size = img_w//12
    img = Image.new(mode="RGB", size=(img_w, img_h), color=c_dark)
    draw = ImageDraw.Draw(img)

    herb_id = data['herb_id']
    herb_name_scientific = data['herb_name_scientific']

    herbs_names_common_rows, herbs_names_common_cols = data_csv.herbs_names_common()
    herb_name_common = ''
    for herb_name_common_row in herbs_names_common_rows:
        _id = herb_name_common_row[herbs_names_common_cols['herb_id']]
        _name_common = herb_name_common_row[herbs_names_common_cols['herb_name_common']]
        if _id == herb_id:
            herb_name_common = _name_common
            break

    gap_y = 10

    text = herb_name_scientific
    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial/ARIALBD.TTF", font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text(
        (img_w//2 - text_w//2, img_h//2 - text_h - gap_y//2), 
        text, c_holy, font=font)

    text = herb_name_common
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial/ARIALI.TTF", font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text(
        (img_w//2 - text_w//2, img_h//2 + gap_y//2), 
        f'({text})', c_holy, font=font)

    img.save(filepath_out, quality=50) 
    # img.show()
    


def template_preparation(filepath_out, data):
    img_w, img_h = 768, 512
    p_x = 48
    stroke_w = 1
    font_size = img_w//12
    img = Image.new(mode="RGB", size=(img_w, img_h), color=c_dark)
    draw = ImageDraw.Draw(img)

    preparation_name = data['preparation_name']
    status_name = data['status_name']
    print(preparation_name, status_name)

    gap_y = 10

        
    text = status_name.title()
    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial/ARIALBD.TTF", font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text(
        (img_w//2 - text_w//2, img_h//2 - text_h - gap_y//2), 
        text, c_holy, font=font)

    text = f'best herbal {preparation_name}'
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial/ARIALI.TTF", font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text(
        (img_w//2 - text_w//2, img_h//2 + gap_y//2), 
        text, c_holy, font=font)


    img.save(filepath_out, quality=50) 
    # img.show()

    # quit()

