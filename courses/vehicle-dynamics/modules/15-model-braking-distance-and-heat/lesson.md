# Model Braking Distance and Heat

> **Guiding question:** How do tire-limited braking force, load transfer, distance, and rotor heat connect?

## Physical model, frame, and units

The vehicle-fixed convention is +x forward, +y left, +z upward, and positive yaw counter-clockwise from above. Loads and forces act on the vehicle unless stated otherwise. The independent controls are **Initial speed** (m/s) and **Requested brake force** (N). Angles displayed in degrees are converted exactly once before trigonometric use.

The governing relation is

`a=F_b/m; s=V0^2/(2*a); E_k=0.5*m*V0^2; DeltaT=eta_h*E_k/(m_rotor*c_p)`

The teaching invariant is: **Stopping work equals initial kinetic energy in the constant-force model.** The implementation is a Python-first native design derived from the reviewed P15 identity and competency. Its source folder was a scaffold; this is not a claim of source or MATLAB-runtime equivalence.

The vehicle mass is 1320 kg with `mu=1.05`, 0.50 m center-of-gravity height, 2.57 m wheelbase, and 53% static front load. Applied force is capped at `mu*m*g`; 85% of kinetic energy heats 28 kg of modeled rotors with 460 J/(kg·°C) heat capacity. Front and rear normal loads must still sum to vehicle weight.

## Predict and sweep one variable at a time

1. Hold `requested_brake_force_n` at 10000.0 N. Predict the sign, monotonic trend, validity boundary, and invariant, then sweep `initial_speed_m_s` through 5.0, 30.0, and 55.0 m/s.
2. Restore `initial_speed_m_s` to 30.0 m/s. Hold every other assumption fixed and sweep `requested_brake_force_n` through 1000.0, 10000.0, and 18000.0 N.

Changing one physical input at a time distinguishes causality from correlation. The plots expose retained SI quantities rather than a renamed normalized waveform.

## Named broken behavior and exact recovery

**Broken behavior:** Broken mode bypasses the tire-force cap and assigns all kinetic energy to the modeled rotors. The invalid field is part of the model result, so a finite plot cannot disguise a nonphysical setup.

**Exact recovery:** Restore the mu*m*g cap, the declared 85% rotor heat split, and nonnegative axle loads. Disable broken mode, restore both defaults, and verify that the deterministic baseline signature returns exactly.

## Limits and limiting cases

The stop uses constant force and friction plus lumped rotor heat capacity; it omits cooling, pad fade, ABS cycling, tire load sensitivity, rotation energy, and road grade. Distance and energy scale with speed squared. Above the tire limit, greater requested force cannot shorten the valid modeled stop because applied force remains capped.

## Common mistakes

- Using requested brake force after the tire cap instead of applied force.
- Adding load transfer to both axles instead of conserving total normal load.
- Treating a single-stop adiabatic temperature rise as a repeated-stop thermal prediction.
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
