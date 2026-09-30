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

        print("STATUS", lo, hi, r.status_code)

        soup = BeautifulSoup(r.text, "html.parser")

    except Exception as e:
        print("ERROR", lo, hi, e)
        continue

    # ページ内のリンクを全部確認
    for a in soup.find_all("a", href=True):

        href = a["href"]

        # racersearch/profile のリンクだけ取得
        if "racersearch/profile" not in href:
            continue

        text = " ".join(a.stripped_strings)

        # 4桁の登録番号を探す
        match = re.search(r"\b(\d{4})\b", text)

        if not match:
            continue

        racer_id = match.group(1)

        # 名前
        name = re.sub(
            r"\b\d{4}\b",
            "",
            text
        ).strip()

        # 写真
        photo = ""

        img = a.find("img")

        if img:
            src = img.get("src") or img.get("data-src")

            if src:
                photo = urljoin(r.url, src)

        items[racer_id] = {
            "id": racer_id,
            "name": name,
            "photo": photo,
            "profile": urljoin(r.url, href),
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
