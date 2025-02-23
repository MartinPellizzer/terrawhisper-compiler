import os
import time
import random
import csv
from datetime import datetime
import re
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

import g
import data_csv
import util
import util_data

from oliark_io import json_write, json_read

vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'

# options = Options()
# options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# driver = webdriver.Firefox(executable_path=r'C:\drivers\geckodriver.exe', options=options)

driver = webdriver.Firefox()
driver.get('https://www.google.com')
driver.maximize_window()



product_slug = 'zingiber-officinale'
product_category = 'teas'
# product_query = 'herbalist stirring device' >> at the moment search manually

# search results
elements = driver.find_elements(By.XPATH, '//*[@role="listitem"]')
rows = []
asins_done = []
for element in elements:
    link = element.find_element(By.XPATH, './/a').get_attribute('href')
    link_no_ref = link.split('/ref=')[0]
    if 'sspa' in link_no_ref: continue
    if '/dp/' not in link_no_ref: continue
    asin = link_no_ref.split('/')[-1]
    print(asin)
    if asin in asins_done: continue
    else: asins_done.append(asin)
    print(link_no_ref)
    row = [link_no_ref]
    rows.append(row)

with open(f'{vault}/amazon/{product_category}/csvs/{product_slug}-links.csv', 'w') as f:
    writer = csv.writer(f, delimiter='\\')
    writer.writerows(rows)

##############################################################################
# PRODUCTS PAGES
##############################################################################

assets_folderpath = f'{vault}/amazon/{product_category}/json/{product_slug}'

rows = []
with open(f'{vault}/amazon/{product_category}/csvs/{product_slug}-links.csv', newline='') as f:
    reader = csv.reader(f, delimiter='\\')
    for row in reader:
        rows.append(row)

urls = [row[0] for row in rows]
    
for i, url in enumerate(urls):
    print(url)
    
    asin = url.split('/')[-1]
    print(f'{i}/{len(urls)} - {asin}')
    
    # if asin in os.listdir(f'equipments/jsons/{product_slug}'): continue
    
    json_filepath = f'{assets_folderpath}/{asin}.json'
    
    data = json_read(json_filepath, create=True)
    
    if (
        'url' in data and 
        'title' in data and 
        'description' in data and 
        'price' in data and 
        'reviews_num' in data and 
        'reviews_score' in data and 
        'reviews_5s' in data and 
        'reviews_1s' in data
    ):
        continue
    
    driver.get(url)
    time.sleep(10)
    
        
    #########################################################
    # url
    #########################################################
    data['url'] = url 
    json_write(json_filepath, data)
    
    #########################################################
    # affiliate link
    #########################################################
    affiliate_elements = driver.find_element(By.XPATH, '//button[contains(text(), "Get Link")]')
    affiliate_elements.click()
    time.sleep(10)
    affiliate_link = driver.find_element(By.XPATH, '//textarea[@id="amzn-ss-text-shortlink-textarea"]').text
    print(affiliate_link)
    data['affiliate_link'] = affiliate_link 
    json_write(json_filepath, data)
        
    #########################################################
    # title
    #########################################################
    title = driver.find_element(By.XPATH, '//h1/span').text
    print(title)
    data['title'] = title 
    json_write(json_filepath, data)

    #########################################################
    # description
    #########################################################
    description = driver.find_element(By.XPATH, '//div[@id="feature-bullets"]').text
    print(description)
    data['description'] = description 
    json_write(json_filepath, data)

    #########################################################
    # price
    #########################################################
    price = driver.find_element(By.XPATH, '//span[@class="a-price-whole"]').text
    print(price)
    data['price'] = price 
    json_write(json_filepath, data)
    
    #########################################################
    # reviews num
    #########################################################
    reviews_num = '0'
    try:
        reviews_num = driver.find_element(By.XPATH, '//span[@id="acrCustomerReviewText"]').text
        reviews_num = reviews_num.replace('ratings', '').replace(',', '').strip()
        print(reviews_num)
        data['reviews_num'] = reviews_num 
        json_write(json_filepath, data)
    except:
        data['reviews_num'] = '0' 
        json_write(json_filepath, data)

    #########################################################
    # reviews score
    #########################################################
    reviews_score = '0'
    try:
        reviews_score = driver.find_element(By.XPATH, '//span[@data-action="acrStarsLink-click-metrics"]').text
        print(reviews_score)
        data['reviews_score'] = reviews_score 
        json_write(json_filepath, data)
    except:
        data['reviews_score'] = '0' 
        json_write(json_filepath, data)

    #########################################################
    # reviews score total
    #########################################################
    try:
        reviews_score_total = str(float(reviews_score) * int(reviews_num))
        print(reviews_score_total)
        data['reviews_score_total'] = reviews_score_total 
        json_write(json_filepath, data)
    except:
        data['reviews_score_total'] = '0' 
        json_write(json_filepath, data)
    
    #########################################################
    # reviews
    #########################################################
    customer_reviews_container = driver.find_element(By.XPATH, '//h2[contains(text(), "Customer reviews")]/../..')
    try:
        stars_5 = customer_reviews_container.find_element(By.XPATH, './/a[contains(@aria-label, "5 stars")]')
        stars_5.click()
        time.sleep(10)
        reviews = driver.find_elements(By.XPATH, '//span[@data-hook="review-body"]')
        export_text = ''
        for review in reviews: 
            content = review.text
            print(content)
            export_text += content
        data['reviews_5s'] = export_text
        json_write(json_filepath, data)
    except:
        data['reviews_5s'] = ''
        json_write(json_filepath, data)

    customer_reviews_container = driver.find_element(By.XPATH, '//h2[contains(text(), "Customer reviews")]/../..')
    try:
        stars_1 = customer_reviews_container.find_element(By.XPATH, './/a[contains(@aria-label, "1 stars")]')
        stars_1.click()
        time.sleep(10)
        reviews = driver.find_elements(By.XPATH, '//span[@data-hook="review-body"]')
        export_text = ''
        for review in reviews: 
            content = review.text
            print(content)
            export_text += content
        data['reviews_1s'] = export_text
        json_write(json_filepath, data)
    except:
        data['reviews_1s'] = ''
        json_write(json_filepath, data)
        

        
        
        
        
        
        

