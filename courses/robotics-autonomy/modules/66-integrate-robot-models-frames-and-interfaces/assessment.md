# P66 course checkpoint

## Predict and derive

Trace one encoder value through units, frames and timestamp contracts.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `q_rad=c_encoder (2 pi/4096)(1+epsilon_scale) converts the typed joint interface exactly once`
- `T_base^tool=T_base^shoulder T_shoulder^elbow(q_1) T_elbow^tool(q_2) composes the declared frame graph`
- `e_tool=||p_model-p_measured||_2 and ||T T^{-1}-I||_F audit integration and group consistency separately`

## Controlled comparison

- `encoder_scale_error_percent`: 0.2 → 2.0. Hold the other controls at baseline and explain the mechanism before executing.
- `timestamp_skew_ms`: 8.0 → 35.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Correct forward kinematics can still consume mis-scaled angles or stale data; check interface validity separately from inverse consistency.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Self-inverse transform residuals alone cannot detect every frame mistake.

Competency links: SYSTEM-INTEGRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
