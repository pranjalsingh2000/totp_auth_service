import os
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("SECRET_KEY")
if not key or len(key.encode()) != 32:
    raise ValueError("SECRET_KEY must be 32 bytes (256 bits)")

key = key.encode()

def encrypt_secret(secret: str) -> str:
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(secret.encode())
    data = cipher.nonce + tag + ciphertext
    return b64encode(data).decode()

def decrypt_secret(encrypted: str) -> str:
    raw = b64decode(encrypted)
    nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()
