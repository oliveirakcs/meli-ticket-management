"""Ticket Model"""

import uuid
from sqlalchemy import UUID, Column, DateTime, String, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.base import Base
from app.core import TicketStatus


class Ticket(Base):
    """
    Represents a support or issue ticket in the system.

    Attributes:
        id (UUID): Primary key for the ticket.
        title (str): Title of the ticket.
        description (str): Detailed description of the ticket issue.
        severity_id (UUID): Foreign key linking to the ticket's severity.
        status (TicketStatus): Status of the ticket (ABERTO, EM_PROGRESSO, RESOLVIDO).
        created_at (timestamp): Timestamp when the ticket was created.
        updated_at (timestamp): Timestamp when the ticket was last updated.
    """

    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity_id = Column(UUID(as_uuid=True), ForeignKey("severity.id"), nullable=False)
    status = Column(SAEnum(TicketStatus), default=TicketStatus.ABERTO, nullable=False)
    comment = Column(Text, nullable=True)
    comment_user = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    ticket_categories = relationship("TicketCategory", back_populates="ticket", cascade="all, delete-orphan")
    ticket_subcategories = relationship("TicketSubcategory", back_populates="ticket")
    severity = relationship("Severity", back_populates="tickets")

    def __repr__(self):
        """Return a string representation of the Ticket instance."""
        return f"<Ticket id={self.id} title={self.title} status={self.status}>"

    def to_dict(self):
        """
        Convert the Ticket instance to a dictionary.

        Returns:
            dict: A dictionary representation of the Ticket instance.
        """
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "severity_id": str(self.severity_id),
            "status": self.status.value,
            "comment": self.comment,
            "comment_user": self.comment_user,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Ticket instance from a dictionary.

        Args:
            data (dict): A dictionary containing the ticket data.

        Returns:
            Ticket: An instance of the Ticket model.
        """
        return cls(
            title=data["title"],
            description=data["description"],
            severity_id=data["severity_id"],
            status=TicketStatus(data.get("status", TicketStatus.ABERTO.value)),
        )
