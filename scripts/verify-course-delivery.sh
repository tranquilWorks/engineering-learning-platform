#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export ELP_BROWSER_URL="${ELP_BROWSER_URL:-http://127.0.0.1:8767}"
export ELP_CONTAINER_NAME="${ELP_CONTAINER_NAME:-elp-gnc-quality}"
export ELP_IMAGE_TAG="${ELP_IMAGE_TAG:-elp-gnc-quality:20261103}"
export ELP_BROWSER_COURSE=controls-gnc
export ELP_BROWSER_REPORT="${ELP_BROWSER_REPORT:-docs/course-quality/gnc-aggregate-baked-browser.json}"
export ELP_BROWSER_SCREENSHOT_DIR="${ELP_BROWSER_SCREENSHOT_DIR:-.state/gnc-baked-captures}"
command -v docker >/dev/null || { echo "BLOCKED: Docker CLI/daemon required for baked delivery; host checks do not replace it." >&2; exit 2; }
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
docker build -t "$ELP_IMAGE_TAG" .
docker run -d --name "$ELP_CONTAINER_NAME" --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=128m --cap-drop ALL \
  --security-opt no-new-privileges --pids-limit 256 --memory 2g --cpus 2 \
  -p "127.0.0.1:${ELP_BROWSER_URL##*:}:8080" "$ELP_IMAGE_TAG"
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

PYTHONPATH=apps/api/src .venv/bin/python scripts/verify-gnc-assessments.py --base-url "$ELP_BROWSER_URL" --output docs/course-quality/gnc-aggregate-baked-http.json
