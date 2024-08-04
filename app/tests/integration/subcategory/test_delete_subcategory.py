"""
Tests for the API endpoints related to subcategories,
specifically focusing on the deletion function.
"""

from app.tests import create_client

client = create_client()


def test_delete_subcategory(access_token, subcategory_to_delete, category_to_delete):
    """
    Test deleting a subcategory and verify the response.

    Args:
        access_token (str): The access token for authorization.
        subcategory_to_delete (dict): Dictionary containing information about the subcategory to delete.

    Test steps:
    1. Send a request to delete a subcategory with a valid access token and an existing subcategory UUID.
    2. Verify the response status code, expecting 204 (No Content).
    """
    response = client.delete(
        url=f"/api/v1/subcategories/{subcategory_to_delete['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


def test_delete_non_existing_subcategory(access_token, category):
    """
    Test deleting a non-existent subcategory and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to delete a subcategory with a valid access token and a non-existent subcategory UUID.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.delete(
        "/api/v1/subcategories/non_existing_id",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_delete_subcategory_unauthorized(subcategory_to_delete):
    """
    Test deleting a subcategory without authorization.

    Args:
        subcategory_to_delete (dict): Dictionary containing information about the subcategory to delete.

    Test steps:
    1. Send a request to delete a subcategory without providing an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    response = client.delete(url=f"/api/v1/subcategories/{subcategory_to_delete['id']}")
    assert response.status_code == 401
