from pydantic import ConfigDict
from pydantic import BaseModel, Field
class OrderItemBase(BaseModel):
    product_id: int
    qty: int = Field(ge=1)
    unit_price: float
class OrderItemCreate(OrderItemBase): pass
class OrderItemUpdate(BaseModel):
    qty: int | None = Field(default=None, ge=1)
    unit_price: float | None = None
class OrderItemOut(OrderItemBase):
    id: int
    subtotal: float
    class Config: from_attributes = True

model_config = ConfigDict(from_attributes=True)
