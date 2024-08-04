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

    Test steps:
    1. Attempt to create a ticket with the same title as an existing one.
    2. Verify the response status code, expecting 409 (Conflict).
    """

    severity_response = client.get(
        "/api/v1/severities/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert severity_response.status_code == 200, "Failed to retrieve severities"
    severities = severity_response.json()
    severity = severities[3] if severities else None

    category_response = client.get(
        "/api/v1/categories/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert category_response.status_code == 200, "Failed to retrieve categories"
    categories = category_response.json()
    category = categories[3] if categories else None

    subcategory_response = client.get(
        f"/api/v1/subcategories/?category_id={category['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert subcategory_response.status_code == 200, "Failed to retrieve subcategories"
    subcategories = subcategory_response.json()
    subcategory = subcategories[3] if subcategories else None

    assert severity is not None, "No severity found"
    assert category is not None, "No category found"
    assert subcategory is not None, "No subcategory found"

    ticket_title = ticket["title"]

    ticket_data = {
        "title": ticket_title,
        "description": "This is a test ticket.",
        "severity_id": severity["id"],
        "category_id": category["id"],
        "subcategory_id": subcategory["id"],
    }

    duplicate_response = client.post(
        "/api/v1/tickets/",
        json=ticket_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert duplicate_response.status_code == 409


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
            "category_id": category["id"],
            "subcategory_id": subcategory["id"],
            "status": "open",
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
            "category_id": "invalid_uuid",
            "subcategory_id": "invalid_uuid",
            "status": "open",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422
