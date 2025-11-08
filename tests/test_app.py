import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success():
    email = "nuevo@mergington.edu"
    response = client.post("/activities/Chess Club/signup?email=" + email)
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Verifica que el participante fue agregado
    get_resp = client.get("/activities")
    assert email in get_resp.json()["Chess Club"]["participants"]


def test_signup_for_activity_already_signed_up():
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    response = client.post("/activities/NoExiste/signup?email=alguien@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant():
    # Primero agrega un participante
    email = "delete@mergington.edu"
    client.post("/activities/Chess Club/signup?email=" + email)
    # Ahora elimina
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    # Verifica que fue eliminado
    get_resp = client.get("/activities")
    assert email not in get_resp.json()["Chess Club"]["participants"]
