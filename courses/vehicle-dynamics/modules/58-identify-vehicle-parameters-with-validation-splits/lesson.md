# Identify Vehicle Parameters with Validation Splits

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It identifies two synthetic stiffness parameters from a deterministic force sequence.

## Model and equations

- `F_y=X[C_front,C_rear]^T+epsilon`
- `theta_hat=argmin_theta ||X_train theta-y_train||_2`
- `RMSE_validation=sqrt(mean((X_validation theta_hat-y_validation)^2))`

Rows are ordered in time. The first contiguous block is training data and the later block remains unavailable to the fit until validation.

## Baseline workflow

Construct front and rear slip regressors, add deterministic force disturbance, freeze a chronological split, estimate two stiffnesses on training rows, and compute training and held-out RMSE separately.

## Two one-variable sweeps

Increase only training fraction, then increase only force disturbance. The first trades validation length for training support; the second tests sensitivity to observation quality.

## Intentionally broken case

Fit all timestamps, including future validation rows, then copy training RMSE into the validation field. The leakage counter records the compromised samples.

## Recovery

Choose the time boundary before fitting, isolate arrays, estimate only on training rows, freeze parameters, and score untouched future rows with the same units and residual definition.

## Limiting cases and invariants

- More training data means fewer independent future validation samples.
- Zero disturbance with full-rank regressors recovers the declared parameters.
- A validation score is invalid if its rows influenced the fitted parameters.

## Independent evidence

A separate chronological least-squares formulation reproduces parameter, error, sample-count, and leakage signatures.

## Common mistakes

- Randomly mixing time-correlated rows across the split.
- Normalizing with statistics computed from the full dataset.
- Reporting training error as validation performance.

## Formative checks

1. Why is chronological splitting appropriate here?
2. Which retained metric makes leakage explicit?

## Teach-back

Explain the regressor, two parameters, chronological split, fit and score domains, leakage failure, and exact recovery.
