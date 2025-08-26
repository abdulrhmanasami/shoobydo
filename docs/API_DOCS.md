# 📚 Shoobydo API Documentation

## نظرة عامة

Shoobydo API هو RESTful API مبني على FastAPI يوفر واجهة برمجية شاملة لإدارة الموردين والمخزون والتقارير.

**Base URL:** `http://localhost:8811`  
**API Version:** `v1`  
**Authentication:** Bearer Token (JWT)

## 🔐 المصادقة

### تسجيل الدخول

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@test.com",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### تجديد التوكن

```http
POST /api/v1/auth/refresh
Authorization: Bearer {refresh_token}
```

### تسجيل الخروج

```http
POST /api/v1/auth/logout
Authorization: Bearer {access_token}
```

## 👥 إدارة الموردين

### قائمة الموردين

```http
GET /api/v1/suppliers
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `limit` (optional): عدد النتائج (default: 100)
- `offset` (optional): عدد النتائج للتخطي (default: 0)
- `search` (optional): البحث في اسم المورد

**Response:**
```json
[
  {
    "id": 1,
    "name": "مورد تجريبي",
    "email": "supplier@example.com",
    "phone": "+966501234567",
    "address": "الرياض، المملكة العربية السعودية",
    "created_at": "2025-08-26T10:00:00Z",
    "updated_at": "2025-08-26T10:00:00Z"
  }
]
```

### إضافة مورد جديد

```http
POST /api/v1/suppliers
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "مورد جديد",
  "email": "new@supplier.com",
  "phone": "+966501234567",
  "address": "جدة، المملكة العربية السعودية"
}
```

**Required Fields:** `name`, `email`  
**Optional Fields:** `phone`, `address`

### تحديث مورد

```http
PUT /api/v1/suppliers/{id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "اسم محدث",
  "phone": "+966501234568"
}
```

### حذف مورد

```http
DELETE /api/v1/suppliers/{id}
Authorization: Bearer {access_token}
```

## 📊 التقارير

### ملخص عام

```http
GET /api/v1/reports/summary
Authorization: Bearer {access_token}
```

**Required Role:** `admin`, `viewer`

**Response:**
```json
{
  "suppliers": {
    "total": 25,
    "active": 23,
    "inactive": 2
  },
  "kpis": {
    "total_orders": 150,
    "total_revenue": 50000.00,
    "avg_order_value": 333.33
  },
  "notes": [
    "زيادة في الطلبات بنسبة 15%",
    "أفضل مورد: شركة ABC"
  ]
}
```

### مؤشرات الأداء

```http
GET /api/v1/reports/kpis
Authorization: Bearer {access_token}
```

**Required Role:** `admin`, `viewer`

**Query Parameters:**
- `period` (optional): الفترة الزمنية (`daily`, `weekly`, `monthly`, `yearly`)
- `start_date` (optional): تاريخ البداية (YYYY-MM-DD)
- `end_date` (optional): تاريخ النهاية (YYYY-MM-DD)

**Response:**
```json
{
  "period": "monthly",
  "start_date": "2025-08-01",
  "end_date": "2025-08-31",
  "metrics": {
    "total_orders": 150,
    "total_revenue": 50000.00,
    "avg_order_value": 333.33,
    "customer_satisfaction": 4.5,
    "order_fulfillment_rate": 0.95
  },
  "trends": {
    "orders_growth": 0.15,
    "revenue_growth": 0.22
  }
}
```

### تحليل التكاليف

```http
GET /api/v1/reports/costs
Authorization: Bearer {access_token}
```

**Required Role:** `admin`, `viewer`

**Response:**
```json
{
  "total_costs": 35000.00,
  "cost_breakdown": {
    "product_costs": 25000.00,
    "shipping_costs": 5000.00,
    "operational_costs": 5000.00
  },
  "profit_margin": 0.30,
  "cost_per_order": 233.33
}
```

### تحديث التقارير

```http
POST /api/v1/reports/refresh
Authorization: Bearer {access_token}
```

**Required Role:** `admin` فقط

**Response:**
```json
{
  "message": "Reports cache cleared",
  "refreshed": true,
  "timestamp": "2025-08-26T10:00:00Z"
}
```

## 🏥 الصحة والمراقبة

### فحص الصحة العام

```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-08-26T10:00:00Z"
}
```

### فحص صحة API

```http
GET /api/health
```

**Response:**
```json
{
  "status": "ok",
  "api_version": "v1",
  "timestamp": "2025-08-26T10:00:00Z"
}
```

## 🔒 نظام الصلاحيات

### مستويات الصلاحيات

| الدور | الوصول | الوصف |
|-------|---------|--------|
| **admin** | كامل | صلاحيات كاملة على النظام |
| **manager** | محدود | إدارة الموردين والتقارير |
| **viewer** | قراءة فقط | عرض التقارير والبيانات |

### Endpoints حسب الصلاحيات

#### Admin Only
- `POST /api/v1/reports/refresh`
- `DELETE /api/v1/suppliers/{id}`

#### Admin + Manager
- `POST /api/v1/suppliers`
- `PUT /api/v1/suppliers/{id}`

#### Admin + Manager + Viewer
- `GET /api/v1/suppliers`
- `GET /api/v1/reports/summary`
- `GET /api/v1/reports/kpis`
- `GET /api/v1/reports/costs`

## 📝 رموز الحالة HTTP

| الكود | المعنى | الوصف |
|-------|---------|--------|
| `200` | OK | الطلب نجح |
| `201` | Created | تم إنشاء المورد بنجاح |
| `400` | Bad Request | بيانات الطلب غير صحيحة |
| `401` | Unauthorized | توكن غير صالح أو مفقود |
| `403` | Forbidden | لا توجد صلاحية للوصول |
| `404` | Not Found | المورد غير موجود |
| `422` | Validation Error | خطأ في التحقق من البيانات |
| `500` | Internal Server Error | خطأ في الخادم |

## 🚨 رسائل الخطأ

### خطأ في المصادقة

```json
{
  "detail": "Invalid credentials",
  "status_code": 401
}
```

### خطأ في الصلاحيات

```json
{
  "detail": "Forbidden",
  "status_code": 403
}
```

### خطأ في التحقق من البيانات

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 🔧 أمثلة على الاستخدام

### Python (requests)

```python
import requests

