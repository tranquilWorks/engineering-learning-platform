# P19 course checkpoint

## Predict and derive

Predict a moving-obstacle conflict using synchronized relative motion.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `r(t)=r_0+(v_o-v_r)t`
- `t_CPA=clip(-r_0 dot v_rel / norm(v_rel)^2,0,T)`

## Controlled comparison

- Vary only `obstacle_speed_m_s` through [0.2, 1, 2]; predict Changing crossing time can create or remove conflict.
- Vary only `prediction_horizon_s` through [2, 8, 10]; predict A short horizon can miss a later collision.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Evaluate robot and obstacle positions at the same future time and include stopping or waiting as an executed action.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A finite candidate set can miss a feasible avoidance maneuver.

Competency links: LOCAL-KINODYNAMIC-PLANNING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
