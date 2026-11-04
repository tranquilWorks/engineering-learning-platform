# P09 course checkpoint

## Predict and derive

Estimate encoder resolution and the speed ripple caused by quantization.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `C_k=round(4N theta_k/(2pi))`
- `theta_hat=2pi C_k/(4N)`

## Controlled comparison

- Vary only `counts_per_rev` through [128, 1024, 4096]; predict Resolution changes quantization error.
- Vary only `sample_rate_hz` through [10, 50, 200]; predict Count increments per sample change speed steps.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Position increments are discrete counts; differentiation divides quantization error by sample time and can amplify it.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Higher sampling alone cannot create additional encoder resolution.

Competency links: SENSOR-MODELING-CALIBRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
