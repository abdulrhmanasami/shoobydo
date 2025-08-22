from pydantic import BaseModel, Field
from typing import Literal

class ProductBase(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    name: str
    supplier_id: int | None = None
    price: float = 0
    currency: Literal["EUR", "USD", "GBP"] = "EUR"
    stock: int = 0
    # New inventory fields
    stock_on_hand: int = 0
    stock_reserved: int = 0
class ProductCreate(ProductBase): pass
class ProductUpdate(BaseModel):
    name: str | None = None
    supplier_id: int | None = None
    price: float | None = None
    currency: Literal["EUR", "USD", "GBP"] | None = None
    stock: int | None = None
    stock_on_hand: int | None = None
    stock_reserved: int | None = None
class ProductOut(ProductBase):
    id: int
    class Config: from_attributes = True
