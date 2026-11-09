# P56 course checkpoint

## Predict and derive

Trace heading integration and explain the sample-time factor in position correction.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `psi[k+1]=psi[k]+r[k]Delta_t`
- `p_predict[k+1]=p[k]+v[k][cos(psi[k]),sin(psi[k])]Delta_t`
- `p[k+1]=p_predict[k+1]+K_gps(p_gps[k+1]-p_predict[k+1])Delta_t`

## Controlled comparison

- `initial_heading_deg`: 15 → -10. Hold the other controls at baseline; predict and explain the change before executing.
- `gps_blend`: 0.12 → 0.25. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Yaw rate in degrees/s is converted to radians/s before multiplying by 0.05 s. Position prediction uses the previous heading and speed. The correction is gps_blend*dt*(GPS-prediction), so gps_blend acts as a rate in 1/s and its per-sample weight at 0.12 is 0.006. Changing the sample rate without retaining dt would change the observer. Separate integrated speed path length from the length of the GPS-corrected position curve.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This fixed-gain synthetic reconstruction is not a Kalman estimate or a calibrated GPS/IMU uncertainty model; deterministic perturbations are not measured GPS noise.

Competency links: VD-STATE-RECONSTRUCTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
