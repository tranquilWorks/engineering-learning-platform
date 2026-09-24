# Run a Forward-Backward Lap-Time Simulation

This competency-derived Python-first module is not a source conversion. It produces deterministic software evidence, not a measured-vehicle result.

## Model and equations

The model evaluates v_curve=sqrt(ay_max/|kappa|); v_next^2<=v^2+2 ax ds; t_lap=sum ds/v. Every reported scalar belongs to a named signature so the independent oracle can reproduce the calculation without importing production code.

## Baseline workflow

Run the declared baseline, inspect both plots, identify the active constraint, and reconcile the metrics with the equations. Record the control values before interpreting any change.

## Two one-variable sweeps

Sweep grip_scale alone to its declared low case, then restore it and sweep energy_limit_mj alone to its high case. This isolates cause and effect while all other assumptions remain fixed.

## Intentionally broken case

Enable broken mode. The experiment violates a domain-specific closure or trace condition and exposes the failure through a nonzero residual or unsigned requirement rather than hiding it in a plausible plot.

## Recovery

Disable broken mode and rerun the exact baseline. Recovery is exact: baseline and recovery signatures must agree within the declared absolute and relative tolerance.

## Limiting cases and invariants

Check the low and high control bounds. Every segment speed must be reachable through both forward acceleration and backward braking passes. Finite values alone are insufficient; the signed residual or requirement ledger is the invariant.

## Independent evidence

Five stored scenarios are calculated twice: once by the production experiment and once by a separate reference implementation that imports no production experiment and consumes no production result.

## Common mistakes

Do not change two controls at once, infer causality from plot shape, ignore units, treat a low residual as proof of physical validity, or generalize synthetic output to a real GR86.

## Formative checks

1. Which equation sets the active constraint in the baseline?
2. Which metric must change in the broken case?
3. Why must baseline and recovery be identical?

## Teach-back

Explain the model, the two isolated sweeps, the deliberate failure, the recovery, one limiting case, and the boundary between deterministic software evidence and physical validation.
