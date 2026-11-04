# P12 course checkpoint

## Predict and derive

Recover a sensor transform and check a held-out point.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `p_B=R_BS p_S+t_BS+n`
- `t=mean(p_B)-R mean(p_S)`

## Controlled comparison

- Vary only `sensor_yaw_deg` through [-30, 0, 30]; predict Rigid calibration tracks yaw without structured residual.
- Vary only `noise_mm` through [0, 2, 20]; predict Parameter error and residual RMS grow with correspondence noise.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Rigid calibration must preserve distances and orientation; fit rotation and translation jointly and evaluate points outside the fit set.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Collinear or poorly spread observations can conceal calibration ambiguity.

Competency links: RIGID-BODY-GEOMETRY, SENSOR-MODELING-CALIBRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
