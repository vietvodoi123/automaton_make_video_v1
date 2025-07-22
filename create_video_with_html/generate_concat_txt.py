import os
import subprocess
import json
def get_audio_duration(mp3_path):
    """
    Lấy độ dài file mp3 bằng ffprobe (không cần audioop hay pydub).
    """
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        mp3_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = json.loads(result.stdout)
    duration = float(info["format"]["duration"])
    return duration

def generate_concat_file_by_audio_duration(input_file="data.txt",
                         frame_dir="frames",
                         output_path="concat.txt",
                         mp3_path=None,
                         pause_duration=0.3):
    """
    Sinh file concat.txt để dùng cho FFmpeg từ dữ liệu text và ảnh frame.

    Parameters:
    - input_file (str): File chứa các dòng text
    - frame_dir (str): Thư mục chứa ảnh PNG
    - output_path (str): Đường dẫn file concat.txt đầu ra
    - mp3_path (str): (Tuỳ chọn) Nếu truyền vào, sẽ dùng độ dài file mp3 để phân chia thời lượng
    - pause_duration (float): Thời gian dừng cho mỗi dòng trắng (nếu không dùng mp3, đơn vị giây)
    """

    # Đọc các dòng văn bản
    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]

    # Danh sách ảnh
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".png")])
    total_frames = len(frame_files)

    # Lấy độ dài file mp3 nếu có
    if mp3_path:
        total_audio_duration = get_audio_duration(mp3_path)
        print(f"🎧 File audio dài {round(total_audio_duration, 2)} giây")
    else:
        total_audio_duration = None

    concat_lines = []
    frame_index = 0

    # Tính tổng "độ nặng" của từng dòng nếu dùng mp3
    line_weights = []
    total_weight = 0

    for line in lines:
        if not line:
            weight = pause_duration  # nếu là dòng trắng
        else:
            word_count = len(line.split())
            bonus = 0
            bonus += line.count('.') * 0.4
            bonus += line.count(',') * 0.25
            bonus += line.count('?') * 0.4
            bonus += line.count('!') * 0.4
            bonus += line.count('…') * 0.6
            weight = word_count + bonus
        line_weights.append(weight)
        total_weight += weight

    for i, line in enumerate(lines):
        if frame_index >= total_frames:
            print(f"⚠️ Không đủ frame cho dòng: {line}")
            break

        # Phân chia thời lượng dựa vào trọng số
        if total_audio_duration:
            proportion = line_weights[i] / total_weight
            duration = round(total_audio_duration * proportion, 3)
        else:
            if not line:
                duration = pause_duration
            else:
                word_count = len(line.split())
                bonus = 0
                bonus += line.count('.') * 0.4
                bonus += line.count(',') * 0.25
                bonus += line.count('?') * 0.4
                bonus += line.count('!') * 0.4
                bonus += line.count('…') * 0.6
                duration = round(word_count * 0.246 + bonus, 3)

        filepath = os.path.join(frame_dir, frame_files[frame_index])
        concat_lines.append(f"file '{filepath}'")
        concat_lines.append(f"duration {duration}")
        frame_index += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(concat_lines))

    print(f"✅ Đã tạo {output_path} với {frame_index} frame và chia thời lượng phù hợp.")
    return output_path

def generate_concat_file_seconds_per_word(input_file="data.txt",
                         frame_dir="frames",
                         output_path=".",
                         seconds_per_word=0.246,
                         pause_duration=0.3):
    """
    Sinh file concat.txt để dùng cho FFmpeg từ dữ liệu text và ảnh frame.

    Parameters:
    - task_id (str): Tên định danh dùng để đặt tên file đầu ra (vd: abc -> abc_concat.txt)
    - input_file (str): File chứa các dòng text (dạng từng dòng một)
    - frame_dir (str): Thư mục chứa ảnh PNG (frames)
    - output_dir (str): Thư mục để ghi file output
    - seconds_per_word (float): Thời gian đọc trung bình mỗi từ
    - pause_duration (float): Thời gian dừng cho mỗi dòng trắng
    """

    # Đọc file văn bản
    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]

    # Lấy danh sách ảnh frame
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".png")])

    concat_lines = []
    buffer = 0
    frame_index = 0

    for line in lines:
        if not line:  # dòng trắng
            buffer += pause_duration
            continue

        base_time = len(line.split()) * seconds_per_word

        # Thêm thời gian dựa trên dấu câu
        bonus = 0
        bonus += line.count('.') * 0.4
        bonus += line.count(',') * 0.25
        bonus += line.count('?') * 0.4
        bonus += line.count('!') * 0.4
        bonus += line.count('…') * 0.6

        duration = base_time + bonus + buffer

        duration = round(duration, 4)
        if frame_index >= len(frame_files):
            print(f"⚠️ Không đủ frame cho dòng: {line}")
            break

        filename = frame_files[frame_index]
        filepath = os.path.join(frame_dir, filename)

        concat_lines.append(f"file '{filepath}'")
        concat_lines.append(f"duration {duration}")

        frame_index += 1
        buffer = 0

    # Đường dẫn đầu ra
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(concat_lines))

    print(f"✅ Đã tạo {output_path} với {frame_index} frame được gắn thời lượng.")
    return output_path

def generate_concat_file_balanced(input_file, frame_dir, output_path,mp3_path):

    # Đọc văn bản
    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".png")])
    assert len(lines) <= len(frame_files), "⚠️ Không đủ frame cho số dòng text!"

    # Tính trọng số cho từng dòng
    weights = []
    for line in lines:
        word_count = len(line.split())
        bonus = (
            line.count('.') * 0.4 +
            line.count(',') * 0.25 +
            line.count('?') * 0.4 +
            line.count('!') * 0.4 +
            line.count('…') * 0.6
        )
        weight = word_count + bonus
        weights.append(weight)

    total_weight = sum(weights)
    audio_duration = get_audio_duration(mp3_path)

    # Gán thời lượng đúng theo tỉ lệ
    concat_lines = []
    used_duration = 0
    for i, line in enumerate(lines):
        proportion = weights[i] / total_weight
        # Dòng cuối cùng lấy phần còn lại (tránh sai số làm tràn)
        if i == len(lines) - 1:
            duration = round(audio_duration - used_duration, 3)
        else:
            duration = round(audio_duration * proportion, 3)
            used_duration += duration

        filepath = os.path.join(frame_dir, frame_files[i])
        concat_lines.append(f"file '{filepath}'")
        concat_lines.append(f"duration {duration}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(concat_lines))

    print(f"✅ Đã tạo {output_path} với thời lượng khớp chính xác {round(audio_duration, 2)}s.")
