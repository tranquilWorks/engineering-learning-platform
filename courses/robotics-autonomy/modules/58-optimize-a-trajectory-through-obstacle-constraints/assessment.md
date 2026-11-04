# P58 course checkpoint

## Predict and derive

Separate objective reduction from feasibility restoration.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `J(Q)=w_s sum_i||q_{i-1}-2q_i+q_{i+1}||^2+w_l sum_i||q_{i+1}-q_i||^2`
- `phi_i=max(0,r_obstacle+r_clearance-||q_i-c||)^2`
- `Q_{k+1}=Project_Cfree(Q_k-alpha grad(J+w_o sum_i phi_i)) with fixed endpoints`

## Controlled comparison

- `required_clearance_m`: 0.35 → 0.8. Hold the other controls at baseline and explain the mechanism before executing.
- `smoothness_weight`: 18.0 → 3.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A smoother path can violate obstacle constraints; inspect every segment and retain fixed endpoints during updates.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Local constrained optimization does not prove global path optimality.

Competency links: GLOBAL-MOTION-PLANNING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
