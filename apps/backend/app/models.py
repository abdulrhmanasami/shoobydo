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


# Import all models to ensure they are registered with SQLAlchemy
from app.models_user import User, UserRole
from app.models_product import Product
from app.models_customer import Customer
from app.models_order import Order
from app.models_order_item import OrderItem
from app.models_stock_movement import StockMovement
