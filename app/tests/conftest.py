"""
Global fixtures for API testing.
"""

import os
from uuid import uuid4
from dotenv import load_dotenv, find_dotenv
import pytest
from app.tests import create_client

load_dotenv(find_dotenv(".env"))
client = create_client()


@pytest.fixture(name="user", scope="session")
def create_user(access_token):
    """
    Fixture to create a user.

    Args:
        access_token (str): Access token for authorization.

    Returns:
        dict: Data of the created user.
    """
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "Test User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password",
            "role": "sysadmin",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(name="access_token", scope="session")
def fixture_access_token():
    """
    Returns an access token by making a POST request to the login endpoint with
    the sysadmin credentials.

    Returns:
        str: A string representing the access token.
    """
    response = client.post(
        url="/api/v1/login/", data={"username": os.environ.get("SYSADMIN_USERNAME"), "password": os.environ.get("SYSADMIN_PASSWORD")}
    )
    return response.json()["access_token"]


@pytest.fixture(name="user_to_delete_test", scope="session")
def create_delete_user(access_token):
    """
    Fixture to create a user for deletion.

    Args:
        access_token (str): Access token for authorization.

    Returns:
        dict: Data of the user created for deletion.
    """
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "Test Delete User",
            "username": "testdeleteuser",
            "email": "testdelete@example.com",
            "password": "password",
            "role": "sysadmin",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(name="severity", scope="session")
def create_severity(access_token):
    """
    Fixture to create a severity level for testing.

    Args:
        access_token (str): Access token for authorization.

    Returns:
        dict: Data of the created severity level.
    """
    response = client.post(
        "/api/v1/severities/",
        json={"level": 10, "description": "High severity level"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(name="severity_to_delete", scope="session")
def create_delete_severity(access_token):
    """
    Fixture to create a severity level intended for deletion testing.

    Args:
        access_token (str): Access token for authorization.

    Returns:
        dict: Data of the created severity level for deletion.
    """
    response = client.post(
        "/api/v1/severities/",
        json={"level": 11, "description": "High severity level to delete"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(name="category", scope="function")
def create_category(access_token):
    """
    Fixture to create a category for testing.

    Args:
        access_token (str): Access token for authorization.

    Returns:
        dict: Data of the created category.
    """
    response = client.post(
        "/api/v1/categories/",
        json={
            "name": f"Test Category {uuid4()}",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(name="category_to_delete", scope="function")
def create_delete_category(access_token):
    """
    Fixture to create a category intended for deletion testing.

    Args:
        access_token (str): Access token for authorization.

    Returns:
        dict: Data of the created category for deletion.
    """
    response = client.post(
        "/api/v1/categories/",
        json={
            "name": f"Delete Category {uuid4()}",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(name="subcategory", scope="function")
def create_subcategory(access_token, category):
    """
    Fixture to create a subcategory for testing.

    Args:
        access_token (str): Access token for authorization.
        category (dict): The parent category for the subcategory.

    Returns:
        dict: Data of the created subcategory.
    """
    response = client.post(
        "/api/v1/subcategories/",
        json={"name": f"Test Subcategory {uuid4()}", "category_id": category["id"]},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(name="subcategory_to_delete", scope="function")
def create_subcategory_to_delete(access_token, category):
    """
    Fixture to create a subcategory intended for deletion testing.

    Args:
        access_token (str): Access token for authorization.
        category (dict): The parent category for the subcategory.

    Returns:
        dict: Data of the created subcategory for deletion.
    """
    response = client.post(
        "/api/v1/subcategories/",
        json={"name": f"Subcategory to Delete {uuid4()}", "category_id": category["id"]},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(name="ticket", scope="function")
def create_ticket(access_token):
    """
    Fixture to create a ticket using the API for testing.

    Args:
        access_token (str): Access token for authorization.

    Returns:
        dict: A dictionary containing the ticket data.
    """
    severity_response = client.get(
        "/api/v1/severities/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert severity_response.status_code == 200
    severities = severity_response.json()
    severity = next((s for s in severities if s["level"] != 1), severities[0])

    category_response = client.get(
        "/api/v1/categories/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert category_response.status_code == 200
    categories = category_response.json()

    category = next((c for c in categories if len(c["subcategories"]) >= 2), categories[0])
    category_id = category["id"]
    subcategory_ids = [subcategory["id"] for subcategory in category["subcategories"][:2]]

    ticket_data = {
        "title": f"Test Ticket {uuid4()}",
        "description": "Test Ticket Description",
        "severity_id": severity["id"],
        "category_ids": [category_id],
        "subcategory_ids": subcategory_ids,
        "status": "aberto",
    }

    response = client.post(
        "/api/v1/tickets/",
        json=ticket_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    return response.json()


@pytest.fixture(name="ticket_to_delete", scope="function")
def create_ticket_to_delete(access_token):
    """
    Fixture to create a ticket specifically for deletion testing.

    Args:
        access_token (str): Access token for authorization.

    Returns:
        dict: A dictionary containing the ticket data to be deleted.
    """
    severity_response = client.get(
        "/api/v1/severities/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert severity_response.status_code == 200
    severities = severity_response.json()
    severity = next((s for s in severities if s["level"] != 1), severities[0])

    category_response = client.get(
        "/api/v1/categories/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert category_response.status_code == 200
    categories = category_response.json()

    category = next((c for c in categories if len(c["subcategories"]) >= 2), categories[0])
    category_id = category["id"]
    subcategory_ids = [subcategory["id"] for subcategory in category["subcategories"][:2]]

    ticket_data = {
        "title": f"Test Ticket to Delete {uuid4()}",
        "description": "Test Ticket Description for Deletion",
        "severity_id": severity["id"],
        "category_ids": [category_id],
        "subcategory_ids": subcategory_ids,
        "status": "aberto",
    }

    response = client.post(
        "/api/v1/tickets/",
        json=ticket_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    return response.json()
