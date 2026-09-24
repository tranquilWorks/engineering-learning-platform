# Relate Acceleration to Tire Force

## Guiding question

What physical inputs, observable effects, and failure modes matter when you relate acceleration to tire force?

## Physical model, frame, and units

The vehicle-fixed frame is +x forward, +y left, and positive yaw counter-clockwise from above. Tire forces act on the vehicle. Inputs are `tractive_force_n` in N and `speed_mps` in m/s; angle equations convert degrees to radians explicitly.

The governing relation is `acceleration = (tractive force - rolling resistance - aerodynamic drag)/mass`. The teaching invariant is: **Applied tire force is bounded by mu*m*g and drag grows with speed squared.** This module has implemented-source comparison provenance. It does not claim MATLAB-runtime equivalence for a source scaffold.

## Predict and sweep one variable at a time

First hold `speed_mps` at 20.0 m/s and sweep `tractive_force_n` through 0.0, 4200.0, and 9000.0 N. Restore the baseline, then hold `tractive_force_n` at 4200.0 N and sweep `speed_mps` through 0.0, 20.0, and 55.0 m/s. Predict sign, monotonicity, and the invariant before running either sweep.

## Named broken behavior and exact recovery

Broken behavior: **Requesting force beyond the tire limit.** The invalid flag makes the assumption failure explicit. Recovery: **Cap requested force at mu*m*g.** Disable broken mode and restore both default inputs; the deterministic baseline signature must return exactly.

## Limits and limiting cases

The point-mass model omits gearing and rotating inertia. At zero excitation, the associated force, acceleration, yaw, or slip response tends toward zero. At a physical boundary the validity result changes instead of silently presenting infeasible values as valid.

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

