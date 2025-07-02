# app/crypto_utils.py

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def generate_key_from_password(password: str) -> bytes:
    """
    Deriva una chiave AES‑256 a 32 byte dalla password
    usando SHA‑256. Questa chiave servirà per cifrare e
    decifrare tutte le note.
    """
    return hashlib.sha256(password.encode("utf-8")).digest()

def encrypt_note(content: str, key: bytes) -> str:
    """
    Cifra il testo `content` con AES‑CBC usando `key`.
    Restituisce una stringa base64(IV):base64(ciphertext).
    """
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(content.encode("utf-8"), AES.block_size))
    iv_b64 = base64.b64encode(cipher.iv).decode("utf-8")
    ct_b64 = base64.b64encode(ct_bytes).decode("utf-8")
    return f"{iv_b64}:{ct_b64}"

def decrypt_note(encrypted_content: str, key: bytes) -> str:
    """
    Decifra la stringa generata da `encrypt_note`.
    Separa IV e ciphertext, li decodifica da base64,
    poi restituisce il plaintext.
    """
    iv_b64, ct_b64 = encrypted_content.split(":")
    iv = base64.b64decode(iv_b64)
    ct = base64.b64decode(ct_b64)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode("utf-8")

