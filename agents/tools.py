import os
import pandas as pd
from dotenv import load_dotenv
from langchain_core.tools import tool
from datetime import datetime
from utils.db_utils import write_to_db
from utils.csv_utils import write_to_csv

# Load env
load_dotenv()

USER_NAME = os.getenv("USER_NAME", "guest")
USER_EMAIL = os.getenv("USER_EMAIL", "guest@example.com")

def generate_ticket_id():
    return f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"


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
