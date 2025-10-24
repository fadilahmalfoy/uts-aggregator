import requests
import time
import json
import random

aggregator_url = "http://aggregator:8000/publish"

topics = ["demo", "sensor", "log"]
for i in range(20):
    event = {
        "topic": random.choice(topics),
        "event_id": str(i % 10),  # 50% duplikat
        "timestamp": "2025-10-23T00:00:00Z",
        "source": "publisher",
        "payload": {"msg": f"Event {i}"}
    }
    try:
        res = requests.post(aggregator_url, json=event)
        print(f"Sent event {i}: {res.status_code}")
    except Exception as e:
        print("Failed to send:", e)
    time.sleep(0.5)
