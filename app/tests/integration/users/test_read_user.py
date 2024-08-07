"""
Tests for API endpoints related to users,
specifically focusing on the read/search functionality.
"""

from app.tests import create_client

client = create_client()


def test_read_all_users(access_token):
    """
    Test reading all users from the API.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to retrieve all users.
    2. Verify the response status code.
    3. Check if there are users returned in the response.
    """
    response = client.get("/api/v1/users/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_read_non_existing_user(access_token):
    """
    Test reading a user by a non-existing ID.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to retrieve a user with a non-existing ID.
    2. Verify the response status code.
    """
    response = client.get("/api/v1/users/non_existing_id", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 422


def test_read_user_by_id(access_token, user):
    """
    Test read an specific user by their ID.

    Args:
        access_token (str): The access token for authorization.
        user (dict): Dictionary containing information about the created user.

    Test steps:
    1. Send a request to fetch the user by ID.
    2. Verify the response status code.
    3. Parse the response and store user information.
    """

    response = client.get(f"/api/v1/users/{user['id']}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == user["id"]
    assert user["name"] == user["name"]


def test_read_all_users_unauthorized():
    """
    Test reading all users without authorization.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to retrieve all users without providing an access token.
    2. Verify the response status code.
    """
    response = client.get("/api/v1/users/")
    assert response.status_code == 401
