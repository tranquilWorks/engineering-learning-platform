# Handoff

ELP-DSP-P01-P84 converts the complete pinned 84-lesson DSP/Radar curriculum
on one branch and is intended for one implementation commit and one pull
request. Do not split the retained candidate into 84 target PRs or mutate the
read-only source gitlink.

Before publishing or updating the final candidate, run in fail-fast order:

```bash
ELP_DSP_SOURCE_ROOT=courses/dsp-radar-learning \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
  python3 -B -m pytest -q \
    apps/api/tests/test_dsp_conversion_framework.py \
    apps/api/tests/test_dsp_course.py
./scripts/agent-verify.sh contract
./scripts/agent-verify.sh quick
./scripts/agent-verify.sh full
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
  python3 -B scripts/validate_courses.py --execute --deterministic --json
git diff --check
test -z "$(git -C courses/dsp-radar-learning status --porcelain=v1 --untracked-files=all)"
```

Expected results are 300 complete DSP/framework tests, 72 contract tests, 376
quick/full backend tests, a passing frontend typecheck/build, 3 courses, 86
modules, 86 interactive modules, and 84 converted coverage rows with no
pending, blocked, or placeholder item. The source/map/schema/authoring/course
framework hashes must remain unchanged.

After the single commit is pushed, open one PR against `main`. GitHub Actions
backend, frontend, and Linux/amd64 container jobs must all pass on that exact
head. A later commit invalidates earlier hosted evidence. Resolve all review
threads and obtain explicit human approval before merging the protected
branch.

Rollback before merge is to close/discard this isolated branch and return to
the exact baseline. After merge, use a reviewed revert of the single aggregate
implementation commit. Do not partially delete modules or rewrite the pinned
source history.

The retained software evidence establishes catalog visibility, deterministic
trusted-Python execution, and source-bound numeric equivalence. It does not
establish MATLAB parity, browser/accessibility acceptance, learner
effectiveness, hostile-code isolation, physical radar performance, release,
deployment, or production operation.
