# P18 course checkpoint

## Predict and derive

Explain exactly which state a GPS position correction changes and which IMU error continues to accumulate.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `p_minus=p+v*dt+0.5*(a+b)*dt^2; v+= (a+b)*dt; p=p_minus+w*(p_gps-p_minus)`

## Controlled comparison

- `gps_weight`: 0.25 → 0. Hold the other controls at baseline; predict and explain the change before executing.
- `imu_bias_m_s2`: 0.05 → 0.3. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

At a 0.5 s sample interval, an acceleration bias of 0.05 m/s² adds 0.025 m/s of velocity error each prediction step. The complementary correction pulls position toward GPS, but does not directly repair the integrated velocity bias. Raising GPS weight can reduce position drift while increasing sensitivity to GPS error or delay. Diagnose a delayed observation by its timestamp and residual, not just the final position.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This is a fixed-gain position correction, not a Kalman filter, bias observer or stochastic sensor validation.

Competency links: VD-STATE-RECONSTRUCTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
