# P20 course checkpoint

## Predict and derive

Explain why speed diversity is needed to identify both rolling resistance and quadratic drag.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `F=F_roll+0.5*rho*CdA*v^2+e; CdA=2*slope/rho`

## Controlled comparison

- `speed_span_m_s`: 20 → 2. Hold the other controls at baseline; predict and explain the change before executing.
- `force_noise_n`: 20 → 100. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Regress resistance against a constant column and v². If every speed is the same, those columns are dependent: many intercept/drag pairs fit the data. Separate estimation samples from held-out samples before solving. A rank-deficient branch returning a zero coefficient or standard-error placeholder has not established exact knowledge. Report rank and excitation alongside residuals, and predict why a wider speed span improves parameter separation.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Despite the inherited title, this drive is synthetic. Neither fitted coefficients nor residuals establish a real vehicle's road loads.

Competency links: VD-IDENTIFICATION-UNCERTAINTY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
