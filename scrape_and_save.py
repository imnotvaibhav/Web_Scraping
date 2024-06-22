# Libraries
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

driver = webdriver.Edge()
driver.get("https://www.google.com")

# Search for a query
search_text = r'arcgis/rest/services'

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(search_text)
search_box.send_keys(Keys.RETURN)

# Function to scroll to the bottom of the page
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Function to scrape links 
def scrape_links(driver):
    links = []
    containers = driver.find_elements(By.XPATH,"//*[@class='MjjYud']/div/div/div[1]/div/div/span/a")
    for i in range(len(containers)):
        links.append(containers[i].get_attribute('href'))
    return links

all_links = []

# Scrolling to bottom
for _ in range(7):
    scroll_to_bottom(driver)
    time.sleep(3)


while len(all_links)<100:
    more_results_button = driver.find_element(By.XPATH, "//span[text()='More results']")
    more_results_button.click()
    scroll_to_bottom(driver)
    time.sleep(3)

    new_links = scrape_links(driver)
    all_links.extend(new_links[len(all_links):])

# Closing the driver
driver.quit()

# Saving Links to .csv file
df = pd.DataFrame(data = all_links)

# Save the DataFrame to a CSV file
df.to_csv("Links.csv", index=False)

# Specify the desired path and filename for the CSV file
filepath = "C:/V/coding_placement/web_scraping/selenium/links.csv"  # Replace with your actual path

# Save the DataFrame to the CSV file
df.to_csv(filepath, index=False)