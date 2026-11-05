# P45 course checkpoint

## Predict and derive

Derive reflected inertia from kinetic energy and distinguish a censored target time from a completed launch.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `m_eq=sum(J_k i_k^2/r_t^2)`
- `a=(min(T_e i_g i_0 eta/r_t,F_tire)-F_resist)/(m+m_eq)`
- `W_drive-W_resist=Delta(E_translation+E_rotation)`

## Controlled comparison

- `launch_torque_nm`: 220 → 270. Hold the other controls at baseline; predict and explain the change before executing.
- `driveline_inertia_kg_m2`: 0.35 → 0.65. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

If engine-side angular speed is G*v/r, its kinetic energy is J*(G*v/r)²/2, giving equivalent mass J*(G/r)². Wheel inertias contribute separately as sum(Jw/r²). The squared ratio is essential: inverse gearing can make acceleration look unrealistically high. Compare drive work, road-loss work and total translational-plus-rotating energy; the finite Euler step leaves a discretization residual. If speed never reaches 27.78 m/s, the horizon value is censored and the reached flag is false.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Constant torque, fixed gear and a lumped reflected mass omit engine-speed limits, clutch dynamics and gear changes.

Competency links: VD-POWERTRAIN. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
