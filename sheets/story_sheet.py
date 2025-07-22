# sheets/story_sheet.py

from sheets.sheet_utils import get_gspread_client

SHEET_NAME = "Stories"  # Tên sheet của bạn

COLUMNS = [
    "story_id", "title", "channel_id","description","type",
    "background_url", "parser_type", "url_list_page",
    "css_chapter_links", "css_title", "css_content", "css_next",
    "quantity_per_task", "status"
]

class StorySheet:
    def __init__(self, spreadsheet_id: str, credentials_path: str = "config/credentials.json"):
        self.client = get_gspread_client(credentials_path)
        self.sheet = self.client.open_by_key(spreadsheet_id).worksheet(SHEET_NAME)

    def get_new_stories(self) -> list[dict]:
        records = self.sheet.get_all_records()
        new_stories = []
        for row in records:
            if str(row.get("status", "")).strip().upper() == "NEW":
                story = {col: row.get(col, "").strip() if isinstance(row.get(col), str) else row.get(col) for col in COLUMNS}
                new_stories.append(story)
        return new_stories

    def update_story_status(self, story_id: str, new_status: str):
        records = self.sheet.get_all_records()
        for idx, row in enumerate(records):
            if row.get("story_id") == story_id:
                cell_row = idx + 2  # +2 vì get_all_records bỏ qua header, và index bắt đầu từ 1
                self.sheet.update_cell(cell_row, COLUMNS.index("status") + 1, new_status.upper())
                break

    def get_story_by_id(self, story_id: str) -> dict | None:
        """
        Trả về thông tin truyện theo story_id. Nếu không tìm thấy thì trả về None.
        """
        records = self.sheet.get_all_records()
        for row in records:
            if str(row.get("story_id", "")).strip() == story_id:
                return {
                    col: row.get(col, "").strip() if isinstance(row.get(col), str) else row.get(col)
                    for col in COLUMNS
                }
        return None