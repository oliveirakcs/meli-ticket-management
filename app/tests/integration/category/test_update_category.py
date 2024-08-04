"""
Tests for the API endpoints related to categories,
specifically focusing on the update function.
"""

from app.tests import create_client

client = create_client()


def test_update_all_fields_category(access_token, category):
    """
    Test updating an existing category's information and verify the response.

    Args:
        access_token (str): The access token for authorization.
        category (dict): Dictionary containing information about the created category.

    Test steps:
    1. Send a request to update the category's information.
    2. Verify the response status code, expecting 200 (OK).
    3. Check if the category's information has been updated correctly.
    """
    updated_name = "Updated Category Name"
    response = client.patch(
        f"/api/v1/categories/{category['id']}",
        json={"name": updated_name},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    updated_category_data = response.json()
    assert updated_category_data["name"] == updated_name


def test_update_one_field_category(access_token, category):
    """
    Test updating a single field of an existing category's information and verify the response.

    Args:
        access_token (str): The access token for authorization.
        category (dict): Dictionary containing information about the created category.

    Test steps:
    1. Send a request to update the category's information.
    2. Verify the response status code, expecting 200 (OK).
    3. Check if the category's information has been updated correctly.
    """
    updated_name = "New Category Name"
    response = client.patch(
        f"/api/v1/categories/{category['id']}",
        json={"name": updated_name},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    updated_category_data = response.json()
    assert updated_category_data["name"] == updated_name


def test_update_non_existing_category(access_token):
    """
    Test updating a non-existent category's information and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to update a non-existent category's information.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.patch(
        "/api/v1/categories/non_existing_id",
        json={"name": "Updated Category Name"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_update_category_unauthorized(category):
    """
    Test updating a category without authorization.

    Args:
        category (dict): Dictionary containing information about the category to update.

    Test steps:
    1. Send a request to update a category without providing an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    updated_name = "Unauthorized Update"
    response = client.patch(
        f"/api/v1/categories/{category['id']}",
        json={"name": updated_name},
    )
    assert response.status_code == 401
