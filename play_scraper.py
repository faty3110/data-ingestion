from google_play_scraper import search
import pandas as pd

# Rechercher des applications sur Google Play
apps = search("note taking AI", lang="en", country="us", n_hits=20)

data = []
for app in apps:
    data.append({
        "Name": app["title"],
        "Rating": app.get("score", "N/A"),
        "Reviews": app.get("reviews", "N/A"),
        "Link": f"https://play.google.com/store/apps/details?id={app['appId']}"
    })

# Enregistrement en CSV
df = pd.DataFrame(data)
df.to_csv("google_play_apps.csv", index=False)
print("✅ Données enregistrées dans `google_play_apps.csv`")
