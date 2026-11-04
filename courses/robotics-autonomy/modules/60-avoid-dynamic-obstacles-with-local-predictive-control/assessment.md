# P60 course checkpoint

## Predict and derive

Explain why a short prediction horizon changes avoidance decisions.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `y_{k+1}=y_k+v_{y,k+1}Delta t and v_{y,k+1}=sat(v_{y,k}+a_{y,k}Delta t)`
- `p^o_{k+j|k}=p^o_k+j Delta t v^o with ||p^r_{k+j|k}-p^o_{k+j|k}||>=r_safe`
- `a_k=first(argmin sum_j(J_goal+J_cross-track+J_separation)+J_control)`

## Controlled comparison

- `prediction_horizon_steps`: 15.0 → 5.0. Hold the other controls at baseline and explain the mechanism before executing.
- `obstacle_speed_m_s`: 0.55 → 1.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The selected acceleration is applied to the plant and the horizon is recomputed; a frozen-obstacle prediction uses the wrong future state.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Finite sampled predictions do not automatically certify between-sample clearance.

Competency links: LOCAL-KINODYNAMIC-PLANNING, REALTIME-SAFETY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
