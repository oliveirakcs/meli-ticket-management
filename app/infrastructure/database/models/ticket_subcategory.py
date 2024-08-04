"TicketSubcategory Model"

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class TicketSubcategory(Base):
    """
    Represents the association between a Ticket and a Subcategory.

    Attributes:
        ticket_id (UUID): Foreign key linking to the ticket.
        subcategory_id (UUID): Foreign key linking to the subcategory.
    """

    __tablename__ = "ticket_subcategories"

    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), primary_key=True)
    subcategory_id = Column(UUID(as_uuid=True), ForeignKey("subcategories.id"), primary_key=True)

    ticket = relationship("Ticket", back_populates="ticket_subcategories")
    subcategory = relationship("Subcategory", back_populates="ticket_subcategories")

    def __repr__(self):
        """
        Return a string representation of the TicketSubcategory object.

        Returns:
            str: A string representation of the TicketSubcategory object.
        """
        return f"<TicketSubcategory ticket_id={self.ticket_id} subcategory_id={self.subcategory_id}>"

    def to_dict(self):
        """
        Return a dictionary representation of the TicketSubcategory object.

        Returns:
            dict: A dictionary representation of the TicketSubcategory object.
        """
        return {
            "ticket_id": str(self.ticket_id),
            "subcategory_id": str(self.subcategory_id),
        }
