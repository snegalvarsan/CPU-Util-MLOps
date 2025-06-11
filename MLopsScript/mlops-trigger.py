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
SPIKE_THRESHOLD = 3
TRIGGER_INTERVAL = 60    # 1 minute during active monitoring
IDLE_INTERVAL = 300     # 30 minutes during idle
RETRAIN_EVERY_N_CYCLES = 2  # Retrain every N full cycles

def fetch_data():
    response = requests.get(DATA_URL)
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df = df.sort_values(by="time")
    return df

def trigger_metrics():
    print("⚡ Triggering /metrics endpoint...")
    try:
        response = requests.get(TRIGGER_URL)
        print("✅ Triggered:", response.status_code)
    except Exception as e:
        print("❌ Failed to trigger /metrics:", e)

def wait_for_enough_data():
    df = fetch_data()
    if len(df) >= WINDOW_SIZE + 1:
        print(f"✅ Sufficient data: {len(df)} rows")
        return df
    else:
        print(f"⏳ Not enough data ({len(df)} rows), calling /metrics")
        trigger_metrics()
        return None

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
    return model

def predict_spike(model, latest_window):
    features = latest_window["cpu"].tolist() + latest_window["memory"].tolist()
    return model.predict([features])[0]

def main_loop():
    model = None
    cycles = 0
    last_trigger_time = 0

    while True:
        df = fetch_data()
        if len(df) < WINDOW_SIZE + 1:
            print("⚠️ Not enough data, triggering and retrying...")
            trigger_metrics()
            time.sleep(TRIGGER_INTERVAL)
            continue

        if model is None or cycles % RETRAIN_EVERY_N_CYCLES == 0:
            print("🔁 Training new model...")
            X, y = generate_training_data(df)
            model = train_and_save_model(X, y)

        latest_window = df.iloc[-WINDOW_SIZE:]
        prediction = predict_spike(model, latest_window)

        if prediction == 1:
            print("🚨 Spike predicted! Triggering metrics...")
            trigger_metrics()
            time.sleep(TRIGGER_INTERVAL)  # check again quickly
        else:
            print("🟢 No spike predicted. Sleeping for 30 minutes.")
            time.sleep(IDLE_INTERVAL)

        cycles += 1

if __name__ == "__main__":
    main_loop()

