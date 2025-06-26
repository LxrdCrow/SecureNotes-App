import os
from pathlib import Path

def get_project_root() -> str:
    """
    Returns the root directory of the project.
    """
    return str(Path(__file__).resolve().parent.parent)

def get_database_path() -> str:
    """
    Returns the path to the SQLite database file.
    """
    return os.path.join(get_project_root(), "secure_notes.db")

def format_timestamp(dt) -> str:
    """
    Formats a datetime object or string to a readable string format.
    """
    if isinstance(dt, str):
        return dt  # Already formatted
    return dt.strftime("%Y-%m-%d %H:%M:%S")


