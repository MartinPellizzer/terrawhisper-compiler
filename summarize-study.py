from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import os
import re
import csv
import time
import random
import winsound
from datetime import datetime

from ctransformers import AutoModelForCausalLM

import utils



duration = 1000
freq = 440


def read_file(filepath):
    with open(filepath, 'a', encoding='utf-8') as f: pass
    with open(filepath, 'r', encoding='utf-8') as f: 
        text = f.read()
    return text


def write_file(filepath, text):
    with open(filepath, 'w', encoding='utf-8') as f: 
        f.write(text)

        
remedies = [
"green tea",
"oolong tea",
"black tea",
"cinnamon tea",
"turmeric tea",
"white tea",
"ginger tea",
"hibiscus tea",
"yerba mate tea",
"dandelion tea",
"peppermint tea",
"celery tea",
"chamomile tea",
"fennel tea",
"rosehip tea",
]

problem = 'weight loss'
problem_formatted = problem.replace(' ', '-')
article_url = f'herbalism/tea/{problem_formatted}'



for remedy in remedies:
    print(remedy)
    # remedy = remedies[5]
    remedy_formatted = remedy.replace(' ', '-').lower().strip()
    filepath_out = f'database-new/articles/{article_url}/{remedy_formatted}-study-scraped.md'
    content = read_file(filepath_out)
    if content.strip() != '': continue

    driver = webdriver.Firefox()
    driver.get("https://scholar.google.com/")
    time.sleep(3)

    query = f'{remedy} {problem}'.lower().strip()

    e = driver.find_element(By.XPATH, '//input[@name="q"]')
    e.send_keys(query)
    time.sleep(3)
    e.send_keys(Keys.RETURN)
    time.sleep(3)

    main_element = driver.find_element(By.XPATH, '//div[@role="main"]')
    articles_elements = main_element.find_elements(By.XPATH, './/h3/..')

    articles_urls = []
    for article_element in articles_elements:
        a_elements = article_element.find_elements(By.XPATH, './/a')
        # for a_element in a_elements:
        #     print(a_element.text)

        study_url = article_element.find_element(By.XPATH, './/h3/a').get_attribute('href')
        articles_urls.append(study_url)

    for study_url in articles_urls:
        print(study_url)
        try: driver.get(study_url)
        except: continue
        time.sleep(10)

        abstract_headers = driver.find_elements(By.XPATH, "//*[contains(text(), 'Abstract')]")
        for abstract_header in abstract_headers:
            abstract_text = ''
            print(filepath_out)
            try:
                abstract_element = abstract_header.find_element(By.XPATH, "following-sibling::*[1]")
                try: abstract_text = abstract_element.text
                except: pass
                print(abstract_text)
            except: pass
            
            write_file(filepath_out, abstract_text)
            content = read_file(filepath_out)
            if content.strip() != '': break

        driver.quit()

        time.sleep(10)




winsound.Beep(freq, duration)




# print(e.find_element(By.XPATH, './/h3').text)

# TODO: extract num of cites


url = e.find_element(By.XPATH, './/h3/a').get_attribute('href')
driver.get(url)





# e.send_keys('martinpellizzer@gmail.com') 
e.send_keys('leenrandell@gmail.com') 
time.sleep(3)

e = driver.find_element(By.XPATH, '//input[@id="password"]')
# e.send_keys('Newoliark1') 
e.send_keys('Newoliark1') 
time.sleep(3)

e = driver.find_element(By.XPATH, '//div[text()="Log in"]')
e.click()
time.sleep(3)