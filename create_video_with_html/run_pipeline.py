import os
import shutil
import subprocess
from create_video_with_html.render_template import render_template
from create_video_with_html.render_video import create_video_from_concat
from create_video_with_html.generate_concat_txt import generate_concat_file_by_audio_duration,generate_concat_file_seconds_per_word,generate_concat_file_balanced
from utils import TMP_DIR,estimate_seconds_per_word
def save_text_to_file(text, path="data.txt"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.strip())
    print(f"📄 Đã lưu văn bản vào {path}")

def render_frames(frames_path,data_file="data.txt"):
    if not os.path.isfile(data_file):
        raise FileNotFoundError(f"❌ File không tồn tại: {data_file}")

    print(f"📸 Đang render các frame từ {data_file}...")
    js_path = os.path.abspath(os.path.join("create_video_with_html", "render_frames.js"))

    data_file = os.path.abspath(data_file)
    subprocess.run(["node", js_path, data_file, frames_path], check=True)
    print("✅ Đã render xong frames")

def generate_concat(task_id,tmp_dir ,frames_path,output_path,data_file='data.txt'):
    print("🧮 Đang tạo concat.txt...")
    data_file = os.path.abspath(data_file)
    mp3_path = os.path.join(tmp_dir, f"{task_id}_merged.mp3")
    # secorns_per_word = estimate_seconds_per_word(mp3_path,data_file)
    generate_concat_file_balanced(data_file, frames_path, output_path,mp3_path)
    print("✅ Đã tạo concat.txt")

def render_video(concat_path, output_path, use_gpu=False):
    print("🎞️ Đang render video...")
    env = os.environ.copy()
    env["USE_GPU"] = "1" if use_gpu else "0"

    create_video_from_concat(concat_path, output_path)
    print("✅ Video đã được tạo: output.mp4")


def run_pipeline(task_id, data_file, meta,output_path, use_gpu=False):
    tmp_dir = os.path.join(TMP_DIR,task_id)

    frames_path = os.path.join(tmp_dir, f"{task_id}_frames")
    os.makedirs(frames_path, exist_ok=True)

    concat_path = os.path.join(tmp_dir,f'{task_id}_concat.txt')

    # 1. Render template HTML
    render_template(
        template_path="create_video_with_html/template.html",
        output_path="create_video_with_html/rendered.html",
        context=meta,
    )

    # 2. Render frame ảnh
    render_frames(frames_path,data_file)

    # 4. Tạo concat.txt
    generate_concat(task_id,tmp_dir,frames_path, concat_path, data_file)

    # 5. Render video
    render_video(concat_path, output_path)




# Chạy demo nếu gọi trực tiếp
# if __name__ == "__main__":
#     with open("data.txt", "r", encoding="utf-8") as f:
#         input_text = f.read()
#
#     metadata = {
#         "title": "Huy động vốn xây Đại học Tu Tiên, Ta thật sự không có đào lửa!",
#         "tags": "#HànhĐộng #XuyênKhông",
#         "background_url": "https://i.pinimg.com/1200x/d0/9d/8b/d09d8b229469ed2417c39f2650229b08.jpg",
#         "channel_name": "Vi Tiếu Hùng Audio",
#         "channel_id": "@truyenaudio12343",
#         "channel_subs": "1,92N Người đăng ký",
#         "mc_name": "MC Tiểu Linh"
#     }
#
#     run_pipeline(input_text, meta=metadata, use_gpu=False)
