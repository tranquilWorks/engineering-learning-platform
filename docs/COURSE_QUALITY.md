# Revised-course quality position — 2026-09-30

All 288 native engineering lessons and two examples are embedded in Engineering
Learning. Nine of the thirteen pinned source repositories remain source-only.
Delivery PR52 is merged: all 290 container HTTP and 580 desktop/mobile page checks
passed. Its historical evidence retains the exact image and screenshot hashes.

| Curriculum | Native lessons | Current content position |
| --- | ---: | --- |
| DSP/Radar | 84 | 84 checkpoints, ten cumulative portfolios and aggregate authored/software review verified |
| Controls/GNC | 68 | P36/P38/P42/P43/P45–P51/P55–P57/P60–P62/P64–P68 repaired within declared models; zero listed findings; aggregate reassessment remains blocked |
| Robotics/Autonomy | 69 | P25–P48, P52 and P68–P69 repaired within declared models; zero listed findings; aggregate reassessment remains blocked |
| Vehicle Dynamics | 67 | P01–P16 and P61–P67 repaired within declared models; zero listed findings; aggregate reassessment remains blocked |

## Final Vehicle powertrain, braking and aero revision

Vehicle P13–P16 now execute delivered-power balance, classified shift decisions, stopping energy/heat and aerodynamic allocation with physical curves and four embedded Course checkpoints. Twenty independent cases, 32 runtime corners and eight selected baked browser pages passed; eight plot captures were inspected. The named register is Controls 0, Robotics 0, Vehicle 0. Final delivery passed 290 HTTP modules, 580 browser pages, 288 checkpoint checks and 174 interactions; all mandatory sequential gates passed. See [batch evidence](evidence/ELP-VEHICLE-DRIVELINE-QUALITY-04-2026-09-30.md). All non-DSP aggregate reviews remain blocked.

## Historical Vehicle foundations revision

Vehicle P01–P12 now display physical response curves, declared units, actual fault/recovery comparisons and twelve authored Course checkpoints. Sixty independent full-mechanism cases, all 96 runtime corners and 24 selected desktop/mobile checks passed; fifteen plot captures were inspected. The P07 steady bicycle model now closes both force and yaw-moment balance. Critical-speed and unstable damping outputs use explicit unavailable semantics.

At the foundations closeout, four named findings remained, all Vehicle P13–P16. All non-DSP aggregate reviews remain blocked. Final delivery and mandatory sequential gates passed: 290 HTTP modules, 580 browser pages, 280 checkpoint checks, 166 interactions and 168 screenshots. See [batch evidence](evidence/ELP-VEHICLE-FOUNDATIONS-QUALITY-12-2026-09-30.md).

## Historical Robotics perception and mapping revision

Robotics P42-P48/P52 now execute known-pose intrinsic calibration, sampled-image
corner descriptors, translation consensus, calibrated stereo rays, local pose fitting
in six degrees of freedom, occupancy ray updates, planar ICP and anchored loop-graph solving.
Eight authored checkpoints, forty independent comparisons, fifty-two focused tests
and sixteen selected browser checks passed. Final delivery verified 290 HTTP modules,
580 desktop/mobile pages, 256 checkpoint checks and 144 real interactions/screenshots.
All mandatory gates passed sequentially; see the [batch evidence](evidence/ELP-ROBOTICS-PERCEPTION-QUALITY-08-2026-09-30.md).

At the Robotics closeout, sixteen named findings remained (Controls 0, Robotics 0, Vehicle 16). All three
non-DSP aggregate reassessments stay blocked; the register is not exhaustive.

## Historical Robotics dynamics revision

Robotics P30-P41 now execute force/torque mapping, point-mass dynamics,
regularized identification, bounded cubic timing, kinematic feedback, computed
torque, operational inertia, contact dynamics, hybrid projection, sampled work
limiting, reaction-wheel swing-up and camera-frame projection. Each includes
an authored browser checkpoint. Sixty independent comparisons, 62 focused
physical/preservation tests and selected desktop/mobile checks passed.

At that revision, the register had 24 findings: Controls 0, Robotics 8 and Vehicle 16.
All non-DSP aggregate reassessments remain blocked. Final delivery passed 290 HTTP modules, 580 desktop/mobile pages, 240 checkpoint checks,
128 real interaction sequences, 21 focused browser tests and all 290 host/baked identities.
Contract, quick and full gates passed sequentially; see the [active batch evidence](evidence/ELP-ROBOTICS-DYNAMICS-QUALITY-12-2026-09-29.md).

## Historical navigation and geometry revision

