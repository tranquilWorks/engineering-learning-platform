# P13 course checkpoint

## Predict and derive

Compare exact planar arc integration with a straight-line approximation.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `Delta s=(Delta s_R+Delta s_L)/2`
- `Delta theta=(Delta s_R-Delta s_L)/b`

## Controlled comparison

- Vary only `encoder_cpr` through [128, 1024, 4096]; predict Quantization decreases with resolution but slip bias remains.
- Vary only `slip_percent` through [0, 2, 15]; predict Unmeasured wheel slip accumulates position and heading error.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Encoder increments determine both heading and displacement; rotation during a sample changes the world-frame endpoint.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Agreement under no-slip motion does not estimate wheel slip.

Competency links: MOBILE-KINEMATICS, STATE-ESTIMATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
