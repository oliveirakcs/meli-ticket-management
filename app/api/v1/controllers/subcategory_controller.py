"""Controllers for managing subcategory operations in the database related to Ticket API endpoints."""

from typing import List
from pydantic import UUID4
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas import Subcategory as SchemaSubcategory, SubcategoryUpdate as SchemaSubcategoryUpdate, SubcategoryShow as SchemaSubcategoryShow
from app.infrastructure import Subcategory, get_db


class SubcategoryController:
    """
    Controller class for managing subcategory operations in the database.
    """

    def __init__(self, db: Session):
        """
        Initialize the TicketController with a database session.

        Args:
            db (Session): The database session.
        """
        self.db = db

    def get_all(self) -> List[SchemaSubcategoryShow]:
        """
        Retrieve all subcategories.

        Returns:
            List[SchemaSubcategoryShow]: A list of all subcategory objects.
        """
        return self.db.query(Subcategory).all()

    def create(self, request: SchemaSubcategory) -> SchemaSubcategoryShow:
        """
        Create a new subcategory.

        Args:
            request (SchemaSubcategory): The request containing subcategory details.

        Returns:
            SchemaSubcategoryShow: The newly created subcategory object.

        Raises:
            HTTPException: If a subcategory with the same name already exists.
        """
        existing_subcategory = self.db.query(Subcategory).filter_by(name=request.name, category_id=request.category_id).first()
        if existing_subcategory:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Subcategory '{request.name}' already exists under this category.",
            )

        new_subcategory = Subcategory(name=request.name, category_id=request.category_id)

        self.db.add(new_subcategory)
        self.db.commit()
        self.db.refresh(new_subcategory)

        return new_subcategory

    def show(self, subcategory_id: UUID4) -> SchemaSubcategoryShow:
        """
        Retrieve a subcategory by its ID.

        Args:
            subcategory_id (UUID4): The ID of the subcategory.

        Returns:
            SchemaSubcategoryShow: The subcategory object.

        Raises:
            HTTPException: If the subcategory is not found.
        """
        subcategory = self.db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
        if not subcategory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subcategory {subcategory_id} not found",
            )
        return subcategory

    def update(self, subcategory_id: UUID4, request: SchemaSubcategoryUpdate) -> SchemaSubcategoryShow:
        """
        Update an existing subcategory.

        Args:
            subcategory_id (UUID4): The ID of the subcategory to update.
            request (SchemaSubcategoryUpdate): The updated subcategory details.

        Returns:
            SchemaSubcategoryShow: The updated subcategory object.

        Raises:
            HTTPException: If the subcategory is not found.
        """
        subcategory = self.db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
        if not subcategory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subcategory {subcategory_id} not found",
            )

        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(subcategory, key, value)

        self.db.commit()
        self.db.refresh(subcategory)
        return subcategory

    def delete(self, subcategory_id: UUID4) -> str:
        """
        Delete a subcategory by its ID.

        Args:
            subcategory_id (UUID4): The ID of the subcategory to delete.

        Returns:
            str: A message confirming the deletion.

        Raises:
            HTTPException: If the subcategory is not found.
        """
        subcategory = self.db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
        if not subcategory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Subcategory {subcategory_id} not found",
            )

        self.db.delete(subcategory)
        self.db.commit()
        return f"Subcategory {subcategory_id} deleted successfully."


def get_subcategory_controller(db: Session = Depends(get_db)):
    """
    Dependency to get an instance of SubcategoryController.

    Args:
        db (Session): The database session.

    Returns:
        SubcategoryController: An instance of SubcategoryController.
    """
    return SubcategoryController(db=db)