Controls P56/P57/P60–P62/P64–P65 and Robotics P25–P29 now execute their declared
models and expose twelve individual Course checkpoints. Sixty independent
comparisons and forty-three physical/preservation tests passed, including all 96
control corners through the unchanged runtime. Twenty-four selected
desktop/mobile page and interaction checks passed in the baked preflight.
The default P62 fault is 16 m so its threshold sweep crosses the computed alarm
boundary; thresholds five and ten respectively exclude and retain the row.

This closes twelve scoped findings. At that revision, the register contained 36 findings:
Controls 0, Robotics 20 and Vehicle 16. Controls still requires its separate
aggregate numerical/curriculum/capstone reassessment; this defect register is
not exhaustive. Final delivery passed 290 HTTP modules, 580 desktop/mobile pages,
216 checkpoint checks, 104 real interactions and 21 focused browser tests.
All 290 host/baked module identities match. Contract, quick and full gates passed
sequentially. Exact results are recorded in
[navigation/geometry evidence](evidence/ELP-NAV-GEOMETRY-QUALITY-12-2026-09-29.md).

## Initial twelve-lesson model revision

The initial audit found 72 affected lessons. The current scoped revision replaces
Controls' algebraic capstone surrogates with executed identification/control/filter,
navigation/guidance and timestamped watchdog loops. Robotics now measures
perception/replanning, fresh-data resume and timed contact recovery, including
exact first-contact spring work. Vehicle now has dimensional signatures, physical
force/power envelopes, local travel-time integration, cyclic energy-constrained
laps, unused-point factorial validation, and executed telemetry/vehicle capstones.

Each revised lesson contains its own equations, worked example, concrete
prediction, two sweeps, limits, failure/recovery and checks with rationale.
Capstone requirement tables expose quantities, units, thresholds and verdicts.
Sixty independently generated numerical scenarios and 40 physical/preservation
checks passed. Mandatory local gates and the new container sweep passed: 290 HTTP
modules, 580 desktop/mobile pages and 36 real interactions. The generic renderer
now falls back to SVG after WebGL initialization failure; the twelve repaired
lessons have post-interaction drawn-curve assertions. PR53 records integration. See
[semantic revision](course-quality/semantic-revision.json).

The browser's expanded lesson review identifies exactly what was checked.
This is scoped synthetic-model evidence, not whole-course or learner acceptance.
The additional findings and their scoped closures are retained in the
[additional finding register](course-quality/additional-semantic-findings.md).
No unlisted lesson is automatically certified. Controls, Robotics and Vehicle aggregate numerical, curriculum and capstone stages
remain blocked. DSP passes the separate authored/synthetic aggregate review
described below; learner validation remains not_run.

## Per-lesson evidence

- `course-quality/lesson-audit.json`: all 288 engineering lessons, payload hashes,
  concept headings, candidate equations/checks, control labels/units, declared
  predictions/plots/interpretations, evidence paths, map availability and named
  semantic defects. Presence findings are **not** pass certificates.
- `course-quality/browser-report.json`: actual Chromium desktop/mobile results,
  automated accessibility findings, rendered plots/metrics/math, page errors,
  overflow, representative interactions and screenshot hashes.
- `course-quality/container-report.json`: actual nonroot read-only container,
  every baked default via HTTP, deterministic repeats, digest rejection,
  declared broken-mode recovery, response sizes and deep/static routes.

The browser embeds the lesson-specific content review and known limitations.
Equations render through KaTeX; code/currency remain literal. The renderer
adapts legacy Plotly title strings so authored axis and colorbar units appear. Revision hashes
are in a collapsed technical disclosure. Navigation supports keyboard focus,
and plots expose numeric ranges in addition to the lesson's interpretation and
metrics. Numeric ranges are not a complete nonvisual description of a curve.

## Remaining acceptance boundaries

Automated accessibility checks and named agent screenshot inspection are
separate from manual screen-reader and representative-learner acceptance.
Those human studies have not run. MATLAB runtime, measured vehicle/track,
hardware/HIL, production deployment and the nine source-only conversions are
not claimed. The course inventory is not evidence of curriculum completeness.

Run `./scripts/verify-course-delivery.sh` with Node 22.12 or newer and a
fresh container name/localhost port. It builds the actual image, waits for
readiness, runs browser and HTTP checks, writes the reports and stops its own
container. The report records the image identity; no production service is
modified. Revert this isolated batch to roll back; no schema or data migration.

## Browser-only numeric boundary

