import json
from sheets.sheet_utils import get_gspread_client

SHEET_NAME = "Tasks"

TASK_COLUMNS = [
    "task_id", "story_id",
    "chapter_from", "chapter_to", "url_chapters",
    "status", "translated",
    "css_title", "css_content", "css_next",
    "doc_url","audio_urls", "video_path","summary"
]

class TaskSheet:
    def __init__(self, spreadsheet_id: str, credentials_path: str = "config/credentials.json"):
        self.client = get_gspread_client(credentials_path)
        self.sheet = self.client.open_by_key(spreadsheet_id).worksheet(SHEET_NAME)

    def append_task(self, task_data: dict):
        row = []
        for col in TASK_COLUMNS:
            value = task_data.get(col, "")
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            row.append(value)
        self.sheet.append_row(row, value_input_option="USER_ENTERED")

    def append_tasks(self, list_of_tasks: list[dict]):
        rows = []
        for task_data in list_of_tasks:
            row = []
            for col in TASK_COLUMNS:
                value = task_data.get(col, "")
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                row.append(value)
            rows.append(row)
        self.sheet.append_rows(rows, value_input_option="USER_ENTERED")

    def get_all_tasks(self) -> list[dict]:
        return self.sheet.get_all_records()

    def find_row(self, column_name: str, value: str) -> tuple[int, dict]:
        """Tìm hàng đầu tiên mà column = value. Trả về (index, row_data)"""
        all_rows = self.get_all_tasks()
        for idx, row in enumerate(all_rows):
            if str(row.get(column_name, "")).strip() == str(value).strip():
                return idx + 2, row  # +2 vì hàng tiêu đề là 1
        raise ValueError(f"Không tìm thấy task có {column_name} = {value}")

    def update_row(self, row_index: int, updates: dict):
        """Cập nhật các cột được chỉ định tại dòng `row_index` (bắt đầu từ 1)"""
        for col_name, new_value in updates.items():
            if col_name not in TASK_COLUMNS:
                continue
            col_idx = TASK_COLUMNS.index(col_name) + 1
            if isinstance(new_value, (dict, list)):
                new_value = json.dumps(new_value, ensure_ascii=False)
            self.sheet.update_cell(row_index, col_idx, new_value)

    def update_task_status(self, task_id: str, status: str, extra_updates: dict = None):
        """Cập nhật trạng thái và các trường khác (nếu có) cho task theo task_id"""
        row_idx, _ = self.find_row("task_id", task_id)
        updates = {"status": status}
        if extra_updates:
            updates.update(extra_updates)
        self.update_row(row_idx, updates)

    def get_task_by_id(self, task_id: str) -> dict:
        _, task_data = self.find_row('task_id', task_id)
        return task_data
