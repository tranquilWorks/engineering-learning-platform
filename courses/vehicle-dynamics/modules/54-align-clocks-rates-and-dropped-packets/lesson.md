# Align Clocks, Rates, and Dropped Packets

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It uses deterministic synthetic timing and signal values.

## Model and equations

- `t_aligned=t_source-delta_t`
- `missing={k where t_k is absent from the declared grid}`
- `x_grid=bounded_linear_interpolation(t_aligned,x)`

Offset, sampling rate, and packet loss are different timing defects. Alignment establishes a common epoch before gap repair reconstructs only declared grid points.

## Baseline workflow

Create a reference signal at 50 Hz, add a 12 ms source-clock offset, remove every seventh sample, estimate the aligned timestamps, and interpolate onto the reference grid. Audit offset, drop count, maximum gap, and RMSE.

## Two one-variable sweeps

Reverse and enlarge only the clock offset, then increase only the drop period. The first sweep changes epoch correction; the second changes gap count and reconstruction error.

## Intentionally broken case

Treat the offset source clock as the reference clock. Interpolation produces a smooth curve but retains a phase error and a nonzero clock residual.

## Recovery

Normalize timestamps to the shared epoch, identify missing grid indices, enforce the maximum permitted gap, and interpolate only after those checks pass.

## Limiting cases and invariants

- Zero offset requires no epoch correction.
- No dropped samples requires no interpolation.
- A smooth reconstruction does not prove correct timestamps.

## Independent evidence

An independent analytic signal, mask, alignment, and interpolation calculation reproduces all five scenario signatures.

## Common mistakes

- Resampling before clock synchronization.
- Confusing sample index with time.
- Filling long outages as though they were single missing samples.

## Formative checks

1. Which metric exposes a smooth but shifted reconstruction?
2. Why is maximum gap retained alongside drop count?

## Teach-back

Explain epoch alignment, rate grids, drop detection, bounded interpolation, the phase-error failure, and exact recovery order.
