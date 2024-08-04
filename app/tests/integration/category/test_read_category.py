"""
Tests for the API endpoints related to categories,
specifically focusing on the read/search functionality.
"""

from app.tests import create_client

client = create_client()


def test_read_all_categories(access_token):
    """
    Test reading all categories from the API.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to retrieve all categories.
    2. Verify the response status code.
    3. Check if there are categories returned in the response.
    """
    response = client.get("/api/v1/categories/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_read_non_existing_category(access_token):
    """
    Test reading a category by a non-existing ID.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to retrieve a category with a non-existing ID.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.get(
        "/api/v1/categories/non_existing_id",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_read_category_by_id(access_token, category):
    """
    Test read a specific category by its ID.

    Args:
        access_token (str): The access token for authorization.
        category (dict): Dictionary containing information about the created category.

    Test steps:
    1. Send a request to fetch the category by ID.
    2. Verify the response status code.
    3. Parse the response and store category information.
    """
    response = client.get(
        f"/api/v1/categories/{category['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    category_data = response.json()
    assert category_data["id"] == category["id"]
    assert category_data["name"] == category["name"]
    assert category_data["parent_id"] == category["parent_id"]


def test_read_all_categories_unauthorized():
    """
    Test reading all categories without authorization.

    Test steps:
    1. Send a request to retrieve all categories without providing an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    response = client.get("/api/v1/categories/")
    assert response.status_code == 401
