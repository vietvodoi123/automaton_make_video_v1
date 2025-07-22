import yaml

def load_yaml_settings(file_path: str = r"D:\py_prj\automation_video_1\config\settings.yaml") -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
