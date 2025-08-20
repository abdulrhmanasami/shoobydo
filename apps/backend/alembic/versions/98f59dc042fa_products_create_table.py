"""products: create table

Revision ID: 98f59dc042fa
Revises: 7b03bdad456c
Create Date: 2025-08-20 03:44:56.905063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98f59dc042fa'
down_revision: Union[str, Sequence[str], None] = '7b03bdad456c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """No-op: prior migration already created products; avoid re-creating users."""
    pass


def downgrade() -> None:
    """No-op."""
    pass
