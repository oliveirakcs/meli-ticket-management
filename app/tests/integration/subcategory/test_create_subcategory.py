"""
Tests for the API endpoints related to subcategories,
specifically focusing on the creation function.
"""

from app.tests import create_client

client = create_client()


def test_create_subcategory(access_token, category):
    """
    Test creating a new subcategory and verify the response.

    Args:
        access_token (str): The access token for authorization.
        category (dict): The parent category for the subcategory.

    Test steps:
    1. Send a request to create a new subcategory.
    2. Verify the response status code, expecting 201 (Created).
    3. Validate that the subcategory has the correct name and parent category.
    """
    response = client.post(
        "/api/v1/subcategories/",
        json={"name": "New Subcategory", "category_id": category["id"]},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Subcategory"
    assert data["category_id"] == category["id"]


def test_create_duplicate_subcategory(access_token, subcategory):
    """
    Test creating a duplicate subcategory and verify the response.

    Args:
        access_token (str): The access token for authorization.
        subcategory (dict): The existing subcategory data.

    Test steps:
    1. Attempt to create a subcategory with the same name and category as an existing one.
    2. Verify the response status code, expecting 409 (Conflict).
    """
    response = client.post(
        "/api/v1/subcategories/",
        json={"name": subcategory["name"], "category_id": subcategory["category_id"]},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 409


def test_create_subcategory_unauthorized(category):
    """
    Test creating a subcategory without authorization.

    Args:
        category (dict): The parent category for the subcategory.

    Test steps:
    1. Send a request to create a subcategory without an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    response = client.post(
        "/api/v1/subcategories/",
        json={"name": "Unauthorized Subcategory", "category_id": category["id"]},
    )
    assert response.status_code == 401


def test_create_subcategory_with_invalid_data(access_token):
    """
    Test creating a subcategory with invalid data and verify the response.

    Args:
        access_token (str): The access token for authorization.
        category (dict): The parent category for the subcategory.

    Test steps:
    1. Send a request to create a subcategory with invalid data.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.post(
        "/api/v1/subcategories/",
        json={"name": "", "category_id": 9},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422
