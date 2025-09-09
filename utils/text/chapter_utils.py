import re
from typing import Any, Iterable

def to_text(obj: Any) -> str:
    """
    Chuyển mọi kiểu obj thành chuỗi văn bản hợp lý.
    - str -> giữ nguyên
    - list/tuple -> nối các phần tử con (đệ quy)
    - dict -> nếu có key phổ biến thì lấy giá trị; ngược lại json-like str
    """
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, (list, tuple, set)):
        parts = []
        for item in obj:
            parts.append(to_text(item))
        # lọc các phần rỗng, join bằng 2 newlines (vừa readable)
        return "\n\n".join([p for p in parts if p])
    if isinstance(obj, dict):
        # một số dict trả về từ API có key kiểu 'ban_dich_da_chinh_sua' hoặc 'text'...
        for k in ("ban_dich_da_chinh_sua", "text", "content", "output_text", "message"):
            if k in obj and obj[k]:
                return to_text(obj[k])
        # fallback: nối mọi giá trị của dict
        vals = [to_text(v) for v in obj.values()]
        return "\n\n".join([v for v in vals if v])
    # fallback generic
    try:
        return str(obj)
    except Exception:
        return ""

def normalize_whitespace(text: str) -> str:
    text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)  # trim đầu/cuối từng dòng
    text = re.sub(r'[ \t]+', ' ', text)    # nhiều space -> 1 space
    text = re.sub(r' *\n *', '\n', text)   # trim trước/sau newline
    return text

def collapse_blank_lines(text: str, max_blank=2) -> str:
    return re.sub(r'\n{'+str(max_blank+1)+r',}', '\n'*max_blank, text)

def remove_consecutive_duplicate_lines(text: str) -> str:
    lines = text.splitlines()
    out = []
    prev = None
    for ln in lines:
        if prev is not None and ln.strip() == prev.strip():
            continue
        out.append(ln)
        prev = ln
    return "\n".join(out)

def clean_chapter_text(title_translated: str, chapter_text: Any) -> str:
    """
    Chuẩn hoá 1 chương (an toàn với nhiều kiểu đầu vào).
    - title_translated: tiêu đề đã dịch (dùng để loại trừ duplication ở đầu)
    - chapter_text: str | list | dict | ...
    Trả về string sạch đã chuẩn hoá.
    """
    # 1) chuyển về str an toàn
    t = to_text(chapter_text).strip()

    # 2) nếu bắt đầu bằng tiêu đề đã dịch thì loại bỏ
    if title_translated:
        title_snippet = to_text(title_translated).strip()
        if title_snippet:
            pattern = r'^\s*' + re.escape(title_snippet) + r'(\s*[:\-\–\—]?\s*|\n+)'
            t = re.sub(pattern, '', t, flags=re.IGNORECASE)

    # 3) normalize + remove dupes + collapse blank lines
    t = normalize_whitespace(t)
    t = remove_consecutive_duplicate_lines(t)
    t = collapse_blank_lines(t, max_blank=2)
    return t.strip()
