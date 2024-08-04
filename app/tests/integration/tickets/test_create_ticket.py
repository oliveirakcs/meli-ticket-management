"""
Tests for creating tickets via API endpoints.
"""

from app.tests import create_client

client = create_client()


def test_create_duplicate_ticket(access_token, ticket):
    """
    Test creating a duplicate ticket and verify the response.

    Args:
        access_token (str): Access token for authorization.
        ticket (Ticket): A Ticket object fixture.

    Test steps:
    1. Attempt to create a ticket with the same title as an existing one.
    2. Verify the response status code, expecting 409 (Conflict).
    """

    ticket_severity = ticket["severity"]
    severity_id = ticket_severity["id"]
    ticket_categories = ticket["categories"]

    category_ids = [category["id"] for category in ticket_categories]
    subcategory_ids = [subcategory["id"] for category in ticket_categories for subcategory in category["subcategories"]]

    ticket_data = {
        "title": ticket["title"],
        "description": "This is a test ticket.",
        "severity_id": severity_id,
        "category_ids": category_ids,
        "subcategory_ids": subcategory_ids,
        "status": "aberto",
    }

    duplicate_response = client.post(
        "/api/v1/tickets/",
        json=ticket_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert duplicate_response.status_code == 409
    assert duplicate_response.json()["detail"] == f"Ticket with title '{ticket['title']}' already exists."


def test_create_ticket_unauthorized(severity, category, subcategory):
    """
    Test creating a ticket without authorization.

    Args:
        severity (dict): The severity level for the ticket.
        category (dict): The category for the ticket.
        subcategory (dict): The subcategory for the ticket.

    Test steps:
    1. Send a request to create a ticket without an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    response = client.post(
        "/api/v1/tickets/",
        json={
            "title": "Unauthorized Ticket",
            "description": "This is a test ticket without authorization.",
            "severity_id": severity["id"],
            "category_ids": [category["id"]],
            "subcategory_ids": [subcategory["id"]],
            "status": "aberto",
        },
    )
    assert response.status_code == 401


def test_create_ticket_with_invalid_data(access_token):
    """
    Test creating a ticket with invalid data and verify the response.

    Args:
        access_token (str): Access token for authorization.

    Test steps:
    1. Send a request to create a ticket with invalid data.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.post(
        "/api/v1/tickets/",
        json={
            "title": "",
            "description": "Invalid ticket due to missing title.",
            "severity_id": None,
            "category_ids": ["invalid_uuid"],
            "subcategory_ids": ["invalid_uuid"],
            "status": "aberto",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422
