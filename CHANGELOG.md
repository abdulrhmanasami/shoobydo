# Changelog

جميع التغييرات المهمة في هذا المشروع سيتم توثيقها في هذا الملف.

## [v0.3.0] - 2025-08-26

### Added ✨
- نظام مصادقة موحد مع JWT tokens
- Role-based access control للتقارير
- اختبارات regression شاملة للتقارير
- متغيرات JWT جديدة (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SKEW_SECONDS)
- تحديث CI workflow مع Python 3.12 وكاش pip

### Changed 🔄
- توحيد `get_current_user` dependency عبر جميع endpoints
- إزالة dependencies من مستوى الراوتر في reports
- تحديث `create_access_token` و `create_refresh_token` لاستخدام `dt.datetime.now(dt.timezone.utc)`
- إزالة middleware التشخيصي المؤقت

### Fixed 🐛
- **CRITICAL**: إصلاح خطأ 401 Unauthorized على `/api/v1/reports/summary`
- توحيد آلية استخراج التوكن عبر `get_bearer_token`
- إصلاح مشكلة JWT expiration مع timezone handling
- إزالة ازدواج في Dependency Injection

### Security 🔒
- تحسين JWT validation مع `jwt_decode_secure`
- إضافة JWT skew handling للتعامل مع clock drift
- توحيد Bearer token extraction

### Technical 🛠️
- تحديث CI ليعمل في `apps/backend` directory
- إضافة كاش pip dependencies
- تحسين اختبارات API مع httpx
- تنظيف الكود وإزالة dead code

### Breaking Changes ⚠️
- تغيير في `get_current_user` dependency signature
- إزالة router-level dependencies من reports

## [v0.2.x] - 2025-08-25

### Added ✨
- نظام مصادقة أساسي مع JWT
- إدارة الموردين (CRUD operations)
- نظام تقارير أساسي
- واجهة مستخدم مع Next.js

### Changed 🔄
- تحسين بنية المشروع
- إضافة middleware CORS
- تحديث نماذج قاعدة البيانات

## [v0.1.0] - 2025-08-24

### Added ✨
- إعداد المشروع الأساسي
- بنية FastAPI backend
- قاعدة بيانات PostgreSQL
- Redis للتخزين المؤقت

---

## ملاحظات الإصدار

### v0.3.0 - إصلاح أمني حرج
هذا الإصدار يركز على إصلاح مشكلة أمنية حرجة في نظام المصادقة:
- **قبل**: خطأ 401 على endpoints التقارير
- **بعد**: نظام مصادقة موحد وآمن مع role-based access control

### كيفية الترقية
1. تأكد من تحديث متغيرات البيئة (JWT_SKEW_SECONDS)
2. اختبر جميع endpoints بعد الترقية
3. راجع الصلاحيات الجديدة للمستخدمين

### الاعتماديات
- Python 3.12+ (مطلوب)
- FastAPI 0.104+
- python-jose[cryptography]
- httpx (للاختبارات)

---

**ملاحظة**: هذا الملف يتبع [Keep a Changelog](https://keepachangelog.com/) format.
