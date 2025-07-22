from openai import OpenAI
import os
import json

def translate_and_summarize_chinese_to_vietnamese(text_chinese: str) -> dict:
    """
    Dịch và tóm tắt văn bản tiếng Trung sang tiếng Việt.
    Trả về dict với 2 khóa: 'translation' và 'summary'.
    """
    # Khởi tạo client với API key từ tham số hoặc biến môi trường
    client = OpenAI()

    # Tạo prompt
    system_prompt = (
        "Bạn là một AI dịch thuật từ tiếng Trung sang tiếng Việt một cách chính xác và tự nhiên. "
        "Khi được cung cấp một đoạn văn bản tiếng Trung, bạn sẽ:\n"
        "1) Hãy dịch **toàn bộ** nội dung gốc sang tiếng Việt (đừng bỏ sót).\n"
        "2) Sau khi dịch xong, hãy tóm tắt nội dung đó trong một đoạn ngắn.\n\n"
        "Trả về kết quả dưới định dạng JSON như sau:\n"
        "{\n"
        '  "translation": "<bản dịch tiếng Việt>",\n'
        '  "summary": "<tóm tắt nội dung bằng tiếng Việt>"\n'
        "}\n"
    )

    # Gửi request
    resp = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",  # hoặc "gpt-4.1-nano"
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text_chinese}
        ],
        temperature=0.3,
        max_tokens=32768
    )

    # Lấy nội dung text trả về
    content = resp.choices[0].message.content.strip()

    # Chuyển chuỗi JSON thành dict
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        # Nếu model không trả đúng JSON, bạn có thể parse thủ công hoặc raise lỗi
        raise ValueError(f"Không parse được JSON từ response:\n{content}")

    return result

def summarized_by_gpt(text:str):
    client = OpenAI()
    system_prompt = (
        "Bạn là một AI chuyên tóm tắt các đoạn văn bản. "
        "Khi được cung cấp một đoạn văn bản bạn sẽ:\n"
        "**Tóm tắt** ngắn gọn nội dung đó trong một đoạn ngắn.\n\n"
        "Trả về kết quả dưới định dạng JSON như sau:\n"
        "{\n"
        '  "summary": "<tóm tắt nội dung bằng tiếng Việt>"\n'
        "}\n"
    )
    resp = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",  # hoặc "gpt-4.1-nano"
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.3,
        max_tokens=32768
    )

    # Lấy nội dung text trả về
    content = resp.choices[0].message.content.strip()

    # Chuyển chuỗi JSON thành dict
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        # Nếu model không trả đúng JSON, bạn có thể parse thủ công hoặc raise lỗi
        raise ValueError(f"Không parse được JSON từ response:\n{content}")

    return result