# Handoff

ELP-ORG-IDENTITY normalizes the transferred GitHub repository identities in
one target commit and one pull request. It must not import, implement, convert,
or polish another course.

Start from exact target baseline
`923a86ab79893bd939d88d275bdcb12a5a1ddad6`. The merged control contract is
`373aa5f5bd1ecc63740a03cba01c3eef237bb8af`.

Before publishing the candidate, run in fail-fast order:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
  python3 -B -m pytest -q \
    apps/api/tests/test_dsp_conversion_framework.py \
    apps/api/tests/test_gnc_conversion_framework.py
ELP_DSP_SOURCE_ROOT=courses/dsp-radar-learning \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
  python3 -B -m pytest -q \
    apps/api/tests/test_dsp_conversion_framework.py \
    apps/api/tests/test_dsp_course.py
ELP_GNC_SOURCE_ROOT=courses/controls-gnc-learning \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
  python3 -B -m pytest -q \
    apps/api/tests/test_gnc_conversion_framework.py \
    apps/api/tests/test_gnc_course.py
./scripts/agent-verify.sh contract
./scripts/agent-verify.sh quick
./scripts/agent-verify.sh full
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
  python3 -B scripts/validate_courses.py --execute --deterministic --json
git diff --check
test -z "$(git diff --raw 923a86ab79893bd939d88d275bdcb12a5a1ddad6 -- courses/*-learning)"
test -z "$(git diff --name-only 923a86ab79893bd939d88d275bdcb12a5a1ddad6 -- \
  'courses/*/modules/*/lesson.md' \
  'courses/*/modules/*/module.yaml' \
  'courses/*/modules/*/experiment.py' \
  'courses/*/modules/*/evidence/**')"
```

Expected final state is 13 canonical `tranquilWorks` submodule URLs, no stale
current `kpbianco` repository identity, unchanged gitlinks/course payloads,
DSP/Radar 84/84, Controls/GNC 24/24, and catalog 4 / 110 / 110.

Publish exactly one commit on `agent/elp-tranquilworks-identity` and one PR
against `main`. Exact-head hosted backend, frontend, and Linux/amd64 container
jobs must pass before human merge. A later commit invalidates earlier hosted
evidence.

Rollback before merge is branch/PR disposal. Rollback after merge is a reviewed
revert of the single identity-normalization commit. GitHub transfer redirects
remain external and no source-course history is rewritten.
