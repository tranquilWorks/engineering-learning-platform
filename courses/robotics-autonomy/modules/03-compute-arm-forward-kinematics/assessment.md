# P03 course checkpoint

## Predict and derive

Predict the endpoint with the elbow straight and then folded.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `p_e=L_1[cos(q_1),sin(q_1)]`
- `p_t=p_e+L_2[cos(q_1+q_2),sin(q_1+q_2)]`

## Controlled comparison

- Vary only `joint1_deg` through [-60, 35, 120]; predict The whole arm rotates about the base.
- Vary only `joint2_deg` through [-120, -45, 60]; predict The tool circles a fixed elbow.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Ordered rotations produce a sum of link vectors; equal links can cancel at a folded elbow although joint angles remain finite.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Planar rigid links omit compliance and joint offsets.

Competency links: MANIPULATOR-KINEMATICS. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
