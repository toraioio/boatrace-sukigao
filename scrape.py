import requests
from bs4 import BeautifulSoup
import re
import json

URL = "https://aiboatrace.jp/racers"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers, timeout=30)
r.raise_for_status()
r.encoding = r.apparent_encoding

soup = BeautifulSoup(r.text, "html.parser")
text = soup.get_text(" ", strip=True)

matches = re.findall(
    r"([一-龥ぁ-んァ-ヶ々ー]{2,8})\s*(\d{4})",
    text
)

racers = []
seen = set()

for name, number in matches:
    if number in seen:
        continue

    seen.add(number)

    racers.append({
        "id": number,
        "name": name,
        "grade": "",
        "photo": f"https://www.boatrace.jp/racerphoto/{number}.jpg"
    })

print("TOTAL RACERS:", len(racers))

with open("racers.js", "w", encoding="utf-8") as f:
    f.write("window.RACERS = ")
    json.dump(racers, f, ensure_ascii=False, indent=2)
    f.write(";")

print("racers.js generated!")
