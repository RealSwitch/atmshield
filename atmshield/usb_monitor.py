import pyudev
import datetime
from atmshield.logger import log_event

class USBMonitor:
    def __init__(self):
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='usb')

    def start(self):
        print("[USB Monitor] Starting USB device monitoring...")
        for device in iter(self.monitor.poll, None):
            if device.action == 'add':
                self._handle_device_event(device, "CONNECTED")
            elif device.action == 'remove':
                self._handle_device_event(device, "DISCONNECTED")

    def _handle_device_event(self, device, status):
        info = {
            "action": status,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "vendor": device.get("ID_VENDOR"),
            "model": device.get("ID_MODEL"),
            "serial": device.get("ID_SERIAL_SHORT")
        }
        message = f"[USB {info['action']}] {info['vendor']} {info['model']} (Serial: {info['serial']}) at {info['time']}"
        print(message)
        log_event(message)
