from pydantic import BaseModel, EmailStr
class CustomerBase(BaseModel):
    email: EmailStr
    name: str | None = None
    phone: str | None = None
    address: str | None = None
class CustomerCreate(CustomerBase): pass
class CustomerUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    phone: str | None = None
    address: str | None = None
class CustomerOut(CustomerBase):
    id: int
    class Config: from_attributes = True
