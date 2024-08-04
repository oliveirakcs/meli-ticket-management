"""Category Model"""

import uuid
from sqlalchemy import UUID, Column, DateTime, String, func
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class Category(Base):
    """
    Represents a category, which can have subcategories nested under it.

    Attributes:
        id (int): Primary key for the category.
        name (str): Name of the category.
    """

    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    ticket_categories = relationship("TicketCategory", back_populates="category")
    subcategories = relationship("Subcategory", back_populates="category")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    ticket_categories = relationship("TicketCategory", back_populates="category")

    def __repr__(self):
        """Return a string representation of the Category instance."""
        return f"<Category id={self.id} name={self.name}>"

    def to_dict(self):
        """
        Convert the Category instance to a dictionary.

        Returns:
            dict: A dictionary representation of the Category instance.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Category instance from a dictionary.

        Args:
            data (dict): A dictionary containing the category data.

        Returns:
            Category: An instance of the Category model.
        """
        return cls(name=data["name"])
