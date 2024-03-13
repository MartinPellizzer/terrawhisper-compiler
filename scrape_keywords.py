from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv
import pyperclip
import util

driver = webdriver.Firefox()


ARTICLE_START = 0
ARTICLE_END = 100
SCRAPE_SECONDS = 300



def get_latin_name(entity):
    entity_words = entity.capitalize().split('-')
    first_word = entity_words[0]
    rest_words = '-'.join(entity_words[1:])
    latin_name = ' '.join([first_word, rest_words])
    return latin_name



rows = util.csv_get_rows(f'database/tables/plants.csv')[1:]
# print(rows)

for i, row in enumerate(rows[ARTICLE_START:ARTICLE_END]):
    entity = row[0].strip()
    common_name = row[1].strip()
    latin_name = get_latin_name(entity)

    driver.get("https://keywordsheeter.com/")
    time.sleep(10) 

    e = driver.find_element(By.XPATH, '//textarea[@id="input"]')
    e.click()
    e.send_keys(Keys.CONTROL, 'a')
    e.send_keys(Keys.BACKSPACE)
    time.sleep(5) 

    e = driver.find_element(By.XPATH, '//textarea[@id="input"]')
    e.send_keys(latin_name)
    time.sleep(5) 

    e = driver.find_element(By.XPATH, '//button[@id="tempSheet"]')
    e.click()
    time.sleep(5) 

    time.sleep(SCRAPE_SECONDS)

    e = driver.find_element(By.XPATH, '//button[@id="startjob"]')
    e.click()
    time.sleep(5) 

    e = driver.find_element(By.XPATH, '//textarea[@id="input"]')
    e.click()
    e.send_keys(Keys.CONTROL, 'a')
    e.send_keys(Keys.CONTROL, 'c')

    s = pyperclip.paste() 
    with open(f'keywords/plants/{entity}.txt', 'w', newline='', encoding='utf-8') as f:
        f.write(s)

    time.sleep(60)