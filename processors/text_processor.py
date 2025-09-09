import json
import time
import traceback

from processors import extract_chapter_content_bs4, translate_full_text
from utils import refine_translation, summarize_text, recursive_summary, load_yaml_settings
from google_docs_oauth import save_translated_task
from sheets import TaskSheet,StorySheet
from utils import retry_with_limit,normalize_whitespace,collapse_blank_lines,remove_consecutive_duplicate_lines,clean_chapter_text

def text_process(task_id: str):
    config = load_yaml_settings()
    task_sheet = TaskSheet(spreadsheet_id=config['google']['sheets_id'])
    story_sheet = StorySheet(spreadsheet_id=config['google']['sheets_id'])

    task_row = task_sheet.get_task_by_id(task_id)
    story_id = task_row["story_id"]
    story_row = story_sheet.get_story_by_id(story_id)

    story_title = story_row["title"]
    urls = json.loads(task_row["url_chapters"])

    css_title = task_row["css_title"]
    css_content = task_row["css_content"]
    css_next = task_row["css_next"]

    log_prefix = f"[{task_id}]"

    full_translated_chapters = ""
    full_summrized = ""

    print(f"{log_prefix} 🔍 Bắt đầu xử lý từng chương...")

    for index, url in enumerate(urls):
        try:
            print(f"{log_prefix} 📖 Chương {index + 1}: Đang trích xuất nội dung...")
            print(f"css_next debug: {css_next!r}")
            result = retry_with_limit(3, 60, extract_chapter_content_bs4, url, css_title, css_content, css_next)
            translation = result["translation"]
            summarized = result["summarized"]

            def final_cleanup_all(text: str) -> str:
                text = normalize_whitespace(text)
                text = remove_consecutive_duplicate_lines(text)
                text = collapse_blank_lines(text, max_blank=2)
                # đảm bảo không có space thừa ở đầu/ cuối
                return text.strip()

            # trước khi save_translated_task(...)
            full_translated_chapters +="\n" + translation
            full_translated_chapters = final_cleanup_all(full_translated_chapters)
            print(index,full_translated_chapters.__len__())
            full_summrized += summarized + "\n"

        except Exception as e:
            print(f"{log_prefix} ❌ Lỗi chương {index + 1}: {e}")
            task_sheet.update_task_status(task_id, "ERROR_PROCESS_CHAPTER")
            return

    #  lưu vào driver
    print(full_translated_chapters.__len__())
    try:
        doc_url = retry_with_limit(
            max_retries=3,
            delay_sec=10,
            func=save_translated_task,
            story_title=story_title,
            task_id=task_id,
            translated_text=full_translated_chapters
        )
        print("✅ Google Docs đã tạo thành công:", doc_url)

    except Exception as e:
        print("❌ Gặp lỗi khi lưu lên Google Docs:", e)
        traceback.print_exc()


    # ✅ Bước 4: Cập nhật task sheet
    try:
        task_sheet.update_task_status(
            task_id,
            "TEXT_DONE",
            extra_updates={
                "translated": "TRUE",
                "doc_url": doc_url,
                "summary": full_summrized
            }
        )
        print(f"{log_prefix} ✅ Hoàn tất toàn bộ task.")
        return
    except Exception as e:
        print(f"{log_prefix} ⚠️ Đã xử lý xong nhưng lỗi khi cập nhật sheet: {e}")
        traceback.print_exc()
