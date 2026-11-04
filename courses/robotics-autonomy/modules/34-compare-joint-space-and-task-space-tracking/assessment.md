# P34 course checkpoint

## Predict and derive

Compare joint-space tracking with task-space error under the same plant.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `qdot_joint=k(q_goal-q)`
- `qdot_task=J(q)^+ k(x_goal-x(q))`
- `applied_qdot=clip(requested_qdot,-2,2)`

## Controlled comparison

- `jacobian_condition`: 4.0 → 40.0. Hold the other controls at baseline and explain the mechanism before executing.
- `joint_gain_per_s`: 3.0 → 10.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Joint errors map through geometry; task commands need a consistent Jacobian and can demand large rates near singularity.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A task-space path is not automatically actuator-feasible.

Competency links: MANIPULATOR-KINEMATICS, ACTUATION-JOINT-CONTROL. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P34 evidence task

Why is the peak control output a joint speed rather than a torque, and why can transpose feedback still reduce error?

Before running: Predict why a Jacobian-transpose descent law can move toward the target without matching the Cartesian convergence of an inverse velocity map.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Joint tracking errors plots Joint error (rad) against Time (s). Its series are Joint servo, Task servo. Cartesian tracking errors plots Position error (m) against Time (s). Its series are Joint servo, Task servo.

### Reasoning rubric

- Model: reconstruct a displayed value using `qdot_joint=k(q_goal-q)` and the actual state or geometry.
- Evidence: Increase feedback gain at fixed geometry. Observe convergence and whether velocity clipping becomes active. A faster requested response need not yield proportionally faster applied motion once rates saturate.
- Diagnosis: The Cartesian controller uses a Jacobian-transpose gradient direction instead of inverse velocity mapping. The joint-space comparison and actual rate limits remain unchanged.
- Recovery and scope: Restore inverse mapping and reset the initial state. Compare complete error curves and applied joint speeds, not just one final position. State this boundary: At zero Cartesian error both mappings command zero motion, so a settled target does not distinguish them. The experiment assumes ideal velocity servos, a fixed local goal branch and no collision or torque constraints. Near singularities, rate clipping changes the nominal exponential error law.

### Check your explanation

The integrated plant is qdot equal to the applied velocity command, with no mass or torque equation. The transpose is a gradient direction for endpoint error, but its task response is weighted by J J transpose and does not implement the inverse velocity law.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