# تسجيل الدخول
response = requests.post(
    "http://localhost:8811/api/v1/auth/login",
    json={"email": "admin@test.com", "password": "admin123"}
)
token = response.json()["access_token"]

# الحصول على قائمة الموردين
headers = {"Authorization": f"Bearer {token}"}
suppliers = requests.get(
    "http://localhost:8811/api/v1/suppliers",
    headers=headers
)
print(suppliers.json())
```

### JavaScript (fetch)

```javascript
// تسجيل الدخول
const loginResponse = await fetch('http://localhost:8811/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'admin@test.com',
    password: 'admin123'
  })
});

const { access_token } = await loginResponse.json();

// الحصول على التقارير
const reportsResponse = await fetch('http://localhost:8811/api/v1/reports/summary', {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});

const reports = await reportsResponse.json();
console.log(reports);
```

### cURL

```bash
# تسجيل الدخول
TOKEN=$(curl -s -X POST "http://localhost:8811/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"admin123"}' | \
  jq -r '.access_token')

# الحصول على التقارير
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8811/api/v1/reports/summary"
```

## 📊 Rate Limiting

حالياً لا يوجد rate limiting على API، لكن يُنصح بعدم تجاوز:
- **100 requests/minute** لكل مستخدم
- **1000 requests/hour** لكل مستخدم

## 🔄 Webhooks

حالياً لا يدعم API webhooks، لكن يمكن إضافتها في الإصدارات المستقبلية.

## 📚 OpenAPI Schema

يمكن الوصول إلى OpenAPI schema التفصيلي عبر:
```
http://localhost:8811/docs
```

## 🆘 الدعم

### الإبلاغ عن الأخطاء

عند مواجهة مشاكل في API:
1. تحقق من رموز الحالة HTTP
2. راجع رسائل الخطأ في response body
3. تأكد من صحة التوكن وصلاحيات المستخدم
4. ارفق تفاصيل الطلب مع report الخطأ

### التواصل

- **GitHub Issues**: للمشاكل التقنية
- **GitHub Discussions**: للأسئلة العامة

---

**آخر تحديث:** 2025-08-26  
**الإصدار:** v0.3.0  
**المطور:** Shoobydo Team
