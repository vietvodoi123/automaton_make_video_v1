import os
import subprocess
from utils.dowloader import download_file  # hoặc sửa lại import đúng theo cấu trúc project của bạn

def merge_audio_from_urls(audio_urls, output_path):
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)

    file_list = []
    for i, url in enumerate(audio_urls):
        # Dùng hàm download_file có sẵn
        audio_path = download_file(url, save_dir=temp_dir)
        file_list.append(audio_path)

    # Ghi file danh sách cho ffmpeg
    input_txt_path = os.path.join(temp_dir, "input.txt")
    with open(input_txt_path, "w", encoding="utf-8") as f:
        for path in file_list:
            f.write(f"file '{os.path.abspath(path)}'\n")

    # Ghép audio
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", input_txt_path, "-c", "copy", output_path
    ], check=True)

    # Dọn file tạm
    for f in [input_txt_path]:
        os.remove(f)
    # Bạn có thể giữ lại file âm thanh gốc nếu muốn dùng lại
    # Hoặc thêm dòng này để xoá tất cả:
    # shutil.rmtree(temp_dir)

    return output_path
