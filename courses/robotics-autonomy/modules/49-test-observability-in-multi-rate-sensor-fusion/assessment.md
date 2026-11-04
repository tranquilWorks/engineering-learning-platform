# P49 course checkpoint

## Predict and derive

Predict which state direction becomes unobservable without excitation.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `h_p(t)=[1,t,double_integral(u),t^2/2], h_a(t)=[0,0,u(t),1]`
- `W=sum_k h_k^T R_k^-1 h_k`
- `rank(W)=n is structural observability; kappa(W) measures usable conditioning`

## Controlled comparison

- `rate_ratio`: 10.0 → 40.0. Hold the other controls at baseline and explain the mechanism before executing.
- `excitation_level`: 0.6 → 2.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The stacked whitened measurement rows determine rank; sample rate cannot recover a state absent from every row.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A numerical rank threshold is not a universal sensor-design criterion.

Competency links: STATE-ESTIMATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
