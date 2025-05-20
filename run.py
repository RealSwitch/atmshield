from atmshield.usb_monitor import USBMonitor
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
    monitor = USBMonitor()
    monitor.start()
