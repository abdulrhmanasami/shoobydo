"""inventory: add stock fields and movements table

Revision ID: 8ab3691aa5d9
Revises: f83a34166d76
Create Date: 2025-08-21 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ab3691aa5d9'
down_revision: Union[str, Sequence[str], None] = 'f83a34166d76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    # Add new stock fields to products table
    op.add_column('products', sa.Column('stock_on_hand', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('products', sa.Column('stock_reserved', sa.Integer(), nullable=False, server_default='0'))
    
    # Create stock_movements table
    op.create_table('stock_movements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('qty_change', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(length=64), nullable=False),
        sa.Column('notes', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_stock_movements_id'), 'stock_movements', ['id'], unique=False)
    op.create_index(op.f('ix_stock_movements_product_id'), 'stock_movements', ['product_id'], unique=False)
    
    # Add CHECK constraints
    op.create_check_constraint('ck_products_stock_on_hand_nonneg', 'products', 'stock_on_hand >= 0')
    op.create_check_constraint('ck_products_stock_reserved_nonneg', 'products', 'stock_reserved >= 0')
    op.create_check_constraint('ck_stock_movements_qty_change_not_zero', 'stock_movements', 'qty_change != 0')


def downgrade() -> None:
    """Downgrade schema."""
    
    # Drop CHECK constraints
    op.drop_constraint('ck_stock_movements_qty_change_not_zero', 'stock_movements', type_='check')
    op.drop_constraint('ck_products_stock_reserved_nonneg', 'products', type_='check')
    op.drop_constraint('ck_products_stock_on_hand_nonneg', 'products', type_='check')
    
    # Drop indexes
    op.drop_index(op.f('ix_stock_movements_product_id'), table_name='stock_movements')
    op.drop_index(op.f('ix_stock_movements_id'), table_name='stock_movements')
    
    # Drop table
    op.drop_table('stock_movements')
    
    # Drop columns
    op.drop_column('products', 'stock_reserved')
    op.drop_column('products', 'stock_on_hand')
