from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_users():
    response = client.get("/user")
    assert response.status_code == 200
    json_data = dict(response.json()[0])
    assert len(json_data["name"]) > 0


def test_hosts():
    response = client.get("/host")
    assert response.status_code == 200
    json_data = dict(response.json()[0])
    assert len(json_data["name"]) > 0


def test_reservations():
    response = client.get("/reservation")
    assert response.status_code == 200
    json_data = dict(response.json()[0])
    assert int(json_data["user_id"]) > 0
