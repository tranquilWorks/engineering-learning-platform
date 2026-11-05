# P27 course checkpoint

## Predict and derive

Identify longitudinal stiffness and peak friction from different regimes and reserve unused slip samples for validation.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `F_x=clip(C_kappa*kappa,-mu*F_z,mu*F_z)`
- `C_kappa_hat=argmin sum(F_x-C*kappa)^2 on unsaturated samples`
- `mu_hat=max(|F_x|)/F_z`

## Controlled comparison

- `longitudinal_stiffness_n`: 80000 → 130000. Hold the other controls at baseline; predict and explain the change before executing.
- `peak_friction`: 1.15 → 0.75. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The low-slip slope identifies stiffness while saturated observations identify mu*Fz. A peak alone cannot identify the initial slope. Slip 0.10 is a ratio, not the numeric percent 10; confusing them changes the inferred scale by 100. Fit on the designated observations, then calculate unused-point residuals without refitting. Explain why a dataset entirely inside the linear region cannot independently identify a saturation peak.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Piecewise clipping is a synthetic calibration target, not a smooth measured tire fit with parameter covariance.

Competency links: VD-TIRE-LONG. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
