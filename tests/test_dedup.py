import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_deduplication():
    event = {
        "topic": "demo",
        "event_id": "abc123",
        "timestamp": "2025-10-23T00:00:00Z",
        "source": "pytest",
        "payload": {"msg": "Hello"}
    }
    client.post("/publish", json=event)
    client.post("/publish", json=event)
    stats = client.get("/stats").json()
    assert stats["unique_processed"] == 1
    assert stats["duplicate_dropped"] >= 0
