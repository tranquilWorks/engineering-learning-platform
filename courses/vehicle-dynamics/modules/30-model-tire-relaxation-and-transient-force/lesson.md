# Model Tire Relaxation and Transient Force

**Guiding question:** Why is tire-force lag naturally a distance-domain effect even when data are timestamped?

Relate relaxation length, vehicle speed, time constant, and the 63-percent transient-force distance. This is a competency-derived Python-first native design. It is not a source conversion, MATLAB-runtime comparison, rig test, track test, or measured-vehicle result.

## Why this lesson exists

The 24 source-bound lessons establish the surface workflow. This depth lesson requires a governing tire relation, a falsifiable invariant, a named failure, and independent evidence. State the frame, sign, unit, and synthetic-data assumptions before reading any curve.

## Model and equations

- `dF/ds=(F_ss-F)/sigma`
- `tau=sigma/v`
- `F(s)=F_ss*(1-exp(-s/sigma))`

All angles cross a labeled degree-to-radian boundary before trigonometric use. Longitudinal force is positive forward, lateral force follows the lesson's displayed convention, normal load is positive into the contact patch, and dissipated energy is nonnegative.

## Predict before running

A first-order tire reaches one minus e to the minus one of steady force after one relaxation length, while the time constant scales inversely with speed. Predict the direction of every signature change before moving a control.

## Baseline workflow

1. Run the defaults with broken mode disabled.
2. Read all signature metrics and their physical units.
3. Compare the response plot with the mechanism plot.
4. Check both limiting cases before accepting the interpretation.
5. Save the baseline so recovery can be compared exactly.

## Two one-variable sweeps

1. Hold speed at 20 m/s and sweep relaxation length from 0.10 to 1.50 m.
2. Restore 0.45 m and sweep speed from 2 to 60 m/s.

Change only one variable per sweep. Attribute the change to one displayed equation rather than to visual resemblance.

## Intentionally broken case

Broken mode treats relaxation length in meters as a time constant in seconds, omitting the speed conversion and moving the 63-percent distance by a factor of speed. The broken case is an invalid counterexample, not an alternate tire calibration.

## Recovery

Use tau equals relaxation length divided by speed, then check both the one-length force fraction and the speed-invariant response distance. Recovery restores the exact baseline inputs and must restore the baseline signature.

## Limiting cases and invariants

- As relaxation length tends to zero the force approaches the steady law immediately.
- At fixed relaxation length, speed changes response time but not response distance.

Teaching invariant: A first-order tire reaches one minus e to the minus one of steady force after one relaxation length, while the time constant scales inversely with speed.

## Independent evidence

Expected signatures come from `expansion_reference_cases.py`, which imports no production experiment, consumes no production result, and perturbs no production value. Baseline, two one-variable sweeps, broken behavior, and exact recovery are retained separately. Agreement covers only these equations and bounded deterministic scenarios.

## Common mistakes

- Using relaxation length directly as seconds.
- Comparing timestamp response without accounting for speed.
- Calling a steady-state force law a transient tire model.
- Treating deterministic synthetic observations as measured tire, rig, track, or vehicle evidence.
- Extending this bounded teaching model beyond its stated validity range.

## Formative checks

- What force fraction occurs at one relaxation length?
- Which quantity stays fixed when speed changes: response time or response distance?
- Which plotted quantity would first reveal the named broken behavior?
- What evidence would still be required before using this relation for physical setup decisions?

## Teach-back

Derive one signature quantity from the displayed equations, explain exactly which invariant the broken case violates, and distinguish the model's software evidence from a measured tire validation claim.
