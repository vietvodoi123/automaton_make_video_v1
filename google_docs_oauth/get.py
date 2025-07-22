import re
from .uploader import get_services
def get_doc_content_from_url(doc_url: str) -> str:
    """
    Trích xuất nội dung từ Google Docs bằng URL.
    """
    # Bước 1: Lấy doc_id từ URL
    match = re.search(r"/document/d/([a-zA-Z0-9-_]+)", doc_url)
    if not match:
        raise ValueError("Không tìm thấy doc_id trong URL.")
    doc_id = match.group(1)

    # Bước 2: Gọi API để lấy nội dung
    _, docs_service = get_services()
    doc = docs_service.documents().get(documentId=doc_id).execute()

    # Bước 3: Trích xuất văn bản từ body
    content = doc.get("body", {}).get("content", [])
    text_parts = []
    for element in content:
        paragraph = element.get("paragraph")
        if paragraph:
            for elem in paragraph.get("elements", []):
                text_run = elem.get("textRun")
                if text_run:
                    text_parts.append(text_run.get("content", ""))

    return "".join(text_parts).strip()
