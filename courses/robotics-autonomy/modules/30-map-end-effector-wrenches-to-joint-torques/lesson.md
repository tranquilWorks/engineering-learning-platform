# Map Planar End-Effector Force to Joint Torque



## Model, derivation, and conventions

`v=J(q) qdot; tau=J(q)^T F`

`joint_power=tau^T qdot; Cartesian_power=F^T v`

`force_to_torque_gain=||J^T F_unit||`

The robot is a planar two-revolute-joint arm. Its proximal link length is L, selected in metres; its distal link is 0.7L. Shoulder angle is fixed at 0.4 rad and elbow angle sweeps from -0.8 to 0.8 rad in 121 samples. Endpoint position is L[cos(q1)+0.7cos(q1+q2), sin(q1)+0.7sin(q1+q2)]. Differentiating each coordinate with respect to both angles constructs the actual two-by-two position Jacobian. Its entries have units metres per radian. This task includes a Cartesian force, not an independently commanded endpoint moment; a full spatial wrench would require the corresponding angular rows.

The force direction is [0.6,0.8], a unit vector, multiplied by the selected force magnitude. Both force components use the same fixed world frame as the endpoint position. Joint velocity is [0.7,-0.4] rad/s. Multiplying J by this velocity gives the Cartesian velocity at each configuration. The force-to-torque map follows directly by equating incremental work: F transpose dx equals tau transpose dq, and dx equals J dq. Consequently tau equals J transpose F. Joint and Cartesian are calculated separately from their actual vectors rather than one being assigned to equal the other.

The third metric is the norm of J transpose times the unit force direction. It has units metres when radians are treated as dimensionless in mechanical work. It is not a dimensionless mechanical advantage. Dividing the torque norm by force magnitude would give the same value at nonzero force, but constructing the unit-force response also defines it at zero magnitude. Peak torque is the largest absolute component across the elbow sweep, whereas this gain is a vector norm; their numerical values therefore need not be proportional by the same coefficient.

For a hand calculation, set shoulder and elbow to zero temporarily and choose L=0.4 m. The Jacobian is [[0,0],[0.68,0.28]]. A vertical 8 N force gives joint torques [5.44,2.24] N m. With the stated joint rates, endpoint vertical speed is 0.364 m/s and both power calculations give 2.912 W. Applying J directly to the force instead gives [0,2.24] N m, whose joint power is -0.896 W. The live sweep uses a different shoulder angle, so this example teaches the multiplication and sign convention rather than supplying its default answer.

## Predict before running

Predict which mapping preserves virtual power throughout an elbow sweep, and whether zero force can expose the wrong mapping. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use End-effector force = 8.0 N; Proximal link length = 0.4 m. Read the response curve, then connect it to the mechanism curve using the governing equations.

Mapped joint torques plots Torque (N·m) against Elbow angle (rad). Its series are Joint 1, Joint 2. Virtual power check plots Power (W) against Elbow angle (rad). Its series are Joint, Cartesian.

The default record is Peak joint torque: 3.78415 N*m; Maximum virtual-power mismatch: 8.88178e-16 W; Peak force-to-torque gain: 0.545518 m. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase force magnitude while holding proximal length fixed. Torque and both power traces scale linearly. The unit-force gain stays unchanged, and normal power discrepancy remains near numerical roundoff.

2. Increase proximal length while holding force fixed. Both links scale together, so Jacobian entries, torques and endpoint speeds scale with length. Compare the gain in metres; do not call the change an efficiency improvement.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The fault applies J F instead of J transpose F. Because this planar map happens to be square, the multiplication has compatible array dimensions and runs, but it violates the work duality.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore the transpose, reset controls, and compare both power traces across every elbow sample. A single zero-power configuration is insufficient evidence.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

At zero force both torque maps produce zero, so the fault is unobservable through power. At zero length the ideal geometric torques vanish; the interactive length range remains positive. This is quasistatic mapping, with no inertia, friction or actuator model.

## Independent evidence and MATLAB-style design boundary

The reference differentiates forward kinematics using complex steps, then independently forms torque and the two scalar powers. It retains Jacobians and torque vectors for full-sweep comparisons.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. At zero force both torque maps produce zero, so the fault is unobservable through power.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why can a matrix multiplication run successfully while producing the wrong joint torques?

Answer rationale: The square array dimensions do not enforce physical duality. Only J transpose maps Cartesian force into joint torque while preserving F dot (J qdot) = tau dot qdot. A zero-force trial cannot distinguish the maps.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
