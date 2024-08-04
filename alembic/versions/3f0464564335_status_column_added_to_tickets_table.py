"""status column added to tickets table

Revision ID: 3f0464564335
Revises: c8ace97bcb9c
Create Date: 2024-08-04 13:03:02.372379

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3f0464564335"
down_revision: Union[str, None] = "c8ace97bcb9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ticket_status_enum = postgresql.ENUM("ABERTO", "EM_PROGRESSO", "RESOLVIDO", name="ticketstatus")


def upgrade() -> None:
    ticket_status_enum.create(op.get_bind())

    op.add_column(
        "tickets", sa.Column("status", sa.Enum("ABERTO", "EM_PROGRESSO", "RESOLVIDO", name="ticketstatus"), nullable=False, server_default="ABERTO")
    )


def downgrade() -> None:
    op.drop_column("tickets", "status")

    ticket_status_enum.drop(op.get_bind())
