"""add new logistics enum values

Revision ID: e4a85146ff81
Revises: f0a6a060bd75
Create Date: 2026-07-08 15:06:24.238177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'e4a85146ff81'
down_revision: Union[str, Sequence[str], None] = 'f0a6a060bd75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade() -> None:
    op.execute("ALTER TYPE delivery_status ADD VALUE IF NOT EXISTS 'WAITING_LOADING'")
    op.execute("ALTER TYPE delivery_status ADD VALUE IF NOT EXISTS 'LOADED'")
    op.execute("ALTER TYPE delivery_status ADD VALUE IF NOT EXISTS 'WAITING_UNLOADING'")
    op.execute("ALTER TYPE delivery_status ADD VALUE IF NOT EXISTS 'UNLOADING'")

    op.execute("ALTER TYPE truck_status ADD VALUE IF NOT EXISTS 'WAITING_LOADING'")
    op.execute("ALTER TYPE truck_status ADD VALUE IF NOT EXISTS 'LOADED'")
    op.execute("ALTER TYPE truck_status ADD VALUE IF NOT EXISTS 'WAITING_UNLOADING'")
    op.execute("ALTER TYPE truck_status ADD VALUE IF NOT EXISTS 'UNLOADING'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
