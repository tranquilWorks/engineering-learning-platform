# P32 course checkpoint

## Predict and derive

Separate parameter fitting from held-out torque prediction.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `tau=0.08 qddot + [0.25 qddot+4.905 cos(q), qdot] theta`
- `theta_hat=argmin ||Y theta-y||²+0.02||theta-theta_prior||²`
- `heldout_error=tau_predicted-tau_true`

## Controlled comparison

- `excitation_amplitude_rad`: 0.7 → 1.5. Hold the other controls at baseline and explain the mechanism before executing.
- `payload_guess_kg`: 1.1 → 3.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Excitation determines regressor rank; fit residual and parameter error must be checked separately on new motion.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Low residual on an unexciting trajectory does not identify unique parameters.

Competency links: ROBOT-DYNAMICS. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
