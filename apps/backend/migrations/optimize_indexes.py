"""Database optimization migrations"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    """Add database indexes for performance"""
    # Unique index on users.email
    op.create_index("ux_users_email", "users", ["email"], unique=True)
    
    # Index on foreign keys
    op.create_index("ix_orders_customer_id", "orders", ["customer_id"])
    op.create_index("ix_order_items_order_id", "order_items", ["order_id"])
    op.create_index("ix_order_items_product_id", "order_items", ["product_id"])

def downgrade():
    """Remove database indexes"""
    op.drop_index("ux_users_email", "users")
    op.drop_index("ix_orders_customer_id", "orders")
    op.drop_index("ix_order_items_order_id", "order_items")
    op.drop_index("ix_order_items_product_id", "order_items")
