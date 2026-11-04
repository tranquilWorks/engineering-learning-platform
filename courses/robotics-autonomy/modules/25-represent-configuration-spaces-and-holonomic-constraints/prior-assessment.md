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
