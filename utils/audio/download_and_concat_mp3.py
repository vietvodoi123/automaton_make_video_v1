import os
import uuid
import subprocess
import gdown

def download_and_concat_mp3(mp3_urls, output_dir="output_audio", output_filepath="merged.mp3"):
    """
    Tải các file mp3 từ danh sách URL và ghép thành 1 file duy nhất theo thứ tự.

    :param mp3_urls: Danh sách URL file mp3 (Google Drive)
    :param output_dir: Thư mục lưu file tạm và file đầu ra
    :param output_filepath: Tên file mp3 sau khi ghép
    :return: Đường dẫn tuyệt đối của file đã ghép
    """
    # Tạo thư mục tạm
    task_id = str(uuid.uuid4())
    tmp_dir = os.path.join(output_dir, task_id)
    os.makedirs(tmp_dir, exist_ok=True)

    downloaded_files = []

    print("📥 Đang tải các file MP3...")
    for idx, url in enumerate(mp3_urls):
        filename = f"{idx:03}.mp3"
        filepath = os.path.join(tmp_dir, filename)
        try:
            gdown.download(url, filepath, quiet=False, fuzzy=True)
            downloaded_files.append(filepath)
        except Exception as e:
            print(f"❌ Không tải được: {url}")
            print(e)
            continue

    if not downloaded_files:
        raise RuntimeError("Không tải được file nào.")

    # Tạo file concat.txt để FFmpeg ghép
    concat_file = os.path.join(tmp_dir, "concat.txt")
    with open(concat_file, "w", encoding="utf-8") as f:
        for file_path in downloaded_files:
            f.write(f"file '{os.path.abspath(file_path)}'\n")

    # Đường dẫn file đầu ra


    # Gọi FFmpeg để ghép
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        output_filepath
    ]

    print("🎬 Đang ghép các file MP3 bằng FFmpeg...")
    try:
        subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Lỗi FFmpeg khi ghép file:")
        print(e)
        raise

    print(f"✅ Đã tạo file: {output_filepath}")
    return
