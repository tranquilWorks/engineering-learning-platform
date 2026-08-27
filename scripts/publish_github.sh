#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

visibility="${1:-}"
case "$visibility" in
  public|private|internal) ;;
  *)
    echo "usage: $0 {public|private|internal}" >&2
    exit 2
    ;;
esac

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required." >&2
  exit 2
fi
if git remote get-url origin >/dev/null 2>&1; then
  echo "origin already exists: $(git remote get-url origin)" >&2
  exit 2
fi

args=(repo create tranquilWorks/engineering-learning-platform --source . --remote origin --push)
case "$visibility" in
  public) args+=(--public) ;;
  private) args+=(--private) ;;
  internal) args+=(--internal) ;;
esac

gh "${args[@]}"
