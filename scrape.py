import requests
from bs4 import BeautifulSoup
import re
import json

URL = "https://aiboatrace.jp/racers"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers, timeout=30)

# 日本語の文字コードを正しく判定
r.encoding = r.apparent_encoding

soup = BeautifulSoup(r.text, "html.parser")

# ページ内の文字から「名前＋4桁の登録番号」を取得
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
        "number": number,
        "name": name
    })

print("TOTAL RACERS:", len(racers))

with open("racers.js", "w", encoding="utf-8") as f:
    f.write("const racers = ")
    json.dump(racers, f, ensure_ascii=False, indent=2)
    f.write(";")

print("racers.js generated!")
