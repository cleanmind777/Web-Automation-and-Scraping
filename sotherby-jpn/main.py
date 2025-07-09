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
driver.get("https://www.sothebysrealty.com/eng/sales/jpn/view-map")
time.sleep(30)
width = driver.execute_script("return window.innerWidth")
height = driver.execute_script("return window.innerHeight")
actions = ActionChains(driver)
while True:
    try:
        time.sleep(1)
        actions.reset_actions()
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
        time.sleep(2)
        pagination_element = driver.find_element(By.CSS_SELECTOR, ".pagination-container.pagination")
        driver.execute_script("arguments[0].scrollIntoView();", pagination_element)
        page_count = int(pagination_element.find_elements(By.TAG_NAME, "a")[-2].text)
        break
    except:
        pass
    


# print("page_count:::::::::::::::::::::::::::::::::", page_count)
buildings = []
buildings.append({"heigh":height, "width":width})
count = 0
for i in range(page_count):
    elements = driver.find_elements(By.CSS_SELECTOR, ".results-card__container.results-card__container--map")
    for element in elements:
        count += 1
        print(count)
        building = {}
        while True:
            try:
                driver.execute_script("arguments[0].scrollIntoView();", element)
                break
            except:
                time.sleep(1)
                pass
    
        actions.reset_actions()
        actions.key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()
        time.sleep(3)
        # Get all tabs
        tabs = driver.window_handles

        # Switch to the newly opened tab (usually the last one)
        driver.switch_to.window(tabs[-1])

        # Now driver controls the new tab
        time.sleep(5)
        title = driver.find_element(By.CSS_SELECTOR, ".c-listing-description").find_element(By.CLASS_NAME, "title").text
        # print("title:::::::::::::::::::::::::::::::::",title)
        building["title"] = title
        length_of_img_element = driver.find_element(By.CSS_SELECTOR, ".c-ldp-hero-info__counter").find_elements(By.TAG_NAME, "span")[-1].text
        print(length_of_img_element)
        imgs = []
        next_img_btn = driver.find_elements(By.CSS_SELECTOR, ".c-ldp-hero-info__btn")[-1]
        for i in range(int(length_of_img_element)-1):
            # print(i)
            try:
                img_element = driver.find_element(By.CSS_SELECTOR, ".c-ldp-hero-slide.c-ldp-hero-slide__photos-wrapper.c-ldp-hero-slide--current").find_element(By.TAG_NAME, "img")
                srcset_value = img_element.get_attribute("srcset")
                
                # Split by comma to separate each URL+descriptor
                last_part = srcset_value.split(",")[-1].strip()

                # Split by space to isolate the URL (before the width descriptor)
                last_url = last_part.split(" ")[0]
                imgs.append(last_url)
                next_img_btn.click()
                time.sleep(1)
            except:
                try:
                    img_element = driver.find_element(By.CSS_SELECTOR, ".c-ldp-hero-slide.c-ldp-hero-slide__video-wrapper.c-ldp-hero-slide--current.c-ldp-hero-slide--current-video").find_element(By.TAG_NAME, "img")
                    srcset_value = img_element.get_attribute("srcset")
                    
                    # Split by comma to separate each URL+descriptor
                    last_part = srcset_value.split(",")[-1].strip()

                    # Split by space to isolate the URL (before the width descriptor)
                    last_url = last_part.split(" ")[0]
                    imgs.append(last_url)
                    next_img_btn.click()
                    time.sleep(1)
                except:
                    try:
                        img_element = driver.find_element(By.CSS_SELECTOR, ".c-ldp-hero-slide.c-ldp-hero-slide__floorplans-wrapper.c-ldp-hero-slide--current").find_element(By.TAG_NAME, "img")
                        srcset_value = img_element.get_attribute("srcset")
                        
                        # Split by comma to separate each URL+descriptor
                        last_part = srcset_value.split(",")[0].strip()

                        # Split by space to isolate the URL (before the width descriptor)
                        last_url = last_part.split(" ")[0]
                        imgs.append(last_url)
                        next_img_btn.click()
                        time.sleep(1)
                    except:
                        pass
        property_detail = {}
        property_detail_element = driver.find_element(By.ID, "property-details")
        properties = property_detail_element.find_elements(By.CSS_SELECTOR, ".m-listing-info__item")
        for property in properties:
            key = property.find_element(By.CSS_SELECTOR, ".m-listing-info__item-title").text
            value = property.find_element(By.CSS_SELECTOR, ".m-listing-info__item-content").text
            property_detail[key] = value
        description_detail = {}
        description_element  = driver.find_element(By.CSS_SELECTOR, ".description-holder")
        descriptions = description_element.find_elements(By.TAG_NAME, "p")
        for description in descriptions:
            try:
                description_detail[description.text.split(":")[0].strip()] = description.text.split(":")[-1].strip()
            except:
                pass
            # print(description.text)
        # print(description_detail)
        building["imgs"] = imgs
        building["property_detail"] = property_detail
        building["description_detail"] = description_detail
        buildings.append(building)
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(buildings, f, indent=4)

        driver.close()

        
        # To switch back to the first tab
        driver.switch_to.window(tabs[0])
        time.sleep(3)
    

    
    next_btn_element = driver.find_element(By.CSS_SELECTOR, '.pagination-container.pagination')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn_element)
    next_btn = next_btn_element.find_elements(By.TAG_NAME, "a")[-1]
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
    next_btn.click()
    time.sleep(10)
driver.quit()