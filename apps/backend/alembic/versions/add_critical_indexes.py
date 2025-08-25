"""add critical indexes for performance

Revision ID: add_critical_indexes
Revises: 984e962781ef
Create Date: 2025-08-24 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_critical_indexes'
down_revision: Union[str, Sequence[str], None] = '984e962781ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add critical indexes for performance"""
    
    # Users table indexes
    op.create_index('ix_users_email_unique', 'users', ['email'], unique=True)
    op.create_index('ix_users_role', 'users', ['role'])
    
    # Products table indexes
    op.create_index('ix_products_sku_unique', 'products', ['sku'], unique=True)
    op.create_index('ix_products_supplier_id', 'products', ['supplier_id'])
    op.create_index('ix_products_stock', 'products', ['stock_on_hand', 'stock_reserved'])
    
    # Orders table indexes
    op.create_index('ix_orders_status_created', 'orders', ['status', 'created_at'])
    op.create_index('ix_orders_customer_status', 'orders', ['customer_id', 'status'])
    op.create_index('ix_orders_total_range', 'orders', ['total'])
    
    # Order items indexes
    op.create_index('ix_order_items_product_order', 'order_items', ['product_id', 'order_id'])
    
    # Stock movements indexes
    op.create_index('ix_stock_movements_product_date', 'stock_movements', ['product_id', 'created_at'])
    op.create_index('ix_stock_movements_reason', 'stock_movements', ['reason'])
    
    # Suppliers indexes
    op.create_index('ix_suppliers_name', 'suppliers', ['name'])
    op.create_index('ix_suppliers_file_path_unique', 'suppliers', ['file_path'], unique=True)


def downgrade() -> None:
    """Remove critical indexes"""
    
    # Users table indexes
    op.drop_index('ix_users_email_unique', table_name='users')
    op.drop_index('ix_users_role', table_name='users')
    
    # Products table indexes
    op.drop_index('ix_products_sku_unique', table_name='products')
    op.drop_index('ix_products_supplier_id', table_name='products')
    op.drop_index('ix_products_stock', table_name='products')
    
    # Orders table indexes
    op.drop_index('ix_orders_status_created', table_name='orders')
    op.drop_index('ix_orders_customer_status', table_name='orders')
    op.drop_index('ix_orders_total_range', table_name='orders')
    
    # Order items indexes
    op.drop_index('ix_order_items_product_order', table_name='order_items')
    
    # Stock movements indexes
    op.drop_index('ix_stock_movements_product_date', table_name='stock_movements')
    op.drop_index('ix_stock_movements_reason', table_name='stock_movements')
    
    # Suppliers indexes
    op.drop_index('ix_suppliers_name', table_name='suppliers')
    op.drop_index('ix_suppliers_file_path_unique', table_name='suppliers')
