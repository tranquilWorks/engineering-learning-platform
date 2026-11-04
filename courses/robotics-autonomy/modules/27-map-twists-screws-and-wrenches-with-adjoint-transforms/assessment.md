# P27 course checkpoint

## Predict and derive

Preserve mechanical power while changing twist and wrench frames.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `V=[omega;v]; W=[moment;force]; power=W^T V`
- `Ad_T=[[R,0],[[t]cross R,R]]; V_A=Ad_T V_B`
- `W_A=Ad_T^-T W_B; pitch=omega·v/(omega·omega)`

## Controlled comparison

- `lever_arm_m`: 0.45 → 1.5. Hold the other controls at baseline and explain the mechanism before executing.
- `angular_speed_rad_s`: 1.8 → 6.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Angular and linear velocity transform together with the lever-arm term; the dual wrench map preserves their scalar power product.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Omitting translation can remain hidden when force or angular velocity is zero.

Competency links: RIGID-BODY-GEOMETRY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
