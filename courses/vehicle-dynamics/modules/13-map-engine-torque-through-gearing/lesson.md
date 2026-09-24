# Map Engine Torque through Gearing

> **Guiding question:** How do gearing, efficiency, and wheel radius turn engine torque into bounded wheel force?

## Physical model, frame, and units

The vehicle-fixed convention is +x forward, +y left, +z upward, and positive yaw counter-clockwise from above. Loads and forces act on the vehicle unless stated otherwise. The independent controls are **Engine torque** (N*m) and **Selected gear ratio** (ratio). Angles displayed in degrees are converted exactly once before trigonometric use.

The governing relation is

`F_w=T_e*i_g*i_f*eta/r_w; rpm=V*i_g*i_f*60/(2*pi*r_w)`

The teaching invariant is: **Power after efficiency equals wheel force times vehicle speed when rotational acceleration is neglected.** The implementation is a Python-first native design derived from the reviewed P13 identity and competency. Its source folder was a scaffold; this is not a claim of source or MATLAB-runtime equivalence.

The fixed assumptions are 4.10 final drive, 90% efficiency, 0.315 m tire radius, 20 m/s road speed, 1320 kg mass, and `mu=1`. Requested wheel force follows the driveline equation; applied force is the lesser of that request and `mu*m*g`. The power residual is zero while unsaturated and becomes negative when the tire boundary prevents all requested power from reaching the road.

## Predict and sweep one variable at a time

1. Hold `gear_ratio` at 3.0 ratio. Predict the sign, monotonic trend, validity boundary, and invariant, then sweep `engine_torque_n_m` through 80.0, 250.0, and 320.0 N*m.
2. Restore `engine_torque_n_m` to 250.0 N*m. Hold every other assumption fixed and sweep `gear_ratio` through 0.8, 3.0, and 4.2 ratio.

Changing one physical input at a time distinguishes causality from correlation. The plots expose retained SI quantities rather than a renamed normalized waveform.

## Named broken behavior and exact recovery

**Broken behavior:** Broken mode assumes lossless gearing and applies unlimited wheel force beyond the tire-force boundary. The invalid field is part of the model result, so a finite plot cannot disguise a nonphysical setup.

**Exact recovery:** Restore 90% drivetrain efficiency and cap transmitted force at mu*m*g. Disable broken mode, restore both defaults, and verify that the deterministic baseline signature returns exactly.

## Limits and limiting cases

The steady driveline model omits rotating inertia, clutch slip, differential behavior, tire slip, aerodynamic load, and transient engine response. At fixed engine torque, both rpm and requested wheel force grow linearly with gear ratio. Once the tire cap is active, more ratio raises requested force but not applied force.

## Common mistakes

- Omitting final drive, efficiency, or tire radius from the torque-to-force chain.
- Mixing rpm with rad/s when checking power.
- Reporting requested force as applied force after traction saturation.
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
