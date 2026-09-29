# Transform Gaussian Uncertainty with Sigma Points

The unscented transform propagates selected points through a nonlinear map, then combines the transformed points with specified weights. This lesson executes that component of an unscented Kalman filter; it does not perform recursive state prediction, measurement assimilation or a complete UKF.

## Model and equations

\[
\bar y=\sum_i W_i^{(m)}f(\chi_i),\qquad P_y=\sum_i W_i^{(c)}(f(\chi_i)-\bar y)^2
\]

`x~N(0,sigma^2); y=x^2; E[y]=sigma^2; Var[y]=2*sigma^4`

`points=[0,+alpha*sigma,-alpha*sigma]; Wm=[1-alpha^-2,1/(2*alpha^2),1/(2*alpha^2)]`

`Wc0=Wm0+1-alpha^2+beta, beta=2; mean=sum(Wm*y); variance=sum(Wc*(y-mean)^2)`

Worked example: At sigma=0.8 and alpha=1, points are 0 and ±0.8. Mean weights are [0,0.5,0.5], while covariance weights are [2,0.5,0.5]. Squaring gives mean 0.64 and variance 2*(0.8)^4=0.8192. Covariance weights sum to three, not one.

## Baseline workflow

Does a negative central mean weight necessarily invalidate the transform? Try alpha below one and compare the computed moments with the Gaussian formulas.

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. Actual sigma-point transform displays the nonlinear curve and the three transformed points. Weighted variance contributions shows what each point adds to the covariance calculation. The metrics expose computed moments, their errors, minimum mean weight and covariance-weight sum.

## Two one-variable sweeps

Increase state standard deviation from 0.8 to 2: mean scales as sigma² and variance as sigma⁴. Reset, then move sigma spread from 1 to 2 and down to 0.2: point positions and weights change, while the healthy quadratic moments stay exact within roundoff.

## Intentionally broken case

Broken mode omits the Gaussian covariance correction and reuses mean weights for covariance. Mean remains correct, but variance becomes (alpha²−1)*sigma⁴: zero at alpha=1 and negative for alpha<1.

## Recovery

Restore the beta=2 covariance correction and reset both controls. Check both computed moments against analytic Gaussian values; do not reject a transform solely because its central mean weight is negative.

## Limiting cases and invariants

- Mean weights sum to one; covariance weights generally do not.
- Symmetric points reconstruct zero input mean and variance sigma².
- Exactness here concerns a zero-mean Gaussian squared map, not every nonlinear function or a full recursive UKF.

## Independent evidence

Independent Gaussian second/fourth moments and the closed-form missing-correction error check the actual weighted production calculation. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

Renormalizing covariance weights as if they were probabilities changes the transform. Negative mean weights alone are not a fault criterion.

## Teach-back

At alpha=1, why does removing the central covariance correction leave the mean correct but reduce variance to zero?

Answer rationale: The two off-center transformed values equal the mean, so their variance contributions vanish. The center maps to zero, differs from mean by sigma² and contributes 2*sigma⁴ only through the covariance correction. Its mean weight is zero.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
