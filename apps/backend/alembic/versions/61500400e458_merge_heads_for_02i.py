"""merge heads for 02I

Revision ID: 61500400e458
Revises: orders_indexes_checks_20250821, 8daeac2d2c8f
Create Date: 2025-08-21 12:32:31.031804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61500400e458'
down_revision: Union[str, Sequence[str], None] = ('orders_indexes_checks_20250821', '8daeac2d2c8f')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
