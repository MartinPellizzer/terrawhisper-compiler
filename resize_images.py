import os
from PIL import Image
import shutil
import sys

if len(sys.argv) != 2:
    print("ERR: missing folder")
    quit()

folder_type = sys.argv[1]

if folder_type == 'all':
    for image_path in os.listdir('G:\\tw-images\\article-images-tmp'):
        print(image_path)
        
        w, h = 1024, 1024
        # w, h = 768, 768

        img = Image.open('G:\\tw-images\\article-images-tmp\\' + image_path)

        start_size = img.size
        if start_size[0] > w or start_size[1] > h:
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

        output_path = f'articles-images/{image_path}'
        img.save(f'{output_path}')

    for image_path in os.listdir('G:\\tw-images\\article-images-not-to-resize'):
        print(image_path)
        
        website_img_path = 'articles-images'
        shutil.copy2('G:\\tw-images\\article-images-not-to-resize\\' + image_path, f'{website_img_path}/{image_path}')

elif folder_type == 'raw':
    for image_path in os.listdir('G:\\tw-images\\article-images-tmp'):
        print(image_path)
        
        w, h = 1024, 1024
        # w, h = 768, 768

        img = Image.open('G:\\tw-images\\article-images-tmp\\' + image_path)

        start_size = img.size
        if start_size[0] > w or start_size[1] > h:
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

        output_path = f'articles-images/{image_path}'
        img.save(f'{output_path}')
        
elif folder_type == 'resized':
    for image_path in os.listdir('G:\\tw-images\\article-images-not-to-resize'):
        print(image_path)
        
        website_img_path = 'articles-images'
        shutil.copy2('G:\\tw-images\\article-images-not-to-resize\\' + image_path, f'{website_img_path}/{image_path}')
