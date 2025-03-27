import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time  

data = []  # Store all 55 pages

for page in range(1, 56):  # loop for extracting data on each page 
    print(f"Scraping page {page}...")

    url = f"https://github.com/search?q=note+taking+ai&type=repositories&p={page}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # sending HTTML request
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error {response.status_code}: GitHub blocked access")
        break  

    soup = BeautifulSoup(response.text, "html.parser")
    repos = soup.find_all("div", class_="Box-sc-g0xbh4-0 flszRz")

    if not repos:
        print("No repositories found")
        break  

    for repo in repos:
        title_tag = repo.find("a", class_="prc-Link-Link-85e08")
        title = title_tag.text.strip() if title_tag else "No title"
        link = "https://github.com" + title_tag["href"] if title_tag and title_tag.has_attr("href") else "No link"

        description_tag = repo.find("span", class_="Box-sc-g0xbh4-0 gKFdvh search-match prc-Text-Text-0ima0")
        description = description_tag.get_text(" ", strip=True) if description_tag else "No description"

        stars_tag = repo.find("a", class_="Box-sc-g0xbh4-0 jJYFGF prc-Link-Link-85e08")
        stars = stars_tag.text.strip().split()[0] if stars_tag else "0"

        data.append({"Title": title, "Link": link, "Description": description, "Stars": stars})

    time.sleep(2)  # Delay to avoid being blocked

# Saving CSV & JSON after scraping all pages
df = pd.DataFrame(data)
df.to_csv("github_repos.csv", index=False)

with open("github_repos.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("\nScraping completed. Here’s the data:")
print(df.head())


