# Robotics aggregate review — work in progress

Owner 2026-11-04: begin from foundations and qualify Robotics to DSP/Controls authored/software rigor. Content-only continuation includes push/merge after verification; Docker delivery remains deferred. No learner, hardware or production claim.

Baseline: target `185e966242c889d3f030bab6016139777fcf0f17`; Control `f274f505a4bb6c99d7fd20ce7eb11e3f9b9697de`. Active batch ELP-ROB-AGGREGATE-QUALITY-01; Control draft PR635. Scope: existing 69 lessons, source pins and other courses preserved.

## Initial audit and implemented work

- Existing P01–P24 lessons already have substantial derivations and independently calculated references. Review them from the beginning; do not replace verified source artifacts or equate inventory with qualification.
- Added 69 individually authored checkpoint prompts with equations, actual two-control sweeps, expected reasoning and scope limits; bound 13 existing cumulative competency portfolios. These still require content/browser review, full numerical replay and provenance reconciliation.
- P51's original nonlinear localization graph uses known fixed landmarks and lacks heading state. Added a separate actual joint planar graph with 3N+6 unknowns (robot x/y/heading plus three unknown landmarks), body odometry/landmark observations, closure and gauge prior, sparse analytic Jacobians, line search and two plots. Original component outputs retained. New integration lesson explains gauge alignment, units, priors, nonlinear iteration, sweeps, failure and scope.
- Independent P51 reference uses complex-coordinate residuals, finite-difference derivatives and trust-region least squares. Nine tests passed (eight size/noise/fault cases and all-column finite perturbations); the first development run exposed a local variable typo, fixed before tests. No broader gate is yet claimed.

## Findings requiring continuation before acceptance

1. P62 labels nine conceptual task states but derives completed-state count directly from endpoint reachability/error. Implement an actual sequence with executed approach, grasp verification, transfer, release, object-state evidence and bounded failure. Preserve the original component study as historical/preflight evidence or reconcile changed values with independent references explicitly.
2. P69 combines visual coordinate transformation/IK, a scalar contact loop and a static friction margin; joint arm dynamics and object placement are not executed together. Extend actual perception → arm dynamics/control → contact/grasp → carried object/placement, with independent full trajectory evidence and computed requirements.
3. P68 executes a valid bounded graph/point-robot perception/freshness/replanning example but has no state estimation, probabilistic map or physical tracking/braking. Its competency-map capstone claims those integrations. Implement them and check actual stage flow; retain original valid bounded component evidence.
4. P67 contains assigned recovery latency constants (20 ms/1000 ms) and does not actually correct clock timestamps in the healthy branch. Replace or supplement with measured event-time recovery and fresh-data source/arrival handling, independently replayed.
5. P59's broken trace ends at zero speed while its terminal-speed error metric equals speed_limit. Reconcile metric and actual trace. Inspect allowed off-grid parameters: a finite lattice may have no terminal-rest state; expose bounded infeasibility rather than uncaught errors.
6. P64 raises when all geometric alternatives are exhausted. Check allowed corners and off-grid inputs and return an explicit bounded infeasible result if required.
7. Audit the remaining models and reference formulations, including P49 mixed-unit information normalization, P50 actual association versus illustrative gate, P53 holdout/covariance and P60 between-sample clearance. Do not close findings merely by renaming them or reducing existing outcomes.

## Remaining qualification work

- Read/review all 69 model/reference/lesson mechanisms; retain concrete per-lesson dispositions.
- Complete missing mechanisms and rigorous integration assessments; improve the 13 portfolios beyond boilerplate where cross-stage evidence requires specific tasks.
- Freshly originate five scenarios per lesson (345) from independent calculations. Source P01–P24 currently retain only baseline/broken JSON; create supplementary sweeps without changing historical artifacts. Preserve tolerances. Add full histories and physical invariants for extensions.
- Reconcile current referenced Markdown digests in `coverage.yaml` and each P01–P24 verification `target` only. Keep source identity, provenance, expected/actual historical files, original source experiments and lesson prose unchanged.
- Update exact plot expectations for extended modules only; add current identity, prerequisite, independence and other-course preservation guards. Prior Controls/DSP historical guard tests must recognize this specifically authorized Robotics batch while continuing to protect all other bytes.
- Implement `verify-robotics-assessments.py`, real host HTTP/browser workflow, all 138 desktop/mobile views, interactions and portfolio/plot captures; inspect rendered math and visuals. Required scoped lint, contract/quick/full run sequentially on frozen inputs; keep exact evidence. No Docker pass inferred.
- Update aggregate maturity only after nine-dimension review and actual checks; push and merge authorized content when complete. Current draft is not accepted.
