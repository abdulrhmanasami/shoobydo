# سجل التغييرات

## v3
- دمج البنية الخلفية مع قاعدة البيانات (Postgres) والكاش (Redis) وتوفير نقاط ping (`/db/ping`, `/cache/ping`).
- إضافة نقاط الكلفة والكفاءات: `/reports/costs`, `/reports/kpis`.
- إنشاء صفحات الواجهة: `/dashboard`, `/suppliers`, `/costs` مع رسم بياني باستخدام recharts.
- إزالة Tailwind وتبسيط CSS عالمي.
- إضافة Alembic للهجرات وتحديث أوامر التشغيل (`tools/dev_up.sh`) وتقارير التشغيل.
- تحسين إدارة الموردين: إضافة CRUD كامل (`POST/GET/PUT/DELETE /suppliers`)، وتحسين واجهة `/suppliers` مع الإشعارات.
- إضافة رفع ملفات Excel عبر `POST /suppliers/upload` وصفحة `/upload` في الواجهة.

## v2
- تنظيف الأرشيف: حذف `__MACOSX/`, ملفات `._*`, و`pasted_content.txt`.
- هيكلة جديدة: `01_Report/`, `02_Excel/`, `03_Assets/`.
- توحيد الأسماء وترتيب الملفات.
- إنشاء تقرير موحّد PDF: `01_Report/EuroDropship-Full-Report.pdf`.
- إضافة README باللغة العربية.

## ما تبقّى للتحسين
- إدراج الصور داخل التقرير بدلاً من الإحالة النصية فقط.
- مراجعة المراجع الموحدة وتنسيق الفهارس المتقدمة.
- 2025-08-21 feat: Orders core merged (EPIC-02/TASK-02H)
- 2025-08-21 feat: Order Items core (EPIC-02/TASK-02I)
- [2025-08-21] feat: Order Totals & Constraints (EPIC-02/TASK-02J)
