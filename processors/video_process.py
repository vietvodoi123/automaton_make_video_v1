import os
from sheets import ChannelSheet,TaskSheet,StorySheet
import json
from create_video_with_html.run_pipeline import run_pipeline
from utils import (
    upload_to_drive,
    load_yaml_settings,create_looped_mc_video_from_url, overlay_all,
    TMP_DIR, download_and_concat_mp3,create_scrolling_text_video,create_looped_scrolling,get_video_duration
)

from utils.run_ffmpeg_with_progress import run_ffmpeg_with_progress

def merge_audio_into_video(video_path, audio_path, output_path):
    """
    Ghép audio vào video:
    - Không tái mã hóa video (dùng copy stream)
    - Chỉ cắt theo độ dài ngắn hơn giữa video và audio (dùng -shortest)
    """

    cmd = [
        "ffmpeg",
        "-y",
        "-loglevel", "info",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",           # Không encode lại video
        "-c:a", "aac",            # Mã hóa audio về AAC
        "-b:a", "192k",           # Bitrate audio
        "-shortest",              # Dừng khi hết video hoặc audio
        output_path
    ]

    print("🎧 Đang ghép audio vào video...")
    run_ffmpeg_with_progress(cmd, input_file=video_path)
    print(f"✅ Đã xuất video kèm âm thanh: {output_path}")

def create_template_video(story_row,task_row,channel_row,template_path):
    task_id = task_row.get('task_id')
    channel_id = channel_row.get("channel_id")
    output_path = template_path
    path_text = os.path.join("tmp", task_id, task_id + ".txt")  # path text
    metadata = {
        "title": story_row.get("title"),
        "chapter_from": task_row.get("chapter_from"),
        "chapter_to": task_row.get("chapter_to"),
        "tags": story_row.get("type"),
        "background_url": story_row.get("background_url"),
        "channel_name": channel_row.get("name"),
        "channel_id": channel_id,
        "channel_subs": channel_row.get("subscriber"),
        "mc_name": channel_row.get("mc_name"),
        "channel_avatar_url": channel_row.get("avatar_url")
    }
    run_pipeline(task_id, path_text, metadata, output_path)

def dowload_and_concat_audio(task_dir, task_id, task_row):
    audio_tmp = os.path.join(task_dir, f"{task_id}_audio")
    os.makedirs(audio_tmp, exist_ok=True)
    # merged path
    merged_path = os.path.join(task_dir, f"{task_id}_merged.mp3")
    # audio url
    audio_urls = json.loads(task_row['audio_urls'])
    download_and_concat_mp3(audio_urls, audio_tmp, merged_path)

def scrolling_notification_and_infor(task_dir,task_id,channel_row):
    scroll_video_path = os.path.join(task_dir, f'{task_id}_text_ticker.mp4')
    donate_info = channel_row.get("donate_info")
    notification = channel_row.get("notification")
    create_scrolling_text_video(
        text=donate_info + " " + notification,
        font_size=20,
        speed=100,
        y_position=12,
        resolution=(1232, 50),
        font_color="white",
        bg_transparent=False,
        output_path=scroll_video_path,
        font_path=r'D:\py_prj\automation_video_1\fonts\Anton-Regular.ttf'
    )


def create_video_with_task_id(task_id:str):
    task_dir =os.path.join(TMP_DIR,task_id)

    # config
    config = load_yaml_settings()
    sheet_id = config["google"]['sheets_id']
    # sheet
    channel_sheet_ws = ChannelSheet(sheet_id)
    stories_sheet_ws = StorySheet(sheet_id)
    task_sheet_ws = TaskSheet(sheet_id)
    # lay task row
    task_row = task_sheet_ws.get_task_by_id(task_id)
    # print(task_row)
    # get story
    story_id = task_row['story_id']
    story_row = stories_sheet_ws.get_story_by_id(story_id)
    # get channel
    channel_id = story_row['channel_id']
    channel_row = channel_sheet_ws.get_channel_by_id(channel_id)

    # download and concat
    # audio download dir
    dowload_and_concat_audio(task_dir,task_id,task_row)

    # create template video
    template_path = os.path.join(task_dir, f"{task_id}_template.mp4")
    create_template_video(story_row, task_row, channel_row, template_path)

    # create scrolling notificaitons
    scrolling_notification_and_infor(task_dir, task_id, channel_row)

    # looped scrolling text
    duration = get_video_duration(template_path)
    scroll_video_path = os.path.join(task_dir, f'{task_id}_text_ticker.mp4')
    scrolling_looped_path = os.path.join(task_dir, f'{task_id}_scrolling_looped.mp4')
    create_looped_scrolling(scroll_video_path,scrolling_looped_path,duration)

    # mc path
    mc_video_url = channel_row['mc_path']
    mc_looped_path = os.path.join(task_dir,'mc_video_looped.mp4')
    create_looped_mc_video_from_url(mc_video_url, mc_looped_path,duration)

    # overlay all
    output_path = os.path.join(task_dir, f'{task_id}_output.mp4')
    audio_merged_path = os.path.join(task_dir,f"{task_id}_merged.mp3")
    overlay_all(template_path,scrolling_looped_path,mc_looped_path,output_path)

    # finish
    output_video_finish = os.path.join(task_dir,f"{task_id}_finish.mp4")
    merge_audio_into_video(output_path,audio_merged_path,output_video_finish)

    # upload gg drive
    config = load_yaml_settings()
    folder_id = config['google']['docs_folder_id']
    url = upload_to_drive(output_video_finish,folder_id,story_row['title'])

    if url:
        print("✅ Upload thành công. Đang cập nhật task")
        task_sheet_ws.update_task_status(task_id,"ALL_DONE",{
            "video_path":url
        })
    # cleanup
    import shutil
    shutil.rmtree(task_dir)