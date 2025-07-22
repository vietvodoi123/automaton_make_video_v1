import subprocess
import re
from tqdm import tqdm
import shlex

def get_video_duration(input_file):
    """Lấy thời lượng của video bằng ffprobe"""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration", "-of",
         "default=noprint_wrappers=1:nokey=1", input_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


def run_ffmpeg_with_progress(ffmpeg_cmd, input_file=None):
    """
    Chạy lệnh ffmpeg với thanh tiến trình.
    - ffmpeg_cmd: list hoặc string của lệnh ffmpeg
    - input_file: đường dẫn file đầu vào để lấy thời lượng
    """

    # Nếu là chuỗi thì chuyển thành list
    if isinstance(ffmpeg_cmd, str):
        ffmpeg_cmd = shlex.split(ffmpeg_cmd)

    # In ra lệnh ffmpeg để debug
    print("📋 FFmpeg Command:")
    print(" ".join(ffmpeg_cmd))  # In toàn bộ lệnh để dễ kiểm tra

    # Lấy thời lượng video nếu có
    duration = get_video_duration(input_file) if input_file else None
    if duration:
        progress_bar = tqdm(total=duration, unit="s", desc="Processing", dynamic_ncols=True)
    else:
        print("⚠️ Không lấy được thời lượng video. Đang chạy ffmpeg...")

    # Regex để bắt thời gian trong log ffmpeg
    time_pattern = re.compile(r"time=(\d+):(\d+):(\d+)\.(\d+)")

    # Mở tiến trình FFmpeg
    process = subprocess.Popen(ffmpeg_cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, universal_newlines=True)

    stderr_log = []  # lưu log lỗi

    for line in process.stderr:
        stderr_log.append(line)  # lưu lại để in nếu lỗi
        match = time_pattern.search(line)
        if match and duration:
            h, m, s, ms = map(int, match.groups())
            current_time = h * 3600 + m * 60 + s + ms / 100
            progress_bar.n = min(current_time, duration)
            progress_bar.refresh()

    process.wait()

    if duration:
        progress_bar.n = duration
        progress_bar.refresh()
        progress_bar.close()

    if process.returncode != 0:
        print("\n❌ FFmpeg trả về lỗi:")
        print("".join(stderr_log))  # In toàn bộ stderr
        raise RuntimeError("❌ ffmpeg bị lỗi. Kiểm tra lại lệnh.")

    print("✅ Hoàn thành.")


