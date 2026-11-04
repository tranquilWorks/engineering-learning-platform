# Controls recursive-estimation and navigation closeout

Continuation of ELP-GNC-AGGREGATE-QUALITY-01 from PR63 commit
`a9dcf2761d04a14e62da20203d14e2c395fb6184`.
The owner requested continuation to DSP's authored/software rigor on 2026-11-03.
This is implementation and review evidence, not learner or physical qualification.

## Scope and executed changes

| Existing lesson | Added mechanism | Independent formulation |
| --- | --- | --- |
| P54 | 80-step nonlinear EKF prediction, process covariance, Joseph measurement update and feedback | Scalar information conditioning |
| P55 | 80-step UKF with propagated sigma points, additive process noise, re-sampling, cross covariance and correction | Symmetric sums and analytic quadratic measurement moments |
| P59 | Full local ENU attitude/velocity/position mechanization with quaternion increments, midpoint force rotation and gravity | DCM propagation with SciPy Rotation; tilted stationary and rotated-force limits |
| P61 | Fifteen-state loosely coupled GNSS/INS error dynamics, pseudorange-derived fixes, bias correction, injection and right-attitude reset | Information-form conditioning, separate normal-equation GNSS solver and linear-operator transition |
| P67 | The same mechanization/fusion inside estimate-driven LOS survey, finite-acceleration braking, turn limits and outage monitoring | Independent DCM-based full mission-segment history and covariance |

No lesson is added. The 68 Controls identities, original outcomes/prerequisite
edges, source-bound P01–P24 numerical artifacts, thirteen source pins, and other
course payloads remain unchanged. The original component calculations remain
visible and their signatures/tolerances are preserved. New sequences have
separate histories, plot keys, tables, tests and declared numerical budgets.

The navigation kernel is embedded identically in three portable entrypoints.
The existing catalog hashes the entrypoint and referenced Markdown, but does not
hash arbitrary helper imports. A synchronized AST test prevents drift between
these copies without changing the generic runtime or weakening content identity.

## Nine review dimensions

1. Foundations/prerequisites: original graph and mathematical outcomes remain;
   component studies precede complete recursive/integrated sequences.
2. Breadth/sequencing: no breadth quota or inventory expansion; the two explicit
   algorithm gaps are addressed within existing mapped lessons.
3. Derivation/physical meaning: each new integration section defines equations,
   dimensions, frame direction, assumptions, and a worked limiting check.
4. Executable fidelity: actual state/covariance feedback is retained at every
   sample; complete navigation includes attitude, gravity, both IMU bias vectors,
   a GNSS position solve, injection and coordinate reset.
5. Sweeps/limits/failure/recovery: existing controls drive each added model;
   corner/off-grid inputs, poor priors, outages, positive covariance, quaternion
   norm, turn constraints and deterministic recovery have explicit checks.
6. Independent evidence: no reference imports production or consumes its output;
   compare full trajectories and every covariance matrix, not only a terminal
   three-number signature. Existing tolerances are unchanged.
7. Assessment: the 68 checkpoints and 22 portfolios remain; five distinct
   integrated assessments and visible numerical evidence tables extend the
   relevant tasks. No learner completion is inferred.
8. Capstones: P67's new fused estimate actually feeds guidance. The separate
   computed requirement table can fail at restrictive turn settings; it does not
   declare full-route completion. P66/P68 retain their reviewed boundaries.
9. Exclusions/handoffs: local flat-Earth navigation, known gravity and bounded
   synthetic forcing; no Earth rotation/ellipsoid, coning/sculling beyond midpoint
   approximation, receiver multipath, measured IMU validation, statistical
   coverage certification, hardware or production claims.

## Verification and budgets

- Preserve all 340 original five-scenario comparisons and 35 component mechanisms.
- Add 25 integrated full-history comparisons: five scenarios each for P54, P55,
  P59, P61 and P67; scalar absolute/relative budget 2e-10 and navigation 2e-7.
- Navigation covariance uses mixed-coordinate units. Relative tolerance covers
  large unaided covariance at 120 s; the absolute budget also covers near-zero
  angular differences from the matrix/quaternion representations. Quaternion
  sign is aligned before comparison because q and -q denote the same rotation.
- A separate finite perturbation and step-halving test checks the second-order
  transition against nominal mechanization. Stationary tilted gravity and a
  90-degree force rotation independently check signs/frame direction.
- Native HTTP/default limits are preserved: no larger timeout, payload allowance,
  weaker browser assertion or disabled security condition.
- Required contract, quick, full, frontend, browser and baked delivery commands
  retain distinct outcomes. The final summary records actual process exit codes.

## Observed corrections during development

The first new test run passed 28/30. Two assertions wrongly demanded small
whole-run RMSE even for a severely overconfident wrong prior. Those tests now
check the large early transient and eventual convergence, while independent
numeric agreement budgets remain unchanged. The revised 30 tests passed.

The first focused shared run passed 138/139: an older capstone assertion assumed
exactly three metrics. Its correction explicitly checks the new navigation error
metric's ID/unit and retains all original signature dimensions. The native plot
contract now names the exact additional plots only for the five extended lessons.

The first HTTP replay passed all 340+35+25 comparisons. The selected browser
review exposed malformed multiline display-math delimiters in P54/P55/P59;
those were fixed and all five new Markdown sections parsed without KaTeX errors.
The failed browser rows and identities remain in gnc-recursive-browser-selected.json.

The selected recheck passed all 22 desktop/mobile views. Its regression suite
passed 22/23: the P55 test still expected the old title and two plots. It now
checks the new title/four plots, locates the original checkpoint explicitly, and
also verifies recursive gain suppression and recovery. Existing component moment
assertions remain unchanged. An earlier local replay interrupted by input edits
is not counted as a pass; subsequent runs use stable lesson files.

A broad exploratory lint command traversed pinned source repositories and old
unrelated course code. It is not a passed gate. The required scoped lint exposed
two pre-existing long lines in the historical Vehicle test guard, corrected by
formatting without changing its assertions. Required scoped lint and all newly
implemented files are checked separately.

## Remaining delivery boundary

The baked-delivery script now selects the Controls image, HTTP verifier and
browser reports. It still requires a real read-only nonroot Docker run. In this
environment Docker CLI/daemon/socket are absent; the attempt exited 2 with an
explicit blocker. A host process is not evidence of a baked-container run.
Neither broad course acceptance nor merge readiness can be inferred from host
success. Learner and manual screen-reader validation remain not_run, as in DSP's
separate authored/software disposition.

## Owner content-only acceptance

Owner 2026-11-03: content-only completion at DSP authored/software rigor; Docker delivery is deferred and does not block this content acceptance or the explicitly authorized push and merge. No container, learner, hardware or production pass is inferred. The earlier Docker merge blocker above is superseded for content acceptance; its not_run result remains unchanged.
