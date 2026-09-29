# Twelve Controls/GNC quality repairs

Status: implementation and all required local numerical, browser/container and
repository gates passed. The development PR is the authoritative merge record.

## Authorization and exact boundary

- Target baseline: PR54 merge `00983cab0599b1ce3a613a2cc8ef42eb7b45f0b4`, tree
  `49b73ca015e87a862e79f98e15f13f5c6fb66150`.
- Control contract: [Portfolio Control PR551](https://github.com/tranquilWorks/portfolio-control/pull/551),
  merged at `6d81736bba58cc05f6ccc78e4a3ad66386d731bb`.
- Existing owner continuation authorizes roughly twelve existing lessons per group
  and normal verified development merges. No production action is authorized here.
- Exactly Controls P36/P38/P42/P43/P45–P51/P55 are revised. All 290 module identities,
  thirteen source pins, prerequisite edges, DSP assessments/numerics and unrelated
  Controls/Robotics/Vehicle payloads are preserved. No new course conversion.

## Changed behavior and teaching

See the [lesson-by-lesson mechanism/reference table](../course-quality/gnc-quality-revision-plan.md).
Each lesson now has an executed model, dimensioned plots and metrics, worked
example, prediction, two sweeps, failure/recovery, limiting cases, answer rationale
and a portable Course checkpoint. The new models perform actual state propagation,
CARE, anti-windup, nonlinear integration, state-dependent filtering, gain-table
interpolation, transfer-function analysis, constrained optimization, identification,
recursive estimation and sigma-point transformation.

P42 explicitly censors recovery that is not observed. P47 reports a terminal
x=10 departure event instead of pretending it reached the four-second horizon.
P48 reports a sampled finite-band sensitivity peak, not an H-infinity certificate
for unstable systems. P55's stable route is retained but its title now says
**Transform Gaussian Uncertainty with Sigma Points**: no recursive UKF is claimed.
Negative central mean weights are distinguished from covariance-weight correction.
P38 exposes normalized cost-derived feedback gains. P48 frequency and P51 covariance
use logarithmic axes to keep meaningful behavior visible over their wide ranges.

## Independent and physical evidence

[Sixty independently formulated comparisons](../course-quality/gnc-quality-revision.json)
cover baseline, two one-variable sweeps, fault and recovery for every lesson.
Absolute and relative tolerances remain 1e-8. The largest observed absolute
signature difference is 1.4231504863460032e-11 (P43). Expected artifacts are generated
from reference functions; production results are never their inputs.

The dedicated physical/preservation suite has 46 tests, including all 96 control
corners through the unchanged three-second runtime. Tests check full feedback
acceleration, CARE and actual plant/observer histories, integral-state recurrence,
energy/work balance, every barrier step, interpolation knots and refinement,
nonlinear event time, true transfer magnitude, whole-plan MPC feasibility/objective/
KKT behavior, held-out free-run recurrence, weighted batch/RLS agreement and
sigma-point moments. They preserve every unselected reference function, origin
and all five outputs against the exact PR54 baseline.

Historical PR53 and DSP aggregate scope guards now compare their own exact merged
batch trees. Their numerical and physical assertions remain. The new guard checks
the current PR54 successor, so prior assertions do not incorrectly prohibit this
separately authorized Controls batch.

## Verification record

- Control-plane contract validation passed: 306 tests across 252/6/33/15 suites,
  with one existing uninitialized GitG source-inventory skip. Portfolio/schema and
  shell checks passed. Hosted control check 109265012321 never started because
  GitHub reported failed recent payments or a spending-limit restriction. No
  account/workflow/protection setting changed.
- Final local numerical verifier: 60 independent comparisons and 46 physical/
  preservation tests passed in 25.54 seconds for the test portion.
- Selected preflight: 18 focused browser tests passed; all 136 Controls desktop/
  mobile pages and 32 interaction sequences passed. The twelve newly revised
  lessons account for 24 visible checkpoint checks and 24 control/fault/recovery/
  reset sequences. See [retained pre-closure evidence](../course-quality/gnc-selected-browser-evidence.json).
  P38 gain visibility and P48/P51 logarithmic presentation were added after this
  preflight image; the final whole-platform image below contains those refinements.
- Final verified image: `sha256:04e381f3626292f390fcd0ba76fe4ad5cfe305507a89e2e65174ae4b36851646`.
  Read-only nonroot container `elp-gnc-quality-12`, localhost port 8772, 2 CPUs,
  2 GiB, read-only baked courses and bounded temporary filesystem.
- Final delivery passed: 18 focused browser tests; 290 HTTP modules; 580 desktop/
  mobile pages; 192 checkpoint checks (168 DSP and 24 Controls); twenty cumulative
  DSP blocks; eighty real control/fault/recovery/reset sequences; eighty retained
  screenshots. All final page rows passed in the same complete invocation.
- Sixty independent comparisons passed again against the actual baked HTTP
  runtime, with selected module content identities checked before execution. All
  290 canonical host module content digests also match the final baked container.
- Mandatory gates ran sequentially after browser work, with no overlapping heavy
  verification. Results:
  - `./scripts/agent-verify.sh contract`: 103 passed in 94.19s (0:01:34); exit 0, 95.58s overall.
  - `./scripts/agent-verify.sh quick`: 1377 passed, 3 warnings in 1377.88s (0:22:57); exit 0, 1379.64s overall.
  - `./scripts/agent-verify.sh full`: 1377 passed, 3 warnings in 1308.66s (0:21:48); exit 0, 1374.17s overall.

The ten frontend unit tests, typecheck and production build also passed. The
three backend warnings concern existing Starlette/httpx and FastAPI response
deprecations; the build retains the existing large Plotly chunk warning. No
dependency or warning threshold changed.

Commands are retained in `contracts/verification.yaml`. Actual reports are
[container-report.json](../course-quality/container-report.json),
[browser-report.json](../course-quality/browser-report.json), and the separate
[independent HTTP replay record](../course-quality/gnc-container-numerical.json).
See also [gate summary](../course-quality/gnc-verification-summary.json) and
[all-module content binding](../course-quality/gnc-container-content-binding.json).
The completed full browser sweep covers all 290 HTTP modules, 580 desktop/mobile pages,
168 retained DSP plus 24 new Controls checkpoint checks, twenty cumulative DSP
blocks, eighty interaction sequences and drawn traces after recovery/reset.

## Review observations and failed attempts

Initial test authoring incorrectly treated a typed PlotSpec as a dictionary and
required an exact zero for a roundoff-sized bumpless residual; both checks were
corrected without changing numerical evidence tolerances. One intermediate run
was invalidated by formatting source files while the catalog retained their
hashes, correctly triggering revision rejection; a temporary work-variable rename
was also corrected before the final numerical run. Subsequent checks use fixed
course files during verification.

The old phase-portrait test ranked distance to a well at one terminal instant.
The executed oscillator disproved that premise: a negative-damping trajectory can
pass near a well while gaining energy. The replacement checks signed energy
change and local stability, while physical tests independently verify its actual
vector field and work balance. No solver/runtime timeout or tolerance was enlarged.

Mobile inspection of P38/P43/P49/P55 confirmed readable controls, equations,
units, real plotted curves, interpretations and checkpoints. Desktop P36/P51
inspection identified the covariance-scale improvement included in the final image.
Final desktop/mobile P38/P48/P51 inspections also confirmed visible LQR gains,
readable logarithmic frequency/covariance curves, units and checkpoint content.
Full-page screenshot fixed navigation positions are capture artifacts; final
navigation assertions separately test the real heading in the viewport.

## Remaining scope and rollback

The original findings remain in history. These twelve scoped closures leave
**48 open findings: Controls 7, Robotics 25, Vehicle 16**. All three course-wide
numerical/curriculum/capstone reviews remain blocked. DSP's earlier authored and
synthetic review is preserved. No unlisted lesson is certified merely by passing
a structural or delivery check.

No representative-learner study, manual screen-reader review, MATLAB execution,
measured hardware, production deployment or concurrent-user capacity is claimed.
The prior broader visual note about some long titles in narrow canvases remains;
full plot names are available in numeric-range summaries.

Rollback is a revert of this isolated batch to PR54, preserving the original
finding history. No schema, persisted learner data or migration changed. The
prior verified DSP preview at port 8771 remains separately available.

A final content review found that P45's fault explanation needed an explicit
finite-window condition: at the slowest closing speed the unfiltered trajectory
remains positive for three seconds. The numerical model already produced that
result. The first final-image sweep was stopped after 76 passing pages (all 290
HTTP checks had passed), the lesson/callout/checkpoint wording was corrected, and
an inactive-filter/slow-closing comparison was added. A fresh final image and
complete sweep replace that intermediate candidate; no failed safety result is
hidden or relabeled. The original attempt remains in local verification logs.

After all 580 final browser pages passed, the independent HTTP verifier hit a
connection reset on its initial catalog-readiness request immediately after the
preview restarted. The existing bounded startup retry now includes that specific
transport exception. No experiment request is retried or suppressed, and the
original startup-reset log is retained. The replay and mandatory gates follow
only after the catalog is ready; lesson payloads and the verified image are unchanged.

The image was built from the reviewed working tree on the exact PR54 baseline.
The content-binding report verifies all 290 canonical course payloads against that
bake; later evidence/documentation commits do not claim a new runtime build.
