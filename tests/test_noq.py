from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_users():
    response = client.get("/users")
    assert response.status_code == 200
    json_data = dict(response.json()[0])
    assert len(json_data["name"]) > 0


def test_create_user():
    data = {
        "name": "Victoria",
        "phone": "0708504033",
        "email": "victoria@queen.se",
        "unokod": "123",
    }
    response = client.post("/users", json=data)
    assert response.status_code == 200


def test_hosts():
    response = client.get("/hosts")
    assert response.status_code == 200
    json_data = dict(response.json()[0])
    assert len(json_data["name"]) > 0


def test_reservations():
    response = client.get("/reservations")
    assert response.status_code == 200
    json_data = dict(response.json()[0])
    assert int(json_data["user_id"]) > 0


def test_host_with_reservations():
    response = client.get("/hosts/1")
    assert response.status_code == 200
    json_data = dict(response.json())["reservations"]
    assert len(json_data) > 0


def test_generate():
    response = client.get("/generate")
    assert response.status_code == 200
