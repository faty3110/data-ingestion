from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import json

# Configurer Selenium avec User-Agent pour éviter la détection
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.headless = False  # Pour voir ce qui se passe

driver = webdriver.Chrome(options=options)
driver.get("https://www.producthunt.com/search?q=note%20taking%20ai")

# Attendre que la page charge les résultats
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "styles_item__2Fz9K"))
    )
    print("Résultats trouvés, extraction des données...")
except:
    print("Aucune donnée trouvée, Product Hunt bloque peut-être le scraper.")

# Scroller pour charger plus de résultats
for _ in range(5):
    time.sleep(3)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

# Récupération des produits
data = []
products = driver.find_elements(By.CLASS_NAME, "styles_item__2Fz9K")

for product in products:
    try:
        name = product.find_element(By.CLASS_NAME, "styles_title__3U-ht").text.strip()
        tagline = product.find_element(By.CLASS_NAME, "styles_tagline__3EvR6").text.strip()
        link = product.find_element(By.TAG_NAME, "a").get_attribute("href")

        data.append({"Name": name, "Tagline": tagline, "Link": link})
    except Exception as e:
        print(f"⚠️ Erreur lors de l'extraction : {e}")
        continue

# Sauvegarde des résultats
df = pd.DataFrame(data)
df.to_csv("producthunt_apps.csv", index=False)

with open("producthunt_apps.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print(f"Scraping terminé avec {len(data)} résultats !")
driver.quit()



