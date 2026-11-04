# P57 course checkpoint

## Predict and derive

Check swept clearance after removing intermediate waypoints.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `t*=clip(((c-a)^T(b-a))/||b-a||^2,0,1)`
- `clearance(a,b)=min_j ||a+t*(b-a)-c_j||-r_j-r_robot`
- `Replace q_i...q_j by segment(q_i,q_j) only when clearance>=0 and length decreases`

## Controlled comparison

- `robot_radius_m`: 0.3 → 0.6. Hold the other controls at baseline and explain the mechanism before executing.
- `smoothing_iterations`: 30.0 → 1.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A shortcut can cross an inflated obstacle even when its endpoints are free; re-evaluate the full segment after smoothing.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Circular planar obstacles do not represent arbitrary articulated collision geometry.

Competency links: GLOBAL-MOTION-PLANNING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
