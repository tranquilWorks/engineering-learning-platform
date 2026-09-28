# Additional direct-review findings

These 60 additional lessons were found during the wider delivery audit, beyond
the initially selected twelve-lesson semantic repair. They remain blocked and
are not covered by that repair contract. This is a defect register, not a claim
that all remaining lessons have passed a complete semantic review.

The last sixteen findings were exposed when restored axis labels made the
Vehicle P01–P16 mixed-unit signature charts visible during screenshot review.
Their physical models are not all rejected; their dimensional presentation and
lesson-specific checks require repair.

| Course / lesson | Directly inspected gap |
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
| robotics-autonomy P42 | Calibration errors are formulas of view count and distortion; no synthetic calibration views are fitted or independently reprojected. |
| robotics-autonomy P43 | Feature repeatability, descriptor distance and count are formulas of threshold and rotation; no image features or descriptors are computed. |
| robotics-autonomy P44 | Inlier and false-acceptance metrics are formulas of outlier fraction and threshold; no correspondence consensus model is fitted. |
| robotics-autonomy P45 | Stereo depth and uncertainty formulas execute, but the round-trip residual is fixed rather than computed from reprojection. |
| robotics-autonomy P46 | Pose and reprojection errors are formulas of noise and landmark count; no landmark pose solve is executed. |
| robotics-autonomy P47 | Occupancy and entropy metrics are formulas of beam count and probability rather than ray updates on an occupancy grid. |
| robotics-autonomy P48 | ICP residual, transform error and iteration count are algebraic surrogates; no point correspondence or registration iteration is executed. |
| robotics-autonomy P52 | Appearance and geometry gates execute, but map deformation is a fixed-factor residual formula rather than a recomputed graph solution. |
| vehicle-dynamics P01 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P02 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P03 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P04 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P05 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P06 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P07 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P08 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P09 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P10 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P11 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P12 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P13 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P14 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P15 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |
| vehicle-dynamics P16 | Main response joins heterogeneous signature values on a generic SI axis; sweep response units and specific limiting checks need revision. |

Review source: each corresponding `courses/<course>/modules/<number>-*/experiment.py`
against its `design.yaml`, lesson claims and retained references. Controls P34–65
and Robotics P25–60 were inspected for executed model stages; Vehicle P25–67
was screened and its final performance/capstone group inspected directly.
The earlier DSP fidelity evidence remains retained. Static presence and these
targeted inspections do not certify every pedagogical claim in all 288 lessons.

Candidate further groups, subject to the owner’s scope preference: Controls
P36/P38/P42/P43/P45–51/P55 (12), Controls P56/P57/P60–62/P64–65 (7),
Robotics P25–36 (12), Robotics P37–48 (12), and Robotics P52 (1), and Vehicle P01–P16 (split into coherent groups). Cohesive
groups may combine the smaller tails. Preserve unrelated model outputs and
require real numerical mechanisms, independent oracles and meaningful teaching
checks in a fresh scoped contract before each repair.
