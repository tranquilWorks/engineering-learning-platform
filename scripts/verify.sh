#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

export PYTHONPATH="${PYTHONPATH:-}:apps/api/src"
python3 -m compileall -q apps/api/src courses scripts
python3 scripts/export_schemas.py --check
python3 scripts/validate_courses.py --execute --deterministic
pytest -q apps/api/tests

if [[ ! -d node_modules ]]; then
  if [[ "${ELP_ALLOW_FRONTEND_SKIP:-0}" == "1" ]]; then
    echo "SKIP: node_modules is absent; frontend typecheck/build explicitly waived for this environment." >&2
    exit 0
  fi
  echo "ERROR: node_modules is absent. Run npm install; frontend verification is mandatory." >&2
  exit 2
fi

npm run typecheck
npm run build
