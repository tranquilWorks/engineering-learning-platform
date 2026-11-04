# P08 course checkpoint

## Predict and derive

Predict contact displacement when stiffness changes with fixed force.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `m x_ddot=K(x_d-x)-B x_dot-F_c`
- `F_c=K_e max(x,0)`

## Controlled comparison

- Vary only `stiffness_n_m` through [75, 200, 600]; predict Stiffness changes static sharing with the wall.
- Vary only `damping_ns_m` through [4, 20, 60]; predict Damping changes transient settling but not static balance.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Impedance sets a force-motion relationship; environment stiffness participates in the coupled dynamics and damping dissipates energy.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

Stable sampled plots do not prove passivity against every environment.

Competency links: PHYSICAL-INTERACTION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
