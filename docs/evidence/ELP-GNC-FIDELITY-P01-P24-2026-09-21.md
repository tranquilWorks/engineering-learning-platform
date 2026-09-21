# ELP-GNC-FIDELITY-P01-P24 evidence — 2026-09-21

## Outcome

Controls/GNC P01-P24 are source-mapped and numerically verified at a deterministic software-only boundary. The course retains 24 source items, 24 platform modules, and 24 interactive modules; those counts are implementation inventory, not curriculum completeness.

- Target baseline: `1506591946ec8e96fe3201e8893b8ad851a1685a` (tree `cff72df08f1c37655e912ca1c24f90e27222f6e3`).
- Merged control authorization: `0038f6ed725ae2fc7b3eb6647e9621a2ad23db34` (Portfolio Control PR #443).
- Source pin: `ffd6623ee2cf8ccd8599fffd935ef07370750fa3`, tree `471a0afead6f44e875627e7ffe9c088c23f784db`.
- Source curriculum SHA-256: `8763981e20d02a88450956682b4daff9ee0d74bfed5f0ad91b08715f16aea930`.
- Catalog after remediation: 5 courses / 134 modules / 134 interactive modules.
- Target implementation PR, commit, and merge identities are recorded in the #438 closure comment after merge; they cannot be embedded in the commit that identifies itself.

## Evidence design

`fidelity-map.yaml` binds every item to the exact source `model.m` hash and records controls, governing relations, observables, two one-variable sweeps, broken/recovery behavior, limiting cases, explicit omissions, reference method, and plot axes. `reference_cases.py` imports no production experiment, accepts no production result, derives no value from production output, and perturbs no production value.

Each item retains exactly two evidence files. `expected-independent.json` is generated from the independent reference package; `actual-production.json` directly captures `experiment.py:run`. Both files contain baseline, sweep 1, sweep 2, broken, and recovery parameters and signatures, with ordered field names and units. A case passes only when its maximum relative error is within the declared relative tolerance and its maximum absolute error is within `max(absolute_floor, relative_tolerance × comparison_scale)`; both the independent and production signatures must also pass the named teaching invariant.

The 96 former expected/actual baseline/broken fixtures were removed because their approximately `1e-13` first-leaf differences did not establish independent origin.

## P01-P24 review rows

| Item | Independent formulation | Scenarios | Max abs error | Max rel error | Abs / rel tolerance | Invariant | Plot axes | Explicit omission boundary |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| P01 | Affine semi-implicit state-transition recurrence | 5/5 | 2.33e-09 | 7.18e-16 | 1e-10 / 1e-10 | pass | response: Time (s), Position (m); mechanism: Position (m), Velocity (m/s), Time (s), Mechanical energy (J) | The platform fixes force, horizon, normal dt, and source resource diagnostics so the three learner levers isolate m, c, and k. |
| P02 | Analytic integrator/first-order response and Euler recurrence formula | 5/5 | 0 | 0 | 1e-10 / 1e-10 | pass | response: Time (s), Normalized response (ratio); mechanism: Time (s), Normalized signal (ratio) | The platform fixes horizon and display grid; source-only validation and extended diagnostic tables are not exposed. |
| P03 | Complex-pole exponential envelope and phase relation | 5/5 | 0 | 0 | 1e-10 / 1e-10 | pass | response: Time (s), Modal amplitude (ratio); mechanism: Modal amplitude (ratio), Modal rate (1/s), Real pole part (1/s), Imaginary pole part (rad/s) | The platform keeps one conjugate-mode visualization and omits the source check-table and resource-bound reporting surface. |
| P04 | High-accuracy continuous nonlinear and linear pendulum integration | 5/5 | 0.0245 | 0.0245 | 0.03 / 0.03 | pass | response: Time (s), Angular displacement (deg); mechanism: Time (s), Angular model gap (deg), Angular displacement (deg), Angular rate (deg/s) | The platform fixes damping and integration grid and omits the source solver-residual and extended validation diagnostics. |
| P05 | Scalar affine closed-loop recurrence | 5/5 | 3.75e-12 | 4.8e-15 | 1e-10 / 1e-10 | pass | response: Time (s), Normalized plant output (ratio); mechanism: Time (s), Normalized control command (ratio), Tracking error (ratio) | The platform fixes reference amplitude and initial condition; source-only bound tables are omitted. |
| P06 | Augmented affine PID state-transition recurrence | 5/5 | 0.366 | 2.1e-12 | 1e-09 / 1e-09 | pass | response: Time (s), Position (m); mechanism: Time (s), Force contribution (N) | The platform fixes Kp, load, damping, horizon, and initial state to isolate Ki and Kd. |
| P07 | Affine plant recurrence plus root-solved frequency crossover | 5/5 | 0.463 | 0.0616 | 0.5 / 0.07 | pass | response: Time (s), Normalized plant output (ratio); mechanism: Angular frequency (rad/s), Magnitude (dB), Phase (deg) | The platform uses a fixed logarithmic display grid and reports an approximate grid crossover; the independent reference root-solves the crossover. |
| P08 | Closed-loop scalar recurrence with analytic sensitivity | 5/5 | 2.22e-16 | 2.22e-16 | 1e-09 / 1e-09 | pass | response: Time (s), Plant disturbance (normalized input), True output (normalized output); mechanism: Time (s), Measured output (normalized output), Control command (normalized input) | The platform fixes plant pole, disturbance start, and horizon; source-only extended sensitivity tables are omitted. |
| P09 | Augmented sampled-data PI state recurrence | 5/5 | 0 | 0 | 1e-10 / 1e-10 | pass | response: Time (s), Normalized plant output (ratio); mechanism: Time (s), Held command (normalized input), Integral state (ratio·s) | The platform fixes Kp, plant pole, reference, and horizon and does not expose alternate discretization families. |
| P10 | Independent sample/compute/apply event state machine | 5/5 | 0 | 0 | 1e-10 / 1e-10 | pass | response: Time (s), Normalized plant output (ratio); mechanism: Time (s), Applied command (normalized input), Equilibrium error (ratio) | The platform fixes controller gain, plant tick, and horizon and omits source-only event counters. |
| P11 | Continuous clipped first-order plant integration | 5/5 | 0.00166 | 0.00166 | 0.015 / 0.015 | pass | response: Time (s), Normalized plant output (ratio); mechanism: Time (s), Normalized actuator command (ratio) | The platform fixes controller gain and plant pole and omits source-only saturation transition tables. |
| P12 | High-accuracy continuous anti-windup state integration | 5/5 | 5.09 | 0.0159 | 0.02 / 0.02 | pass | response: Time (s), Normalized plant output (ratio); mechanism: Time (s), Normalized actuator command (ratio), Integral state (ratio·s) | The platform fixes Kp, Ki, saturation limit, demand levels, and plant pole to isolate anti-windup gain and demand duration. |
| P13 | Direct controllability matrix and finite-horizon Gramian construction | 5/5 | 8.33e-17 | 8.33e-17 | 1e-12 / 1e-12 | pass | response: Time (s), Position (m); mechanism: Ordered direction (index), Controllability singular value (state/input), Gramian eigenvalue (state²/input²) | The platform is a fixed two-state structural demonstrator; broader source parameterization, exact-ZOH variants, and complete finite-horizon Gramian tables are omitted. |
| P14 | Direct observability matrix and least-squares reconstruction | 5/5 | 1.11e-16 | 1.11e-16 | 1e-12 / 1e-12 | pass | response: Time (s), Position-equivalent measurement (m); mechanism: Ordered direction (index), Observability singular value (measurement/state), Time (s), Reconstructed rate (m/s) | The platform is a fixed two-state sensing demonstrator; broader source measurement models and complete reconstruction residual tables are omitted. |
| P15 | Exact affine observer-error transition from a matrix exponential | 5/5 | 0.00162 | 0.00162 | 0.02 / 0.02 | pass | response: Time (s), Position (m); mechanism: Time (s), Position error (m), Rate error (m/s) | The platform fixes the two-state plant and observer structure and omits source-only pole/residual tables. |
| P16 | Joseph-form covariance Kalman recurrence | 5/5 | 3.89e-16 | 3.89e-16 | 1e-09 / 1e-09 | pass | response: Time (s), Position (m); mechanism: Time (s), Position error (m), Velocity estimate (m/s) | The platform fixes the deterministic truth/noise record and two-state model and omits source-only covariance history tables. |
| P17 | Schur-method discrete Riccati solution | 5/5 | 9.81e-07 | 9.81e-07 | 2e-06 / 2e-06 | pass | response: Time (s), Position (m), Velocity (m/s); mechanism: Time (s), Control command (N), Absolute position (m) | The platform uses its documented discrete cart approximation and 500-step Riccati iteration rather than the source exact-ZOH plant and full 40000-iteration diagnostics. |
| P18 | High-accuracy continuous feedforward/feedback integration | 5/5 | 0.00165 | 0.00165 | 0.02 / 0.02 | pass | response: Time (s), Position (m); mechanism: Time (s), Acceleration (m/s²) | The platform fixes the sinusoidal demand, disturbance step, feedback shape, and plant mass to isolate feedforward and feedback scale. |
| P19 | Scalar uncertain closed-loop recurrence | 5/5 | 2.62e-10 | 6.56e-15 | 1e-10 / 1e-10 | pass | response: Time (s), Speed (m/s); mechanism: Time (s), Commanded acceleration (m/s²), Speed prediction gap (m/s) | The platform uses the documented forward-Euler scalar plant and omits the source exact-ZOH recurrence and extended uncertainty tables. |
| P20 | Two fixed-gain scalar recurrences over the declared uncertainty point | 5/5 | 3.31e+28 | 0.0259 | 1e-06 / 0.04 | pass | response: Time (s), Speed (m/s); mechanism: Time (s), Commanded acceleration (m/s²) | The source finite enumeration of 12 PI candidates over 25 plant points, feedforward term, effort screen, and PI state are omitted; this item claims only two preselected proportional gains. |
| P21 | Analytic quintic trajectory and derivative extrema | 5/5 | 0 | 0 | 1e-12 / 1e-12 | pass | response: Time (s), Position (m), Velocity (m/s), Acceleration (m/s²); mechanism: Time (s), Speed limit (m/s), Acceleration limit (m/s²) | The platform fixes zero endpoint velocity/acceleration and the 5 m/s and 2 m/s^2 limits; alternate boundary conditions are omitted. |
| P22 | Complex-plane proportional-navigation geometry recurrence | 5/5 | 0 | 0 | 1e-08 / 1e-08 | pass | response: Time (s), Range (m), Line-of-sight angle (deg); mechanism: Time (s), Lateral acceleration (m/s²) | The platform fixes initial geometry, speeds, target motion, hit radius, dt, and horizon; source-only event and geometry tables are omitted. |
| P23 | Independent convolution/IIR realization of actuator and sensor lags | 5/5 | 2.13e-14 | 1.29e-15 | 1e-10 / 1e-10 | pass | response: Time (s), Acceleration (m/s²); mechanism: Time (s), Acceleration error (m/s²) | The platform omits ideal zero-time-constant branches, sensor bias, independent amplitude/limit controls, and the source exact coupled repeated-pole sensor update. |
| P24 | Independent timestamped delivery/watchdog event scheduler | 5/5 | 2.52e-14 | 2.52e-14 | 1e-10 / 1e-10 | pass | response: Time (s), Position (m); mechanism: Time (s), Force (N), Packet age (s) | The platform omits cancellation, user-set watchdog/drop cadence/mass/dt/duration, packet counters, and cancellation precedence; retained behavior is software-only and not a capstone. |

## Material corrections

- P01 now reproduces the pinned source failure: explicit Euler at `dt=1 s`; the recovered path retains the resolved semi-implicit update.
- P14 separates direction index from time instead of placing incompatible x quantities on one axis.
- P17 no longer plots a dimensionally invalid norm of position and velocity; control force and absolute position use separate axes.
- P20 is explicitly a comparison of two preselected proportional gains. The source finite search over 12 PI candidates and 25 plant points is an omission, not a platform synthesis claim.
- P23 labels the command, actuator, sensor, and error signals in `m/s²`.
- P24 now models measurement latency and command latency as two ordered paths, uses the exact held-force mass-damper transition, reverses the reference at 4 seconds, and exposes watchdog fail-zero intervals. Cancellation and the broader source control surface remain explicit omissions. P24 is software-only and is not a capstone.

## Local verification

| Gate | Result |
| --- | --- |
| Controls/GNC source, schema, semantic-map, five-scenario, invariant, and runtime tests | `106 passed in 10.04s` |
| DSP/Radar unchanged-course regression | `300 passed in 17.79s` |
| Robotics plus course-caliber regression | `91 passed in 6.37s` |
| Course-caliber focused status tests | `12 passed in 0.19s` |
| `./scripts/agent-verify.sh contract` | `72 passed in 11.66s` |
| `./scripts/agent-verify.sh quick` | `573 passed, 4 dependency deprecation warnings, in 44.63s` |
| `./scripts/agent-verify.sh full` | catalog pass; `573 passed`; web TypeScript check and production build passed |
| Deterministic catalog execution | pass; 5 courses / 134 modules / 134 interactive modules |
| Ruff | passed for Controls/GNC course and focused tests |
| `git diff --check` | passed |
| Source/untouched-course scope | source gitlink and DSP/Radar, Robotics, demo, and showcase course paths unchanged |

The four Python warnings are existing dependency deprecations from Starlette/FastAPI. The web build also reports the existing Plotly chunk-size advisory; neither is a test or build failure.

## Maturity and residual limitations

Controls/GNC is `source_authored: passed`, `platform_converted: passed`, and `numerically_verified: passed` at the evidence boundary above. `curriculum_covered` and `capstone_integrated` remain `partial`; `learner_validated` remains `not_run`. Issue #439 is the sole owner of a reviewed competency map, course expansion, and cumulative integration.

No licensed MATLAB runtime was executed. No browser visual or accessibility acceptance, learner study, physical hardware/HIL, bench, field, release, deployment, credentials/settings, or production evidence was performed. Hosted GitHub Actions were not required by owner direction and no hosted result is claimed.

## Rollback

Before merge, close the single target PR and discard the isolated branch. After merge, revert the single target remediation commit. The Controls/GNC source repository, source gitlink, issue #439, other courses, runtime/UI, dependencies, workflows, and deployment artifacts do not require rewriting.
