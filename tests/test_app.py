import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Basketball" in data
    assert "Tennis Club" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Basketball/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Basketball" in response.json()["message"]

    # Clean up: remove the test participant
    client.post("/activities/Basketball/unregister", params={"email": "newstudent@mergington.edu"})

def test_signup_for_activity_already_signed_up():
    # Use an existing participant
    response = client.post("/activities/Basketball/signup", params={"email": "alex@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_success():
    # Add a participant, then remove
    client.post("/activities/Drama Club/signup", params={"email": "temp@mergington.edu"})
    response = client.post("/activities/Drama Club/unregister", params={"email": "temp@mergington.edu"})
    assert response.status_code == 200
    assert "Removed temp@mergington.edu from Drama Club" in response.json()["message"]

def test_unregister_from_activity_not_registered():
    response = client.post("/activities/Drama Club/unregister", params={"email": "notregistered@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"

def test_unregister_from_nonexistent_activity():
    response = client.post("/activities/Nonexistent/unregister", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
