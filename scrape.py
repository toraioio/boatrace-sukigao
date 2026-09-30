import requests
from bs4 import BeautifulSoup

url = "https://www.boatrace.jp/owpc/pc/data/racersearch/result"

params = {
    "prevpgid": "TDAT320",
    "toban_left": "2000",
    "toban_right": "2099",
}

r = requests.get(
    url,
    params=params,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30,
)

print("STATUS:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

print("TITLE:", soup.title.get_text(strip=True) if soup.title else "なし")

text = soup.get_text(" ", strip=True)

print("2538あり:", "2538" in text)
print("高橋 二朗あり:", "高橋" in text)
print("HTML文字数:", len(r.text))
