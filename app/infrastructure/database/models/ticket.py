"""Ticket Model"""

import uuid
from sqlalchemy import UUID, Column, String, Text, ForeignKey, TIMESTAMP, Enum as SAEnum
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
        category_id (UUID): Foreign key linking to the ticket's category.
        subcategory_id (UUID): Foreign key linking to the ticket's subcategory.
        severity_id (UUID): Foreign key linking to the ticket's severity.
        status (TicketStatus): Status of the ticket (ABERTO, EM_PROGRESSO, RESOLVIDO).
        created_at (timestamp): Timestamp when the ticket was created.
        updated_at (timestamp): Timestamp when the ticket was last updated.
    """

    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    subcategory_id = Column(UUID(as_uuid=True), ForeignKey("subcategories.id"), nullable=True)
    severity_id = Column(UUID(as_uuid=True), ForeignKey("severity.id"), nullable=False)
    status = Column(SAEnum(TicketStatus), default=TicketStatus.ABERTO, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    category = relationship("Category", back_populates="tickets")
    subcategory = relationship("Subcategory", back_populates="tickets")
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
            "category_id": str(self.category_id),
            "subcategory_id": str(self.subcategory_id) if self.subcategory_id else None,
            "severity_id": str(self.severity_id),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
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
            category_id=data["category_id"],
            subcategory_id=data.get("subcategory_id"),
            severity_id=data["severity_id"],
            status=TicketStatus(data.get("status", TicketStatus.ABERTO.value)),
        )
