import json
import os

import requests
from bs4 import BeautifulSoup


def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, "html.parser")


url = "https://cdimage.debian.org/mirror/cdimage/archive/"
soup = get_soup(url)

data = {}

# GEt all tr with class "odd" or "even"
rows = soup.find_all("tr", class_=["odd", "even"])[1:]
for row in rows:
    version = row.find_all("td", class_="indexcolname")[
        0].text.strip().replace("/", "")
    archs = {}
    iso_dir = ""
    if "live" not in version:
        continue
    print("Folder: root")
    last_modified = row.find_all("td", class_="indexcollastmod")[
        0].text.strip()

    soup_in = get_soup(url + version + "/")
    rows_in = soup_in.find_all("tr", class_=["odd", "even"])[1:]
    os.system("clear")
    print(f"Folder: root/{version}/")

    for row2 in rows_in:
        arch_name = row2.find_all("td", class_="indexcolname")[
            0].text.strip().replace("/", "")
        os.system("clear")

        if arch_name in ("amd64", "i386", "arm64", "armhf", "arm"):
            archs[arch_name] = {}

        soup_in2 = get_soup(url + version + "/" + arch_name + "/")
        rows_in2 = soup_in2.find_all("tr", class_=["odd", "even"])[1:]
        print(f"Folder: root/{version}/{arch_name}/")

        for row3 in rows_in2:
            list_name = row3.find_all("td", class_="indexcolname")[
                0].text.strip().replace("/", "")
            if list_name == "iso-cd":
                iso_dir = "iso-cd"
            elif list_name == "iso-hybrid":
                iso_dir = "iso-hybrid"
            else:
                continue

        print(iso_dir)
        soup_in_3 = get_soup(url + version + "/" +
                             arch_name + "/" + iso_dir + "/")
        rows_in_3 = soup_in_3.find_all("tr", class_=["odd", "even"])[1:]

        for row4 in rows_in_3:
            list_item = row4.find_all("td", class_="indexcolname")[0].text.strip().replace("/", "")
            if list_item.endswith(".iso"):
                date_modified_file = row4.find_all(
                    "td", class_="indexcollastmod")[0].text.strip()
                size = row4.find_all("td")[3].text.strip()
                desktop = list_item.split("-")[4].split(".")[0]
                print(list_item)
                archs[arch_name][desktop] = {
                    "file": list_item,
                    "url": url + version + "/" + arch_name + "/" + iso_dir + "/" + list_item,
                    "last_modified": date_modified_file,
                    "size": size

                }

    t_data = {
        version: {
            "last_modified": last_modified,
            "archs": archs
        }
    }

    data.update(t_data)

    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


print(data)

# dump data to json file "data.json"
