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


---

## P65 course checkpoint

**Predict and calculate.** Compare a bounded terminal objective with its actual optimized controls and residual.

Use `p[k+1]=p[k]+dt v[k]+dt² u[k]/2; v[k+1]=v[k]+dt u[k]; J=0.1 sum u[k]²+w p[N]²+0.5w v[N]², normalized by 1 m, 1 s; |u[k]|<=a_max; N=20; dt=0.1 s` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Acceleration limit**, **Terminal weight**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

A finite control horizon trades terminal error against limits. If the desired terminal state is infeasible, report the residual and active bounds rather than silently declaring success from solver convergence.

### Model boundary

This bounded teaching problem is not a complete autonomous planner.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-GUIDANCE**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
