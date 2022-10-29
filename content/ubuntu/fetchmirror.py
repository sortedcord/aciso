# Go to https://launchpad.net/ubuntu/+cdmirrors and get all text

import requests

from bs4 import BeautifulSoup

url = "https://launchpad.net/ubuntu/+cdmirrors"

r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")

# print(soup.prettify())

# get all <tr> with class "head"
headings = (soup.find_all("tr", class_="head"))
datarows = (soup.find_all("tr", class_=""))

rows = soup.find_all("tr")

print(rows)
data = {"start":0}

current_country = ""
mirrors = []
for row in rows:
    if row.has_attr("class") and "section-break" in row["class"]:
        continue

    elif row.has_attr("class") and "head" in row["class"]:
        if "start" not in data:
            data[current_country] = mirrors
        else:
            del data["start"]

        heads = row.find_all("th")
        country = heads[0].text.strip()
        current_country = country
        mirrors = []

        
    elif not row.has_attr("class"):
        td = row.find_all("td")
        mirror_name = td[0].text.strip()

        try:
            mirror_url = row.find_all("a")[1]["href"]
        except:
            mirror_url = ""

        mirror_speed = td[2].text.strip()

        mirrors.append({
            "name": mirror_name,
            "url": mirror_url,
            "speed": mirror_speed
        })

print(data)

#dump data as json file
import json

with open("mirrors.json", "w") as f:
    json.dump(data, f, indent=4)
    