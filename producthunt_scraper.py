from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd
import json

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
driver = webdriver.Chrome()
web_page = 'https://www.producthunt.com/search?q=note%20taking%20ai'
driver.get(web_page)

time.sleep(5)

data=[]
products = driver.find_elements(By.XPATH, "//*[@class='col-start-2 flex flex-col items-start']") 
for product in products :
    title = product.find_element(By.XPATH, ".//div[contains(@class, 'text-16') and contains(@class, 'font-semibold') and contains(@class, 'text-dark-gray')]").text
    description = product.find_element(By.XPATH, ".//div[contains(@class, 'text-14') and contains(@class, 'font-normal') and contains(@class, 'text-light-gray')]").text
    reviews_elem = product.find_elements(By.XPATH, ".//div[contains(@class, 'text-14') and contains(@class, 'font-semibold') and contains(@class, 'text-brand-500')]")
    reviews = reviews_elem[0].text if reviews_elem else "No Reviews"    
    data.append({"Title": title, "Decription": description, "Reviews": reviews })

df = pd.DataFrame(data)
df.to_csv("producthunt_apps.csv", index=False)

with open("producthunt_apps.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

driver.quit()
