# User Manual

## Getting Started
- Open the web UI (local dev): http://127.0.0.1:$FRONTEND_PORT/
- Navigation: Dashboard, Suppliers, Products, Costs, Analytics, Brand, Upload

## Suppliers Management
- View list: `/suppliers`
- Reindex from Excel: click “Reindex Suppliers” (POST `/suppliers/reindex`)
- Create supplier: fill form (name, file_path, rows, sheets) and submit (POST `/suppliers`)
- Edit supplier: click “Edit”, update fields, submit (PUT `/suppliers/{id}`)
- Delete supplier: click “Delete” and confirm (DELETE `/suppliers/{id}`)
- Upload Excel: `/upload` then choose `.xlsx` file (POST `/suppliers/upload`), data auto‑reindexed

## Reports & Analytics
- KPIs: `/analytics` combines `/suppliers/stats`, `/reports/kpis`, `/reports/costs`
- Costs summary: `/costs` shows totals and chart for cost/margin
- Health: backend `/health`, summaries under `reports/`

## Reading the Final Report & Docs
- Final report: `docs/final_report.md`
- Legal policies: `docs/legal/`
- Brand identity: `/brand` page and `docs/brand_identity.md`

## Training Plan (Suggested)
- Session 1 (60m): Overview & navigation; suppliers CRUD; upload workflow
- Session 2 (60m): Analytics & KPIs; interpreting charts; cost summary
- Session 3 (45m): Compliance & security basics; backups & recovery runbook
- Materials: this manual, `docs/execution_guide.md`, `docs/final_report.md`, `docs/security_plan.md`
