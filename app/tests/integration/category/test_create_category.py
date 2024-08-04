"""
Tests for the API endpoints related to categories,
specifically focusing on the creation function.
"""

from app.tests import create_client

client = create_client()


def test_create_category(access_token):
    """
    Test creating a new category and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to create a new category.
    2. Verify the response status code, expecting 201 (Created).
    3. Check if the returned category data matches the request data.
    """
    response = client.post(
        "/api/v1/categories/",
        json={
            "name": "New Category",
            "parent_id": None,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    category_data = response.json()
    assert category_data["name"] == "New Category"
    assert category_data["parent_id"] is None


def test_create_duplicate_category(access_token, category):
    """
    Test creating a duplicate category and verify the response.

    Args:
        access_token (str): The access token for authorization.
        category (dict): Dictionary containing information about an existing category.

    Test steps:
    1. Send a request to create a category with the same name as an existing one.
    2. Verify the response status code, expecting 409 (Conflict).
    """
    response = client.post(
        "/api/v1/categories/",
        json={
            "name": category["name"],
            "parent_id": category["parent_id"],
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409


def test_create_category_unauthorized():
    """
    Test creating a category without authorization.

    Test steps:
    1. Send a request to create a category without an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    response = client.post(
        "/api/v1/categories/",
        json={
            "name": "Unauthorized Category",
            "parent_id": None,
        },
    )
    assert response.status_code == 401


def test_create_category_with_invalid_data(access_token):
    """
    Test creating a category with invalid data and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to create a category with invalid data.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.post(
        "/api/v1/categories/",
        json={
            "name": "",
            "parent_id": "invalid-uuid",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422
