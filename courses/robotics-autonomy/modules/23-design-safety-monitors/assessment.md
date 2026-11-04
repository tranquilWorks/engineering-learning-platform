# P23 course checkpoint

## Predict and derive

Distinguish detection time from achieving a safe state.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `d_{req}=v t_r+v^2/(2a)+m`
- `v_{k+1}=\max(0,v_k-a\Delta t)`

## Controlled comparison

- Vary only `command_speed_m_s` through [0.5, 2, 3]; predict Braking distance grows quadratically with speed and moves intervention earlier.
- Vary only `reaction_time_s` through [0, 0.2, 0.8]; predict Longer reaction bounds add linear travel to the required envelope.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

A monitor must observe a relevant fault, decide within its threshold and cause a bounded fallback; inspect the actual state after the alarm.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Passing injected faults is not safety certification or complete fault coverage.

Competency links: REALTIME-SAFETY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
