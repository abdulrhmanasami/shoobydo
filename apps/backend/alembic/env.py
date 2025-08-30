import os
from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from alembic import context

# --- Alembic config ---
config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

# Build DATABASE_URL from env if not set in alembic.ini
DATABASE_URL = os.getenv("DATABASE_URL") or (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER','postgres')}:"
    f"{os.getenv('POSTGRES_PASSWORD','postgres')}@"
    f"{os.getenv('POSTGRES_HOST','db')}:{os.getenv('POSTGRES_PORT','5432')}/"
    f"{os.getenv('POSTGRES_DB','shoobydo')}"
)

if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Target metadata (make sure Base aggregates all models)
from app.db.base import Base  # noqa: E402

try:
    import app.models  # noqa: F401 # force-load models for autogenerate
except Exception:
    pass

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(
        config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
