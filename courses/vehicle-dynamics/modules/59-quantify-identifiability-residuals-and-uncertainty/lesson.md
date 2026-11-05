# Quantify Identifiability, Residuals, and Uncertainty

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. Its design matrix, force disturbance, and parameter truth are deterministic synthetic values.

## Model and equations

- `kappa(X)=sigma_max(X)/sigma_min(X)`
- `r=y-X theta_hat`
- `Cov(theta_hat)=sigma_force^2 pinv(X^T X)`

Singular values describe parameter separation, residuals test model structure, and covariance combines design geometry with the declared observation-noise scale.

## Baseline workflow

Build the two-column design matrix, solve by least squares, inspect condition number and smallest singular value, compute residual RMS and lag-one correlation, then propagate force variance into parameter intervals and truth containment.

## Two one-variable sweeps

Reduce only maneuver excitation, then increase only force-noise sigma. Excitation changes design singular values; noise scale changes parameter uncertainty without changing matrix conditioning.

## Intentionally broken case

Use an unscaled normal-equation inverse and declare one tenth of the actual observation sigma. The fit is unchanged while intervals narrow, truth containment falls, and the covariance ledger no longer closes.

## Recovery

Use an SVD-based least-squares solve, expose singular values, retain residual correlation, propagate the declared physical variance, and test whether intervals cover known synthetic truth.

## Limiting cases and invariants

- Lower excitation lowers singular values and enlarges uncertainty.
- Noise scale does not change the noiseless design condition number.
- Small residual RMS cannot rescue a rank-deficient design.

## Independent evidence

An independent design, fit, residual, QR covariance, and containment calculation reproduces every signature.

## Common mistakes

- Treating fit error as identifiability.
- Ignoring correlated residuals.
- Reporting covariance without the variance scale used to compute it.

## Formative checks

1. Which diagnostic reveals nearly dependent regressors?
2. Why can the point estimate stay fixed while truth containment changes?

## Teach-back

Explain singular values, residual structure, covariance scaling, truth containment, understated-noise failure, and recovery.


## Detailed model audit

Production computes conditional covariance from the SVD X=U*S*V transpose as sigma²*V*S^(-2)*V transpose. The independent reference uses QR triangular solves. Both avoid forming normal equations for the healthy branch; the intentionally broken branch retains the normal-equation inverse and understates sigma. The displayed containment statistic checks just two known synthetic coefficients against their conditional 1.96-standard-error intervals. It is not an empirical coverage probability. Residual lag correlation explicitly challenges the independent-noise assumption behind those intervals; a narrow band cannot override that limitation.
