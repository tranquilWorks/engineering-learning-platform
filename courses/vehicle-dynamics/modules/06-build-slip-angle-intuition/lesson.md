# Build Slip-Angle Intuition

## Guiding question

What physical inputs, observable effects, and failure modes matter when you build slip-angle intuition?

## Physical model, frame, and units

The vehicle-fixed frame is +x forward, +y left, and positive yaw counter-clockwise from above. Tire forces act on the vehicle. Inputs are `slip_angle_deg` in deg and `normal_load_n` in N; angle equations convert degrees to radians explicitly.

The governing relation is `Fy = -mu*Fz*tanh(Calpha*alpha/(mu*Fz))`. The teaching invariant is: **Force is zero at zero slip angle and opposes positive slip angle.** This module has Python-first native provenance. It does not claim MATLAB-runtime equivalence for a source scaffold.

## Predict and sweep one variable at a time

First hold `normal_load_n` at 3600.0 N and sweep `slip_angle_deg` through -14.0, 4.0, and 14.0 deg. Restore the baseline, then hold `slip_angle_deg` at 4.0 deg and sweep `normal_load_n` through 1000.0, 3600.0, and 6000.0 N. Predict sign, monotonicity, and the invariant before running either sweep.

## Named broken behavior and exact recovery

Broken behavior: **Reversing the force sign.** The invalid flag makes the assumption failure explicit. Recovery: **Restore Fy=-Calpha*alpha near zero.** Disable broken mode and restore both default inputs; the deterministic baseline signature must return exactly.

## Limits and limiting cases

The curve omits combined slip, camber, and relaxation length. At zero excitation, the associated force, acceleration, yaw, or slip response tends toward zero. At a physical boundary the validity result changes instead of silently presenting infeasible values as valid.

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

