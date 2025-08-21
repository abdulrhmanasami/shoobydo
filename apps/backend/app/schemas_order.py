from pydantic import BaseModel, Field
class OrderBase(BaseModel):
    customer_email: str
    status: str = Field(default="new", max_length=32)
    total: float = 0
class OrderCreate(OrderBase): pass
class OrderUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=32)
    total: float | None = None
class OrderOut(OrderBase):
    id: int
    class Config: from_attributes = True
