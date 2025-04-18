from google_play_scraper import search
import pandas as pd
import json

apps = search("note taking AI", lang="en", country="us", n_hits=20)

data = []
for app in apps:
    data.append({
        "Title": app["title"],
        "Star_rating": app.get("score", "N/A"),
        "Link": f"https://play.google.com/store/apps/details?id={app['appId']}"
    })

df = pd.DataFrame(data)
df.to_csv("google_play_apps.csv", index=False)

with open("google_play_apps.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Data stored in `google_play_apps.csv` & `google_play_apps.json`")

