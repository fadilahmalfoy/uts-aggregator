import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_stress_batch():
    for i in range(50):
        e = {
            "topic": "load",
            "event_id": str(i % 25),  # 50% duplikat
            "timestamp": "2025-10-23T00:00:00Z",
            "source": "pytest",
            "payload": {"id": i}
        }
        response = client.post("/publish", json=e)
        assert response.status_code == 200

    stats = client.get("/stats").json()
    assert stats["received"] >= 50
    assert stats["unique_processed"] <= 50
