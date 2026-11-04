# P22 course checkpoint

## Predict and derive

Compute a deadline miss from release, execution and response time.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `U=\sum_i C_i/T_i`
- `R_i=C_i+\sum_{j\in hp(i)}\lceil R_i/T_j\rceil C_j`

## Controlled comparison

- Vary only `control_wcet_ms` through [1, 5, 10]; predict More control execution consumes capacity and increases lower-priority interference.
- Vary only `perception_wcet_ms` through [5, 18, 30]; predict More perception execution lengthens planning response and can consume its deadline margin.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Interference and blocking affect completion time; utilization alone does not prove every job meets its deadline.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A simulated schedule is not a real operating-system latency measurement.

Competency links: REALTIME-SAFETY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
