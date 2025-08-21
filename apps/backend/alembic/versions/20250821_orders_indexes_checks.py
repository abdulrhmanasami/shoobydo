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
    # Guarded DDL to avoid failures if 'orders' not yet present on some envs
    op.execute(
        """
        DO $$
        BEGIN
            IF to_regclass('public.orders') IS NOT NULL THEN
                -- indexes (IF NOT EXISTS is supported for indexes)
                CREATE INDEX IF NOT EXISTS ix_orders_customer_id ON orders (customer_id);
                CREATE INDEX IF NOT EXISTS ix_orders_status ON orders (status);
                CREATE INDEX IF NOT EXISTS ix_orders_created_at ON orders (created_at);

                -- checks (no IF NOT EXISTS, emulate via pg_constraint lookup)
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint WHERE conname = 'ck_orders_total_nonneg'
                ) THEN
                    ALTER TABLE orders ADD CONSTRAINT ck_orders_total_nonneg CHECK (total >= 0);
                END IF;

                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint WHERE conname = 'ck_orders_currency_len3'
                ) THEN
                    ALTER TABLE orders ADD CONSTRAINT ck_orders_currency_len3 CHECK (length(currency) = 3);
                END IF;
            END IF;
        END$$;
        """
    )


def downgrade() -> None:
    # Best-effort drops (skip if table/objects are missing)
    op.execute(
        """
        DO $$
        BEGIN
            IF to_regclass('public.orders') IS NOT NULL THEN
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_orders_currency_len3') THEN
                    ALTER TABLE orders DROP CONSTRAINT ck_orders_currency_len3;
                END IF;
                IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_orders_total_nonneg') THEN
                    ALTER TABLE orders DROP CONSTRAINT ck_orders_total_nonneg;
                END IF;
                DROP INDEX IF EXISTS ix_orders_created_at;
                DROP INDEX IF EXISTS ix_orders_status;
                DROP INDEX IF EXISTS ix_orders_customer_id;
            END IF;
        END$$;
        """
    )


