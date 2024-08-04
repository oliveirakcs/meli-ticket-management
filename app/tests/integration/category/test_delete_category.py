"""
Tests for the API endpoints related to categories,
specifically focusing on the deletion function.
"""

from app.tests import create_client

client = create_client()


def test_delete_category(access_token, category_to_delete):
    """
    Test deleting a category and verify the response.

    Args:
        access_token (str): The access token for authorization.
        category_to_delete (dict): Dictionary containing information about the category to delete.

    Test steps:
    1. Send a request to delete a category with a valid access token and an existing category UUID.
    2. Verify the response status code, expecting 202 (Accepted).
    """
    response = client.delete(
        url=f"/api/v1/categories/?category_id={category_to_delete['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 202


def test_delete_non_existing_category(access_token):
    """
    Test deleting a non-existent category and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to delete a category with a valid access token and a non-existent category UUID.
    2. Verify the response status code, expecting 404 (Not Found).
    """
    response = client.delete(
        "/api/v1/categories/?category_id=non_existing_id",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_delete_category_unauthorized(category_to_delete):
    """
    Test deleting a category without authorization and verify the response.

    Args:
        category_to_delete (dict): Dictionary containing information about the category to delete.

    Test steps:
    1. Send a request to delete a category without providing an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    response = client.delete(url=f"/api/v1/categories/?category_id={category_to_delete['id']}")
    assert response.status_code == 401
