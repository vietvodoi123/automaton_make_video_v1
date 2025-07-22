import asyncio
import json
import os
import traceback
from utils.audio.audio_tts_freetts import split_text, call_audio_api
from sheets import ChannelSheet, StorySheet, TaskSheet
from utils.audio.add_intro_and_comments import add_intro_and_comments
from google_docs_oauth.get import get_doc_content_from_url
from utils import load_yaml_settings
async def call_audio_with_retry(text, max_retries=3, delay_sec=2):
    async def wrapper():
        audio_url = await call_audio_api(text)
        if not audio_url:
            raise ValueError("API trả về URL rỗng.")
        return audio_url

    for attempt in range(1, max_retries + 1):
        try:
            return await wrapper()
        except Exception as e:
            print(f"❌ Lỗi API ở đoạn {attempt}/{max_retries}: {e}")
            if attempt < max_retries:
                print(f"🔁 Đợi {delay_sec}s trước khi thử lại...")
                await asyncio.sleep(delay_sec)
            else:
                print("❌ Bỏ qua đoạn này.")
                return ""

async def audio_process(task_id: str):
    config = load_yaml_settings()
    spreadsheet_id = config['google']['sheets_id']
    # Khởi tạo các sheet
    channel_sheet = ChannelSheet(spreadsheet_id=spreadsheet_id)
    story_sheet = StorySheet(spreadsheet_id=spreadsheet_id)
    task_sheet = TaskSheet(spreadsheet_id=spreadsheet_id)

    # print("lấy thông tin task")
    # Lấy thông tin task
    try:
        task_row = task_sheet.get_task_by_id(task_id)
    except ValueError as e:
        print(f"Không tìm thấy task có id {task_id}: {e}")
        return []
    # print("lấy thông tin kênh")


    # Lấy intro2: mô tả hoặc tóm tắt
    chapter_from = str(task_row.get("chapter_from", "")).strip()
    story_id = task_row["story_id"]
    story_info = story_sheet.get_story_by_id(story_id)
    intro2= ""
    if chapter_from == "1":

        if not story_info:
            print(f"Không tìm thấy story có id {story_id}")
            return []
        intro2 = story_info.get("description", "")
        if not intro2:
            print(f"Story có id {story_id} không có mô tả")
            return []
    else:
        try:
            # Dự đoán task trước đó theo định dạng `_partN`
            if "_part" in task_id:
                prefix, part = task_id.rsplit("_part", 1)
                previous_task_id = f"{prefix}_part{int(part) - 1}"
            else:
                previous_task_id = task_id[:-1] + str(int(task_id[-1]) - 1)
            previous_task_row = task_sheet.get_task_by_id(previous_task_id)
            intro2 = previous_task_row.get("summary", "")
            if not intro2:
                print(f"Task có id {previous_task_id} không có tóm tắt")
                return []
        except Exception as e:
            print(f"Không tìm thấy task trước đó cho {task_id}: {e}")
            return []

        # Lấy thông tin kênh
    channel_id = story_info.get("channel_id") or task_row.get("channel_id")  # fallback nếu viết sai chính tả
    channel_info = channel_sheet.get_channel_by_id(channel_id)
    if not channel_info:
        print(f"Không tìm thấy thông tin kênh với id {channel_id}")
        return []

    # print("lấy nội dung doc")
    # Lấy nội dung từ Google Docs
    doc_url = task_row["doc_url"]
    raw_text = get_doc_content_from_url(doc_url)

    # Chuẩn bị meta để truyền vào add_intro_and_comments
    intro1 = channel_info.get("mc_intro", "").format(channel_name=channel_info.get('name'),mc_name=channel_info.get('mc_name') ,story_title=story_info.get("title"),episode_number=f"Chương {task_row.get("chapter_from")} - {task_row.get("chapter_to")}")
    meta = {
        "intro1": intro1,
        "intro2": intro2,
        "comments": json.loads(channel_info.get("comments")),
    }

    full_text = add_intro_and_comments(raw_text, **meta)

    os.makedirs(f"tmp/{task_id}", exist_ok=True)
    # Lưu full_text vào file txt
    with open(f"tmp/{task_id}/{task_id}.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    # print("đã lưu file")

    chunks = split_text(full_text)
    semaphore = asyncio.Semaphore(15)

    async def call_with_limit(chunk):
        async with semaphore:
            return await call_audio_with_retry(chunk)

    tasks = [call_with_limit(chunk) for chunk in chunks]
    results = await asyncio.gather(*tasks)

    # caapj nhaatj task sheet
    try:
        task_sheet.update_task_status(
            task_id,
            "AUDIO_DONE",
            extra_updates={
                "audio_urls": results,
            }
        )
        print(f"{task_id} ✅ Hoàn tất toàn Audio.")
        return
    except Exception as e:
        print(f"{task_id} ⚠️ Đã xử lý xong nhưng lỗi khi cập nhật sheet: {e}")
        traceback.print_exc()

    return

