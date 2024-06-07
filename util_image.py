
from PIL import Image, ImageDraw, ImageFont
import random
import os



c_dark = '#030712'
c_holy = '#f5f5f5'
c_bg = '#f5f5f5'

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