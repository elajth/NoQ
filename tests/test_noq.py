from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_generate():
    response = client.get("/generate")
    assert response.status_code == 200


def test_users():
    response = client.get("/users")
    assert response.status_code == 200
    # json_data = dict(response.json()[0])
    # assert len(json_data["name"]) > 0


def test_add_user():
    person = {
        "name": "Victoria",
        "phone": "0708504033",
        "email": "victoria@queen.se",
        "unokod": "123",
    }
    response = client.post("/users", json=person)
    assert response.status_code == 200
    user_id = response.json()["id"]
    assert user_id is not None and user_id > 0


def test_hosts():
    response = client.get("/hosts")
    assert response.status_code == 200
    json_data = dict(response.json()[0])
    assert len(json_data["name"]) > 0
