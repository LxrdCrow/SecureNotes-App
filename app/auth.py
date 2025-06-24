import os
import base64 # for base64 encoding/decoding
import secrets # for generating secure random bytes
import hashlib # for hashing
from cryptography.fernet import Fernet
from datetime import datetime
from database import database

# KDF parameters
KDF_ITERATIONS = 200_000  
SALT_LENGTH = 16        

def _derive_key_from_password(password: str, salt: bytes) -> bytes:
    """
    Derive a key-encryption-key (KEK) from the given password + salt using PBKDF2-HMAC-SHA256.
    """
    # PBKDF2-HMAC-SHA256
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        KDF_ITERATIONS,
        dklen=32
    )

    return base64.urlsafe_b64encode(dk)  # bytes

def setup_master_password(password: str) -> bytes:
    """
    For the first run:
    1. Generate a random salt.
    2. Derive a key-encryption-key (KEK) from the password and salt.
    3. Hash the password to generate a password hash.
    4. Generate a random master key.
    5. Encrypt the master key with the KEK.
    6. Save the password hash, salt, and encrypted master key to the database.
    """
    # 1. Generate random salt
    salt = secrets.token_bytes(SALT_LENGTH)

    # 2. KEK derivation from password and salt
    kek = _derive_key_from_password(password, salt)

    # 3. Hash for password verification
    pw_hash_raw = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, KDF_ITERATIONS)
    password_hash = pw_hash_raw.hex()  # stringa hex per confronto

    # 4. Generate a random master key
    master_key = Fernet.generate_key()  # bytes base64

    # 5. Encrypt the master key with the KEK
    fernet_kek = Fernet(kek)
    encrypted_master_key = fernet_kek.encrypt(master_key)  # bytes

    # 6. Save to database (auth table)
    # Convert salt and encrypted master key to base64 for storage
    salt_b64 = base64.urlsafe_b64encode(salt).decode('utf-8')
    encrypted_master_b64 = encrypted_master_key.decode('utf-8')

    conn = database.create_connection()
    if conn is None:
        raise RuntimeError("Cannot connect to DB to save master key.")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM auth")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute(
            "INSERT INTO auth (password_hash, salt, encrypted_master_key) VALUES (?, ?, ?)",
            (password_hash, salt_b64, encrypted_master_b64)
        )
    else:
        cursor.execute(
            "UPDATE auth SET password_hash = ?, salt = ?, encrypted_master_key = ? WHERE id = ?",
            (password_hash, salt_b64, encrypted_master_b64, 1)
        )
    conn.commit()
    cursor.close()
    conn.close()

    print("🔑 Master password set and master key generated.")
    return master_key

def verify_master_password(password: str) -> bytes:
    conn = database.create_connection()
    if conn is None:
        raise RuntimeError("Cannot connect to DB for authentication.")
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash, salt, encrypted_master_key FROM auth LIMIT 1")
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        raise RuntimeError("No master password set. Call setup_master_password first.")

    stored_hash_hex, salt_b64, encrypted_master_b64 = row
    salt = base64.urlsafe_b64decode(salt_b64.encode('utf-8'))
    encrypted_master_key = encrypted_master_b64.encode('utf-8')

    pw_hash_raw = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, KDF_ITERATIONS)
    if pw_hash_raw.hex() != stored_hash_hex:
        return None

    kek = _derive_key_from_password(password, salt)
    fernet_kek = Fernet(kek)
    try:
        master_key = fernet_kek.decrypt(encrypted_master_key)
    except Exception as e:
        raise RuntimeError("Failed to decrypt master key: possibly corrupted data.") from e

    print("🔓 Master password verified and master key decrypted.")
    return master_key

def is_master_password_set() -> bool:
    """
    Check if a master password is already set by querying the auth table.
    Returns True if a master password exists, False otherwise.
    """
    conn = database.create_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM auth")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

