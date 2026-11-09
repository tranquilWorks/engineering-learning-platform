# P29 course checkpoint

## Predict and derive

Derive the combined-slip projection and show why the two pure-slip maxima cannot generally coexist.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `F_x0=mu*F_z*tanh(C_kappa*kappa/(mu*F_z))`
- `F_y0=-mu*F_z*tanh(C_alpha*alpha/(mu*F_z))`
- `u_0=sqrt((F_x0/(mu*F_z))^2+(F_y0/(mu*F_z))^2)`
- `[F_x,F_y]=min(1,1/u_0)*[F_x0,F_y0]`

## Controlled comparison

- `slip_ratio`: 0.12 → 0.28. Hold the other controls at baseline; predict and explain the change before executing.
- `slip_angle_deg`: 8 → 17. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Compute the unconstrained longitudinal and lateral forces first. If their norm exceeds mu*Fz, apply one common scale factor so their ratio is preserved. For equal requested components each at capacity, utilization is sqrt(2); correct projection reduces each to capacity/sqrt(2). The broken independent-channel result can look individually plausible while exceeding the shared contact budget. Compare both force components and the combined utilization.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A friction circle is a bounded allocation model, not a validated friction ellipse or a transient brush model.

Competency links: VD-TIRE-LONG, VD-TIRE-LAT, VD-HANDLING-NONLINEAR. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
