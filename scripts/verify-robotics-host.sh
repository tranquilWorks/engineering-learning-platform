#!/usr/bin/env bash
# Real built-site HTTP/browser checks. This is deliberately NOT Docker evidence.
set -euo pipefail
cd "$(dirname "$0")/.."
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export PYTHONPATH=apps/api/src
export ELP_WEB_DIST="$PWD/apps/web/dist"
export ELP_BROWSER_URL="${ELP_BROWSER_URL:-http://127.0.0.1:8879}"
export ELP_BROWSER_COURSE=robotics-autonomy
export ELP_BROWSER_REPORT="${ELP_BROWSER_REPORT:-docs/course-quality/robotics-aggregate-browser.json}"
export ELP_BROWSER_SCREENSHOT_DIR="${ELP_BROWSER_SCREENSHOT_DIR:-.state/robotics-browser-captures}"
mkdir -p .state
.venv/bin/python -m uvicorn elp_api.main:app --host 127.0.0.1 --port "${ELP_BROWSER_URL##*:}" > .state/robotics-host-server.log 2>&1 &
elp_robotics_server_pid=$!
trap 'kill "$elp_robotics_server_pid" 2>/dev/null || true' EXIT
.venv/bin/python - <<'PY'
import os
import time
import urllib.request
for attempt in range(45):
    try:
        with urllib.request.urlopen(os.environ['ELP_BROWSER_URL'] + '/api/v1/health', timeout=2) as response:
            assert response.status == 200
        break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit('Host API did not become ready')
PY
.venv/bin/python scripts/verify-robotics-assessments.py --base-url "$ELP_BROWSER_URL" --output docs/course-quality/robotics-aggregate-http.json
node scripts/browser-quality.mjs
npm run test:browser
