import os
import pandas as pd
from dotenv import load_dotenv
from langchain_core.tools import tool
from datetime import datetime

# Load env
load_dotenv()
CSV_PATH = os.getenv("CSV_PATH", "./tickets.csv")
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