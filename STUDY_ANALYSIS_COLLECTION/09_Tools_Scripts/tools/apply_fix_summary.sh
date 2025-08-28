#!/usr/bin/env bash
set -euo pipefail
f="apps/backend/app/main.py"
if ! grep -q "os.walk" "$f"; then
  patch -p1 <<'PATCH'
*** Begin Patch
*** Update File: apps/backend/app/main.py
@@
 @app.get("/reports/summary", response_model=ReportSummary)
 def reports_summary():
-    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
-    suppliers = len([f for f in os.listdir(data_dir) if f.endswith(".xlsx")]) if os.path.isdir(data_dir) else 0
-    return ReportSummary(suppliers=suppliers, kpis=2, notes="based on Excel models")
+    import os
+    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
+    suppliers = 0
+    if os.path.isdir(data_dir):
+        for root, _, files in os.walk(data_dir):
+            suppliers += sum(1 for f in files if f.lower().endswith(".xlsx"))
+    return ReportSummary(suppliers=suppliers, kpis=2, notes="based on Excel models")
*** End Patch
PATCH
  echo "[patch] applied"
else
  echo "[patch] already applied"
fi
