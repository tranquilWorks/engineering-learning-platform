# Additional direct-review findings

All sixty additional named findings now have scoped repairs, completing the owner-authorized Vehicle twelve-plus-four revision. The current named register is Controls 0, Robotics 0, Vehicle 0. This register is not exhaustive; all three non-DSP aggregate numerical, curriculum and capstone reassessments remain blocked.

## Closed by ELP-VEHICLE-DRIVELINE-QUALITY-04

P13–P16 originally joined signature quantities with different physical units on a generic SI axis, with unnamed sweep units and insufficient limiting-case checks. Those findings are retained here as history. Each lesson now has physical curves, a substantial individual lesson and an embedded Course checkpoint. Twenty independent full-mechanism comparisons, 32 runtime corners, 106 selected/regression tests, eight baked desktop/mobile checks and the actual-control P14 crossover test passed before closure. Eight plot captures were inspected. Full delivery and all mandatory sequential gates subsequently passed; exact counts and hashes are retained in vehicle-driveline-verification-summary.json.

- **P13:** Executed engine-to-wheel gearing, capped applied force and delivered-power balance; independent power-first formulation separates requested-torque curtailment from drivetrain loss. Fixed-speed mapping does not establish engine/redline feasibility or tire-slip dynamics.
- **P14:** Executed post-shift torque lookup and wheel-force comparison with resolved crossover, redline fallback and unavailable invalid-ratio decisions; independent analytic polynomial root. The actual refined controls reach 2.09 to 2.08 and the 7399.34147 RPM crossover. No shift-time or lap-optimality claim.
- **P15:** Executed constant-force capped stopping, longitudinal load transfer and kinetic-energy/work/heat closure; independent energy-first trajectory. Actual double-counted heat fault changes rotor temperature while preserving motion. Cooling, brake bias and transient tire dynamics are excluded.
- **P16:** Executed drag/downforce coefficients, complementary axle allocation, normal loads and drag power; independent coefficient-area formulation and speed-scaling checks. Negative faulty rear aerodynamic contribution is distinguished from total wheel load; no measured-aero or tire-load-sensitivity claim.

## Closed by ELP-GNC-SEMANTIC-QUALITY-12

The following original findings are retained as history. Each has five independent
numerical comparisons, model-specific physical tests, an embedded Course checkpoint
and desktop/mobile control, fault, recovery and reset evidence. See
[revision evidence](gnc-quality-revision.json) and the current browser report.
These scoped closures do not promote the Controls course aggregate.

| Course / lesson | Original finding, now repaired |
| --- | --- |
| controls-gnc P36 | The displayed state-feedback control omits the velocity feedback term; recompute control from both propagated states and reconcile its units. |
| controls-gnc P38 | The separation-principle model places poles directly but the lesson calls the design LQR; distinguish pole placement from a cost-derived optimal gain. |
| controls-gnc P42 | The peak integral-state metric uses peak command in nominal mode and final integral state in broken mode; it does not measure the named quantity consistently. |
| controls-gnc P43 | The declared nonlinear double-well phase portrait is replaced by an exponential sinusoid and unrelated energy formulas; the stated dynamics are not integrated. |
| controls-gnc P45 | The barrier plot extrapolates one fixed command without reevaluating the state-dependent barrier; it can cross the safety boundary while presented as a filtered trajectory. |
| controls-gnc P46 | The interpolation error is assigned from grid spacing instead of measuring interpolation of a sampled gain schedule. |
| controls-gnc P47 | The quadratic feedback-linearization model is replaced by a linear exponential and an algebraic terminal-error formula; the nonlinear closed loop is not executed. |
| controls-gnc P48 | The uncertainty plot does not sweep the declared uncertainty interval, and the inverse decay-rate metric is labeled dimensionless sensitivity without a defined transfer response. |
| controls-gnc P49 | The MPC lesson clips a fixed move and divides a residual by horizon; it does not minimize the stated horizon cost or execute receding-horizon control. |
| controls-gnc P50 | Identification conditioning, parameter error and held-out residual are algebraic functions of excitation settings; no dynamic model is fitted or validated. |
| controls-gnc P51 | The online-identification lesson does not execute its recursive least-squares update; error and covariance metrics are parameter formulas. |
| controls-gnc P55 | Unscented-transform errors and weights are assigned directly; sigma points and their weighted transformed moments are not computed. |

## Navigation/geometry revision: closed findings history

The following original observations are preserved. Their closure is limited to the executed synthetic models and retained numerical/browser evidence; it is not an aggregate course promotion.

