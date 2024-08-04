"""Category Schemas"""

from typing import Optional, List
from pydantic import UUID4, BaseModel

from app.schemas.subcategory import SubcategoryShow


class Category(BaseModel):
    """Category Base Model"""

    name: str


class CategoryUpdate(BaseModel):
    """Category Update Model"""

    name: Optional[str] = None


class CategoryShow(Category):
    """Category Show Model"""

    id: UUID4
    subcategories: Optional[List[SubcategoryShow]] = None

    class Config:
        """Config"""

        from_attributes = True


class CategoryId(BaseModel):
    """Category ID Model"""

    id: UUID4

    class Config:
        """Config"""

        from_attributes = True
