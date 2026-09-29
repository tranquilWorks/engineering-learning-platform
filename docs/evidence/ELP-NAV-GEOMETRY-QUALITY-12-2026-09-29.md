# Navigation and geometry quality revision — verified development delivery

Authorized scope: existing Controls P56/P57/P60–P62/P64–P65 and Robotics P25–P29, twelve lessons. Control contract [PR559](https://github.com/tranquilWorks/portfolio-control/pull/559) merged at `15f2c1537b2be9710143d03ffbc182574de51376`. Target base is exact PR55 merge `8820f21d349836b63db00f1e596f5eb00b488ab9`, tree `c30d90aa2dacdf7ceecad518efca787fb3f51f73`.

The twelve modules retain their identities and controls. The revised mechanisms execute filtering/smoothing, quaternion composition, pseudorange fitting, one-axis error-state injection, measurement exclusion, civilian guidance trajectories, bounded terminal optimization, constraint projection, rigid transforms, dual wrench transforms, a planar position Jacobian and null-space velocity projection. Scope labels narrow the claims to those calculations. No schema, runtime limit, generic platform component, source pin, DSP or Vehicle payload changed.

Each lesson has a worked example, prediction, two sweeps, a named executed fault, recovery, limits and an embedded Course checkpoint with answer rationale. Expected scenario artifacts come solely from independent references; actual artifacts come separately from production. Absolute/relative tolerance remains 1e-8. Historical PR55 scope guards compare their original merged trees, while their physical checks continue testing live code. New preservation checks compare this batch to exact PR55.

## Executed mechanisms and independent checks

| Lesson | Executed model | Independent formulation and key limit |
| --- | --- | --- |
| Controls P56 | Forward scalar Kalman filter and retained backward RTS recursion | Joint Gaussian conditioning; final filter/smoother equality and positive covariance. |
| Controls P57 | Hamilton quaternion composition, normalization, matrices and sensor vectors | Rotation-vector matrices and scaled-quaternion identity; zero-angle norm-fault limit. |
| Controls P60 | Eight synthetic pseudoranges fitted for position and clock | Complex-step nonlinear least squares; residual stationarity and clock omission. |
| Controls P61 | One-axis position/velocity/bias propagation, Joseph update, injection and reset | Equivalent full-state filter with quadrature process covariance; withheld-injection drift. |
| Controls P62 | Leverage-standardized residual alarm, actual row removal and refit | SVD leverage and independent nonlinear fit; zero-fault and threshold-crossing cases. |
| Controls P64 | Civilian pursuit, PN and declared feed-forward trajectories | Independently integrated relative-polar PN equations; capture event and sampled minimum boundaries. |
| Controls P65 | Bounded twenty-input terminal objective and propagated double integrator | Two-dimensional clipped dual equation; command bounds, dynamics and projected KKT residual. |
| Robotics P25 | Circle constraint/Jacobian, actual configuration and velocity projections | Polar geometry and tangent-basis velocity; zero-offset fault and sampled clearance. |
| Robotics P26 | Homogeneous transforms, composition order and rigid inverse | Scalar coordinate composition and analytic blend defect; valid endpoints with invalid interior. |
| Robotics P27 | Adjoint twist and inverse-transpose dual wrench transformation | Separate rotated components/cross products; power and dimensionally separate round trips. |
| Robotics P28 | Two-link planar position Jacobian, SVD and central differences | Complex-step kinematics and Gram eigenvalues; true alignment singularity versus omitted column. |
| Robotics P29 | Damped primary task inverse plus exact null-space posture projection | Complex-step Jacobian, SVD inverse and cross-product null basis; zero gain/damping limits. |

Every comparison uses the retained 1e-8 absolute/relative tolerances. P64's closest distance is sampled and its one-metre capture event is explicit. P61 implements an additive one-axis model; P28 implements a position task; P29 is instantaneous. These limits are embedded in the lessons and checkpoints.

## Verification evidence

- Control contract validation: 306 tests, one existing GitG skip, portfolio and shell validation passed.
- Initial direct numerical probe: sixty independent scenario comparisons and ninety-six control corners passed; maximum measured model execution in that probe was 0.126 seconds with one BLAS thread.
- Forty new physical/preservation tests passed, including the ninety-six runtime corner cases under unchanged three-second limits.
- Frontend typecheck, build and ten web tests passed. Existing chunk-size and Node experimental-feature warnings remain.
- Thirty Controls/Robotics expansion regressions passed. The local verifier passed sixty comparisons and forty tests; after the threshold example adjustment it passed again (40 tests in 50.05 seconds). A final direct sixty-case/ninety-six-corner probe also passed after equation-unit clarification.
- Selected baked browser preflight passed 24 desktop/mobile pages and 24 control/fault/recovery/reset sequences, with checkpoint navigation and drawn plots. The twelve selected findings are closed within this evidence boundary. Seventeen historical preservation/status checks passed.
- Final complete delivery and the mandatory sequential gates passed; exact results follow below.

## Failed attempts and corrections

An early runtime run rejected payloads edited after catalog loading (seven failures, fifteen passes before interruption). The payloads were frozen before restarting. A new test then incorrectly indexed a typed PlotSpec as a dictionary; the test now uses the public JSON serialization before inspecting traces. The physical suite passed after that correction. Broader schema validation required multiple limiting-case entries instead of one paragraph; the existing lesson-specific limits were split into separate entries without weakening the schema. A mistyped targeted test selector collected no tests; the actual expansion suites were then invoked.

## Hosted evidence is separate

Control PR559 hosted check `109443815948` did not start because the GitHub annotation reported failed account payments or a spending limit. Local validation passed; hosted CI remains nonmandatory under retained owner direction. No account or workflow configuration was changed.

Prior target PR55's backend run subsequently completed with 75 failed, 1288 passed and 14 errors: its hosted checkout lacks pinned source content and historical Git objects required by those tests. Frontend passed; container CI was skipped. These failures are retained separately from PR55's passed local gates and container evidence. This batch does not claim that previous hosted run was green.

## Acceptance boundary and rollback

After selected numerical/browser closure the register is 36 findings: Controls 0, Robotics 20 and Vehicle 16. All three non-DSP aggregate numerical, curriculum and capstone reassessments remain blocked; zero listed Controls findings is not exhaustive acceptance. Representative learners, manual screen-reader testing, MATLAB execution, hardware and production evidence remain not_run.

Rollback is a revert to the exact PR55 baseline; there is no schema or persisted-data migration. Earlier localhost previews remain untouched. The verified final development preview is running on port 8773.

## Additional review corrections and retries

The initial browser preflight passed eight desktop lessons before Chromium crashed. Host storage was nearly full (110 MB available); no lesson assertion failed in those eight rows. Unreferenced ELP build images and stopped disposable ELP review containers were removed after their logs/metadata were archived. All running earlier previews were preserved, and available storage recovered to about 5 GB. The next preflight passed all 24 selected pages.

P62 now defaults to a 16 m injected fault so the threshold sweep crosses its actual statistic of 9.5158558: threshold five excludes the suspect, while threshold ten retains all rows. The new regression checks both decisions. No fixed alarm or residual reduction was substituted.

Agent screenshot review corrected R27's normal power-axis magnification of machine roundoff without changing plotted data, and gave R29's mobile task-velocity legend two columns with explicit axis spacing. Corrected plots were inspected in a rebuilt image; six representative captures and exact image identity are retained in navigation-geometry-visual-review.json.

The first complete-delivery attempt passed nineteen focused browser tests and failed one stale expectation that repaired R26 should still be Under revision. The test now verifies that warning on unresolved R30 and checks R26's scoped review and whole-course boundary. The next attempt passed all twenty browser tests and all 290 HTTP modules; its page sweep was intentionally stopped when final equation review found implicit unit-bearing constants. C64 now explicitly shows beacon speed in the augmented acceleration and speed/heading gain in pursuit; R28 explicitly shows the one-metre proximal link in forward kinematics. Numerical probes passed again and complete baked verification restarted. Partial logs are retained rather than reported as full acceptance.

Zero-span review added visible point markers for C57 yaw zero, R28 elbow span zero and R29 posture gain zero, preserving the actual coordinates. The focused suite now passes 43 tests (46.13 seconds) plus sixty independent comparisons. A dedicated real-browser check passed all three settings via slider keyboard controls (one test, 5.9 seconds). Its first attempt used a number-input selector, but these controls are sliders; the selector was corrected to keyboard range interaction without changing the UI or runtime. The full page sweep was restarted to cover the final source identity.

## Final frozen-input delivery and gates

The final read-only nonroot image is `sha256:65d1de31cc56d2d3ca053ac3bdcfe0b1dae39497637dca3b4bb9b31542a1f9ee`, served at `http://127.0.0.1:8773`. All 106 frozen implementation/test/contract input hashes remained unchanged throughout final verification. The retained [verification summary](../course-quality/navigation-geometry-verification-summary.json) binds those hashes, image identity, report counts and gate-log hashes.

- 21 focused real-browser tests passed, including actual zero-span points via keyboard controls.
- 290 container HTTP module checks and all 290 canonical host/baked content identities passed.
- 580 desktop/mobile page checks, 216 checkpoint checks, twenty cumulative DSP checks, 104 control/fault/recovery/reset sequences and 104 screenshot hash checks passed.
- Sixty independent scenario comparisons passed locally and sixty through baked HTTP, at unchanged 1e-8 absolute/relative tolerances. The focused 43-test suite covers physical behavior, preservation and 96 runtime control corners under the unchanged three-second limit.
- Mandatory local gates passed in sequence: contract: 103 tests in 100.15 seconds; quick: 1420 tests in 1424.59 seconds; full: 1420 tests in 1324.75 seconds. Quick/full include the full backend suite; full also checks deterministic course execution, frontend typecheck and production build. Existing warnings are retained in the gate summaries.
- Six additional representative plot-grid captures were inspected by the agent; their separate review-image identity is retained in navigation-geometry-visual-review.json. These supplement automated accessibility checks and do not claim manual screen-reader or learner validation.

Development integration is recorded by this change's pull request; the subsequent Portfolio Control closeout binds its exact merged commit. Hosted checks remain separately reported in the PR and control record, without inferring a pass from local results.
