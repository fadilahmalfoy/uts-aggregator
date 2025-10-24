import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_stats_and_events_consistency():
    event = {
        "topic": "sensor",
        "event_id": "1",
        "timestamp": "2025-10-23T00:00:00Z",
        "source": "pytest",
        "payload": {"data": "x"}
    }
    client.post("/publish", json=event)

    stats = client.get("/stats").json()
    events = client.get("/events?topic=sensor").json()

    assert isinstance(events, list)
    assert len(events) <= stats["unique_processed"]
