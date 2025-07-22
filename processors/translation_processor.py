import requests
from utils.text.extract_text_with_linebreaks import extract_text_with_linebreaks
def translate_full_text(text: str, text_type: str = "Ancient") -> str:
    url = "https://api.dichnhanh.com/"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "vi-VN,vi;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://dichnhanh.com",
        "referer": "https://dichnhanh.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/138.0.0.0 Safari/537.36"
    }
    data = {
        "type": text_type,
        "enable_analyze": "1",
        "enable_fanfic": "0",
        "mode": "qt",
        "text": text
    }

    response = requests.post(url, headers=headers, data=data)
    result = response.json()

    if not result.get("success"):
        raise ValueError(f"Dịch thất bại: {result}")

    html_content = result.get("data", {}).get("content", "")
    plain_text = extract_text_with_linebreaks(html_content)

    return plain_text
