SHOOBYDO Dropship Monorepo

- docs/research: الملفات البحثية والتقارير (مرجع التنفيذ).
- assets: الأصول البصرية (شعارات، لقطات، موك‌آبس).
- data: جداول Excel ونماذج التحليل.
- apps/frontend: واجهة المستخدم (Next.js 14 + TS).
- apps/backend: واجهة برمجية (FastAPI).
- infra: حاويات التطوير (Docker Compose).

## التشغيل السريع

- تهيئة بيئة التطوير وتشغيل الخدمات:
  - `tools/dev_up.sh` يطبق سياسة عدم التعارض (اختيار منافذ متاحة)، يرفع Postgres/Redis، يشغّل الـ backend، ويولّد تقارير صحية.
- تشغيل الواجهة الأمامية:
  - `tools/start_frontend.sh` يستخدم `FRONTEND_PORT` من `.env.dev` ويبدأ Next.js.
- اختبارات الـ backend:
  - `tools/run_tests.sh` لتشغيل وحدات الاختبار (pytest).

## واجهة البرمجة (API)
- GET `/health`
- GET `/reports/summary`
- GET `/reports/kpis`
- GET `/reports/costs`
- GET `/db/ping`
- GET `/cache/ping`
- GET `/suppliers`
- GET `/suppliers/stats`
- POST `/suppliers/reindex`
- POST `/suppliers`
- GET `/suppliers/{id}`
- PUT `/suppliers/{id}`
- DELETE `/suppliers/{id}`
- POST `/suppliers/upload` (multipart/form-data: file .xlsx)

## واجهة المستخدم (Frontend)
- `/dashboard`
- `/suppliers`
- `/costs`
- `/analytics`

## ملاحظات تقنية
- قاعدة البيانات: PostgreSQL (Docker).
- الكاش/الصفوف السريعة: Redis (Docker).
- backend: Python FastAPI + Alembic للهجرات.
- frontend: Next.js (React 18)؛ تم تبسيط CSS بدون Tailwind.
 
### CRUD للموردين
- إضافة مورد عبر API: `POST /suppliers` مع JSON يحتوي `name`, `file_path`, `rows`, `sheets`.
- تعديل مورد: `PUT /suppliers/{id}` مع القيم المراد تحديثها.
- حذف مورد: `DELETE /suppliers/{id}`.
- من الواجهة: صفحة `/suppliers` توفر نموذج إضافة، تعديل سريع لكل صف، وحذف.

### رفع ملفات Excel
- صفحة `/upload` تسمح برفع ملف `.xlsx` وسيتم حفظه في `data/02_Excel/` وإعادة فهرسة الموردين تلقائيًا.


<!-- EPIC-02-TASK-02F:BEGIN -->
## Customers Core (EPIC-02/TASK-02F)
### Permissions
- GET /customers ⇒ user
- POST /customers ⇒ admin|manager
- PUT /customers/{id} ⇒ admin|manager
- DELETE /customers/{id} ⇒ admin

### OpenAPI
- `/customers/` → get, post
- `/customers/{cid}` → delete, put

<!-- EPIC-02-TASK-02F:END -->


<!-- EPIC-02-TASK-02G:BEGIN -->
## Products Core (EPIC-02/TASK-02G) — Verification
### OpenAPI
- `/products/` → get, post
- `/products/{pid}` → delete, put

### Artifacts
- reports/EPIC-02/TASK-02G/openapi_products_paths_after_merge.txt
- reports/EPIC-02/TASK-02G/health_after_merge.txt
- reports/EPIC-02/TASK-02G/curl_01_create.txt
- reports/EPIC-02/TASK-02G/curl_02_list.txt
- reports/EPIC-02/TASK-02G/curl_03_update.txt
- reports/EPIC-02/TASK-02G/curl_04_delete.txt
<!-- EPIC-02-TASK-02G:END -->


<!-- EPIC-02-TASK-02H:BEGIN -->
## Orders Core (EPIC-02/TASK-02H)
### Permissions
- GET /orders ⇒ user
- POST /orders ⇒ admin|manager
- PUT /orders/<built-in function id> ⇒ admin|manager
- DELETE /orders/<built-in function id> ⇒ admin
### OpenAPI
 - `/orders/` → get (filters: q,status,customer_id,limit,offset), post
 - `/orders/{oid}` → get, delete, put

### Artifacts
- reports/EPIC-02/TASK-02H/health_after_merge.txt
- reports/EPIC-02/TASK-02H/openapi_orders_paths_after_merge.txt
- reports/EPIC-02/TASK-02H/curl_01_create.txt
- reports/EPIC-02/TASK-02H/curl_02_list.txt
- reports/EPIC-02/TASK-02H/curl_03_update.txt
- reports/EPIC-02/TASK-02H/curl_04_delete.txt
<!-- EPIC-02-TASK-02H:END -->


<!-- EPIC-02-TASK-02I:BEGIN -->
## Order Items (EPIC-02/TASK-02I)
### OpenAPI
- `/orders/` → get, post
- `/orders/{oid}` → delete, get, put
- `/orders/{oid}/items` → get, post
- `/orders/{oid}/items/{iid}` → delete, put

### Artifacts
- reports/EPIC-02/TASK-02I/curl_01_create.txt
- reports/EPIC-02/TASK-02I/curl_02_list.txt
- reports/EPIC-02/TASK-02I/curl_03_update.txt
- reports/EPIC-02/TASK-02I/curl_04_delete.txt
<!-- EPIC-02-TASK-02I:END -->


<!-- EPIC-02-TASK-02J:BEGIN -->
## Order Totals & Constraints (EPIC-02/TASK-02J)
- CHECKs: quantity>0, unit_price>=0, total>=0
- Auto-recalc of orders.total on item changes
### OpenAPI (order-items)

<!-- EPIC-02-TASK-02J:END -->
