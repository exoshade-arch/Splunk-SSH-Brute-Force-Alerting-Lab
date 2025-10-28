#!/opt/splunk/bin/python
import sys
from datetime import datetime

# Path to the log file
LOG_FILE = "/var/log/splunk/alerts.log"

# -------- Argument validation --------
# Expect exactly 2 arguments (src_ip and attempts)
if len(sys.argv) != 3:
    print("ERROR: Expected 2 arguments: <src_ip> <attempts>", file=sys.stderr)
    sys.exit(1)

# Read arguments
src_ip = sys.argv[1].strip()
attempts = sys.argv[2].strip()

# -------- Build log message --------
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
message = f"{timestamp} | ALERT | IP: {src_ip} | Attempts: {attempts} | SSH Brute Force"

# -------- Write to log file --------
with open(LOG_FILE, "a", encoding="utf-8") as f:
    f.write(message + "\n")

# -------- Confirmation --------
print(f"Logged: {src_ip} ({attempts} attempts)")