driver.get('https://webservices.amazon.com/paapi5/scratchpad/index.html')
time.sleep(30)        

e = driver.find_element(By.XPATH, './/a[@id="GetItems_link"]')
e.click()
time.sleep(10)
e = driver.find_element(By.XPATH, './/input[@id="PartnerTag"]')
e.send_keys('martinpelli06-20')
time.sleep(10)
e = driver.find_element(By.XPATH, './/input[@id="AccessKeyID"]')
e.send_keys('AKIAI4X5DDPLH2UNO2OA')
time.sleep(10)
e = driver.find_element(By.XPATH, './/input[@id="SecretAccessKey"]')
e.send_keys('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')
time.sleep(10)
e = driver.find_element(By.XPATH, './/select[@id="Resources"]/following-sibling::div')
e.click()
time.sleep(10)
e = driver.find_element(By.XPATH, './/input[@value="Images.Primary.Large"]')
e.click()
time.sleep(10)
e = driver.find_element(By.XPATH, ".//b[contains(text(), ' ItemInfo')]")
e.click()
time.sleep(10)

try: os.makedirs(f'{vault}/amazon/{product_category}/images/{product_slug}')
except: pass
asins = [filename.split('.')[0] for filename in os.listdir(f'{vault}/amazon/{product_category}/json/{product_slug}')]
for asin_i, asin in enumerate(asins):
    print(f'{asin_i}/{len(asins)} - {asin}')
    e = driver.find_element(By.XPATH, './/input[@id="ItemIds"]')
    e.clear()
    time.sleep(1)
    e.send_keys(asin)
    time.sleep(3)

    e = driver.find_element(By.XPATH, ".//button[@id='RequestButton']")
    e.click()
    time.sleep(30)
    e = driver.find_element(By.XPATH, ".//a[@href='#HTMLResponseSection']")
    e.click()
    time.sleep(3)
    code = driver.find_element(By.XPATH, ".//code[@id='HTMLResponseCode']").text
    time.sleep(3)

    adding = False
    html_image = ''
    for line in code.split('\n'):
        line = line.strip()
        if line == '': continue
        if line.startswith('<!-- HTML code for ASIN'):
            adding = True
            continue
        if line.startswith('</body>'):
            adding = False
            break
        if adding:
            html_image += line
    print(html_image)
    with open(f'{vault}/amazon/{product_category}/images/{product_slug}/{asin}.txt', 'w') as f: f.write(html_image)
    time.sleep(30)
















