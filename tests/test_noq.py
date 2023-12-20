from fastapi.testclient import TestClient
from main import app
from icecream import ic


client = TestClient(app)


def test_generate():
    response = client.get("/generate")
    assert response.status_code == 200


def test_users():
    response = client.get("/users")
    assert response.status_code == 200
    # json_data = dict(response.json()[0])
    # assert len(json_data["name"]) > 0


def test_add_and_update_user():
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

    # Update data
    person = {"name": "Lisa"}
    response = client.patch(f"/users/{user_id}", json=person)
    assert response.status_code == 200
    name = response.json()["name"]

    assert user_id is not None and name == "Lisa"


def test_hosts():
    response = client.get("/hosts")
    assert response.status_code == 200
    json_data = dict(response.json()[0])
    assert len(json_data["name"]) > 0


def test_add_and_update_host():
    host = {
        "name": "Grimmans Akutboende",
        "address1": "Aspgränd 30",
        "address2": "19836 Sundsvall",
        "count_of_available_places": 3,
        "total_available_places": 3,
    }
    response = client.post("/hosts", json=host)
    assert response.status_code == 200
    host_id = response.json()["id"]
    assert host_id is not None and host_id > 0

    # Update data
    host = {"name": "Stället"}
    response = client.patch(f"/hosts/{host_id}", json=host)
    assert response.status_code == 200
    name = response.json()["name"]

    assert host_id is not None and name == "Stället"
