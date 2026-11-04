# P25 course checkpoint

## Predict and derive

Check both radial constraint residual and tangent-velocity projection.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `h(q)=||q||-1 m=0; J_h=q^T/||q||`
- `P=I-J_h^T(J_h J_h^T)^-1 J_h; v=P[1,0]^T m/s`
- `clearance=||q-[1.5,0.5] m||-0.2 m`

## Controlled comparison

- `constraint_offset_m`: 0.08 → 0.4. Hold the other controls at baseline and explain the mechanism before executing.
- `joint_span_rad`: 1.2 → 3.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

The constraint Jacobian removes the radial velocity component; instantaneous tangency does not guarantee finite-step collision freedom.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The circle example is a configuration-space slice, not general manifold planning.

Competency links: RIGID-BODY-GEOMETRY. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
