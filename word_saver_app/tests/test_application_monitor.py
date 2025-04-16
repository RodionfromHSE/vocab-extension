import sys
import os

# add the parent directory to the system path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(f"Root directory: {root_dir}")
sys.path.append(root_dir)

from app.utils.application_monitor import ApplicationMonitor
from time import sleep

while True:
    # app_name = get_active_application_name()
    app_monitor = ApplicationMonitor()
    app_name = app_monitor.get_active_application()
    print(f"Active application: {app_name}")
    sleep(1)  # Check every second