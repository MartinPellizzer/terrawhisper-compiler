from PIL import Image, ImageColor, ImageEnhance
import random

def image_variate(i):
    image = Image.open('C:/terrawhisper-assets/images/tea/anise/0000.jpg')

    # image_rotate = image.rotate(60, expand=True, fillcolor=ImageColor.getcolor('red', 'RGB'))
    # image_crop = image.crop((0, 0, 500, 500))
    # image_flip_horizontal = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    # image_flip_vertical = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    # image_transpose = image.transpose(Image.Transpose.TRANSPOSE)
    # image_resize = image.resize((600, 1000))

    random_enhancer_val = random.uniform(0.9, 1.1)
    image_enhancer = ImageEnhance.Color(image)
    image = image_enhancer.enhance(random_enhancer_val)
    random_enhancer_val = random.uniform(0.9, 1.1)
    image_enhancer = ImageEnhance.Contrast(image)
    image = image_enhancer.enhance(random_enhancer_val)
    random_enhancer_val = random.uniform(0.9, 1.1)
    image_enhancer = ImageEnhance.Brightness(image)
    image = image_enhancer.enhance(random_enhancer_val)
    random_enhancer_val = random.uniform(0.9, 1.1)
    image_enhancer = ImageEnhance.Sharpness(image)
    image = image_enhancer.enhance(random_enhancer_val)


    random_val_x1 = random.randint(50, 100)
    random_val_y1 = random.randint(50, 100)
    random_val_x2 = random.randint(50, 100)
    random_val_y2 = random.randint(50, 100)
    image = image.crop((random_val_x1, random_val_y1, 1024-random_val_x2, 1024-random_val_y2))
    image = image.resize((1024, 1024))
    image.save(f'test/{i}.jpg')

for i in range(10):
    image_variate(i)