from openai import OpenAI
import os
import json


from openai import OpenAI
import json
from typing import Any, Dict

def chinh_sua_ban_dich(prompt_id: str, raw_text: str, prompt_version: str = "8") -> Dict[str, Any]:
    """
    Gọi prompt đã lưu (Playground) qua prompt_id, truyền biến raw_text.
    Trả về dict Python: {"ban_dich_da_chinh_sua": ..., "tom_tat_nhanh": ...}
    """
    client = OpenAI()

    response = client.responses.create(
        model="gpt-5-nano-2025-08-07",
        prompt={
            "id": prompt_id,
            "version": prompt_version,
            "variables": {
                "raw_text": raw_text
            }
        },
        # nếu cần đảm bảo model trả JSON, giữ json_object
        text={"format": {"type": "json_object"}},
        # thêm 1 input ngắn (không bắt buộc nếu prompt trong Playground đã có chữ "JSON")
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Please respond in JSON format."}
                ]
            }
        ]
    )

    # Thường thì SDK sẽ có output_parsed khi format=json_object
    if getattr(response, "output_parsed", None):
        return response.output_parsed

    # fallback: lấy raw text và cố parse JSON
    raw = getattr(response, "output_text", None) or ""
    raw = raw.strip()
    try:
        return json.loads(raw)
    except Exception:
        # nếu không parse được JSON, trả về raw để debug
        return {"error": "Không parse được JSON từ model", "raw_output": raw, "full_response": str(response)}



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

import json
import re

def fix_broken_json(s: str) -> str:
    """
    Cố gắng sửa JSON bị lỗi do model trả về.
    """
    # Cắt phần thừa sau dấu }
    if "}" in s:
        s = s[:s.rfind("}")+1]

    # Loại bỏ dấu phẩy thừa trước }
    s = re.sub(r",\s*}", "}", s)

    # Đảm bảo key được bọc trong dấu "
    s = re.sub(r"(\w+):", r'"\1":', s)

    return s.strip()

def summarized_by_gpt(text: str):
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
        model="gpt-4.1-nano-2025-04-14",  # thử gpt-4.1-mini ổn định hơn
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.3,
        max_tokens=2048,
        response_format={"type": "json_object"}
    )

    content = resp.choices[0].message.content.strip()
    if not content:
        raise ValueError("⚠️ API trả về nội dung rỗng!")

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Vá JSON rồi parse lại
        fixed = fix_broken_json(content)
        try:
            return json.loads(fixed)
        except Exception:
            raise ValueError(f"⚠️ Không parse được JSON từ response:\n{content}")




