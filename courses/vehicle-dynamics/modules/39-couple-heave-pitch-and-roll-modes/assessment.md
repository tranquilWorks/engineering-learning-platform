# P39 course checkpoint

## Predict and derive

Derive chassis modes from corner spring energy and interpret modal participation without mixing metres and radians.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `K=sum_i k_i q_i q_i^T`
- `K phi=lambda M phi`
- `f_n=sqrt(lambda)/(2 pi)`

## Controlled comparison

- `front_spring_rate_n_m`: 42000 → 56000. Hold the other controls at baseline; predict and explain the change before executing.
- `rear_spring_rate_n_m`: 38000 → 52000. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Corner displacement is z+x*theta+y*phi, so its energy contributes k*b*b transpose to stiffness with b=[1,x,y]. Solve K*phi=omega²*M*phi. A raw heave displacement cannot be compared directly with a pitch angle. Instead, modal kinetic-energy fractions are M_jj*phi_j² divided by phi transpose M phi and sum to one. The residual and coupling use mass-weighted coordinates so force and moment units are not mixed. Deleting off-diagonal stiffness changes physical eigen residuals even if all frequencies remain positive.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Three linear rigid-body modes exclude unsprung wheel hop, nonlinear dampers, frequency-dependent bushings and measured modal correlation.

Competency links: VD-RIDE-SUSPENSION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
