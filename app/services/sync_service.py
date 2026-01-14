
import requests
from app.database.local_db import insert_report, get_unsynced_reports, mark_as_synced

API_URL = "http://127.0.0.1:8000/api/report"

def save_local_report(report):
    insert_report(report)

def sync_reports():
    reports = get_unsynced_reports()
    count = 0
    for report_id, data in reports:
        try:
            r = requests.post(API_URL, json=eval(data))
            if r.status_code == 200:
                mark_as_synced(report_id)
                count += 1
        except:
            break
    return count
