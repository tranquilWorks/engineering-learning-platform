# Measure Motion in Body, Path, and Wheel Frames

**Guiding question:** Which frame owns each velocity component, and how can invariants expose a silent angle-unit error?

Resolve one planar velocity through inertial, path, body, and steered-wheel frames while checking round-trip and norm invariants. This is a competency-derived Python-first native design. It is not a source conversion, MATLAB-runtime comparison, rig test, track test, or measured-vehicle result.

## Why this lesson exists

The 24 source-bound lessons establish the surface workflow. This depth lesson requires a governing tire relation, a falsifiable invariant, a named failure, and independent evidence. State the frame, sign, unit, and synthetic-data assumptions before reading any curve.

## Model and equations

- `v_path=R(-psi_path)*v_inertial`
- `v_body=R(-psi_body)*v_inertial`
- `v_wheel=R(-delta)*v_body`
- `||R(theta)*v||_2=||v||_2`

All angles cross a labeled degree-to-radian boundary before trigonometric use. Longitudinal force is positive forward, lateral force follows the lesson's displayed convention, normal load is positive into the contact patch, and dissipated energy is nonnegative.

## Predict before running

A proper planar rotation preserves speed norm, and a transform followed by its inverse recovers the original vector in the same angle unit. Predict the direction of every signature change before moving a control.

## Baseline workflow

1. Run the defaults with broken mode disabled.
2. Read all signature metrics and their physical units.
3. Compare the response plot with the mechanism plot.
4. Check both limiting cases before accepting the interpretation.
5. Save the baseline so recovery can be compared exactly.

## Two one-variable sweeps

1. Hold wheel steer at 8 deg and sweep path heading from -180 to 180 deg.
2. Restore path heading to 32 deg and sweep wheel steer from -35 to 35 deg.

Change only one variable per sweep. Attribute the change to one displayed equation rather than to visual resemblance.

## Intentionally broken case

Broken mode sends degree values directly to sine and cosine, so the named path components no longer match the declared heading even though a self-consistent inverse can look plausible. The broken case is an invalid counterexample, not an alternate tire calibration.

## Recovery

Convert every declared degree angle exactly once at the frame boundary, then verify both the expected path components and the rotation norm invariant. Recovery restores the exact baseline inputs and must restore the baseline signature.

## Limiting cases and invariants

- At zero path heading the path and inertial axes coincide.
- At zero wheel steer the wheel and body velocity components coincide.

Teaching invariant: A proper planar rotation preserves speed norm, and a transform followed by its inverse recovers the original vector in the same angle unit.

## Independent evidence

Expected signatures come from `expansion_reference_cases.py`, which imports no production experiment, consumes no production result, and perturbs no production value. Baseline, two one-variable sweeps, broken behavior, and exact recovery are retained separately. Agreement covers only these equations and bounded deterministic scenarios.

## Common mistakes

- Mixing active vector rotation with passive coordinate transformation.
- Checking only a round trip that repeats the same wrong angle convention.
- Calling wheel lateral velocity a force or slip angle without the sign convention.
- Treating deterministic synthetic observations as measured tire, rig, track, or vehicle evidence.
- Extending this bounded teaching model beyond its stated validity range.

## Formative checks

- Why does a correct rotation preserve speed magnitude?
- Which residual catches degrees passed to trigonometric functions?
- Which plotted quantity would first reveal the named broken behavior?
- What evidence would still be required before using this relation for physical setup decisions?

## Teach-back

Derive one signature quantity from the displayed equations, explain exactly which invariant the broken case violates, and distinguish the model's software evidence from a measured tire validation claim.
