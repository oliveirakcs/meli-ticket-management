"""
Tests for the API endpoints related to tickets.
"""

from app.tests import create_client

client = create_client()


def test_delete_ticket(access_token, ticket_to_delete):
    """
    Test deleting a ticket and verify the response.

    Args:
        access_token (str): The access token for authorization.
        ticket_to_delete (dict): Dictionary containing information about the ticket to delete.

    Test steps:
    1. Send a request to delete a ticket with a valid access token and an existing ticket UUID.
    2. Verify the response status code, expecting 202 (Accepted).
    """
    response = client.delete(
        f"/api/v1/tickets/?ticket_id={ticket_to_delete['id']}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 202


def test_delete_non_existing_ticket(access_token):
    """
    Test deleting a non-existent ticket and verify the response.

    Args:
        access_token (str): The access token for authorization.

    Test steps:
    1. Send a request to delete a ticket with a valid access token and a non-existent ticket UUID.
    2. Verify the response status code, expecting 422 (Unprocessable Entity).
    """
    response = client.delete(
        "/api/v1/tickets/?ticket_id=non_existing_id",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_delete_ticket_unauthorized(ticket_to_delete):
    """
    Test deleting a ticket without authorization.

    Args:
        ticket_to_delete (dict): Dictionary containing information about the ticket to delete.

    Test steps:
    1. Send a request to delete a ticket without providing an access token.
    2. Verify the response status code, expecting 401 (Unauthorized).
    """
    response = client.delete(f"/api/v1/tickets/?ticket_id={ticket_to_delete['id']}")
    assert response.status_code == 401
