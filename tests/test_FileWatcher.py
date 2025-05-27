import os
import tempfile
import time
import shutil
from atmshield.file_watcher import FileWatcher

def test_file_addition_and_quarantine():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup config
        config_path = "/tmp/watcher_path.txt"
        with open(config_path, "w") as f:
            f.write(tmpdir)

        # Create honeypot
        honeypot_path = os.path.join("honeypots", "get_admin_password.py")
        os.makedirs("honeypots", exist_ok=True)
        with open(honeypot_path, "w") as f:
            f.write("print('Fake admin password collector')")

        # Create watcher
        watcher = FileWatcher()
        watcher.update_watch_paths()
        watcher.snapshot = watcher.build_snapshot()

        # Add clean file
        clean_file = os.path.join(tmpdir, "hello.txt")
        with open(clean_file, "w") as f:
            f.write("Safe content")

        time.sleep(1)
        watcher.start()  # normally runs forever, simulate internal methods

        # Add malicious file
        malicious_file = os.path.join(tmpdir, "hack.py")
        with open(malicious_file, "w") as f:
            f.write("import subprocess")

        time.sleep(2)
        watcher.update_watch_paths()
        watcher.snapshot = watcher.build_snapshot()

        # Simulate one scan cycle
        new_snapshot = watcher.build_snapshot()
        for path in new_snapshot:
            if path not in watcher.snapshot or watcher.snapshot.get(path) != new_snapshot[path]:
                watcher.scan_file(path)

        # Check quarantine
        quarantined_path = os.path.join("atmshield", "quarantine", "hack.py")
        assert os.path.exists(quarantined_path)

def test_honeypot_deployment():
    mount_point = tempfile.mkdtemp()
    honeypot_src = os.path.join("honeypots", "get_admin_password.py")
    os.makedirs("honeypots", exist_ok=True)
    with open(honeypot_src, "w") as f:
        f.write("# honeypot")

    # Call deploy method directly
    # from atmshield.filewatcher import FileWatcher
    FileWatcher.deploy_honeypot_to_usb(mount_point)

    target_file = os.path.join(mount_point, "get_admin_password.py")
    assert os.path.exists(target_file)
    shutil.rmtree(mount_point)
