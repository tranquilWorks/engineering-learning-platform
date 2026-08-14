#!/usr/bin/env bash
set -euo pipefail

if command -v portfolio >/dev/null 2>&1; then
  exec portfolio run engineering-learning-platform "$@"
fi

control_dir="${PORTFOLIO_CONTROL_DIR:?install portfolio or set PORTFOLIO_CONTROL_DIR}"
exec python3 -B "$control_dir/scripts/roadmap_autopilot.py" engineering-learning-platform "$@"
