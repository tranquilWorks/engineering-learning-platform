# Solve a Bounded Terminal Guidance Objective



## Model and equations

`p[k+1]=p[k]+dt v[k]+dt² u[k]/2; v[k+1]=v[k]+dt u[k]`

`J=0.1 sum u[k]²+w p[N]²+0.5w v[N]², normalized by 1 m, 1 s`

`|u[k]|<=a_max; N=20; dt=0.1 s`

The one-dimensional double integrator starts 30 m from the origin at zero velocity. Twenty piecewise-constant accelerations act over two seconds. The endpoint map has position coefficients dt²(N-k-0.5) and velocity coefficients dt. A bounded least-squares solve minimizes normalized command effort and terminal position/velocity penalties. With a 3 m/s² limit, even continuous maximum deceleration over two seconds changes position by only 6 m before considering the velocity objective, so zero position error is impossible. With larger authority, exact endpoint feasibility still does not force a soft-penalty optimizer to choose exact arrival. The actual chosen controls propagate every displayed position and velocity sample. The peak command and limit violation are computed from that sequence, while the terminal residual comes from its last propagated state.

## Predict before running

Predict whether a finite terminal penalty forces exact arrival, even when the command limits permit arrival.

## Baseline workflow

Reset controls and leave the named fault disabled. Use Acceleration limit = 20.0 m/s^2; Terminal weight = 8.0 1. Write a prediction before executing. Read the response curve first, then explain it using the mechanism curve.

Executed terminal trajectory plots Position (m) against Time (s). Its series are Position. Applied bounded commands plots Acceleration (m/s²) against Interval start (s). Its series are Applied, Upper limit, Lower limit.

The computed default record is Peak applied acceleration: 20 m/s^2; Actuator violation: 0 m/s^2; Terminal position residual: 4.81371 m; Terminal velocity residual: 7.76155 m/s. These values are a reproducible worked example, not acceptance thresholds for every slider setting. Retain units and parameter values when comparing another run. A displayed residual near machine precision should be interpreted with the stated model and numerical tolerance.

## Two one-variable sweeps

1. Increase acceleration authority from 3 to 50 m/s² at fixed terminal weight. Identify which intervals lie on bounds and compare actual terminal position and velocity.

2. Increase terminal weight from 1 to 20 with authority fixed. More emphasis on arrival can increase command effort, but active bounds may prevent the requested improvement.

Return to defaults between sweeps. Keep the other control fixed, record the changed quantity and identify an expected invariant. A control need not change every output; explain the model path through which it acts.

## Intentionally broken case

Broken mode solves the unconstrained objective and applies that command sequence without enforcing the selected actuator limit.

Run the same selected controls with the fault enabled. Compare the curve shape as well as the numerical summary. The fault is a specific executed operation; a red warning or a changed mode flag would not by itself demonstrate its consequence.

## Recovery

Restore the bounded solve, reset controls and verify every applied interval satisfies the limit. Compare the residual rather than assuming it becomes zero.

Repeat one previously saved nominal setting and check that its values and curves return. Recovery should restore the mechanism, not merely dismiss the warning.

## Limiting cases and invariants

This is an open-loop finite-horizon optimization, not a robust receding-horizon controller. Soft terminal penalties allow residual. The declared dimensionless normalization is necessary when adding position, velocity and acceleration costs.

## Independent evidence

The independent reference solves a two-dimensional dual terminal-residual equation with clipped controls, rather than the production twenty-variable bounded least-squares problem.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values are generated independently; actual values come from the executable lesson. Absolute and relative tolerances remain 1e-8. Agreement checks the declared synthetic model, not empirical validity. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence are recorded separately from numerical evidence.

## Engineering review checklist

Check the declared coordinates, units and ordering before evaluating the result. Reconstruct at least one displayed value from retained state or geometric data. Identify which output changes in each sweep and which should remain invariant. Diagnose the named faulty operation, then demonstrate its recovery. Finally state the strongest claim supported by these observations and one claim that requires additional evidence.

## Common mistakes

Do not infer correctness from a changing headline alone. In this lesson, the critical limit is: This is an open-loop finite-horizon optimization, not a robust receding-horizon controller. Soft terminal penalties allow residual. The declared dimensionless normalization is necessary when adding position, velocity and acceleration costs.

Do not compare two runs after changing both controls and attribute the difference to one cause. Do not treat a near-zero floating-point residual as symbolic identity, or a finite sample sweep as a proof for all configurations. Keep the operation that creates the evidence separate from the interpretation assigned to it.

## Teach-back

Why is a positive terminal residual compatible with a correct bounded optimizer?

Answer rationale: Bounds may make exact arrival infeasible, and finite penalties trade residual against effort even when arrival is feasible. Correctness requires executed dynamics, feasible controls and optimality evidence, not an assigned zero endpoint.

Use the embedded Course checkpoint to collect a default record, a sweep, a faulty record and a recovered record. Explain the evidence to a colleague using the governing relation and units, then name the untested boundary. This is a self-assessment; no learner score is stored.
