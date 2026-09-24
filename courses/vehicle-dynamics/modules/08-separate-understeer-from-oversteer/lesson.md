# Separate Understeer from Oversteer

## Guiding question

What physical inputs, observable effects, and failure modes matter when you separate understeer from oversteer?

## Physical model, frame, and units

The vehicle-fixed frame is +x forward, +y left, and positive yaw counter-clockwise from above. Tire forces act on the vehicle. Inputs are `front_cornering_stiffness_n_rad` in N/rad and `rear_cornering_stiffness_n_rad` in N/rad; angle equations convert degrees to radians explicitly.

The governing relation is `K=m/L*(b/Cf-a/Cr); delta=L/R+K*V^2/R`. The teaching invariant is: **K>0 understeers; K=0 is neutral; K<0 has finite critical speed.** This module has Python-first native provenance. It does not claim MATLAB-runtime equivalence for a source scaffold.

## Predict and sweep one variable at a time

First hold `rear_cornering_stiffness_n_rad` at 100000.0 N/rad and sweep `front_cornering_stiffness_n_rad` through 45000.0, 90000.0, and 140000.0 N/rad. Restore the baseline, then hold `front_cornering_stiffness_n_rad` at 90000.0 N/rad and sweep `rear_cornering_stiffness_n_rad` through 45000.0, 100000.0, and 140000.0 N/rad. Predict sign, monotonicity, and the invariant before running either sweep.

## Named broken behavior and exact recovery

Broken behavior: **Operating at or above oversteer critical speed.** The invalid flag makes the assumption failure explicit. Recovery: **Increase rear stability margin or reduce speed.** Disable broken mode and restore both default inputs; the deterministic baseline signature must return exactly.

## Limits and limiting cases

The steady linear result omits nonlinear saturation. At zero excitation, the associated force, acceleration, yaw, or slip response tends toward zero. At a physical boundary the validity result changes instead of silently presenting infeasible values as valid.

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

