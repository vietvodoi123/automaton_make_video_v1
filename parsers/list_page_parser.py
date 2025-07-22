from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def parse_chapter_list_from_list_page(url_list_page: str, base_url: str = None) -> list[dict]:
    """
    Truy cập url_list_page, tìm ul.section-list.fix, lấy các chương (a[href])
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    resp = requests.get(url_list_page, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    ul = soup.find_all("ul", class_="section-list fix")
    if not ul:
        raise Exception("Không tìm thấy ul.section-list.fix")

    chapter_links = ul[1].find_all("a", href=True)
    chapters = []
    for a in chapter_links:
        title = a.get_text(strip=True)
        href = a["href"]
        full_url = urljoin(base_url or url_list_page, href)
        chapters.append({
            "title": title,
            "url": full_url
        })
    return chapters
