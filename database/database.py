import mysql.connector  
from mysql.connector import Error
import config  

def create_connection():
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME
        )
        if conn.is_connected():
            print("✅ Connection to the database established successfully.")
            return conn
        else:
            print("❌ Failed to connect to the database.")
            return None
    except Error as e:
        print(f"❌ Error connecting to the database: {e}")
        return None

def initialize_database():
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    table_queries = [
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS settings (
            id INT PRIMARY KEY AUTO_INCREMENT,
            theme VARCHAR(50) DEFAULT 'light',
            language VARCHAR(50) DEFAULT 'en'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS master_key (
            id INT PRIMARY KEY AUTO_INCREMENT,
            password_hash TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS encryption_keys (
            id INT PRIMARY KEY AUTO_INCREMENT,
            key_data TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INT PRIMARY KEY AUTO_INCREMENT,
            action VARCHAR(255) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]

    try:
        for query in table_queries:
            cursor.execute(query)
        conn.commit()
        print("✅ Tables created successfully.")
    except Error as e:
        print(f"❌ Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()
        print("✅ Connection to the database closed.")
