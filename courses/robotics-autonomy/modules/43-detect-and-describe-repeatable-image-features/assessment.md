# P43 course checkpoint

## Predict and derive

Explain why detected corners are not yet reliable correspondences.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `H=det(M)-0.04*trace(M)²; M=smooth(gradient(I)*gradient(I)^T)`
- `theta=atan2(sum(y*I),sum(x*I)) within a circular patch`
- `descriptor=(rotated_sampled_patch-mean)/norm; distance=||d1-d2||2`

## Controlled comparison

- `detector_threshold`: 0.12 → 0.8. Hold the other controls at baseline and explain the mechanism before executing.
- `image_rotation_deg`: 25.0 → 180.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Local gradient structure determines feature strength; descriptors require consistent sampling and a matching rule.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Repeatability on a generated scene is not invariance to every viewpoint.

Competency links: VISION-PERCEPTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
