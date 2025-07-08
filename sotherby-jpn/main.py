from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse, parse_qs, unquote
import json
import math

# Initialize the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()
driver.maximize_window()
# Open a webpage
driver.get("https://www.sothebysrealty.com/eng/sales/jpn")
time.sleep(20)

try :
    frame = driver.find_element(By.CSS_SELECTOR, "iframe[title='TrustArc Cookie Consent Manager']")
    driver.switch_to.frame(frame)
    print('11111')
    yesbtn = driver.find_elements(By.CSS_SELECTOR, ".gwt-InlineHTML.off")
    print("!")
    yesbtn[0].click()
    yesbtn[1].click()
    time.sleep(5)
    submitbtn = driver.find_element(By.CSS_SELECTOR, "pdynamicbutton")
    submitbtn.click()
    time.sleep(5)
    closebtn = driver.find_element(By.id, "gwt-debug-close_id")
    closebtn.click()
    time.sleep(5)
except :
    print("no modal")
    pass

time.sleep(5)
try:
    map_to_list_button = driver.find_element(By.CSS_SELECTOR, ".icon.icon-list-view-1.u-margin-right-10")
    map_to_list_button.click()
except:
    pass


time.sleep(500)