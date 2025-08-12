from parsers.single_page_parser import parse_chapter_list_from_single_page

def dispatch_tasks_test_single_page():
    # Giả lập 1 truyện có tất cả chương nằm chung 1 trang
    new_stories = [
        {
            "story_id": "test_story",
            "title": "Truyện Test Single Page",
            "url_list_page": "https://www.xm200.com/book/371789",  # đổi thành link thật
            "quantity_per_task": 10,
            "parser_type": "single_page",
            "css_title": "title",
            "css_content": "div.content",
            "css_next": "a.next"
        }
    ]

    for story in new_stories:
        story_id = story["story_id"]
        url_list_page = story["url_list_page"]
        quantity_per_task = int(story.get("quantity_per_task", 10))
        parser_type = story.get("parser_type", "list_page")

        print(f"\n🚀 Đang xử lý truyện: {story_id} - {story['title']}")
        print(f"URL danh sách chương: {url_list_page}")
        print(f"Parser type: {parser_type}")

        try:
            if parser_type == "single_page":
                all_chapters = parse_chapter_list_from_single_page(url_list_page)
            else:
                raise Exception(f"parser_type '{parser_type}' không được hỗ trợ trong test này.")

            print(f"📚 Tổng số chương thu được: {len(all_chapters)}")

            # Chia thành các task
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

            # In ra task để kiểm tra
            for t in tasks:
                print(t)

            print(f"✅ Đã chia {len(tasks)} task cho truyện {story_id}")

        except Exception as e:
            print(f"❌ Lỗi khi xử lý truyện {story_id}: {e}")


if __name__ == "__main__":
    dispatch_tasks_test_single_page()
