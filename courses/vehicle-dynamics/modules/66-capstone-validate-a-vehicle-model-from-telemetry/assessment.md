# P66 course checkpoint

## Predict and derive

Trace a telemetry requirement from exact bytes through synchronization, calibration, reconstruction and untouched validation.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `logger_time=(1+0.0008 f)*source_time+0.02f s; calibrate with known sync markers`
- `speed_reading=(1+0.02f)*speed+0.2f m/s; two-point calibration precedes reconstruction`
- `synthetic F=1450*a+0.45*v^2+2sin(0.9i) N; fit only chronological prefix`
- `covariance=residual_variance*(X^T X)^-1; normalize columns for information eigenvalues`

## Controlled comparison

- `validation_fraction`: 0.3 → 0.2. Hold the other controls at baseline; predict and explain the change before executing.
- `fault_severity`: 1 → 2. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Establish CAN/BLE payload identity before decoding, then fit clock rate/offset from the three explicit synchronization pairs. Apply the separate speed gain/bias calibration and yaw-bias correction before trajectory reconstruction. The force channel is synthetic 1450*a+0.45*v²+2*sin(0.9*i), not a claim about the fixture's IMU channel. Freeze the chronological fitting prefix before computing held-out residuals. For every passing requirement, identify its actual residual or event evidence and reproduce the injected fault and deterministic recovery.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Redundant CAN bytes enable the declared BLE recovery; missing both sources would not be recoverable by this mechanism. No measured vehicle, manual screen-reader, learner or hardware acceptance is implied.

Competency links: VD-IDENTIFICATION-UNCERTAINTY, VD-SYSTEM-INTEGRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
