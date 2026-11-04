# P54 course checkpoint

## Predict and derive

Trace a changed edge through incremental search state.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `rhs(s_start)=0 and rhs(s)=min_{s' in Pred(s)}(g(s')+c(s',s))`
- `key(s)=[min(g,rhs)+w h(s,s_goal), min(g,rhs)]`
- `A changed edge is repaired until top_key>=key(goal) and rhs(goal)=g(goal)`

## Controlled comparison

- `grid_resolution_m`: 0.5 → 1.0. Hold the other controls at baseline and explain the mechanism before executing.
- `heuristic_weight`: 1.0 → 0.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Reusable cost-to-come and one-step lookahead values must be made consistent after a map change; compare with a cold search.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Weighted heuristics and tie rules affect expansion counts and optimality claims.

Competency links: GLOBAL-MOTION-PLANNING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
