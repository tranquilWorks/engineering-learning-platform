# Adapt a Parameter Estimate Online

Recursive least squares updates a parameter estimate using each regressor and prediction residual. The experiment uses theta_true=1, theta_0=0 and P_0=10, with 200 samples over ten seconds. P is the RLS inverse-information scale; without a calibrated measurement-noise model it is not a certified probabilistic interval.

## Model and equations

\[
g_k=\frac{P_{k-1}\phi_k}{\lambda+\phi_k^2P_{k-1}},\qquad P_k=\frac{P_{k-1}-g_k\phi_kP_{k-1}}{\lambda}
\]

`g[k]=P[k-1]*phi[k]/(lambda+phi[k]^2*P[k-1])`

`theta[k]=theta[k-1]+g[k]*(y[k]-phi[k]*theta[k-1])`

`P[k]=(P[k-1]-g[k]*phi[k]*P[k-1])/lambda`

Worked example: For lambda=0.98 and a zero regressor, gain is zero: the estimate cannot learn. The correct covariance becomes P/0.98, so uncertainty increases. Multiplying by 0.98 would report shrinking uncertainty without any information.

## Baseline workflow

What should happen to covariance when excitation vanishes and lambda<1? Decide before enabling the broken case.

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. Recursive parameter estimate displays each computed update and known truth. Covariance and missing excitation compares reported P with the correct zero-excitation evolution. Information rate is the actual sum of squared regressors divided by ten seconds.

The covariance axis is logarithmic because excited and unexcited information scales can differ by many orders of magnitude.

## Two one-variable sweeps

Increase forgetting factor from 0.98 to 1 and compare retained information and parameter error. Reset, then raise excitation level from 0.8 to 2: inspect covariance and measured information rate rather than assuming a fixed error formula.

## Intentionally broken case

Broken mode sets the actual regressor to zero and uses the incorrect covariance update lambda*P. The parameter stays at zero while the reported covariance shrinks for lambda<1. The selected forgetting factor remains active.

## Recovery

Restore excitation and the correct covariance recurrence, then reset the controls. Check estimate motion is accompanied by nonzero regressors and actual information accumulation.

## Limiting cases and invariants

- At lambda=1, recursive estimates match regularized batch least squares with prior information 1/P0.
- For zero regressor the correct estimate is unchanged and P cannot shrink when lambda<=1.
- The deterministic disturbance is explicitly 0.01*sin(0.73*k); observed error is not a statistical convergence guarantee.

## Independent evidence

An independent exponentially weighted batch normal equation computes the final estimate and inverse information, without replaying the production covariance recurrence. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

A decreasing covariance curve is not proof of learning. Examine regressors, gains and estimation error together.

## Teach-back

At lambda=1, why does the broken covariance no longer shrink, and why is the estimate still wrong?

Answer rationale: Multiplication by one leaves P fixed, so this particular false-confidence symptom disappears. The zero regressor still gives zero gain and no information, leaving theta=0 instead of the true value one.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
