# P59 course checkpoint

## Predict and derive

Reconstruct position and velocity from every bounded acceleration action.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `x_{k+1}=x_k+v_k Delta t+0.5 a_k Delta t^2`
- `v_{k+1}=v_k+a_k Delta t with |a_k|<=a_max and 0<=v_k<=v_max`
- `goal={(x,v) | |x-x_goal|<=epsilon_x and |v|<=epsilon_v}`

## Controlled comparison

- `acceleration_limit_m_s2`: 1.0 → 2.0. Hold the other controls at baseline and explain the mechanism before executing.
- `speed_limit_m_s`: 2.0 → 1.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A kinodynamic state includes velocity; reaching the target at nonzero speed is a different goal from terminal rest.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A finite lattice can fail to represent a feasible continuous trajectory.

Competency links: LOCAL-KINODYNAMIC-PLANNING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
