from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import util

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path=r'C:\drivers\geckodriver.exe', options=options)
driver.get("https://plants.usda.gov/home")
time.sleep(10)

rows = util.csv_get_rows('database/tables/plants.csv')
for row in rows[1:]:
    latin_name = row[0]
    latin_name_dash = latin_name.lower().strip().replace(' ', '-')
    rows = util.csv_get_rows_by_entity('database/tables/taxonomy.csv', latin_name_dash)
    if rows != []: continue

    e = driver.find_element(By.XPATH, '//input[contains(@id, "basic-search-input")]')
    e.clear()
    e.send_keys(latin_name) 
    time.sleep(3)
    e = driver.find_element(By.XPATH, '//button[contains(text(), "Go")]')
    e.click() 
    time.sleep(10)

    elements = driver.find_elements(By.XPATH, '//table[@class="table"]/tbody/tr')
    link = ''
    found = False
    for e in elements:
        cell = e.find_element(By.XPATH, './/td')
        text = cell.text
        if latin_name.lower().strip() in text.strip().lower():
            link = cell.find_element(By.XPATH, './/a').get_attribute('href')
            print(text, '>>', link)
            found = True
            break
    if not found: continue
    driver.get(link)
    time.sleep(10)


    kingdom = ''
    phylum = ''
    clss = ''
    order = ''
    family = ''
    genus = ''
    species = ''
    element = driver.find_element(By.XPATH, '//h6[contains(text(),"Kingdom")]/../../..')
    elements = element.find_elements(By.XPATH, './/tr')
    for e in elements:
        category = e.find_element(By.XPATH, './/th').text
        val = e.find_element(By.XPATH, './/td').text
        if category.strip().lower() == 'kingdom': kingdom = val.split(' ')[0].strip()
        if category.strip().lower() == 'division': phylum = val.split(' ')[0].strip()
        if category.strip().lower() == 'class': clss = val.split(' ')[0].strip()
        if category.strip().lower() == 'order': order = val.split(' ')[0].strip()
        if category.strip().lower() == 'family': family = val.split(' ')[0].strip()
        genus = latin_name.split(' ')[0]
        species = latin_name
    print('kingdom:', kingdom)
    print('phylum:', phylum)
    print('clss:', clss)
    print('order:', order)
    print('family:', family)
    print('genus:', genus)
    print('species:', species)

    latin_name_dash = latin_name.lower().strip().replace(' ', '-')
    rows = util.csv_get_rows_by_entity('database/tables/taxonomy.csv', latin_name_dash)
    if rows == []:
        util.csv_add_rows('database/tables/taxonomy.csv', [[
            latin_name_dash, kingdom, phylum, clss, order, family, genus, species,
        ]])

    # break
    time.sleep(10)
