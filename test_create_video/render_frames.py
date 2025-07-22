import os
from PIL import Image, ImageDraw, ImageFont

def render_scrolling_text_frames(
    text_file='noidung_wrap.txt',
    output_dir='frames',
    image_size=(740, 380),
    font_path='C:/Windows/Fonts/arial.ttf',
    font_size=28,
    scroll_speed=60,  # pixel/giây
    fps=12
):
    width, height = image_size

    # Đảm bảo thư mục output tồn tại
    os.makedirs(output_dir, exist_ok=True)

    # Đọc nội dung text
    with open(text_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Tạo ảnh text đầy đủ
    font = ImageFont.truetype(font_path, font_size)
    line_spacing = 10
    line_height = font_size + line_spacing
    text_height = len(lines) * line_height

    full_img_height = text_height + height  # đủ để cuộn từ dưới lên

    full_img = Image.new('RGB', (width, full_img_height), color='white')
    draw = ImageDraw.Draw(full_img)

    y = height  # bắt đầu từ ngoài khung hình
    for line in lines:
        draw.text((50, y), line.strip(), font=font, fill='black')
        y += line_height

    # Tính tổng số frame
    total_scroll_pixels = text_height + height
    total_frames = int(total_scroll_pixels / scroll_speed * fps)

    for i in range(total_frames):
        frame = Image.new('RGB', (width, height), color='white')
        frame_y = int(i * scroll_speed / fps)
        crop_box = (0, frame_y, width, frame_y + height)
        frame.paste(full_img.crop(crop_box), (0, 0))
        frame.save(f"{output_dir}/frame_{i:05d}.png")

    print(f"✅ Đã render {total_frames} khung hình vào thư mục: {output_dir}")

if __name__ == "__main__":
    render_scrolling_text_frames()
