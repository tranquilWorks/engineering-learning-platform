# Handoff

The course-caliber governance projection is complete at control revision
`f6745e44f459a52431b81a3f953c8f2e03cbe45e` and target audit baseline
`39aed41de4e3c84fc00c3b8546c5488e253b6be2`.

Future course work must start from `docs/course-caliber-status.yaml` and obey
these boundaries:

1. Do not use source, platform, authored, interactive, or `P##` counts as a
   curriculum-completeness claim.
2. Require a reviewed schema-valid competency-to-module matrix before a new
   conversion or expansion. Derive the module count from that matrix.
3. Authorize only the smallest coherent batch, with no more than ten new
   lessons.
4. Run the semantic anti-template review across governing relations, state,
   controls, transformations, outputs, failures, and reference methods.
5. Reject an independent-evidence claim when its fixture imports the
   production entrypoint, derives from production output, or perturbs
   production output.
6. Preserve separate evidence and limitations for all six maturity states and
   all nine rubric dimensions.

Owned next work remains deliberately separate: #438 repairs Controls/GNC
fidelity and evidence, #439 expands Controls/GNC against a reviewed competency
map, #440 expands Robotics and adds integrated assessment/capstone work, and
#441 replaces the generic DSP/Radar implementation structure.

Vehicle Dynamics remains blocked and unimplemented. Release the hold only when
its reviewed competency map validates, replayable GR86 CAN/BLE fixtures and
provenance are available, and Portfolio Control separately authorizes a
coherent batch of at most ten lessons.

Verification commands are listed in `contracts/verification.yaml`; retained
results are in `docs/evidence/ELP-COURSE-CALIBER-00-2026-09-21.md`. Roll back
this governance projection by reverting its single target merge. No course or
source history needs rewriting.
