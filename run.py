import threading
from atmshield.usb_monitor import USBMonitor
from atmshield.process_monitor import ProcessMonitor
from atmshield.logger import log_event
from atmshield.file_watcher import FileWatcher
def print_banner():
    print(r"""
     █████╗ ████████╗███╗   ███╗ ███████╗██╗  ██╗██╗██╗     ███████╗██████╗ 
    ██╔══██╗╚══██╔══╝████╗ ████║ ██╔════╝╚██╗██╔╝██║██║     ██╔════╝██╔══██╗
    ███████║   ██║   ██╔████╔██║ █████╗   ╚███╔╝ ██║██║     █████╗  ██████╔╝
    ██╔══██║   ██║   ██║╚██╔╝██║ ██╔══╝   ██╔██╗ ██║██║     ██╔══╝  ██╔══██╗
    ██║  ██║   ██║   ██║ ╚═╝ ██║ ███████╗██╔╝ ██╗██║███████╗███████╗██║  ██║
    ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝ ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
                Lightweight ATM Security Auditing Tool
    """)

if __name__ == "__main__":
    file_watcher = FileWatcher(["/usr/local/bin/atmcore","/etc/atm_config"])
    print_banner()
    log_event("ATMShield started.")

    usb_monitor = USBMonitor()
    process_monitor = ProcessMonitor()

    t1 = threading.Thread(target=usb_monitor.start)
    t2 = threading.Thread(target=process_monitor.start)
    t3 = threading.Thread(target=file_watcher.start)
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
