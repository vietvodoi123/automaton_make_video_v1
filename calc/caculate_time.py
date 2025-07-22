import os
from mutagen.mp3 import MP3

AUDIO_DIR = "audio"
TEXT_DIR = "text"
BREAK_TIME = 0.3  # giây giữa các dòng

def count_words_in_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    word_count = sum(len(line.split()) for line in lines)
    return word_count, len(lines)

def get_audio_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length  # thời lượng tính bằng giây

def estimate_seconds_per_word():
    total_audio_time = 0.0
    total_words = 0
    total_breaks = 0

    for filename in os.listdir(TEXT_DIR):
        if filename.endswith(".txt"):
            base_name = os.path.splitext(filename)[0]
            text_path = os.path.join(TEXT_DIR, filename)
            audio_path = os.path.join(AUDIO_DIR, base_name + ".mp3")

            if not os.path.exists(audio_path):
                print(f"⚠️ Không tìm thấy audio cho {filename}")
                continue

            word_count, num_lines = count_words_in_text(text_path)
            duration = get_audio_duration(audio_path)
            break_time = (num_lines - 1) * BREAK_TIME

            total_audio_time += duration - break_time
            total_words += word_count
            total_breaks += num_lines - 1

            print(f"✅ {base_name}: {word_count} từ, {duration:.2f}s audio, {break_time:.2f}s nghỉ")

    if total_words == 0:
        print("❌ Không có từ nào để tính.")
        return

    seconds_per_word = total_audio_time / total_words
    print(f"\n📊 Tổng thời gian thực: {total_audio_time:.2f}s")
    print(f"📝 Tổng số từ: {total_words}")
    print(f"🔢 Tổng thời gian nghỉ: {total_breaks * BREAK_TIME:.2f}s")
    print(f"⏱️ seconds_per_word = {seconds_per_word:.4f} giây/từ")

    return seconds_per_word

# Gọi hàm:
estimate_seconds_per_word()
