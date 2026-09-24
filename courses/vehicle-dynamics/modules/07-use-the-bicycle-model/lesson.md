# Use the Bicycle Model

## Guiding question

What physical inputs, observable effects, and failure modes matter when you use the bicycle model?

## Physical model, frame, and units

The vehicle-fixed frame is +x forward, +y left, and positive yaw counter-clockwise from above. Tire forces act on the vehicle. Inputs are `steering_deg` in deg and `speed_mps` in m/s; angle equations convert degrees to radians explicitly.

The governing relation is `Solve steady linear-bicycle force and yaw-moment balance for sideslip and yaw rate.`. The teaching invariant is: **Axle forces balance m*V*r and yaw moments balance zero.** This module has Python-first native provenance. It does not claim MATLAB-runtime equivalence for a source scaffold.

## Predict and sweep one variable at a time

First hold `speed_mps` at 18.0 m/s and sweep `steering_deg` through -8.0, 3.0, and 8.0 deg. Restore the baseline, then hold `steering_deg` at 3.0 deg and sweep `speed_mps` through 3.0, 18.0, and 40.0 m/s. Predict sign, monotonicity, and the invariant before running either sweep.

## Named broken behavior and exact recovery

Broken behavior: **Using the linear model at large angles.** The invalid flag makes the assumption failure explicit. Recovery: **Return steer and axle slip angles to the small-angle range.** Disable broken mode and restore both default inputs; the deterministic baseline signature must return exactly.

## Limits and limiting cases

Linear tires require small angles and constant speed. At zero excitation, the associated force, acceleration, yaw, or slip response tends toward zero. At a physical boundary the validity result changes instead of silently presenting infeasible values as valid.

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

