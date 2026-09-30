# Regulate Tangential Motion and Normal Contact Force



## Model, derivation, and conventions

`n=[-sin(theta),cos(theta)]; t=[cos(theta),sin(theta)]`

`P_force=n n^T; P_motion=I-P_force`

`F=600 max(n^T x,0); xdot=P_motion(v_t+5(x_goal-x))+n*0.012(F_goal-F)`

The environment is a planar contact surface through the origin. Its unit normal is n=[-sin(theta),cos(theta)] and its unit tangent is t=[cos(theta),sin(theta)], with the selected angle converted from degrees. The endpoint begins at the surface origin. Positive normal displacement is penetration, and a unilateral spring produces force magnitude F=600*max(n dot x,0) N. Negative penetration corresponds to loss of contact and zero spring force. This distinction matters even in a simple kinematic controller.

The desired tangential velocity is 0.03 m/s and the moving position goal is 0.03*time*t. Tangential feedback adds five per second times position error before projection. Normal force feedback uses gain 0.012 m/(N s) times desired-minus-measured force, converting force error into an endpoint velocity along the selected controller normal. The ideal velocity servo integrates this two-dimensional command over two seconds. There is no inertial robot, force sensor delay or joint-space torque mapping in this experiment.

In normal mode, the force projector n n transpose and motion projector I-n n transpose split orthogonal directions of the actual surface. Tangential motion then has no normal component, while force feedback has no tangential component. With zero initial normal displacement and a nonnegative force goal, penetration approaches goal force divided by 600. For example, a 10 N goal corresponds to approximately 0.01667 m spring deflection. That number describes this soft synthetic environment, not an acceptable physical indentation.

Broken mode uses world vertical [0,1] as the controller normal regardless of the surface angle. Its two projectors remain symmetric, idempotent, complementary and orthogonal. The failure is geometric alignment: world vertical is not the actual surface normal when the plane is tilted. Force feedback can then cause tangential motion, and the nominal motion command can change penetration. Reporting an orthogonality defect would falsely claim that these valid matrix properties had failed.

The tangential-speed plot includes zero and a 0.06 m/s reference span, expanding if actual motion requires it. This prevents automatic scaling from magnifying roundoff around the constant nominal speed into an apparent physical oscillation. The underlying samples are retained unchanged.

The first metric is terminal normal-force error. The second is RMS tangential speed error across the actual trajectory, not merely its terminal value. The third is the norm of the difference between the used force projector and the physical normal projector. This dimensionless frame-alignment defect identifies the selected direction error even when force happens to converge. Retained diagnostics include position, velocity, force and both projectors.

At zero requested force, faulty tangential motion can move the endpoint away from the surface. The unilateral force then remains zero rather than becoming a tensile spring force. The independent reference explicitly handles this branch in surface coordinates. A linear bilateral formula would be insufficient at that boundary and could agree in the baseline while failing a valid corner case.

## Predict before running

Predict whether two perfectly orthogonal projectors can still be wrong for a tilted contact surface. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Normal-force setpoint = 12.0 N; Surface angle = 25.0 deg. Read the response curve, then connect it to the mechanism curve using the governing equations.

Normal force feedback plots Normal force (N) against Time (s). Its series are Actual, Setpoint. Tangential motion plots Velocity (m/s) against Time (s). Its series are Actual, Desired.

The default record is Terminal normal-force error: 6.68868e-06 N; Tangential speed-error RMS: 3.14725e-17 m/s; Force-projector frame mismatch: 0 1. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase force goal at fixed surface angle. Compare terminal force and transient tangential speed. Correct projection preserves tangential tracking while normal displacement changes to support the new force.

2. Increase surface angle at fixed force goal. In normal mode the coordinate directions rotate together. In faulty world-axis mode compare frame-alignment error and tangential leakage.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The fault retains complementary orthogonal projectors but builds them from world vertical instead of the actual surface normal. Physical force is still measured along the real normal.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore surface-aligned projectors and reset position. Check physical force and tangential velocity, then verify that the matrix alignment defect returns to roundoff.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

At zero surface angle world vertical and the physical normal coincide, so both modes agree. At zero force goal the unilateral contact may open in faulty mode. This ideal velocity-servo example omits impacts, robot inertia, sensor delay and actuator constraints.

## Independent evidence and MATLAB-style design boundary

The reference integrates normal and tangential surface coordinates with RK45, including the unilateral force law. Production integrates Cartesian position with DOP853; the resulting positions, velocities and forces are compared after an independent basis transformation.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. At zero surface angle world vertical and the physical normal coincide, so both modes agree.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

How can the projector algebra pass while hybrid motion and force regulation is still wrong?

Answer rationale: Orthogonality describes the relation between the two chosen subspaces, not their alignment with the environment. World-axis projectors are internally orthogonal but mix real normal and tangential directions on a tilted surface.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
