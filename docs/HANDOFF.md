# Handoff

Controls/GNC P01-P24 fidelity remediation is complete within
`ELP-GNC-FIDELITY-P01-P24` at source pin
`ffd6623ee2cf8ccd8599fffd935ef07370750fa3`. The implementation retains one
target commit and pull request for 24 separately checked work items.

The durable course evidence is:

1. `courses/controls-gnc/fidelity-map.yaml` — exact source-model identity,
   controls, equations, observables, two sweeps, failure/recovery, limiting
   cases, omissions, reference method, and axes for every P01-P24 item.
2. `courses/controls-gnc/reference_cases.py` — course-owned closed-form,
   alternate-algorithm, or separately formulated numerical references that do
   not import production experiments or consume production output.
3. Each module's `expected-independent.json` and `actual-production.json` —
   baseline, sweep 1, sweep 2, broken, and recovery signatures with ordered
   fields and units.
4. `docs/evidence/ELP-GNC-FIDELITY-P01-P24-2026-09-21.md` — the retained
   verification and claim boundary.

Do not reintroduce production-derived expected vectors or generic axes. Preserve
P20's narrow two-fixed-gain statement and P24's software-only, non-capstone
boundary. The next Controls/GNC work is issue #439: create or review the
competency map, derive the expansion count from it, and authorize coherent
batches of at most ten new lessons.

Issues #440 and #441 remain separate Robotics and DSP/Radar work. Vehicle
Dynamics remains blocked until its reviewed competency map, replayable GR86
CAN/BLE fixtures, and separate first batch are authorized.

Rollback this remediation by reverting its single target merge. The source
repository and all source gitlinks remain unchanged.
