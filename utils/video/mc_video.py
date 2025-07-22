import os
import tempfile
import requests
import gdown
import re
from utils.run_ffmpeg_with_progress import get_video_duration, run_ffmpeg_with_progress


def extract_file_id_from_url(url):
    """
    Trích xuất file ID từ link Google Drive.
    Hỗ trợ 2 dạng phổ biến:
    - https://drive.google.com/file/d/<FILE_ID>/view?usp=sharing
    - https://drive.google.com/uc?export=download&id=<FILE_ID>
    """
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    match = re.search(r"id=([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    raise ValueError("❌ Không tìm được file ID trong link Google Drive.")


def convert_gdrive_to_direct(url):
    """
    Chuyển link Google Drive sang link tải trực tiếp.
    """
    file_id = extract_file_id_from_url(url)
    return f"https://drive.google.com/uc?export=download&id={file_id}"


def download_video_from_url(url, save_path):
    """
    Tải video từ URL về máy (hỗ trợ cả Google Drive và link thường)
    """
    if "drive.google.com" in url:
        file_id = extract_file_id_from_url(url)
        print(f"🔽 Đang tải từ Google Drive với ID: {file_id}")
        gdown.download(id=file_id, output=save_path, quiet=False)
    else:
        print(f"🔽 Đang tải video từ URL: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    return save_path


def create_looped_mc_video_from_url(video_url, output_path, duration):
    """
    Tải video từ URL → lặp lại cho đến khi đủ thời lượng yêu cầu → xuất ra video đích (đã resize + crop)
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        local_input_path = os.path.join(tmpdir, "input_video.mp4")

        print(f"🔽 Downloading video from {video_url} ...")
        download_video_from_url(video_url, local_input_path)

        # Lấy thời lượng video gốc
        input_duration = get_video_duration(local_input_path)
        if input_duration is None:
            raise ValueError("❌ Không lấy được thời lượng video! Kiểm tra định dạng/codec file.")

        # Tính số vòng lặp
        loop_count = int(duration // input_duration) + 1

        # Resize (scale) thành 263px chiều ngang, crop chiều cao còn 306
        vf_filter = "fps=8,scale=265:-1,crop=265:300:0:0"

        # Tạo video loop + crop
        cmd = [
            "ffmpeg", "-y", "-loglevel", "info",
            "-stream_loop", str(loop_count),
            "-i", local_input_path,
            "-t", str(duration),
            "-an",
            "-vf", vf_filter,
            "-r", "8",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output_path
        ]
        run_ffmpeg_with_progress(cmd, input_file=local_input_path)

    return output_path


