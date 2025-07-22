# sheets/sheet_utils.py
import gspread
from google.oauth2.service_account import Credentials

def get_gspread_client(credentials_path: str = "config/credentials.json"):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    client = gspread.authorize(creds)
    return client
