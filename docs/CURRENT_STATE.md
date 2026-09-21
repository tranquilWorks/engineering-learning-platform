# Current state

`ELP-COURSE-CALIBER-00` is the active governance batch. It starts from exact
Engineering Learning Platform baseline
`39aed41de4e3c84fc00c3b8546c5488e253b6be2` (tree
`648c193722e8d356b7520ba064e23e884d25d36c`) and projects Portfolio Control
merge `f6745e44f459a52431b81a3f953c8f2e03cbe45e` without changing course,
runtime, UI, dependency, workflow, or deployment files.

The catalog remains five courses, 134 modules, and 134 interactive modules.
Those counts describe implementation inventory, not curriculum completeness.
The ordered course-caliber states are `source_authored`,
`platform_converted`, `numerically_verified`, `curriculum_covered`,
`capstone_integrated`, and `learner_validated`; every state requires its own
evidence and limitations.

At this audit baseline:

- DSP/Radar is source-authored and platform-converted, but numerical fidelity,
  curriculum coverage, and capstone integration are blocked by the generic
  P02-P84 execution structure. Issue #441 owns remediation.
- Controls/GNC is source-authored and platform-converted, but its fixtures do
  not establish independent numerical evidence. Curriculum and capstone
  coverage are partial. Issues #438 and #439 own repair and expansion.
- Robotics and Autonomy is platform-converted and independently verified at
  the software level. Source authorship, curriculum coverage, and capstone
  integration remain partial. Issue #440 owns expansion.
- No reviewed course has passed `curriculum_covered` or `learner_validated`.

Vehicle Dynamics remains queued and unimplemented. It is blocked until the
course-caliber gate is projected, a reviewed schema-valid competency map
exists, replayable GR86 CAN/BLE fixtures have provenance, and a separate
coherent batch of at most ten lessons is authorized.

The authoritative projection is `docs/course-caliber-status.yaml`. This batch
does not implement #438 through #441 and does not claim MATLAB runtime,
browser/accessibility, learner, physical hardware/HIL, bench, field, release,
deployment, credentials/settings, or production evidence.
