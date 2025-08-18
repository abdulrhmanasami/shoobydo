"""create suppliers table with fields

Revision ID: 4b86998887ef
Revises: 257477cfcef8
Create Date: 2025-08-18 20:04:45.578226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b86998887ef'
down_revision: Union[str, Sequence[str], None] = '257477cfcef8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'suppliers',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=1024), nullable=False, unique=True),
        sa.Column('rows', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('sheets', sa.Integer(), nullable=False, server_default='0'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('suppliers')
