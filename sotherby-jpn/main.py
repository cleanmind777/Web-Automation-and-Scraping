from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse, parse_qs, unquote
import json
import math
from selenium.webdriver.common.action_chains import ActionChains

# Initialize the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()
driver.maximize_window()
# Open a webpage
driver.get("https://www.sothebysrealty.com/eng/sales/jpn")
time.sleep(10)
width = driver.execute_script("return window.innerWidth")
height = driver.execute_script("return window.innerHeight")
actions = ActionChains(driver)
actions.move_by_offset(1225 / 1903 * width, 440 / 901 * height).click().perform()
actions.reset_actions()
actions.move_by_offset(1225 / 1903 * width, 592 / 901 * height).click().perform()
actions.reset_actions()
actions.move_by_offset(950 / 1903 * width, 644 / 901 * height).click().perform()
time.sleep(5)
actions.reset_actions()
actions.move_by_offset(956 / 1903 * width, 189 / 901 * height).click().perform()
try:
    map_to_list_button = driver.find_element(By.CSS_SELECTOR, ".icon.icon-list-view-1.u-margin-right-10")
    map_to_list_button.click()
except:
    pass

elements = driver.find_elements(By.CSS_SELECTOR, ".results-card__container.results-card__container--map")
for element in elements:
    actions.reset_actions()
    actions.key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()
    time.sleep(3)
    # Get all tabs
    tabs = driver.window_handles

    # Switch to the newly opened tab (usually the last one)
    driver.switch_to.window(tabs[-1])

    # Now driver controls the new tab
    print(driver.title)

    # To switch back to the first tab
    driver.switch_to.window(tabs[0])
    time.sleep(500)
time.sleep(500)