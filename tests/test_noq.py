from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_generate():
    response = client.get("/generate")
    assert response.status_code == 200


def test_users():
    response = client.get("/users")
    assert response.status_code == 200
    json_data = dict(response.json()[0])
    assert len(json_data["name"]) > 0


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


def test_add_reservation():
    # Add a new User to make sure it is possible to add reservation
    person = {
        "name": "Victor Testsson",
        "phone": "0708504033",
        "email": "victor@test.se",
        "unokod": "100",
    }
    response = client.post("/users", json=person)
    assert response.status_code == 200
    added_user_id = response.json()["id"]

    # Add reservation for new user
    data = {"start_date": "2024-01-01", "user_id": added_user_id, "host_id": 1}
    response = client.post("/reservations", json=data)
    assert response.status_code == 200

    # Samma data ska ge FEL och returkod 400
    response = client.post("/reservations", json=data)
    assert response.status_code == 400


def test_reservations():
    response = client.get("/reservations")
    assert response.status_code == 200
    json_data = dict(response.json()[0])
    assert json_data is not None


def test_host_with_reservations():
    response = client.get("/hosts/1")
    assert response.status_code == 200
    list = dict(response.json())["reservations"]
    assert len(list) > 0


def test_reservation_user():
    response = client.get("/reservations")
    assert response.status_code == 200
    added_rsrv = response.json()[1]["id"]
    
    response = client.get(f"/reservations/{added_rsrv}")
    assert response.status_code == 200
    list = dict(response.json())["user"]
    assert len(list) > 0
