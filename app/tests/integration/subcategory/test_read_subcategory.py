"""
Tests for reading subcategories via API endpoints.
"""

from app.tests import create_client

client = create_client()


def test_read_subcategory_by_id(access_token, subcategory):
    """
    Test reading a specific subcategory by its ID.

    Args:
        access_token (str): The access token for authorization.
        subcategory (dict): Dictionary containing information about the created subcategory.

    Test steps:
    1. Send a request to fetch the subcategory by ID.
    2. Verify the response status code.
    3. Parse the response and validate the subcategory information.
    """
    response = client.get(
        f"/api/v1/subcategories/{subcategory['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == subcategory["id"]
    assert data["name"] == subcategory["name"]


def test_read_non_existing_subcategory(access_token):
    """
    Test reading a non-existent subcategory and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to read a subcategory by a non-existent ID.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.get(
        "/api/v1/subcategories/non_existing_id",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_read_subcategory_unauthorized(subcategory):
    """
    Test reading a subcategory without authorization.

    Args:
        subcategory (dict): Dictionary containing information about the created subcategory.

    Test steps:
    1. Send a request to read a subcategory without providing an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    response = client.get(f"/api/v1/subcategories/{subcategory['id']}")
    assert response.status_code == 401
