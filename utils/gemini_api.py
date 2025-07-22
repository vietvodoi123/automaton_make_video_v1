import google.generativeai as genai
from utils.yaml_loader import load_yaml_settings

def get_gemini_model(model_name="models/gemini-1.5-flash"):
    settings = load_yaml_settings()
    api_key = settings.get("gemini_api_key")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in settings.yaml")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

def refine_translation(chinese_text: str, raw_translation: str) -> str:
    model = get_gemini_model()
    prompt = f"""
Bạn là một biên tập viên tiếng Việt chuyên chỉnh sửa bản dịch truyện tiên hiệp từ tiếng Trung.

Dưới đây là một đoạn văn gốc tiếng Trung và bản dịch máy sang tiếng Việt. Hãy:
- Sửa các câu dịch sai nghĩa, cứng nhắc hoặc không tự nhiên.
- Dịch lại các từ/đoạn tiếng Trung còn sót lại chưa được dịch (nếu có).
- Giữ văn phong truyện tiên hiệp, không thêm chú thích hoặc nhận xét.
- Trả về bản dịch đã hiệu đính hoàn chỉnh.

### Văn bản gốc (tiếng Trung gốc):
{chinese_text}

### Bản dịch máy:
{raw_translation}

### Bản dịch sau khi hiệu đính:
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Có lỗi xảy ra khi dịch văn bản: {e}")
        return ""


# ✨ HÀM TÓM TẮT VĂN BẢN (khoảng 15% nội dung gốc)
def summarize_text(text: str) -> str:
    model = get_gemini_model()
    prompt = f"""
Tôi có một đoạn truyện sau. Hãy tóm tắt nó với độ dài khoảng 20% độ dài gốc. Chỉ ghi nội dung chính và ngắn gọn, giữ mạch truyện liền lạc, không thêm nhận xét hay chú thích.

### Nội dung:
{text}

### Tóm tắt:
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Lỗi khi tóm tắt văn bản: {e}")
        return ""

# 📚 HÀM TÓM TẮT TOÀN BỘ - ĐỆ QUY NHIỀU BƯỚC
def recursive_summary(summaries: list[str], max_chunk_size=5) -> str:
    """
    Nhận vào danh sách các bản tóm tắt chương, tóm gọn chúng thành một bản tóm tắt cuối cùng.
    Quá trình tóm tắt nhiều bước nếu có > max_chunk_size phần.
    """
    if not summaries:
        return ""

    model = get_gemini_model()

    # Nếu số lượng nhỏ hơn max_chunk_size, gộp và tóm tắt 1 lần duy nhất
    if len(summaries) <= max_chunk_size:
        prompt = f"""
Tôi có một số đoạn tóm tắt truyện. Hãy gộp nội dung và tóm tắt thành một đoạn gọn gàng, ngắn gọn, dễ hiểu. Không thêm bình luận hay tiêu đề.

### Các tóm tắt chương:
{'\n\n'.join(summaries)}

### Tóm tắt cuối cùng:
"""
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Lỗi khi tóm tắt tất cả: {e}")
            return ""

    # Nếu dài hơn, chia nhỏ rồi tóm tắt từng nhóm
    print(f"🔁 Tóm tắt theo nhóm {max_chunk_size}...")
    grouped_summaries = [
        summaries[i:i + max_chunk_size]
        for i in range(0, len(summaries), max_chunk_size)
    ]

    intermediate_summaries = []
    for idx, group in enumerate(grouped_summaries):
        print(f"📚 Đang tóm tắt nhóm {idx + 1}/{len(grouped_summaries)}...")
        group_summary = recursive_summary(group, max_chunk_size)
        intermediate_summaries.append(group_summary)

    # Đệ quy tiếp tục trên các bản tóm tắt trung gian
    return recursive_summary(intermediate_summaries, max_chunk_size)
