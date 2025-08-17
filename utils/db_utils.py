import sqlite3

DB_FILE = "installations.db"

def log_install(user: str, app: str, version: str = "latest"):
    """Logs installation into SQLite"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS installations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            app TEXT,
            version TEXT
        )
    """)

    cur.execute(
        "INSERT INTO installations (user, app, version) VALUES (?, ?, ?)",
        (user, app, version)
    )
    conn.commit()
    conn.close()
