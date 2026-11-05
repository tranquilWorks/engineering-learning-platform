# P63 course checkpoint

## Predict and derive

Derive offset-curve curvature and audit both geometric feasibility and the optimization objective.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `ds_offset=(1-offset*kappa)ds; kappa_offset=kappa/(1-offset*kappa)`
- `v=sqrt(11.5 m/s^2 / kappa_offset); time=sum(ds_offset/v) s`
- `objective=time+penalty*offset^2 with penalty in s/m^2 and |offset|<=bound`

## Controlled comparison

- `maximum_offset_m`: 3 → 1. Hold the other controls at baseline; predict and explain the change before executing.
- `smoothness_weight`: 0.02 → 0.06. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

For constant offset d, ds_offset=(1-d*kappa)*ds and kappa_offset=kappa/(1-d*kappa). The same denominator changes both length and curvature, so adjusting only one is inconsistent. Require positive offset Jacobian and the declared width bound. Compare time with time+penalty*d²; the penalty has units s/m². A finite scalar search over offsets is not a general spatially varying racing-line optimizer.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Track smoothness, vehicle width, linked transient steering and obstacle constraints are outside this constant-offset study.

Competency links: VD-PERFORMANCE-OPTIMIZATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
