import requests

def call_tts_api(params: str, cookies: str) -> str:
    """Gửi request với params đã mã hóa, trả về response text"""
    url = "https://freetts.com/text-to-speech"

    headers = {
        "accept": "text/x-component",
        "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.6,en;q=0.5",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://freetts.com",
        "referer": "https://freetts.com/text-to-speech",
        "user-agent": "Mozilla/5.0",
        "next-action": "f6a37f3b9ffdb01ba2da16f264fdabab4a254f61",
        "next-router-state-tree": "[\"\",{\"children\":[\"(functions)\",{\"children\":[\"text-to-speech\",{\"children\":[\"__PAGE__\",{},\"/text-to-speech\",\"refresh\"]}]}]},null,null,true]",
        "cookie": cookies,  # copy từ DevTools
    }

    body = [{"params": params}]
    res = requests.post(url, headers=headers, json=body)

    return res.text
