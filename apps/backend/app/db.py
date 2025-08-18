from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session
import os

DB_USER = os.getenv("POSTGRES_USER","postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD","postgres")
DB_HOST = os.getenv("POSTGRES_HOST","127.0.0.1")
DB_PORT = os.getenv("POSTGRES_PORT","5432")
DB_NAME = os.getenv("POSTGRES_DB","eurodropship")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
