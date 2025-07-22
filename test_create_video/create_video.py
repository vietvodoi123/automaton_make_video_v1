import subprocess

def encode_video_with_gpu(input_pattern='frames/frame_%05d.png', output='cuon_text.mp4', fps=30):
    cmd = [
        'ffmpeg',
        '-y',
        '-hwaccel', 'auto',
        '-framerate', str(fps),
        '-i', input_pattern,
        '-c:v', 'h264_amf',
        '-pix_fmt', 'yuv420p',
        output
    ]
    subprocess.run(cmd)
    print(f"✅ Video đã được tạo: {output}")

encode_video_with_gpu()  # Uncomment để chạy
