"""Severity Schemas"""

from typing import Optional
from pydantic import UUID4, BaseModel


class Severity(BaseModel):
    """Severity Base Model"""

    level: int
    description: str


class SeverityUpdate(BaseModel):
    """Severity Update Model"""

    level: Optional[int] = None
    description: Optional[str] = None


class SeverityShow(Severity):
    """Severity Show Model"""

    id: UUID4

    class Config:
        """Config"""

        from_attributes = True


class SeverityId(Severity):
    """Severity Id Model"""

    id: UUID4
