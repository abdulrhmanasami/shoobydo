"""orders: indexes + checks

Revision ID: orders_indexes_checks_20250821
Revises: 
Create Date: 2025-08-21
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'orders_indexes_checks_20250821'
down_revision = '8daeac2d2c8f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # indexes
    op.create_index('ix_orders_customer_id', 'orders', ['customer_id'], unique=False)
    op.create_index('ix_orders_status', 'orders', ['status'], unique=False)
    op.create_index('ix_orders_created_at', 'orders', ['created_at'], unique=False)
    # checks
    op.create_check_constraint('ck_orders_total_nonneg', 'orders', 'total >= 0')
    op.create_check_constraint('ck_orders_currency_len3', 'orders', 'length(currency)=3')


def downgrade() -> None:
    op.drop_constraint('ck_orders_currency_len3', 'orders', type_='check')
    op.drop_constraint('ck_orders_total_nonneg', 'orders', type_='check')
    op.drop_index('ix_orders_created_at', table_name='orders')
    op.drop_index('ix_orders_status', table_name='orders')
    op.drop_index('ix_orders_customer_id', table_name='orders')


