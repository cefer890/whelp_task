from fastapi.testclient import TestClient

# Import the FastAPI app instance
from main import app

# Create a test client using the TestClient constructor
client = TestClient(app)


def test_create_user():
    """
    Test case to create a new user.
    """
    # Define the user data
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }

    # Send a POST request to the /api/v1/signup endpoint with user data
    response = client.post("/api/v1/signup", json=user_data)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response contains the message "User created successfully"
    assert response.json()["message"] == "User created successfully"


def test_user_authentication():
    """
    Test case to authenticate a user and obtain access tokens.
    """
    # Define the login data
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Send a POST request to the /api/v1/auth endpoint with login data
    response = client.post("/api/v1/auth", json=login_data)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response contains the keys "access_token", "refresh_token", and "token_type"
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_refresh_token():
    """
    Test case to refresh the access token using a refresh token.
    """
    # Send a POST request to the /api/v1/refresh endpoint with a refresh token data
    response = client.post("/api/v1/refresh", json={"refresh_token": "test_refresh_token"})

    # Assert that the response status code is 401 (Unauthorized) since it's a placeholder test
    assert response.status_code == 401


def test_get_user_details():
    """
    Test case to retrieve user details using an access token.
    """
    # Send a GET request to the /api/v1/user endpoint with an invalid access token
    response = client.get("/api/v1/user", headers={"Authorization": "Bearer invalid_access_token"})

    # Assert that the response status code is 401 (Unauthorized) since it's a placeholder test
    assert response.status_code == 401


def test_create_task():
    """
    Test case to create a new task.
    """
    # Define the task data
    task_data = {
        "ip_address": "127.0.0.1"
    }

    # Send a POST request to the /api/v1/task endpoint with task data
    response = client.post("/api/v1/task", json=task_data)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response contains the expected content
    expected_content = {"status": "processing", "message": "Task submitted successfully"}
    assert response.json() == expected_content


def test_get_task_status():
    """
    Test case to retrieve the status of a task.
    """
    # Send a GET request to the /api/v1/status/{task_id} endpoint with a valid task ID
    response = client.get("/api/v1/status/valid_task_id")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the task status is either completed or not_found
    response_data = response.json()
    assert response_data["task_status"] in ["completed", "not_found"]
