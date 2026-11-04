# P24 course checkpoint

## Predict and derive

Follow a delayed command through a watchdog and virtual plant.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `y_{k+1}=y_k+\Delta t(-y_k+u_k)/\tau`
- `a_k=t_k-t_{last};\quad a_k>T_w\Rightarrow u_k=0`

## Controlled comparison

- Vary only `io_latency_ms` through [0, 30, 100]; predict More interface delay increases phase lag and changes closed-loop peak response.
- Vary only `fault_duration_s` through [0.2, 1, 2]; predict Longer dropout holds the software safe command for more samples after watchdog detection.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Source age determines command validity; fail-zero behavior and plant response must be visible after packet loss.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Software-only HIL methodology is not physical HIL evidence.

Competency links: REALTIME-SAFETY, SYSTEM-INTEGRATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
