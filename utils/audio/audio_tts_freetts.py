
import json

import asyncio
def extract_audio_url(raw_item: str) -> str:
    print(raw_item)
    lines = raw_item.split("\n")
    if len(lines) < 2:
        return ""

    second_line = lines[1].strip()
    if ":" in second_line:
        _, json_str = second_line.split(":", 1)
        try:
            data_obj = json.loads(json_str.strip())
            return data_obj.get("data", {}).get("audiourl", "")
        except json.JSONDecodeError:
            pass
    return ""

def split_text(text: str, limit: int = 3000) -> list[str]:
    text_with_break = text.replace("\n", '\n<break time="0.3s"/>')
    lines = text_with_break.split("\n")

    segments = []
    current_segment = ""

    for line in lines:
        if len(line) >= limit:
            if current_segment:
                segments.append(current_segment.strip())
                current_segment = ""
            for i in range(0, len(line), limit - 1):
                segments.append(line[i:i + limit - 1])
        else:
            if len(current_segment) + 1 + len(line) < limit:
                current_segment += ("\n" + line if current_segment else line)
            else:
                segments.append(current_segment.strip())
                current_segment = line

    if current_segment:
        segments.append(current_segment.strip())

    # Gộp đoạn nhỏ liền kề (optional step)
    merged_segments = []
    buffer = ""
    for seg in segments:
        if not buffer:
            buffer = seg
        elif len(buffer) + 1 + len(seg) < limit:
            buffer += "\n" + seg
        else:
            merged_segments.append(buffer)
            buffer = seg
    if buffer:
        merged_segments.append(buffer)

    return merged_segments

import json
from utils import encrypt_payload, decrypt_params, call_tts_api

async def call_audio_api(segment: str) -> str:
    payload_object = {
        "text": segment,
        "type": 0,
        "ssml": 0,
        "voiceType": "WaveNet",
        "languageCode": "vi-VN",
        "voiceName": "vi-VN-Wavenet-C",
        "gender": "FEMALE",
        "speed": "1.0",
        "pitch": "0",
        "volume": "0",
        "format": "mp3",
        "quality": 0,
        "isListenlingMode": 0,
        "displayName": "Veronica Chan"
    }

    # Encrypt thành params
    params = encrypt_payload(payload_object)
    # print("Params:", params)

    COOKIE_STRING = "_ga=...; Authorization=eyJhbGc...; __gpi=..."  # ⚠️ thay bằng cookie thực tế
    response = call_tts_api(params, COOKIE_STRING)

    # print("Response:", response)

    # Tách lấy dòng JSON (dòng bắt đầu bằng '1:')
    lines = response.split("\n")
    audio_url = ""
    if len(lines) > 1 and lines[1].startswith("1:"):
        try:
            _, json_str = lines[1].split(":", 1)
            data_obj = json.loads(json_str.strip())
            audio_url = data_obj.get("data", {}).get("audiourl", "")
        except Exception as e:
            print("❌ Lỗi parse response:", e)

    # # Debug: giải mã payload để chắc chắn
    # try:
    #     decoded = decrypt_params(params)
    #     print("Decrypted payload:", decoded)
    # except Exception:
    #     pass
    print(audio_url)
    return audio_url



# if __name__ == "__main__":
#     asyncio.run(call_audio_api("""Xin chào các bạn khán giả! Mình là MC Tiểu Linh, chào mừng các bạn đến với kênh Vi Tiếu Hùng Audio.
# Kênh chuyên sưu tầm và đọc những bộ truyện mới nhất về mọi thể loại, nếu bạn muốn yêu cầu truyện hãy comment xuống dưới hoặc vào bio của mình vào phần bài viết và để lại yêu cầu. truyện sẽ đươc làm nhanh nhất cho bạn.
# Hôm nay chúng ta sẽ cùng tiếp tục theo dõi bộ truyện "Bị Cấm Thi Đại Học – Ta Tự Chế Máy Bay Tàng Hình Thế Hệ 6!", tập Chương 171 - 180.
# Trước khi vào nội dung chính của tập ngày hôm nay, chúng ta sẽ đi nói qua nội dung chính của tập trước nhé:
# """))
