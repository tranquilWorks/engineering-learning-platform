# P55 course checkpoint

## Predict and derive

Invert sensor bias and scale before rotating to body axes, and explain why norm closure alone is insufficient.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `a_sensor=S_sensor R(-psi_mount)a_body+b_sensor`
- `a_body_hat=R(psi_mount)S_sensor^-1(a_sensor-b_sensor)`
- `yaw_body=yaw_measured-b_yaw`

## Controlled comparison

- `yaw_bias_deg_s`: 1.5 → -1.2. Hold the other controls at baseline; predict and explain the change before executing.
- `mounting_yaw_deg`: 8 → -12. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The forward sensor model scales R(-angle)*truth and then adds sensor bias. Inversion must subtract bias and divide channelwise by scale before applying R(angle). With the declared truth, corrected body acceleration returns (1.20,4.50) m/s² and corrected yaw returns 12 deg/s. A wrong rotation angle still preserves norm, so compare direction and truth residual too. Mixed acceleration and yaw errors use declared 1 m/s² and 1 deg/s scales.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Known synthetic calibration constants are applied, not identified from a real calibration campaign; uncertainty and three-dimensional gravity alignment are omitted.

Competency links: VD-MOTION-FRAMES, VD-STATE-RECONSTRUCTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
