from sheets.sheet_utils import get_gspread_client

SHEET_NAME = "Channel"  # Tên sheet chứa thông tin channel

COLUMNS = ["channel_id", "name", "subscriber", "avatar_url", "donate_info","notification", "mc_path", "mc_name", "mc_intro", "comments", "voice"]

class ChannelSheet:
    def __init__(self, spreadsheet_id: str, credentials_path: str = "config/credentials.json"):
        self.client = get_gspread_client(credentials_path)
        self.sheet = self.client.open_by_key(spreadsheet_id).worksheet(SHEET_NAME)

    def get_all_channels(self) -> list[dict]:
        records = self.sheet.get_all_records()
        return [
            {
                col: row.get(col, "").strip() if isinstance(row.get(col), str) else row.get(col)
                for col in COLUMNS
            }
            for row in records
        ]

    def get_channel_by_id(self, channel_id: str) -> dict | None:
        """
        Truy vấn channel theo id. Trả về dict nếu tìm thấy, None nếu không.
        """
        records = self.sheet.get_all_records()
        for row in records:
            if str(row.get("channel_id", "")).strip() == channel_id:
                return {
                    col: row.get(col, "").strip() if isinstance(row.get(col), str) else row.get(col)
                    for col in COLUMNS
                }
        return None
