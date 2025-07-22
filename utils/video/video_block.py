import os
import numpy as np
from moviepy.video.fx.Loop import Loop
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip,TextClip,ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx import MaskColor

def create_rect_with_border(
    size=(200, 400),
    bg_color=(255, 255, 255),
    border_color=(0, 0, 0),
    border_width=5,
    opacity=1,
    duration=10
):
    w, h = size
    img = np.zeros((h, w, 3), dtype=np.uint8)

    # Viền
    img[:, :] = border_color

    # Bên trong
    img[border_width:h-border_width, border_width:w-border_width] = bg_color

    return ImageClip(img).with_duration(duration).with_opacity(opacity)

def create_text_block_with_background(
    text: str,
    size: tuple,
    font_path: str,
    font_size: int,
    bg_color=(33, 36, 41),
    border_color=(173, 182, 189),
    border_width=3,
    opacity=0.7,
    text_color="black",
    duration=10
):
    """
    Tạo khối nội dung với chữ nằm giữa, nền có viền và độ trong suốt.
    """
    w, h = size

    # 1. Nền với viền
    bg_clip = create_rect_with_border(
        size=size,
        bg_color=bg_color,
        border_color=border_color,
        border_width=border_width,
        opacity=opacity,
        duration=duration
    )

    # 2. Text nằm giữa
    text_clip = TextClip(
        text=text,
        font=font_path,
        font_size=font_size,
        color=text_color,
        size=(int(w * 0.9), int(h * 0.9)),  # chừa margin
        method='caption',
        text_align='center'
    ).with_duration(duration)

    # 3. Tính toán vị trí để canh giữa
    tw, th = text_clip.size
    text_pos = ((w - tw) // 2, (h - th) // 2)

    # 4. Gộp lại thành một block
    block = CompositeVideoClip(
        [bg_clip, text_clip.with_position(text_pos)],
        size=size
    ).with_duration(duration)

    return block
def create_video_with_overlay(
    background_path: str,
    output_path: str,
    mc_video_path:str,
    episode_text:str="Tập 1",
    tag_title:str="Truyện hay 2025",
    type_title:str="Huyền huyễn - Tu tiên",
    name_title_1:str="Thiên Ma Biến",
    name_title_2:str="Truyền nhân ma đạo",
    donate_info="Ủng hộ tại: momo/zalo...",
    audio_path: str = None,
    resolution: tuple = (1280, 720),
    fps: int = 24,
    font_path: str = r"D:\py_prj\tu_dong_hoa\font\static\Roboto-ExtraBoldItalic.ttf"
):
    duration = AudioFileClip(audio_path).duration
    # global
    h = 720
    w = 1280
    padding = 30

    # content
    h_c = int((h-2*padding) / 5)
    w_c = int(w-2*padding)

    #tag
    w_tag = int((w - 2 * padding) / 5)
    h_tag = int(h_c/3)

    #name1
    h_name1 = int((h-2*padding)-padding-h_c / 3)
    #name2
    h_name2 = int(3*h_c/4)

    # 1. Background + làm mờ nhẹ
    background = (
        ImageClip(background_path)
        .with_duration(duration)
        .resized(resolution)
        .with_opacity(0.9)  # làm mờ
    )
    #tag
    tag_block = create_text_block_with_background(
        text=tag_title,
        size=(w_tag, h_tag),
        font_path=font_path,
        font_size=20,
        text_color="white",
        duration=duration
    ).with_position((padding, padding))

    # type
    type_block = create_text_block_with_background(
        text=type_title,
        size=(w_c - padding - w_tag, h_tag),
        font_path=font_path,
        font_size=20,
        text_color="white",
        duration=duration
    ).with_position((padding+padding + w_tag, padding))

    # name1
    name_1_block = create_text_block_with_background(
        text=name_title_1.replace(" ", "\n\n"),
        size=(w_tag, h_name1),
        font_path=font_path,
        font_size=80,
        text_color="white",
        duration=duration
    ).with_position((padding, 2*padding + h_tag))

    #name 2
    name_2_block = create_text_block_with_background(
        text=name_title_2,
        size=(w_c-padding-w_tag, h_name2),
        font_path=font_path,
        font_size=60,
        text_color="white",
        duration=duration
    ).with_position((padding+padding +w_tag, 2 * padding + h_tag))

    mc_clip = (
        VideoFileClip(mc_video_path).resized(height=h_name1-h_name2)
        .with_position((3 * padding + w_tag, 2 * padding + h_tag)).with_duration(4.5)
    )

    mc_clip_looped = Loop(duration).apply(mc_clip).with_duration(duration).resized(1.5)
    remove_green = MaskColor(color=(0, 255, 0), threshold=80, stiffness=3).copy()
    mc_clip_final = remove_green.apply(mc_clip_looped)

    #episode_text
    episode_text_block = create_text_block_with_background(
        text=episode_text,
        size=(int(w_tag*1.5), int(1.5*h_name2)),
        font_path=font_path,
        font_size=80,
        text_color="white",
        duration=duration
    ).with_position((w_c-int(w_tag*1.5) +padding, 3 * padding + h_tag + h_name2))

    # donate infor
    donate_info_block = create_text_block_with_background(
        text=donate_info,
        size=(int(w_tag*1.5), int(2.7*h_name2)),
        font_path=font_path,
        font_size=20,
        text_color="white",
        duration=duration
    ).with_position((w_c-int(w_tag*1.5) +padding, 4 * padding + h_tag + h_name2 + int(1.5*h_name2)))

    clips = [background, tag_block, type_block, name_1_block,name_2_block,mc_clip_final,episode_text_block,donate_info_block]
    final = CompositeVideoClip(clips, size=resolution)
    if audio_path:
        final = final.with_audio(AudioFileClip(audio_path))
    final.write_videofile(output_path, fps=fps)

    mc_clip.close()
