# P47 course checkpoint

## Predict and derive

Explain free-space and occupied updates along a range ray.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `log_odds_next=clip(log_odds+inverse_sensor_evidence,-5,5)`
- `hit_evidence=log(p_hit/(1-p_hit)); traversed_free_evidence=-hit_evidence`
- `entropy=sum(-p*log2(p)-(1-p)*log2(1-p)) over grid cells`

## Controlled comparison

- `hit_probability`: 0.72 → 0.98. Hold the other controls at baseline and explain the mechanism before executing.
- `beam_count`: 90.0 → 360.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Only traversed cells receive free evidence and the endpoint receives occupied evidence; log odds accumulate bounded belief.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Repeated correlated scans do not provide independent probability evidence.

Competency links: RANGE-PERCEPTION, SLAM-MAPPING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
