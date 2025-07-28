import os
from datetime import datetime
from cryptography.fernet import Fernet
from database import database  

def generate_key() -> bytes:
    """
    Generate a new Fernet key.
    """
    return Fernet.generate_key()

def get_fernet(key: bytes) -> Fernet:
    """
    Return a Fernet instance for the given key.
    """
    return Fernet(key)

def encrypt_string(data: str, key: bytes) -> bytes:
    """
    Encrypt a string using the provided key.
    Returns encrypted bytes.
    """
    return get_fernet(key).encrypt(data.encode())

def decrypt_string(encrypted_data: bytes, key: bytes) -> str:
    """
    Decrypt bytes using the provided key.
    Returns the original string.
    """
    return get_fernet(key).decrypt(encrypted_data).decode()

def load_master_key() -> bytes:
    """
    Load the master key from the SQLite database, or generate & save it if not present.
    Returns the key (bytes).
    """
    conn = database.create_connection()
    if conn is None:
        raise RuntimeError("Cannot connect to database to load/generate master key.")
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM master_key LIMIT 1")
    row = cursor.fetchone()

    if row:
        key = row[0].encode()
        print("🔑 Master key loaded.")
    else:
        key = generate_key()
        cursor.execute(
            "INSERT INTO master_key (password_hash) VALUES (?)",
            (key.decode(),)
        )
        conn.commit()
        print("🆕 Master key generated and saved.")

    cursor.close()
    conn.close()
    return key

def create_note(title: str, content: str, key: bytes,
                expires_at: datetime = None,
                max_opens: int = None,
                is_reflection: bool = False,
                blind_mode: bool = False):
    """
    Create a new encrypted note in the database.
    - title, content: strings to be encrypted
    - key: master key (bytes) for encryption
    - expires_at: datetime or None
    - max_opens: int or None
    - is_reflection, blind_mode: boolean flags
    """
    encrypted_title = encrypt_string(title, key)
    encrypted_content = encrypt_string(content, key)

    expires_str = None
    if expires_at:
        if isinstance(expires_at, datetime):
            expires_str = expires_at.isoformat(sep=' ')
        else:
            expires_str = str(expires_at)

    conn = database.create_connection()
    if conn is None:
        print("❌ Cannot create note: no DB connection.")
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO notes
                (title, content, expires_at, max_opens, is_reflection, blind_mode)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (encrypted_title, encrypted_content, expires_str, max_opens, int(is_reflection), int(blind_mode))
        )
        conn.commit()
        print("📝 Note created.")
    except Exception as e:
        print(f"❌ Failed to create note: {e}")
    finally:
        cursor.close()
        conn.close()

def should_delete_note(note_row: dict) -> bool:
    now = datetime.now()
    max_opens = note_row.get("max_opens")
    open_count = note_row.get("open_count", 0)

    if max_opens is not None:
        try:
            if open_count >= max_opens:
                return True
        except Exception:
            pass

    expires_at = note_row.get("expires_at")
    if expires_at:
        try:
            if isinstance(expires_at, str):
                expires_dt = datetime.fromisoformat(expires_at)
            elif isinstance(expires_at, datetime):
                expires_dt = expires_at
            else:
                expires_dt = None
            if expires_dt and now > expires_dt:
                return True
        except Exception:
            pass

    return False

def increment_open_count(note_id: int):
    conn = database.create_connection()
    if conn is None:
        print("❌ Cannot increment open_count: no DB connection.")
        return
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE notes SET open_count = open_count + 1 WHERE id = ?",
            (note_id,)
        )
        cursor.execute(
            "UPDATE notes SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (note_id,)
        )
        conn.commit()
    except Exception as e:
        print(f"⚠️ Error incrementing open_count for note {note_id}: {e}")
    finally:
        cursor.close()
        conn.close()

def mark_note_deleted(note_id: int):
    conn = database.create_connection()
    if conn is None:
        print("❌ Cannot delete note: no DB connection.")
        return
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        print(f"🗑️ Note {note_id} deleted.")
    except Exception as e:
        print(f"⚠️ Error deleting note {note_id}: {e}")
    finally:
        cursor.close()
        conn.close()

def is_blind_mode_enabled(note_row: dict) -> bool:
    return bool(note_row.get("blind_mode"))

def is_reflection(note_row: dict) -> bool:
    return bool(note_row.get("is_reflection"))
