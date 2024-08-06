"""Subcategory routers"""

from typing import List
from fastapi import APIRouter, Depends, status, Security
from pydantic import UUID4
from app.api.v1 import SubcategoryController, get_subcategory_controller
from app.schemas import Subcategory, SubcategoryShow, SubcategoryUpdate
from app.core.auth.oauth import get_current_active_user

router = APIRouter(prefix="/subcategories", tags=["Subcategories"])


@router.get("/", response_model=List[SubcategoryShow], status_code=status.HTTP_200_OK)
def get_all_subcategories(
    controller: SubcategoryController = Depends(get_subcategory_controller),
    current_user=Security(get_current_active_user, scopes=["read"]),
):
    """
    Retrieve all subcategories.

    Parameters:
    - controller (SubcategoryController): The subcategory controller instance.
    - current_user: The current user for authorization (unused here).

    Returns:
    - List[SubcategoryShow]: A list of subcategory objects with restricted information.
    """
    return controller.get_all()


@router.post("/", response_model=SubcategoryShow, status_code=status.HTTP_201_CREATED)
def create_subcategory(
    request: Subcategory,
    controller: SubcategoryController = Depends(get_subcategory_controller),
    current_user=Security(get_current_active_user, scopes=["admin"]),
):
    """
    Create a new subcategory.

    Parameters:
    - request (Subcategory): The subcategory data to create.
    - controller (SubcategoryController): The subcategory controller instance.
    - current_user: The current user for authorization.

    Returns:
    - SubcategoryShow: The created subcategory object with restricted information.
    """
    return controller.create(request)


@router.get("/{subcategory_id}", response_model=SubcategoryShow, status_code=status.HTTP_200_OK)
def get_subcategory(
    subcategory_id: UUID4,
    controller: SubcategoryController = Depends(get_subcategory_controller),
    current_user=Security(get_current_active_user, scopes=["read"]),
):
    """
    Retrieve a subcategory by ID.

    Parameters:
    - subcategory_id (UUID4): The ID of the subcategory to retrieve.
    - controller (SubcategoryController): The subcategory controller instance.
    - current_user: The current user for authorization.

    Returns:
    - SubcategoryShow: The subcategory object with restricted information.
    """
    return controller.show(subcategory_id)


@router.get("/{category_id}/show", response_model=List[SubcategoryShow], status_code=status.HTTP_200_OK)
def get_subcategory_by_category(
    category_id: UUID4,
    controller: SubcategoryController = Depends(get_subcategory_controller),
    current_user=Security(get_current_active_user, scopes=["read"]),
):
    """
    Retrieve a subcategory by category ID.

    Parameters:
    - category_id (UUID4): The ID of the category to retrieve subcategories.
    - controller (SubcategoryController): The subcategory controller instance.
    - current_user: The current user for authorization.

    Returns:
    - List[SubcategoryShow]: A list of subcategory objects with restricted information.
    """
    return controller.show_by_category(category_id)


@router.patch("/{subcategory_id}", response_model=SubcategoryShow, status_code=status.HTTP_200_OK)
def update_subcategory(
    subcategory_id: UUID4,
    request: SubcategoryUpdate,
    controller: SubcategoryController = Depends(get_subcategory_controller),
    current_user=Security(get_current_active_user, scopes=["admin"]),
):
    """
    Update a subcategory.

    Parameters:
    - subcategory_id (UUID4): The ID of the subcategory to update.
    - request (SubcategoryUpdate): The updated subcategory data.
    - controller (SubcategoryController): The subcategory controller instance.
    - current_user: The current user for authorization.

    Returns:
    - SubcategoryShow: The updated subcategory object with restricted information.
    """
    return controller.update(subcategory_id, request)


@router.delete("/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subcategory(
    subcategory_id: UUID4,
    controller: SubcategoryController = Depends(get_subcategory_controller),
    current_user=Security(get_current_active_user, scopes=["admin"]),
):
    """
    Delete a subcategory.

    Parameters:
    - subcategory_id (UUID4): The ID of the subcategory to delete.
    - controller (SubcategoryController): The subcategory controller instance.
    - current_user: The current user for authorization.

    Returns:
    - str: A message confirming the deletion of the subcategory.
    """
    return controller.delete(subcategory_id)
