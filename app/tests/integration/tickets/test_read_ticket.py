# """
# Tests for the API endpoints related to tickets.
# """

# from app.tests import create_client

# client = create_client()


# def test_read_ticket_by_id(access_token, ticket):
#     """
#     Test reading a specific ticket by its ID.

#     Args:
#         access_token (str): The access token for authorization.
#         ticket (dict): Data of the created ticket.

#     Test steps:
#     1. Send a request to fetch the ticket by ID.
#     2. Verify the response status code.
#     3. Parse the response and validate the ticket information.
#     """
#     response = client.get(
#         f"/api/v1/tickets/{ticket['id']}",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == ticket["id"]
#     assert data["title"] == ticket["title"]
#     assert data["description"] == ticket["description"]


# def test_read_non_existing_ticket(access_token):
#     """
#     Test reading a non-existent ticket and verify the response.

#     Args:
#         access_token (str): The access token for authorization.

#     Test steps:
#     1. Send a request to read a ticket by a non-existent ID.
#     2. Verify the response status code, expecting 404 (Not Found).
#     """
#     response = client.get(
#         "/api/v1/tickets/00000000-0000-0000-0000-000000000000",  # Non-existent ID
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     assert response.status_code == 404


# def test_read_ticket_unauthorized(ticket):
#     """
#     Test reading a ticket without authorization.

#     Args:
#         ticket (dict): Data of the created ticket.

#     Test steps:
#     1. Send a request to read a ticket without providing an access token.
#     2. Verify the response status code, expecting 401 (Unauthorized).
#     """
#     response = client.get(f"/api/v1/tickets/{ticket['id']}")
#     assert response.status_code == 401


# def test_read_all_tickets(access_token):
#     """
#     Test reading all tickets and verify the response.

#     Args:
#         access_token (str): The access token for authorization.

#     Test steps:
#     1. Send a request to fetch all tickets.
#     2. Verify the response status code.
#     3. Parse the response and ensure it returns a list.
#     """
#     response = client.get(
#         "/api/v1/tickets/",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
