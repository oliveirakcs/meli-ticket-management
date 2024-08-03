"""Severity Model"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class Severity(Base):
    """
    Represents the severity level of a ticket.

    Attributes:
        id (int): Primary key for severity.
        level (int): Severity level ranging from 1 to 4.
        description (str): Description of the severity level.
    """

    __tablename__ = "severity"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, nullable=False, unique=True)
    description = Column(String, nullable=False)

    tickets = relationship("Ticket", back_populates="severity")

    def __repr__(self):
        """Return a string representation of the Severity instance."""
        return f"<Severity id={self.id} level={self.level}>"

    def to_dict(self):
        """
        Convert the Severity instance to a dictionary.

        Returns:
            dict: A dictionary representation of the Severity instance.
        """
        return {
            "id": str(self.id),
            "level": self.level,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Severity instance from a dictionary.

        Args:
            data (dict): A dictionary containing the severity data.

        Returns:
            Severity: An instance of the Severity model.
        """
        return cls(level=data["level"], description=data["description"])
