#!/bin/bash
set -euo pipefail
# 1) أوقف الإصدار الحالي
docker compose -f docker-compose.staging.yml --env-file .env.staging down || true
# 2) بدّل الوسوم إلى الإصدار السابق (اقرأ من REV ملف حالة إن وُجد)
REVFILE=.staging_prev_rev
if [ -f "$REVFILE" ]; then
  PREV=$(cat "$REVFILE")
  echo "↩️ rolling back to $PREV"
  sed -i.bak "s|^BACKEND_IMAGE=.*|BACKEND_IMAGE=$PREV|" .env.staging || true
fi
# 3) تشغيل
docker compose -f docker-compose.staging.yml --env-file .env.staging up -d
ok=0; for i in {1..60}; do curl -sSfL --max-time 5 --connect-timeout 2 http://127.0.0.1:8801/health >/dev/null && ok=1 && break || sleep 2; done
[ "$ok" = 1 ] || { echo "❌ rollback failed"; exit 1; }
echo "✅ rollback ok"
