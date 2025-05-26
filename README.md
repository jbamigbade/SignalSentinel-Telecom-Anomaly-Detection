# SignalSentinel – Telecom Anomaly Detection (GxP-Compliant)

![GitHub Workflow Status](https://github.com/jbamigbade/SignalSentinel-Telecom-Anomaly-Detection/actions/workflows/run-check.yml/badge.svg)

A GxP-compliant anomaly detection system for identifying suspicious telecom call activity using machine learning.

## Key Features

- 📡 Call and caller-level anomaly detection (Isolation Forest)
- 🧠 Feature engineering: call duration, time-of-day, international flags
- ✅ GxP-compliant logs with user, timestamp, and traceability
- 🕒 Scheduled automation using Windows Task Scheduler
- 📊 CSV reports + matplotlib/seaborn visual plots
- 📧 Email alert notifications

## Run Instructions

```bash
.\run_spam_detector.bat

File Structure
spam_call_anomaly_dual.py — ML + logging script

run_spam_detector.bat — automation entry point

logs/ — run_log.txt, error_log.txt, timestamped logs

output/ — CSV reports and PNG plots