# P61 course checkpoint

## Predict and derive

Distinguish force closure from supporting one selected external load.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `G_i=[f_{ix},f_{iy},(r_i cross f_i)/r_o]^T for both edges f_i=n_i+-mu t_i`
- `G alpha=0 with alpha_j>0 and rank(G)=3 is the planar positive-equilibrium force-closure test`
- `lambda*=argmin_{lambda>=0} ||G lambda-w_ext||_2^2 by projected gradient descent`

## Controlled comparison

- `friction_coefficient`: 0.6 → 0.25. Hold the other controls at baseline and explain the mechanism before executing.
- `contact_misalignment_deg`: 8.0 → 25.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Positive combinations of friction-cone wrenches must span all wrench directions for closure; one feasible load is weaker evidence.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Unbounded contact effort is not a grasp with finite actuator limits.

Competency links: PHYSICAL-INTERACTION, MANIPULATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
