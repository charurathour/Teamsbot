import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os

# Load env
load_dotenv()
DB_PATH = os.getenv("DB_PATH", "./installations.db")

def write_to_db(ticket_id, user, app, version):
    """Log installation in SQLite DB"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("Database file exists, appending new entry.")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS installations (
                TicketID TEXT PRIMARY KEY,
                User TEXT,
                App TEXT,
                Version TEXT,
                Status TEXT,
                CreatedAt TEXT
            )
        """)
        cursor.execute(
            "INSERT INTO installations VALUES (?, ?, ?, ?, ?, ?)",
            (
                ticket_id,
                user,
                app,
                version,
                "Installed",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        return f"⚠️ Failed to write DB: {e}"

