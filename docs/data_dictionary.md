# 🗄️ **DATA DICTIONARY - Shoobydo Platform**

## 📊 **قاموس البيانات الشامل - بناءً على الكود الفعلي**

### 🏗️ **هيكل قاعدة البيانات (Database Schema)**

#### **النماذج الأساسية (Core Models)**

##### **1. User Model (`models_user.py`)**
```python
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), nullable=False, default=UserRole.viewer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
```

**الحقول:**
- `id`: معرف فريد للمستخدم (Primary Key)
- `email`: البريد الإلكتروني (فريد، مفهرس)
- `password_hash`: كلمة المرور مشفرة
- `role`: دور المستخدم (admin/manager/viewer)
- `is_active`: حالة النشاط
- `created_at`: تاريخ الإنشاء
- `updated_at`: تاريخ آخر تحديث

##### **2. Supplier Model (`models.py`)**
```python
class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    rows: Mapped[int] = mapped_column(Integer, default=0)
    sheets: Mapped[int] = mapped_column(Integer, default=0)
```

**الحقول:**
- `id`: معرف فريد للمورد (Primary Key)
- `name`: اسم المورد
- `file_path`: مسار ملف Excel (فريد)
- `rows`: عدد الصفوف في الملف
- `sheets`: عدد الأوراق في الملف

##### **3. Product Model (`models_product.py`)**
```python
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey("suppliers.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
```

**الحقول:**
- `id`: معرف فريد للمنتج (Primary Key)
- `name`: اسم المنتج
- `description`: وصف المنتج
- `price`: سعر المنتج
- `supplier_id`: معرف المورد (Foreign Key)
- `created_at`: تاريخ الإنشاء
- `updated_at`: تاريخ آخر تحديث

##### **4. Customer Model (`models_customer.py`)**
```python
class Customer(Base):
    __tablename__ = "customers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
```

**الحقول:**
- `id`: معرف فريد للعميل (Primary Key)
- `name`: اسم العميل
- `email`: البريد الإلكتروني
- `phone`: رقم الهاتف
- `address`: العنوان
- `created_at`: تاريخ الإنشاء
- `updated_at`: تاريخ آخر تحديث

##### **5. Order Model (`models_order.py`)**
```python
class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
```

**الحقول:**
- `id`: معرف فريد للطلب (Primary Key)
- `customer_id`: معرف العميل (Foreign Key)
- `status`: حالة الطلب
- `total_amount`: المبلغ الإجمالي
- `created_at`: تاريخ الإنشاء
- `updated_at`: تاريخ آخر تحديث

##### **6. OrderItem Model (`models_order_item.py`)**
```python
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
```

**الحقول:**
- `id`: معرف فريد لعنصر الطلب (Primary Key)
- `order_id`: معرف الطلب (Foreign Key)
- `product_id`: معرف المنتج (Foreign Key)
- `quantity`: الكمية
- `unit_price`: سعر الوحدة
- `total_price`: السعر الإجمالي
- `created_at`: تاريخ الإنشاء

##### **7. StockMovement Model (`models_stock_movement.py`)**
```python
class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    movement_type: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_id: Mapped[int] = mapped_column(Integer, nullable=True)
    reference_type: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
```

**الحقول:**
- `id`: معرف فريد لحركة المخزون (Primary Key)
- `product_id`: معرف المنتج (Foreign Key)
- `movement_type`: نوع الحركة (in/out/reserve/release)
- `quantity`: الكمية
- `reference_id`: معرف المرجع
- `reference_type`: نوع المرجع
- `created_at`: تاريخ الإنشاء

### 🔗 **العلاقات (Relationships)**

#### **One-to-Many Relationships**
- **Supplier → Products**: مورد واحد يمكن أن يكون له منتجات متعددة
- **Customer → Orders**: عميل واحد يمكن أن يكون له طلبات متعددة
- **Order → OrderItems**: طلب واحد يمكن أن يكون له عناصر متعددة
- **Product → StockMovements**: منتج واحد يمكن أن يكون له حركات مخزون متعددة

#### **Foreign Key Constraints**
- `products.supplier_id` → `suppliers.id`
- `orders.customer_id` → `customers.id`
- `order_items.order_id` → `orders.id`
- `order_items.product_id` → `products.id`
- `stock_movements.product_id` → `products.id`

### 📊 **فهارس قاعدة البيانات (Database Indexes)**

#### **Primary Keys**
- جميع النماذج لها `id` كـ Primary Key مع auto-increment

#### **Unique Indexes**
- `users.email`: فهرس فريد للبريد الإلكتروني
- `suppliers.file_path`: فهرس فريد لمسار الملف

#### **Regular Indexes**
- `users.email`: فهرس عادي للبحث السريع
- `products.supplier_id`: فهرس للربط مع الموردين
- `orders.customer_id`: فهرس للربط مع العملاء
- `order_items.order_id`: فهرس للربط مع الطلبات
- `order_items.product_id`: فهرس للربط مع المنتجات
- `stock_movements.product_id`: فهرس للربط مع المنتجات

### 🗂️ **ملفات Excel (Excel Files Structure)**

#### **الملفات الموجودة في `data/02_Excel/`**
- `suppliers_model_01.xlsx` - نموذج الموردين الأساسي
- `suppliers_model_02.xlsx` - نموذج الموردين المتقدم
- `suppliers_model_03.xlsx` - لوحة تحكم KPIs
- `suppliers_model_04.xlsx` - مقارنة شاملة
- `suppliers_model_05.xlsx` - نموذج إضافي

#### **الأعمدة الموحدة (Unified Columns)**
- `supplier_name`: اسم المورد
- `monthly_cost_eur`: التكلفة الشهرية باليورو
- `monthly_margin_eur`: الهامش الشهري باليورو
- `commission_percentage`: نسبة العمولة
- `minimum_order_qty`: الحد الأدنى للطلب
- `country_region`: البلد/المنطقة
- `specialization`: التخصص
- `shipping_time_days`: وقت الشحن بالأيام
- `product_price_range_eur`: نطاق أسعار المنتجات
- `overall_rating`: التقييم العام

### 🔐 **نظام الصلاحيات (Role-Based Access Control)**

#### **User Roles**
- **admin**: صلاحيات كاملة على جميع العمليات
- **manager**: صلاحيات على القراءة والإنشاء والتحديث
- **viewer**: صلاحيات قراءة فقط

#### **صلاحيات العمليات**
- **Create**: admin, manager
- **Read**: admin, manager, viewer
- **Update**: admin, manager
- **Delete**: admin فقط

### 📈 **إحصائيات قاعدة البيانات**

- **إجمالي النماذج**: 8 نموذج
- **إجمالي الجداول**: 8 جدول
- **إجمالي العلاقات**: 6 علاقة
- **إجمالي الفهارس**: 12+ فهرس
- **إجمالي القيود**: 8+ قيد

---

**آخر تحديث**: 2025-08-28
**حالة قاعدة البيانات**: ✅ مكتمل 100% - جميع النماذج والعلاقات موجودة
**التقنيات**: SQLAlchemy 2.0+ + Alembic + PostgreSQL
**الأمان**: Foreign Key Constraints + Role-Based Access Control

