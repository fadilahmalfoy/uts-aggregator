import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_invalid_event_schema():
    invalid_event = {"topic": "demo"}  # tidak lengkap
    response = client.post("/publish", json=invalid_event)
    assert response.status_code == 422  # validation error
