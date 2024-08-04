"""Subcategory Model"""

import uuid
from sqlalchemy import UUID, Column, DateTime, String, ForeignKey, func
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class Subcategory(Base):
    """
    Represents a subcategory linked to a specific category.

    Attributes:
        id (int): Primary key for the subcategory.
        name (str): Name of the subcategory.
        category_id (int): Foreign key linking to the parent category.
    """

    __tablename__ = "subcategories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)

    ticket_subcategories = relationship("TicketSubcategory", back_populates="subcategory")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category", back_populates="subcategories")

    def __repr__(self):
        """Return a string representation of the Subcategory instance."""
        return f"<Subcategory id={self.id} name={self.name} category_id={self.category_id}>"

    def to_dict(self):
        """
        Convert the Subcategory instance to a dictionary.

        Returns:
            dict: A dictionary representation of the Subcategory instance.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "category_id": str(self.category_id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Subcategory instance from a dictionary.

        Args:
            data (dict): A dictionary containing the subcategory data.

        Returns:
            Subcategory: An instance of the Subcategory model.
        """
        return cls(name=data["name"], category_id=data["category_id"])
