"""
Tests for the API endpoints related to subcategories,
specifically focusing on the update function.
"""

from uuid import uuid4
from app.tests import create_client

client = create_client()


def test_update_all_fields_subcategory(access_token, subcategory, category):
    """
    Test updating all fields of an existing subcategory and verify the response.

    Args:
        access_token (str): The access token for authorization.
        subcategory (dict): Dictionary containing information about the created subcategory.
        category (dict): Dictionary containing information about the parent category.

    Test steps:
    1. Send a request to update the subcategory's information.
    2. Verify the response status code, expecting 200 (OK).
    3. Check if the subcategory's information has been updated correctly.
    """
    updated_name = f"Updated Subcategory {uuid4()}"
    response = client.patch(
        f"/api/v1/subcategories/{subcategory['id']}",
        json={"name": updated_name, "category_id": category["id"]},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    updated_subcategory_data = response.json()
    assert updated_subcategory_data["name"] == updated_name


def test_update_one_field_subcategory(access_token, subcategory):
    """
    Test updating a single field of an existing subcategory and verify the response.

    Args:
        access_token (str): The access token for authorization.
        subcategory (dict): Dictionary containing information about the created subcategory.

    Test steps:
    1. Send a request to update the subcategory's information.
    2. Verify the response status code, expecting 200 (OK).
    3. Check if the subcategory's information has been updated correctly.
    """
    updated_name = f"Partially Updated Subcategory {uuid4()}"
    response = client.patch(
        f"/api/v1/subcategories/{subcategory['id']}",
        json={"name": updated_name},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    updated_subcategory_data = response.json()
    assert updated_subcategory_data["name"] == updated_name


def test_update_non_existing_subcategory(access_token):
    """
    Test updating a non-existent subcategory and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to update a non-existent subcategory's information.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.patch(
        "/api/v1/subcategories/non_existing_id",
        json={"name": "Updated Name", "category_id": "some_category_id"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_update_subcategory_unauthorized(subcategory):
    """
    Test updating a subcategory without authorization.

    Args:
        subcategory (dict): Dictionary containing information about the created subcategory.

    Test steps:
    1. Send a request to update a subcategory without providing an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    updated_name = f"Unauthorized Update {uuid4()}"
    response = client.patch(
        f"/api/v1/subcategories/{subcategory['id']}",
        json={"name": updated_name},
    )
    assert response.status_code == 401
