# Controls/GNC aggregate completion work — 2026-11-03

Status: implemented first revision, host verification in review; whole-course
acceptance remains blocked. This is not a claim that Controls is finished.
Owner requested Controls at the same depth as DSP. Baseline is PR61,
`abe7c49cea2a649354f20ad19dbe8a2e6c78540a`. The new contract is in Portfolio
Control PR633; neither a draft contract nor authored assessments establish course
acceptance.

## Concrete changes

| Lesson | Repair | Independent evidence |
| --- | --- | --- |
| P37 | Correct normalized first-order state/drive/integral-gain units, preserving legacy control IDs | Piecewise affine saturated servo recurrence |
| P44 | Actual cubic vector field, selected Lyapunov sublevel, boundary derivative and same-input damping-sign fault | Polynomial derivative and factored boundary identity |
| P52 | Actual selected-time covariance propagation, same-input noise-sign fault and unavailable invalid standard deviation | Integrated scalar covariance equation |
| P53 | Executed filter, innovation NIS, posterior truth NEES, actual gate bypass and recovery | Information-form posterior updates |
| P54 | Actual scalar EKF state/Joseph covariance update and nonlinear Taylor residual | Completing the square in the linearized Gaussian likelihood |
| P58 | Actual calibration regressors/information, rank, reciprocal condition and unavailable singular uncertainty | SVD geometry and covariance in the singular basis |
| P59 | Velocity and position paths integrated over the actual selected coast, with prescribed bias correction | Closed-form bias integrals |
| P63 | Nonlinear LOS trajectory and actual heading history; local exponential labeled as an approximation | Implicit separated solution and geometric along-track relation |

Thirteen revised reference entrypoints calculate new inputs instead of returning
stored answers: P34/P35/P37/P39/P40/P41/P44/P52/P53/P54/P58/P59/P63. Historical
unused lookup data remain as history; the revised live functions never read them.
Other reference definitions are preserved. All P01–P24 experiment, source-copied
lesson and independent numerical artifacts remain byte-identical to PR61.

All 68 lessons have individually authored referenced Course checkpoints. The
nineteen earlier checkpoint texts are preserved. Twenty-two cumulative portfolios
contain concrete tasks, linked labs, diagnosis/recovery and four-criterion rubrics.
The competency graph has reciprocal module/assessment bindings, unchanged
prerequisite edges and actual current titles. Referenced Markdown participates in
the real catalog digest. Only source-bound conversion target identities are
reconciled; original conversion provenance and numerical claims are preserved.

## Verified host evidence

- 340 fresh retained independent comparisons through the trusted runtime and
  through the actual HTTP API, retaining original per-module scientific tolerances
  and reference origins. The original GNC comparison uses its global comparison
  scale for the absolute budget plus its elementwise scaled-relative constraint.
- 35 full-mechanism comparisons cover the seven numerical repairs. Discriminating
  physical tests, unretained inputs and all 56 repaired-model control corners are
  in `test_gnc_aggregate_quality.py`.
- 136 desktop/mobile Controls pages, 136 control/fault/recovery/reset sequences,
  136 checkpoint navigations and 44 cumulative-portfolio views passed.
- Strict title/tick/legend geometry initially failed twelve of sixteen revised
  desktop/mobile pages. Those observations and content identities are retained in
  `gnc-aggregate-layout-initial.json`. Shorter titles and legends fixed the actual
  clipping; all sixteen final rechecks passed. Final current identities reconcile
  the unchanged 120 initial rows with these sixteen final rows.
- All eight mobile plot captures were inspected. They show readable curves,
  units, axes and legends. The existing sticky mobile header overlays the top
  section heading in cropped captures; no generic header repair is claimed.
- All 23 existing real-browser regressions passed. Thirteen frontend unit tests,
  frontend typecheck/build and focused lint passed. Existing Plotly bundle-size
  warnings remain.
- The focused revision suite passed 31 tests before the final gap guard was added.
  Exact final contract/quick/full results are recorded in the verification summary,
  with their logs and frozen implementation identities.

The browser is standard Chromium headless-shell 141.0.7390.37. The project's
requested Chromium 153 archive was invalid in this environment. Full Chrome 141
then failed its Unix-socket singleton initialization; normal headless-shell 141
launched successfully. `ELP_CHROMIUM_EXECUTABLE` supports an explicit installed
browser without changing dependency versions. No browser security assertion or
runtime limit was weakened.

The first aggregate verifier attempt incorrectly applied a raw absolute budget
rather than the repository's existing scale-aware GNC comparison definition.
It failed P01's large-energy fault at a 2.33e-9 difference. The verifier now uses
the original comparison definition; original scientific and strict retained
fixture tests remain. Initial schema/link failures, stale covariance/singular
invariants and clipped titles were fixed rather than waived. One early broad
suite was interrupted to finish the implementation. An early host-shell attempt
was edited while running and exited on a shell read offset; the immutable clean
rerun passed all selected browser checks and regressions.

## Remaining finish-line work

`gnc-aggregate-open-gaps.json` retains two genuine course-level findings:

1. Complete recursive nonlinear EKF/UKF predict-update coverage. The existing
   scalar EKF update, unscented transform and scalar RTS smoother are component
   studies; renaming them does not complete the broader outcome.
2. Full strapdown attitude/gravity mechanization and coupled GNSS/INS fusion.
   Frame transforms, one-axis drift/error-state examples, pseudorange solving and
   planar position aiding do not constitute that complete integration.

The three capstones are now described exactly: scalar identification/control/
estimation stress; planar position-aided LOS survey with freshness/turn checks;
and software packet/watchdog HIL. No capstone claims to integrate absent stages.
Broader scope must be implemented and independently verified, or explicitly
reconsidered by the owner; these gaps cannot silently disappear from acceptance.

Docker is not installed in this execution environment. The required final
read-only nonroot baked-container build/HTTP/browser gate is **not run**. Host
HTTP/browser evidence does not replace it. Full private Portfolio Control checkout
validation is also not available here, so its contract stays draft; JSON Schema
validation of the new contract passed. Hosted CI is separate and is not inferred
from local success. No workflow, protection or billing setting changed.

Controls aggregate numerical/curriculum/capstone maturity remains blocked. DSP,
Robotics and Vehicle dispositions, all thirteen source pins, all other course
payloads and the 68/290 inventory remain unchanged. No representative-learner,
manual screen-reader, MATLAB, hardware, concurrent-capacity, production or release
acceptance is claimed.

Rollback is a revert of this isolated revision to PR61. There is no schema or
learner-data migration.
