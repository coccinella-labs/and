import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat():
    response = client.post("/chat", json={"prompt": "Hello"})
    assert response.status_code == 200
    assert "response" in response.json()


def test_models():
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) > 0


def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert data["model_loaded"] is True
