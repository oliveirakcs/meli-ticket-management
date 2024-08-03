"""User routers"""

from typing import List
from fastapi import APIRouter, Depends, Security, status
from pydantic import UUID4
from app.schemas import User, UserShow, UserUpdate, UserPassword
from app.api.v1 import get_user_controller, UserController
from app.core.auth.oauth import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=List[UserShow],
    status_code=status.HTTP_200_OK,
)
def get_all_users(
    controller: UserController = Depends(get_user_controller),
    current_user: User = Security(get_current_active_user, scopes=["read"]),
):
    """
    Retrieve all users.

    Retrieves all users stored in the database.

    Parameters:
    - controller (UserController): The user controller instance.
    - _: User: The current user (unused).

    Returns:
    - List[UserShow]: A list of user objects with restricted information.

    Raises:
    - HTTPException: If there's an issue retrieving users from the database.
    """
    return controller.get_all()


@router.post(
    "/",
    response_model=UserShow,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: User, controller: UserController = Depends(get_user_controller), current_user: User = Security(get_current_active_user, scopes=["admin"])
):
    """
    Create a new user.

    Parameters:
    - request (User): The user data to create the new user.
    - controller (UserController): The user controller instance.
    - _: User: The current user (unused).

    Returns:
    - UserShow: The created user data with restricted information.

    Raises:
    - HTTPException: If there's an issue creating the user.
    """
    return controller.create(request)


@router.delete("/", status_code=status.HTTP_202_ACCEPTED)
def delete_user(
    user_id: UUID4,
    controller: UserController = Depends(get_user_controller),
    current_user: User = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Delete a user.

    Parameters:
    - user_id (UUID4): The ID of the user to delete.
    - controller (UserController): The user controller instance.
    - _: User: The current user (unused).

    Returns:
    - None

    Raises:
    - HTTPException: If there's an issue deleting the user.
    """
    return controller.delete(user_id)


@router.get("/{user_id}", response_model=UserShow, status_code=status.HTTP_200_OK)
def get_user(
    user_id: UUID4, controller: UserController = Depends(get_user_controller), current_user: User = Security(get_current_active_user, scopes=["read"])
):
    """
    Retrieve user by user ID.

    Parameters:
    - user_id (UUID4): The ID of the user to retrieve.
    - controller (UserController): The user controller instance.
    - _: User: The current user (unused).

    Returns:
    - UserShow: The user data with restricted information.

    Raises:
    - HTTPException: If the user with the specified ID is not found.
    """
    return controller.show(user_id)


@router.patch(
    "/{user_id}",
    response_model=UserShow,
    status_code=status.HTTP_200_OK,
)
def update_user(
    user_id: UUID4,
    request: UserUpdate,
    controller: UserController = Depends(get_user_controller),
    current_user: User = Security(get_current_active_user, scopes=["manage"]),
):
    """
    Update user data.

    Parameters:
    - user_id (UUID4): The ID of the user to update.
    - request (UserUpdate): The user data to be updated.
    - controller (UserController): The user controller instance.
    - _: User: The current user (unused).

    Returns:
    - UserShow: The updated user data with restricted information.

    Raises:
    - HTTPException: If the user with the specified ID is not found or if there's an issue updating the user.
    """
    updated_user = controller.update(user_id, request)
    return updated_user


@router.put(
    "/{user_id}/reset_password",
    response_model=UserShow,
    status_code=status.HTTP_200_OK,
)
def reset_password(
    user_id: UUID4,
    request: UserPassword,
    controller: UserController = Depends(get_user_controller),
    current_user: User = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Reset user password.

    Resets the password for the user corresponding to the specified user ID.

    Parameters:
    - user_id (UUID4): The ID of the user whose password needs to be reset.
    - request (UserPassword): The new password request.
    - controller (UserController): The user controller instance.
    - _: User: The current user (unused).

    Returns:
    - UserShow: The updated user data with restricted information.

    Raises:
    - HTTPException: If the user with the specified ID is not found or if there's an issue resetting the password.
    """
    password = request.password
    return controller.reset_password(user_id, password)
