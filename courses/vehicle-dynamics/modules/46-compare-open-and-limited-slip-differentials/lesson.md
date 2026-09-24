# Compare Open and Limited-Slip Differentials

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. Its split-friction axle is deterministic and synthetic.

## Model and equations

- `F_open=2 min(F_demand/2,mu_L F_z,mu_R F_z)`
- `F_R<=TBR F_L`
- `F_L+F_R<=F_demand` and `F_k<=mu_k F_z`

Both wheel forces are positive forward in `N`; friction and torque-bias ratio are dimensionless. Equal fixed wheel loads isolate differential behavior.

## Baseline workflow

Compare open and limited-slip total delivery, inspect each wheel force, and require zero capacity residual.

## Two one-variable sweeps

Raise low-side friction alone, then reduce torque-bias ratio alone to separate available grip from differential authority.

## Intentionally broken case

Apply the bias ratio without enforcing the high-grip wheel capacity or total driveshaft demand.

## Recovery

Bound low- and high-side force by their contact capacities, the bias inequality, and the shared input demand.

## Limiting cases and invariants

- A bias ratio of one tends toward equal wheel force.
- With sufficient grip at both wheels, the open differential supplies full demand.
- Bias redistributes force but cannot create demand or tire capacity.

## Independent evidence

An independent inequality-based allocation recomputes all five scenarios without production execution.

## Common mistakes

- Treating torque-bias ratio as a force multiplier with no upper cap.
- Forgetting the shared driveshaft demand.
- Comparing axle totals without inspecting individual wheel capacity.

## Formative checks

1. Why does the low-grip wheel constrain an open differential twice?
2. Which boundary limits the default limited-slip result?

## Teach-back

Explain the split-friction allocation with units, forward-positive signs, bounded bias, named capacity violation, and exact capped recovery.
