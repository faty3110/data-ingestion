import requests
from bs4 import BeautifulSoup
import pandas as pd
import time  # <-- Ajout du module time

url = "https://github.com/search?q=note+taking+ai&type=repositories"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# Attendre 2 secondes avant d'envoyer la requête pour éviter l'erreur 429
time.sleep(2)

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    repos = soup.find_all("li", class_="repo-list-item")

    data = []
    for repo in repos:
        title = repo.find("a", class_="v-align-middle").text.strip()
        link = "https://github.com" + repo.find("a", class_="v-align-middle")["href"]
        description = repo.find("p", class_="mb-1")
        description = description.text.strip() if description else "No description"

        data.append({"Title": title, "Link": link, "Description": description})

    df = pd.DataFrame(data)
    df.to_csv("github_repos.csv", index=False)
    print("✅ Scraping terminé ! Données enregistrées.")
else:
    print(f"❌ Erreur {response.status_code} : Impossible d'accéder à GitHub")
