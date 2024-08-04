"""
Tests for the API endpoints related to severity,
specifically focusing on the update function.
"""

from app.tests import create_client

client = create_client()


def test_update_severity(access_token, severity):
    """
    Test updating an existing severity level and verify the response.

    Args:
        access_token (str): The access token for authorization.
        severity (dict): Dictionary containing information about the created severity level.

    Test steps:
    1. Send a request to update the severity level.
    2. Verify the response status code, expecting 200 (OK).
    3. Check if the severity level has been updated correctly.
    """
    updated_description = "Updated Description"
    response = client.patch(
        f"/api/v1/severities/{severity['id']}",
        json={"description": updated_description},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    updated_severity_data = response.json()
    assert updated_severity_data["description"] == updated_description


def test_update_severity_invalid_data(access_token, severity):
    """
    Test updating an existing severity level with invalid data and verify the response.

    Args:
        access_token (str): The access token for authorization.
        severity (dict): Dictionary containing information about the created severity level.

    Test steps:
    1. Send a request to update the severity level with invalid data.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.patch(
        f"/api/v1/severities/{severity['id']}",
        json={"level": "invalid"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_update_non_existing_severity(access_token):
    """
    Test updating a non-existent severity level and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to update a non-existent severity level.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.patch(
        "/api/v1/severities/non_existing_id",
        json={"description": "Updated Description"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_update_severity_unauthorized(severity):
    """
    Test updating a severity level without authorization and verify the response.

    Args:
        severity (dict): Dictionary containing information about the severity to update.

    Test steps:
    1. Send a request to update a severity level without providing an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    updated_description = "Unauthorized Update"
    response = client.patch(
        f"/api/v1/severities/{severity['id']}",
        json={"description": updated_description},
    )
    assert response.status_code == 401
