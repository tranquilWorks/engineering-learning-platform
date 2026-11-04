# P65 course checkpoint

## Predict and derive

Check vertex and edge-swap conflicts in a reservation schedule.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `R_v={(p_A(tau),t): abs(tau-t)<=b} reserves vertices across the temporal assurance buffer b`
- `(p_B(t),t)->(p_B(t+1),t+1) is admissible only outside R_v and every opposing edge reservation`
- `pi_B*=argmin g+h in the bounded space-time grid and d_min=min_t ||p_A(t)-p_B(t)||_2`

## Controlled comparison

- `reservation_buffer_steps`: 1.0 → 0.0. Hold the other controls at baseline and explain the mechanism before executing.
- `robot_b_start_delay_steps`: 0.0 → 2.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Robots can collide by sharing a cell or swapping cells during one step; waits and delayed starts remain part of the schedule.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Discrete reservations do not certify continuous physical separation.

Competency links: TASK-AUTONOMY, REALTIME-SAFETY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
