"""Controllers for managing ticket operations in the database related to Ticket API endpoints."""

from typing import List
from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from app.infrastructure import get_db, Ticket, Category, Subcategory, Severity
from app.schemas import TicketUpdate as SchemaTicketUpdate, TicketShow as SchemaTicketShow, Ticket as SchemaTicket


class TicketController:
    """
    A controller class for managing ticket operations in the database.
    """

    def __init__(self, db: Session):
        """
        Initialize the TicketController with a database session.

        Args:
            db (Session): The database session.
        """
        self.db = db

    def get_all(self) -> List[SchemaTicketShow]:
        """
        Get all tickets.

        Returns:
            List[SchemaTicketShow]: A list of ticket objects.

        Raises:
            HTTPException: Raised if no tickets are found.
        """
        tickets = self.db.query(Ticket).all()
        if not tickets:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tickets found")
        return tickets

    def create(self, request: SchemaTicket) -> SchemaTicketShow:
        """
        Create a new ticket.

        Args:
            request (SchemaTicket): The request containing details of the new ticket.

        Returns:
            SchemaTicketShow: The newly created ticket object.

        Raises:
            HTTPException: Raised if any required field is not provided or if the category, subcategory, or severity doesn't exist.
        """
        required_fields = [request.title, request.category_id, request.severity_id]
        if not all(required_fields):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title, category_id, and severity_id must be filled",
            )

        severity = self.db.query(Severity).filter(Severity.id == request.severity_id).first()
        if not severity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Severity with ID '{request.severity_id}' not found.",
            )

        if severity.level == 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot create a ticket with severity level 1.",
            )

        category = self.db.query(Category).filter(Category.id == request.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID '{request.category_id}' not found.",
            )

        if request.subcategory_id:
            subcategory = self.db.query(Subcategory).filter(Subcategory.id == request.subcategory_id).first()
            if not subcategory:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Subcategory with ID '{request.subcategory_id}' not found.",
                )

        new_ticket = Ticket(
            title=request.title,
            description=request.description,
            category_id=request.category_id,
            subcategory_id=request.subcategory_id,
            severity_id=request.severity_id,
            status=request.status,
        )

        self.db.add(new_ticket)
        self.db.commit()
        self.db.refresh(new_ticket)

        return new_ticket

    def show(self, ticket_id: UUID4) -> SchemaTicketShow:
        """
        Retrieve a ticket by ticket ID.

        Args:
            ticket_id (UUID4): The ID of the ticket to retrieve.

        Returns:
            SchemaTicketShow: The ticket corresponding to the provided ID.

        Raises:
            HTTPException: Raised if the ticket with the provided ID is not found.
        """
        ticket = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket {ticket_id} not found",
            )
        return ticket

    def update(self, ticket_id: UUID4, request: SchemaTicketUpdate) -> SchemaTicketShow:
        """
        Update ticket information.

        Args:
            ticket_id (UUID4): The ID of the ticket to update.
            request (SchemaTicketUpdate): The updated ticket information.

        Returns:
            SchemaTicketShow: The updated ticket information.

        Raises:
            HTTPException: Raised if the ticket with the provided ID is not found or if any field is invalid.
        """
        ticket = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket {ticket_id} not found",
            )

        if request.severity_id:
            severity = self.db.query(Severity).filter(Severity.id == request.severity_id).first()
            if not severity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Severity with ID '{request.severity_id}' not found.",
                )
            if severity.level == 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot update ticket to severity level 1.",
                )

        if request.category_id:
            category = self.db.query(Category).filter(Category.id == request.category_id).first()
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with ID '{request.category_id}' not found.",
                )

        if request.subcategory_id:
            subcategory = self.db.query(Subcategory).filter(Subcategory.id == request.subcategory_id).first()
            if not subcategory:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Subcategory with ID '{request.subcategory_id}' not found.",
                )

        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(ticket, key, value)

        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def delete(self, ticket_id: UUID4) -> str:
        """
        Delete a ticket by ticket UUID.

        Args:
            ticket_id (UUID4): The ID of the ticket to be deleted.

        Returns:
            str: A message confirming the deletion of the ticket.

        Raises:
            HTTPException: Raised if the ticket with the provided ID is not found.
        """
        ticket = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket {ticket_id} not found")

        self.db.delete(ticket)
        self.db.commit()
        return f"Ticket {ticket_id} deleted."


def get_ticket_controller(db: Session = Depends(get_db)):
    """
    Dependency to get an instance of TicketController.

    Args:
        db (Session): The database session.

    Returns:
        TicketController: An instance of TicketController.
    """
    return TicketController(db=db)
