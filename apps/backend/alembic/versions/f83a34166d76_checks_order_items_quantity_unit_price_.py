"""checks: order_items/quantity,unit_price and orders/total

Revision ID: f83a34166d76
Revises: 72a2e306cde0
Create Date: 2025-08-21 21:37:14.174776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f83a34166d76'
down_revision: Union[str, Sequence[str], None] = '72a2e306cde0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
