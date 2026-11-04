# P68 course checkpoint

## Predict and derive

Connect a sensor observation to map, state estimate, route and executed motion.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `occupancy receives source-ordered range observations within 2.5 m before A* replanning`
- `tau=clip(-r dot d/(d dot d),0,1); separation=norm(r+tau*d) m over each 1 s segment`
- `1 Hz motion decision holds when range age>0.6 s; fresh post-gap source and motion prove resume`

## Controlled comparison

- `range_dropout_percent`: 10.0 → 40.0. Hold the other controls at baseline and explain the mechanism before executing.
- `dynamic_obstacle_speed_m_s`: 0.3 → 0.55. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Map and estimator outputs must feed planning and control; assess freshness, swept clearance, goal progress and recovery separately.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A bounded deterministic mission does not establish field autonomy or safety certification.

Competency links: SLAM-MAPPING, LOCAL-KINODYNAMIC-PLANNING, SYSTEM-INTEGRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
