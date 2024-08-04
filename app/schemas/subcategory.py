"""Subcategory Schemas"""

from typing import Optional
from pydantic import BaseModel, UUID4


class Subcategory(BaseModel):
    """
    Base schema for subcategory attributes.

    Attributes:
        name (str): The name of the subcategory.
        category_id (UUID4): The UUID of the parent category.
    """

    name: str
    category_id: UUID4


class SubcategoryUpdate(BaseModel):
    """
    Schema for updating a subcategory.

    Attributes:
        name (Optional[str]): The updated name of the subcategory.
        category_id (Optional[UUID4]): The updated UUID of the parent category.
    """

    name: Optional[str] = None
    category_id: Optional[UUID4] = None


class SubcategoryShow(Subcategory):
    """
    Schema for displaying subcategory details.

    Attributes:
        id (UUID4): The UUID of the subcategory.
    """

    id: UUID4

    class Config:
        """Config"""

        from_attributes = True


class SubcategoryId(BaseModel):
    """
    Schema for displaying the UUID of a subcategory.

    Attributes:
        id (UUID4): The UUID of the subcategory.
    """

    id: UUID4

    class Config:
        """Config"""

        from_attributes = True
