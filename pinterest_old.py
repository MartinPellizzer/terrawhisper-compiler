

# def pin_generate(entity, common_name, filename):
#     img = Image.open(f'{img_folder}/{filename}')

#     img_w = 600
#     img_h = 900
#     img = img.resize((600, 900), Image.Resampling.LANCZOS)

#     draw = ImageDraw.Draw(img)
#     rect_h = 200
#     draw.rectangle(((0, img_h//2 - rect_h//2), (img_w, img_h//2 + rect_h//2)), fill ="#0f766e") 
#     draw.rectangle(((0, 350), (600, 550)), fill ="#0c0a09") 
#     draw.rectangle(((0, 350), (600, 550)), fill ="#1c1917") 

#     offset_center_y = 0
#     font_size = 72
#     line_spacing = 1.3
#     font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
#     line = common_name.upper()
#     line_w = font.getbbox(line)[2]
#     line_h = font.getbbox(line)[3]
#     draw.text((img_w//2 - line_w//2, img_h//2 - line_h - 20 + offset_center_y), line, '#ffffff', font=font)
    
#     draw.rectangle(((0 + 50, img_h//2 - 1 + offset_center_y), (img_w - 50, img_h//2 + 1 + offset_center_y)), fill ="#ffffff") 

#     font_size = 24
#     font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
#     line = 'A Medicinal, Botanical, and Horticultural Guide'
#     line_w = font.getbbox(line)[2]
#     line_h = font.getbbox(line)[3]
#     draw.text((img_w//2 - line_w//2, img_h//2 + 20 + offset_center_y), line, '#ffffff', font=font)
#     # line = ''
#     # line_w = font.getbbox(line)[2]
#     # line_h = font.getbbox(line)[3]
#     # draw.text((img_w//2 - line_w//2, img_h//2 - line_h//2 + 56), line, '#ffffff', font=font)
    
#     font_size = 14
#     font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
#     line = '© TerraWhisper.com'
#     line_w = font.getbbox(line)[2]
#     line_h = font.getbbox(line)[3]
#     # draw.rectangle(((0, img_h - 50), (600, img_h)), fill ="#1c1917") 

#     draw.text((img_w//2 - line_w//2, img_h//2 + 60 + offset_center_y), line, '#ffffff', font=font)

#     # img.show()

#     common_name = common_name.lower().replace(' ', '-')
#     img.save(f'pinterest/tmp/{common_name}-guide.jpg', format='JPEG', subsampling=0, quality=100)




def pin_generate_root(entity, common_name, filename, attribute, subtitle):
    img = Image.open(f'{img_folder}/{filename}')

    img_w = 600
    img_h = 900
    img = img.resize((600, 900), Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(img)
    rect_h = 200
    draw.rectangle(((0, img_h//2 - rect_h//2), (img_w, img_h//2 + rect_h//2)), fill ="#0f766e") 
    draw.rectangle(((0, 350), (600, 550)), fill ="#0c0a09") 
    draw.rectangle(((0, 350), (600, 550)), fill ="#1c1917") 

    offset_center_y = -30

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = subtitle
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h//2 - line_h + offset_center_y), line, '#ffffff', font=font)


    font_size = 72
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.upper()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h//2 + offset_center_y), line, '#ffffff', font=font)
    
    # draw.rectangle(((0 + 50, img_h//2 - 1 + offset_center_y), (img_w - 50, img_h//2 + 1 + offset_center_y)), fill ="#ffffff") 
    
    font_size = 14
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = '© TerraWhisper.com'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    # draw.rectangle(((0, img_h - 50), (600, img_h)), fill ="#1c1917") 

    draw.text((img_w//2 - line_w//2, img_h//2 + 80 + offset_center_y), line, '#ffffff', font=font)

    # img.show()

    common_name = common_name.lower().replace(' ', '-')
    img.save(f'pinterest/tmp/{common_name}-{attribute}.jpg', format='JPEG', subsampling=0, quality=100)


quit()

# img_folder = f'G:\\tw-images\\pin\\{entity}'
# img_filenames = os.listdir(img_folder)
# pin_generate(entity, common_name, img_filenames[1])






# WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
#     (By.XPATH, "//div[@class='DraftEditor-editorContainer']/div[@class='notranslate public-DraftEditor-content' and starts-with(@aria-describedby, 'placeholder')]")
#     )).send_keys("Abdul Moiz")

# e.clear()
# e.send_keys('test') 
# e.hover() 
# e.click() 

# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)

# driver.close()




def pin_generate(entity, common_name, filename, attribute, subtitle):
    img = Image.open(f'{img_folder}/{filename}')

    img_w = 600
    img_h = 900
    img = img.resize((600, 900), Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(img)
    rect_h = 200
    draw.rectangle(((0, img_h//2 - rect_h//2), (img_w, img_h//2 + rect_h//2)), fill ="#0f766e") 
    draw.rectangle(((0, 350), (600, 550)), fill ="#0c0a09") 
    draw.rectangle(((0, 350), (600, 550)), fill ="#1c1917") 
    

    offset_center_y = 0
    line = common_name.upper()
    num_characters = len(line)
    if num_characters <= 10: font_size = 72
    else: font_size = 750 // num_characters 
    # print(num_characters, font_size)
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h//2 - line_h - 20 + offset_center_y), line, '#ffffff', font=font)
    
    draw.rectangle(((0 + 50, img_h//2 - 1 + offset_center_y), (img_w - 50, img_h//2 + 1 + offset_center_y)), fill ="#ffffff") 

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = subtitle
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, img_h//2 + 20 + offset_center_y), line, '#ffffff', font=font)
    # line = ''
    # line_w = font.getbbox(line)[2]
    # line_h = font.getbbox(line)[3]
    # draw.text((img_w//2 - line_w//2, img_h//2 - line_h//2 + 56), line, '#ffffff', font=font)
    
    font_size = 14
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = '© TerraWhisper.com'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    # draw.rectangle(((0, img_h - 50), (600, img_h)), fill ="#1c1917") 

    draw.text((img_w//2 - line_w//2, img_h//2 + 60 + offset_center_y), line, '#ffffff', font=font)

    # img.show()

    common_name = common_name.lower().replace(' ', '-')
    img.save(f'pinterest/tmp/{common_name}-{attribute}.jpg', format='JPEG', subsampling=0, quality=100)
