# P67 course checkpoint

## Predict and derive

Measure recovery latency from the actual accepted event sequence.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `x_hat_{k+1}=x_hat_k+v_hat_k Delta t_source propagates replay state in monotonic source time`
- `gap_k=t_source,k-t_source,k-1>60 ms and r_clock=t_remote-t_source diagnose missing data and clock drift`
- `x_hat_recovery=x_measured at the first valid checkpoint after safe hold bounds replay divergence`

## Controlled comparison

- `dropout_duration_ms`: 120.0 → 240.0. Hold the other controls at baseline and explain the mechanism before executing.
- `clock_drift_ppm`: 50.0 → 250.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Source time and arrival time serve different roles; stale rejection, gap detection and fresh-state recovery must be observable.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A synthetic replay is not middleware or clock-synchronization qualification.

Competency links: REALTIME-SAFETY, SYSTEM-INTEGRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
