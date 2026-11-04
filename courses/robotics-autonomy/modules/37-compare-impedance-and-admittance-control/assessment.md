# P37 course checkpoint

## Predict and derive

Compare impedance and admittance under the same environment stiffness.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `m xddot+b xdot+(k_virtual+k_environment)x=0`
- `contact_force=k_environment*x`
- `E=0.5m xdot²+0.5(k_virtual+k_environment)x²; Edot=-b xdot²`

## Controlled comparison

- `environment_stiffness_n_m`: 800.0 → 3000.0. Hold the other controls at baseline and explain the mechanism before executing.
- `virtual_damping_n_s_m`: 45.0 → 150.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Impedance maps motion error to force; admittance integrates measured force into motion; interface choice changes closed-loop dynamics.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Stable behavior in one environment does not guarantee passive interaction.

Competency links: PHYSICAL-INTERACTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
