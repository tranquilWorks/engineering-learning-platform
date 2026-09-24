# Use the Friction Circle

## Guiding question

What physical inputs, observable effects, and failure modes matter when you use the friction circle?

## Physical model, frame, and units

The vehicle-fixed frame is +x forward, +y left, and positive yaw counter-clockwise from above. Tire forces act on the vehicle. Inputs are `longitudinal_force_n` in N and `lateral_force_n` in N; angle equations convert degrees to radians explicitly.

The governing relation is `utilization = sqrt(Fx^2+Fy^2)/(mu*Fz)`. The teaching invariant is: **Combined-force utilization cannot exceed one.** This module has Python-first native provenance. It does not claim MATLAB-runtime equivalence for a source scaffold.

## Predict and sweep one variable at a time

First hold `lateral_force_n` at 3500.0 N and sweep `longitudinal_force_n` through -6500.0, 2800.0, and 6500.0 N. Restore the baseline, then hold `longitudinal_force_n` at 2800.0 N and sweep `lateral_force_n` through -6500.0, 3500.0, and 6500.0 N. Predict sign, monotonicity, and the invariant before running either sweep.

## Named broken behavior and exact recovery

Broken behavior: **Commanding force outside the circle.** The invalid flag makes the assumption failure explicit. Recovery: **Scale both components by reciprocal utilization.** Disable broken mode and restore both default inputs; the deterministic baseline signature must return exactly.

## Limits and limiting cases

A circular, load-independent boundary is an approximation. At zero excitation, the associated force, acceleration, yaw, or slip response tends toward zero. At a physical boundary the validity result changes instead of silently presenting infeasible values as valid.

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

