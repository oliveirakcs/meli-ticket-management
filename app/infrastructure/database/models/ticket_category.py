"""TicketCategory Model"""

from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class TicketCategory(Base):
    """
    Represents the association between a Ticket and a Category.

    Attributes:
        ticket_id (UUID): Foreign key linking to the ticket.
        category_id (UUID): Foreign key linking to the category.
    """

    __tablename__ = "ticket_categories"

    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), primary_key=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), primary_key=True)

    ticket = relationship("Ticket", back_populates="ticket_categories")
    category = relationship("Category", back_populates="ticket_categories")

    def __repr__(self):
        """
        Return a string representation of the TicketCategory object.

        Returns:
            str: A string representation of the TicketCategory object.
        """
        return f"<TicketCategory ticket_id={self.ticket_id} category_id={self.category_id}>"

    def to_dict(self):
        """
        Return a dictionary representation of the TicketCategory object.

        Returns:
            dict: A dictionary representation of the TicketCategory object.
        """
        return {
            "ticket_id": str(self.ticket_id),
            "category_id": str(self.category_id),
        }
