from datetime import datetime
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "events.log")

os.makedirs(LOG_DIR, exist_ok=True)  # Ensure logs/ exists

def log_event(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}"
    print(entry)

    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")
