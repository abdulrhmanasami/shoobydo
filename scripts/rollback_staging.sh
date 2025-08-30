#!/usr/bin/env bash
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

# 3) إرجاع قاعدة البيانات إذا كانت مُهاجرة في هذا النشر
if [ -f .staging_db_flag ]; then
  echo "[rollback] DB was migrated in this deploy → attempting alembic downgrade -1"
  # تشغيل الخدمات أولاً
  docker compose -f docker-compose.staging.yml --env-file .env.staging up -d
  ok=0; for i in {1..60}; do curl -sSfL --max-time 5 --connect-timeout 2 http://127.0.0.1:8802/health >/dev/null && ok=1 && break || sleep 2; done
  if [ "$ok" = 1 ]; then
    cid="$(docker compose -f docker-compose.staging.yml ps -q backend || true)"
    if [ -n "${cid:-}" ]; then
      set +e
      docker exec "$cid" bash -lc "alembic downgrade -1"
      set -e
      echo "[rollback] DB downgrade attempted (check state)."
    else
      echo "[rollback] backend container not running; skip DB downgrade"
    fi
  else
    echo "[rollback] backend not healthy; skip DB downgrade"
  fi
  rm -f .staging_db_flag || true
else
  # 3) تشغيل بدون إرجاع DB
  docker compose -f docker-compose.staging.yml --env-file .env.staging up -d
  ok=0; for i in {1..60}; do curl -sSfL --max-time 5 --connect-timeout 2 http://127.0.0.1:8802/health >/dev/null && ok=1 && break || sleep 2; done
fi

[ "$ok" = 1 ] || { echo "❌ rollback failed"; exit 1; }
echo "✅ rollback ok"
