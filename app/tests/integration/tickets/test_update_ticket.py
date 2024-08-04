# """
# Tests for the API endpoints related to tickets.
# """

# from uuid import uuid4
# from app.tests import create_client

# client = create_client()


# def test_update_all_fields_ticket(access_token, ticket, severity, category, subcategory):
#     """
#     Test updating all fields of an existing ticket and verify the response.

#     Args:
#         access_token (str): The access token for authorization.
#         ticket (dict): Data of the created ticket.
#         severity (dict): The severity level for the ticket.
#         category (dict): The category for the ticket.
#         subcategory (dict): The subcategory for the ticket.

#     Test steps:
#     1. Send a request to update the ticket's information.
#     2. Verify the response status code, expecting 200 (OK).
#     3. Check if the ticket's information has been updated correctly.
#     """
#     updated_title = f"Updated Ticket {uuid4()}"
#     response = client.patch(
#         f"/api/v1/tickets/{ticket['id']}",
#         json={
#             "title": updated_title,
#             "description": "Updated ticket description",
#             "severity_id": severity["id"],
#             "category_id": category["id"],
#             "subcategory_id": subcategory["id"],
#             "status": "closed",
#         },
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     assert response.status_code == 200
#     updated_ticket_data = response.json()
#     assert updated_ticket_data["title"] == updated_title
#     assert updated_ticket_data["status"] == "closed"


# def test_update_one_field_ticket(access_token, ticket):
#     """
#     Test updating a single field of an existing ticket and verify the response.

#     Args:
#         access_token (str): The access token for authorization.
#         ticket (dict): Data of the created ticket.

#     Test steps:
#     1. Send a request to update the ticket's information.
#     2. Verify the response status code, expecting 200 (OK).
#     3. Check if the ticket's information has been updated correctly.
#     """
#     updated_title = f"Partially Updated Ticket {uuid4()}"
#     response = client.patch(
#         f"/api/v1/tickets/{ticket['id']}",
#         json={"title": updated_title},
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     assert response.status_code == 200
#     updated_ticket_data = response.json()
#     assert updated_ticket_data["title"] == updated_title


# def test_update_non_existing_ticket(access_token):
#     """
#     Test updating a non-existent ticket and verify the response.

#     Args:
#         access_token (str): The access token for authorization.

#     Test steps:
#     1. Send a request to update a non-existent ticket's information.
#     2. Verify the response status code, expecting 404 (Not Found).
#     """
#     response = client.patch(
#         "/api/v1/tickets/00000000-0000-0000-0000-000000000000",  # Non-existent ID
#         json={
#             "title": "Updated Name",
#             "description": "Updated Description",
#             "status": "closed",
#         },
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     assert response.status_code == 404


# def test_update_ticket_unauthorized(ticket):
#     """
#     Test updating a ticket without authorization.

#     Args:
#         ticket (dict): Data of the created ticket.

#     Test steps:
#     1. Send a request to update a ticket without providing an access token.
#     2. Verify the response status code, expecting 401 (Unauthorized).
#     """
#     updated_title = f"Unauthorized Update {uuid4()}"
#     response = client.patch(
#         f"/api/v1/tickets/{ticket['id']}",
#         json={"title": updated_title},
#     )
#     assert response.status_code == 401
