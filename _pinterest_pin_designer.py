import os

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

import util

VAULT_FOLDER_PATH = '/home/ubuntu/vault'

def get_images_filepaths_by_preparation():
    images_folder = f'{VAULT_FOLDER_PATH}/images/2x3/teas'
    img_folders = os.listdir(images_folder)
    img_filepaths_filtered = []
    for folder in img_folders:
        img_filepaths = os.listdir(f'{images_folder}/{folder}')
        for img_filepath in img_filepaths:
            img_filepaths_filtered.append(f'{images_folder}/{folder}/{img_filepath}')
    return img_filepaths_filtered

def template_plain(images_filepaths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.open(images_filepaths[0])
    img = util.img_resize(img, pin_w, pin_h)
    img.save(export_file_name)
    img.show()
    return export_file_name

images_filepaths = get_images_filepaths_by_preparation()
export_filepath = 'test.jpg'
pin_filepath = template_plain(images_filepaths, export_file_name)
print(pin_filepath)

'''
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
    text_pos_x = 200
    num = str(num)
    img_w, img_h = 1000, 1500
    
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, img_h//2 - 160), (img_w, img_h//2 + 160)), fill='#ffffff')
'''
