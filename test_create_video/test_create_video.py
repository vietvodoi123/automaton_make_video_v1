import textwrap
import subprocess
import tempfile

def parse_text_blocks(input_path, width=60):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    blocks = []
    current_block = []

    for line in lines:
        line = line.strip()
        if line == '':
            if current_block:
                blocks.append(current_block)
                current_block = []
        else:
            wrapped = textwrap.wrap(line, width=width)
            current_block.extend(wrapped)

    if current_block:
        blocks.append(current_block)

    return blocks


def create_drawtext_lines(blocks,
                          font_path='C\\:/Windows/Fonts/arial.ttf',
                          fontsize=32,
                          spacing=10,
                          video_height=720,
                          highlight_color='red',
                          normal_color='black',
                          start_time=0.0,
                          duration_per_line=0.6,
                          pause_between_blocks=0.3):
    drawtext_lines = []
    current_time = start_time

    for block in blocks:
        num_lines = len(block)
        line_height = fontsize + spacing
        total_block_height = num_lines * line_height
        base_y = f"(h/2)-{total_block_height / 2}"

        for i, line in enumerate(block):
            y_pos = f"{base_y}+{i * line_height}"
            highlight_start = current_time + i * duration_per_line
            highlight_end = highlight_start + duration_per_line

            # Dòng chữ màu đen (luôn hiển thị trừ khi đang được highlight)
            normal_drawtext = (
                f"drawtext=text='{line}':"
                f"fontfile='{font_path}':"
                f"fontsize={fontsize}:"
                f"fontcolor={normal_color}:"
                f"x=(w-text_w)/2:"
                f"y={y_pos}:"
                f"line_spacing={spacing}:"
                f"enable='lt(t,{highlight_start})+gt(t,{highlight_end})'"
            )
            drawtext_lines.append(normal_drawtext)

            # Dòng chữ màu đỏ (chỉ hiển thị trong thời gian highlight)
            highlight_drawtext = (
                f"drawtext=text='{line}':"
                f"fontfile='{font_path}':"
                f"fontsize={fontsize}:"
                f"fontcolor={highlight_color}:"
                f"x=(w-text_w)/2:"
                f"y={y_pos}:"
                f"line_spacing={spacing}:"
                f"enable='between(t,{highlight_start},{highlight_end})'"
            )
            drawtext_lines.append(highlight_drawtext)

        current_time += duration_per_line * num_lines + pause_between_blocks

    return drawtext_lines



def generate_video(input_txt='noidung.txt',
                   output_video='cuon_text.mp4',
                   resolution='1280x720',
                   duration=60,
                   width_wrap=60,
                   fontsize=32,
                   spacing=10):
    blocks = parse_text_blocks(input_txt, width=width_wrap)
    drawtext_filters = create_drawtext_lines(
        blocks,
        fontsize=fontsize,
        spacing=spacing,
        video_height=int(resolution.split('x')[1])
    )

    # Gắn nhãn đầu vào/đầu ra cho từng drawtext
    filter_lines = []
    prev = "[0:v]"
    for idx, drawtext in enumerate(drawtext_filters):
        label = f"[v{idx}]"
        filter_lines.append(f"{prev}{drawtext}{label}")
        prev = label

    # Đầu ra cuối cùng
    filter_lines.append(f"{prev}null[vidout]")

    # Ghi vào file .ffscript
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.ffscript', encoding='utf-8') as f:
        filter_script_path = f.name
        f.write(";\n".join(filter_lines))

    cmd = [
        'ffmpeg',
        '-y',
        '-f', 'lavfi',
        '-i', f"color=c=white:s={resolution}:d={duration}",
        '-filter_complex_script', filter_script_path,
        '-map', '[vidout]',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        output_video
    ]

    print("🎬 Đang tạo video, vui lòng chờ...")
    subprocess.run(cmd)
    print(f"✅ Đã tạo video: {output_video}")




# --- Chạy thử ---
if __name__ == "__main__":
    generate_video(
        input_txt='noidung.txt',
        output_video='cuon_text.mp4',
        resolution='1280x720',
        duration=120,
        width_wrap=60,
        fontsize=32,
        spacing=10
    )
