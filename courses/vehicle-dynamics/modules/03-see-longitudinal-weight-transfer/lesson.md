# See Longitudinal Weight Transfer

## Guiding question

What physical inputs, observable effects, and failure modes matter when you see longitudinal weight transfer?

## Physical model, frame, and units

The vehicle-fixed frame is +x forward, +y left, and positive yaw counter-clockwise from above. Tire forces act on the vehicle. Inputs are `acceleration_mps2` in m/s^2 and `cg_height_m` in m; angle equations convert degrees to radians explicitly.

The governing relation is `load transfer = mass*acceleration*CG height/wheelbase`. The teaching invariant is: **Front plus rear axle load remains mass*g.** This module has Python-first native provenance. It does not claim MATLAB-runtime equivalence for a source scaffold.

## Predict and sweep one variable at a time

First hold `cg_height_m` at 0.5 m and sweep `acceleration_mps2` through -9.0, 4.0, and 9.0 m/s^2. Restore the baseline, then hold `acceleration_mps2` at 4.0 m/s^2 and sweep `cg_height_m` through 0.25, 0.5, and 0.85 m. Predict sign, monotonicity, and the invariant before running either sweep.

## Named broken behavior and exact recovery

Broken behavior: **Unloading an axle below zero.** The invalid flag makes the assumption failure explicit. Recovery: **Restore acceleration so both axle loads are nonnegative.** Disable broken mode and restore both default inputs; the deterministic baseline signature must return exactly.

## Limits and limiting cases

Quasi-static pitch omits suspension compliance and pitch inertia. At zero excitation, the associated force, acceleration, yaw, or slip response tends toward zero. At a physical boundary the validity result changes instead of silently presenting infeasible values as valid.

## Common mistakes and formative checks

- Do not mix degrees and radians, reverse a tire-force convention, or change both controls before assigning causality.
- Explain every signature field with its units and state the coordinate/sign convention.
- Derive the expected direction of both sweeps and identify the conserved or bounded quantity.
- Diagnose the broken assumption, demonstrate exact recovery, and state the model limitation.

## Teach-back checklist

- [ ] I can explain the governing equation and invariant.
- [ ] I predicted and ran both one-variable sweeps.
- [ ] I identified the broken behavior and restored the exact baseline.
- [ ] I can state what this deterministic software-only model does not prove.

This experiment is not measured-vehicle, track, firmware, radio, hardware, HIL, safety, or production evidence.

