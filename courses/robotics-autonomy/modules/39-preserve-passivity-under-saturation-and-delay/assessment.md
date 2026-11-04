# P39 course checkpoint

## Predict and derive

Audit the energy tank when saturation and delayed commands occur.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `work_k=F_applied,k*v_k*dt; E_next=E-work_k`
- `F_requested=-900*x_delayed-0.4*v_delayed`
- `positive_work_applied=min(positive_work_requested,E_available)`

## Controlled comparison

- `round_trip_delay_ms`: 18.0 → 120.0. Hold the other controls at baseline and explain the mechanism before executing.
- `force_limit_n`: 25.0 → 80.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Applied work, not requested work, must be charged to the tank; a nonnegative energy record requires actual command limiting.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A discrete tank model is not a physical passivity certificate.

Competency links: PHYSICAL-INTERACTION, REALTIME-SAFETY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
