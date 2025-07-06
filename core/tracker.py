# core/tracker.py
import json
import os
from datetime import datetime

LOG_FILE = "data/study_log.json"

def save_study_session(subject, topic, duration, notes):
    entry = {
        "subject": subject,
        "topic": topic,
        "duration": duration,
        "notes": notes,
        "timestamp": datetime.now().isoformat()
    }

    if not os.path.exists("data"):
        os.makedirs("data")

    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_study_sessions():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []
