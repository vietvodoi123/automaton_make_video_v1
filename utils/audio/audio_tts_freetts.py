import aiohttp
import json
from bs4 import BeautifulSoup

def extract_audio_url(raw_item: str) -> str:
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

async def call_audio_api(segment):
    url = "https://freetts.com/text-to-speech"

    headers = {
        "accept": "text/x-component",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "content-type": "text/plain;charset=UTF-8",
        "next-action": "f6a37f3b9ffdb01ba2da16f264fdabab4a254f61",
        "next-router-state-tree": "[\"\",{\"children\":[\"functions\",{\"children\":[\"text-to-speech\",{\"children\":[\"__PAGE__\",{},\"/text-to-speech\",\"refresh\"]}]}]}]",
        "origin": "https://freetts.com",
        "priority": "u=1, i",
        "referer": "https://freetts.com/text-to-speech",
        "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Cookie": "_ga=GA1.1.1605508501.1741007918; _ga_R18J4BQM3E=GS1.1.1742456868.5.0.1742456868.0.0.0; Authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjU0Njg1LCJ1c2VybmFtZSI6InZpZXR2b2RvaTEyMzJAZ21haWwuY29tIiwicGFzc3dvcmQiOiJBQjkwNjZFMDQwMkQwNjNGMUNDNzlGNEQ3REY4MzMzMyIsImlhdCI6MTc0MjQ1Njg2OH0.dssyfScOgELjr5XduB08lnE7WOaxPnpA-zTbik3jTAY; __gads=ID=d6442946faeba0f3:T=1741598683:RT=1742456868:S=ALNI_MYipaz-6Z1Qbzc5xhsCZVS4G-SCSw; __gpi=UID=00000ffbff0ceb6d:T=1741598683:RT=1742456868:S=ALNI_MaHLL0nBsoxr4xfa3IuEftiLlGPIw; __eoi=ID=b51a9010f4ca1855:T=1741598683:RT=1742456868:S=AA-Afja4a2TWWnn4WgO_P9kaI9Cn; FCNEC=%5B%5B%22AKsRol9cfzexBfgumw5dI4iaw4_sN1fuB6qiXeE4QCq1amz0H_pQh-Cg4UfyZc5RvNUPkPcyeH8tfOyFPWCtSLkChtnxVTA6kkg-RRe4OBh7SJofun6Vs1iHqf4tMReR-OGOs4tVKM7Et7QpLBXcWoaYl4VDpRKjog%3D%3D%22%5D%5D"
    }

    payload = [{
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
    }]

    data = json.dumps(payload)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status != 200:
                    text = await response.text()
                    print(f"⚠️ Lỗi khi gọi API: {response.status} - {text}")
                    return None  # Trả về None thay vì raise Exception

                text_response = await response.text()
                return extract_audio_url(text_response)  # Hàm này cần được định nghĩa để lấy URL từ phản hồi
    except Exception as e:
        print(f"❌ Lỗi ngoại lệ khi gọi API: {e}")
