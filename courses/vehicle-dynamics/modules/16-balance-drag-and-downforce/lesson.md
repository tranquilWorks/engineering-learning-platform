# Balance Drag and Downforce

> **Guiding question:** How does aero setup trade straight-line drag against downforce and tire capacity?

## Physical model, frame, and units

The vehicle-fixed convention is +x forward, +y left, +z upward, and positive yaw counter-clockwise from above. Loads and forces act on the vehicle unless stated otherwise. The independent controls are **Vehicle speed** (m/s) and **Wing angle** (deg). Angles displayed in degrees are converted exactly once before trigonometric use.

The governing relation is

`q=0.5*rho*V^2; D=q*CdA; L_down=q*ClA; F_grip=mu*(m*g+L_down)`

The teaching invariant is: **At fixed coefficients, drag and downforce scale with speed squared.** The implementation is a Python-first native design derived from the reviewed P16 identity and competency. Its source folder was a scaffold; this is not a claim of source or MATLAB-runtime equivalence.

Air density is fixed at 1.225 kg/m³. Wing angle raises the declared `ClA` linearly and `CdA` quadratically; drag power is `D*V`, tire capacity is `mu*(m*g+L_down)`, and front aero share must remain between zero and one. Downward force is reported positive, while drag is a positive resistance magnitude.

## Predict and sweep one variable at a time

1. Hold `wing_angle_deg` at 8.0 deg. Predict the sign, monotonic trend, validity boundary, and invariant, then sweep `speed_m_s` through 10.0, 40.0, and 70.0 m/s.
2. Restore `speed_m_s` to 40.0 m/s. Hold every other assumption fixed and sweep `wing_angle_deg` through 0.0, 8.0, and 18.0 deg.

Changing one physical input at a time distinguishes causality from correlation. The plots expose retained SI quantities rather than a renamed normalized waveform.

## Named broken behavior and exact recovery

**Broken behavior:** Broken mode reverses the drag sign and drives aero balance outside [0,1]. The invalid field is part of the model result, so a finite plot cannot disguise a nonphysical setup.

**Exact recovery:** Restore positive CdA, downward-positive ClA, and a bounded front aero share. Disable broken mode, restore both defaults, and verify that the deterministic baseline signature returns exactly.

## Limits and limiting cases

The steady aero map omits ride-height sensitivity, yaw, blockage, transient flow, tire load sensitivity, powertrain limits, and lap-time integration. At fixed angle, force scales with speed squared and drag power with speed cubed. More downforce increases the modeled force capacity, but this static gain cannot establish a net lap-time benefit.

## Common mistakes

- Reversing the downward-positive convention and reporting negative downforce.
- Comparing drag force with engine power without multiplying by speed.
- Treating aero force or balance as measured track performance.
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
