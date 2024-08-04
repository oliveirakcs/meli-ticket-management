"""Controllers for managing user operations in the database related to User API endpoints."""

from typing import List
from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from app.core import Hash
from app.infrastructure import get_db, User
from app.schemas import UserUpdate as SchemaUserUpdate, User as SchemaUser, UserShow as SchemaUserShow


class UserController:
    """
    A controller class for managing user operations in the database.
    """

    def __init__(self, db: Session):
        """
        Initialize the UserController with a database session.

        Args:
            db (Session): The database session.
        """
        self.db = db

    def get_all(self) -> List[SchemaUserShow]:
        """
        Get all users.

        Returns:
            List[SchemaUserShow]: A list of user objects.

        Raises:
            HTTPException: Raised if no users are found.
        """
        users = self.db.query(User).all()
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return users

    def create(self, request: SchemaUser) -> SchemaUserShow:
        """
        Create a new user.

        Args:
            request (UserCreate): The request containing details of the new user.

        Returns:
            SchemaUserShow: The newly created user object.

        Raises:
            HTTPException: Raised if any required field is not provided or if a user with the same username already exists.
        """
        required_fields = [request.name, request.username, request.email, request.password]
        if not all(required_fields):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All fields must be filled",
            )

        existing_user = self.db.query(User).filter_by(username=request.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A user with the username '{request.username}' already exists.",
            )

        new_user = User(
            name=request.name,
            username=request.username,
            email=request.email,
            password=Hash.bcrypt(request.password),
            role=request.role,
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def show(self, user_id: UUID4) -> SchemaUserShow:
        """
        Retrieve a user by user ID.

        Args:
            user_id (UUID4): The ID of the user to retrieve.

        Returns:
            SchemaUserShow: The user corresponding to the provided ID.

        Raises:
            HTTPException: Raised if the user with the provided ID is not found.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )
        return user

    def update(self, user_id: UUID4, request: SchemaUserUpdate) -> SchemaUserShow:
        """
        Update user information.

        Args:
            user_id (UUID4): The ID of the user to update.
            request (UserUpdate): The updated user information.

        Returns:
            SchemaUserShow: The updated user information.

        Raises:
            HTTPException: Raised if the user with the provided ID is not found or if any field is left blank.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )

        if any(value == "" for value in request.model_dump(exclude_unset=True).values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No field can be left blank",
            )

        for key, value in request.dict(exclude_unset=True).items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def reset_password(self, user_id: UUID4, password: str) -> User:
        """
        Update the password of a user.

        Args:
            user_id (UUID4): The ID of the user whose password is to be updated.
            password (str): The new password for the user.

        Returns:
            User: The user with the updated password.

        Raises:
            HTTPException: Raised if the user with the provided ID is not found.
        """
        user = self.db.query(User).filter(User.id == user_id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")

        user_dict = user.first().to_dict()
        user_dict["password"] = Hash.bcrypt(password)
        user.update(user_dict)
        self.db.commit()
        return user.first()

    def delete(self, user_id: UUID4) -> str:
        """
        Delete a user by user UUID.

        Args:
            user_id (UUID4): The ID of the user to be deleted.

        Returns:
            str: A message confirming the deletion of the user.

        Raises:
            HTTPException: Raised if the user with the provided ID is not found.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")

        self.db.delete(user)
        self.db.commit()
        return f"User {user_id} deleted."


def get_user_controller(db: Session = Depends(get_db)):
    """
    Dependency to get an instance of UserController.

    Args:
        db (Session): The database session.

    Returns:
        UserController: An instance of UserController.
    """
    return UserController(db=db)
