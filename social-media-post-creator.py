from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
import os
import random
import utils
import csv
import shutil



def img_generate(line_1, line_2, img_filepath, out_filename):
    img_w, img_h = 1024, 1024
    OPACITY = 0.8
    img = Image.new(mode="RGBA", size=(img_w, img_h), color='#e7e5e4')
    
    img1 = Image.open(img_filepath)
    img.paste(img1, (0, 0))

    draw = ImageDraw.Draw(img)


    ##########################
    # Calc height
    ##########################

    curr_y = 50

    text = 'herb of the week'
    font_size = 48
    font = ImageFont.truetype("assets/fonts/playfairdisplay/PlayfairDisplay-Italic.ttf", font_size)
    text_w, text_h = font.getbbox(text)[2], font.getbbox(text)[3]
    # draw.text((img_w//2 - text_w//2, curr_y), text, '#e7e5e4', font=font)
    curr_y += font_size

    text = 'Cayenne'
    font_size = 96
    font = ImageFont.truetype("assets/fonts/playfairdisplay/PlayfairDisplay-Black.ttf", font_size)
    text_w, text_h = font.getbbox(text)[2], font.getbbox(text)[3]
    # draw.text((img_w//2 - text_w//2, curr_y), text, '#e7e5e4', font=font)
    curr_y += font_size + 96



    text = '5 surprising benefits of basil for health-conscious women (according to modern medicine).'
    font = ImageFont.truetype("assets/fonts/playfairdisplay/arial.ttf", 48)
    
    padding = 150
    words = text.split(' ')
    lines = []
    curr_line = ''
    for word in words:
        word_w = font.getbbox(word)[2]
        curr_line_w = font.getbbox(curr_line.strip())[2]
        if word_w + curr_line_w < img_w - padding*2:
            curr_line += f'{word} '
        else:
            lines.append(curr_line)
            curr_line = f'{word} '
    lines.append(curr_line)

    line_spacing = int(36 * 1.5)
    for i, line in enumerate(lines):
        text_w = font.getbbox(line)[2]
        text_h = font.getbbox(line)[3]
        # draw.text((img_w//2 - text_w//2, curr_y + (line_spacing * i)), line, '#e7e5e4', font=font)
    curr_y += text_h + (line_spacing * i)


    triangle_size = 16
    # draw.rectangle(((0 + 400, 0 + curr_y + 30), (0 + 400 + 200, 0 + curr_y + 30 + 4)), fill='#e7e5e4')
    # draw.polygon([(400 + 200, curr_y + 30 + 2 - triangle_size), (400 + 200 + triangle_size, curr_y + 30 + 2), (400 + 200, curr_y + 30 + 2 + triangle_size)], fill='#e7e5e4')
    curr_y += text_h + 96

    text = 'TerraWhisper'
    font = ImageFont.truetype("assets/fonts/playfairdisplay/arial.ttf", 24)
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    # draw.text((img_w//2 - text_w//2, curr_y), text, '#e7e5e4', font=font)
    curr_y += text_h + 30


    tot_height = curr_y

    ##########################
    # Draw
    ##########################
    offset_y = (img_h - tot_height)//2
    # offset_y = 0
    
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle(((0 + 100, offset_y), (img_w - 100, tot_height + offset_y)), fill=(0, 0, 0, int(255*OPACITY)))

    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")

    curr_y = offset_y + 50

    decor_y = 35
    decor_w = 150
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0 + 150, 0 + decor_y + curr_y), (0 + 150 + decor_w, 0 + decor_y + 4 + curr_y)), fill='#e7e5e4')
    draw.rectangle(((img_w - 150 - decor_w, 0 + decor_y + curr_y), (img_w - 150, 0 + decor_y + 4 + curr_y)), fill='#e7e5e4')


    text = 'herb of the week'
    font_size = 48
    font = ImageFont.truetype("assets/fonts/playfairdisplay/PlayfairDisplay-Italic.ttf", font_size)
    text_w, text_h = font.getbbox(text)[2], font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, curr_y), text, '#e7e5e4', font=font)
    curr_y += font_size

    text = 'Cayenne'
    font_size = 96
    font = ImageFont.truetype("assets/fonts/playfairdisplay/PlayfairDisplay-Black.ttf", font_size)
    text_w, text_h = font.getbbox(text)[2], font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, curr_y), text, '#e7e5e4', font=font)
    curr_y += font_size + 96



    text = '5 surprising benefits of basil for health-conscious women (according to modern medicine).'
    font = ImageFont.truetype("assets/fonts/playfairdisplay/arial.ttf", 48)
    
    padding = 150
    words = text.split(' ')
    lines = []
    curr_line = ''
    for word in words:
        word_w = font.getbbox(word)[2]
        curr_line_w = font.getbbox(curr_line.strip())[2]
        if word_w + curr_line_w < img_w - padding*2:
            curr_line += f'{word} '
        else:
            lines.append(curr_line)
            curr_line = f'{word} '
    lines.append(curr_line)

    line_spacing = int(36 * 1.5)
    for i, line in enumerate(lines):
        text_w = font.getbbox(line)[2]
        text_h = font.getbbox(line)[3]
        draw.text((img_w//2 - text_w//2, curr_y + (line_spacing * i)), line, '#e7e5e4', font=font)
    curr_y += text_h + (line_spacing * i)


    triangle_size = 16
    draw.rectangle(((0 + 400, 0 + curr_y + 30), (0 + 400 + 200, 0 + curr_y + 30 + 4)), fill='#e7e5e4')
    draw.polygon([(400 + 200, curr_y + 30 + 2 - triangle_size), (400 + 200 + triangle_size, curr_y + 30 + 2), (400 + 200, curr_y + 30 + 2 + triangle_size)], fill='#e7e5e4')
    curr_y += text_h + 96

    text = 'TerraWhisper'
    font = ImageFont.truetype("assets/fonts/playfairdisplay/arial.ttf", 24)
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, curr_y), text, '#e7e5e4', font=font)
    curr_y += text_h + 30



    # img.show()
    # quit()


    img.save(
        f'social-media/tmp/{out_filename}.jpg',
        format='JPEG',
        subsampling=0,
        quality=100,
    )


