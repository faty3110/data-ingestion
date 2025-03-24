import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

# Liste pour stocker toutes les données
data = []

# Scraper 5 pages de résultats
for page in range(1, 6):  
    url = f"https://github.com/search?p={page}&q=note+taking+ai&type=repositories"

    headers = {"User-Agent": "Mozilla/5.0"}
    time.sleep(2)  # Pause pour éviter l'erreur 429

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Vérifier si la requête a réussi
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur : {e}")
        continue  # Passer à la page suivante en cas d'erreur

    soup = BeautifulSoup(response.text, "html.parser")
    repos = soup.find_all("li", class_="repo-list-item")

    for repo in repos:
        title = repo.find("a", class_="v-align-middle").text.strip()
        link = "https://github.com" + repo.find("a", class_="v-align-middle")["href"]
        description = repo.find("p", class_="mb-1")
        description = description.text.strip() if description else "No description"

        data.append({"Title": title, "Link": link, "Description": description})

# Sauvegarde en CSV
df = pd.DataFrame(data)
df.to_csv("github_repos.csv", index=False)

# Sauvegarde en JSON
with open("github_repos.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("✅ Scraping terminé pour plusieurs pages !")

