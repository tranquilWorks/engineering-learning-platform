# Handoff

ELP-ROB-P01-P10 adds Robotics and Autonomy P01-P10 in one target commit and one
pull request. Keep `courses/robotics-autonomy-learning` read-only at
`f8807640258f1a6c1c77f1dcc9e61734551c585b`; the platform-owned derivative is
`courses/robotics-autonomy`.

Start from exact target baseline
`71e3842f0839d9534a1c77e9d95d84a929489aff`. Canonical control authority is
Portfolio Control merge `d434e7a36dccc9c85577798c80a5e05b0dbfc677`, which
includes the narrow authorization to update the retained GNC catalog count
assertion from 4/110/110 to 5/120/120.

Before publishing the candidate, run in fail-fast order:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
  python3 -B -m pytest -q \
    apps/api/tests/test_robotics_conversion_framework.py \
    apps/api/tests/test_robotics_course.py
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
.venv/bin/ruff check \
  apps/api/tests/test_robotics_conversion_framework.py \
  apps/api/tests/test_robotics_course.py \
  courses/robotics-autonomy/modules \
  courses/robotics-autonomy/reference_cases.py
git diff --check
test -z "$(git -C courses/robotics-autonomy-learning status --porcelain=v1 --untracked-files=all)"
```

Expected final state is Robotics P01-P10 authored with 14 remaining,
DSP/Radar 84/84, Controls/GNC 24/24, unchanged source gitlinks, and catalog
5 / 120 / 120.

Publish exactly one implementation commit on
`agent/elp-robotics-p01-p10-20260921` and one PR against `main`. Exact-head
hosted backend, frontend, and Linux/amd64 container jobs must pass before a
separate human merge decision. A later target commit invalidates prior hosted
evidence.

Rollback before merge is branch/PR disposal. Rollback after merge is a reviewed
revert of the single Robotics implementation commit; the pinned source history
is never rewritten.
