# P05 course checkpoint

## Predict and derive

Predict current and speed when gear ratio changes under load.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `L di/dt=V-Ri-K_e omega_m`
- `J_eq d omega_m/dt=K_t i-b omega_m-tau_L/N`

## Controlled comparison

- Vary only `voltage_v` through [6, 12, 18]; predict Voltage changes current transient and steady speed.
- Vary only `gear_ratio` through [5, 20, 40]; predict Reduction trades output speed for torque and reflection.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Back EMF couples speed to current; gearing changes reflected inertia and output torque rather than creating mechanical power.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The motor model does not qualify thermal limits or gearbox backlash.

Competency links: ACTUATION-JOINT-CONTROL. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
