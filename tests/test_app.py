import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (No setup needed, just use the client)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Remove if already present (idempotent for test)
    client.post(f"/activities/{activity}/signup?email={email}")
    client.get("/activities")['Chess Club']['participants'] = [p for p in client.get("/activities").json()['Chess Club']['participants'] if p != email]

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json().get("message", "")

    # Cleanup
    client.get("/activities")['Chess Club']['participants'] = [p for p in client.get("/activities").json()['Chess Club']['participants'] if p != email]

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"  # Already present
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

def test_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
