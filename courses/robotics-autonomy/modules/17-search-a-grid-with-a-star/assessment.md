# P17 course checkpoint

## Predict and derive

Predict whether changing a heuristic preserves shortest-path optimality.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `f(n)=g(n)+w_h h(n)`
- `h=abs(dx)+abs(dy)`

## Controlled comparison

- Vary only `heuristic_weight` through [0, 1, 2]; predict Higher weight reduces expansions but can weaken optimality guarantees.
- Vary only `gap_offset` through [-7, 0, 7]; predict Safe path cost follows the wall-gap detour.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

An admissible estimate changes search order without overestimating remaining cost; obstacle occupancy determines feasibility independently.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Finite grid resolution can hide passages or inflate obstacles.

Competency links: GLOBAL-MOTION-PLANNING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
