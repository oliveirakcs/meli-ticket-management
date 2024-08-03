"""Subcategory Model"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure import Base


class Subcategory(Base):
    """
    Represents a subcategory linked to a specific category.

    Attributes:
        id (int): Primary key for the subcategory.
        name (str): Name of the subcategory.
        category_id (int): Foreign key linking to the parent category.
    """

    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="subcategories")
    tickets = relationship("Ticket", back_populates="subcategory")

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
