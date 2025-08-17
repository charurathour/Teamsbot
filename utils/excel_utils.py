import pandas as pd
import os

EXCEL_FILE = "tickets.xlsx"

def create_ticket(user: str, app: str, version: str = "latest") -> str:
    """Creates/updates Excel ticket log and returns ticket_id"""
    # Create file if doesn't exist
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=["ticket_id", "user", "app", "version", "status"])
        df.to_excel(EXCEL_FILE, index=False)

    # Load existing
    df = pd.read_excel(EXCEL_FILE)

    # Generate ticket_id
    ticket_id = f"T{len(df)+1:04d}"

    # Add new record
    new_row = {
        "ticket_id": ticket_id,
        "user": user,
        "app": app,
        "version": version,
        "status": "In Progress"
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save
    df.to_excel(EXCEL_FILE, index=False)

    return ticket_id
