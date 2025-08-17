import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from langchain_core.tools import tool
from datetime import datetime

# Load env
load_dotenv()

USER_NAME = os.getenv("USER_NAME", "guest")
USER_EMAIL = os.getenv("USER_EMAIL", "guest@example.com")
CSV_PATH = os.getenv("CSV_PATH", "./tickets.csv")
DB_PATH = os.getenv("DB_PATH", "./installations.db")


def generate_ticket_id():
    return f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"




def write_to_csv(ticket_id, user, app, version, status):
    data = {
        "TicketID": ticket_id,
        "User": user,
        "App": app,
        "Version": version,
        "Status": status,
        "CreatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    df = pd.DataFrame([data])
    if not os.path.exists(CSV_PATH):
        df.to_csv(CSV_PATH, index=False)
    else:
        df.to_csv(CSV_PATH, mode="a", index=False, header=False)


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


@tool
def install_software(user: str = USER_NAME, app: str = "UnknownApp", version: str = "latest") -> str:
    """
    Simulates software installation:
    1. Creates ticket in Excel
    2. Logs to SQLite DB
    3. Returns confirmation
    """
    print("⚡ Tool called with:", user, app, version)
    ticket_id = generate_ticket_id()
    status = "Installed"

    write_to_csv(ticket_id, user, app, version, status)
    write_to_db(ticket_id, user, app, version)

    return f"✅ Ticket {ticket_id} created for {user}. {app} (v{version}) installed successfully."
