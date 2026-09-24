# Quantify Identifiability, Residuals, and Uncertainty

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. Its design matrix, force disturbance, and parameter truth are deterministic synthetic values.

## Model and equations

- `kappa(X)=sigma_max(X)/sigma_min(X)`
- `r=y-X theta_hat`
- `Cov(theta_hat)=sigma_force^2 pinv(X^T X)`

Singular values describe parameter separation, residuals test model structure, and covariance combines design geometry with the declared observation-noise scale.

## Baseline workflow

Build the two-column design matrix, solve by least squares, inspect condition number and smallest singular value, compute residual RMS and lag-one correlation, then propagate force variance into parameter intervals and coverage.

## Two one-variable sweeps

Reduce only maneuver excitation, then increase only force-noise sigma. Excitation changes design singular values; noise scale changes parameter uncertainty without changing matrix conditioning.

## Intentionally broken case

Use an unscaled normal-equation inverse and declare one tenth of the actual observation sigma. The fit is unchanged while intervals narrow, coverage falls, and the covariance ledger no longer closes.

## Recovery

Use an SVD-based least-squares solve, expose singular values, retain residual correlation, propagate the declared physical variance, and test whether intervals cover known synthetic truth.

## Limiting cases and invariants

- Lower excitation lowers singular values and enlarges uncertainty.
- Noise scale does not change the noiseless design condition number.
- Small residual RMS cannot rescue a rank-deficient design.

## Independent evidence

An independent design, fit, residual, pseudoinverse, and coverage calculation reproduces every signature.

## Common mistakes

- Treating fit error as identifiability.
- Ignoring correlated residuals.
- Reporting covariance without the variance scale used to compute it.

## Formative checks

1. Which diagnostic reveals nearly dependent regressors?
2. Why can the point estimate stay fixed while coverage changes?

## Teach-back

Explain singular values, residual structure, covariance scaling, coverage, understated-noise failure, and recovery.
