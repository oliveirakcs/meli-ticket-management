"""
Tests for the API endpoints related to users,
specifically focusing on the sign up function.
"""

from app.tests import create_client

client = create_client()


def test_signup_duplicate_user(access_token, user):
    """
    Test signing up a duplicate user and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to sign up a user with duplicate information.
    2. Verify the response status code, expecting 409 (Conflict).
    """
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "Test User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password",
            "role": "sysadmin",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409


def test_signup_with_empty_fields(access_token):
    """
    Test signing up with empty fields and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to sign up a user with empty fields.
    2. Verify the response status code, expecting 400 (Bad Request).
    """
    response = client.post(
        "/api/v1/users/",
        json={"name": "", "username": "", "email": "", "password": "", "role": ""},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 400


def test_signup_unauthorized():
    """
    Test signing up without authorization.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to sign up without providing an access token.
    2. Verify the response status code.
    """
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "Test Not Authorized User",
            "username": "notauthorized",
            "email": "notauthorized@example.com",
            "password": "notauthorized",
            "role": "notauthorized",
        },
    )
    assert response.status_code == 401
