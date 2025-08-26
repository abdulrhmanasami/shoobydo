# 🚀 Shoobydo - نظام إدارة الموردين والمخزون

[![CI](https://github.com/abdulrhmanasami/shoobydo/workflows/CI/badge.svg)](https://github.com/abdulrhmanasami/shoobydo/actions)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 نظرة عامة

Shoobydo هو نظام متكامل لإدارة الموردين والمخزون مبني على **FastAPI** مع واجهة مستخدم حديثة باستخدام **Next.js**. يوفر النظام حلاً شاملاً لإدارة العلاقات مع الموردين، تتبع المخزون، وإنشاء تقارير مفصلة.

## ✨ الميزات الرئيسية

- 🔐 **نظام مصادقة موحد** مع JWT tokens و role-based access control
- 👥 **إدارة الموردين** مع عمليات CRUD كاملة
- 📊 **نظام تقارير شامل** مع مؤشرات الأداء والتحليلات
- 🚀 **واجهة API RESTful** آمنة وسريعة
- 💾 **قاعدة بيانات PostgreSQL** مع Redis للتخزين المؤقت
- 🧪 **اختبارات شاملة** مع pytest و httpx
- 🐳 **دعم Docker** للتطوير والنشر

## 🏗️ البنية التقنية

```
shoobydo/
├── apps/
│   ├── backend/              # FastAPI Backend
│   │   ├── app/
│   │   │   ├── security.py   # نظام المصادقة
│   │   │   ├── routers/      # API endpoints
│   │   │   └── main.py       # التطبيق الرئيسي
│   │   ├── tests/            # الاختبارات
│   │   └── requirements.txt  # تبعيات Python
│   └── frontend/             # Next.js Frontend
│       ├── app/              # صفحات التطبيق
│       ├── components/       # المكونات
│       └── package.json      # تبعيات Node.js
├── docs/                     # التوثيق
├── infra/                    # ملفات البنية التحتية
└── tools/                    # أدوات مساعدة
```

## 🚀 البدء السريع

### المتطلبات الأساسية

- **Python 3.12+**
- **Node.js 18+**
- **PostgreSQL 16**
- **Redis 7**

### التثبيت السريع

1. **استنساخ المشروع**
```bash
git clone https://github.com/abdulrhmanasami/shoobydo.git
cd shoobydo
```

2. **تشغيل Backend**
```bash
cd apps/backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# أو .venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8811
```

3. **تشغيل Frontend**
```bash
cd apps/frontend
npm install
npm run dev
```

4. **إعداد قاعدة البيانات**
```bash
cd apps/backend
alembic upgrade head
```

## ⚙️ الإعداد

### متغيرات البيئة

أنشئ ملف `.env` في `apps/backend/`:

```bash
# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_SKEW_SECONDS=300

# Database
POSTGRES_PASSWORD=your-password
POSTGRES_DB=shoobydo
POSTGRES_PORT=5432

# Redis
REDIS_PORT=6379

# Server
SHOOBYDO_BACKEND_PORT=8811
```

### تشغيل مع Docker

```bash
docker-compose up -d
```

## 📚 API Documentation

### Endpoints الرئيسية

| Method | Endpoint | الوصف | الصلاحيات |
|--------|----------|--------|------------|
| `POST` | `/api/v1/auth/login` | تسجيل الدخول | - |
| `GET` | `/api/v1/suppliers` | قائمة الموردين | admin, manager |
| `GET` | `/api/v1/reports/summary` | ملخص عام | admin, viewer |
| `GET` | `/api/v1/reports/kpis` | مؤشرات الأداء | admin, viewer |
| `POST` | `/api/v1/reports/refresh` | تحديث التقارير | admin |

### مثال على الاستخدام

```bash
# تسجيل الدخول
curl -X POST "http://localhost:8811/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"admin123"}'

# الحصول على التقارير
curl -X GET "http://localhost:8811/api/v1/reports/summary" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🧪 الاختبارات

### تشغيل الاختبارات

```bash
cd apps/backend
pytest tests/ -v
```

### اختبارات محددة

```bash
# اختبارات التقارير
pytest tests/test_reports_auth.py -v

# اختبارات أساسية
pytest tests/test_api_smoke.py -v

# جميع الاختبارات مع تغطية
pytest tests/ --cov=app --cov-report=html
```

## 🔒 الأمان

### نظام المصادقة

- **JWT Tokens** مع expiration time قابل للتكوين
- **Role-based Access Control** مع 3 مستويات: admin, manager, viewer
- **Bearer Token Authentication** مع validation محسن
- **JWT Skew Handling** للتعامل مع clock drift

### الصلاحيات

| الدور | الوصول | الوصف |
|-------|---------|--------|
| **admin** | كامل | صلاحيات كاملة على النظام |
| **manager** | محدود | إدارة الموردين والتقارير |
| **viewer** | قراءة فقط | عرض التقارير والبيانات |

## 🚀 النشر

### Production

```bash
# بناء Docker image
docker build -t shoobydo:latest apps/backend/

# تشغيل
docker run -d -p 8811:8811 \
  -e SECRET_KEY=your-production-secret \
  shoobydo:latest
```

### CI/CD

- **GitHub Actions** مع اختبارات تلقائية
- **Docker** للبناء والنشر
- **Python 3.12** مع كاش pip dependencies

## 🤝 المساهمة

نرحب بالمساهمات! يرجى اتباع الخطوات التالية:

1. **Fork** المشروع
2. **إنشاء فرع** للميزة الجديدة (`git checkout -b feature/AmazingFeature`)
3. **Commit** التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. **Push** إلى الفرع (`git push origin feature/AmazingFeature`)
5. **فتح Pull Request**

### إرشادات التطوير

- اتبع معايير PEP 8 للكود
- اكتب اختبارات شاملة لكل ميزة جديدة
- اختبر التطبيق محلياً قبل الـ PR
- اتبع نمط commit messages التقليدي

## 📝 الترخيص

هذا المشروع مرخص تحت رخصة **MIT** - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## 🆘 الدعم

### المشاكل المعروفة

- لا توجد مشاكل معروفة حالياً

### الإبلاغ عن الأخطاء

1. تحقق من [Issues](https://github.com/abdulrhmanasami/shoobydo/issues) الموجودة
2. أنشئ issue جديد مع تفاصيل كاملة
3. ارفق سجلات الخطأ إن أمكن

### التواصل

- **GitHub Issues**: للمشاكل والاقتراحات
- **GitHub Discussions**: للمناقشات العامة

## 📊 الحالة الحالية

**الإصدار:** v0.3.0  
**الحالة:** جاهز للإنتاج  
**آخر تحديث:** 2025-08-26

### الإنجازات الأخيرة

- ✅ توحيد نظام المصادقة
- ✅ إصلاح خطأ 401 على التقارير
- ✅ إضافة role-based access control
- ✅ اختبارات regression شاملة

---

**⭐ إذا أعجبك المشروع، لا تنس إعطاءه نجمة!**

**المطور:** Shoobydo Team  
**الإصدار:** v0.3.0  
**آخر تحديث:** 2025-08-26
