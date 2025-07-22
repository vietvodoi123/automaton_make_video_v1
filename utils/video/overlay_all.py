from utils.run_ffmpeg_with_progress import run_ffmpeg_with_progress

from utils.run_ffmpeg_with_progress import run_ffmpeg_with_progress

from utils.run_ffmpeg_with_progress import run_ffmpeg_with_progress

def overlay_all(template_path, scrolling_path, mc_path, output_path):
    """
    Ghép scrolling + mc-video vào template:
    - scrolling đặt ở dưới (centered)
    - mc-video (đã resize/crop sẵn 265x300) đặt tại (x=965, y=256)
    - KHÔNG GHÉP ÂM THANH để tăng tốc render
    """

    template_width = 1280
    mc_width, mc_height = 265, 300
    mc_x = template_width - mc_width - 44  # 965
    mc_y = 256

    filter_complex = (
        "[0:v]fps=8,setpts=PTS-STARTPTS[base];"
        "[1:v]setpts=PTS-STARTPTS[scroll];"
        "[2:v]setpts=PTS-STARTPTS[mc];"
        "[base][scroll]overlay=x=(W-w)/2:y=H-h-50[tmp];"
        f"[tmp][mc]overlay=x={mc_x}:y={mc_y}[vout]"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-loglevel", "info",
        "-i", template_path,
        "-i", scrolling_path,
        "-i", mc_path,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-shortest",
        "-r", "8",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "23",
        "-preset", "medium",
        output_path
    ]

    print("▶️ Đang ghép video (scroll + mc)...")
    run_ffmpeg_with_progress(cmd, input_file=template_path)
    print(f"✅ Đã xuất video không audio: {output_path}")