def img_twitter_4_squares(
    line_1, 
    line_2, 
    line_3, 
    line_4, 
    img1_filepath,
    img2_filepath,
    img3_filepath,
    img4_filepath,
    out_filename):

    img_w, img_h = 1024, 1024
    OPACITY = 0.8
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#e7e5e4')
    
    img1 = Image.open(img1_filepath)
    img2 = Image.open(img2_filepath)
    img3 = Image.open(img3_filepath)
    img4 = Image.open(img4_filepath)

    img1.thumbnail((img_w//2, img_h//2), Image.Resampling.LANCZOS)
    img2.thumbnail((img_w//2, img_h//2), Image.Resampling.LANCZOS)
    img3.thumbnail((img_w//2, img_h//2), Image.Resampling.LANCZOS)
    img4.thumbnail((img_w//2, img_h//2), Image.Resampling.LANCZOS)

    img.paste(img1, (0, 0))
    img.paste(img2, (img_w//2, 0))
    img.paste(img3, (0, img_h//2))
    img.paste(img4, (img_w//2, img_h//2))

    draw = ImageDraw.Draw(img)

    padding_x = 20
    padding_t = 5
    padding_b = 10
    margin_bottom = padding_b + 50

    text = line_1
    font_size = 48
    font = ImageFont.truetype("assets/fonts/playfairdisplay/arial.ttf", font_size)
    text_w, text_h = font.getbbox(text)[2], font.getbbox(text)[3]
    draw.rectangle(
        ((img_w//4 - text_w//2 - padding_x, img_h//2 - text_h - margin_bottom - padding_t), 
        (img_w//4 + text_w//2 + padding_x, img_h//2 - margin_bottom + padding_b)), 
        fill='#e7e5e4')
    draw.text(
        (img_w//4 - text_w//2, img_h//2 - text_h - margin_bottom), 
        text, '#271C13', font=font)

    text = line_2
    font_size = 48
    font = ImageFont.truetype("assets/fonts/playfairdisplay/arial.ttf", font_size)
    text_w, text_h = font.getbbox(text)[2], font.getbbox(text)[3]
    draw.rectangle(
        ((int(img_w*0.75) - text_w//2 - padding_x, img_h//2 - text_h - margin_bottom - padding_t), 
        (int(img_w*0.75) + text_w//2 + padding_x, img_h//2 - margin_bottom + padding_b)), 
        fill='#e7e5e4')
    draw.text(
        (int(img_w*0.75) - text_w//2, img_h//2 - text_h - margin_bottom), 
        text, '#271C13', font=font)
        
        
    text = line_3
    font_size = 48
    font = ImageFont.truetype("assets/fonts/playfairdisplay/arial.ttf", font_size)
    text_w, text_h = font.getbbox(text)[2], font.getbbox(text)[3]
    draw.rectangle(
        ((img_w//4 - text_w//2 - padding_x, img_h - text_h - margin_bottom - padding_t), 
        (img_w//4 + text_w//2 + padding_x, img_h - margin_bottom + padding_b)), 
        fill='#e7e5e4')
    draw.text(
        (img_w//4 - text_w//2, img_h - text_h - margin_bottom), 
        text, '#271C13', font=font)

        
    text = line_4
    font_size = 48
    font = ImageFont.truetype("assets/fonts/playfairdisplay/arial.ttf", font_size)
    text_w, text_h = font.getbbox(text)[2], font.getbbox(text)[3]
    draw.rectangle(
        ((int(img_w*0.75) - text_w//2 - padding_x, img_h - text_h - margin_bottom - padding_t), 
        (int(img_w*0.75) + text_w//2 + padding_x, img_h - margin_bottom + padding_b)), 
        fill='#e7e5e4')
    draw.text(
        (int(img_w*0.75) - text_w//2, img_h - text_h - margin_bottom), 
        text, '#271C13', font=font)

    line_width = 4
    draw.rectangle(
        ((img_w//2 - line_width//2, 0), 
        (img_w//2 + line_width//2, img_h)), 
        fill='#e7e5e4')

    draw.rectangle(
        ((0, img_h//2 - line_width//2), 
        (img_w, img_h//2 + line_width//2)), 
        fill='#e7e5e4')


    # img.show()
    # quit()


    img.save(
        f'social-media/tmp/{out_filename}.jpg',
        format='JPEG',
        subsampling=0,
        quality=100,
    )


try: shutil.rmtree('social-media/tmp')
except: pass
try: os.mkdir('social-media/tmp')
except: pass

img1_folderpath = 'C:/Users/admin/Desktop/images/plant/lavender/0000.png'
img2_folderpath = 'C:/Users/admin/Desktop/images/plant/aloe-vera/0000.png'
img3_folderpath = 'C:/Users/admin/Desktop/images/plant/neem/0000.png'
img4_folderpath = 'C:/Users/admin/Desktop/images/plant/calendula/0000.png'
img_twitter_4_squares(
    'Lavender', 
    'Aloe Vera', 
    'Neem', 
    'Calendula', 
    img1_folderpath, 
    img2_folderpath, 
    img3_folderpath, 
    img4_folderpath, 
    'herbal-hacks-skin-acne'
)



