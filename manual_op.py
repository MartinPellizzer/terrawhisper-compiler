import os
import shutil

IMG_FOLDER = 'H:/tw-images/auto'

for folder in os.listdir(IMG_FOLDER):
    os.mkdir(f'{IMG_FOLDER}/{folder}/4x3')
    try: os.mkdir(f'{IMG_FOLDER}/{folder}/3x4')
    except: pass

    for image in os.listdir(f'{IMG_FOLDER}/{folder}'):
        if not os.path.isfile(f'{IMG_FOLDER}/{folder}/{image}'): continue
        if image[0].isdigit():
            if not os.path.exists(f'{IMG_FOLDER}/{folder}/3x4/{image}'):
                shutil.move(
                    f'{IMG_FOLDER}/{folder}/{image}', 
                    f'{IMG_FOLDER}/{folder}/3x4/{image}', 
                )
                print(f'{IMG_FOLDER}/{folder}/{image}')
        
        if image == 'overview.jpg':
            shutil.move(
                f'{IMG_FOLDER}/{folder}/{image}', 
                f'{IMG_FOLDER}/{folder}/4x3/0000.jpg', 
            )
            print(f'{IMG_FOLDER}/{folder}/{image}')


    last_image = ''
    for image in os.listdir(f'{IMG_FOLDER}/{folder}/3x4'):
        last_image = image
    # print(last_image)

    last_image_num = 0
    try: last_image_num = int(last_image.split('.')[0])
    except: pass
    # print(last_image_num)

    if os.path.exists(f'{IMG_FOLDER}/{folder}/medicine/benefits'):
        for image in os.listdir(f'{IMG_FOLDER}/{folder}/medicine/benefits'):
            if image[0].isdigit():
                curr_image_num = int(image.split('.')[0]) + last_image_num + 1
                if curr_image_num < 10: curr_image_num = f'000{curr_image_num}'
                elif curr_image_num < 100: curr_image_num = f'00{curr_image_num}'
                curr_image_num += '.jpg'
                
                shutil.move(
                    f'{IMG_FOLDER}/{folder}/medicine/benefits/{image}', 
                    f'{IMG_FOLDER}/{folder}/3x4/{curr_image_num}', 
                )
                # print(f'{IMG_FOLDER}/{folder}/medicine/benefits/{image}')
                # print(f'{IMG_FOLDER}/{folder}/3x4/{curr_image_num}')

    
    

    last_image = ''
    for image in os.listdir(f'{IMG_FOLDER}/{folder}/4x3'):
        last_image = image
    # print(last_image)

    last_image_num = 0
    try: last_image_num = int(last_image.split('.')[0])
    except: pass
    # print(last_image_num)

    if os.path.exists(f'{IMG_FOLDER}/{folder}/medicine/benefits'):
        for image in os.listdir(f'{IMG_FOLDER}/{folder}/medicine/benefits'):
            if image == 'overview.jpg':
                curr_image_num = last_image_num + 1
                if curr_image_num < 10: curr_image_num = f'000{curr_image_num}'
                elif curr_image_num < 100: curr_image_num = f'00{curr_image_num}'
                curr_image_num += '.jpg'
                
                shutil.move(
                    f'{IMG_FOLDER}/{folder}/medicine/benefits/{image}', 
                    f'{IMG_FOLDER}/{folder}/4x3/{curr_image_num}', 
                )
                # print(f'{IMG_FOLDER}/{folder}/medicine/benefits/{image}')
                # print(f'{IMG_FOLDER}/{folder}/4x3/{curr_image_num}')

    