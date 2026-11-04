# P56 course checkpoint

## Predict and derive

Verify that rewiring updates descendant costs as well as a parent pointer.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `q_new=Steer(q_nearest,q_sample,eta) subject to segment(q_nearest,q_new) subset C_free`
- `parent(q_new)=argmin_{q in Near}(J(q)+||q-q_new||)`
- `Rewire q when J(q_new)+||q_new-q||<J(q) and the connecting edge is free`

## Controlled comparison

- `sample_count`: 220.0 → 100.0. Hold the other controls at baseline and explain the mechanism before executing.
- `rewire_radius_m`: 1.6 → 3.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A better connection changes the entire subtree's accumulated cost; the final path must follow the revised ancestry.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A finite deterministic sample sequence is not an asymptotic optimality demonstration.

Competency links: GLOBAL-MOTION-PLANNING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
