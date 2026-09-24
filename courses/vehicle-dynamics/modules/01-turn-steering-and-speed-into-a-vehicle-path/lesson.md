# Turn Steering and Speed into a Vehicle Path

## Guiding question

What physical inputs, observable effects, and failure modes matter when you turn steering and speed into a vehicle path?

## Physical model, frame, and units

The vehicle-fixed frame is +x forward, +y left, and positive yaw counter-clockwise from above. Tire forces act on the vehicle. Inputs are `steering_deg` in deg and `speed_mps` in m/s; angle equations convert degrees to radians explicitly.

The governing relation is `curvature = tan(steering/ratio)/wheelbase; yaw_rate = speed*curvature; lateral_acceleration = speed*yaw_rate`. The teaching invariant is: **Absolute lateral acceleration cannot exceed mu*g without sliding.** This module has implemented-source comparison provenance. It does not claim MATLAB-runtime equivalence for a source scaffold.

## Predict and sweep one variable at a time

First hold `speed_mps` at 15.0 m/s and sweep `steering_deg` through -20.0, 5.0, and 20.0 deg. Restore the baseline, then hold `steering_deg` at 5.0 deg and sweep `speed_mps` through 1.0, 15.0, and 45.0 m/s. Predict sign, monotonicity, and the invariant before running either sweep.

## Named broken behavior and exact recovery

Broken behavior: **Ignoring the friction boundary at high speed.** The invalid flag makes the assumption failure explicit. Recovery: **Reduce steering or speed until |a_y| <= mu*g.** Disable broken mode and restore both default inputs; the deterministic baseline signature must return exactly.

## Limits and limiting cases

Kinematic bicycle behavior omits tire compliance and transients. At zero excitation, the associated force, acceleration, yaw, or slip response tends toward zero. At a physical boundary the validity result changes instead of silently presenting infeasible values as valid.

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