if 0:
    for i, url in enumerate(urls):
        print(url)
        
        data = url.split('\\')
        page_link = data[0]
        
        asin = page_link.split('/')[-1] # amazon asin
        
        json_filepath = f'equipments/jsons/{product_slug}.json'
        
        found = False
        for filename in os.listdir(assets_folderpath):
            if asin in filename:
                found = True
                break
        if found: 
            print('found')
            continue
        else: 
            print('not found')
            print('scraping...')
        
        driver.get(url)
        time.sleep(10)
        
        #########################################################
        # title
        #########################################################
        title = driver.find_element(By.XPATH, '//h1/span').text
        print(title)
        output_filepath = f'{assets_folderpath}/{asin}-title.txt'
        with open(output_filepath, 'w') as f: f.write(title)

        #########################################################
        # description
        #########################################################
        description = driver.find_element(By.XPATH, '//div[@id="feature-bullets"]').text
        print(description)
        output_filepath = f'{assets_folderpath}/{asin}-description.txt'
        with open(output_filepath, 'w') as f: f.write(description)

        #########################################################
        # reviews
        #########################################################
        customer_reviews_container = driver.find_element(By.XPATH, '//h2[contains(text(), "Customer reviews")]/../..')
        stars_5 = customer_reviews_container.find_element(By.XPATH, './/a[contains(@aria-label, "5 stars")]')
        stars_5.click()
        time.sleep(10)
        reviews = driver.find_elements(By.XPATH, '//span[@data-hook="review-body"]')
        export_text = ''
        try:
            for review in reviews: 
                content = review.text
                print(content)
                export_text += content
            with open(f'{assets_folderpath}/{asin}-reviews-5star.txt', 'w') as f: f.write(export_text)
        except:
            with open(f'{assets_folderpath}/{asin}-reviews-5star.txt', 'w') as f: f.write('')

        customer_reviews_container = driver.find_element(By.XPATH, '//h2[contains(text(), "Customer reviews")]/../..')
        try:
            stars_1 = customer_reviews_container.find_element(By.XPATH, './/a[contains(@aria-label, "1 stars")]')
            stars_1.click()
            time.sleep(10)
            reviews = driver.find_elements(By.XPATH, '//span[@data-hook="review-body"]')
            export_text = ''
            for review in reviews: 
                content = review.text
                print(content)
                export_text += content
            with open(f'{assets_folderpath}/{asin}-reviews-1star.txt', 'w') as f: f.write(export_text)
        except:
            with open(f'{assets_folderpath}/{asin}-reviews-1star.txt', 'w') as f: f.write('')


#####################################################
# JSON
#####################################################

data = json_read(json_filepath, create=True)
data['product_type'] = 'jars'
json_write(json_filepath, data)

# ;json products
for i, url in enumerate(urls):
    print(url)
    _id = url.split('/')[-1] # amazon asin
    _title_short = url.split('/')[-3] # amazon title short
    
    # init products list
    key = 'products'
    if key not in data: data[key] = []
    found = False
    for obj in data[key]:
        if obj['product_id'] == _id:
            found = True
            break
    if not found:
        product = {'product_id': _id}
        data[key].append(product)
    json_write(json_filepath, data)
    
    # update products data
    key = 'products'
    if key not in data: data[key] = []
    for obj in data[key]:
        if obj['product_id'] == _id:
            obj['product_title_short'] = _title_short
            json_write(json_filepath, data)
            break
    

for element in elements:
    title = element.find_element(By.XPATH, './/h2').text
    reviews = element.find_element(By.XPATH, './/a[contains(@aria-label, "ratings")]').text
    link = element.find_element(By.XPATH, './/a').get_attribute('href')
    print(title)
    print(reviews)
    print(link)
    print()
    break
