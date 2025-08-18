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


class CostsSummary(BaseModel):
    files: int
    rows: int
    total_cost: float
    total_margin: float
    notes: Optional[str] = None


class SupplierIn(BaseModel):
    name: str
    file_path: str
    rows: int = 0
    sheets: int = 0

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    file_path: Optional[str] = None
    rows: Optional[int] = None
    sheets: Optional[int] = None

