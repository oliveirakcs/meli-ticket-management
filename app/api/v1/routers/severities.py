"""Severity routers"""

from typing import List
from fastapi import APIRouter, Depends, Security, status
from pydantic import UUID4
from app.schemas import Severity, SeverityShow, SeverityUpdate
from app.api.v1 import get_severity_controller, SeverityController
from app.core.auth.oauth import get_current_active_user

router = APIRouter(prefix="/severities", tags=["Severities"])


@router.get(
    "/",
    response_model=List[SeverityShow],
    status_code=status.HTTP_200_OK,
)
def get_all_severities(
    controller: SeverityController = Depends(get_severity_controller),
    current_user: SeverityShow = Security(get_current_active_user, scopes=["read"]),
):
    """
    Retrieve all severity levels.

    Retrieves all severity levels stored in the database.

    Parameters:
    - controller (SeverityController): The severity controller instance.
    - _: SeverityShow: The current user (unused).

    Returns:
    - List[SeverityShow]: A list of severity objects with restricted information.

    Raises:
    - HTTPException: If there's an issue retrieving severity levels from the database.
    """
    return controller.get_all()


@router.post(
    "/",
    response_model=SeverityShow,
    status_code=status.HTTP_201_CREATED,
)
def create_severity(
    request: Severity,
    controller: SeverityController = Depends(get_severity_controller),
    current_user: SeverityShow = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Create a new severity level.

    Parameters:
    - request (Severity): The severity data to create the new severity level.
    - controller (SeverityController): The severity controller instance.
    - _: SeverityShow: The current user (unused).

    Returns:
    - SeverityShow: The created severity data with restricted information.

    Raises:
    - HTTPException: If there's an issue creating the severity level.
    """
    return controller.create(request)


@router.delete("/", status_code=status.HTTP_202_ACCEPTED)
def delete_severity(
    severity_id: UUID4,
    controller: SeverityController = Depends(get_severity_controller),
    current_user: SeverityShow = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Delete a severity level.

    Parameters:
    - severity_id (UUID4): The ID of the severity level to delete.
    - controller (SeverityController): The severity controller instance.
    - _: SeverityShow: The current user (unused).

    Returns:
    - None

    Raises:
    - HTTPException: If there's an issue deleting the severity level.
    """
    return controller.delete(severity_id)


@router.get("/{severity_id}", response_model=SeverityShow, status_code=status.HTTP_200_OK)
def get_severity(
    severity_id: UUID4,
    controller: SeverityController = Depends(get_severity_controller),
    current_user: SeverityShow = Security(get_current_active_user, scopes=["read"]),
):
    """
    Retrieve severity level by severity ID.

    Parameters:
    - severity_id (UUID4): The ID of the severity level to retrieve.
    - controller (SeverityController): The severity controller instance.
    - _: SeverityShow: The current user (unused).

    Returns:
    - SeverityShow: The severity level data with restricted information.

    Raises:
    - HTTPException: If the severity level with the specified ID is not found.
    """
    return controller.show(severity_id)


@router.patch(
    "/{severity_id}",
    response_model=SeverityShow,
    status_code=status.HTTP_200_OK,
)
def update_severity(
    severity_id: UUID4,
    request: SeverityUpdate,
    controller: SeverityController = Depends(get_severity_controller),
    current_user: SeverityShow = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Update severity level data.

    Parameters:
    - severity_id (UUID4): The ID of the severity level to update.
    - request (SeverityUpdate): The severity level data to be updated.
    - controller (SeverityController): The severity controller instance.
    - _: SeverityShow: The current user (unused).

    Returns:
    - SeverityShow: The updated severity level data with restricted information.

    Raises:
    - HTTPException: If the severity level with the specified ID is not found or if there's an issue updating the severity level.
    """
    updated_severity = controller.update(severity_id, request)
    return updated_severity
