#!/usr/bin/env bash
set -euo pipefail
# يحوّل Config.orm_mode إلى model_config = ConfigDict(from_attributes=True)
apply_fix() {
  local f="$1"
  # أضف الاستيراد إن لزم
  grep -q 'from pydantic import ConfigDict' "$f" || \
    sed -i '' '1s/^/from pydantic import ConfigDict\n/' "$f"
  # احذف كلاس Config القديم (إن وُجد)
  perl -0777 -pe 's/class\s+Config\s*:\s*\{?\s*[^}]*?orm_mode\s*=\s*True\s*\}?//s' -i "$f"
  # أضف model_config إن لم توجد
  grep -q 'model_config\s*=\s*ConfigDict' "$f" || \
    printf '\nmodel_config = ConfigDict(from_attributes=True)\n' >> "$f"
}
export -f apply_fix
find apps/backend -type f -name "*schema*.py" -print0 | xargs -0 -I{} bash -c 'apply_fix "$@"' _ {}
find apps/backend -type f -name "*schemas*.py" -print0 | xargs -0 -I{} bash -c 'apply_fix "$@"' _ {}
