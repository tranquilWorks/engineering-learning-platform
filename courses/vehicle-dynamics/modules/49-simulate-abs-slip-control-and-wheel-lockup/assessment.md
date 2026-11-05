# P49 course checkpoint

## Predict and derive

Derive brake torque from slip-rate control and identify the low-speed boundary of the simulation.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `kappa=(v-r omega)/max(v,0.5)`
- `I omega_dot=F_x r-T_brake and m v_dot=-F_x`
- `T_brake=F_x r+(I/r)[v k(kappa_target-kappa)-(1-kappa)v_dot]`

## Controlled comparison

- `target_slip`: 0.15 → 0.2. Hold the other controls at baseline; predict and explain the change before executing.
- `brake_torque_nm`: 2200 → 3000. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

With slip=1-r*omega/v, differentiate using wheel torque balance J*omega_dot=r*Fx-Tb and vehicle deceleration -Fx/m. The controller chooses torque to drive slip toward its target, subject to the requested-torque ceiling. Here target_slip also locates the synthetic tire-force peak, so sweeping it changes plant and controller together; it is not an independent target-optimization experiment. The wheel-speed projection at zero introduces a reaction not captured by the free wheel equation.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The 0.1 m/s floor and four-second horizon preclude interpreting accumulated distance as an exact physical stopping distance. Above-2-m/s diagnostics are distinct from low-speed behavior.

Competency links: VD-BRAKES. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
