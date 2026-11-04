# P10 course checkpoint

## Predict and derive

Predict position drift from a constant accelerometer bias.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `delta theta=b_g t`
- `delta p=(1/2)b_a t^2`

## Controlled comparison

- Vary only `gyro_bias_deg_s` through [0, 0.2, 1]; predict Angle drift scales linearly with gyro bias.
- Vary only `accel_bias_m_s2` through [0, 0.03, 0.1]; predict Velocity is linear and position quadratic in time.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Velocity bias grows linearly and position bias quadratically with coast time; angular and translational errors have different units.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This one-axis drift study does not execute full inertial navigation.

Competency links: SENSOR-MODELING-CALIBRATION, STATE-ESTIMATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
