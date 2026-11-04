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
