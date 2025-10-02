from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"

def test_version():
    r = client.get("/version")
    assert r.status_code == 200
    body = r.json()
    assert "app" in body and "version" in body

def test_chat_echo():
    r = client.post("/chat",
        headers={"Authorization": "Bearer demo-token"},
        json={"text": "hi"})
    assert r.status_code == 200
    assert "answer" in r.json()
