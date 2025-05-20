import os
import datetime

LOG_FILE = os.path.join("logs", "events.log")

def log_event(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")
