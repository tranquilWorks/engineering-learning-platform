# P18 course checkpoint

## Predict and derive

Explain why node collision checks do not certify sampled-tree edges.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `q_new=q_near+min(eta,d) direction`
- `c(e)=min_alpha distance(segment(alpha), obstacle)-r`

## Controlled comparison

- Vary only `sample_budget` through [200, 700, 1200]; predict More samples increase the opportunity to connect through free space.
- Vary only `goal_bias` through [0.05, 0.15, 0.35]; predict Goal bias trades direct progress against detour exploration.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A valid connection must clear the entire segment; a tree path must follow actual parent links back to the start.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Finite sampling offers neither guaranteed success nor a universal optimality bound.

Competency links: GLOBAL-MOTION-PLANNING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
