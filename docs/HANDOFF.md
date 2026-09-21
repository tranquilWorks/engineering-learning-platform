# Handoff

`ELP-ROB-P01-P24` retains merged Robotics and Autonomy P01-P10 and completes
P11-P24 in one new target commit and one new pull request. Keep
`courses/robotics-autonomy-learning` read-only at
`f8807640258f1a6c1c77f1dcc9e61734551c585b`; the platform-owned derivative is
`courses/robotics-autonomy`.

Start from exact target baseline
`5f6fdae255cf5f188e4ee8a4d50e74949538b8eb`. Canonical control authority is
Portfolio Control merge `b9437c60a12e6c72918e55b037ef4d49e33166fa`, which
treats merged PR #12 as immutable and authorizes P11-P24 as fourteen full-rigor
sequential gates in exactly one new PR, plus the narrow completed-GNC catalog
assertion update to 5/134/134.

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

Expected final state is Robotics P01-P24 authored with zero remaining,
DSP/Radar 84/84, Controls/GNC 24/24, unchanged source gitlinks, and catalog
5 / 134 / 134. P24 is a software-only virtual-plant and fault-injection lesson;
do not convert it into a physical-HIL claim.

Publish exactly one P11-P24 implementation commit on
`agent/elp-robotics-p11-p24-20260921` and exactly one new PR (#13) against
`main`. Do not rewrite merged PR #12. Exact-head hosted backend, frontend, and
Linux/amd64 container jobs must pass before a separate human merge decision. A
later target commit invalidates prior hosted evidence.

Rollback before merge is branch/PR disposal. Rollback after merge is a reviewed
revert of the single P11-P24 implementation commit, restoring merged P01-P10
and catalog 5/120/120; the pinned source history is never rewritten.
