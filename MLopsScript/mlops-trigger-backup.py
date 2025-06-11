import os
import time
import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

DATA_URL = os.getenv("DATA_URL", "http://35.154.27.230/data")
TRIGGER_URL = os.getenv("TRIGGER_URL", "http://35.154.27.230/metrics")
WINDOW_SIZE = 10
SPIKE_THRESHOLD = 2

def fetch_data():
    response = requests.get(DATA_URL)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df = df.sort_values(by="time")
    return df

def trigger_metrics():
    print("⚡ Triggering /metrics to fetch more data...")
    response = requests.get(TRIGGER_URL)
    print("✅ Triggered:", response.status_code)

def wait_for_enough_data():
    retries = 10
    for i in range(retries):
        df = fetch_data()
        if len(df) >= WINDOW_SIZE + 1:
            print(f"✅ Sufficient data received: {len(df)} rows")
            return df
        print(f"⏳ Only {len(df)} rows. Retrying after 60s...")
        trigger_metrics()
        time.sleep(60)
    raise Exception("❌ Failed to get enough data after multiple retries.")

def generate_training_data(df):
    X, y = [], []
    for i in range(len(df) - WINDOW_SIZE):
        cpu_window = df["cpu"].iloc[i:i+WINDOW_SIZE].tolist()
        mem_window = df["memory"].iloc[i:i+WINDOW_SIZE].tolist()
        features = cpu_window + mem_window
        label = int(any(cpu > SPIKE_THRESHOLD for cpu in cpu_window))
        X.append(features)
        y.append(label)
    return np.array(X), np.array(y)

def train_and_save_model(X, y):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, "cpu_spike_model.pkl")
    print("📦 Model saved as cpu_spike_model.pkl")

def main():
    df = wait_for_enough_data()
    X, y = generate_training_data(df)
    print(f"📊 Training on {len(X)} samples")
    train_and_save_model(X, y)

if __name__ == "__main__":
    main()

