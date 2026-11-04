# P04 course checkpoint

## Predict and derive

Explain why an unreachable target must be rejected before clipping the cosine.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `c_2=(x_d^2+y_d^2-L_1^2-L_2^2)/(2L_1L_2)`
- `q_1=atan2(y_d,x_d)-atan2(L_2 sin(q_2),L_1+L_2 cos(q_2))`

## Controlled comparison

- Vary only `target_x_m` through [0.4, 1, 1.4]; predict Conditioning changes near the reach boundary.
- Vary only `target_y_m` through [-0.8, 0.4, 1]; predict The shoulder follows the target quadrant.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The annular workspace has both inner and outer boundaries; elbow branches can share an endpoint while differing in joint configuration.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A small algebraic residual does not establish collision-free motion.

Competency links: MANIPULATOR-KINEMATICS. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
