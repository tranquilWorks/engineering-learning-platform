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


# Retained scoped evidence task

## P47 evidence task

Why should the endpoint-only fault be described as missing free-space evidence rather than creating false-free cells?

Before running: Predict what an endpoint-only mapper can know about the free cells crossed by a beam, and distinguish unknown space from a false occupied measurement.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Occupancy probability plots World y (m) against World x (m). Its series are Map, Hits. Central grid section plots Occupancy (1) against World x (m). Its series are Prob., Truth.

### Reasoning rubric

- Model: reconstruct a displayed value using `log_odds_next=clip(log_odds+inverse_sensor_evidence,-5,5)` and the actual state or geometry.
- Evidence: Increase the inverse-model hit probability at a fixed beam count. Reconstruct one hit and one free log-odds update, then inspect entropy and the unconfirmed-free fraction without treating stronger confidence as new independent data.
- Diagnosis: The mapper records occupied endpoints but skips the free cells that each ray actually traversed. It preserves beam geometry and evidence strength.
- Recovery and scope: Restore free-cell evidence, reset the prior grid and replay the same beams. Check whole probability rows and ray paths as well as aggregate entropy. State this boundary: Unobserved and occluded cells retain their prior; the unconfirmed-free fraction deliberately includes them and should not be read as a visible-cell false-positive rate. Known sensor pose, deterministic ranges, independent-cell updates and repeated-ray evidence are simplifying assumptions. Marginal entropy reduction does not prove calibrated joint uncertainty.

### Check your explanation

Its omitted negative updates leave crossed free cells at the 0.5 prior. They remain unknown; the algorithm has not asserted that occupied cells are free. The metric must describe the posterior that was actually produced.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
