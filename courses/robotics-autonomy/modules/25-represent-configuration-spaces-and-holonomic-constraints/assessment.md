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


# Retained scoped evidence task

## P25 evidence task

At q=[1,0] m, why does projecting [1,0] m/s produce zero, and why can zero radius error fail to diagnose the broken mode?

Before running: Predict which quantities remain invariant when only the radial offset changes in normal mode, and whether tangency guarantees clearance.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Configuration projection plots Configuration y (m) against Configuration x (m). Its series are Raw configurations, Used configurations, Unit-radius constraint. Velocity tangency plots Radial velocity (m/s) against Configuration angle (rad). Its series are Used candidate velocity, Requested radial part.

### Reasoning rubric

- Model: use `h(q)=||q||-1 m=0; J_h=q^T/||q||` to reconstruct a quantity from the executed mechanism.
- Evidence: Increase radial offset from zero to 0.2 m with span fixed. The raw arc moves outward, while normal projection returns the same unit-circle arc. Confirm nearly zero constraint residual and unchanged projected clearance; an invariant output can be correct when the preprocessing intentionally removes the changed coordinate.
- Diagnosis: Broken mode bypasses both radial configuration projection and velocity projection. The Jacobian and its actual rank are still computed at the used configuration; the fault does not invent an extra tangent dimension.
- Recovery and scope: Disable broken mode, restore defaults and compare raw versus used configurations. Check both radius residual and radial velocity; repairing the position alone would leave the velocity condition unverified. State this limit: At zero offset the broken configuration already lies on the circle, so its radius residual can vanish while its unprojected velocity is still wrong. The Jacobian rank remains one. First-order tangency describes an instantaneous velocity and does not establish finite-step constraint preservation or collision avoidance.

### Check your explanation

The requested velocity is wholly normal to the constraint and has no tangent component. With zero input offset the configuration is already valid, but a nonzero outward velocity violates J_h v=0. Both configuration and velocity evidence are needed.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.
