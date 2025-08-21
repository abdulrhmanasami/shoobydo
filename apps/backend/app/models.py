from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app.db import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    rows: Mapped[int] = mapped_column(Integer, default=0)
    sheets: Mapped[int] = mapped_column(Integer, default=0)


import app.models_product  # ensure Product model is imported
import app.models_customer  # ensure Customer model is imported
import app.models_order  # ensure Order model is imported
import app.models_order_item  # ensure OrderItem model is imported
