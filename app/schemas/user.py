"""User Schema"""

from typing import Optional
from pydantic import UUID4, BaseModel


class User(BaseModel):
    """User Base Model"""

    name: str
    username: str
    email: str
    password: str
    company_id: UUID4
    role: str


class UserUpdate(BaseModel):
    """User Update"""

    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    company_id: Optional[UUID4] = None
    role: Optional[str] = None


class UserShow(BaseModel):
    """User Show"""

    id: UUID4
    name: str
    username: str
    email: str
    password: str
    role: str

    class Config:
        """Config"""

        from_attributes = True


class UserId(User):
    """User Id"""

    id: UUID4


class UserPassword(BaseModel):
    """User Password"""

    password: str
