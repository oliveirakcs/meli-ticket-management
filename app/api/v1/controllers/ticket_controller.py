"""Controllers for managing ticket operations in the database related to Ticket API endpoints."""

from typing import List
import logging
from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status, Depends
from app.infrastructure import get_db, Ticket, Category, Subcategory, Severity, TicketSubcategory, TicketCategory
from app.schemas import TicketUpdate as SchemaTicketUpdate, TicketShow as SchemaTicketShow, Ticket as SchemaTicket, SeverityShow as SchemaSeverity
from app.scripts import External

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"


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
        return [self._load_categories_and_subcategories(ticket) for ticket in tickets]

    def create(self, request: SchemaTicket) -> SchemaTicketShow:
        """
        Create a new ticket.
        """
        try:
            required_fields = [request.title, request.category_ids, request.severity_id]
            if not all(required_fields):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Title, category_ids, and severity_id must be filled",
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

            categories = self.db.query(Category).filter(Category.id.in_(request.category_ids)).all()
            if len(categories) != len(request.category_ids):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="One or more categories not found.",
                )

            subcategories = []
            if request.subcategory_ids:
                subcategories = self.db.query(Subcategory).filter(Subcategory.id.in_(request.subcategory_ids)).all()
                if len(subcategories) != len(request.subcategory_ids):
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="One or more subcategories not found.",
                    )

                for subcategory in subcategories:
                    if subcategory.category_id not in request.category_ids:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Subcategory '{subcategory.name}' does not belong to the provided categories.",
                        )

            existing_ticket = self.db.query(Ticket).filter(Ticket.title == request.title).first()
            if existing_ticket:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ticket with title '{request.title}' already exists.",
                )

            new_ticket = Ticket(
                title=request.title,
                description=request.description,
                severity_id=request.severity_id,
                status=request.status,
            )

            for category in categories:
                ticket_category = TicketCategory(ticket=new_ticket, category=category)
                self.db.add(ticket_category)

            for subcategory in subcategories:
                ticket_subcategory = TicketSubcategory(ticket=new_ticket, subcategory=subcategory)
                self.db.add(ticket_subcategory)

            self.db.add(new_ticket)
            self.db.commit()
            self.db.refresh(new_ticket)

            return self._load_categories_and_subcategories(new_ticket)

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("Error creating ticket: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the ticket. Please try again.",
            ) from e

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
        ticket = self._get_ticket_by_id(ticket_id)
        return self._load_categories_and_subcategories(ticket)

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
        try:
            ticket = self._get_ticket_by_id(ticket_id)
            self._validate_and_update_severity(ticket, request)
            self._update_categories(ticket, request)
            self._update_subcategories(ticket, request)
            self._update_ticket_fields(ticket, request)

            self.db.commit()
            self.db.refresh(ticket)

            return self._load_categories_and_subcategories(ticket)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("Error updating ticket %s: %s", ticket_id, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the ticket. Please try again.",
            ) from e

    def _get_ticket_by_id(self, ticket_id: UUID4) -> Ticket:
        ticket = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket {ticket_id} not found",
            )
        return ticket

    def _validate_and_update_severity(self, ticket: Ticket, request: SchemaTicketUpdate):
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
            ticket.severity_id = request.severity_id

    def _update_categories(self, ticket: Ticket, request: SchemaTicketUpdate):
        """
        Update the categories associated with a ticket to match the request.

        Args:
            ticket (Ticket): The ticket object to update.
            request (SchemaTicketUpdate): The request containing the updated category IDs.

        Raises:
            HTTPException: If any category is not found.
        """
        if request.category_ids is not None:
            new_category_ids = request.category_ids

            categories = self.db.query(Category).filter(Category.id.in_(new_category_ids)).all()
            if len(categories) != len(new_category_ids):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="One or more categories not found.",
                )

            self.db.query(TicketCategory).filter(TicketCategory.ticket_id == ticket.id).delete(synchronize_session="fetch")

            for category in categories:
                ticket_category = TicketCategory(ticket=ticket, category=category)
                self.db.add(ticket_category)

            self.db.flush()

    def _update_subcategories(self, ticket: Ticket, request: SchemaTicketUpdate):
        """
        Update the subcategories associated with a ticket to match the request.

        Args:
            ticket (Ticket): The ticket object to update.
            request (SchemaTicketUpdate): The request containing the updated subcategory IDs.

        Raises:
            HTTPException: If any subcategory is not found or doesn't belong to the specified categories.
        """
        if request.subcategory_ids is not None:
            new_sub_ids = request.subcategory_ids
            current_category_ids = {category.category_id for category in ticket.ticket_categories}

            subcategories = self.db.query(Subcategory).filter(Subcategory.id.in_(new_sub_ids)).all()
            if len(subcategories) != len(new_sub_ids):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="One or more subcategories not found.",
                )

            for subcategory in subcategories:
                if subcategory.category_id not in current_category_ids:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Subcategory '{subcategory.name}' does not belong to any current categories of the ticket.",
                    )

            self.db.query(TicketSubcategory).filter(TicketSubcategory.ticket_id == ticket.id).delete(synchronize_session="fetch")

            for subcategory in subcategories:
                ticket_subcategory = TicketSubcategory(ticket=ticket, subcategory=subcategory)
                self.db.add(ticket_subcategory)

            self.db.flush()

    def _update_ticket_fields(self, ticket: Ticket, request: SchemaTicketUpdate):
        for key, value in request.model_dump(exclude_unset=True).items():
            if key not in {"category_ids", "subcategory_ids"}:
                setattr(ticket, key, value)

    def _load_categories_and_subcategories(self, ticket: Ticket) -> SchemaTicketShow:
        """
        Load categories and subcategories for a ticket.

        Args:
            ticket (Ticket): The ticket object.

        Returns:
            SchemaTicketShow: The schema object with loaded categories and subcategories.
        """
        categories = [tc.category for tc in ticket.ticket_categories]
        subcategories = [ts.subcategory for ts in ticket.ticket_subcategories]

        category_subcategory_map = {category.id: [] for category in categories}
        for subcategory in subcategories:
            if subcategory.category_id in category_subcategory_map:
                category_subcategory_map[subcategory.category_id].append(subcategory)

        severity = ticket.severity

        ticket_data = SchemaTicketShow(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            severity=SchemaSeverity(id=severity.id, level=severity.level, description=severity.description),
            status=ticket.status,
            categories=[
                {
                    "id": category.id,
                    "name": category.name,
                    "subcategories": [
                        {"id": sub.id, "name": sub.name, "category_id": sub.category_id} for sub in category_subcategory_map[category.id]
                    ],
                }
                for category in categories
            ],
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,
            comment=ticket.comment,
            comment_user=ticket.comment_user,
        )

        return ticket_data

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
        try:
            ticket = self._get_ticket_by_id(ticket_id)

            self.db.query(TicketSubcategory).filter(TicketSubcategory.ticket_id == ticket.id).delete(synchronize_session="fetch")

            self.db.query(TicketCategory).filter(TicketCategory.ticket_id == ticket.id).delete(synchronize_session="fetch")

            self.db.delete(ticket)

            self.db.commit()

            return f"Ticket {ticket_id} deleted."

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("Error deleting ticket %s: %s", ticket_id, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the ticket. Please try again.",
            ) from e

    def add_comment_to_ticket(self, ticket_id: UUID4) -> dict:
        """
        Add a comment from JSONPlaceholder to a ticket.

        Args:
            ticket_id (UUID4): The ID of the ticket to add a comment to.

        Returns:
            dict: A dictionary confirming the addition of the comment.

        Raises:
            HTTPException: If there's an issue fetching comments or updating the ticket.
        """
        try:
            comment_data = External.fetch_random_comment()
            comment_text = comment_data["comment_text"]
            comment_user = comment_data["comment_user"]

            ticket = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
            if not ticket:
                raise HTTPException(status_code=404, detail="Ticket not found.")

            ticket.comment = comment_text
            ticket.comment_user = comment_user
            self.db.commit()
            self.db.refresh(ticket)

            return {"ticket_id": str(ticket_id), "comment": comment_text, "comment_user": comment_user}

        except Exception as e:
            self.db.rollback()
            logger.error("Error adding comment to ticket: %s", e)
            raise HTTPException(status_code=500, detail=str(e)) from e


def get_ticket_controller(db: Session = Depends(get_db)):
    """
    Dependency to get an instance of TicketController.

    Args:
        db (Session): The database session.

    Returns:
        TicketController: An instance of TicketController.
    """
    return TicketController(db=db)
