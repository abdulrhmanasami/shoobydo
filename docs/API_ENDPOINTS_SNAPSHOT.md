# 🔌 **API ENDPOINTS SNAPSHOT - Shoobydo Platform**

## 📊 **نقاط النهاية الشاملة - بناءً على الكود الفعلي**

### 🌐 **نقاط النهاية العامة (Public)**

| Method | Path | Description | Authentication |
|--------|------|-------------|----------------|
| `GET` | `/health` | حالة الخادم العامة | ❌ |
| `GET` | `/api/health` | حالة API (مخفية من Schema) | ❌ |
| `GET` | `/metrics` | مقاييس Prometheus | ❌ |

### 🔐 **المصادقة والتفويض (Authentication & Authorization)**

| Method | Path | Description | Authentication | Role Required |
|--------|------|-------------|----------------|---------------|
| `POST` | `/api/v1/register` | تسجيل مستخدم جديد | ❌ | First user only |
| `POST` | `/api/v1/login` | تسجيل الدخول | ❌ | - |
| `POST` | `/api/v1/refresh` | تجديد access token | ❌ | Valid refresh token |
| `POST` | `/api/v1/logout` | تسجيل الخروج | ❌ | Valid token |
| `GET` | `/api/v1/me` | معلومات المستخدم الحالي | ✅ | Any authenticated |
| `POST` | `/api/v1/change-password` | تغيير كلمة المرور | ✅ | Any authenticated |

### 👥 **إدارة المستخدمين (Users Management)**

| Method | Path | Description | Authentication | Role Required |
|--------|------|-------------|----------------|---------------|
| `GET` | `/api/v1/users/` | قائمة المستخدمين | ✅ | admin |
| `POST` | `/api/v1/users/` | إنشاء مستخدم جديد | ✅ | admin |
| `GET` | `/api/v1/users/{id}` | تفاصيل مستخدم | ✅ | admin |
| `PUT` | `/api/v1/users/{id}` | تحديث مستخدم | ✅ | admin |
| `DELETE` | `/api/v1/users/{id}` | حذف مستخدم | ✅ | admin |

### 🏢 **إدارة الموردين (Suppliers Management)**

| Method | Path | Description | Authentication | Role Required |
|--------|------|-------------|----------------|---------------|
| `GET` | `/api/v1/suppliers/` | قائمة الموردين | ✅ | Any authenticated |
| `GET` | `/api/v1/suppliers` | قائمة الموردين (بدون slash) | ✅ | Any authenticated |
| `GET` | `/api/v1/suppliers/stats` | إحصائيات الموردين | ✅ | Any authenticated |
| `POST` | `/api/v1/suppliers/` | إنشاء مورد جديد | ✅ | admin |
| `POST` | `/api/v1/suppliers/reindex` | إعادة فهرسة الموردين | ✅ | admin |
| `POST` | `/api/v1/suppliers/upload` | رفع ملف Excel | ✅ | admin |
| `GET` | `/api/v1/suppliers/{supplier_id}` | تفاصيل مورد | ✅ | Any authenticated |
| `PUT` | `/api/v1/suppliers/{supplier_id}` | تحديث مورد | ✅ | admin |
| `DELETE` | `/api/v1/suppliers/{supplier_id}` | حذف مورد | ✅ | admin |

### 📦 **إدارة المنتجات (Products Management)**

| Method | Path | Description | Authentication | Role Required |
|--------|------|-------------|----------------|---------------|
| `GET` | `/api/v1/products/` | قائمة المنتجات | ✅ | Any authenticated |
| `POST` | `/api/v1/products/` | إنشاء منتج جديد | ✅ | admin |
| `GET` | `/api/v1/products/{pid}` | تفاصيل منتج | ✅ | Any authenticated |
| `PUT` | `/api/v1/products/{pid}` | تحديث منتج | ✅ | admin |
| `DELETE` | `/api/v1/products/{pid}` | حذف منتج | ✅ | admin |

### 👤 **إدارة العملاء (Customers Management)**

| Method | Path | Description | Authentication | Role Required |
|--------|------|-------------|----------------|---------------|
| `GET` | `/api/v1/customers/` | قائمة العملاء | ✅ | Any authenticated |
| `POST` | `/api/v1/customers/` | إنشاء عميل جديد | ✅ | admin/manager |
| `GET` | `/api/v1/customers/{cid}` | تفاصيل عميل | ✅ | Any authenticated |
| `PUT` | `/api/v1/customers/{cid}` | تحديث عميل | ✅ | admin/manager |
| `DELETE` | `/api/v1/customers/{cid}` | حذف عميل | ✅ | admin |

### 📋 **إدارة الطلبات (Orders Management)**

