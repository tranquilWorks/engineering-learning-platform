# P30 course checkpoint

## Predict and derive

Derive joint torques from a specified end-effector wrench.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `v=J(q) qdot; tau=J(q)^T F`
- `joint_power=tau^T qdot; Cartesian_power=F^T v`
- `force_to_torque_gain=||J^T F_unit||`

## Controlled comparison

- `force_n`: 8.0 → 30.0. Hold the other controls at baseline and explain the mechanism before executing.
- `lever_arm_m`: 0.4 → 1.2. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Virtual work equates task and joint power, giving a Jacobian-transpose mapping with explicit force and moment units.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A static torque map does not include inertia, friction or saturation.

Competency links: ROBOT-DYNAMICS. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
