from utils import get_audio_duration
def estimate_seconds_per_word(mp3_path, text_path):
    """
    Ước lượng thời gian trung bình để đọc 1 từ, dựa vào độ dài audio và số từ trong văn bản.

    Parameters:
    - mp3_path (str): Đường dẫn đến file mp3.
    - text_path (str): Đường dẫn đến file văn bản chứa nội dung đọc (1 dòng 1 câu).

    Returns:
    - seconds_per_word (float): Số giây trung bình cho mỗi từ.
    """

    # Lấy độ dài audio (giây)
    audio_duration = get_audio_duration(mp3_path)

    # Đọc nội dung và đếm số từ
    with open(text_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_words = 0
    for line in lines:
        line = line.strip()
        if line:  # bỏ qua dòng trắng
            total_words += len(line.split())

    if total_words == 0:
        raise ValueError("⚠️ File text không có từ nào để tính toán.")

    # Tính thời gian trung bình mỗi từ
    seconds_per_word = round(audio_duration / total_words, 4)

    print(f"📊 Tổng thời lượng audio: {round(audio_duration, 2)} giây")
    print(f"📝 Tổng số từ: {total_words}")
    print(f"⏱️ Thời gian trung bình mỗi từ: {seconds_per_word} giây")

    return seconds_per_word
