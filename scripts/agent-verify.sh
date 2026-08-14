#!/usr/bin/env bash
set -euo pipefail

mode="${1:-full}"
case "$mode" in
  contract)
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
      python3 -B -m pytest -q apps/api/tests/test_catalog.py apps/api/tests/test_runtime.py
    ;;
  quick)
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
      python3 -B -m pytest -q apps/api/tests
    ;;
  full)
    exec ./scripts/verify.sh
    ;;
  *)
    echo "usage: $0 {contract|quick|full}" >&2
    exit 2
    ;;
esac
