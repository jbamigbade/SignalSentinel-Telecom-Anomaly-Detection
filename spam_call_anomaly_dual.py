# spam_call_anomaly_dual.py

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
import logging
import getpass
from datetime import datetime, timezone
import argparse

# === CLI Argument Parsing for logtime sync with .bat ===
parser = argparse.ArgumentParser()
parser.add_argument("--logtime", required=False, help="Log timestamp from batch file")
args = parser.parse_args()
LOGTIME = args.logtime or datetime.now(timezone.utc).isoformat()

# === GxP-Compliant Logging Setup ===
os.makedirs('logs', exist_ok=True)
USERNAME = getpass.getuser()

class GxPFormatter(logging.Formatter):
    def format(self, record):
        timestamp = LOGTIME
        base = super().format(record)
        return f"{timestamp} | User: {USERNAME} | {base}"

# Run log setup
run_handler = logging.FileHandler('logs/run_log.txt', mode='a')
run_handler.setFormatter(GxPFormatter('%(levelname)s | %(message)s'))
run_logger = logging.getLogger('run_logger')
run_logger.setLevel(logging.INFO)
run_logger.addHandler(run_handler)
run_logger.propagate = False

# Error log setup
error_handler = logging.FileHandler('logs/error_log.txt', mode='a')
error_handler.setFormatter(GxPFormatter('%(levelname)s | %(message)s'))
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)
error_logger.propagate = False

# === Load environment variables ===
load_dotenv()
SENDER = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER = os.getenv("EMAIL_RECEIVER")

# === Shared Plot ===
def plot_and_save(df, x_col, y_col, title, plot_path):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_col, y=y_col, hue='Anomaly', palette={0: 'blue', 1: 'red'})
    plt.title(title)
    plt.savefig(plot_path)
    plt.close()

# === 1. Caller-Level Aggregation ===
def caller_level_anomaly(df):
    try:
        df['CallStartTime'] = pd.to_datetime(df['CallStartTime'])
        df['Hour'] = df['CallStartTime'].dt.hour
        df['IsNightCall'] = df['Hour'].apply(lambda x: 1 if x < 6 or x > 22 else 0)
        df['IsInternational'] = df['ReceiverID'].apply(lambda x: 1 if str(x).startswith('+') else 0)

        caller_df = df.groupby('CallerID').agg(
            calls_per_hour=('CallerID', 'count'),
            avg_duration=('CallDuration', 'mean'),
            unique_receivers=('ReceiverID', 'nunique'),
            night_calls=('IsNightCall', 'sum'),
            intl_calls=('IsInternational', 'sum')
        ).fillna(0)

        scaler = StandardScaler()
        scaled = scaler.fit_transform(caller_df)
        model = IsolationForest(contamination=0.05, random_state=42)
        model.fit(scaled)
        scores = model.decision_function(scaled) * -1
        flags = model.predict(scaled)

        caller_df['AnomalyScore'] = scores
        caller_df['Anomaly'] = [1 if f == -1 else 0 for f in flags]
        return caller_df
    except Exception as e:
        error_logger.error(f"Caller-level anomaly detection failed: {e}")
        raise

# === 2. Call-Level Detection (with top 50 export) ===
def call_level_anomaly(df, output_dir):
    try:
        df['CallStartTime'] = pd.to_datetime(df['CallStartTime'])
        df['Hour'] = df['CallStartTime'].dt.hour
        df['IsNightCall'] = df['Hour'].apply(lambda x: 1 if x < 6 or x > 22 else 0)
        df['IsInternational'] = df['ReceiverID'].apply(lambda x: 1 if str(x).startswith('+') else 0)

        features = df[["CallDuration", "Hour", "IsNightCall", "IsInternational"]]
        scaler = StandardScaler()
        scaled = scaler.fit_transform(features)

        model = IsolationForest(contamination=0.05, random_state=42)
        model.fit(scaled)
        scores = model.decision_function(scaled) * -1
        flags = model.predict(scaled)

        df['AnomalyScore'] = scores
        df['Anomaly'] = [1 if f == -1 else 0 for f in flags]

        df_sorted = df.sort_values(by='AnomalyScore', ascending=False)

        top_50 = df_sorted[df_sorted['Anomaly'] == 1].head(50)
        top_50_path = os.path.join(output_dir, "top_50_suspicious_calls.csv")
        top_50_plot = os.path.join(output_dir, "top_50_plot.png")

        top_50.to_csv(top_50_path, index=False)
        plot_and_save(top_50, "CallDuration", "Hour", "Top 50 Suspicious Calls", top_50_plot)

        return df_sorted
    except Exception as e:
        error_logger.error(f"Call-level anomaly detection failed: {e}")
        raise

# === Email Alert ===
def send_email_alert():
    subject = "Spam Call Anomaly Alert"
    body = "Anomaly detection complete. Caller-level and call-level reports, including the Top 50 suspicious calls, have been saved."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER
    msg['To'] = RECEIVER

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, RECEIVER, msg.as_string())
        print("[OK] Email alert sent successfully.")
        run_logger.info("Email alert sent successfully.")
    except Exception as e:
        print(f"[FAIL] Failed to send email: {e}")
        error_logger.error(f"Failed to send email: {e}")

# === Runner ===
def run_dual_anomaly(input_path, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
        df = pd.read_csv(input_path)
        caller_df = caller_level_anomaly(df)
        call_df = call_level_anomaly(df, output_dir)

        caller_path = os.path.join(output_dir, "caller_level_anomalies.csv")
        call_path = os.path.join(output_dir, "call_level_anomalies.csv")
        caller_plot = os.path.join(output_dir, "caller_plot.png")
        call_plot = os.path.join(output_dir, "call_plot.png")

        caller_df.to_csv(caller_path)
        call_df.to_csv(call_path)

        plot_and_save(caller_df, "calls_per_hour", "avg_duration", "Caller-Level Anomalies", caller_plot)
        plot_and_save(call_df, "CallDuration", "Hour", "Call-Level Anomalies", call_plot)

        print(f"[OK] Caller-level saved to {caller_path}")
        print(f"[OK] Call-level saved to {call_path}")
        print("[OK] Top 50 suspicious calls saved and plotted.")

        run_logger.info(f"Caller-level saved to {caller_path}")
        run_logger.info(f"Call-level saved to {call_path}")
        run_logger.info("Top 50 suspicious calls saved and plotted.")

        if SENDER and PASSWORD and RECEIVER:
            send_email_alert()
    except Exception as e:
        error_logger.error(f"Script execution failed: {e}")
        raise

# === Entry Point ===
if __name__ == "__main__":
    input_path = "spam_calls_1000.csv"
    output_dir = "output"
    run_dual_anomaly(input_path, output_dir)

