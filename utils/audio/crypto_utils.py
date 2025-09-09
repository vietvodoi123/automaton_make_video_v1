import base64
import json
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

PASSWORD = b"vH33r_2025_AES_GCM_S3cur3_K3y_9X7mP4qR8nT2wE5yU1oI6aS3dF7gH0jK9lZ"
SALT = b"freetts-salt-2025"

def derive_key(password: bytes = PASSWORD) -> bytes:
    """Sinh AES-256 key bằng PBKDF2 (SHA-256, 10000 vòng)"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=10000,
        backend=default_backend()
    )
    return kdf.derive(password)

def encrypt_payload(payload: dict) -> str:
    """Mã hóa JSON -> Base64(IV + ciphertext)"""
    key = derive_key()
    aesgcm = AESGCM(key)
    iv = os.urandom(12)
    data = json.dumps(payload).encode("utf-8")
    ct = aesgcm.encrypt(iv, data, None)
    blob = iv + ct
    return base64.b64encode(blob).decode("utf-8")

def decrypt_params(params: str) -> str:
    """Giải mã Base64 params -> JSON text"""
    raw = base64.b64decode(params)
    iv, ct = raw[:12], raw[12:]
    key = derive_key()
    aesgcm = AESGCM(key)
    plain = aesgcm.decrypt(iv, ct, None)
    return plain.decode("utf-8")
