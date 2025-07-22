import textwrap

def wrap_text_file(input_path, output_path, width=60):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    wrapped_lines = []
    for line in lines:
        line = line.strip()
        if line == '':
            wrapped_lines.append('')
        else:
            wrapped_lines.extend(textwrap.wrap(line, width=width))

    with open(output_path, 'w', encoding='utf-8') as f:
        for l in wrapped_lines:
            f.write(l + '\n')

wrap_text_file('noidung.txt', 'noidung_wrap.txt', width=48)
# 740x380

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

    return blocks  # List[List[str]]

def create_drawtext_lines(blocks, fontsize=32, spacing=10, video_height=720, start_time=0.0, duration_per_line=0.6, pause_between_blocks=0.3):
    drawtext_lines = []
    current_time = start_time

    for block in blocks:
        num_lines = len(block)
        total_block_height = num_lines * (fontsize + spacing)
        base_y = f"(h/2)-{total_block_height/2}"

        for i, line in enumerate(block):
            y_pos = f"{base_y}+{i * (fontsize + spacing)}"
            highlight_expr = f"if(between(t,{current_time},{current_time + duration_per_line * num_lines}), red, black)"

            drawtext = (
                f"drawtext=text='{line}':"
                f"fontfile='C\\:/Windows/Fonts/arial.ttf':"
                f"fontsize={fontsize}:"
                f"fontcolor_expr='{highlight_expr}':"
                f"x=(w-text_w)/2:"
                f"y={y_pos}:"
                f"line_spacing={spacing}"
            )
            drawtext_lines.append(drawtext)

        current_time += duration_per_line * num_lines + pause_between_blocks

    return drawtext_lines
