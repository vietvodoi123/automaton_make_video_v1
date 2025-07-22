import random
import re

def normalize_colon(text: str) -> str:
    # Chuẩn hóa dấu hai chấm Unicode đặc biệt thành dấu chuẩn ":"
    return text.replace("：", ":")

def add_intro_and_comments(text: str, intro1: str, intro2: str, comments: list[str]) -> str:
    print("COMMENTS:", comments)
    intro_block = f"{intro1.strip()}\n\n{intro2.strip()}\nChúng ta bắt đầu vào nghe truyện nhé! Chúc các bạn nghe truyện vui vẻ"

    text = normalize_colon(text)
    lines = text.split("\n")
    insert_positions = []

    # ✅ Xác định vị trí sau dòng có dấu hai chấm
    for i in range(len(lines)):
        if lines[i].strip().endswith(":"):
            insert_positions.append(i + 1)

    print("DEBUG insert_positions:", insert_positions)

    if not insert_positions:
        return intro_block + "\n\n" + "\n".join(lines)

    # ✅ Rải đều comment vào các vị trí chèn
    step = len(insert_positions) / len(comments)
    selected_indices = [round(i * step) for i in range(len(comments))]
    selected_positions = [insert_positions[i] for i in selected_indices if i < len(insert_positions)]

    for idx, comment in sorted(zip(selected_positions, comments), reverse=True):
        lines.insert(idx, f"({comment.strip()})")

    return intro_block + "\n\n" + "\n".join(lines)


