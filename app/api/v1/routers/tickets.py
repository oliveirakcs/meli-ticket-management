"""Ticket routers"""

from typing import List
from fastapi import APIRouter, Depends, Security, status
from pydantic import UUID4
from app.schemas import Ticket, TicketShow, TicketUpdate
from app.api.v1 import get_ticket_controller, TicketController
from app.core.auth.oauth import get_current_active_user

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get(
    "/",
    response_model=List[TicketShow],
    status_code=status.HTTP_200_OK,
)
def get_all_tickets(
    controller: TicketController = Depends(get_ticket_controller),
    current_user: Ticket = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Retrieve all tickets.

    Retrieves all tickets stored in the database.

    Parameters:
    - controller (TicketController): The ticket controller instance.
    - _: Ticket: The current user (unused).

    Returns:
    - List[TicketShow]: A list of ticket objects with restricted information.

    Raises:
    - HTTPException: If there's an issue retrieving tickets from the database.
    """
    return controller.get_all()


@router.post(
    "/",
    response_model=TicketShow,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    request: Ticket,
    controller: TicketController = Depends(get_ticket_controller),
    current_user: Ticket = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Create a new ticket.

    Parameters:
    - request (Ticket): The ticket data to create the new ticket.
    - controller (TicketController): The ticket controller instance.
    - _: Ticket: The current user (unused).

    Returns:
    - TicketShow: The created ticket data with restricted information.

    Raises:
    - HTTPException: If there's an issue creating the ticket.
    """
    return controller.create(request)


@router.delete("/", status_code=status.HTTP_202_ACCEPTED)
def delete_ticket(
    ticket_id: UUID4,
    controller: TicketController = Depends(get_ticket_controller),
    current_user: Ticket = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Delete a ticket.

    Parameters:
    - ticket_id (UUID4): The ID of the ticket to delete.
    - controller (TicketController): The ticket controller instance.
    - _: Ticket: The current user (unused).

    Returns:
    - None

    Raises:
    - HTTPException: If there's an issue deleting the ticket.
    """
    return controller.delete(ticket_id)


@router.get("/{ticket_id}", response_model=TicketShow, status_code=status.HTTP_200_OK)
def get_ticket(
    ticket_id: UUID4,
    controller: TicketController = Depends(get_ticket_controller),
    current_user: Ticket = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Retrieve ticket by ticket ID.

    Parameters:
    - ticket_id (UUID4): The ID of the ticket to retrieve.
    - controller (TicketController): The ticket controller instance.
    - _: Ticket: The current user (unused).

    Returns:
    - TicketShow: The ticket data with restricted information.

    Raises:
    - HTTPException: If the ticket with the specified ID is not found.
    """
    return controller.show(ticket_id)


@router.patch(
    "/{ticket_id}",
    response_model=TicketShow,
    status_code=status.HTTP_200_OK,
)
def update_ticket(
    ticket_id: UUID4,
    request: TicketUpdate,
    controller: TicketController = Depends(get_ticket_controller),
    current_user: Ticket = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Update ticket data.

    Parameters:
    - ticket_id (UUID4): The ID of the ticket to update.
    - request (TicketUpdate): The ticket data to be updated.
    - controller (TicketController): The ticket controller instance.
    - _: Ticket: The current user (unused).

    Returns:
    - TicketShow: The updated ticket data with restricted information.

    Raises:
    - HTTPException: If the ticket with the specified ID is not found or if there's an issue updating the ticket.
    """
    updated_ticket = controller.update(ticket_id, request)
    return updated_ticket


@router.post(
    "/add/{ticket_id}",
    status_code=status.HTTP_200_OK,
)
def add_comment(
    ticket_id: UUID4,
    controller: TicketController = Depends(get_ticket_controller),
    current_user=Security(get_current_active_user, scopes=["admin"]),
):
    """
    Add a comment to a ticket using JSONPlaceholder API.

    Parameters:
    - ticket_id (UUID4): The ID of the ticket to add a comment to.
    - controller (CommentController): The comment controller instance.
    - _: The current user (unused).

    Returns:
    - dict: Confirmation of the added comment.

    Raises:
    - HTTPException: If there's an issue adding the comment.
    """
    return controller.add_comment_to_ticket(ticket_id)
