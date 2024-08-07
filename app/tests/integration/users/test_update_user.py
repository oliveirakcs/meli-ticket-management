"""
Tests for the API endpoints related to users,
specifically focusing on the update function.
"""

from app.tests import create_client

client = create_client()


def test_update_all_fields_user(access_token, user):
    """
    Test updating an existing user's information and verify the response.

    Args:
        access_token (str): The access token for authorization.
        user (dict): Dictionary containing information about the created user.

    Test steps:
    1. Send a request to update the user's information.
    2. Verify the response status code, expecting 200 (OK).
    3. Check if the user's information has been updated correctly.
    """
    updated_name = "Updated Name"
    response = client.patch(
        f"/api/v1/users/{user['id']}",
        json={"name": updated_name, "username": user["username"], "email": user["email"]},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    updated_user_data = response.json()
    assert updated_user_data["name"] == updated_name


def test_update_one_field_user(access_token, user):
    """
    Test updating a single field an existing user's information and verify the response.

    Args:
        access_token (str): The access token for authorization.
        user (dict): Dictionary containing information about the created user.

    Test steps:
    1. Send a request to update the user's information.
    2. Verify the response status code, expecting 200 (OK).
    3. Check if the user's information has been updated correctly.
    """
    updated_name = "New Name"
    response = client.patch(f"/api/v1/users/{user['id']}", json={"name": updated_name}, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    updated_user_data = response.json()
    assert updated_user_data["name"] == updated_name


def test_update_non_existing_user(access_token):
    """
    Test updating a non-existent user's information and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to update a non-existent user's information.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.patch(
        "/api/v1/users/non_existing_id",
        json={"name": "Updated Name", "username": "updated_username", "email": "updated@example.com"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_update_user_unauthorized(user):
    """
    Test updated an userwithout authorization.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to update an user without providing an access token.
    2. Verify the response status code.
    """
    updated_name = "Updated Name"
    response = client.patch(
        f"/api/v1/users/{user['id']}",
        json={"name": updated_name, "username": user["username"], "email": user["email"]},
    )
    assert response.status_code == 401
