#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export ELP_BROWSER_URL="${ELP_BROWSER_URL:-http://127.0.0.1:8767}"
export ELP_CONTAINER_NAME="${ELP_CONTAINER_NAME:-elp-course-quality}"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
# Existing named containers are never replaced by this verifier.
if docker container inspect "$ELP_CONTAINER_NAME" >/dev/null 2>&1; then
  echo "Container $ELP_CONTAINER_NAME already exists; choose a fresh ELP_CONTAINER_NAME and localhost port." >&2
  exit 2
fi
PYTHONPATH=apps/api/src .venv/bin/python scripts/audit_course_quality.py
npm ci
npx playwright install chromium
npm run test:web
npm run typecheck
npm run build
docker build -t elp-robotics-perception-quality:20260930 .
docker run -d --name "$ELP_CONTAINER_NAME" --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=128m --cap-drop ALL \
  --security-opt no-new-privileges --pids-limit 256 --memory 2g --cpus 2 \
  -p "127.0.0.1:${ELP_BROWSER_URL##*:}:8080" elp-robotics-perception-quality:20260930
trap 'docker stop "$ELP_CONTAINER_NAME" >/dev/null' EXIT
python3 - <<'PY'
import os,time,urllib.request
for attempt in range(60):
    try:
        with urllib.request.urlopen(os.environ['ELP_BROWSER_URL']+'/api/v1/catalog',timeout=5) as response:
            assert response.status==200
        break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit('Container did not become ready')
PY
npm run test:browser
PYTHONPATH=apps/api/src .venv/bin/python scripts/container-quality.py
node scripts/browser-quality.mjs

PYTHONPATH=apps/api/src .venv/bin/python scripts/verify-robotics-perception-quality.py --base-url "$ELP_BROWSER_URL"
