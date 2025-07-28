import sqlite3
import os
import config 
from sqlite3 import Error

def create_connection():
    try:
        db_path = getattr(config, "DB_PATH", "secure_notes.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print("✅ Connection to SQLite database established.")
        return conn
    except Error as e:
        print(f"❌ Error connecting to SQLite database: {e}")
        return None

def initialize_database():
    conn = create_connection()
    if conn is None:
        return
    cursor = conn.cursor()

    table_queries = [
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            open_count INTEGER DEFAULT 0,
            max_opens INTEGER DEFAULT NULL,
            expires_at DATETIME DEFAULT NULL,
            is_reflection INTEGER DEFAULT 0,
            blind_mode INTEGER DEFAULT 0
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            theme TEXT DEFAULT 'light',
            language TEXT DEFAULT 'en'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS master_key (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_hash TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS encryption_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_data TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            encrypted_master_key TEXT NOT NULL
        )
        """
    ]

    try:
        for query in table_queries:
            cursor.execute(query)
        conn.commit()
        print("✅ Tables created successfully (SQLite).")
    except Error as e:
        print(f"❌ Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()
        print("✅ SQLite connection closed.")

