import os
import subprocess
import json
def get_audio_duration(mp3_path):
    """
    Lấy độ dài file mp3 bằng ffprobe (không cần audioop hay pydub).
    """
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        mp3_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = json.loads(result.stdout)
    duration = float(info["format"]["duration"])
    return duration