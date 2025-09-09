import requests

url = "https://freetts.com/text-to-speech"

headers = {
    "accept": "text/x-component",
    "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "content-type": "text/plain;charset=UTF-8",
    "dnt": "1",
    "origin": "https://freetts.com",
    "referer": "https://freetts.com/text-to-speech",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "next-action": "f6a37f3b9ffdb01ba2da16f264fdabab4a254f61",
    "next-router-state-tree": "[\"\",{\"children\":[\"(functions)\",{\"children\":[\"text-to-speech\",{\"children\":[\"__PAGE__\",{},\"/text-to-speech\",\"refresh\"]}]}]},null,null,true]",
    # Cookie + Authorization phải copy đúng từ DevTools
    "cookie": "_ga=GA1.1...; Authorization=eyJhbGc...; __gpi=UID=..."
}

# Body phải là array JSON
body = [
    {
        "params": "AVibRz4uZZxyJViaU12mM4GywwS+NOKUzpUW2LUXBVmckcJsYASfzZ+sTT5F69aQJZiFVzeaPF3ERYkdAMhEnzEnJzwc37Vr8Ks6oj12NEPTVOrRo0zWGtG7FKGnd+L6/NF/vJWmzIyVKWXq7fiJGamcPRE3fApJNtTyd0grIWE/stnt5A8PJYXk73oJPvTUEKdwGxidbj5t0svIMNOpC3bmDD3a0dFECZfkiPiqGAlGGUcpfduZDXS09VlLRNP7wO8c5fs6lzF9MmgkXE1QO1x5tT3LExCrWkCgS1Uv7BKg4b5GoJltUoJ+bmJs1bskLQnPv4qQJcIqn0gwCeD1CuEvKb8OZTfF7+DNPn1ia7KaouW0hZ9zbnf3m8rKC5HgXAVZi2qNjojVs525TcHCSXDDM/JNdxe8cxfeOxRuY9i/vA=="
    }
]

res = requests.post(url, headers=headers, json=body)

print("Status:", res.status_code)
print("Response:", res.text)

# import base64
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# from cryptography.hazmat.backends import default_backend
#
# params = "8xLV1EqFUpcz1PiKlFV1/p2M8k9UDpGIaZXtMLg9T/SCBC5/jytop6RNC2D/vaVXfi7pnQf8W24lDbOehq1VqnFEBoOrhZFeUC1ttCUgQhNKcX/ADSO/2FEZeWNqEleNkiq9qYrw7GEz1x7qbkl7F/f4SOYVYCgyETglyZX0Hd/2AOgejzaSgBlbK/puqOqUAcVcw70qp3qzbIYTTFXJr6jdGfIRpiKpRMh1QMHn8B5PAj7yneWgaO6NEzSbDAp+8hymusyhPAQSrIZU2ODcHsv+ANCMKJyDR/0ydWA0WSTGjur6frZEthO369o4wNiZh24d9qSfIeEah8n09LrE2UpkyuGML37gkULtMKg0KqYNcNPOHsPmVxivG2Vz96WU"
#
# # 1. Base64 decode
# raw = base64.b64decode(params)
# iv, ct = raw[:12], raw[12:]
#
# # 2. Derive key với PBKDF2
# password = b"vH33r_2025_AES_GCM_S3cur3_K3y_9X7mP4qR8nT2wE5yU1oI6aS3dF7gH0jK9lZ"  # fallback trong bundle
# salt = b"freetts-salt-2025"
#
# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=10000,
#     backend=default_backend()
# )
# key = kdf.derive(password)
#
# # 3. Thử decrypt
# aesgcm = AESGCM(key)
# try:
#     plain = aesgcm.decrypt(iv, ct, None)
#     print("Decrypted:", plain.decode("utf-8"))
# except Exception as e:
#     print("Decrypt failed:", e)
