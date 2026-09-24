# ELP-VEHICLE-CHASSIS-P34-P43 evidence — 2026-09-24

The batch starts from merged target `d7486da7a0207cebcee17de2825879495bce66d8`, tree `f700ddc5fbb9b392a06db7a818d84e7406ac3492`. Portfolio Control authorization was merged in PR #484 at `7cfaf6f6be05d6ac3a7ade77b0b31b0e09839ddc`; PR #485 corrected the omitted status-test allow path without changing acceptance or baseline, producing final control revision `7487b57cc31fd01926fac8cbd888ebf5a29af5a0`. The read-only Vehicle Dynamics source remains commit `57264b3ffeb517ee5eb73e8957b9cd190d022457`, tree `d9e7267ba02c8d3d836c0ae481b80e91233eb81a`.

Exactly competency-map P34-P43 are added. All ten are Python-first native designs derived from the reviewed 67-module competency map. They are not conversions of the 24-item source inventory and claim neither source nor MATLAB-runtime equivalence.

| Item | Governing relation or method | Teaching invariant | Axes and units | Residual limitation |
| --- | --- | --- | --- | --- |
| P34 | Linear beta/yaw-rate bicycle state matrix and steady equilibrium | Stable poles and physical lateral-force/yaw-moment closure must agree | steer/state (deg, deg/s), pole plane (1/s, rad/s) | Linear planar small-angle model with fixed rear stiffness; no measured handling data |
| P35 | Complex state solve `(j omega I-A)X=B Delta` | Hertz converts to radians per second before the state solve | frequency (Hz), gain (1 or 1/s), phase (deg) | Linear single-track frequency response; no steering-system, compliance, or measured FRF |
| P36 | `K=W_f/C_f-W_r/C_r`, steer law, positive-domain characteristic speed | Characteristic speed exists only for positive understeer gradient | lateral acceleration (g), steer (deg), speed (m/s) | Steady linear cornering on fixed radius; no nonlinear tire or transient validation |
| P37 | Bounded axle `tanh` forces, yaw moment, numerical stability slope | Restoring slope and axle capacity must both pass | sideslip (deg), yaw moment (N*m), utilization (1) | Fixed-speed slip proxy with deterministic parameters; no track or recovery-maneuver evidence |
| P38 | Geometric plus elastic lateral-load-transfer partition | Front and rear paths reconstruct one total roll moment | stiffness fraction (1), transfer (N), capacity loss (N) | Quasi-static rigid-body partition with fixed roll centers; no suspension rig validation |
| P39 | Corner-assembled 3-DOF generalized eigenproblem | Each mode satisfies the full coupled `K phi=lambda M phi` equation | mode index (1), frequency (Hz), participation (1) | Undamped small-motion heave/pitch/roll model; no measured modal survey |
| P40 | Base-excited sprung-mass complex transmissibility | Road wavelength and speed map through hertz to angular frequency | wavelength (m), transmissibility (1), acceleration (m/s^2) | One sprung-mass mode and sinusoidal road; no tire unsprung mode or road measurement |
| P41 | Continuous odd-symmetric digressive force law and cycle-energy integral | Tangent slope transitions from low- to high-speed damping while energy stays dissipative | velocity (m/s), force (N), power (W) | Ideal symmetric passive law; no hysteresis, temperature, cavitation, or damper-dyno data |
| P42 | Bump gradients plus lateral-force compliance and motion-ratio wheel rate | Per-millimetre geometry and per-newton compliance retain distinct units | travel (mm), force (N), alignment (deg) | Linearized alignment gradients; no hardpoint sweep, bushing nonlinearity, or rig data |
| P43 | Side-view anti geometry and longitudinal transfer partition | Geometry redirects one pitch-transfer total without creating load transfer | angle (deg), anti (%), transfer (N) | Bounded non-lifting side-view geometry; no 3D link loads, jacking, or physical test |

Every work item retains baseline, `sweep_1`, `sweep_2`, broken, and recovery evidence at `1e-8` absolute and relative tolerance. The largest observed independent-versus-production scalar difference is `1.21e-13`. The course-owned independent reference imports no production experiment, consumes no production result, and perturbs no production value. Broken scenarios respectively expose a rear-force sign error, hertz/radian misuse, stiffness unit misuse, uncapped axle force, double-counted load transfer, erased modal coupling, road-frequency misuse, damper velocity-unit misuse, suspension travel-unit misuse, and anti-geometry angle misuse.

## Exact retained identities

- Active contract SHA-256: `9c5863c7fcb22ea5192a7f1f6630287e0ac242529b58265cc79900ff58242241`.
- Expansion map SHA-256: `544f3daaf713243c943d929762beb07c6d356fcd076851cfe0e76775e78776f5`.
- Independent reference SHA-256: `9b5c88a7102b32f0e82d6cd9cfaa3de02470f3483e77f3af13802ae7e7ab4d1b`.
- Source-bound conversion manifest SHA-256: `f2355103ecb9ff015b1dbcf25f0fe919f35659882cb1e77084cb672bd6f1a673`.
- Source-bound coverage ledger SHA-256: `bd49c77818f5cee93b8c185c6ee51220bb637a1753329a6503c5177836038ef0`.
- The reviewed competency map, native-design schema, source map, source-bound reference, synthetic fixtures, source gitlink, P01-P33 modules, every retained course, runtime, web application, package, script, and build configuration remain byte-identical to the starting tree. Only explicitly authorized catalog assertions, batch contracts, status, and handoff documentation change outside the P34-P43 expansion.

The source-bound ledger remains total 24, converted 24, pending 0, blocked 0, placeholder 0. The separate expansion ledger records 67 reviewed modules, P25-P43 implemented natively, and P44-P67 pending.

## Local verification

| Gate | Result |
| --- | --- |
| Focused Vehicle Dynamics expansion/framework/course/course-caliber tests | 58 passed |
| Retained DSP/Radar tests | 300 passed |
| Retained Controls/GNC and Robotics tests | 215 passed |
| Contract suite | 72 passed |
| Quick suite | 649 passed; three existing dependency deprecation warnings |
| Full suite | 649 passed; three existing dependency deprecation warnings |
| Deterministic catalog execution | six courses; 266 modules; 266 interactive; pass |
| Ruff batch and retained-test scopes | passed |
| TypeScript project build | passed |
| Production web build | passed; existing Plotly chunk-size advisory only |
| Diff, authorized scope, P01-P33 preservation, and source-gitlink cleanliness | passed |

One earlier full-suite invocation was interrupted by the execution runner at 66 percent without a reported test failure. The required full command was restarted from the beginning and passed, including TypeScript and the production build. Hosted CI is not a completion gate by owner direction.

MATLAB runtime comparison, browser accessibility, representative learner validation, measured damper, suspension, tire, rig, track, or vehicle data, firmware/radio/bench/vehicle/track execution, physical HIL/hardware, certification, release, deployment, credentials/settings, and production use remain explicitly unperformed.
