# P63 course checkpoint

## Predict and derive

Compare base travel with arm dexterity for one target.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `p_target=[x_b,0]^T+FK_arm(q) couples base placement and arm inverse kinematics`
- `w(q)=l_1 l_2 |sin(q_2)| is the planar arm manipulability retained by each candidate placement`
- `(x_b*,q*)=argmin rho_b |x_b|+0.18/(w(q)+0.025) over reachable bounded base candidates`

## Controlled comparison

- `target_distance_m`: 1.8 → 2.1. Hold the other controls at baseline and explain the mechanism before executing.
- `base_motion_weight`: 0.7 → 2.5. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Moving the base changes relative target coordinates and arm conditioning; a weighted objective trades travel against singularity avoidance.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A configuration choice does not establish nonholonomic base trajectory feasibility.

Competency links: MOBILE-KINEMATICS, MANIPULATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
