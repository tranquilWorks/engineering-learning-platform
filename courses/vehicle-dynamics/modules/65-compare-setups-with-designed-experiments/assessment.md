# P65 course checkpoint

## Predict and derive

Recover factorial main and interaction effects and test genuinely unused setup combinations.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `synthetic T=90-2a*x1-3t*x2-1.2at*x1*x2 s`
- `time-reduction effects=-2 beta1,-2 beta2,-4 beta12 s`
- `unused-point RMS=sqrt(mean((T_predicted-T_synthetic)^2)) s; held-out points are not training corners`

## Controlled comparison

- `aero_scale`: 1 → 0.8. Hold the other controls at baseline; predict and explain the change before executing.
- `tire_scale`: 1 → 1.15. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

For T=90-2*a*x1-3*t*x2-1.2*a*t*x1*x2, changing coded x1 from -1 to +1 changes the averaged response by -4*a seconds. The difference-in-differences is -4.8*a*t seconds. Omitting the interaction can fit some comparisons while failing others. Fit on the four corners, then evaluate the separate unused points without refitting. Distinguish fitted coefficients from time-reduction effects with their factor-of-two and factor-of-four conventions.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The response surface is a declared synthetic law; it is not a causal conclusion from randomized real track tests.

Competency links: VD-PERFORMANCE-OPTIMIZATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
