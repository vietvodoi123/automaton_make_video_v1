import requests
from bs4 import BeautifulSoup

proxies = {
    "http": "socks5://EAzGMRSu:ZiNQDnXh@156.246.164.173:64445",
    "https": "socks5://EAzGMRSu:ZiNQDnXh@156.246.164.173:64445",
}

headers = {"User-Agent": "Mozilla/5.0", "Connection": "close"}

urls = [
    "https://www.xm200.com/book/371789/128363226.html",
    "https://www.xm200.com/book/371789/128363227.html"
]

for u in urls:
    try:
        r = requests.get(u, headers=headers, proxies=proxies, timeout=20)
        print(u, r.status_code, len(r.text))
    except Exception as e:
        print("❌", u, e)
