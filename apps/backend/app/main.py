from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="EuroDropship API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

class ReportSummary(BaseModel):
    suppliers: int
    kpis: int
    notes: str

@app.get("/reports/summary", response_model=ReportSummary)
def reports_summary():
    import os
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
    suppliers = 0
    if os.path.isdir(data_dir):
        for root, _, files in os.walk(data_dir):
            suppliers += sum(1 for f in files if f.lower().endswith(".xlsx"))
    return ReportSummary(suppliers=suppliers, kpis=2, notes="based on Excel models")
