import subprocess
import os
from utils.run_ffmpeg_with_progress import get_video_duration, run_ffmpeg_with_progress


def create_scrolling_text_video(
        text,
        font_size=20,
        speed=100,
        y_position=50,
        resolution=(1280, 200),
        font_color="white",
        bg_transparent=False,
        output_path="scrolling_text.mp4",
        font="Anton"
):
    import math

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    width, height = resolution

    # Ước lượng chiều dài dòng chữ tính theo pixel
    avg_char_width = font_size * 0.6  # hệ số xấp xỉ
    text_width = len(text) * avg_char_width

    # Tính thời gian cần để chạy hết dòng chữ (ra khỏi màn hình)
    duration = (text_width + width) / speed
    duration = math.ceil(duration)  # làm tròn lên để không bị cắt chữ

    if bg_transparent:
        bg_filter = f"color=black@0.0:s={width}x{height}:d={duration}"
        pix_fmt = "yuva420p"
        codec = "libvpx-vp9"
        ext = ".webm"
    else:
        bg_filter = f"color=black@0.3:s={width}x{height}:d={duration}"
        pix_fmt = "yuv420p"
        codec = "libx264"
        ext = ".mp4"

    # Fix output path extension
    output_path = os.path.splitext(output_path)[0] + ext
    escaped_text = text.replace(":", r'\:').replace("'", r"\\'")
    drawtext = (
        f"drawtext=font='{font}':"
        f"text='{escaped_text}':"
        f"fontcolor={font_color}:fontsize={font_size}:"
        f"x=w-mod(t*{speed}\\,w+tw):y={y_position}"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-loglevel", "info",
        "-f", "lavfi",
        "-i", bg_filter,
        "-vf", drawtext,
        "-t", str(duration),
        "-pix_fmt", pix_fmt,
        "-c:v", codec,
        output_path
    ]

    print("▶️ Đang tạo video chạy chữ với FFmpeg...")
    run_ffmpeg_with_progress(cmd)
    print(f"✅ Video đã tạo: {output_path} (duration: {duration}s)")

    return


def create_looped_scrolling(input_path, output_path, duration):
    input_duration = get_video_duration(input_path)
    loop_count = int(duration // input_duration) + 1

    cmd = [
        "ffmpeg",
        "-y",
        "-loglevel", "info",
        "-stream_loop", str(loop_count),
        "-i", input_path,
        "-t", str(duration),
        "-an",
        "-r", "8",  # đặt FPS đầu ra rõ ràng
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    run_ffmpeg_with_progress(cmd, input_file=input_path)
