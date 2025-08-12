# parsers/single_page_parser.py
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
from typing import List, Dict

def parse_chapter_list_from_single_page(
    url_list_page: str,
    base_url: str | None = None,
    debug: bool = False
) -> List[Dict]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url_list_page, headers=headers, timeout=15)
    resp.raise_for_status()

    try:
        resp.encoding = resp.apparent_encoding or resp.encoding
    except Exception:
        pass

    html = resp.text
    if debug:
        with open("debug_single_page.html", "w", encoding="utf-8") as f:
            f.write(html)

    soup = BeautifulSoup(html, "html.parser")

    # Tìm khu vực newlist
    newlist = soup.find(id="newlist") or \
              soup.select_one("dl#newlist, div#newlist, ul#newlist")

    if not newlist:
        # fallback tìm block nhiều link nhất
        candidates = soup.select("dl, div, ul")
        best = None
        best_count = 0
        for c in candidates:
            links = c.select("a")
            if len(links) > best_count:
                best_count = len(links)
                best = c
        if best_count >= 5:
            newlist = best

    if not newlist:
        raise Exception("Không tìm thấy phần chứa mục lục (id='newlist') trong trang.")

    # Lấy tất cả <a> trong newlist
    chapter_links = newlist.select("a[rel=chapter], a[title], a")

    if not chapter_links:
        raise Exception("Không tìm thấy link chương trong phần newlist.")

    chapters: List[Dict] = []
    seen = set()
    for a in chapter_links:
        href = (a.get("href") or "").strip()

        # Nếu không có href → thử lấy từ onclick
        if not href:
            onclick = a.get("onclick", "")
            m = re.search(r"read\((\d+),\s*(\d+)\)", onclick)
            if m:
                book_id, chap_id = m.groups()
                href = f"/book/{book_id}/{int(chap_id)+1}.html"

        full_url = urljoin(base_url or url_list_page, href)
        if full_url in seen:
            continue
        seen.add(full_url)

        title = a.get_text(strip=True) or a.get("title", "").strip()
        chapters.append({
            "title": title,
            "url": full_url
        })

    return chapters
