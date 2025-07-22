import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, MediaFileUpload

# Khai báo scope để dùng Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_SECRET_FILE = "google_docs_oauth/client_secret.json"
TOKEN_FILE = "google_docs_oauth/token.json"

def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return build("drive", "v3", credentials=creds)

def get_or_create_subfolder(parent_folder_id: str, subfolder_name: str, drive_service) -> str:
    """
    Tìm hoặc tạo thư mục con trong thư mục cha theo tên
    """
    query = (
        f"mimeType='application/vnd.google-apps.folder' and "
        f"name='{subfolder_name}' and '{parent_folder_id}' in parents and trashed = false"
    )
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])

    if folders:
        return folders[0]["id"]

    metadata = {
        "name": subfolder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_folder_id]
    }
    folder = drive_service.files().create(body=metadata, fields="id").execute()
    return folder["id"]

def upload_to_drive(file_path: str, folder_id: str, story_title: str) -> str:
    """
    Upload file video vào Google Drive.
    - Tìm thư mục con theo tên truyện (`story_title`) trong `folder_id`.
    - Nếu chưa có thì tạo mới.
    - Upload file vào thư mục con.
    - Trả về link chia sẻ công khai.
    """
    drive_service = get_drive_service()

    # Tìm hoặc tạo thư mục theo tên truyện
    story_folder_id = get_or_create_subfolder(folder_id, story_title, drive_service)

    # Chuẩn bị metadata để upload
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [story_folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True, mimetype='video/mp4')

    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get("id")

    # Set quyền chia sẻ công khai
    drive_service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"}
    ).execute()

    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
