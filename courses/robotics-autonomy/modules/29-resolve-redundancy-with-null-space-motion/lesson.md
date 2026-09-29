# Separate Damped Task Motion from Exact Null-Space Motion



## Model, derivation, and conventions

`qdot_primary=J^T(JJ^T+lambda²I)^-1 v_desired`

`N=I-Jplus J; qdot_secondary=-gain N q`

`qdot=qdot_primary+qdot_secondary; leakage=||J qdot_secondary||`

The arm has three planar revolute joints with link lengths [1,0.8,0.6] m. The fixed joint configuration is [0.3,-0.7,0.9] rad. Forward kinematics uses cumulative joint angles, and differentiating the end-effector position gives a two-by-three Jacobian. The task asks for velocity [0.1,-0.06] m/s. With two independent position constraints and three joint velocities, the full-row-rank Jacobian has a one-dimensional null space. This redundancy makes an instantaneous posture change possible without first-order task motion.

The primary command is a damped inverse solution. Length and angle coordinates are normalized by one metre and one radian before applying the dimensionless damping slider; reported velocities retain m/s and rad/s. Increasing damping regularizes the inverse but also introduces a task tracking residual. That residual belongs to the primary solution and must not automatically be called secondary leakage. The secondary command uses a separate exact Moore-Penrose null projector, formed from the current full-row-rank Jacobian. Its task effect should be near numerical roundoff for every selected posture gain.

The posture direction is minus q, pulling joint coordinates toward zero instantaneously. The displayed sweep evaluates 121 gains from zero to the selected gain at the same configuration. It does not integrate joint angles or update the Jacobian as the arm moves. A decreasing instantaneous quadratic posture objective can motivate the direction, but it does not demonstrate eventual convergence or compliance with any joint limit. The third metric is the actual joint velocity norm, not an invented remaining joint-limit margin.

For a small worked algebra example, let J=[[1,0,1],[0,1,0]]. A normalized null vector is [1,0,-1]/sqrt(2). Projecting posture q=[1,2,0] onto that direction gives [0.5,0,-0.5]. With unit gain, secondary velocity is [-0.5,0,0.5], and multiplying by J gives [0,0]. Bypassing projection instead gives [-1,-2,0], which produces task velocity [-1,-2]. This shows why a posture direction that seems reasonable in joint coordinates can corrupt the primary task unless its null-space property is actually checked.

## Predict before running

Predict whether primary damping requires secondary posture motion to leak into the task when an exact null projector is used.

## Baseline workflow

Reset controls and leave the named fault disabled. Use Pseudoinverse damping = 0.08 1; Null-space gain = 0.6 1/s. Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

Instantaneous joint commands plots Joint velocity (rad/s) against Posture gain (1/s). Its series are Joint 1, Joint 2, Joint 3. Resulting task velocity plots Task velocity (m/s) against Posture gain (1/s). Its series are Actual x, Actual y, Desired x, Desired y.

The computed default record is Task velocity residual: 0.00696372 m/s; Secondary task leakage: 3.35421e-16 m/s; Joint velocity norm: 0.31833 rad/s. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Increase primary damping from zero to 0.5 while holding posture gain fixed. Compare task velocity residual and joint speed. Secondary leakage should remain near roundoff in normal mode because the exact projector is independent of primary damping.

2. Increase posture gain from zero to two per second at fixed damping. The joint velocities change, while normal task velocity stays at the primary value. In broken mode the task velocity changes with gain because the unprojected posture direction has a task component.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode bypasses the null projector and adds minus gain times the full posture vector to the primary command.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Restore the exact projector and defaults. Check actual task velocity, secondary leakage and joint velocity together; a low total joint speed alone cannot certify task preservation.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Alternative and limiting cases

At zero gain both modes coincide because no secondary motion is requested. At zero damping the full-row-rank primary inverse tracks the desired task to roundoff. The null projector is local to one configuration; finite motion requires recomputing it. No joint limits, collision constraints or integrated posture trajectory are claimed.

## Independent evidence and MATLAB-style design boundary

The reference derives the Jacobian by complex-step kinematics, computes the primary command with SVD and constructs the one-dimensional null basis from the cross product of the two Jacobian rows. It does not use the production pseudoinverse projector.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: At zero gain both modes coincide because no secondary motion is requested. At zero damping the full-row-rank primary inverse tracks the desired task to roundoff. The null projector is local to one configuration; finite motion requires recomputing it. No joint limits, collision constraints or integrated posture trajectory are claimed.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Focused check and teach-back

Why can the total task residual be nonzero while secondary leakage is essentially zero?

Answer rationale: The damped primary inverse trades tracking accuracy against joint speed. An exact null projector preserves that primary task velocity when posture motion is added; it does not undo the original damping residual.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.
