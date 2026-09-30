# Compare Joint and Cartesian Kinematic Feedback



## Model, derivation, and conventions

`qdot_joint=k(q_goal-q)`

`qdot_task=J(q)^+ k(x_goal-x(q))`

`applied_qdot=clip(requested_qdot,-2,2)`

This lesson integrates two kinematic velocity servos for a planar two-link arm with lengths 1 and 0.7 m. It does not integrate torque dynamics. The gain slider has units inverse seconds. The legacy geometry control sets c and chooses the goal configuration [0.4,-1.2/sqrt(c)] rad. It is a straightness parameter, not a measured Jacobian condition number. The actual condition number is computed from the current geometry and retained separately.

Both servos start at the goal configuration plus [0.18,-0.12] rad. The joint-space servo commands gain times joint error. The Cartesian servo first computes the goal endpoint through forward kinematics, then commands gain times Cartesian position error. In normal mode it maps that Cartesian velocity through the Moore-Penrose inverse of the actual position Jacobian at the current state. Both systems clip each commanded joint velocity to ±2 rad/s before integrating over four seconds. The Jacobian is recalculated during integration, rather than frozen at the initial configuration.

Without clipping, joint-space error obeys a scalar exponential decay in each coordinate. Cartesian inverse feedback similarly gives xdot=k*(x_goal-x) where the Jacobian is nonsingular. However, straight-line endpoint motion need not correspond to a straight line in joint coordinates. The two controllers therefore trace different paths even when both eventually approach the same local inverse-kinematic solution. Near a straight arm, a modest Cartesian velocity can require large joint rates, making the clipping operation consequential.

The named faulty comparison substitutes J transpose for the inverse in the Cartesian command. This is a recognizable gradient direction for squared endpoint error; it is not universally unstable or meaningless. It generally produces xdot=J J transpose k e rather than k e. The matrix J J transpose weights different task directions differently, especially near a singular geometry, so its convergence can be slow and anisotropic. Calling it a transpose alternative with changed convergence is more accurate than pretending every transpose use is an algebraic impossibility.

The first two metrics are the Cartesian controller's terminal joint error in rad and terminal endpoint error in metres. The third is its peak applied joint speed in rad/s. The plots compare joint-error norms and Cartesian-error norms for both controllers through time; applied joint velocities are retained in diagnostics. No N m torque claim follows from those velocities. The four-second horizon can leave a nonzero residual without proving eventual divergence, and the local goal branch does not establish global inverse-kinematic convergence.

## Predict before running

Predict why a Jacobian-transpose descent law can move toward the target without matching the Cartesian convergence of an inverse velocity map. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Goal straightness parameter = 4.0 1; Velocity feedback gain = 3.0 1/s. Read the response curve, then connect it to the mechanism curve using the governing equations.

Joint tracking errors plots Joint error (rad) against Time (s). Its series are Joint servo, Task servo. Cartesian tracking errors plots Position error (m) against Time (s). Its series are Joint servo, Task servo.

The default record is Task-controller terminal joint error: 1.71021e-06 rad; Task-controller terminal Cartesian error: 1.31783e-06 m; Peak applied task joint speed: 0.476095 rad/s. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase feedback gain at fixed geometry. Observe convergence and whether velocity clipping becomes active. A faster requested response need not yield proportionally faster applied motion once rates saturate.

2. Increase the straightness parameter at fixed gain. Compare measured Jacobian conditioning and endpoint error in both modes. The slider chooses a pose; the resulting condition must be calculated.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The Cartesian controller uses a Jacobian-transpose gradient direction instead of inverse velocity mapping. The joint-space comparison and actual rate limits remain unchanged.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore inverse mapping and reset the initial state. Compare complete error curves and applied joint speeds, not just one final position.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

At zero Cartesian error both mappings command zero motion, so a settled target does not distinguish them. The experiment assumes ideal velocity servos, a fixed local goal branch and no collision or torque constraints. Near singularities, rate clipping changes the nominal exponential error law.

## Independent evidence and MATLAB-style design boundary

The reference differentiates forward kinematics by complex steps, uses an explicit two-by-two inverse, and integrates a separate Cartesian-controller state with RK45. Production uses an analytic Jacobian, pseudoinverse and DOP853.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. At zero Cartesian error both mappings command zero motion, so a settled target does not distinguish them.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why is the peak control output a joint speed rather than a torque, and why can transpose feedback still reduce error?

Answer rationale: The integrated plant is qdot equal to the applied velocity command, with no mass or torque equation. The transpose is a gradient direction for endpoint error, but its task response is weighted by J J transpose and does not implement the inverse velocity law.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
