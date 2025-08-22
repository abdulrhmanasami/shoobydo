# Inventory System - Curl Tests (EPIC-02/TASK-02K)

## 🧪 اختبارات المخزون والحجز (D-rule compliant)

### 1. إنشاء منتج مع مخزون
```bash
# إنشاء منتج
scurl -X POST "http://127.0.0.1:8805/products" \
  -H "Authorization: Bearer $ADM" \
  -H 'Content-Type: application/json' \
  -d '{
    "sku": "INV001",
    "name": "Inventory Test Product",
    "price": 25.99,
    "currency": "EUR",
    "stock": 100
  }'
```

### 2. تعديل المخزون (admin/manager)
```bash
# تعديل المخزون إلى 50
scurl -X POST "http://127.0.0.1:8805/inventory/products/1/adjust" \
  -H "Authorization: Bearer $ADM" \
  -H 'Content-Type: application/json' \
  -d '{
    "adjustment": -50,
    "reason": "manual_adjust",
    "notes": "Reducing stock for testing"
  }'
```

### 3. إنشاء طلب وعنصر (حجز المخزون)
```bash
# إنشاء طلب
scurl -X POST "http://127.0.0.1:8805/orders" \
  -H "Authorization: Bearer $ADM" \
  -H 'Content-Type: application/json' \
  -d '{
    "customer_id": 1,
    "status": "pending",
    "currency": "EUR",
    "total": 0
  }'

# إضافة عنصر (يجب أن يحجز 30 وحدة)
scurl -X POST "http://127.0.0.1:8805/orders/1/items" \
  -H "Authorization: Bearer $ADM" \
  -H 'Content-Type: application/json' \
  -d '{
    "product_id": 1,
    "quantity": 30,
    "unit_price": 25.99
  }'
```

### 4. التحقق من حالة المخزون
```bash
# عرض حالة المخزون
scurl "http://127.0.0.1:8805/inventory/products/1/stock" \
  -H "Authorization: Bearer $ADM"
```

### 5. اختبار oversell (يجب أن يفشل)
```bash
# محاولة إضافة عنصر يتجاوز المخزون المتاح
scurl -i -X PUT "http://127.0.0.1:8805/orders/1/items/1" \
  -H "Authorization: Bearer $ADM" \
  -H 'Content-Type: application/json' \
  -d '{"quantity":12}' \
  || true  # نتوقع 409 Conflict
```

### 6. تحديث العنصر (تعديل الحجز)
```bash
# تحديث الكمية من 30 إلى 40
scurl -X PUT "http://127.0.0.1:8805/orders/1/items/1" \
  -H "Authorization: Bearer $ADM" \
  -H 'Content-Type: application/json' \
  -d '{
    "quantity": 40
  }'
```

### 7. حذف العنصر (إفراج المخزون)
```bash
# حذف العنصر
scurl -X DELETE "http://127.0.0.1:8805/orders/1/items/1" \
  -H "Authorization: Bearer $ADM"
```

## 📊 النتائج المتوقعة

- **قبل الحجز**: stock_on_hand=50, stock_reserved=0, available=50
- **بعد الحجز (30)**: stock_on_hand=50, stock_reserved=30, available=20
- **بعد التحديث (40)**: stock_on_hand=50, stock_reserved=40, available=10
- **بعد الحذف**: stock_on_hand=50, stock_reserved=0, available=50

## 🚫 اختبارات الفشل

- **oversell**: يجب أن يعطي 409 Conflict
- **تعديل مخزون سالب**: يجب أن يعطي 409 Conflict
- **حجز كمية سالبة**: يجب أن يعطي 400 Bad Request

## 🔧 ملاحظات D-rule

- **scurl**: `--max-time 5 --connect-timeout 2 -f -L`
- **oversell tests**: استخدم `|| true` بعد `scurl` عند التوقع بفشل منطقي
- **nohup+PID+LOG**: الخادم يعمل وفق القاعدة
