# Distribute Roll Stiffness

> **Guiding question:** How does front/rear roll-stiffness distribution allocate lateral load transfer?

## Physical model, frame, and units

The vehicle-fixed convention is +x forward, +y left, +z upward, and positive yaw counter-clockwise from above. Loads and forces act on the vehicle unless stated otherwise. The independent controls are **Front roll stiffness** (N*m/rad) and **Rear roll stiffness** (N*m/rad). Angles displayed in degrees are converted exactly once before trigonometric use.

The governing relation is

`phi=M_roll/(K_phi_f+K_phi_r); DeltaF_f=K_phi_f*phi/t_f; DeltaF_r=K_phi_r*phi/t_r`

The teaching invariant is: **Front and rear transfer sum to `M_roll/t`, so their elastic roll moments sum to the applied roll moment.** The implementation is a Python-first native design derived from the reviewed P11 identity and competency. Its source folder was a scaffold; this is not a claim of source or MATLAB-runtime equivalence.

The model applies `M_roll=m*a_y*h` for a 1320 kg vehicle at 7 m/s² lateral acceleration, 0.50 m effective height, and 1.53 m effective track. With one declared track, front plus rear lateral load transfer is exactly `M_roll/t`, while stiffness share decides how much each axle carries. More front share is a handling-balance indicator, not by itself a complete understeer prediction.

## Predict and sweep one variable at a time

1. Hold `rear_roll_stiffness_n_m_rad` at 26000.0 N*m/rad. Predict the sign, monotonic trend, validity boundary, and invariant, then sweep `front_roll_stiffness_n_m_rad` through 10000.0, 32000.0, and 60000.0 N*m/rad.
2. Restore `front_roll_stiffness_n_m_rad` to 32000.0 N*m/rad. Hold every other assumption fixed and sweep `rear_roll_stiffness_n_m_rad` through 10000.0, 26000.0, and 60000.0 N*m/rad.

Changing one physical input at a time distinguishes causality from correlation. The plots expose retained SI quantities rather than a renamed normalized waveform.

## Named broken behavior and exact recovery

**Broken behavior:** Broken mode gives the rear axle negative roll stiffness and flags the nonphysical allocation. The invalid field is part of the model result, so a finite plot cannot disguise a nonphysical setup.

**Exact recovery:** Restore positive axle stiffnesses and verify moment conservation. Disable broken mode, restore both defaults, and verify that the deterministic baseline signature returns exactly.

## Limits and limiting cases

The elastic distribution excludes geometric load transfer, roll-center migration, unequal tracks, tire load sensitivity, and transient roll. Scaling both axle stiffnesses together reduces roll angle without changing transfer share; changing only one axle moves the share while total transfer remains fixed. Zero or negative total stiffness is nonphysical and outside the valid setup.

## Common mistakes

- Adding axle stiffnesses without first computing the common roll angle.
- Comparing axle transfer forces without checking their sum and moment residual.
- Claiming that elastic distribution alone predicts full vehicle balance.
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