Real browser requests exposed a separate platform defect: JavaScript serializes
`240.0` as `240`, while the old menu validator demanded the same Python scalar
type as the declared option. DSP P17–P20 could therefore pass Python HTTP tests
and still fail in the browser. Control amendment PR532 permits the narrow
repair: equal finite numeric spellings resolve to the declared option value;
booleans, strings and undeclared values remain distinct. Numerically duplicate
menu options are rejected at authoring time. No existing course manifest or
public schema shape changes. Regression checks cover the actual browser request.

The verification script installs the Chromium revision selected by the pinned
Playwright package. The host must supply Chromium's operating-system libraries;
this is development verification tooling, not a runtime container dependency.
Numeric alias rejection tightens authoring validation: remove duplicate `1`/`1.0`
choices from an ambiguous manifest. The audit found no such current manifests.

Concurrent-load limitation: six simultaneous lesson pages on the two-CPU container
produced an observed three-second runtime deadline miss in DSP P26, despite its
passing sequential HTTP check. The retained `browser-load-observation.json`
records that failure. The final delivery driver paces actual experiment requests
one at a time while inspecting pages in parallel; it changes neither request
parameters nor server responses or runtime deadlines. Concurrent-user capacity
is not certified by the delivery sweep.

## Verified delivery result

The baked image passed all 290 default HTTP/repeat/recovery checks and all
580 Chromium desktop/mobile page checks, with no serious or critical automatic
accessibility findings. Twelve representative interaction/reset checks passed.
Ten focused browser regressions and nine frontend tests passed. See
[the exact batch evidence](evidence/ELP-COURSE-DELIVERY-QUALITY-01-2026-09-28.md)
for the image identity, all retained artifacts and hosted-CI limitations. Those results did not close the historical 72 semantic findings; the later scoped model revision is recorded above.

The older delivery sweep checked its named DOM assertions; later screenshot review
found unsupported WebGL notices. The semantic revision retains that negative
evidence and the actual rendering correction, including separate legend/axis
spacing and coordinate-preserving fallback. Historical page counts alone did not
establish that every curve was drawn.

Browser recheck boundary: the final all-page invocation exited 1 after one
Robotics P58 mobile request exceeded its unchanged three-second deadline. It
retained 579 initial passes. Three isolated desktop/mobile repetitions on the
same image passed all six checks; the reconciled 580 identities retain the
original failed row and links to every recheck. This is not an initial clean
sweep or concurrent-capacity certification; the timeout cause is not proven.

## DSP aggregate assessment revision

All 84 DSP lessons now have a Course checkpoint navigation link, individual
prediction/evidence task, dimensioned relation, expected reasoning, exact retained
fault/recovery and a model limit. Ten domain endpoints carry four-task cumulative
portfolios and four-criterion rubrics. The map records prerequisites, exclusions
and cross-course handoffs; no learner score or completion is stored.

The fresh independent replay passed 417 retained cases, with 84 content bindings
and ten concrete cumulative metric/plot probes. The final container passed 290
HTTP modules, 580 desktop/mobile pages, 168 checkpoint navigation checks, 20
cumulative blocks and 56 real control/fault/recovery/reset interactions. Every
DSP plot has drawn SVG or image evidence. Exact image: `sha256:53892d096feb4f23c30a7aa9fa2c2f0b25d7ebf3924be7e5d41f971672a39b67`.

This passes authored curriculum and retained synthetic model review. The P84
pulsed chain does not execute the separate array/FMCW/imaging/passive branches,
and selected first-scan controls do not alter its fixed baseline tracking sequence.
The 60 other lesson findings and all human/physical/production acceptance limits
remain. Historical item conversion claims are retained as provenance; current
aggregate browser evidence is recorded separately rather than rewriting them.

## Next twelve Controls model repairs

ELP-GNC-SEMANTIC-QUALITY-12 repairs P36/P38/P42/P43/P45–P51/P55 and adds twelve
individually authored Course checkpoints. These execute state feedback, CARE LQR,
anti-windup, nonlinear dynamics, sampled barrier filtering, gain interpolation,
feedback linearization, sensitivity analysis, constrained MPC, dynamic fitting,
RLS and actual sigma-point transformation. Five independently formulated cases
per lesson retain 1e-8 absolute/relative tolerances. Physical tests check actual
trajectories and all 96 control corners through the unchanged runtime.
See [model and evidence plan](course-quality/gnc-quality-revision-plan.md) and
[numerical record](course-quality/gnc-quality-revision.json). The selected browser
checks passed before closing these findings; final whole-container and mandatory
gate results are recorded in the batch evidence. P55 explicitly teaches the
unscented-transform component rather than claiming recursive UKF implementation.
