import threading
from atmshield.usb_monitor import USBMonitor
from atmshield.process_monitor import ProcessMonitor
from atmshield.logger import log_event

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
    print_banner()
    log_event("ATMShield started.")

    usb_monitor = USBMonitor()
    process_monitor = ProcessMonitor()

    t1 = threading.Thread(target=usb_monitor.start)
    t2 = threading.Thread(target=process_monitor.start)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
