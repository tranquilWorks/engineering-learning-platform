# P06 course checkpoint

## Predict and derive

Separate speed tracking, saturation and integral windup.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `u_k=K_p e_k+K_i I_k`
- `I_(k+1)=I_k+T_s e_k`

## Controlled comparison

- Vary only `kp_v_per_rad_s` through [0.5, 1.5, 3.5]; predict Proportional gain changes the first correction.
- Vary only `ki_v_per_rad` through [0.5, 4, 10]; predict Integral gain changes residual error and saturation.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Accumulated error can demand unavailable voltage; recovery depends on the stored integral as well as the present speed error.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A deterministic speed step is not a robustness certificate for every load.

Competency links: ACTUATION-JOINT-CONTROL. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
