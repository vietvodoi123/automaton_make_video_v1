import base64
import json
import os
import requests
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

# --- THIẾT LẬP ---
PASSWORD = b"vH33r_2025_AES_GCM_S3cur3_K3y_9X7mP4qR8nT2wE5yU1oI6aS3dF7gH0jK9lZ"
SALT = b"freetts-salt-2025"

def derive_key(password: bytes) -> bytes:
    """PBKDF2 với SHA-256, 10000 vòng"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256
        salt=SALT,
        iterations=10000,
        backend=default_backend()
    )
    return kdf.derive(password)

def encrypt_payload(payload: dict) -> str:
    """Mã hóa JSON -> Base64(IV + ciphertext)"""
    key = derive_key(PASSWORD)
    aesgcm = AESGCM(key)
    iv = os.urandom(12)
    data = json.dumps(payload).encode("utf-8")
    ct = aesgcm.encrypt(iv, data, None)  # AES-GCM
    blob = iv + ct
    return base64.b64encode(blob).decode("utf-8")

# --- TẠO PARAMS ---
payload_object = {
  "text": "Xin chào từ Python",
  "type": 0,
  "ssml": 0,
  "voiceType": "WaveNet",
  "languageCode": "vi-VN",
  "voiceName": "vi-VN-Wavenet-C",
  "gender": "FEMALE",
  "speed": "1.0",
  "pitch": "0",
  "volume": "0",
  "format": "mp3",
  "quality": 0,
  "isListenlingMode": 0,
  "displayName": "Veronica Chan"
}


params = encrypt_payload(payload_object)
print("Params:", params)
