"""Controllers for managing category operations in the database related to Ticket API endpoints."""

from typing import List
import logging
from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status, Depends
from app.infrastructure import get_db, Category
from app.schemas import CategoryUpdate as SchemaCategoryUpdate, CategoryShow as SchemaCategoryShow, Category as SchemaCategory

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CategoryController:
    """
    A controller class for managing category operations in the database.
    """

    def __init__(self, db: Session):
        """
        Initialize the CategoryController with a database session.

        Args:
            db (Session): The database session.
        """
        self.db = db

    def get_all(self) -> List[SchemaCategoryShow]:
        """
        Get all categories.

        Returns:
            List[SchemaCategoryShow]: A list of category objects.

        Raises:
            HTTPException: Raised if no categories are found.
        """
        categories = self.db.query(Category).all()
        if not categories:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No categories found")
        return categories

    def create(self, request: SchemaCategory) -> SchemaCategoryShow:
        """
        Create a new category.

        Args:
            request (SchemaCategory): The request containing details of the new category.

        Returns:
            SchemaCategoryShow: The newly created category object.

        Raises:
            HTTPException: Raised if a category with the same name already exists.
        """
        if not request.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name is required.",
            )
        try:
            existing_category = self.db.query(Category).filter_by(name=request.name).first()
            if existing_category:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"A category with name '{request.name}' already exists.",
                )

            new_category = Category(name=request.name)

            self.db.add(new_category)
            self.db.commit()
            self.db.refresh(new_category)

            return new_category
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("Error creating category: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the category. Please try again."
            ) from e

    def show(self, category_id: UUID4) -> SchemaCategoryShow:
        """
        Retrieve a category by category ID.

        Args:
            category_id (UUID4): The ID of the category to retrieve.

        Returns:
            SchemaCategoryShow: The category corresponding to the provided ID.

        Raises:
            HTTPException: Raised if the category with the provided ID is not found.
        """
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category {category_id} not found",
            )
        return category

    def update(self, category_id: UUID4, request: SchemaCategoryUpdate) -> SchemaCategoryShow:
        """
        Update category information.

        Args:
            category_id (UUID4): The ID of the category to update.
            request (CategoryUpdate): The updated category information.

        Returns:
            SchemaCategoryShow: The updated category information.

        Raises:
            HTTPException: Raised if the category with the provided ID is not found or if any field is invalid.
        """
        try:
            category = self.db.query(Category).filter(Category.id == category_id).first()
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category {category_id} not found",
                )

            if request.name:
                existing_category = self.db.query(Category).filter_by(name=request.name).first()
                if existing_category:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"A category with name '{request.name}' already exists.",
                    )

            for key, value in request.model_dump(exclude_unset=True).items():
                setattr(category, key, value)

            self.db.commit()
            self.db.refresh(category)
            return category
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("Error updating category %s: %s", category_id, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while updating the category. Please try again."
            ) from e

    def delete(self, category_id: UUID4) -> str:
        """
        Delete a category by category UUID.

        Args:
            category_id (UUID4): The ID of the category to be deleted.

        Returns:
            str: A message confirming the deletion of the category.

        Raises:
            HTTPException: Raised if the category with the provided ID is not found.
        """
        try:
            category = self.db.query(Category).filter(Category.id == category_id).first()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category {category_id} not found")

            self.db.delete(category)
            self.db.commit()
            return f"Category {category_id} deleted."
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("Error deleting category %s: %s", category_id, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while deleting the category. Please try again."
            ) from e


def get_category_controller(db: Session = Depends(get_db)):
    """
    Dependency to get an instance of CategoryController.

    Args:
        db (Session): The database session.

    Returns:
        CategoryController: An instance of CategoryController.
    """
    return CategoryController(db=db)
