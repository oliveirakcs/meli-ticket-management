"""
Tests for the API endpoints related to severity,
specifically focusing on the deletion function.
"""

from app.tests import create_client

client = create_client()


def test_delete_severity(access_token, severity_to_delete):
    """
    Test deleting a severity level and verify the response.

    Args:
        access_token (str): The access token for authorization.
        severity_to_delete (dict): Dictionary containing information about the severity to delete.

    Test steps:
    1. Send a request to delete a severity level with a valid access token and an existing severity UUID.
    2. Verify the response status code, expecting 202 (Accepted).
    """
    response = client.delete(
        url=f"/api/v1/severities/?severity_id={severity_to_delete['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 202


def test_delete_non_existing_severity(access_token):
    """
    Test deleting a non-existent severity level and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to delete a severity level with a valid access token and a non-existent severity UUID.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.delete("/api/v1/severities/?severity_id=non_existing_id", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 422


def test_delete_severity_unauthorized(severity):
    """
    Test deleting a severity level without authorization and verify the response.

    Args:
        severity (dict): Dictionary containing information about the severity to delete.

    Test steps:
    1. Send a request to delete a severity level without providing an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    response = client.delete(
        url=f"/api/v1/severities/?severity_id={severity['id']}",
    )
    assert response.status_code == 401
