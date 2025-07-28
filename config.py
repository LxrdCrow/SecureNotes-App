import os
from dotenv import load_dotenv
load_dotenv()

DB_PATH = os.getenv("DB_PATH", "secure_notes.db")
APP_NAME = os.getenv("APP_NAME", "Secure Notes")
