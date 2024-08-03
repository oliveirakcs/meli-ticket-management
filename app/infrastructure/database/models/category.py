"""Category Model"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class Category(Base):
    """
    Represents a category, which can have subcategories nested under it.

    Attributes:
        id (int): Primary key for the category.
        name (str): Name of the category.
        parent_id (int): Optional foreign key linking to the parent category.
    """

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    subcategories = relationship("Subcategory", back_populates="category")
    tickets = relationship("Ticket", back_populates="category")

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
            "parent_id": str(self.parent_id) if self.parent_id else None,
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
        return cls(name=data["name"], parent_id=data.get("parent_id"))
