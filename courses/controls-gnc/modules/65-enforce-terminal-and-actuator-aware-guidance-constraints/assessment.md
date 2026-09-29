## P65 evidence task

Why is a positive terminal residual compatible with a correct bounded optimizer?

Before running: Predict whether a finite terminal penalty forces exact arrival, even when the command limits permit arrival.

Collect the default result, one single-control sweep, the named fault and recovery. Record controls and units beside the evidence.

Executed terminal trajectory plots Position (m) against Time (s). Its series are Position. Applied bounded commands plots Acceleration (m/s²) against Interval start (s). Its series are Applied, Upper limit, Lower limit.

### Reasoning rubric

- Model: use `p[k+1]=p[k]+dt v[k]+dt² u[k]/2; v[k+1]=v[k]+dt u[k]` to reconstruct a quantity from the executed mechanism.
- Evidence: Increase acceleration authority from 3 to 50 m/s² at fixed terminal weight. Identify which intervals lie on bounds and compare actual terminal position and velocity.
- Diagnosis: Broken mode solves the unconstrained objective and applies that command sequence without enforcing the selected actuator limit.
- Recovery and scope: Restore the bounded solve, reset controls and verify every applied interval satisfies the limit. Compare the residual rather than assuming it becomes zero. State this limit: This is an open-loop finite-horizon optimization, not a robust receding-horizon controller. Soft terminal penalties allow residual. The declared dimensionless normalization is necessary when adding position, velocity and acceleration costs.

### Check your explanation

Bounds may make exact arrival infeasible, and finite penalties trade residual against effort even when arrival is feasible. Correctness requires executed dynamics, feasible controls and optimality evidence, not an assigned zero endpoint.

A complete answer includes the calculation or geometric construction, an observed comparison with units, fault/recovery evidence and the stated limitation. This is a self-assessment; no learner score is stored.
