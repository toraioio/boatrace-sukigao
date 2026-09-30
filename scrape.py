import requests
from bs4 import BeautifulSoup
import json
import time

URL = "https://www.boatrace.jp/owpc/pc/data/racersearch/result"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36"
}

racers = []

session = requests.Session()
session.headers.update(headers)

for start in range(2000, 5600, 100):
    end = start + 99

    params = {
        "prevpgid": "TDAT320",
        "toban_left": str(start),
        "toban_right": str(end),
    }

    try:
        r = session.get(URL, params=params, timeout=30)
        print("STATUS", start, end, r.status_code)

        soup = BeautifulSoup(r.text, "html.parser")

        for row in soup.select("table tbody tr"):
            cells = row.find_all("td")

            if len(cells) < 3:
                continue

            text = [c.get_text(" ", strip=True) for c in cells]

            number = ""
            name = ""

            for value in text:
                if value.isdigit() and len(value) == 4:
                    number = value

            for value in text:
                if value and not value.isdigit() and len(value) >= 2:
                    name = value
                    break

            if number and name:
                racers.append({
                    "number": number,
                    "name": name
                })

        print(start, end, "racers:", len(racers))

        time.sleep(1)

    except Exception as e:
        print("ERROR:", e)

print("TOTAL RACERS:", len(racers))

with open("racers.js", "w", encoding="utf-8") as f:
    f.write("const racers = ")
    json.dump(racers, f, ensure_ascii=False, indent=2)
    f.write(";")

print("racers.js generated!")
