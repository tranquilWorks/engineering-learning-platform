# Identify Parameters from a Real Drive

> **Guiding question:** What excitation, residual, and uncertainty evidence is required before coastdown parameters are identifiable?

## Physical model, synthetic data, and units

The exact source title is retained, but this implementation deliberately uses a deterministic **synthetic offline stand-in**, not a real drive. Twelve speeds span a selected interval above 10 m/s. Synthetic resistive force follows `F = F_roll + 0.5 rho CdA v² + e`, with `rho = 1.225 kg/m³`, truth `F_roll = 180 N`, truth `CdA = 0.64 m²`, and a fixed zero-randomness disturbance pattern scaled in newtons.

Writing `x = v²` makes the model affine: intercept is rolling resistance and slope is `0.5 rho CdA`. Even-index samples form training data; odd-index samples remain validation data. The evidence includes training and validation RMSE, speed-squared span, an excitation ratio, and slope-derived drag-area standard error.

This Python-first native P20 model derives from a scaffold. It is not source- or MATLAB-runtime equivalence, measured telemetry, or proof that the same estimator works on an actual vehicle.

## Predict and sweep one variable at a time

1. Hold the deterministic force disturbance at 20 N and widen speed span from 2 to 20 to 25 m/s. Predict how regressor leverage changes drag-area uncertainty.
2. Restore the 20 m/s span and scale disturbance from 0 to 20 to 100 N. Predict training residual, validation residual, and parameter error.

A low residual at one speed cannot separate intercept from slope. Identification needs excitation as well as fit quality.

## Named broken behavior and exact recovery

**Broken behavior:** collapse every training regressor to the same speed-squared value. The least-squares denominator becomes zero, drag slope is unidentifiable, and validation error exposes the failed generalization. The model returns a finite intercept and explicit invalid flag rather than dividing by zero.

**Exact recovery:** restore the 20 m/s synthetic speed span, alternating train/validation split, and correct `v²` regressor. With the 20 N disturbance the exact baseline signature returns.

## Limits and limiting cases

At zero disturbance, the affine parameters are recovered to numerical tolerance. With a narrow but nonzero span, the fit exists but becomes disturbance-sensitive. The model assumes level road, known air density, no wind, constant rolling force, exact speed, and no drivetrain torque. It omits sensor calibration, grade, temperature, tire pressure, covariance validity, and real-drive preprocessing.

## Common mistakes

- Regressing force on speed rather than speed squared.
- Reporting training residual without held-out validation.
- Calling a full-rank calculation well-conditioned without an excitation metric.
- Treating deterministic synthetic samples as measured road data.
- Using the retained title as evidence that a real drive occurred.

## Formative checks

1. Derive `CdA = 2*slope/rho` and its units.
2. Explain why alternating samples remain independent of the fit calculation.
3. Predict the zero-disturbance limiting result.
4. Diagnose the collapsed-regressor failure from denominator and validation residual.

## Teach-back checklist

- [ ] I can separate parameter identifiability from small residuals.
- [ ] I predicted both one-variable sweeps.
- [ ] I can explain train/validation separation.
- [ ] I diagnosed the named broken behavior and exact recovery.
- [ ] I can state that no real drive or measured vehicle data was used.

This is not measured-vehicle, real-drive, browser/learner, firmware, radio, bench, track, hardware/HIL, certification, release, or production evidence.
