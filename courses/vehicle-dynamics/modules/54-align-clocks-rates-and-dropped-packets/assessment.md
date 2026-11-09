# P54 course checkpoint

## Predict and derive

Apply the known clock offset before interpolation and quantify the gaps created by drops.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `t_aligned=t_source-delta_t`
- `missing={k where t_k is absent from the declared grid}`
- `x_grid=bounded_linear_interpolation(t_aligned,x)`

## Controlled comparison

- `clock_offset_ms`: 12 → -18. Hold the other controls at baseline; predict and explain the change before executing.
- `drop_period`: 7 → 10. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Source time equals reference time plus the declared offset. At 12 ms, subtract 0.012 s before resampling; this example applies a known offset rather than estimating it from data. The base period is 20 ms and an isolated missing interior sample creates a 40 ms interpolation span. Record maximum gap and interpolation error separately. Endpoint extension by the interpolator is not a new measurement.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

There is no clock drift estimation, latency distribution or anti-alias filtering here. P66 adds explicit synchronization markers for an affine clock fit.

Competency links: VD-TELEMETRY-PROTOCOL. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
