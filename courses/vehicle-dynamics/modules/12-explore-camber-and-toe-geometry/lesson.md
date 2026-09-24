# Explore Camber and Toe Geometry

> **Guiding question:** How do camber and toe create distinct lateral-force and scrub effects?

## Physical model, frame, and units

The vehicle-fixed convention is +x forward, +y left, +z upward, and positive yaw counter-clockwise from above. Loads and forces act on the vehicle unless stated otherwise. The independent controls are **Camber angle** (deg) and **Toe angle** (deg). Angles displayed in degrees are converted exactly once before trigonometric use.

The governing relation is

`F_gamma=-C_gamma*gamma; F_scrub=F_z*|tan(toe)|; P_scrub=F_scrub*V`

The teaching invariant is: **Zero camber removes camber thrust and zero toe removes this model's scrub loss.** The implementation is a Python-first native design derived from the reviewed P12 identity and competency. Its source folder was a scaffold; this is not a claim of source or MATLAB-runtime equivalence.

For the representative left wheel, positive camber means the wheel top leans outward and positive toe rotates its heading toward +y. The linear camber stiffness is 60 kN/rad at 3.6 kN vertical load; toe scrub uses the magnitude of `tan(toe)` at 20 m/s, so toe sign changes heading direction but not this simple loss estimate.

## Predict and sweep one variable at a time

1. Hold `toe_deg` at 0.1 deg. Predict the sign, monotonic trend, validity boundary, and invariant, then sweep `camber_deg` through -5.0, -2.0, and 2.0 deg.
2. Restore `camber_deg` to -2.0 deg. Hold every other assumption fixed and sweep `toe_deg` through -0.5, 0.1, and 0.5 deg.

Changing one physical input at a time distinguishes causality from correlation. The plots expose retained SI quantities rather than a renamed normalized waveform.

## Named broken behavior and exact recovery

**Broken behavior:** Broken mode feeds degree values directly to radian trigonometric relations. The invalid field is part of the model result, so a finite plot cannot disguise a nonphysical setup.

**Exact recovery:** Convert both alignment angles to radians exactly once and restore the declared signs. Disable broken mode, restore both defaults, and verify that the deterministic baseline signature returns exactly.

## Limits and limiting cases

The alignment model is not a complete tire/contact-patch model and excludes slip-angle interaction, compliance steer, pressure, wear, and temperature. Camber thrust changes sign through zero camber, while scrub magnitude is symmetric about zero toe. The small-angle interpretation becomes progressively weaker toward the declared angular limits.

## Common mistakes

- Feeding displayed degree values directly into radian relations.
- Treating signed toe heading and unsigned scrub loss as the same output.
- Generalizing this single-wheel linear relation into a complete tire model.
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
