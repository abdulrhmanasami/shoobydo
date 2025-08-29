#!/bin/bash
# /etc/cron.d/pg-backup

# نسخ احتياطي يومي لقاعدة البيانات
0 2 * * * pg_dump -Fc "$DATABASE_URL" > /backups/shoobydo_$(date +\%F).dump

# الاحتفاظ 7 أيام
find /backups -name 'shoobydo_*.dump' -mtime +7 -delete

# استعادة: pg_restore -d "$DATABASE_URL" /backups/shoobydo_YYYY-MM-DD.dump
