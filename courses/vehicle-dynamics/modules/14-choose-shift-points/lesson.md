# Choose Shift Points

> **Guiding question:** When should the current gear be exchanged for the next gear to maximize wheel force?

## Physical model, frame, and units

The vehicle-fixed convention is +x forward, +y left, +z upward, and positive yaw counter-clockwise from above. Loads and forces act on the vehicle unless stated otherwise. The independent controls are **Current gear ratio** (ratio) and **Next gear ratio** (ratio). Angles displayed in degrees are converted exactly once before trigonometric use.

The governing relation is

`shift at first rpm where T(rpm_next)*i_next >= T(rpm)*i_current, otherwise at redline`

The teaching invariant is: **At a valid force-crossover shift, adjacent-gear wheel forces are equal within grid resolution.** The implementation is a Python-first native design derived from the reviewed P14 identity and competency. Its source folder was a scaffold; this is not a claim of source or MATLAB-runtime equivalence.

The search evaluates 121 deterministic points from 2500 to 7400 rpm on the declared torque curve. At each point, post-shift rpm is `rpm*i_next/i_current`; the first point where next-gear force meets or exceeds current-gear force is selected, otherwise the result is redline. A valid adjacent upshift requires `i_next<i_current`.

## Predict and sweep one variable at a time

1. Hold `next_gear_ratio` at 1.541 ratio. Predict the sign, monotonic trend, validity boundary, and invariant, then sweep `current_gear_ratio` through 1.4, 2.188, and 3.7 ratio.
2. Restore `current_gear_ratio` to 2.188 ratio. Hold every other assumption fixed and sweep `next_gear_ratio` through 0.8, 1.541, and 2.4 ratio.

Changing one physical input at a time distinguishes causality from correlation. The plots expose retained SI quantities rather than a renamed normalized waveform.

## Named broken behavior and exact recovery

**Broken behavior:** Broken mode makes the next ratio greater than the current ratio and flags the invalid sequence. The invalid field is part of the model result, so a finite plot cannot disguise a nonphysical setup.

**Exact recovery:** Restore a strictly descending adjacent-gear pair and recompute the crossover below redline. Disable broken mode, restore both defaults, and verify that the deterministic baseline signature returns exactly.

## Limits and limiting cases

The deterministic torque curve omits shift time, traction variation, gearbox losses by gear, rev limits after downshift, and engine transients. A redline result can mean there is no crossover inside the bounded search; it is not evidence that forces are equal there. Grid resolution bounds how closely a detected crossover can approach exact equality.

## Common mistakes

- Choosing peak engine power without comparing wheel force after the ratio change.
- Forgetting to map current rpm into the next gear before evaluating torque.
- Accepting a next-gear ratio greater than or equal to the current ratio as an upshift.
- Changing two controls simultaneously and attributing the result to one.
- Treating a steady instructional model as setup, safety, vehicle, or track validation.

## Formative checks

1. State every input, output, sign, and unit in the governing relation.
2. Predict both one-variable sweep directions before running them.
3. Identify the conserved or bounded quantity and verify it numerically.
4. Name the broken assumption, recover the exact baseline, and state the residual limitation.

## Teach-back checklist

- [ ] I can answer the guiding question in two or three sentences.
- [ ] I can derive or explain the governing relation and its units.
- [ ] I predicted and verified both sweeps.
- [ ] I diagnosed the named failure and demonstrated exact recovery.
- [ ] I can state what this deterministic software-only model does not prove.

This module is not measured-vehicle, firmware, radio, bench, track, hardware/HIL, certification, release, or production evidence.