| Course / lesson | Original inspected gap, now repaired in this scope |
| --- | --- |
| controls-gnc P56 | The claimed RTS smoother multiplies filtered covariance by a fixed 0.65 instead of executing a forward filter and backward smoother. |
| controls-gnc P57 | Quaternion norm and rotation orthogonality errors are fixed constants; no quaternion-to-matrix transformation is evaluated. |
| controls-gnc P60 | GNSS position and clock errors are algebraic dilution formulas; the claimed pseudorange position/clock solve is not executed. |
| controls-gnc P61 | GNSS/INS uncertainty is reduced by a fixed 0.35 factor rather than an error-state covariance update and state reset. |
| controls-gnc P62 | The post-exclusion residual is multiplied by a fixed 0.15 without excluding a measurement and recomputing the navigation solution. |
| controls-gnc P64 | The guidance comparison reports an explicitly named miss proxy, but the trajectories and variants are not integrated; its scope and cumulative interpretation need revision. |
| controls-gnc P65 | Terminal error is assigned from an acceleration shortfall; the terminal dynamics are not propagated and the displayed violation is not measured from applied commands. |
| robotics-autonomy P25 | Constraint residual and tangent dimension are assigned without constructing the constraint Jacobian or projecting a configuration velocity. |
| robotics-autonomy P26 | Orthogonality, determinant and composition errors are algebraic surrogates without constructing and composing rigid transforms. |
| robotics-autonomy P27 | Power-invariance and adjoint round-trip errors are assigned without transforming an actual twist/wrench pair. |
| robotics-autonomy P28 | Singular values and finite-difference errors are assigned from elbow-angle formulas without constructing the Jacobian or differencing kinematics. |
| robotics-autonomy P29 | Task error and null-space leakage are parameter formulas without executing a Jacobian pseudoinverse and null-space projection. |

## Robotics dynamics revision: closed findings history

The original findings below are retained. Closure is limited to the executed synthetic models, independent calculations, physical checks and embedded browser checkpoints. It does not promote aggregate course acceptance.

| Course / lesson | Original inspected gap, now repaired in this scope |
| --- | --- |
| robotics-autonomy P30 | The virtual-power error is assigned from force times lever arm, which has torque units; no joint/Cartesian velocity power comparison is executed. |
| robotics-autonomy P31 | Inertia eigenvalue and skew-identity error are assigned without constructing inertia and Coriolis matrices. |
| robotics-autonomy P32 | Payload error, regressor conditioning and inverse-dynamics residual are formulas of the guess and excitation rather than an identified model and held-out torque calculation. |
| robotics-autonomy P33 | The cubic trajectory duration omits its 1.5 peak-velocity factor, while the nominal limit-violation metric is forced to zero and plotted acceleration omits time scaling. |
| robotics-autonomy P34 | Joint/task tracking and torque metrics use condition-number formulas rather than executing the stated kinematics and feedback loops. |
| robotics-autonomy P35 | Computed-torque tracking and gravity residuals are algebraic surrogates rather than an integrated robot model with model-based compensation. |
| robotics-autonomy P36 | Operational-space inertia and residuals are assigned without forming the joint inertia, Jacobian or operational-space dynamics. |
| robotics-autonomy P37 | Contact responses and settling metrics use exponential surrogates instead of the declared impedance/admittance differential equations. |
| robotics-autonomy P38 | Hybrid motion/force residuals and projector error are assigned without constructing the surface-frame projectors or executing feedback. |
| robotics-autonomy P39 | Passivity energy and recovery are formulas of delay and force limit; no delayed work/energy trace is executed. |
| robotics-autonomy P40 | Swing-up time and balance error are algebraic surrogates; no underactuated dynamics, energy controller or balancing transition is executed. |
| robotics-autonomy P41 | Pinhole projection executes, but the near-plane violation metric is a fixed mode flag rather than a test of projected point depth. |

## Robotics perception revision: closed findings history

The original findings below are retained. Closure covers the executed synthetic models, independent geometry/solver checks and embedded browser checkpoints. It does not promote aggregate course acceptance.

| Course / lesson | Original inspected gap, now repaired in this scope |
| --- | --- |
| robotics-autonomy P42 | Calibration errors are formulas of view count and distortion; no synthetic calibration views are fitted or independently reprojected. |
| robotics-autonomy P43 | Feature repeatability, descriptor distance and count are formulas of threshold and rotation; no image features or descriptors are computed. |
| robotics-autonomy P44 | Inlier and false-acceptance metrics are formulas of outlier fraction and threshold; no correspondence consensus model is fitted. |
| robotics-autonomy P45 | Stereo depth and uncertainty formulas execute, but the round-trip residual is fixed rather than computed from reprojection. |
| robotics-autonomy P46 | Pose and reprojection errors are formulas of noise and landmark count; no landmark pose solve is executed. |
| robotics-autonomy P47 | Occupancy and entropy metrics are formulas of beam count and probability rather than ray updates on an occupancy grid. |
| robotics-autonomy P48 | ICP residual, transform error and iteration count are algebraic surrogates; no point correspondence or registration iteration is executed. |
| robotics-autonomy P52 | Appearance and geometry gates execute, but map deformation is a fixed-factor residual formula rather than a recomputed graph solution. |

## Closed by ELP-VEHICLE-FOUNDATIONS-QUALITY-12

Each selected lesson now has five independent full-mechanism comparisons, lesson-specific physical checks, all runtime corners, an embedded checkpoint and baked desktop/mobile evidence. P07 additionally fixes the inconsistent speed factors that previously violated both equilibrium equations. Original source/conversion records remain historical; revised native faults do not claim unchanged full-source equivalence.

| Course / lesson | Original finding, now repaired |
| --- | --- |
| vehicle-dynamics P01 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P02 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P03 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P04 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P05 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P06 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P07 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P08 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P09 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P10 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P11 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P12 | Original chart joined heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
