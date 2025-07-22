import subprocess
import os
from utils.run_ffmpeg_with_progress import run_ffmpeg_with_progress  # Đảm bảo đã import

def create_video_from_concat(concat_file="concat.txt",
                             output_file="output.mp4",
                             use_gpu=False,
                             codec=None):
    """
    Tạo video từ concat.txt bằng FFmpeg
    :param concat_file: Đường dẫn đến concat.txt
    :param output_file: Tên file video đầu ra
    :param use_gpu: Dùng GPU nếu True
    :param codec: Codec tùy chọn (vd: "libx264", "h264_nvenc")
    """

    if not os.path.exists(concat_file):
        print(f"❌ Không tìm thấy file: {concat_file}")
        return

    if not codec:
        codec = "h264_nvenc" if use_gpu else "libx264"

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-loglevel", "info",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-vsync", "vfr",
        "-pix_fmt", "yuv420p",
        "-c:v", codec,
        output_file
    ]

    print("▶️ Đang tạo video từ concat.txt bằng FFmpeg...")
    try:
        run_ffmpeg_with_progress(ffmpeg_cmd)
        print(f"✅ Đã tạo video: {output_file}")
    except RuntimeError as e:
        print("❌ FFmpeg gặp lỗi:")
        print(e)
