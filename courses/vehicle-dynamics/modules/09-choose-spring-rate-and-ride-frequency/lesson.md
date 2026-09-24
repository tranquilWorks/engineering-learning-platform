# Choose Spring Rate and Ride Frequency

> **Guiding question:** How do spring rate, motion ratio, and sprung mass set wheel rate and ride frequency?

## Physical model, frame, and units

The vehicle-fixed convention is +x forward, +y left, +z upward, and positive yaw counter-clockwise from above. Loads and forces act on the vehicle unless stated otherwise. The independent controls are **Spring rate** (N/m) and **spring-travel / wheel-travel motion ratio** (dimensionless). A ratio below one means the spring moves less than the wheel.

The governing relation is

`k_w = k_s i^2; f_n = (1/(2*pi))*sqrt(k_w/m_s)`

The teaching invariant is: **Wheel rate follows the square of motion ratio, and static load equals wheel rate times static deflection.** The implementation is a Python-first native design derived from the reviewed P09 identity and competency. Its source folder was a scaffold; this is not a claim of source or MATLAB-runtime equivalence.

The bounded quarter-car uses 300 kg of sprung mass and 9.81 m/s² gravity. Because both force and displacement transform through the linkage, motion ratio appears twice: halving the ratio quarters wheel rate rather than halving it.

## Predict and sweep one variable at a time

1. Hold `motion_ratio` at 0.9 ratio. Predict the sign, monotonic trend, validity boundary, and invariant, then sweep `spring_rate_n_m` through 15000.0, 35000.0, and 80000.0 N/m.
2. Restore `spring_rate_n_m` to 35000.0 N/m. Hold every other assumption fixed and sweep `motion_ratio` through 0.6, 0.9, and 1.1 ratio.

Changing one physical input at a time distinguishes causality from correlation. The plots expose retained SI quantities rather than a renamed normalized waveform.

## Named broken behavior and exact recovery

**Broken behavior:** Broken mode incorrectly omits the squared motion-ratio transformation. The invalid field is part of the model result, so a finite plot cannot disguise a nonphysical setup.

**Exact recovery:** Restore k_w=k_s*i^2 and the baseline spring rate and motion ratio. Disable broken mode, restore both defaults, and verify that the deterministic baseline signature returns exactly.

## Limits and limiting cases

The quarter-car ride-frequency model omits tire stiffness, unsprung mass, damping, bump stops, and suspension friction. As motion ratio approaches zero, wheel rate and ride frequency approach zero while static deflection diverges, so zero is deliberately outside the control range. Increasing spring rate raises frequency with a square-root trend, not linearly.

## Common mistakes

- Reversing the declared spring-travel / wheel-travel ratio.
- Using `k_w=k_s i` instead of applying the linkage twice.
- Using total vehicle mass instead of the declared corner sprung mass.
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
