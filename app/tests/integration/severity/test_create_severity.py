"""
Tests for the API endpoints related to severity,
specifically focusing on the creation function.
"""

from app.tests import create_client

client = create_client()


def test_create_severity_level_1_handled_externally(access_token):
    """
    Test creating a severity level 1 and verify it returns the correct message.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to create a severity level 1.
    2. Verify the response status code, expecting 400 (Bad Request).
    3. Check if the correct message is returned indicating that level 1 is handled externally.
    """
    response = client.post(
        "/api/v1/severities/",
        json={
            "level": 1,
            "description": "Critical severity level",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Severity level 1 is handled by another team. Please contact the dedicated support team."


def test_create_duplicate_severity(access_token, severity):
    """
    Test creating a duplicate severity level and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to create a severity level that already exists.
    2. Verify the response status code, expecting 409 (Conflict).
    """
    response = client.post(
        "/api/v1/severities/",
        json={
            "level": severity["level"],
            "description": severity["description"],
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409


def test_create_severity_unauthorized():
    """
    Test creating a severity level without authorization.

    Test steps:
    1. Send a request to create a severity level without an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    response = client.post(
        "/api/v1/severities/",
        json={
            "level": 3,
            "description": "Medium severity level",
        },
    )
    assert response.status_code == 401


def test_create_severity_with_invalid_data(access_token):
    """
    Test creating a severity level with invalid data and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to create a severity level with invalid data.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.post(
        "/api/v1/severities/",
        json={
            "level": "invalid",
            "description": "",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_create_severity_with_missing_data(access_token):
    """
    Test creating a severity level with missing data and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to create a severity level with missing required fields.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.post(
        "/api/v1/severities/",
        json={},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422
