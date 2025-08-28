#!/usr/bin/env bash
set -euo pipefail
OUTDIR="reports/EPIC-02/TASK-02K"
OUT="$OUTDIR/DELIVERABLES.md"
mkdir -p "$OUTDIR"
{
  echo "# EPIC-02 / TASK-02K — Deliverables"
  echo
  echo "## Inventory Adjustment (Stock to 10)"
  echo '```'
  if [ -s "$OUTDIR/curl_01_adjust_to_10.txt" ]; then
    cat "$OUTDIR/curl_01_adjust_to_10.txt"
  else
    echo "(inventory adjustment file not found)"
  fi
  echo '```'
  echo
  echo "## Oversell Attempt (409/422 expected)"
  echo '```'
  if [ -s "$OUTDIR/curl_03_oversell_attempt_12.txt" ]; then
    sed -n '1,60p' "$OUTDIR/curl_03_oversell_attempt_12.txt"
  else
    echo "(oversell attempt file not found)"
  fi
  echo '```'
  echo
  echo "## Add/Delete Evidence"
  echo '```'
  if [ -s "$OUTDIR/curl_02_add_item_qty7.txt" ]; then
    sed -n '1,40p' "$OUTDIR/curl_02_add_item_qty7.txt"
  else
    echo "(add item file not found)"
  fi
  echo '```'
  echo '```'
  if [ -s "$OUTDIR/curl_04_delete_item.txt" ]; then
    sed -n '1,40p' "$OUTDIR/curl_04_delete_item.txt"
  else
    echo "(delete item file not found)"
  fi
  echo '```'
  echo
  echo "## Totals"
  echo '```'
  echo "after_add:"
  if [ -s "$OUTDIR/total_after_add.txt" ]; then
    cat "$OUTDIR/total_after_add.txt"
  else
    echo "(total_after_add.txt not found)"
  fi
  echo "after_delete:"
  if [ -s "$OUTDIR/total_after_delete.txt" ]; then
    cat "$OUTDIR/total_after_delete.txt"
  else
    echo "(total_after_delete.txt not found)"
  fi
  echo '```'
  echo
  echo "## IDs"
  echo '```'
  if [ -s "$OUTDIR/_ids.txt" ]; then
    cat "$OUTDIR/_ids.txt"
  else
    echo "(IDs file not found)"
  fi
  echo '```'
  echo
  echo "## Backend log (last 200)"
  echo '```'
  if [ -s "$OUTDIR/backend_last200.log" ]; then
    sed -n '1,200p' "$OUTDIR/backend_last200.log"
  else
    echo "(backend log not found)"
  fi
  echo '```'
} > "$OUT"
echo "✅ جاهز: $OUT"
