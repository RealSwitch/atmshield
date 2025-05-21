import psutil
import time
from atmshield.logger import log_event


class ProcessMonitor:
    def __init__(self):
        self.blacklist = [
            "mimikatz", "msfconsole", "nc", "netcat", "nmap",
            "john", "hydra", "sqlmap", "python", "powershell"
        ]

    def start(self):
        print("[Process Monitor] Monitoring suspicious processes...")
        while True:
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
                try:
                    proc_name = proc.info['name'].lower()
                    if any(bad in proc_name for bad in self.blacklist):
                        message = f"[ALERT] Suspicious process detected: {proc_name} (PID: {proc.info['pid']})"
                        print(message)
                        log_event(message)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            time.sleep(5)  # Check every 5 seconds
