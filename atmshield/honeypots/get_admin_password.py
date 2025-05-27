# /honeypots/get_admin_password.py
import os
import socket
import time
from atmshield.logger import log_event

log_event("[HONEYPOT] Reverse shell bait script executed.")
print("Contacting admin server...")

# Optional: simulate a reverse shell connection
try:
    s = socket.socket()
    s.connect(("198.51.100.1", 1337))  # Fake IP (you can use your own server for real honeypot)
    s.sendall(b"root:admin123\n")
    time.sleep(2)
    s.close()
except Exception as e:
    log_event(f"[HONEYPOT] Connection attempt blocked: {e}")
    print("Connection failed. Admin server unreachable.")
