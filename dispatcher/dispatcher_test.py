from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

from parsers.list_page_parser import parse_chapter_list_from_list_page
from parsers.single_page_parser import parse_chapter_list_from_single_page
from sheets.story_sheet import StorySheet
from sheets.task_sheet import TaskSheet


def dispatch_tasks(spreadsheet_id: str):
    # Khởi tạo sheet
    story_sheet = StorySheet(spreadsheet_id)
    task_sheet = TaskSheet(spreadsheet_id)

    # Lấy các truyện có trạng thái NEW
    new_stories = story_sheet.get_new_stories()

    for story in new_stories:
        story_id = story["story_id"]
        url_list_page = story["url_list_page"]
        quantity_per_task = int(story.get("quantity_per_task", 10))
        parser_type = story.get("parser_type", "list_page")  # Mặc định là list_page

        print(f"\n🚀 Đang xử lý truyện: {story_id} - {story['title']}")
        print(f"URL danh sách chương: {url_list_page}")
        print(f"Parser type: {parser_type}")

        try:
            if parser_type == "list_page":
                # B1: Lấy toàn bộ các trang chứa danh sách chương
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                }
                resp = requests.get(url_list_page, headers=headers, timeout=10)
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, "html.parser")
                select = soup.find("select", id="indexselect")
                if not select:
                    raise Exception("Không tìm thấy <select id='indexselect'> trong trang danh sách chương.")

                page_urls = [urljoin(url_list_page, opt.get("value")) for opt in select.find_all("option")]

                print(f"🔍 Tìm thấy {len(page_urls)} trang danh sách chương.")

                all_chapters = []
                for page_url in page_urls:
                    chapter_list = parse_chapter_list_from_list_page(page_url)
                    all_chapters.extend(chapter_list)

            elif parser_type == "single_page":
                # Chỉ cần parse trực tiếp từ 1 trang
                all_chapters = parse_chapter_list_from_single_page(url_list_page)

            else:
                raise Exception(f"parser_type '{parser_type}' không được hỗ trợ.")

            print(f"📚 Tổng số chương thu được: {len(all_chapters)}")

            # B2: Chia thành các task
            tasks = []
            for i in range(0, len(all_chapters), quantity_per_task):
                chapter_group = all_chapters[i:i+quantity_per_task]
                task = {
                    "task_id": f"{story_id}_part{i//quantity_per_task + 1}",
                    "story_id": story_id,
                    "chapter_from": i + 1,
                    "chapter_to": i + len(chapter_group),
                    "url_chapters": [ch["url"] for ch in chapter_group],
                    "status": "PENDING",
                    "translated": False,
                    "css_title": story["css_title"],
                    "css_content": story["css_content"],
                    "css_next": story["css_next"],
                    "doc_url": "",
                    "audio_urls": [],
                    "video_path": "",
                    "summary": ""
                }
                tasks.append(task)
            print(tasks)
            # # B3: Ghi các task vào sheet
            # task_sheet.append_tasks(tasks)
            #
            # # B4: Cập nhật trạng thái truyện
            # story_sheet.update_story_status(story_id, "DISPATCHED")

            print(f"✅ Đã chia {len(tasks)} task cho truyện {story_id}")

        except Exception as e:
            print(f"❌ Lỗi khi xử lý truyện {story_id}: {e}")


if __name__ == "__main__":
    # Ví dụ chạy
    spreadsheet_id = "YOUR_SPREADSHEET_ID_HERE"
    dispatch_tasks(spreadsheet_id)
