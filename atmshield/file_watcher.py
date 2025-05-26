import os
import time
import hashlib
from atmshield.logger import log_event

class FileWatcher:
    def __init__(self, paths):
        self.watch_paths = paths
        self.snapshot = {}

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

    def start(self):
        print("[File Watcher] Monitoring file integrity...")
        self.snapshot = self.build_snapshot()
        while True:
            new_snapshot = self.build_snapshot()
            for path, old_hash in self.snapshot.items():
                if path not in new_snapshot:
                    log_event(f"[ALERT] File deleted: {path}")
                    print(f"[ALERT] File deleted: {path}")
                elif old_hash != new_snapshot[path]:
                    log_event(f"[ALERT] File modified: {path}")
                    print(f"[ALERT] File modified: {path}")

            for path in new_snapshot:
                if path not in self.snapshot:
                    log_event(f"[ALERT] New file detected: {path}")
                    print(f"[ALERT] New file detected: {path}")

            self.snapshot = new_snapshot
            time.sleep(10)
