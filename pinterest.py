from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("http://www.python.org")

# assert "Python" in driver.title

e = driver.find_element(By.XPATH, '//div[text()="Log in"]')
e.click()

e = driver.find_element(By.XPATH, '//input[@id="email"]')
e.send_keys('martinpellizzer@gmail.com') 

e = driver.find_element(By.XPATH, '//input[@id="password"]')
e.send_keys('Newoliark1') 


driver.get("https://www.pinterest.com/pin-creation-tool/")


e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
e.send_keys(r'G:\tw-images\article-images-not-to-resize\acorus-calamus-history-general-3x4.jpg') 

elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)

# driver.close()