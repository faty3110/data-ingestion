from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import json

options = webdriver.ChromeOptions()
options.headless = True  # Ouvre Chrome en arrière-plan
driver = webdriver.Chrome(options=options)

driver.get("https://www.producthunt.com/search?q=note%20taking%20ai")
time.sleep(5)  # Attendre le chargement de la page

data = []
for _ in range(5):  # Scroller 5 fois pour charger plus de résultats
    time.sleep(3)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

    products = driver.find_elements(By.CLASS_NAME, "styles_item__2Fz9K")
    
    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, "styles_title__3U-ht").text.strip()
            tagline = product.find_element(By.CLASS_NAME, "styles_tagline__3EvR6").text.strip()
            link = product.find_element(By.TAG_NAME, "a").get_attribute("href")

            data.append({"Name": name, "Tagline": tagline, "Link": link})
        except:
            continue

df = pd.DataFrame(data)
df.to_csv("producthunt_apps.csv", index=False)

with open("producthunt_apps.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("✅ Scraping terminé pour ProductHunt !")
driver.quit()

