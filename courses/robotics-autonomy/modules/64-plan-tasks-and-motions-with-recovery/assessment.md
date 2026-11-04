# P64 course checkpoint

## Predict and derive

Demonstrate recovery after a motion edge becomes infeasible.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `pi*=argmin_pi sum_{e in pi} c(e) subject to symbolic preconditions and predicted motion clearance`
- `m_e=w_actual-w_required(e) is the execution-time geometric feasibility margin for each carry edge`
- `E_failed is blacklisted and pi_recovery=search(s_certified,goal,E without E_failed)`

## Controlled comparison

- `corridor_width_m`: 0.27 → 0.31. Hold the other controls at baseline and explain the mechanism before executing.
- `geometry_error_cm`: 5.0 → 9.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The symbolic plan must use geometric feasibility and retain the actual execution state when selecting an alternative.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Exhausting all alternatives must report failure rather than invent success.

Competency links: TASK-AUTONOMY, MANIPULATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
