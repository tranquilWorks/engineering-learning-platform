# ELP-VEHICLE-TIRES-P25-P33 evidence — 2026-09-24

The batch starts from merged target `c14c2d3d7376a2f06cb12c55e91ad8bb98ae8088`, tree `3959fa6915484ed8e3d8563c7dc4a3f7c1448183`, under merged Portfolio Control authorization `85c062604e5dba94d97fd95d07b65a0949fc1d2a` (PR #480). The read-only Vehicle Dynamics source remains commit `57264b3ffeb517ee5eb73e8957b9cd190d022457`, tree `d9e7267ba02c8d3d836c0ae481b80e91233eb81a`.

Exactly competency-map P25-P33 are added. All nine are Python-first native designs derived from the reviewed 67-module competency map. They are not conversions of the 24-item source inventory and claim neither source nor MATLAB-runtime equivalence.

| Item | Governing relation or method | Teaching invariant | Axes and units | Residual limitation |
| --- | --- | --- | --- | --- |
| P25 | Passive planar transforms `v_B=R(-psi)v_I`, wheel rotation, inverse and norm checks | A proper rotation preserves speed norm and recovers declared components in one angle convention | steer/heading (deg), velocity/error (m/s) | Planar deterministic velocity with fixed nominal sideslip; no 3D attitude, sensor calibration, or measured motion |
| P26 | `F_peak=mu_ref F_ref (F_z/F_ref)^n` and fixed-total-load paired capacity | For `n<1`, force grows while effective friction falls and unequal sharing loses capacity | normal load/force (N), transfer/friction (1) | One empirical exponent and fixed transfer fraction; no construction, pressure, temperature, or measured tire data |
| P27 | Clipped longitudinal law; unsaturated slope fit; saturated peak estimate; held-out residual | Low-slip samples identify stiffness while saturated samples identify peak friction in dimensionless slip ratio | slip ratio (1), longitudinal force/residual (N) | Piecewise-linear saturation and noiseless deterministic synthetic observations; no rig identification |
| P28 | Two-column slip-angle/camber regression with force clipping and held-out validation | Independent radian-valued angle columns separate cornering and camber stiffness | slip angle (deg), lateral force/residual (N), stiffness (N/rad) | Static SAE-style instructional convention; no aligning moment, load sweep, ply steer, or measured tire data |
| P29 | Pure-slip `tanh` demands projected radially onto a friction circle | Delivered combined utilization stays at or below one with a common scale factor | longitudinal/lateral force (N), slip/utilization (1) | Circular isotropic boundary; no friction ellipse calibration, aligning moment, or transient coupling |
| P30 | `dF/ds=(F_ss-F)/sigma`, `tau=sigma/v`, analytic step response | The 63.2-percent response occurs after one relaxation length; speed changes time, not distance | time (s), distance (m), force (N) | First-order constant-speed lag only; no carcass modes, load/temperature effects, or measured transient data |
| P31 | Lumped thermal ODE, Kelvin pressure ratio, bounded temperature-pressure grip envelope | Supplied heat equals stored plus rejected energy and gas pressure uses absolute temperature | time (s), temperature (degC), pressure (kPa), grip (1) | Single lumped state and idealized gas/grip laws; no tread/carcass gradients, leakage, or physical pressure evidence |
| P32 | `P_slip=|F_x v kappa|+|F_y v tan(alpha)|` and cumulative energy balance | Nonnegative slip work equals stored thermal energy plus rejected heat | time (s), work/heat (J), power (W), temperature (degC) | Constant forces, speed, and slips over one bounded interval; no spatial temperature or wear model |
| P33 | Training-only least squares plus held-out bias, RMSE, normalized residual, and 95-percent coverage | Validation rows remain outside fitting and coverage uses the declared positive observation sigma | force (N), row (1), normalized residual/coverage (1) | Deterministic synthetic residual pattern and one scalar scale factor; no probability calibration or measured tire validation |

Every work item retains baseline, `sweep_1`, `sweep_2`, broken, and recovery evidence at `1e-8` absolute and relative tolerance. The largest observed independent-versus-production scalar difference is `2.91e-11`. The course-owned independent reference imports no production experiment, consumes no production result, and perturbs no production value. Broken scenarios respectively expose degree/radian misuse, erased load sensitivity, percent/ratio confusion, degree-domain regression, uncapped combined force, omitted speed conversion, Celsius pressure ratio, missing heat rejection, and validation leakage with underreported uncertainty.

## Exact retained identities

- Active contract SHA-256: `c1f0e4b603bce4303d42df1e6e2f7d84af03de2ae0eb7e0be69eefbac1abe138`.
- Expansion map SHA-256: `76d79fa4427bcfbf05b10651424111ea451d82da4a17d5903aa74afaa188205b`.
- Independent reference SHA-256: `78f4b931256555db427fca418d4481899fa280423367db2093bbd7fd48012237`.
- Source-bound conversion manifest SHA-256: `f2355103ecb9ff015b1dbcf25f0fe919f35659882cb1e77084cb672bd6f1a673`.
- Source-bound coverage ledger SHA-256: `bd49c77818f5cee93b8c185c6ee51220bb637a1753329a6503c5177836038ef0`.
- The reviewed competency map, source map, source-bound reference, synthetic fixtures, source gitlink, P01-P24 modules, all retained course content, runtime, web application, packages, scripts, and build configuration remain byte-identical to the starting tree. Only explicitly authorized catalog assertions, batch contracts, status, and handoff documentation change outside the P25-P33 expansion.

The source-bound ledger remains total 24, converted 24, pending 0, blocked 0, placeholder 0. The separate expansion ledger records 67 reviewed modules, P25-P33 implemented natively, and P34-P67 pending.

## Local verification

| Gate | Result |
| --- | --- |
| Focused Vehicle Dynamics expansion/framework/course/course-caliber tests | 57 passed |
| Retained DSP/Radar tests | 300 passed |
| Retained Controls/GNC and Robotics tests | 215 passed |
| Contract suite | 72 passed |
| Quick suite | 648 passed; three existing dependency deprecation warnings |
| Full suite | 648 passed; three existing dependency deprecation warnings |
| Deterministic catalog execution | six courses; 256 modules; 256 interactive; pass |
| Ruff batch and retained-test scopes | passed |
| TypeScript project build | passed |
| Production web build | passed; existing Plotly chunk-size advisory only |
| Diff, authorized scope, P01-P24 preservation, and source-gitlink cleanliness | passed |

Hosted CI is not a completion gate by owner direction.

MATLAB runtime comparison, browser accessibility, representative learner validation, measured tire or vehicle data, tire rig or proving-ground comparison, firmware/radio/bench/vehicle/track execution, physical HIL/hardware, certification, release, deployment, credentials/settings, and production use remain explicitly unperformed.
