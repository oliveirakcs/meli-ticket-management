"""Ticket Schema"""

from typing import Optional
from datetime import datetime
from pydantic import UUID4, BaseModel
from app.core.enums.enums import TicketStatus


class Ticket(BaseModel):
    """Ticket Base Model"""

    title: str
    description: Optional[str] = None
    category_id: UUID4
    subcategory_id: Optional[UUID4] = None
    severity_id: UUID4
    status: TicketStatus = TicketStatus.ABERTO


class TicketUpdate(BaseModel):
    """Ticket Update Model"""

    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID4] = None
    subcategory_id: Optional[UUID4] = None
    severity_id: Optional[UUID4] = None
    status: Optional[TicketStatus] = None


class TicketShow(Ticket):
    """Ticket Show Model"""

    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        """Config"""

        from_attributes = True


class TicketId(Ticket):
    """Ticket Id Model"""

    id: UUID4
