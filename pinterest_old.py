

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



quit()



# articles rows
articles_master_rows = csv_to_llst('pinterest/articles.csv')

# articles indexes
articles_dict = {}
for i, item in enumerate(articles_master_rows[0]):
    articles_dict[item] = i

for i, row in enumerate(articles_master_rows[1:]):
    print(f'{i}/{len(articles_master_rows[1:])}')
    
    to_pin = row[articles_dict['to_pin']].strip()
    entity = row[articles_dict['entity']].strip()
    common_name = row[articles_dict['common_name']].strip()
    org = row[articles_dict['org']].strip()
    url = row[articles_dict['url']].strip()
    title = row[articles_dict['title']].strip()
    subtitle = row[articles_dict['subtitle']].strip()
    last_day = row[articles_dict['last_day']].strip()
    current_image = row[articles_dict['current_image']].strip()
    image_name = row[articles_dict['image_name']].strip()
    image_subfolder = row[articles_dict['image_subfolder']].strip()
    description_folder = row[articles_dict['description_folder']].strip()
    # print(image_name)

    if to_pin.strip() != 'x': continue

    today_day = datetime.now().day
    if int(last_day) == int(today_day): 
        print(f'>> skipped {entity} {url}')
        continue

    latin_name = entity.replace('-', ' ').capitalize()
    common_name_title = common_name.title()
    common_name_formatted = common_name.lower().replace(' ', '-')

    img_folder = f'G:\\tw-images\\pin\\{entity}\\{image_subfolder}'
    img_filenames = os.listdir(f'{img_folder}')
    img_filename = img_filenames[int(current_image)]
    pin_generate_2(entity, common_name_title, img_filename, image_name, subtitle)

    folderpath = f'database/articles/{entity}'
    if description_folder.strip() != '': folderpath += '/' + description_folder.replace('-', '/')

    files = [f for f in os.listdir(folderpath) if f.endswith('.md')]
    description = []
    for file in files:
        with open(f'{folderpath}/{file}', encoding="utf-8") as f:
            content = f.read()
        content = content.split('\n')
        for p in content:
            if p.strip() != '':
                description.append(p) 

    description = ''.join(description)
    description = description.split('. ')
    random.shuffle(description)
    description = '. '.join(description[:3])
    words = description.split(' ')
    description = ''
    for word in words:
        if len(description) + len(word) + 1 < 460:
            description += word + ' '
        else:
            break
    description = description.strip() + '... '
    description += 'Click the pin link to learn more.'

    print(entity)
    print(common_name_title)
    print(img_filename)
    print(image_name)
    print(subtitle)
    print(title)
    print(description)
    print(url)
    print()



    driver.get("https://www.pinterest.com/pin-creation-tool/")
    time.sleep(3)

    e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
    e.send_keys(f'C:\\terrawhisper-compiler\\pinterest\\tmp\\{common_name_formatted}-{image_name}.jpg') 
    time.sleep(3)

    e = driver.find_element(By.XPATH, '//input[@id="storyboard-selector-title"]')
    e.send_keys(title)
    time.sleep(3) 

    e = driver.find_element(By.XPATH, "//div[@class='notranslate public-DraftEditor-content']")
    for c in description:
        e.send_keys(c)
    time.sleep(3)

    e = driver.find_element(By.XPATH, '//input[@id="WebsiteField"]')
    e.send_keys(url) 
    time.sleep(3)

    e = driver.find_element(By.XPATH, '//button[@data-test-id="board-dropdown-select-button"]')
    e.click()
    time.sleep(5)

    e = driver.find_element(By.XPATH, '//input[@id="pickerSearchField"]')
    # e.send_keys(common_name_title) 
    e.send_keys('Medicinal Plants') 
    time.sleep(3)

    # e = driver.find_element(By.XPATH, f'//div[@data-test-id="board-row-{common_name_title} ({latin_name})"]')
    e = driver.find_element(By.XPATH, f'//div[@data-test-id="board-row-Medicinal Plants"]')
    e.click()
    time.sleep(3)

    e = driver.find_element(By.XPATH, '//div[@data-test-id="storyboard-creation-nav-done"]/..')
    e.click()

    time.sleep(30)

    driver.get("https://www.google.com/")

    time.sleep(300)

driver.get("https://www.google.com/")
