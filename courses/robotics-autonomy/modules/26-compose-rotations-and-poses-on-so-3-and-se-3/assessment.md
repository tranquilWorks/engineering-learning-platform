# P26 course checkpoint

## Predict and derive

Compare rigid pose composition with elementwise matrix interpolation.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `T=[R,t;0,1]; p_A=T_AB p_B`
- `T^-1=[R^T,-R^T t;0,1] only when R^T R=I`
- `R_blend(f)=(1-f)I+f Rz(theta)`

## Controlled comparison

- `rotation_angle_deg`: 35.0 → 170.0. Hold the other controls at baseline and explain the mechanism before executing.
- `translation_m`: 0.6 → 2.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Proper rotations preserve orthogonality and determinant one; translation and rotation composition generally do not commute.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A valid SE(3) matrix does not establish a correct sensor-frame convention.

Competency links: RIGID-BODY-GEOMETRY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
