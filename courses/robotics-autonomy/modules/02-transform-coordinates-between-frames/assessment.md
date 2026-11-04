# P02 course checkpoint

## Predict and derive

Compose two planar frame changes and reverse their order.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `p_W=R(theta)p_B+t_WB`
- `p_B=R(theta)^T(p_W-t_WB)`

## Controlled comparison

- Vary only `heading_deg` through [-90, 30, 120]; predict The point rotates around the robot origin.
- Vary only `point_x_m` through [-1, 1.2, 2.5]; predict The vector length from robot origin is preserved.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Translation rotates with its parent frame; use the inverse transform for a round trip, not a negated translation in the wrong frame.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A valid inverse does not prove the transform represents a calibrated sensor.

Competency links: RIGID-BODY-GEOMETRY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
