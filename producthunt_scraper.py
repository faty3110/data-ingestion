from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Configuration du driver
options = Options()
options.headless = True  # Mettre False si tu veux voir le navigateur
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL de recherche ProductHunt
url = "https://www.producthunt.com/search?q=note%20taking%20ai"
driver.get(url)
time.sleep(5)  # Attendre le chargement de la page

# Récupérer les applications
products = driver.find_elements(By.CLASS_NAME, "styles_item__2Fz9K")

data = []
for product in products:
    try:
        name = product.find_element(By.CLASS_NAME, "styles_title__3U-ht").text.strip()
        tagline = product.find_element(By.CLASS_NAME, "styles_tagline__3EvR6").text.strip()
        link = product.find_element(By.TAG_NAME, "a").get_attribute("href")

        data.append({"Name": name, "Tagline": tagline, "Link": link})
    except Exception as e:
        print("Erreur :", e)

# Enregistrement en CSV
df = pd.DataFrame(data)
df.to_csv("producthunt_apps.csv", index=False)
print("✅ Scraping terminé ! Données enregistrées dans `producthunt_apps.csv`")

driver.quit()
