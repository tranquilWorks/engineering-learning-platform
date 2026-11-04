# P35 course checkpoint

## Predict and derive

Explain the effect of payload mismatch on computed-torque compensation.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `M(q) qddot+C(q,qdot) qdot+g(q)=tau_applied`
- `tau_requested=(1+epsilon)[M(a_d+2w(v_d-v)+w²(q_d-q))+Cv+g]`
- `tau_applied=clip(tau_requested,-20,20)`

## Controlled comparison

- `model_error_fraction`: 0.08 → 0.6. Hold the other controls at baseline and explain the mechanism before executing.
- `tracking_bandwidth_per_s`: 3.0 → 8.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Model cancellation uses inertia, coupling and gravity; feedback corrects residual error only within available effort.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Nominal cancellation is not robust to arbitrary model mismatch.

Competency links: ROBOT-DYNAMICS, ACTUATION-JOINT-CONTROL. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
