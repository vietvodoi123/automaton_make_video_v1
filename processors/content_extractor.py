
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
from processors import translate_full_text
from utils import refine_translation, summarize_text,retry_with_limit
from utils import translate_and_summarize_chinese_to_vietnamese,summarized_by_gpt
import requests

def extract_chapter_content_bs4(url: str, css_title: str, css_content: str, css_next: str = None) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    visited_urls = set()
    current_url = url
    title = ""
    full_translated = ""
    full_raw = ""
    # full_summarized = ""

    parsed_origin = urlparse(url)
    origin_chapter_id = parsed_origin.path.strip("/").split("/")[-1].split("_")[0].split(".")[0]  # ID chương

    while current_url not in visited_urls:
        visited_urls.add(current_url)
        time.sleep(5)

        response = requests.get(current_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Không thể tải trang: {current_url}")

        soup = BeautifulSoup(response.text, "html.parser")

        if not title:
            title_elem = soup.select_one(css_title)
            if not title_elem:
                raise ValueError(f"Không tìm thấy tiêu đề với selector: {css_title}")
            title = title_elem.text.strip()

        content_elem = soup.select_one(css_content)
        if not content_elem:
            raise ValueError(f"Không tìm thấy nội dung với selector: {css_content}")
        raw_cn_content = content_elem.get_text(separator="\n").strip().replace("请收藏本站：.nibq。笔趣阁手机版：.nibq","").replace("本章未完，点击下一页继续阅读","").replace("请收藏本站：.biq01。笔趣阁手机版：.biq01","")

        # dich truyen
        res = translate_full_text(raw_cn_content)
        # full_summarized += res['summary']
        full_translated += res + "\n"
        full_raw += raw_cn_content + "\n"

        # Xử lý link tiếp theo
        next_btn = soup.select_one(css_next) if css_next else None
        next_href = next_btn.get("href") if next_btn else None
        print("➡️ next_href:", next_href)
        print(f"origin {origin_chapter_id}")
        if next_href:
            next_url = urljoin(current_url, next_href)
            next_path = urlparse(next_url).path.strip("/")
            next_chapter_id = next_path.split("/")[-1].split("_")[0].split(".")[0]
            print(f"next chapter {next_chapter_id}")

            if next_chapter_id != origin_chapter_id:
                print("⛔ Đã sang chương khác, dừng lại.")
                break

            current_url = next_url
        else:
            break

    title_trans=translate_full_text(title).split('_')[0]
    summary = summarized_by_gpt(full_translated)
    return {
        "title": title,
        "title_translated": title_trans,
        "raw_cn_content": title + "\n" + full_raw.strip(),
        "translation": title_trans + "\n" + full_translated.strip(),
        "summarized": summary["summary"]
    }


if __name__ == "__main__":
    a = extract_chapter_content_bs4(
        "https://www.xm200.com/book/371789/128363226.html",
        "title",
        "div#booktxt",
        'a[rel="next"]'
    )
    print(a)