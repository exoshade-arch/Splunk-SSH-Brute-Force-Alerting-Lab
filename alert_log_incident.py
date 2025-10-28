#!/opt/splunk/bin/python
import sys
from datetime import datetime

LOG_FILE = "/var/log/splunk/alerts.log"

if len(sys.argv) != 3:
   print("GRESKA: Ocekivana 2 argumenta", file=sys.stderr)
   sys.exit(1)

src_ip = sys.argv[1].strip()
attempts = sys.argv[2].strip()

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
message = f"{timestamp} | ALERT | IP: {src_ip} | Pokusaja: {attempts} | SSH Brute Force"

with open(LOG_FILE, "a", encoding="utf-8") as f:
    f.write(message + "\n")

print(f"Logovano: {src_ip} ({attempts} pokusaja)")