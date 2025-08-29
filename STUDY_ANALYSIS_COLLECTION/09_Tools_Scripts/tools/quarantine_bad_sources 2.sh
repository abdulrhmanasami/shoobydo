#!/usr/bin/env bash
set -euo pipefail
src="docs/research/01_Report/Sources"
dst="docs/research/01_Report/_quarantine"
mkdir -p "$dst" reports
rep="reports/quarantine_$(date +%Y%m%d-%H%M%S).md"
echo "# Quarantine Report" > "$rep"; echo >> "$rep"
cnt=0
[ -d "$src" ] && while IFS= read -r -d '' f; do
  if grep -q "unsupported image format" "$f"; then
    rel="${f#$src/}"
    mkdir -p "$dst/$(dirname "$rel")"
    mv "$f" "$dst/$rel"
    echo "- moved: $rel" >> "$rep"
    cnt=$((cnt+1))
  fi
done < <(find "$src" -type f -print0)
echo >> "$rep"; echo "**Total moved:** $cnt" >> "$rep"
echo "[written] $rep"
