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

### نقاط النهاية العامة
- GET `/health` - حالة الخادم
- GET `/api/health` - حالة API

### المصادقة والتفويض (Auth)
- POST `/api/v1/auth/register` - تسجيل مستخدم جديد (مقيد للمستخدم الأول فقط)
- POST `/api/v1/auth/login` - تسجيل الدخول وإرجاع JWT tokens
- POST `/api/v1/auth/refresh` - تجديد access token
- POST `/api/v1/auth/logout` - تسجيل الخروج
- GET `/api/v1/auth/me` - معلومات المستخدم الحالي
- POST `/api/v1/auth/change-password` - تغيير كلمة المرور

### الموردين (Suppliers) - محمي بـ JWT
- GET `/api/v1/suppliers/` - قائمة الموردين
- GET `/api/v1/suppliers/stats` - إحصائيات الموردين
- POST `/api/v1/suppliers/reindex` - إعادة فهرسة (admin فقط)
- POST `/api/v1/suppliers/` - إنشاء مورد جديد (admin فقط)
- POST `/api/v1/suppliers/upload` - رفع ملف Excel (admin فقط)
- GET `/api/v1/suppliers/{id}` - تفاصيل مورد
- PUT `/api/v1/suppliers/{id}` - تحديث مورد (admin فقط)
- DELETE `/api/v1/suppliers/{id}` - حذف مورد (admin فقط)

### المنتجات (Products) - محمي بـ JWT
- GET `/api/v1/products/` - قائمة المنتجات
- POST `/api/v1/products/` - إنشاء منتج جديد (admin فقط)
- GET `/api/v1/products/{pid}` - تفاصيل منتج
- PUT `/api/v1/products/{pid}` - تحديث منتج (admin فقط)
- DELETE `/api/v1/products/{pid}` - حذف منتج (admin فقط)

### العملاء (Customers) - محمي بـ JWT
- GET `/api/v1/customers/` - قائمة العملاء
- POST `/api/v1/customers/` - إنشاء عميل جديد (admin/manager فقط)
- GET `/api/v1/customers/{cid}` - تفاصيل عميل
- PUT `/api/v1/customers/{cid}` - تحديث عميل (admin/manager فقط)
- DELETE `/api/v1/customers/{cid}` - حذف عميل (admin فقط)

### الطلبات (Orders) - محمي بـ JWT
- GET `/api/v1/orders/` - قائمة الطلبات
- POST `/api/v1/orders/` - إنشاء طلب جديد (admin/manager فقط)
- GET `/api/v1/orders/{oid}` - تفاصيل طلب
- PUT `/api/v1/orders/{oid}` - تحديث طلب (admin/manager فقط)
- DELETE `/api/v1/orders/{oid}` - حذف طلب (admin فقط)
- GET `/api/v1/orders/stats/summary` - ملخص إحصائيات الطلبات
- GET `/api/v1/orders/stats/daily` - إحصائيات يومية

### عناصر الطلبات (Order Items) - محمي بـ JWT
- GET `/api/v1/order_items/orders/{oid}/items` - عناصر طلب
- POST `/api/v1/order_items/orders/{oid}/items` - إضافة عنصر (admin/manager فقط)
- GET `/api/v1/order_items/orders/{oid}/items/{iid}` - تفاصيل عنصر
- PUT `/api/v1/order_items/orders/{oid}/items/{iid}` - تحديث عنصر (admin/manager فقط)
- DELETE `/api/v1/order_items/orders/{oid}/items/{iid}` - حذف عنصر (admin فقط)

### المخزون (Inventory) - محمي بـ JWT
- GET `/api/v1/inventory/products/{product_id}/stock` - حالة المخزون
- POST `/api/v1/inventory/products/{product_id}/adjust` - تعديل المخزون (admin فقط)
- POST `/api/v1/inventory/products/{product_id}/reserve` - حجز مخزون
- POST `/api/v1/inventory/products/{product_id}/release` - إطلاق مخزون محجوز

### التقارير (Reports) - محمي بـ JWT
- GET `/api/v1/reports/kpis` - مؤشرات الأداء الرئيسية
- GET `/api/v1/reports/summary` - ملخص عام
- GET `/api/v1/reports/costs` - تحليل التكاليف
- POST `/api/v1/reports/refresh` - تحديث التقارير

### نقاط النهاية القديمة (Legacy)
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

## نظام الأمان والصلاحيات

### المصادقة (Authentication)
- JWT tokens مع access و refresh tokens
- Access token صالح لمدة 30 دقيقة
- Refresh token صالح لمدة 7 أيام

### التفويض (Authorization) - RBAC
- **admin**: صلاحيات كاملة على جميع العمليات
- **manager**: صلاحيات على القراءة والإنشاء والتحديث (لا حذف)
- **viewer**: صلاحيات قراءة فقط

### الحماية
- جميع نقاط النهاية (إلا المصادقة) تتطلب JWT token صالح
- عمليات التعديل والحذف تتطلب صلاحيات admin/manager
- عمليات القراءة متاحة للمستخدمين المصادق عليهم

## ملاحظات تقنية
- قاعدة البيانات: PostgreSQL (Docker).
- الكاش/الصفوف السريعة: Redis (Docker).
- backend: Python FastAPI + Alembic للهجرات.
- frontend: Next.js (React 18)؛ تم تبسيط CSS بدون Tailwind.
- المصادقة: JWT + bcrypt لكلمات المرور
- الحماية: CORS مفعل، RBAC مطبق
 
### CRUD للموردين
- إضافة مورد عبر API: `POST /api/v1/suppliers/` مع JSON يحتوي `name`, `file_path`, `rows`, `sheets`.
- تعديل مورد: `PUT /api/v1/suppliers/{id}` مع القيم المراد تحديثها.
- حذف مورد: `DELETE /api/v1/suppliers/{id}`.
- من الواجهة: صفحة `/suppliers` توفر نموذج إضافة، تعديل سريع لكل صف، وحذف.

### رفع ملفات Excel
- صفحة `/upload` تسمح برفع ملف `.xlsx` وسيتم حفظه في `data/02_Excel/` وإعادة فهرسة الموردين تلقائيًا.

## التشغيل المحلي

### Backend
```bash
cd apps/backend
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8807 --reload
```

### Frontend
```bash
cd apps/frontend
npm run dev
```

### اختبارات
```bash
cd apps/backend
python -m pytest tests/ -v
```

## المتغيرات البيئية المطلوبة
```bash
# Backend (.env.isolated)
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=30
JWT_REFRESH_EXPIRES_MINUTES=10080

# Database
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5546
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=eurodropship

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6389
```

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
- reports/EPIC-02-TASK-02H/health_after_merge.txt

## Auth Endpoints

- POST `/api/v1/login` (canonical)
- GET  `/api/v1/me`
- POST `/api/v1/logout`

Aliases (hidden): `/api/v1/auth/*`.

Tokens: HS256, `sub` (string user id), `exp`, `iat`, `nbf`.

