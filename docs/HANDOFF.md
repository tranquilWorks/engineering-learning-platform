# Handoff

ELP-B010-01 is already merged and its exact-head hosted verification passed.
ELP-DSP-00 now advances only the `courses/dsp-radar-learning` gitlink from
`203c3738a88070bd43a93d969b6991a195bb6e27` to the reviewed read-only source
commit `5d73667a486df4a7b6c581e4c9406e810ed4f0f6` and establishes the separate
platform-owned `courses/dsp-radar` conversion framework.

Before claiming the ELP-DSP-00 candidate complete, run the active contract's
focused framework and source-attested immutability tests, followed in fail-fast
order by:

```bash
./scripts/agent-verify.sh contract
./scripts/agent-verify.sh quick
./scripts/agent-verify.sh full
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
  python3 -B scripts/validate_courses.py --execute --deterministic --json
git diff --check
git diff --submodule=log \
  8019d1798ea771f1f466e24c9983549ec1d6c127 -- \
  courses/dsp-radar-learning
```

Retain exact commands, exits, revisions, source before/after inventories, and
catalog counts in `docs/evidence/ELP-DSP-00-<date>.md`. The expected framework
catalog is three courses, two implemented modules, and two interactive modules.
The DSP coverage ledger must remain 84 pending, zero converted, zero blocked,
and zero placeholders, with no directory under `courses/dsp-radar/modules/`.

After ELP-DSP-00 is reviewed, CI-green, and merged, the next authorized work is
only ELP-DSP-P01. Each successor may convert exactly its one mapped item,
advance coverage by one, and retain its own source-equivalence evidence. Do not
bulk-create P02-P84, skip a blocked item, modify the pinned source, or treat the
inventory as learner content.

Rollback before any successor merges is a reviewed revert of ELP-DSP-00: restore
the old DSP gitlink and remove the platform-owned framework, focused tests,
documentation, and evidence added by the batch. There is no source-course
write, learner data, database migration, dependency change, release, deployment,
or production state to reverse.

Repository-static, deterministic trusted-Python, API protocol, frontend build,
and source-immutability evidence do not establish a converted DSP lesson,
MATLAB execution or equivalence, visual or accessibility universality, learner
effectiveness, physical/operational radar behavior, release, deployment, or
production operation.
