# P28 course checkpoint

## Predict and derive

Predict Jacobian rank near a straight or folded elbow.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `x=l1 cos(q1)+l2 cos(q1+q2); y=l1 sin(q1)+l2 sin(q1+q2); l1=1 m`
- `J=partial(x,y)/partial(q1,q2); task_velocity=J joint_velocity`
- `manipulability=sigma_max sigma_min=|det J|`

## Controlled comparison

- `elbow_angle_deg`: 70.0 → 175.0. Hold the other controls at baseline and explain the mechanism before executing.
- `link_ratio`: 0.8 → 1.5. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Singular values measure local directional mobility; finite perturbations of forward kinematics check derivative signs and link contributions.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A nonsingular instantaneous Jacobian does not ensure global reachability.

Competency links: MANIPULATOR-KINEMATICS. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.


# Retained scoped evidence task

## P28 evidence task

How do you distinguish a real position singularity from the omitted-column fault?

Before running: Predict what a missing elbow column does to task rank and to an independently differenced forward-kinematic check.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Position-task singular values plots Singular value (m/rad) against Elbow angle (deg). Its series are Largest, Smallest. Kinematic derivative check plots Jacobian difference (m/rad) against Elbow angle (deg). Its series are Central-difference residual.

### Reasoning rubric

- Model: use `x=l1 cos(q1)+l2 cos(q1+q2); y=l1 sin(q1)+l2 sin(q1+q2); l1=1 m` to reconstruct a quantity from the executed mechanism.
- Evidence: Sweep elbow angle from zero to 70 and then 175 degrees at fixed link ratio. Compare the smallest singular value near straight and nearly folded configurations. The graph covers every intermediate sampled elbow angle, so its starting point is singular even when the selected endpoint is not.
- Diagnosis: Broken mode omits the elbow Jacobian column while leaving the forward kinematics unchanged. The computed Jacobian loses a joint contribution and the finite-difference residual exposes it.
- Recovery and scope: Restore the second column, reset controls and compare both derivative agreement and task singular values. A small singular value at a truly aligned configuration is expected and should not be repaired by adding an arbitrary floor. State this limit: At elbow zero the correct position map is singular. The shoulder angle rotates the task axes without changing singular values. A derivative check has truncation and floating-point error; exact symbolic zero is not required. No orientation or dynamics claim follows from this position-only calculation.

### Check your explanation

At a real aligned configuration the correct analytic Jacobian still agrees with independently differentiated kinematics. The omitted column disagrees with a nonzero elbow derivative and causes rank loss even away from geometric alignment.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.
