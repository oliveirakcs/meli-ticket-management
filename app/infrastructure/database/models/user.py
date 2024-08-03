"""User Model"""

import uuid
from sqlalchemy import Column, String, Boolean, DateTime, UUID
from sqlalchemy.sql import func

from app.infrastructure.database import Base


class User(Base):
    """
    User model representing a user in the database.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (UUID): The unique identifier for the user, auto-generated.
        username (str): The unique username of the user.
        name (str): The name of the user, cannot be null.
        email (str): The email address of the user, cannot be null.
        password (str): The password of the user, cannot be null.
        active (bool): Indicates whether the user account is active, defaults to True.
        role (str): The role of the user.
        company_id (UUID): The identifier of the associated company.
        company (relationship): A read-only relationship to the Company model.
        created_at (DateTime): The timestamp when the user record was created, auto-generated.
        updated_at (DateTime): The timestamp when the user record was last updated, auto-generated.

    Methods:
        __repr__(): Returns a string representation of the user object.
        to_dict(): Returns a dictionary representation of the user object.
    """

    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    role = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        """
        Return a string representation of the user object.

        Returns:
            str: A string representation of the user object.
        """
        return f"<User id={self.id} username={self.username}>"

    def to_dict(self):
        """
        Return a dictionary representation of the user object.

        Returns:
            dict: A dictionary representation of the user object.
        """
        return {
            "id": str(self.id),
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "active": self.active,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
