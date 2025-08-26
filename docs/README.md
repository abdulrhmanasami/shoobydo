# Shoobydo - نظام إدارة الموردين والمخزون

## نظرة عامة
Shoobydo هو نظام متكامل لإدارة الموردين والمخزون مبني على FastAPI مع واجهة مستخدم حديثة.

## الميزات الرئيسية
- ✅ نظام مصادقة موحد مع JWT
- ✅ إدارة الموردين مع صلاحيات مختلفة
- ✅ نظام تقارير شامل مع role-based access control
- ✅ واجهة API RESTful آمنة
- ✅ قاعدة بيانات PostgreSQL مع Redis للتخزين المؤقت

## الحالة الحالية
**الإصدار:** v0.3.0  
**الحالة:** جاهز للإنتاج  
**آخر تحديث:** 2025-08-26

### الإصلاحات الأخيرة
- ✅ توحيد نظام المصادقة عبر جميع endpoints
- ✅ إصلاح خطأ 401 على `/api/v1/reports/summary`
- ✅ إضافة role-based access control
- ✅ اختبارات regression شاملة

## البنية التقنية

### Backend (FastAPI)
```
apps/backend/
├── app/
│   ├── security.py          # نظام المصادقة الموحد
│   ├── routers/             # API endpoints
│   │   ├── auth.py         # تسجيل الدخول والخروج
│   │   ├── suppliers.py    # إدارة الموردين
│   │   └── reports.py      # التقارير (مُصلح)
│   └── main.py             # التطبيق الرئيسي
├── tests/                   # الاختبارات
│   ├── test_api_smoke.py   # اختبارات أساسية
│   └── test_reports_auth.py # اختبارات التقارير
└── requirements.txt         # التبعيات
```

### Frontend (Next.js)
```
apps/frontend/
├── app/                     # صفحات التطبيق
├── components/              # المكونات
└── lib/                     # المكتبات المساعدة
```

## التثبيت والتشغيل

### متطلبات النظام
- Python 3.12+
- Node.js 18+
- PostgreSQL 16
- Redis 7

### متغيرات البيئة
```bash
# JWT Configuration
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_SKEW_SECONDS=300

# Database
POSTGRES_PASSWORD=your-password
POSTGRES_DB=shoobydo

# Redis
REDIS_PORT=6379
```

### تشغيل Backend
```bash
cd apps/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8811
```

### تشغيل Frontend
```bash
cd apps/frontend
npm install
npm run dev
```

## API Endpoints

### المصادقة
- `POST /api/v1/auth/login` - تسجيل الدخول
- `POST /api/v1/auth/refresh` - تجديد التوكن
- `POST /api/v1/auth/logout` - تسجيل الخروج

### الموردين
- `GET /api/v1/suppliers` - قائمة الموردين
- `POST /api/v1/suppliers` - إضافة مورد جديد
- `PUT /api/v1/suppliers/{id}` - تحديث مورد
- `DELETE /api/v1/suppliers/{id}` - حذف مورد

### التقارير
- `GET /api/v1/reports/summary` - ملخص عام (admin/viewer)
- `GET /api/v1/reports/kpis` - مؤشرات الأداء (admin/viewer)
- `GET /api/v1/reports/costs` - تحليل التكاليف (admin/viewer)
- `POST /api/v1/reports/refresh` - تحديث التقارير (admin فقط)

## الاختبارات

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
```

## الأمان

### نظام المصادقة
- JWT tokens مع expiration time
- Role-based access control
- Bearer token authentication
- JWT skew handling للتعامل مع drift في الوقت

### الصلاحيات
- **admin**: صلاحيات كاملة
- **manager**: إدارة الموردين والتقارير
- **viewer**: عرض التقارير فقط

## المساهمة

### إرشادات التطوير
1. استخدم فرع جديد لكل ميزة
2. اكتب اختبارات شاملة
3. اتبع معايير الكود
4. اختبر التطبيق محلياً قبل الـ PR

### إجراءات الـ CI/CD
- اختبارات تلقائية على كل PR
- بناء Docker images
- فحص جودة الكود

## الدعم والصيانة

### السجلات
- سجلات التطبيق: `/tmp/shoobydo-api.log`
- سجلات الاختبارات: `pytest` output

### المراقبة
- Health check: `GET /health`
- API health: `GET /api/health`

## الترخيص
MIT License - انظر ملف `LICENSE` للتفاصيل.

---

**آخر تحديث:** 2025-08-26  
**المطور:** Shoobydo Team  
**الإصدار:** v0.3.0
