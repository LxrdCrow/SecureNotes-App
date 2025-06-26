from datetime import datetime
from database import database
from app.logic import (
    encrypt_string,
    decrypt_string,
    should_delete_note,
    increment_open_count,
    mark_note_deleted
)

def create_note(title: str, content: str, master_key: bytes,
                expires_at: datetime = None,
                max_opens: int = None,
                is_reflection: bool = False,
                blind_mode: bool = False):
    """
    Create a new encrypted note in the database.
    
    :param title: The plaintext title.
    :param content: The plaintext content.
    :param master_key: The Fernet key (bytes) used for encryption.
    :param expires_at: Optional datetime when note should expire.
    :param max_opens: Optional int maximum number of opens before auto-delete.
    :param is_reflection: If True, this note uses “reflection mode” logic.
    :param blind_mode: If True, this note uses “blind mode” logic.
    """
    # Encrypt title and content
    encrypted_title = encrypt_string(title, master_key)
    encrypted_content = encrypt_string(content, master_key)

    # Prepare expires_at as ISO string or None
    expires_str = None
    if expires_at:
        if isinstance(expires_at, datetime):
            expires_str = expires_at.isoformat(sep=' ')
        else:
            expires_str = str(expires_at)

    # Convert booleans to integers for SQLite (0 or 1)
    reflection_flag = 1 if is_reflection else 0
    blind_flag = 1 if blind_mode else 0

    conn = database.create_connection()
    if conn is None:
        raise RuntimeError("Cannot connect to database to create note.")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO notes
                (title, content, created_at, updated_at, open_count, max_opens, expires_at, is_reflection, blind_mode)
            VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0, ?, ?, ?, ?)
        """, (encrypted_title, encrypted_content, max_opens, expires_str, reflection_flag, blind_flag))
        conn.commit()
        print(f"Note created with title (encrypted).")
    except Exception as e:
        print(f"Error creating note: {e}")
    finally:
        cursor.close()
        conn.close()


def read_note(note_id: int, master_key: bytes):
    """
    Read a note by ID:
    - If the note should auto-delete (due to max_opens or expiration), delete it and return {'deleted': True}.
    - Otherwise, increment open_count, decrypt and return note data.
    
    :param note_id: ID of the note to read.
    :param master_key: The Fernet key (bytes) used for decryption.
    :return: A dict with decrypted fields and metadata, or {'deleted': True}, or None if not found.
    """
    conn = database.create_connection()
    if conn is None:
        raise RuntimeError("Cannot connect to database to read note.")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        if not row:
            # Note not found
            return None

        note_row = dict(row)

        if should_delete_note(note_row):
            mark_note_deleted(note_id)
            print(f"Note {note_id} auto-deleted.")
            return {"deleted": True}

        
        increment_open_count(note_id)

        # Decrypt title and content
        try:
            decrypted_title = decrypt_string(note_row["title"], master_key)
        except Exception:
            decrypted_title = "<Decryption Error>"

        try:
            decrypted_content = decrypt_string(note_row["content"], master_key)
        except Exception:
            decrypted_content = "<Decryption Error>"

        # Build result with metadata
        result = {
            "id": note_id,
            "title": decrypted_title,
            "content": decrypted_content,
            "created_at": note_row.get("created_at"),
            "updated_at": datetime.now(),
            "open_count": note_row.get("open_count", 0) + 1,
            "max_opens": note_row.get("max_opens"),
            "expires_at": note_row.get("expires_at"),
            "is_reflection": bool(note_row.get("is_reflection")),
            "blind_mode": bool(note_row.get("blind_mode")),
            "deleted": False
        }
        return result
    finally:
        cursor.close()
        conn.close()


def update_note(note_id: int, title: str, content: str, master_key: bytes,
                expires_at: datetime = None,
                max_opens: int = None,
                is_reflection: bool = False,
                blind_mode: bool = False):
    """
    Update an existing note with new encrypted data and metadata.
    
    :param note_id: ID of the note to update.
    :param title: New plaintext title.
    :param content: New plaintext content.
    :param master_key: The Fernet key (bytes) used for encryption.
    :param expires_at: Optional datetime when note should expire.
    :param max_opens: Optional int maximum number of opens.
    :param is_reflection: If True, enable reflection mode.
    :param blind_mode: If True, enable blind mode.
    """
    
    encrypted_title = encrypt_string(title, master_key)
    encrypted_content = encrypt_string(content, master_key)

    expires_str = None
    if expires_at:
        if isinstance(expires_at, datetime):
            expires_str = expires_at.isoformat(sep=' ')
        else:
            expires_str = str(expires_at)

    reflection_flag = 1 if is_reflection else 0
    blind_flag = 1 if blind_mode else 0

    conn = database.create_connection()
    if conn is None:
        raise RuntimeError("Cannot connect to database to update note.")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE notes
            SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP,
                max_opens = ?, expires_at = ?, is_reflection = ?, blind_mode = ?
            WHERE id = ?
        """, (encrypted_title, encrypted_content, max_opens, expires_str, reflection_flag, blind_flag, note_id))
        conn.commit()
        print(f"Note {note_id} updated.")
    except Exception as e:
        print(f"Error updating note {note_id}: {e}")
    finally:
        cursor.close()
        conn.close()


def delete_note(note_id: int):
    """
    Delete a note by ID.
    
    :param note_id: ID of the note to delete.
    """
    conn = database.create_connection()
    if conn is None:
        raise RuntimeError("Cannot connect to database to delete note.")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        print(f"Note {note_id} deleted.")
    except Exception as e:
        print(f"Error deleting note {note_id}: {e}")
    finally:
        cursor.close()
        conn.close()


def list_notes(master_key: bytes):
    """
    List all notes, decrypting only the title for display in a list.
    
    :param master_key: The Fernet key (bytes) used for decryption.
    :return: A list of dicts, each with keys:
        id, title (decrypted), created_at, updated_at, open_count,
        max_opens, expires_at, is_reflection (bool), blind_mode (bool).
    """
    conn = database.create_connection()
    if conn is None:
        raise RuntimeError("Cannot connect to database to list notes.")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, title, created_at, updated_at, open_count, max_opens, expires_at, is_reflection, blind_mode
            FROM notes
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            note_row = dict(row)
            try:
                decrypted_title = decrypt_string(note_row["title"], master_key)
            except Exception:
                decrypted_title = "<Decryption Error>"
            item = {
                "id": note_row["id"],
                "title": decrypted_title,
                "created_at": note_row.get("created_at"),
                "updated_at": note_row.get("updated_at"),
                "open_count": note_row.get("open_count"),
                "max_opens": note_row.get("max_opens"),
                "expires_at": note_row.get("expires_at"),
                "is_reflection": bool(note_row.get("is_reflection")),
                "blind_mode": bool(note_row.get("blind_mode"))
            }
            result.append(item)
        return result
    finally:
        cursor.close()
        conn.close()