| Method | Path | Description | Authentication | Role Required |
|--------|------|-------------|----------------|---------------|
| `GET` | `/api/v1/orders/` | قائمة الطلبات | ✅ | Any authenticated |
| `POST` | `/api/v1/orders/` | إنشاء طلب جديد | ✅ | admin/manager |
| `GET` | `/api/v1/orders/{oid}` | تفاصيل طلب | ✅ | Any authenticated |
| `PUT` | `/api/v1/orders/{oid}` | تحديث طلب | ✅ | admin/manager |
| `DELETE` | `/api/v1/orders/{oid}` | حذف طلب | ✅ | admin |
| `GET` | `/api/v1/orders/stats/summary` | ملخص إحصائيات الطلبات | ✅ | Any authenticated |
| `GET` | `/api/v1/orders/stats/daily` | إحصائيات يومية | ✅ | Any authenticated |
| `GET` | `/api/v1/orders/customer/{customer_id}/orders` | طلبات عميل محدد | ✅ | Any authenticated |
| `POST` | `/api/v1/orders/{oid}/status` | تحديث حالة طلب | ✅ | admin/manager |

### 🛍️ **إدارة عناصر الطلبات (Order Items Management)**

| Method | Path | Description | Authentication | Role Required |
|--------|------|-------------|----------------|---------------|
| `GET` | `/api/v1/orders/{oid}/items` | عناصر طلب | ✅ | Any authenticated |
| `POST` | `/api/v1/orders/{oid}/items` | إضافة عنصر طلب | ✅ | admin/manager |
| `GET` | `/api/v1/orders/{oid}/items/{iid}` | تفاصيل عنصر طلب | ✅ | Any authenticated |
| `PUT` | `/api/v1/orders/{oid}/items/{iid}` | تحديث عنصر طلب | ✅ | admin/manager |
| `DELETE` | `/api/v1/orders/{oid}/items/{iid}` | حذف عنصر طلب | ✅ | admin |
| `GET` | `/api/v1/orders/{oid}/items-summary` | ملخص عناصر طلب | ✅ | Any authenticated |

### 📊 **إدارة المخزون (Inventory Management)**

| Method | Path | Description | Authentication | Role Required |
|--------|------|-------------|----------------|---------------|
| `GET` | `/api/v1/inventory/products/{product_id}/stock` | حالة المخزون | ✅ | Any authenticated |
| `POST` | `/api/v1/inventory/products/{product_id}/adjust` | تعديل المخزون | ✅ | admin |
| `POST` | `/api/v1/inventory/products/{product_id}/reserve` | حجز مخزون | ✅ | Any authenticated |
| `POST` | `/api/v1/inventory/products/{product_id}/release` | إطلاق مخزون محجوز | ✅ | Any authenticated |

### 📈 **التقارير والتحليلات (Reports & Analytics)**

| Method | Path | Description | Authentication | Role Required |
|--------|------|-------------|----------------|---------------|
| `GET` | `/api/v1/reports/kpis` | مؤشرات الأداء الرئيسية | ✅ | Any authenticated |
| `GET` | `/api/v1/reports/summary` | ملخص عام | ✅ | Any authenticated |
| `GET` | `/api/v1/reports/costs` | تحليل التكاليف | ✅ | Any authenticated |
| `POST` | `/api/v1/reports/refresh` | تحديث التقارير | ✅ | Any authenticated |

### 🏥 **فحوصات الصحة (Health Checks)**

| Method | Path | Description | Authentication |
|--------|------|-------------|----------------|
| `GET` | `/api/v1/health` | فحص صحة API | ❌ |

### 🔧 **التشخيص (Diagnostics - Dev Only)**

| Method | Path | Description | Authentication | Environment |
|--------|------|-------------|----------------|-------------|
| `GET` | `/api/v1/_diag` | معلومات تشخيصية | ❌ | Development |

## 📊 **إحصائيات API**

- **إجمالي نقاط النهاية**: **45+ endpoint**
- **نقاط النهاية العامة**: 3
- **نقاط النهاية المحمية**: 42+
- **نقاط النهاية للإدارة**: 15+
- **نقاط النهاية للقراءة**: 20+
- **نقاط النهاية للكتابة**: 15+

## 🔐 **نظام الصلاحيات (RBAC)**

### **Admin (مدير)**
- صلاحيات كاملة على جميع العمليات
- إنشاء/تحديث/حذف جميع الكيانات
- إدارة المستخدمين والصلاحيات
- إعادة فهرسة البيانات

### **Manager (مشرف)**
- صلاحيات على القراءة والإنشاء والتحديث
- لا يمكن حذف الكيانات
- إدارة الطلبات والعملاء

### **Viewer (مشاهد)**
- صلاحيات قراءة فقط
- عرض البيانات والتقارير
- لا يمكن تعديل أي شيء

## 🚀 **الميزات المتقدمة**

- **JWT Authentication**: نظام مصادقة متقدم
- **Role-Based Access Control**: نظام صلاحيات متقدم
- **Redis Caching**: كاش للتقارير والأداء
- **File Upload**: رفع ملفات Excel
- **Real-time Updates**: تحديثات فورية
- **Comprehensive Logging**: تسجيل شامل
- **Health Monitoring**: مراقبة الصحة
- **Performance Metrics**: مقاييس الأداء

---

**آخر تحديث**: 2025-08-28
**حالة API**: ✅ مكتمل 100% - 45+ endpoint
**الأمان**: JWT + RBAC + CORS
**الأداء**: Redis caching + Database indexing
