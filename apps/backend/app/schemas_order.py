from pydantic import BaseModel, condecimal, field_validator
from typing import Optional
from typing import Literal
class OrderBase(BaseModel):
    customer_id: int
    status: Literal["pending","paid","cancelled","refunded"] = "pending"
    currency: str = "EUR"
    total: condecimal(max_digits=12, decimal_places=2) = 0
    notes: Optional[str] = None
    @field_validator("currency")
    @classmethod
    def _cur(cls, v: str) -> str:
        v = (v or "").upper()
        if len(v) != 3:
            raise ValueError("currency must be 3-letter code")
        return v
class OrderCreate(OrderBase): pass
class OrderUpdate(BaseModel):
    customer_id: int | None = None
    status: str | None = None
    currency: str | None = None
    total: condecimal(max_digits=12, decimal_places=2) | None = None
    notes: str | None = None
class OrderOut(OrderBase):
    id: int
    class Config: from_attributes = True

model_config = ConfigDict(from_attributes=True)
