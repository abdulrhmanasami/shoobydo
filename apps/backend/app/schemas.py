from pydantic import BaseModel
from typing import Optional


class SupplierOut(BaseModel):
    id: int
    name: str
    file_path: str
    rows: int
    sheets: int

    class Config:
        orm_mode = True


class SupplierStats(BaseModel):
    total: int
    files: int
    rows: int
    sheets: int
    notes: Optional[str] = None


