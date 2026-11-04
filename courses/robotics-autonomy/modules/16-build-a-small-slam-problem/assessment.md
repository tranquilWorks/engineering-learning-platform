# P16 course checkpoint

## Predict and derive

Identify the unknown landmark and the global translation gauge.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `x_i-x_(i-1)=u_i+n_i`
- `l-x_i=z_i+v_i`

## Controlled comparison

- Vary only `odometry_sigma_m` through [0.01, 0.05, 0.3]; predict Odometry weighting trades against landmark factors.
- Vary only `range_sigma_m` through [0.02, 0.1, 0.5]; predict Landmark coupling weakens as range uncertainty grows.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Odometry constrains differences; landmark observations couple pose and map variables; one absolute anchor removes the common translation ambiguity.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The linear one-dimensional graph does not establish nonlinear planar SLAM.

Competency links: SLAM-MAPPING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
