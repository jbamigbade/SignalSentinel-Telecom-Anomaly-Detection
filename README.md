# SignalSentinel – Telecom Anomaly Detection (GxP-Compliant)  
![Run SignalSentinel](https://github.com/jbamigbade/SignalSentinel-Telecom-Anomaly-Detection/actions/workflows/run-check.yml/badge.svg)

🔗 [SignalSentinel Dashboard](https://jbamigbade.github.io/SignalSentinel-Telecom-Anomaly-Detection/)

> A GxP-compliant anomaly detection system that identifies suspicious telecom call patterns using machine learning and automated reporting.

---

## 📌 Overview

Spam calls are a growing menace in today's telecom landscape, leading to fraud, data breaches, and consumer mistrust. **SignalSentinel** is an intelligent, automated solution for detecting telecom anomalies using unsupervised machine learning — built with **traceability, compliance, and operational automation** at its core.

---

## 🔍 Use Cases

- 📞 Fraudulent call activity detection
- 🕵️ Call center monitoring and escalation
- 🧪 Unsupervised anomaly detection in telecom logs
- 🧾 GxP-compliant trace logging for audit-ready environments

---

## 🔧 Key Features

- ✅ Caller- and call-level anomaly detection (Isolation Forest)
- 🧠 Feature engineering: duration, hour-of-day, international patterns
- 🧾 GxP-compliant logs with timestamp, username, and traceability
- ⚙️ Automation via `.bat` + Windows Task Scheduler
- 📊 Visual reports using `matplotlib` + `seaborn`
- 📤 Email alerts upon detection
- 🔁 Continuous Integration with GitHub Actions (CI/CD)

---

## 🗂️ Project Structure

📁 SignalSentinel-Telecom-Anomaly-Detection
├── spam_call_anomaly_dual.py # Main ML script (with logging)
├── run_spam_detector.bat # Automation entry point
├── requirements.txt # Python dependencies
├── spam_calls_1000.csv # Sample data
├── output/ # CSVs and plots
├── logs/ # GxP-compliant logs
└── .github/workflows/run-check.yml # CI/CD automation


## Run Instructions

---

## ▶️ How to Run

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

Run: 

python spam_call_anomaly_dual.py


```bash
.\run_spam_detector.bat



logs/ — run_log.txt, error_log.txt, timestamped logs


📈 Output
caller_level_anomalies.csv and call_level_anomalies.csv

top_50_suspicious_calls.csv

Plot images: anomaly visualizations by time + duration

Logged alerts + email notification (SMTP)

✅ CI/CD
This project is automatically tested using GitHub Actions on every push to main.

## 📊 Interactive Dashboard

View the live spam call anomaly detection dashboard:
🔗 [SignalSentinel Dashboard](https://jbamigbade.github.io/SignalSentinel-Telecom-Anomaly-Detection/)
