"""
Tests for the API endpoints related to tickets.
"""

from uuid import uuid4
from app.tests import create_client

client = create_client()


def test_update_one_field_ticket(access_token, ticket):
    """
    Test updating a single field of an existing ticket and verify the response.

    Args:
        access_token (str): The access token for authorization.
        ticket (dict): Data of the created ticket.

    Test steps:
    1. Send a request to update the ticket's information.
    2. Verify the response status code, expecting 200 (OK).
    3. Check if the ticket's information has been updated correctly.
    """
    updated_title = f"Partially Updated Ticket {uuid4()}"
    response = client.patch(
        f"/api/v1/tickets/{ticket['id']}",
        json={"title": updated_title},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    updated_ticket_data = response.json()
    assert updated_ticket_data["title"] == updated_title


def test_update_non_existing_ticket(access_token):
    """
    Test updating a non-existent ticket and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to update a non-existent ticket's information.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.patch(
        "/api/v1/tickets/00000000-0000-0000-0000-000000000000",
        json={
            "title": "Updated Name",
            "description": "Updated Description",
            "status": "closed",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_update_ticket_unauthorized(ticket):
    """
    Test updating a ticket without authorization.

    Args:
        ticket (dict): Data of the created ticket.

    Test steps:
    1. Send a request to update a ticket without providing an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    updated_title = f"Unauthorized Update {uuid4()}"
    response = client.patch(
        f"/api/v1/tickets/{ticket['id']}",
        json={"title": updated_title},
    )
    assert response.status_code == 401


def test_update_ticket_categories_and_subcategories(access_token, ticket, category, subcategory):
    """
    Test updating the categories and subcategories of an existing ticket and verify the response.

    Args:
        access_token (str): The access token for authorization.
        ticket (dict): Data of the created ticket.
        category (dict): The new category for the ticket.
        subcategory (dict): The new subcategory for the ticket.

    Test steps:
    1. Send a request to update the ticket's categories and subcategories.
    2. Verify the response status code, expecting 200 (OK).
    3. Check if the ticket's categories and subcategories have been updated correctly.
    """
    response = client.patch(
        f"/api/v1/tickets/{ticket['id']}",
        json={
            "category_ids": [category["id"]],
            "subcategory_ids": [subcategory["id"]],
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    updated_ticket_data = response.json()
    assert updated_ticket_data["categories"][0]["id"] == category["id"]
    assert updated_ticket_data["categories"][0]["subcategories"][0]["id"] == subcategory["id"]
