"""
Tests for the API endpoints related to users,
specifically focusing on the deletion function.
"""

from app.tests import create_client

client = create_client()


def test_delete_user(access_token, user_to_delete_test):
    """
    Test deleting a user and verify the response.

    Args:
        access_token (str): The access token for authorization.
        user_to_delete_test (dict): Dictionary containing information about the user to delete.

    Test steps:
    1. Send a request to delete a user with a valid access token and an existing user UUID.
    2. Verify the response status code, expecting 202 (Accepted).
    """
    response = client.delete(url=f"/api/v1/users/?user_id={user_to_delete_test['id']}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 202


def test_delete_non_existing_user(access_token):
    """
    Test deleting a non-existent user and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to delete a user with a valid access token and a non-existent user UUID.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.delete("/api/v1/users/?user_id=non_existing_id'", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 422


def test_delete_user_unauthorized():
    """
    Test deleting a user without authorization and verify the response.

    Test steps:
    1. Send a request to delete a user without providing an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    response = client.delete(url="/api/v1/users/?user_id=uuid")
    assert response.status_code == 401
