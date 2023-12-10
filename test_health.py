from fastapi.testclient import TestClient
from main import app, Host

client = TestClient(app)


def test_health_status():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Health status": "noQ API backend status = OK"}
