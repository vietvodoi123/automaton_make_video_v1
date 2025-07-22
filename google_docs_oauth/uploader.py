import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from utils import load_yaml_settings

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive"
]

CLIENT_SECRET_FILE = "google_docs_oauth/client_secret.json"
TOKEN_FILE = "google_docs_oauth/token.json"


def get_services():
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

    drive_service = build("drive", "v3", credentials=creds)
    docs_service = build("docs", "v1", credentials=creds)
    return drive_service, docs_service


def get_or_create_subfolder(parent_folder_id: str, subfolder_name: str, drive_service) -> str:
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


def create_or_update_doc(folder_id: str, doc_title: str, content: str, drive_service, docs_service):
    query = (
        f"mimeType='application/vnd.google-apps.document' and "
        f"name='{doc_title}' and '{folder_id}' in parents and trashed = false"
    )
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])

    if files:
        doc_id = files[0]["id"]
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={
                "requests": [
                    {"deleteContentRange": {"range": {"startIndex": 1, "endIndex": 1_000_000}}},
                    {"insertText": {"location": {"index": 1}, "text": content}}
                ]
            }
        ).execute()
        return doc_id
    else:
        metadata = {
            "name": doc_title,
            "mimeType": "application/vnd.google-apps.document",
            "parents": [folder_id]
        }
        file = drive_service.files().create(body=metadata, fields="id").execute()
        doc_id = file["id"]
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]}
        ).execute()
        return doc_id


def save_translated_task(story_title: str, task_id: str, translated_text: str) -> str:
    """
    Lưu task đã dịch vào Google Docs như sau:
    - Trong thư mục chính (từ settings.yaml), tạo thư mục con theo `story_title`
    - Trong đó, lưu file docs tên `task_id`
    Trả về URL tài liệu Google Docs
    """
    settings = load_yaml_settings("config/settings.yaml")
    root_folder_id = settings.get("GOOGLE_DRIVE_FOLDER_ID")
    if not root_folder_id:
        raise ValueError("GOOGLE_DRIVE_FOLDER_ID không tồn tại trong settings.yaml")

    drive_service, docs_service = get_services()

    # Tạo/thấy folder con theo tên truyện
    story_folder_id = get_or_create_subfolder(root_folder_id, story_title, drive_service)

    # Lưu docs theo tên task_id trong thư mục truyện
    doc_id = create_or_update_doc(story_folder_id, task_id, translated_text, drive_service, docs_service)
    return f"https://docs.google.com/document/d/{doc_id}/edit"
