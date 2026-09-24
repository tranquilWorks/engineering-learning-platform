# ELP-VEHICLE-PROPULSION-P44-P52 evidence — 2026-09-24

The batch starts from merged target `e33d1356f15f88c876fb41a482bb3882dcb20783`, tree `607ddefbbe9dc2fdabd9b01bed60a47f5131379f`. Portfolio Control authorization was merged in PR #486 at final control revision `7ae96819e00c1f893955b7e8bde94023b23ea393`. The read-only Vehicle Dynamics source remains commit `57264b3ffeb517ee5eb73e8957b9cd190d022457`, tree `d9e7267ba02c8d3d836c0ae481b80e91233eb81a`.

Exactly competency-map P44-P52 are added. All nine are Python-first native designs derived from the reviewed 67-module competency map. They are not conversions of the 24-item source inventory and claim neither source nor MATLAB-runtime equivalence.

| Item | Governing relation or method | Teaching invariant | Axes and units | Residual limitation and risk |
| --- | --- | --- | --- | --- |
| P44 | Bounded torque curve through gear, final drive, efficiency, and tire radius; minimum traction envelope | Delivered force is the lower of engine-limited force and driven-tire capacity | engine speed (rpm), road speed (m/s), force (N) | Synthetic torque and fixed driven load; no dyno, tire, or vehicle measurement |
| P45 | Squared-ratio inertia reflection and fixed-step traction-limited launch integration | Every rotating inertia is reflected through its squared speed ratio | elapsed time (s), speed (m/s), energy (kJ) | Lumped inertias and resistance; finite-step energy residual, no measured launch |
| P46 | Open and torque-biasing differential allocation under deterministic split friction | Bias redistributes demand but cannot exceed either wheel capacity or total demand | low-side friction (1), wheel force (N), capacity (N) | Fixed wheel loads and static friction; no differential-map or driveline compliance data |
| P47 | Bounded gear candidate search, engine-speed band, wheel-force selection, and shift interruption | Select the greatest valid wheel force and pay every declared shift delay | time (s), speed (m/s), gear (1), engine speed (rpm) | Fixed four-ratio set and synthetic torque curve; no shift transient or measured acceleration |
| P48 | Longitudinal load transfer, dynamic axle capacities, selected bias, and achieved deceleration | Brake force uses deceleration-dependent axle loads rather than static weights | deceleration (g), normal load and force (N), utilization (1) | Quasi-static rigid-body allocation; no hydraulic, tire-transient, or road-gradient effects |
| P49 | Quarter-vehicle wheel/vehicle dynamics with signed slip and deterministic torque modulation | ABS tracks positive braking slip without sustained wheel lock | time (s), slip (1), torque (N*m), distance (m) | Synthetic peak-slip tire curve and ideal state feedback; no sensor, actuator, or surface validation |
| P50 | Six-stop thermal integration with absorbed energy, convection, stored heat, and fade | Absorbed heat equals stored rotor energy plus convective rejection | stop count (1), temperature (degC), energy (kJ) | Lumped uniform rotor and synthetic fade law; no airflow, pad, rotor, or dyno data |
| P51 | Front/rear speed-squared aero forces with metre-based ride-height sensitivity and pitch moment | Convert millimetres to metres once and retain both axle contributions | ride height (mm), speed (m/s), force (N), balance (%) | Bounded linear front-height sensitivity; no wind-tunnel, yaw, rake, or floor-stall evidence |
| P52 | Downforce/drag, tire load sensitivity, power force, lap energy, and thermal/energy stint minimum | Count downforce once and debit drag from force and lap-energy ledgers | speed (m/s), acceleration (m/s^2), energy (MJ), stint (lap) | Aggregate fixed-lap budget with synthetic thermal cap; no route, weather, driver, or track validation |

Every work item retains baseline, `sweep_1`, `sweep_2`, broken, and recovery evidence at `1e-8` absolute and relative tolerance. Independent and production signatures match exactly across all 45 retained scenarios. The course-owned independent reference imports no production experiment, consumes no production result, and perturbs no production value. Broken scenarios respectively expose a missing tire envelope, inverse/omitted inertia reflection, wheel-capacity violation, redline/shift-delay violation, static brake-load allocation, unmodulated wheel lock, omitted cooling state update, millimetre/metre misuse, and downforce/drag double counting.

## Exact retained identities

- Active contract SHA-256: `8aaf80f5f415f152b21812846d49f6d65b41c876164078e83a95a54aa5ce0f34`.
- Expansion map SHA-256: `da9b0b9ab9aa98907407ff46f6f453f4fc4e8c33370a35bcb42bb6592cb0af2e`.
- Independent reference SHA-256: `b7937c709f86658bc00493656ea01dc6c3d00f3a9eb76866a2e1b29c866d05aa`.
- Source-bound conversion manifest SHA-256: `f2355103ecb9ff015b1dbcf25f0fe919f35659882cb1e77084cb672bd6f1a673`.
- Source-bound coverage ledger SHA-256: `bd49c77818f5cee93b8c185c6ee51220bb637a1753329a6503c5177836038ef0`.
- The reviewed competency map, native-design schema, source map, source-bound reference, synthetic fixtures, source gitlink, P01-P43 modules, every retained course, runtime, web application, package, script, and build configuration remain byte-identical to the starting tree. Only explicitly authorized catalog assertions, batch contracts, status, and handoff documentation change outside the P44-P52 expansion.

The source-bound ledger remains total 24, converted 24, pending 0, blocked 0, placeholder 0. The separate expansion ledger records 67 reviewed modules, P25-P52 implemented natively, and P53-P67 pending.

## Local verification

| Gate | Result |
| --- | --- |
| Focused Vehicle Dynamics expansion/framework/course/course-caliber tests | 59 passed |
| Retained DSP/Radar tests | 300 passed |
| Retained Controls/GNC and Robotics tests | 215 passed |
| Contract suite | 72 passed |
| Quick suite | 650 passed; three existing dependency deprecation warnings |
| Full suite | 650 passed; three existing dependency deprecation warnings |
| Deterministic catalog execution | six courses; 275 modules; 275 interactive; pass |
| Ruff batch and retained-test scopes | passed |
| TypeScript project build | passed |
| Production web build | passed; existing Plotly chunk-size advisory only |
| Diff, authorized scope, P01-P43 preservation, and source-gitlink cleanliness | passed |

Hosted CI is not a completion gate by owner direction. Publication and target merge are deliberately not claimed in this local evidence document; the exact published commit/tree and squash-merge identity must be recorded only after explicit publication authorization and remote verification.

MATLAB runtime comparison, browser accessibility, representative learner validation, measured engine, driveline, brake, aero, tire, rig, track, or vehicle data, firmware/radio/bench/vehicle/track execution, physical HIL/hardware, certification, release, deployment, credentials/settings, and production use remain explicitly unperformed.
