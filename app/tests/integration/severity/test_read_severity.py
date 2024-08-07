"""
Tests for the API endpoints related to severity,
specifically focusing on the read/search functionality.
"""

from app.tests import create_client

client = create_client()


def test_read_all_severities(access_token):
    """
    Test reading all severity levels from the API.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to retrieve all severity levels.
    2. Verify the response status code.
    3. Check if there are severity levels returned in the response.
    """
    response = client.get("/api/v1/severities/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_read_non_existing_severity(access_token):
    """
    Test reading a severity level by a non-existing ID.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to retrieve a severity level with a non-existing ID.
    2. Verify the response status code.
    """
    response = client.get("/api/v1/severities/non_existing_id", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 422


def test_read_severity_by_id(access_token, severity):
    """
    Test read a specific severity level by its ID.

    Args:
        access_token (str): The access token for authorization.
        severity (dict): Dictionary containing information about the created severity level.

    Test steps:
    1. Send a request to fetch the severity level by ID.
    2. Verify the response status code.
    3. Parse the response and store severity information.
    """
    response = client.get(f"/api/v1/severities/{severity['id']}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    severity_data = response.json()
    assert severity_data["id"] == severity["id"]
    assert severity_data["level"] == severity["level"]
    assert severity_data["description"] == severity["description"]


def test_read_all_severities_unauthorized():
    """
    Test reading all severity levels without authorization.

    Test steps:
    1. Send a request to retrieve all severity levels without providing an access token.
    2. Verify the response status code.
    """
    response = client.get("/api/v1/severities/")
    assert response.status_code == 401
