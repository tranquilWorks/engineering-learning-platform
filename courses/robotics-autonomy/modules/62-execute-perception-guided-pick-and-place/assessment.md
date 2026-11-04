# P62 course checkpoint

## Predict and derive

Trace observation, approach, grasp verification, transfer and release.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `p_b^o=t_b^c+R(theta_b^c+delta theta) p_c^o maps the visual estimate into the robot base frame`
- `cos(q_2)=(||p_b^o||^2-l_1^2-l_2^2)/(2 l_1 l_2) with q_1 from the analytic two-link branch`
- `grasp_ok=reachable and ||FK(q)-p_true||_2<=epsilon_gripper gates lift and transfer states`

## Controlled comparison

- `vision_noise_cm`: 1.2 → 5.0. Hold the other controls at baseline and explain the mechanism before executing.
- `camera_yaw_error_deg`: 0.8 → 5.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Every task transition must follow measured geometric or contact evidence; endpoint reachability alone cannot prove placement.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Planar kinematic execution omits full gripper and object-contact dynamics.

Competency links: VISION-PERCEPTION, MANIPULATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
