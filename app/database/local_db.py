
import sqlite3
from datetime import datetime

conn = sqlite3.connect("offline_reports.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    synced INTEGER DEFAULT 0,
    created_at TEXT
)
""")
conn.commit()

def insert_report(data):
    cursor.execute(
        "INSERT INTO reports (data, synced, created_at) VALUES (?, ?, ?)",
        (str(data), 0, datetime.now().isoformat())
    )
    conn.commit()

def get_unsynced_reports():
    cursor.execute("SELECT id, data FROM reports WHERE synced = 0")
    return cursor.fetchall()

def mark_as_synced(report_id):
    cursor.execute("UPDATE reports SET synced = 1 WHERE id = ?", (report_id,))
    conn.commit()
