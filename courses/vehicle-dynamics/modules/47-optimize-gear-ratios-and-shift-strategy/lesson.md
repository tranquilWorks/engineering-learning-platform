# Optimize Gear Ratios and Shift Strategy

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It uses a fixed bounded gear set and synthetic engine curve.

## Model and equations

- `n_e=60 v i_g i_0/(2 pi r_t)`
- `g_selected=argmax_g F_wheel(g)` subject to `1500<=n_e<=7000`
- `v_dot=(F_selected-F_resist)/m`, with zero selected force during each shift interruption

Speed and acceleration are positive forward; engine speed is in `rpm`, ratios dimensionless, delay in `s`, and force in `N`.

## Baseline workflow

Run the default strategy, inspect shift speeds and the acceleration envelope, then verify no selected gear exceeds redline.

## Two one-variable sweeps

Raise final-drive ratio alone, then raise shift delay alone to distinguish force leverage from interruption loss.

## Intentionally broken case

Hold first gear beyond redline and remove every shift interruption.

## Recovery

At each bounded time step choose the largest valid in-band wheel force and apply the declared delay when gear changes.

## Limiting cases and invariants

- Zero shift delay removes interruption loss but not engine-speed limits.
- Shorter gearing increases early wheel force and reaches redline sooner.
- A valid strategy has zero redline excess.

## Independent evidence

A separately formulated fixed-step search recomputes all five scenarios without importing the production experiment.

## Common mistakes

- Selecting maximum ratio instead of maximum valid wheel force.
- Ignoring engine-speed limits.
- Reporting a time gain while omitting shift interruption.

## Formative checks

1. Why is the highest numerical ratio not always the best gear?
2. How can a shorter final drive worsen the target time?

## Teach-back

Explain the candidate search, engine band, units, forward-positive convention, broken redline behavior, and delayed-shift recovery.
