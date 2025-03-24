import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://github.com/search?q=note+taking+ai&type=repositories"
headers = {"User-Agent": "Mozilla/5.0"}

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
    print("❌ Erreur :", response.status_code)
