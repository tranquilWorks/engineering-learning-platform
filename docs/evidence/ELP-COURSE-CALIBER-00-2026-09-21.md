# ELP-COURSE-CALIBER-00 evidence — 2026-09-21

## Identity and scope

- Target repository: `tranquilWorks/engineering-learning-platform`
- Exact starting commit: `39aed41de4e3c84fc00c3b8546c5488e253b6be2`
- Exact starting tree: `648c193722e8d356b7520ba064e23e884d25d36c`
- Merged Portfolio Control authority:
  `f6745e44f459a52431b81a3f953c8f2e03cbe45e`
- Control issue: `tranquilWorks/portfolio-control#437`
- Scope: governance documentation, target status, verification contract, and
  one focused status-contract test only.

No `courses/**`, API runtime, web source, package, dependency, workflow,
deployment, source-gitlink, or Vehicle Dynamics content changed. The target
candidate commit is the exact pull-request head reported in the merge and
issue-close records; a commit cannot embed its own SHA without changing it.

## Local verification

All commands ran from the isolated target worktree on the projected change.

| Gate | Result |
| --- | --- |
| `python -m pytest -q apps/api/tests/test_course_caliber_status.py` | PASS — 12 tests in 0.21 s |
| `./scripts/agent-verify.sh contract` | PASS — 72 tests in 11.45 s |
| `./scripts/agent-verify.sh quick` | PASS — 547 tests in 39.86 s; four retained dependency deprecation warnings |
| `./scripts/agent-verify.sh full` | PASS — deterministic catalog 5 courses / 134 modules / 134 interactive; 547 backend tests; frontend TypeScript build and Vite production build |
| `scripts/validate_courses.py --execute --deterministic --json` | PASS — 5 courses, 134 modules, 134 interactive modules, zero errors |
| `ruff check apps/api/tests/test_course_caliber_status.py` | PASS |
| `git diff --check` | PASS |
| `test -z "$(git status --short -- courses)"` | PASS — no course-path changes |

The focused tests validate the closed status shape, exact six-stage ordering,
nine rubric dimensions, inventory-only count semantics, three audited course
dispositions, issue ownership, Vehicle Dynamics hold, competency-map count
source, coherent ten-lesson limit, and rejection of production-imported,
production-derived, or production-perturbed evidence.

## Dispositions

- DSP/Radar remediation remains issue #441. It was not implemented here.
- Controls/GNC fidelity repair remains issue #438. It was not implemented here.
- Controls/GNC curriculum expansion remains issue #439. It was not implemented here.
- Robotics and Autonomy expansion remains issue #440. It was not implemented here.
- Vehicle Dynamics remains queued and unimplemented pending its reviewed map,
  replayable GR86 CAN/BLE fixtures, and a separate coherent batch of no more
  than ten new lessons.

## Evidence boundary

Hosted GitHub Actions were not used as a completion gate at the user's explicit
direction, so no hosted-CI result is claimed. MATLAB runtime, browser or
accessibility acceptance, representative-learner effectiveness, physical
hardware/HIL, bench, field, release, deployment, credentials/settings, and
production operation were not performed and are not implied.

This evidence closes only the course-caliber governance projection. It does
not close any numerical-fidelity, curriculum-expansion, capstone, or learner
validation finding identified by the audit.
