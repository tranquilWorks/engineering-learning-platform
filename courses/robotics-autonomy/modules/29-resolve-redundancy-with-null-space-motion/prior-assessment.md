## P29 evidence task

Why can the total task residual be nonzero while secondary leakage is essentially zero?

Before running: Predict whether primary damping requires secondary posture motion to leak into the task when an exact null projector is used.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Instantaneous joint commands plots Joint velocity (rad/s) against Posture gain (1/s). Its series are Joint 1, Joint 2, Joint 3. Resulting task velocity plots Task velocity (m/s) against Posture gain (1/s). Its series are Actual x, Actual y, Desired x, Desired y.

### Reasoning rubric

- Model: use `qdot_primary=J^T(JJ^T+lambda²I)^-1 v_desired` to reconstruct a quantity from the executed mechanism.
- Evidence: Increase primary damping from zero to 0.5 while holding posture gain fixed. Compare task velocity residual and joint speed. Secondary leakage should remain near roundoff in normal mode because the exact projector is independent of primary damping.
- Diagnosis: Broken mode bypasses the null projector and adds minus gain times the full posture vector to the primary command.
- Recovery and scope: Restore the exact projector and defaults. Check actual task velocity, secondary leakage and joint velocity together; a low total joint speed alone cannot certify task preservation. State this limit: At zero gain both modes coincide because no secondary motion is requested. At zero damping the full-row-rank primary inverse tracks the desired task to roundoff. The null projector is local to one configuration; finite motion requires recomputing it. No joint limits, collision constraints or integrated posture trajectory are claimed.

### Check your explanation

The damped primary inverse trades tracking accuracy against joint speed. An exact null projector preserves that primary task velocity when posture motion is added; it does not undo the original damping residual.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.
