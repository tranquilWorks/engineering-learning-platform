# P20 course checkpoint

## Predict and derive

Reconstruct a behavior-tree tick from child status and traversal order.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `s_{seq}=s_j\;\text{for the first child }j\text{ not returning SUCCESS}`
- `p_{k+1}=p_k+1\;\text{while an action remains RUNNING}`

## Controlled comparison

- Vary only `navigate_ticks` through [2, 5, 10]; predict Longer navigation delays every downstream child while preserving the sequence order.
- Vary only `retry_limit` through [0, 3, 6]; predict Too few retries cause explicit failure; enough retries allow the scripted grasp success.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Sequence and fallback nodes propagate running, success and failure differently; trace which children actually execute.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A diagram without tick semantics cannot establish recovery behavior.

Competency links: TASK-AUTONOMY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
