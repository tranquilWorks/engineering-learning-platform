# ELP-ROB-MANIPULATION-P61-P65 evidence — 2026-09-23

## Authorized boundary

- Portfolio Control contract: `products/engineering-learning-platform/batches/ELP-ROB-MANIPULATION-P61-P65.yaml`
- Control merge: `d018fa3cacce804246420224c731a4e1b267ceea`
- Exact target baseline: `b84f5b29f5b842584439209e41f79655bbde8d19`
- Exact baseline tree: `99cd3b2ef13a39639f05eead017c9e52dd209eeb`
- Pinned source gitlink: `f8807640258f1a6c1c77f1dcc9e61734551c585b`
- Implemented scope: P61, P62, P63, P64, and P65 only.

## Per-item review

| Item | Executable model | Named invariant and failure | Physical signature |
|---|---|---|---|
| P61 | Planar friction-cone grasp map, positive null-space equilibrium, and projected nonnegative external-load solve | Full grasp-map rank is force closure only with a strictly positive equilibrium; broken mode reverses one contact normal | closure margin (1), equivalent load residual (N), contact effort (N) |
| P62 | Calibrated camera-to-base transform, analytic two-link IK, forward check, and nine-state pick/place gate | Lift requires a consistent transformed pose, reachability, and physical pickup tolerance; broken mode treats camera coordinates as base coordinates | pickup error (m), reach margin (m), completed states (count) |
| P63 | Bounded base-placement search paired with analytic arm IK, manipulability scoring, and synchronized execution | The world-frame endpoint must use the same base/joint pair selected by the composite search; broken mode freezes the base and clips reach | endpoint error (m), manipulability (m^2), base travel (m) |
| P64 | Uniform-cost task graph with predicted motion predicates, execution clearance monitor, failed-edge blacklist, and bounded recovery | A failed carry may precede success only after the edge is excluded and search resumes from the last certified state; broken mode abandons recovery | task success (1), replans (count), task time (s) |
| P65 | Time-expanded A-star against terminally extended vertex, opposing-edge, and temporal-buffer reservations | The joint schedule must contain neither vertex occupancy conflicts nor opposing edge swaps; broken mode plans independent shortest paths | conflicts (count), makespan (step), minimum separation (cell) |

All five modules retain a baseline, two one-variable sweeps, an intentionally broken scenario, exact recovery, at least two limiting cases, domain-specific axes and units, bounded deterministic execution, and a unique learner lesson. Lesson word counts are P61 1,326; P62 1,288; P63 1,294; P64 1,311; and P65 1,258.

## Independent numerical evidence

`courses/robotics-autonomy/expansion_reference_cases.py` independently reconstructs all five algorithms. It imports no production experiment, consumes no production result, and perturbs no production value. For each item, retained `expected-independent.json` and `actual-production.json` records cover baseline, sweep 1, sweep 2, broken, and recovery inputs and signatures. All 25 independent/production comparisons agree within absolute and relative tolerances of `1e-8`.

## Local verification

- Robotics focused/framework/course/status: **107 passed**.
- DSP/Radar regression: **300 passed**.
- Controls/GNC regression: **118 passed**.
- Contract suite: **72 passed**.
- Quick suite: **601 passed**, with four pre-existing dependency deprecation warnings.
- Full suite: **601 passed**, with the same four warnings.
- Deterministic catalog: **pass**, 5 courses / 219 modules / 219 interactive; deterministic execution checked.
- TypeScript typecheck and Vite production build: **passed** as part of the full gate.
- Ruff over Robotics source and focused tests: **passed**.
- `git diff --check`: **passed**.
- Forbidden-course/source scope and the Robotics source gitlink remained unchanged.

## Claim boundary and residual risk

This batch establishes deterministic software-only evidence for P61-P65 and advances Robotics to 65 implemented interactive modules. P66-P69 remain separately authorized work: robot interfaces, timed replay and diagnostics, and two cumulative capstones. MATLAB runtime comparison, browser/accessibility review, learner validation, physical HIL/hardware, timing on deployed robots, safety certification, release, deployment, credentials/settings, and production use remain explicitly unperformed.
