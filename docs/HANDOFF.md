# Handoff

ELP-GNC-P01-P24 converts the complete pinned 24-lesson Controls/GNC
curriculum in one target commit and one pull request. The work was internally
gated P01 through P24; do not split it into 24 PRs, mutate the read-only source,
or partially publish the retained prefix.

Before publishing or updating the final candidate, run in fail-fast order:

```bash
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
  apps/api/tests/test_gnc_conversion_framework.py \
  apps/api/tests/test_gnc_course.py courses/controls-gnc/modules
git diff --check
test -z "$(git -C courses/controls-gnc-learning status --porcelain=v1 --untracked-files=all)"
```

Expected GNC results are 80 source-attested tests, 24 converted rows with no
pending/blocked/placeholder item, all 24 closed-schema conversion records, and
4 courses / 110 modules / 110 interactive modules. Retained DSP/Radar tests
must remain green and the generic frontend must build without course-specific
changes.

Publish one commit on `agent/elp-gnc-p01-p24` and one PR against `main`.
GitHub Actions backend, frontend, and Linux/amd64 container jobs must all pass
on that exact head. A later commit invalidates earlier hosted evidence. Human
approval is required before merging the protected target.

Rollback before merge is to close/discard the isolated branch and return to
the exact baseline. After merge, use a reviewed revert of the single aggregate
commit, restoring the old GNC gitlink and removing the native `controls-gnc`
course without changing the completed DSP/Radar course.

The retained evidence establishes source-bound, deterministic trusted-Python
software behavior. It does not establish MATLAB parity, browser/accessibility
acceptance, learner effectiveness, hostile-code isolation, physical HIL/HWIL,
release, deployment, or production operation.
