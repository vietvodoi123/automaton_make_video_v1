import os
import requests
from urllib.parse import urlparse

def download_file(url: str, save_dir: str = "downloads") -> str:
    os.makedirs(save_dir, exist_ok=True)
    file_name = os.path.basename(urlparse(url).path)
    path = os.path.join(save_dir, file_name)

    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(requests.get(url).content)

    return path
