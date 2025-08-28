#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
git rev-parse --git-dir >/dev/null 2>&1 || git init -b main
git add -A
git commit -m "chore: prepare push" || true
if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    REPO_NAME=${REPO_NAME:-shoobydo}
    USER=$(gh api user -q .login)
    if ! gh repo view "$USER/$REPO_NAME" >/dev/null 2>&1; then
      gh repo create "$USER/$REPO_NAME" --source . --public --remote origin --push -y
    else
      git remote | grep -q "^origin$" || gh repo fork "$USER/$REPO_NAME" >/dev/null 2>&1 || git remote add origin "https://github.com/$USER/$REPO_NAME.git"
      git push -u origin main
    fi
    echo "[push] success via gh to https://github.com/$USER/$REPO_NAME"
    exit 0
  fi
fi
if git remote | grep -q "^origin$"; then
  git push -u origin main
  echo "[push] success via existing origin"
else
  echo "[push] no gh/remote. Add origin then push:"
  echo "  git remote add origin https://github.com/<YOUR_USERNAME>/shoobydo.git"
  echo "  git push -u origin main"
  exit 1
fi
