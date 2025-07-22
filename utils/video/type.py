from dataclasses import dataclass
from typing import List

@dataclass
class VideoInput:
    episode_text: str
    tag_title: str
    type_title: str
    name_title_1: str
    name_title_2: str
    donate_info: str
    background_url: str
    mc_id: str
    audio_urls: List[str]
    output_path: str
    duration: int = 10
    resolution: tuple = (1280, 720)
    fps: int = 24
