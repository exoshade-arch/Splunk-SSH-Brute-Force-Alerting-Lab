# Splunk SSH Brute Force Alerting Lab

## Overview
This lab demonstrates **real-time SSH brute force alerting** using **Splunk Enterprise**.  
It includes:
- Monitoring of `/var/log/auth.log`
- Custom SPL query with IP extraction, geolocation, and severity scoring
- **Scheduled alert** (every 5 minutes) with **automated script execution**
- Persistent incident logging via Python script

---

## Architecture

| Host | IP Address | Role |
|------|------------|------|
| **Splunk + SSH Target** | `192.168.50.20` | Ubuntu 22.04 + Splunk Enterprise + OpenSSH server |
| **Attacker** | `192.168.50.40` | Kali Linux with Hydra |

> All logs are ingested in real-time via Splunk `monitor` input.

---

## 1. Splunk Configuration

### 1.1 Create Index
```bash
# Via Splunk Web: Settings → Indexes → New Index
Index name: linux_security
1.2 Add Monitor for SSH Logs
bashsudo /opt/splunk/bin/splunk add monitor /var/log/auth.log \
  -index linux_security \
  -sourcetype linux_secure

2. SPL Query (Search Processing Language)

splindex=linux_security sourcetype=linux_secure "Failed password"
| rex field=_raw "from (?<src_ip>\d+\.\d+\.\d+\.\d+) port"
| stats count as attempts by src_ip
| where attempts >= 5
| iplocation src_ip
| eval severity = case(
    attempts >= 20, "HIGH",
    attempts >= 10, "MEDIUM",
    attempts >= 5,  "LOW"
)
| table src_ip attempts Country Region City severity

All SPL commands were manually typed in the Splunk search bar.


3. Scheduled Alert

Name: Brute Force - multiple failed SSH logins
--
App: search
--
Schedule: */5 * * * * (every 5 minutes)
--
Trigger Condition: Number of Results > 0
--
Action: Run a script

Script Call:
textalert_log_incident.py $result.src_ip$ $result.attempts$

Script: alert_log_incident.py (attached in repository)
Path: /opt/splunk/bin/scripts/alert_log_incident.py
Permissions: splunk:splunk, 755


4. Incident Log Output

bash2025-10-28 19:29:03 | ALERT | IP: 192.168.50.40 | Pokusaja: 7 | SSH Brute Force

File: /var/log/splunk/alerts.log
Owner: splunk:splunk
Permissions: 664


5. Attack Simulation (Hydra on Kali)

bashhydra -l testuser -P ~/passlist.txt 192.168.50.20 ssh -t 4 -V

Generated 7+ failed login attempts → detected and logged by Splunk.


6. Conclusion

This alerting lab successfully demonstrates:

- Automated detection of SSH brute force attempts
- Scheduled alert with real-time response
- Custom Python script for persistent incident logging
- Full integration with Splunk’s alerting engine

All components manually configured and tested.
No copy/paste used in production setup.
