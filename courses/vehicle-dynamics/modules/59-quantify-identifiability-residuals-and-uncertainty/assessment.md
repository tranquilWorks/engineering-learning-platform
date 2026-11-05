# P59 course checkpoint

## Predict and derive

Audit singular values, residual correlation and conditional uncertainty before interpreting parameter accuracy.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `kappa(X)=sigma_max(X)/sigma_min(X)`
- `r=y-X theta_hat`
- `Cov(theta_hat)=sigma_force^2 pinv(X^T X)`

## Controlled comparison

- `excitation_level`: 0.7 → 0.35. Hold the other controls at baseline; predict and explain the change before executing.
- `noise_sigma_n`: 80 → 140. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Scaling every excitation by c scales singular values by c and parameter standard deviations by 1/c at fixed force-noise sigma; the condition number need not change. Compute covariance through the SVD of X, not an inverse of X transpose X that squares conditioning. The displayed truth-containment fraction counts only two known synthetic coefficients, so it can be 0, 0.5 or 1; it is not repeated-trial 95 percent coverage. Correlated residuals challenge the independent-noise covariance assumption.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Full rank and narrow conditional intervals do not remove model-form error, noise correlation or inadequate real-world excitation.

Competency links: VD-IDENTIFICATION-UNCERTAINTY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
