from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_detect():
    response = client.post("/detect", json={"type": "image"})
    assert response.status_code == 200
    assert response.json()["type"] == "image"
    assert response.json()["requires_human"] is True

def test_review_is_handoff_only():
    response = client.post("/review", json={
        "provider": "local-test",
        "challenge_id": "fixture-001",
    })
    assert response.status_code == 200
    assert response.json()["status"] == "human_review_required"
