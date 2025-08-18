#!/usr/bin/env bash
set -euo pipefail
f="apps/backend/app/main.py"
if ! grep -q "CORSMiddleware" "$f"; then
  patch -p1 <<'PATCH'
*** Begin Patch
*** Update File: apps/backend/app/main.py
@@
 from fastapi import FastAPI
+from fastapi.middleware.cors import CORSMiddleware
@@
-app = FastAPI(title="EuroDropship API", version="0.1.0")
+app = FastAPI(title="shoobydo-api")
+
+# CORS: اسمح لواجهة التطوير بالاتصال
+import os as _os
+_fe_port = _os.getenv("FRONTEND_PORT", "3000")
+_origins = [f"http://127.0.0.1:{_fe_port}", f"http://localhost:{_fe_port}"]
+app.add_middleware(
+    CORSMiddleware,
+    allow_origins=_origins,
+    allow_credentials=True,
+    allow_methods=["*"],
+    allow_headers=["*"],
+)
*** End Patch
PATCH
  echo "[cors] applied"
else
  echo "[cors] already present"
fi
