"""Ticket Schema"""

from typing import Optional, List
from datetime import datetime
from pydantic import UUID4, BaseModel
from app.core.enums.enums import TicketStatus
from app.schemas.category import CategoryShow
from app.schemas.severity import SeverityShow


class Ticket(BaseModel):
    """Ticket Base Model"""

    title: str
    description: Optional[str] = None
    category_ids: List[UUID4]
    subcategory_ids: Optional[List[UUID4]] = None
    severity_id: UUID4
    status: TicketStatus = TicketStatus.ABERTO
    comment: Optional[str] = None
    comment_user: Optional[str] = None


class TicketUpdate(BaseModel):
    """Ticket Update Model"""

    title: Optional[str] = None
    description: Optional[str] = None
    category_ids: Optional[List[UUID4]] = None
    subcategory_ids: Optional[List[UUID4]] = None
    severity_id: Optional[UUID4] = None
    status: Optional[TicketStatus] = None
    comment: Optional[str] = None
    comment_user: Optional[str] = None


class TicketShow(BaseModel):
    """Ticket Show Model"""

    id: UUID4
    title: str
    description: Optional[str] = None
    categories: List[CategoryShow]
    severity: SeverityShow
    status: TicketStatus
    comment: Optional[str] = None
    comment_user: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Config"""

        from_attributes = True


class TicketId(Ticket):
    """Ticket Id Model"""

    id: UUID4
