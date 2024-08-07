"""
Integration tests for the login endpoint in the authentication system.
"""

import os
from app.tests import create_client

client = create_client()


def test_login_success():
    """
    Test the login endpoint for successful authentication.

    Args:
        user (User): The test user fixture.

    Test steps:
    1. Send a POST request to the login endpoint with valid credentials.
    2. Verify the response status code is 200 (OK).
    3. Check the presence of an access token in the response.
    """
    response = client.post(
        url="/api/v1/login/", data={"username": os.environ.get("SYSADMIN_USERNAME"), "password": os.environ.get("SYSADMIN_PASSWORD")}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_username(access_token):
    """
    Test the login endpoint with an invalid username.

    Args:
        test_db_session (Session): The test database session.

    Test steps:
    1. Send a POST request to the login endpoint with an invalid username.
    2. Verify the response status code is 401 (Unauthorized).
    """
    response = client.post(
        "/api/v1/login/", data={"username": "invalid_user", "password": "password123"}, headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_invalid_password(access_token, user):
    """
    Test the login endpoint with an invalid password.

    Args:
        user (User): The test user fixture.

    Test steps:
    1. Send a POST request to the login endpoint with an invalid password.
    2. Verify the response status code is 401 (Unauthorized).
    """
    response = client.post(
        "/api/v1/login/",
        data={"username": user["username"], "password": "wrongpassword"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect password"


def test_login_empty_credentials(access_token):
    """
    Test the login endpoint with empty credentials.

    Test steps:
    1. Send a POST request to the login endpoint with empty credentials.
    2. Verify the response status code is 422 (Unprocessable Entity).
    """
    response = client.post("/api/v1/login/", data={"username": "", "password": ""}, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 422


def test_login_without_password(user, access_token):
    """
    Test the login endpoint without a password.

    Args:
        user (User): The test user fixture.

    Test steps:
    1. Send a POST request to the login endpoint without a password.
    2. Verify the response status code is 422 (Unprocessable Entity).
    """
    response = client.post(
        "/api/v1/login/",
        data={"username": user["username"], "password": ""},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_login_without_username(access_token):
    """
    Test the login endpoint without a username.

    Test steps:
    1. Send a POST request to the login endpoint without a username.
    2. Verify the response status code is 422 (Unprocessable Entity).
    """
    response = client.post(
        "/api/v1/login/",
        data={"username": "", "password": "password123"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422
