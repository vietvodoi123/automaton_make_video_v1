# config.py
import os

# Đường dẫn tuyệt đối tới thư mục tmp
PROJECT_ROOT = os.getcwd()
TMP_DIR = os.path.join(PROJECT_ROOT, "tmp")

# Đảm bảo thư mục tmp tồn tại
os.makedirs(TMP_DIR, exist_ok=True)
