# Validate a Tire Model with Uncertainty

**Guiding question:** When does a small residual become statistically inconsistent with the uncertainty claimed by a tire model?

Fit on deterministic synthetic training data and judge held-out bias, RMSE, normalized residuals, and interval coverage. This is a competency-derived Python-first native design. It is not a source conversion, MATLAB-runtime comparison, rig test, track test, or measured-vehicle result.

## Why this lesson exists

The 24 source-bound lessons establish the surface workflow. This depth lesson requires a governing tire relation, a falsifiable invariant, a named failure, and independent evidence. State the frame, sign, unit, and synthetic-data assumptions before reading any curve.

## Model and equations

- `theta_hat=argmin sum_train(y-theta*x)^2`
- `r_i=y_i-theta_hat*x_i`
- `z_i=r_i/sigma`
- `coverage=mean(|z_i|<=1.96)`

All angles cross a labeled degree-to-radian boundary before trigonometric use. Longitudinal force is positive forward, lateral force follows the lesson's displayed convention, normal load is positive into the contact patch, and dissipated energy is nonnegative.

## Predict before running

Model fitting uses training rows only, and held-out residual coverage is interpreted against the same declared observation uncertainty. Predict the direction of every signature change before moving a control.

## Baseline workflow

1. Run the defaults with broken mode disabled.
2. Read all signature metrics and their physical units.
3. Compare the response plot with the mechanism plot.
4. Check both limiting cases before accepting the interpretation.
5. Save the baseline so recovery can be compared exactly.

## Two one-variable sweeps

1. Hold validation fraction at 0.35 and sweep declared sigma from 20 to 250 N.
2. Restore sigma to 80 N and sweep the held-out fraction from 0.20 to 0.60.

Change only one variable per sweep. Attribute the change to one displayed equation rather than to visual resemblance.

## Intentionally broken case

Broken mode fits on all rows and reports only one fifth of the declared uncertainty, combining validation leakage with visibly under-covered prediction intervals. The broken case is an invalid counterexample, not an alternate tire calibration.

## Recovery

Restore the train/validation boundary, use the declared positive sigma unchanged, and recompute held-out bias, RMSE, normalized residuals, and coverage. Recovery restores the exact baseline inputs and must restore the baseline signature.

## Limiting cases and invariants

- With zero residual every held-out point is covered by any positive interval.
- As declared uncertainty shrinks, normalized residual magnitude grows for unchanged observations.

Teaching invariant: Model fitting uses training rows only, and held-out residual coverage is interpreted against the same declared observation uncertainty.

## Independent evidence

Expected signatures come from `expansion_reference_cases.py`, which imports no production experiment, consumes no production result, and perturbs no production value. Baseline, two one-variable sweeps, broken behavior, and exact recovery are retained separately. Agreement covers only these equations and bounded deterministic scenarios.

## Common mistakes

- Fitting or tuning on held-out rows.
- Reporting RMSE without a declared noise scale.
- Treating nominal interval width as observed coverage.
- Treating deterministic synthetic observations as measured tire, rig, track, or vehicle evidence.
- Extending this bounded teaching model beyond its stated validity range.

## Formative checks

- Why must the validation rows stay out of the fit?
- What happens to normalized residuals when sigma is underreported?
- Which plotted quantity would first reveal the named broken behavior?
- What evidence would still be required before using this relation for physical setup decisions?

## Teach-back

Derive one signature quantity from the displayed equations, explain exactly which invariant the broken case violates, and distinguish the model's software evidence from a measured tire validation claim.
