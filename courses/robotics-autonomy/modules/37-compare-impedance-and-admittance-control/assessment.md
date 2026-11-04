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


# Retained scoped evidence task

## P37 evidence task

Why does a reported value of 0.4 s not necessarily mean that the response settled at 0.4 s?

Before running: Predict the energy trend when damping is positive and when the same damping is given the wrong sign.

Collect a default record, one single-control sweep, the named fault and recovery. Record the parameter values, plotted quantities and units so another learner can reproduce the comparison.

Contact perturbations plots Contact force (N) against Time (s). Its series are Impedance, Admittance. Stored contact energy plots Stored energy (J) against Time (s). Its series are Impedance, Admittance.

### Reasoning rubric

- Model: reconstruct a displayed value using `m xddot+b xdot+(k_virtual+k_environment)x=0` and the actual state or geometry.
- Evidence: Increase environment stiffness at fixed damping. Recalculate initial impedance force and energy, then compare oscillation frequency and the observed settling or censoring status.
- Diagnosis: The fault changes b to negative b in the integrated impedance and virtual-admittance equations. The resulting positive energy derivative drives the observed growth.
- Recovery and scope: Restore positive damping and repeat the same initial excitations. Check energy decay and both state-band conditions before interpreting settling. State this boundary: At zero damping the ideal system conserves energy and generally does not settle. The maintained-preload linearization and ideal position servo exclude contact loss, actuator limits and servo bandwidth. A censored 0.4 s result is not a measured settling time.

### Check your explanation

The value can be the observation horizon with a censored status. Settling requires both normalized displacement and velocity to stay within the band; an oscillatory force zero crossing or the last available sample does not establish it.

A complete explanation contains a calculation, an observed comparison with units, the executed fault and a reproduced recovery. Name a setting that can hide the fault and a claim requiring evidence outside this model. This is a self-assessment; no learner score is stored.
