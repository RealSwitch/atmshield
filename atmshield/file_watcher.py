import os
import time
import shutil
import hashlib
from atmshield.logger import log_event

CONFIG_FILE = "/tmp/watcher_path.txt"
QUARANTINE_DIR = "atmshield/quarantine"

class FileWatcher:
    def __init__(self, paths=None):
        self.watch_paths = paths or []
        self.snapshot = {}
        os.makedirs(QUARANTINE_DIR, exist_ok=True)

    def hash_file(self, path):
        try:
            with open(path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return None

    def build_snapshot(self):
        snapshot = {}
        for path in self.watch_paths:
            if os.path.isfile(path):
                snapshot[path] = self.hash_file(path)
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        snapshot[full_path] = self.hash_file(full_path)
        return snapshot

    def update_watch_paths(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                dynamic_path = f.read().strip()
                if dynamic_path and dynamic_path not in self.watch_paths:
                    self.watch_paths = [dynamic_path]
                    log_event(f"Switched watch path to: {dynamic_path}", "INFO")
        except FileNotFoundError:
            pass

    @staticmethod
    def deploy_honeypot_to_usb(mount_path):
        honeypot_src = "honeypots/get_admin_password.py"
        honeypot_dst = os.path.join(mount_path, "get_admin_password.py")
        try:
            shutil.copy2(honeypot_src, honeypot_dst)
            log_event(f"[HONEYPOT] Bait deployed to {honeypot_dst}")
        except Exception as e:
            log_event(f"[HONEYPOT] Failed to deploy bait: {e}")

    def quarantine_file(self, path):
        try:
            filename = os.path.basename(path)
            destination = os.path.join(QUARANTINE_DIR, filename)
            shutil.move(path, destination)
            log_event(f"Quarantined suspicious file: {filename}", "ALERT")
        except Exception as e:
            log_event(f"Failed to quarantine {path}: {e}", "ERROR")

    def scan_file(self, path):
        try:
            with open(path, 'r', errors='ignore') as f:
                content = f.read()
                if 'eval(' in content or 'subprocess' in content or 'socket' in content:
                    log_event(f"Suspicious content detected in: {path}", "SCAN")
                    self.quarantine_file(path)
        except Exception:
            pass

    def start(self):
        log_event("Starting File Watcher...", "INFO")
        self.update_watch_paths()
        self.snapshot = self.build_snapshot()

        while True:
            self.update_watch_paths()
            new_snapshot = self.build_snapshot()

            for path, old_hash in self.snapshot.items():
                if path not in new_snapshot:
                    log_event(f"File deleted: {path}", "ALERT")
                elif old_hash != new_snapshot[path]:
                    log_event(f"File modified: {path}", "ALERT")
                    self.scan_file(path)

            for path in new_snapshot:
                if path not in self.snapshot:
                    log_event(f"New file detected: {path}", "ALERT")
                    self.scan_file(path)

            self.snapshot = new_snapshot
            time.sleep(5)
