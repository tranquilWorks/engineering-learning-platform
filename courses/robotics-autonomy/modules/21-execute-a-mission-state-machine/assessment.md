# P21 course checkpoint

## Predict and derive

Show which guard permits a mission-state transition.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `x_{k+1}=\delta(x_k,e_k)`
- `t-t_{enter}\ge T_{watchdog}`

## Controlled comparison

- Vary only `target_detect_s` through [0.5, 2, 8]; predict A late target can delay progress or let the SEARCH watchdog win.
- Vary only `fault_time_s` through [1, 5, 11]; predict Earlier faults shorten active execution and route immediately to SAFE.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

State, event and guard jointly determine the next action; a recovery transition must preserve or explicitly reset its evidence.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A finite mission model does not enumerate every field failure.

Competency links: TASK-AUTONOMY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
