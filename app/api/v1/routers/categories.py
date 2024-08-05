"""Category routers"""

from typing import List
from fastapi import APIRouter, Depends, Security, status
from pydantic import UUID4
from app.schemas import Category, CategoryShow, CategoryUpdate
from app.api.v1 import get_category_controller, CategoryController
from app.core.auth.oauth import get_current_active_user

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get(
    "/",
    response_model=List[CategoryShow],
    status_code=status.HTTP_200_OK,
)
def get_all_categories(
    controller: CategoryController = Depends(get_category_controller),
    current_user: CategoryShow = Security(get_current_active_user, scopes=["read"]),
):
    """
    Retrieve all categories.

    Retrieves all categories stored in the database.

    Parameters:
    - controller (CategoryController): The category controller instance.
    - _: CategoryShow: The current user (unused).

    Returns:
    - List[CategoryShow]: A list of category objects with restricted information.

    Raises:
    - HTTPException: If there's an issue retrieving categories from the database.
    """
    return controller.get_all()


@router.post(
    "/",
    response_model=CategoryShow,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    request: Category,
    controller: CategoryController = Depends(get_category_controller),
    current_user: CategoryShow = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Create a new category.

    Parameters:
    - request (Category): The category data to create the new category.
    - controller (CategoryController): The category controller instance.
    - _: CategoryShow: The current user (unused).

    Returns:
    - CategoryShow: The created category data with restricted information.

    Raises:
    - HTTPException: If there's an issue creating the category.
    """
    return controller.create(request)


@router.delete("/", status_code=status.HTTP_202_ACCEPTED)
def delete_category(
    category_id: UUID4,
    controller: CategoryController = Depends(get_category_controller),
    current_user: CategoryShow = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Delete a category.

    Parameters:
    - category_id (UUID4): The ID of the category to delete.
    - controller (CategoryController): The category controller instance.
    - _: CategoryShow: The current user (unused).

    Returns:
    - None

    Raises:
    - HTTPException: If there's an issue deleting the category.
    """
    return controller.delete(category_id)


@router.get("/{category_id}", response_model=CategoryShow, status_code=status.HTTP_200_OK)
def get_category(
    category_id: UUID4,
    controller: CategoryController = Depends(get_category_controller),
    current_user: CategoryShow = Security(get_current_active_user, scopes=["read"]),
):
    """
    Retrieve category by category ID.

    Parameters:
    - category_id (UUID4): The ID of the category to retrieve.
    - controller (CategoryController): The category controller instance.
    - _: CategoryShow: The current user (unused).

    Returns:
    - CategoryShow: The category data with restricted information.

    Raises:
    - HTTPException: If the category with the specified ID is not found.
    """
    return controller.show(category_id)


@router.patch(
    "/{category_id}",
    response_model=CategoryShow,
    status_code=status.HTTP_200_OK,
)
def update_category(
    category_id: UUID4,
    request: CategoryUpdate,
    controller: CategoryController = Depends(get_category_controller),
    current_user: CategoryShow = Security(get_current_active_user, scopes=["admin"]),
):
    """
    Update category data.

    Parameters:
    - category_id (UUID4): The ID of the category to update.
    - request (CategoryUpdate): The category data to be updated.
    - controller (CategoryController): The category controller instance.
    - _: CategoryShow: The current user (unused).

    Returns:
    - CategoryShow: The updated category data with restricted information.

    Raises:
    - HTTPException: If the category with the specified ID is not found or if there's an issue updating the category.
    """
    updated_category = controller.update(category_id, request)
    return updated_category
