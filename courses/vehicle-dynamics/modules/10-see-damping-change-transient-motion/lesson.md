# See Damping Change Transient Motion

> **Guiding question:** How does damping ratio change overshoot, decay rate, and settling time?

## Physical model, frame, and units

The vehicle-fixed convention is +x forward, +y left, +z upward, and positive yaw counter-clockwise from above. Loads and forces act on the vehicle unless stated otherwise. The independent controls are **Damper coefficient** (N*s/m) and **Wheel rate** (N/m). Angles displayed in degrees are converted exactly once before trigonometric use.

The governing relation is

`omega_n=sqrt(k/m); zeta=c/(2*sqrt(k*m)); x(t) decays with zeta*omega_n`

The teaching invariant is: **Positive damping dissipates energy; negative damping makes the homogeneous response grow.** The implementation is a Python-first native design derived from the reviewed P10 identity and competency. Its source folder was a scaffold; this is not a claim of source or MATLAB-runtime equivalence.

The modeled sprung mass is 300 kg. For `0<zeta<1`, the response oscillates at the damped frequency and the usual second-order formula gives overshoot; at or above critical damping, oscillatory frequency and overshoot are reported as zero. The settling estimate is the conventional 2% approximation `4/(zeta*omega_n)`.

## Predict and sweep one variable at a time

1. Hold `spring_rate_n_m` at 35000.0 N/m. Predict the sign, monotonic trend, validity boundary, and invariant, then sweep `damping_n_s_m` through 400.0, 3200.0, and 8000.0 N*s/m.
2. Restore `damping_n_s_m` to 3200.0 N*s/m. Hold every other assumption fixed and sweep `spring_rate_n_m` through 15000.0, 35000.0, and 70000.0 N/m.

Changing one physical input at a time distinguishes causality from correlation. The plots expose retained SI quantities rather than a renamed normalized waveform.

## Named broken behavior and exact recovery

**Broken behavior:** Broken mode reverses the damping sign and creates an explicitly unstable response. The invalid field is part of the model result, so a finite plot cannot disguise a nonphysical setup.

**Exact recovery:** Restore positive damping and verify a finite positive decay rate. Disable broken mode, restore both defaults, and verify that the deterministic baseline signature returns exactly.

## Limits and limiting cases

The linear quarter-car mode omits damper digression, bump stops, tire compliance, temperature, and road input spectra. Near zero damping, settling time becomes very large and overshoot approaches one; negative damping is not a slow-settling case but an unstable one. The finite control bounds keep every displayed quantity deterministic.

## Common mistakes

- Confusing damping coefficient `c` in N·s/m with dimensionless damping ratio `zeta`.
- Applying the underdamped overshoot formula at or above critical damping.
- Treating the 2% settling estimate as a measured damper trace.
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
