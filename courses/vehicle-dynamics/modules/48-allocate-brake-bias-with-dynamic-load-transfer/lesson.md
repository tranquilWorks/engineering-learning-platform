# Allocate Brake Bias with Dynamic Load Transfer

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It uses bounded synthetic axle and tire parameters.

## Model and equations

- `Delta F_z=m a_x h/L`
- `F_zf=m g b/L+Delta F_z`, `F_zr=m g a/L-Delta F_z`
- `F_b,k<=mu F_z,k` and `a_achieved=(F_bf+F_br)/(m g)`

Requested deceleration is positive in braking `g`; normal load is positive downward at each tire contact, and brake force magnitude is positive opposite travel.

## Baseline workflow

Compute dynamic axle loads, compare selected with ideal front bias, and check axle utilizations and closure residual.

## Two one-variable sweeps

Raise requested deceleration alone, then raise selected front bias alone to separate load transfer from allocation choice.

## Intentionally broken case

Size both axle capacities from static load despite longitudinal load transfer.

## Recovery

Transfer normal load forward once, cap each axle force by its dynamic capacity, and recompute achieved deceleration.

## Limiting cases and invariants

- Zero deceleration recovers static axle loads.
- Zero center-of-gravity height removes longitudinal transfer.
- Neither axle utilization may exceed one in the recovered model.

## Independent evidence

An independent force-allocation calculation recomputes baseline, two sweeps, broken, and recovery cases.

## Common mistakes

- Adding transfer to both axles.
- Using static weight to size rear brake force.
- Calling selected bias ideal without comparing dynamic loads.

## Formative checks

1. Why does ideal front bias rise with deceleration?
2. Which axle is overused by the default broken case?

## Teach-back

Explain the load-transfer sign, force units, bounded friction capacities, static-load failure, and exact dynamic-allocation recovery.
