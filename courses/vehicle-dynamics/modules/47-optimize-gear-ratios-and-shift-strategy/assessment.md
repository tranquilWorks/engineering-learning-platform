# P47 course checkpoint

## Predict and derive

Explain gear selection at a shared road speed and account for resistance during torque interruption.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `n_e=60 v i_g i_0/(2 pi r_t)`
- `g_selected=argmax_g F_wheel(g) subject to 1500<=n_e<=7000`
- `v_dot=(F_selected-F_resist)/m with F_selected=0 during shift delay`

## Controlled comparison

- `final_drive_ratio`: 4.1 → 4.6. Hold the other controls at baseline; predict and explain the change before executing.
- `shift_delay_s`: 0.25 → 0.5. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

For each gear compute rpm=v*G*final_drive*60/(2*pi*r), reject rpm outside 1500–7000, and compare valid wheel forces. A shift sets drive force to zero for the declared delay, but rolling and aerodynamic resistance still decelerate the car. At 20 m/s the declared resistance is 180+0.38*400=332 N, giving -0.22897 m/s² for 1450 kg during interruption. Compare the full speed history and redline excess, not just the target time.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

This greedy force-based strategy is not a globally optimal shift schedule, and the simulation starts at 5 m/s. A horizon target-time value is censored unless the reached flag is true.

Competency links: VD-POWERTRAIN. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
