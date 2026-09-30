import json
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://www.boatrace.jp/owpc/pc/data/racersearch/result"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

items = {}

for lo in range(2000, 5600, 100):
    hi = lo + 99

    try:
        r = session.get(
            BASE,
            params={
                "prevpgid": "TDAT320",
                "toban_left": f"{lo:04d}",
                "toban_right": f"{hi:04d}",
            },
            timeout=30,
        )

        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

    except Exception as e:
        print("ERROR", lo, hi, e)
        continue

    # レーサー検索結果のテーブルを探す
    for row in soup.select("table tbody tr"):

        cells = row.find_all("td")

        if not cells:
            continue

        row_text = " ".join(row.stripped_strings)

        # 4桁の登録番号を探す
        match = re.search(r"(?<!\d)(\d{4})(?!\d)", row_text)

        if not match:
            continue

        racer_id = match.group(1)

        # 行の中にあるプロフィールへのリンク
        profile_link = None

        for a in row.find_all("a", href=True):
            href = a["href"]

            if "racersearch" in href or "profile" in href:
                profile_link = href
                break

        if not profile_link:
            continue

        # 名前
        name = ""

        for a in row.find_all("a"):
            text = " ".join(a.stripped_strings)

            if text and not re.fullmatch(r"\d{4}", text):
                name = text
                break

        # 写真
        photo = ""

        img = row.find("img")

        if img:
            src = img.get("src") or img.get("data-src")

            if src:
                photo = urljoin(r.url, src)

        items[racer_id] = {
            "id": racer_id,
            "name": name,
            "photo": photo,
            "profile": urljoin(r.url, profile_link),
        }

    print(lo, hi, "racers:", len(items))

    time.sleep(0.3)

print("TOTAL RACERS:", len(items))

with open("racers.js", "w", encoding="utf-8") as f:
    f.write(
        "window.RACERS="
        + json.dumps(
            list(items.values()),
            ensure_ascii=False,
            separators=(",", ":")
        )
        + ";\n"
    )
